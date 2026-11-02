#!/usr/bin/env python3
"""TikTok posting for Worldcraft Shorts, through Buffer (see posting/TIKTOK.md).

  tiktok_post.py select   [--episode epNN] [--force]     which episode goes out next (writes GITHUB_OUTPUT)
  tiktok_post.py caption  --episode-json PATH             print the caption that would be posted
  tiktok_post.py check                                    verify the Buffer key and TikTok channel (read-only)
  tiktok_post.py publish  --episode-json PATH --video-url URL [--dry-run]

TikTok's posted-state lives in posting/tiktok_state.json, separate from Instagram's state.json.
Settings are under "tiktok" in posting/config.json. The workflow .github/workflows/tiktok-post.yml
runs these commands.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from post import CONFIG_PATH, ep_id, episode_marker, load, now_utc, pick, resolve, set_output  # noqa: E402

STATE_PATH = HERE / "tiktok_state.json"
MAX_CAPTION = 2200  # TikTok and Buffer both count UTF-16 code units for video captions


def tiktok_cfg(cfg):
    """The shared config with TikTok's own overrides (start episode, gap) on top."""
    return {**cfg, **cfg["tiktok"]}


def save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def utf16_len(s):
    return len(s.encode("utf-16-le")) // 2


def summary(text):
    print(text)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(text + "\n")


# ── caption ──────────────────────────────────────────────────────────────

def build_caption(cfg, episode):
    """episode.json → metadata.tiktok.caption, with an "Episode N · Title" line before the hashtags.
    That line matches Instagram's and is what the duplicate check looks for."""
    c = cfg["tiktok"]["caption"]
    source = episode.get("metadata", {}).get("tiktok", {}).get("caption", "").strip()
    body = re.sub(r"\s*#\w+", "", source).strip() or episode["title"]

    tags, seen = [], set()
    for t in re.findall(r"#\w+", source) or c["fallbackHashtags"]:
        if t.lower() not in seen:
            seen.add(t.lower())
            tags.append(t)
    tags = tags[: c["maxHashtags"]]

    caption = c["template"].format(text=body, number=episode["number"], title=episode["title"],
                                   hashtags=" ".join(tags)).strip()
    if utf16_len(caption) > MAX_CAPTION:
        raise ValueError(f"caption is {utf16_len(caption)} UTF-16 units; TikTok allows {MAX_CAPTION}")
    return caption


# ── commands ─────────────────────────────────────────────────────────────

def cmd_select(args):
    cfg = tiktok_cfg(load(CONFIG_PATH))
    set_output(**pick(cfg, load(STATE_PATH), args.episode, args.force, first=cfg["startEpisode"]))


def cmd_caption(args):
    print(build_caption(load(CONFIG_PATH), load(Path(args.episode_json))))


def cmd_check(_args):
    from buffer import Client

    buf = Client()
    for org in buf.organizations():
        print(f"[check] organization {org['name']} ({org['id']})")
        for ch in buf.channels(org["id"]):
            flags = [f for f in ("isDisconnected", "isLocked", "isQueuePaused") if ch.get(f)]
            print(f"[check]   {ch['service']:<10} {ch['name']} ({ch['id']}) {' '.join(flags)}".rstrip())
    org_id, ch = buf.tiktok_channel()
    print(f"[check] will post to TikTok channel {ch['name']} ({ch['id']})")
    return buf, org_id, ch


def cmd_publish(args):
    cfg, state = load(CONFIG_PATH), load(STATE_PATH)
    tcfg = cfg["tiktok"]
    episode = load(Path(args.episode_json))
    number = int(episode["number"])
    eid = ep_id(number)
    caption = build_caption(cfg, episode)
    pinned = episode.get("metadata", {}).get("tiktok", {}).get("pinnedComment")

    print(f"[tiktok] {eid}: {episode['title']}\n[tiktok] video: {args.video_url}")
    print(f"[tiktok] AI-generated label: {'on' if tcfg['aiLabel'] else 'off'}")
    print(f"[tiktok] caption ({utf16_len(caption)}/{MAX_CAPTION}):\n{caption}")

    if args.dry_run:
        print(f"[tiktok] video download resolves to {resolve(args.video_url).split('?')[0]}")
        if os.environ.get("BUFFER_API_KEY"):
            cmd_check(args)
        else:
            print("[tiktok] BUFFER_API_KEY not set: skipped the Buffer check")
        summary(f"### TikTok dry run: {eid}\nNothing was published.\n\n```\n{caption}\n```")
        return

    buf, org_id, ch = cmd_check(args)

    marker = episode_marker(number)
    for p in buf.recent_posts(org_id, ch["id"]):
        if marker.search(p.get("text") or ""):
            print(f"[tiktok] {eid} is already in Buffer as {p['status']} ({p['id']}); recording it, not reposting")
            state["posted"][eid] = {"by": "workflow", "buffer_post_id": p["id"], "status": p["status"],
                                    "link": p.get("externalLink"),
                                    "posted_at": (p.get("sentAt") or p.get("dueAt") or now_utc().isoformat())[:19] + "+00:00"}
            save_state(state)
            return

    def attempt(url):
        post = buf.create_tiktok_video(ch["id"], caption, url, ai_generated=tcfg["aiLabel"],
                                       thumbnail_offset_ms=tcfg.get("thumbnailOffsetMs"))
        print(f"[tiktok] Buffer post {post['id']} created ({post['status']})")
        return buf.wait_until_sent(post["id"])

    from buffer import BufferError
    try:
        post = attempt(args.video_url)
    except BufferError as e:
        # GitHub release links redirect to a signed storage URL. If Buffer won't follow the redirect,
        # retry once with the resolved URL; it stays valid for about an hour, and shareNow fetches at once.
        # (A timeout is not retried: the first post may still go out, and a retry could double-post.)
        print(f"::warning::first attempt failed ({e}); retrying with the resolved download URL")
        post = attempt(resolve(args.video_url))

    state["posted"][eid] = {"by": "workflow", "buffer_post_id": post["id"], "status": post["status"],
                            "link": post.get("externalLink"), "posted_at": now_utc().isoformat()}
    save_state(state)
    summary(f"### TikTok: posted {eid}\n{post.get('externalLink') or '(link not reported yet; check the TikTok app)'}")
    if pinned:
        summary(f"\nPin this comment by hand (TikTok's API can't post or pin comments):\n\n> {pinned}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("select")
    s.add_argument("--episode")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_select)
    s = sub.add_parser("caption")
    s.add_argument("--episode-json", required=True)
    s.set_defaults(fn=cmd_caption)
    s = sub.add_parser("check")
    s.set_defaults(fn=cmd_check)
    s = sub.add_parser("publish")
    s.add_argument("--episode-json", required=True)
    s.add_argument("--video-url", required=True)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_publish)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
