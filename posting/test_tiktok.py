"""Tests for the TikTok (Buffer) posting path, against a local mock of Buffer's GraphQL API.
No network, no secrets:  python3 posting/test_tiktok.py
"""

import io
import json
import os
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import buffer  # noqa: E402
import post  # noqa: E402
import tiktok_post  # noqa: E402

EPISODE = {
    "number": 14, "title": "Give Every Nation a Different Definition of Honor",
    "metadata": {"tiktok": {
        "caption": "She broke her oath. Hero or traitor? #Worldbuilding #FantasyWriting #WritingTips",
        "pinnedComment": "Freedom or responsibility?"}},
}


class MockBuffer:
    """Answers the handful of GraphQL operations buffer.py sends. Scripted per test."""

    def __init__(self):
        self.requests = []
        self.channels = [{"id": "ch-tt", "name": "worldcraft", "displayName": None, "service": "tiktok",
                          "isDisconnected": False, "isLocked": False, "isQueuePaused": False},
                         {"id": "ch-ig", "name": "worldcraft", "displayName": None, "service": "instagram",
                          "isDisconnected": False, "isLocked": False, "isQueuePaused": False}]
        self.existing_posts = []
        self.create_results = []      # popped per createPost: "ok" or an error message
        self.status_sequence = {}     # post id -> statuses returned by successive post() polls
        self.reject_auth = False

    def handle(self, body, auth):
        self.requests.append(body)
        if self.reject_auth or auth != "Bearer test-key":
            return 401, {"errors": [{"message": "Access token is not valid",
                                     "extensions": {"code": "UNAUTHENTICATED"}}]}
        q, v = body["query"], body.get("variables", {})
        if "account" in q:
            return 200, {"data": {"account": {"organizations": [{"id": "org1", "name": "Mine"}]}}}
        if "channels(" in q:
            return 200, {"data": {"channels": self.channels}}
        if "posts(" in q:
            return 200, {"data": {"posts": {"edges": [{"node": p} for p in self.existing_posts]}}}
        if "createPost" in q:
            result = self.create_results.pop(0) if self.create_results else "ok"
            if result != "ok":
                return 200, {"data": {"createPost": {"__typename": "InvalidInputError", "message": result}}}
            pid = f"post{len([r for r in self.requests if 'createPost' in r['query']])}"
            self.status_sequence.setdefault(pid, ["sending", "sent"])
            return 200, {"data": {"createPost": {"__typename": "PostActionSuccess", "post": self._post(pid, "scheduled")}}}
        if "post(input" in q:
            pid = v["in"]["id"]
            seq = self.status_sequence[pid]
            status = seq.pop(0) if len(seq) > 1 else seq[0]
            return 200, {"data": {"post": self._post(pid, status)}}
        return 200, {"errors": [{"message": f"unexpected query {q[:60]}"}]}

    @staticmethod
    def _post(pid, status):
        return {"id": pid, "status": status, "text": "", "dueAt": None, "sentAt": None,
                "externalLink": "https://www.tiktok.com/@worldcraft/video/1" if status == "sent" else None,
                "error": {"message": "Video could not be fetched", "supportUrl": None} if status == "error" else None}

    def creates(self):
        return [r["variables"]["in"] for r in self.requests if "createPost" in r["query"]]


class TikTokTests(unittest.TestCase):
    def setUp(self):
        self.mock = MockBuffer()
        m = self.mock

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                code, payload = m.handle(body, self.headers.get("Authorization"))
                data = json.dumps(payload).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *a):
                pass

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

        self.tmp = Path(tempfile.mkdtemp())
        self.state_path = self.tmp / "tiktok_state.json"
        self.state_path.write_text(json.dumps({"hold": [], "posted": {}}))
        self.episode_path = self.tmp / "episode.json"
        self.episode_path.write_text(json.dumps(EPISODE))

        env = {"BUFFER_API_KEY": "test-key", "BUFFER_API_URL": f"http://127.0.0.1:{self.server.server_port}",
               "GITHUB_STEP_SUMMARY": str(self.tmp / "summary.md")}
        os.environ.pop("BUFFER_CHANNEL_ID", None)
        self.patches = [mock.patch.dict(os.environ, env),
                        mock.patch.object(tiktok_post, "STATE_PATH", self.state_path),
                        mock.patch.object(tiktok_post, "resolve", lambda u: u + "?signed=1"),
                        mock.patch.object(buffer.time, "sleep", lambda s: None)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.server.shutdown()

    def publish(self, dry_run=False):
        args = mock.Mock(episode_json=str(self.episode_path), dry_run=dry_run,
                         video_url="https://github.com/o/r/releases/download/videos/ep14.mp4")
        out = io.StringIO()
        with redirect_stdout(out):
            tiktok_post.cmd_publish(args)
        return out.getvalue()

    def state(self):
        return json.loads(self.state_path.read_text())

    # ── publishing ──
    def test_publishes_with_ai_label_and_records_state(self):
        self.publish()
        (create,) = self.mock.creates()
        self.assertEqual(create["channelId"], "ch-tt")
        self.assertEqual(create["mode"], "shareNow")
        self.assertEqual(create["schedulingType"], "automatic")
        self.assertIs(create["needsApproval"], False)
        self.assertIs(create["metadata"]["tiktok"]["isAiGenerated"], True)
        self.assertEqual(create["assets"], [{"video": {"url": "https://github.com/o/r/releases/download/videos/ep14.mp4"}}])
        self.assertIn("Episode 14 · Give Every Nation", create["text"])
        rec = self.state()["posted"]["ep14"]
        self.assertEqual(rec["status"], "sent")
        self.assertEqual(rec["link"], "https://www.tiktok.com/@worldcraft/video/1")
        summary = (self.tmp / "summary.md").read_text()
        self.assertIn("Pin this comment by hand", summary)
        self.assertIn("Freedom or responsibility?", summary)

    def test_duplicate_guard_records_instead_of_reposting(self):
        self.mock.existing_posts = [{"id": "old", "status": "sent", "text": "x\n\nEpisode 14 · Give\n\n#a",
                                     "dueAt": None, "sentAt": "2026-11-01T18:00:00.000Z",
                                     "externalLink": "https://www.tiktok.com/@w/video/9", "error": None}]
        self.publish()
        self.assertEqual(self.mock.creates(), [])
        rec = self.state()["posted"]["ep14"]
        self.assertEqual((rec["buffer_post_id"], rec["posted_at"]), ("old", "2026-11-01T18:00:00+00:00"))

    def test_episode_1_marker_does_not_match_episode_14(self):
        EP1 = dict(EPISODE, number=1)
        self.episode_path.write_text(json.dumps(EP1))
        self.mock.existing_posts = [{"id": "old", "status": "sent", "text": "Episode 14 · x", "dueAt": None,
                                     "sentAt": None, "externalLink": None, "error": None}]
        self.publish()
        self.assertEqual(len(self.mock.creates()), 1)

    def test_rejected_url_is_retried_with_resolved_url(self):
        self.mock.create_results = ["Media URL could not be fetched"]
        out = self.publish()
        first, second = self.mock.creates()
        self.assertEqual(second["assets"][0]["video"]["url"], first["assets"][0]["video"]["url"] + "?signed=1")
        self.assertIn("retrying with the resolved download URL", out)
        self.assertIn("ep14", self.state()["posted"])

    def test_failed_publish_raises_and_leaves_state_untouched(self):
        self.mock.status_sequence = {"post1": ["error"], "post2": ["error"]}
        with self.assertRaisesRegex(buffer.BufferError, "Video could not be fetched"):
            self.publish()
        self.assertEqual(self.state()["posted"], {})

    def test_timeout_is_not_retried(self):
        self.mock.status_sequence = {"post1": ["sending"]}
        clock = mock.Mock(time=mock.Mock(side_effect=[0] + [10_000] * 10), sleep=lambda s: None)
        with mock.patch.object(buffer, "time", clock):  # only buffer.py's clock, not the mock server's
            with self.assertRaises(TimeoutError):
                self.publish()
        self.assertEqual(len(self.mock.creates()), 1)

    def test_dry_run_publishes_nothing(self):
        out = self.publish(dry_run=True)
        self.assertEqual(self.mock.creates(), [])
        self.assertIn("will post to TikTok channel worldcraft", out)
        self.assertEqual(self.state()["posted"], {})

    def test_dry_run_without_key_skips_buffer(self):
        with mock.patch.dict(os.environ, {"BUFFER_API_KEY": ""}):
            out = self.publish(dry_run=True)
        self.assertIn("BUFFER_API_KEY not set", out)
        self.assertEqual(self.mock.requests, [])

    # ── channel selection and errors ──
    def test_several_tiktok_channels_need_explicit_id(self):
        self.mock.channels.append(dict(self.mock.channels[0], id="ch-tt2", name="other"))
        with self.assertRaisesRegex(buffer.BufferError, "BUFFER_CHANNEL_ID"):
            self.publish()
        with mock.patch.dict(os.environ, {"BUFFER_CHANNEL_ID": "ch-tt2"}):
            self.publish()
        self.assertEqual(self.mock.creates()[0]["channelId"], "ch-tt2")

    def test_disconnected_channel_fails_clearly(self):
        self.mock.channels[0]["isDisconnected"] = True
        with self.assertRaisesRegex(buffer.BufferError, "reconnect"):
            self.publish()

    def test_no_tiktok_channel(self):
        self.mock.channels = self.mock.channels[1:]
        with self.assertRaisesRegex(buffer.BufferError, "no TikTok channel"):
            self.publish()

    def test_bad_key_message(self):
        self.mock.reject_auth = True
        with self.assertRaisesRegex(buffer.BufferError, "rejected the API key"):
            self.publish()


class CaptionAndSelectTests(unittest.TestCase):
    def test_caption_layout_and_limit(self):
        cfg = post.load(post.CONFIG_PATH)
        cap = tiktok_post.build_caption(cfg, EPISODE)
        self.assertEqual(cap, "She broke her oath. Hero or traitor?\n\nEpisode 14 · Give Every Nation a Different "
                              "Definition of Honor\n\n#Worldbuilding #FantasyWriting #WritingTips")
        long = dict(EPISODE, metadata={"tiktok": {"caption": "😀" * 1101}})  # 2202 UTF-16 units
        with self.assertRaises(ValueError):
            tiktok_post.build_caption(cfg, long)

    def test_caption_falls_back_to_title_and_default_tags(self):
        cap = tiktok_post.build_caption(post.load(post.CONFIG_PATH), dict(EPISODE, metadata={}))
        self.assertTrue(cap.startswith("Give Every Nation"))
        self.assertTrue(cap.endswith("#worldbuilding #fantasywriting #writingtok"))

    def test_select_uses_tiktok_state_and_start_episode(self):
        cfg = tiktok_post.tiktok_cfg(post.load(post.CONFIG_PATH))
        branches = {f"claude/worldcraft-ep{i:02d}" for i in range(2, 26)}
        with mock.patch.object(post, "remote_branches", lambda: branches), \
                mock.patch.object(post, "unfinished", lambda b, e: None):
            empty = {"hold": [], "posted": {}}
            self.assertEqual(post.pick(cfg, empty, first=cfg["startEpisode"])["episode"], "ep14")
            done14 = {"hold": ["ep15"], "posted": {"ep14": {"posted_at": "2020-01-01T00:00:00+00:00"}}}
            self.assertEqual(post.pick(cfg, done14, first=14)["episode"], "ep16")
            recent = {"hold": [], "posted": {"ep14": {"posted_at": post.now_utc().isoformat()}}}
            self.assertEqual(post.pick(cfg, recent, first=14)["go"], "false")
            # Instagram's start is untouched: with an empty state it still wants EP01 (which has no branch).
            ig = post.pick(post.load(post.CONFIG_PATH), {"hold": [], "posted": {}})
            self.assertEqual(ig["go"], "false")
            self.assertIn("ep01 is next", ig["reason"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
