"""Minimal Instagram Graph API client (stdlib only).

Credentials come from the environment:
  IG_ACCESS_TOKEN  long-lived token (Instagram Login: IGAA...; Facebook Login: EAA...)
  IG_USER_ID       the Instagram professional account id
  IG_API_BASE      optional; default https://graph.instagram.com/v24.0
                   (use https://graph.facebook.com/v24.0 for Facebook Login tokens)
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE = "https://graph.instagram.com/v24.0"


class GraphError(RuntimeError):
    def __init__(self, status, payload):
        self.status = status
        self.payload = payload
        err = payload.get("error", {}) if isinstance(payload, dict) else {}
        msg = err.get("error_user_msg") or err.get("message") or str(payload)
        sub = err.get("error_subcode")
        super().__init__(f"HTTP {status}: {msg}" + (f" (subcode {sub})" if sub else ""))


class Client:
    def __init__(self, token=None, user_id=None, base=None):
        self.token = token or os.environ["IG_ACCESS_TOKEN"]
        self.user_id = user_id or os.environ["IG_USER_ID"]
        self.base = (base or os.environ.get("IG_API_BASE") or DEFAULT_BASE).rstrip("/")

    def _call(self, method, path, params=None):
        params = {k: v for k, v in (params or {}).items() if v is not None}
        params["access_token"] = self.token
        url = f"{self.base}/{path.lstrip('/')}"
        data = None
        if method == "GET":
            url += "?" + urllib.parse.urlencode(params)
        else:
            data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            body = e.read()
            try:
                payload = json.loads(body)
            except ValueError:
                payload = {"raw": body.decode(errors="replace")[:500]}
            raise GraphError(e.code, payload) from None

    # ── account ──────────────────────────────────────────────────────────
    def account(self):
        return self._call("GET", self.user_id, {"fields": "id,username,followers_count,media_count"})

    def recent_media(self, limit=10):
        res = self._call("GET", f"{self.user_id}/media",
                         {"fields": "id,caption,timestamp,permalink,media_product_type", "limit": limit})
        return res.get("data", [])

    # ── publishing ───────────────────────────────────────────────────────
    def create_reel(self, video_url, caption, cover_url=None, ai_generated=True, share_to_feed=True):
        return self._call("POST", f"{self.user_id}/media", {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "cover_url": cover_url,
            "share_to_feed": "true" if share_to_feed else "false",
            "is_ai_generated": "true" if ai_generated else None,
        })["id"]

    def wait_until_ready(self, container_id, timeout=900, every=20, log=print):
        deadline = time.time() + timeout
        while True:
            res = self._call("GET", container_id, {"fields": "status_code,status"})
            code = res.get("status_code")
            log(f"[ig] container {container_id}: {code} {res.get('status', '')}".rstrip())
            if code == "FINISHED":
                return
            if code in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"container {container_id} {code}: {res.get('status')}")
            if time.time() > deadline:
                raise TimeoutError(f"container {container_id} still {code} after {timeout}s")
            time.sleep(every)

    def publish(self, container_id):
        return self._call("POST", f"{self.user_id}/media_publish", {"creation_id": container_id})["id"]

    def media(self, media_id, fields="id,permalink,timestamp,caption"):
        return self._call("GET", media_id, {"fields": fields})

    def comment(self, media_id, message):
        return self._call("POST", f"{media_id}/comments", {"message": message})["id"]

    # ── insights ─────────────────────────────────────────────────────────
    def insights(self, media_id, metrics):
        """Fetch metrics; if the batch is rejected, fall back to one call per metric and skip the ones that fail."""
        def parse(res):
            out = {}
            for row in res.get("data", []):
                vals = row.get("values") or [{}]
                out[row["name"]] = row.get("total_value", {}).get("value", vals[0].get("value"))
            return out

        try:
            return parse(self._call("GET", f"{media_id}/insights", {"metric": ",".join(metrics)}))
        except GraphError:
            out = {}
            for m in metrics:
                try:
                    out.update(parse(self._call("GET", f"{media_id}/insights", {"metric": m})))
                except GraphError:
                    pass
            return out
