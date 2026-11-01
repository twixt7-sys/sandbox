"""Minimal Buffer GraphQL API client (stdlib only), used to publish to TikTok through Buffer.

Credentials come from the environment:
  BUFFER_API_KEY     personal API key from publish.buffer.com → Settings → API
  BUFFER_CHANNEL_ID  optional: the Buffer channel id of the TikTok account. If unset, the
                     account's only TikTok channel is used (and it's an error if there are several).
  BUFFER_API_URL     optional override of https://api.buffer.com

Docs: https://developers.buffer.com (createPost, posts, channels). GraphQL answers HTTP 200 even on
errors, so every call checks both the `errors` array and the typed MutationError result.
"""

import json
import os
import time
import urllib.error
import urllib.request

API_URL = "https://api.buffer.com"


class BufferError(RuntimeError):
    pass


class Client:
    def __init__(self, api_key=None, url=None):
        self.api_key = api_key or os.environ["BUFFER_API_KEY"]
        self.url = url or os.environ.get("BUFFER_API_URL") or API_URL

    def _call(self, query, variables=None):
        body = json.dumps({"query": query, "variables": variables or {}}).encode()
        req = urllib.request.Request(self.url, data=body, method="POST", headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                payload = json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            try:
                payload = json.loads(body)
            except ValueError:
                raise BufferError(f"HTTP {e.code}: {body[:500]}") from None
            if e.code == 401:
                raise BufferError("Buffer rejected the API key (HTTP 401). Create a new key and update "
                                  "the BUFFER_API_KEY secret (posting/TIKTOK.md, step 3).") from None
            if not payload.get("errors"):
                raise BufferError(f"HTTP {e.code}: {body[:500]}") from None
        if payload.get("errors"):
            err = payload["errors"][0]
            code = (err.get("extensions") or {}).get("code", "")
            raise BufferError(f"{code or 'error'}: {err.get('message')}")
        return payload["data"]

    # ── account ──────────────────────────────────────────────────────────
    def organizations(self):
        return self._call("query { account { organizations { id name } } }")["account"]["organizations"]

    def channels(self, organization_id):
        q = """query($org: OrganizationId!) {
                 channels(input: {organizationId: $org}) {
                   id name displayName service isDisconnected isLocked isQueuePaused } }"""
        return self._call(q, {"org": organization_id})["channels"]

    def tiktok_channel(self, channel_id=None):
        """Returns (organization_id, channel). Picks BUFFER_CHANNEL_ID if set, else the only TikTok channel."""
        channel_id = channel_id or os.environ.get("BUFFER_CHANNEL_ID") or None
        found = []
        for org in self.organizations():
            for ch in self.channels(org["id"]):
                if (channel_id and ch["id"] == channel_id) or (not channel_id and ch["service"] == "tiktok"):
                    found.append((org["id"], ch))
        if not found:
            raise BufferError(f"channel {channel_id} not found" if channel_id else
                              "no TikTok channel is connected to this Buffer account")
        if len(found) > 1:
            names = ", ".join(f"{c['name']} ({c['id']})" for _, c in found)
            raise BufferError(f"several TikTok channels ({names}); set the BUFFER_CHANNEL_ID secret to one id")
        org_id, ch = found[0]
        if ch["service"] != "tiktok":
            raise BufferError(f"channel {ch['id']} is {ch['service']}, not TikTok")
        if ch["isDisconnected"] or ch["isLocked"]:
            raise BufferError(f"TikTok channel {ch['name']} is disconnected or locked in Buffer; reconnect it")
        return org_id, ch

    # ── posts ────────────────────────────────────────────────────────────
    POST_FIELDS = "id status text dueAt sentAt externalLink error { message supportUrl }"

    def recent_posts(self, organization_id, channel_id, statuses=("sent", "sending", "scheduled"), limit=20):
        q = f"""query($in: PostsInput!, $n: Int) {{
                  posts(input: $in, first: $n) {{ edges {{ node {{ {self.POST_FIELDS} }} }} }} }}"""
        data = self._call(q, {"n": limit, "in": {
            "organizationId": organization_id,
            "filter": {"channelIds": [channel_id], "status": list(statuses)},
            "sort": [{"field": "createdAt", "direction": "desc"}]}})
        return [e["node"] for e in (data["posts"]["edges"] or [])]

    def create_tiktok_video(self, channel_id, text, video_url, ai_generated=True, thumbnail_offset_ms=None):
        """Publish now (Buffer sends it straight away) with TikTok's AI-generated content label."""
        video = {"url": video_url}
        if thumbnail_offset_ms is not None:
            video["metadata"] = {"thumbnailOffset": int(thumbnail_offset_ms)}
        q = f"""mutation($in: CreatePostInput!) {{ createPost(input: $in) {{
                  __typename
                  ... on PostActionSuccess {{ post {{ {self.POST_FIELDS} }} }}
                  ... on MutationError {{ message }} }} }}"""
        res = self._call(q, {"in": {
            "channelId": channel_id,
            "text": text,
            "schedulingType": "automatic",
            "mode": "shareNow",
            "needsApproval": False,
            "assets": [{"video": video}],
            "metadata": {"tiktok": {"isAiGenerated": bool(ai_generated)}},
        }})["createPost"]
        if "post" not in res:
            raise BufferError(f"{res.get('__typename', 'error')}: {res.get('message')}")
        return res["post"]

    def post(self, post_id):
        q = f"query($in: PostInput!) {{ post(input: $in) {{ {self.POST_FIELDS} }} }}"
        return self._call(q, {"in": {"id": post_id}})["post"]

    def wait_until_sent(self, post_id, timeout=1200, every=20, log=print):
        """Buffer reports `sent` once TikTok accepted the video, or `error` with TikTok's reason."""
        deadline = time.time() + timeout
        while True:
            p = self.post(post_id)
            log(f"[buffer] post {post_id}: {p['status']}")
            if p["status"] == "sent":
                return p
            if p["status"] == "error":
                err = p.get("error") or {}
                raise BufferError(f"Buffer could not publish: {err.get('message')}"
                                  + (f" (see {err['supportUrl']})" if err.get("supportUrl") else ""))
            if time.time() > deadline:
                raise TimeoutError(f"post {post_id} still {p['status']} after {timeout}s; check Buffer")
            time.sleep(every)
