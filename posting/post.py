#!/usr/bin/env python3
"""Instagram posting for Worldcraft Shorts.

  post.py select   [--episode epNN] [--force]       which episode goes out next (writes GITHUB_OUTPUT)
  post.py caption  --episode-json PATH               print the caption that would be posted
  post.py publish  --episode-json PATH --video-url URL [--cover-url URL] [--dry-run]
  post.py insights                                   append metric snapshots to posting/metrics.csv

State lives in posting/state.json (what has been posted) and posting/config.json (caption and
schedule rules). The workflows in .github/workflows/instagram-*.yml run these commands.
"""

import argparse
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "config.json"
STATE_PATH = HERE / "state.json"
METRICS_PATH = HERE / "metrics.csv"
ACCOUNT_PATH = HERE / "account.csv"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def now_utc():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def ep_id(n):
    return f"ep{n:02d}"


def set_output(**kv):
    for k, v in kv.items():
        print(f"{k}={v}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            for k, v in kv.items():
                f.write(f"{k}={v}\n")


def branch_for(cfg, n):
    return cfg["branchOverrides"].get(ep_id(n)) or cfg["branchPattern"].format(nn=f"{n:02d}")


def remote_branches():
    out = subprocess.run(["git", "ls-remote", "--heads", "origin"], check=True,
                         capture_output=True, text=True).stdout
    return {line.split("refs/heads/", 1)[1] for line in out.splitlines() if "refs/heads/" in line}


# ── caption ──────────────────────────────────────────────────────────────

def build_caption(cfg, episode):
    c = cfg["caption"]
    meta = episode.get("metadata", {})
    ig_caption = meta.get("instagram", {}).get("caption", "")
    source = ig_caption or meta.get("tiktok", {}).get("caption", "")
    hook = next((ln.strip() for ln in source.splitlines() if ln.strip() and not ln.strip().startswith("#")),
                episode["title"])

    base = [h.lower() for h in c["baseHashtags"]]
    skip = set(base) | {h.lower() for h in c["excludeHashtags"]}
    topical = [h.lower() for h in re.findall(r"#\w+", source) if h.lower() not in skip]
    tags = (base + [topical[0] if topical else c["fallbackTopicHashtag"]])[: c["maxHashtags"]]

    caption = c["template"].format(hook=hook, number=episode["number"], title=episode["title"],
                                   cta=c["cta"], hashtags=" ".join(tags))
    if len(caption) > 2200:
        raise ValueError(f"caption is {len(caption)} chars; Instagram allows 2200")
    return caption


def resolve(url):
    import urllib.request
    # GET, not HEAD: GitHub's signed release-asset URLs reject HEAD with 401. Range keeps it to 1 byte.
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Range": "bytes=0-0"}), timeout=30) as r:
        return r.geturl()


def episode_marker(number):
    # Matches the "Episode {number} · {title}" line in the template; used to detect duplicates.
    return re.compile(rf"Episode {int(number)} ·")


# ── commands ─────────────────────────────────────────────────────────────

def cmd_select(args):
    cfg, state = load(CONFIG_PATH), load(STATE_PATH)
    posted, hold = state["posted"], set(state.get("hold", []))
    branches = remote_branches()

    if args.episode:
        n = int(args.episode.lower().removeprefix("ep"))
        if ep_id(n) in posted and not args.force:
            return set_output(go="false", reason=f"{ep_id(n)} is already posted (use force to repost)")
    else:
        last = max((v["posted_at"] for v in posted.values() if v.get("posted_at")), default=None)
        if last and not args.force:
            age = (now_utc() - dt.datetime.fromisoformat(last)).total_seconds() / 3600
            if age < cfg["minHoursBetweenPosts"]:
                return set_output(go="false", reason=f"last post was {age:.1f} h ago "
                                                     f"(minimum {cfg['minHoursBetweenPosts']} h)")
        n = next((i for i in range(1, cfg["totalEpisodes"] + 1)
                  if ep_id(i) not in posted and ep_id(i) not in hold), None)
        if n is None:
            return set_output(go="false", reason="every episode is posted or on hold")

    branch = branch_for(cfg, n)
    if branch not in branches:
        return set_output(go="false", reason=f"{ep_id(n)} is next but branch {branch} does not exist yet")
    missing = unfinished(branch, ep_id(n))
    if missing:
        return set_output(go="false", reason=f"{ep_id(n)} is still in progress on {branch} (no {missing} yet)")
    set_output(go="true", episode=ep_id(n), branch=branch)


def unfinished(branch, eid):
    """An episode branch exists from its first WIP commit. The cover and subtitles are made last, so
    require both before posting. Returns what's missing, or None when the episode looks finished."""
    subprocess.run(["git", "fetch", "-q", "--depth=1", "origin", branch], check=True)
    files = subprocess.run(["git", "ls-tree", "-r", "--name-only", "FETCH_HEAD", f"episodes/{eid}/"],
                           check=True, capture_output=True, text=True).stdout.split()
    if not any(f.endswith("_cover.jpg") for f in files):
        return "cover image"
    if f"episodes/{eid}/{eid}.srt" not in files:
        return "subtitles (.srt)"
    return None


def cmd_caption(args):
    print(build_caption(load(CONFIG_PATH), load(Path(args.episode_json))))


def cmd_publish(args):
    from ig import Client

    cfg, state = load(CONFIG_PATH), load(STATE_PATH)
    episode = load(Path(args.episode_json))
    eid, number = ep_id(int(episode["number"])), int(episode["number"])
    caption = build_caption(cfg, episode)
    print(f"[post] {eid}: {episode['title']}\n[post] video: {args.video_url}\n[post] cover: {args.cover_url}")
    print("[post] caption:\n" + caption)
    if args.dry_run:
        print("[post] dry run: nothing published")
        return

    ig = Client()
    marker = episode_marker(number)
    for m in ig.recent_media(limit=15):
        if marker.search(m.get("caption") or ""):
            print(f"[post] {eid} is already on the account ({m.get('permalink')}); recording it, not reposting")
            state["posted"][eid] = {"by": "workflow", "media_id": m["id"], "permalink": m.get("permalink"),
                                    "posted_at": m.get("timestamp", now_utc().isoformat())[:19] + "+00:00"}
            save_state(state)
            return

    def attempt(video_url, cover_url):
        container = ig.create_reel(video_url, caption, cover_url=cover_url,
                                   ai_generated=cfg["aiLabel"], share_to_feed=cfg["shareToFeed"])
        ig.wait_until_ready(container)
        return container

    try:
        container = attempt(args.video_url, args.cover_url)
    except Exception as e:
        # GitHub release links redirect to a signed storage URL. If Instagram won't follow the
        # redirect, retry once with the resolved URL (valid long enough for Meta to fetch it).
        print(f"::warning::first attempt failed ({e}); retrying with resolved download URLs")
        container = attempt(resolve(args.video_url), resolve(args.cover_url) if args.cover_url else None)
    media_id = ig.publish(container)
    info = ig.media(media_id)
    state["posted"][eid] = {"by": "workflow", "media_id": media_id, "permalink": info.get("permalink"),
                            "posted_at": now_utc().isoformat()}
    save_state(state)
    print(f"[post] published {eid}: {info.get('permalink')}")

    first = episode.get("metadata", {}).get("instagram", {}).get("pinnedComment")
    if cfg["postFirstComment"] and first:
        try:
            ig.comment(media_id, first)
            print(f"[post] first comment: {first}")
        except Exception as e:  # the post is live; a failed comment shouldn't fail the run
            print(f"::warning::posted {eid} but the first comment failed: {e}")


def cmd_insights(_args):
    from ig import Client

    cfg, state = load(CONFIG_PATH), load(STATE_PATH)
    ig, now = Client(), now_utc()
    metrics = cfg["insights"]["metrics"]

    acct = ig.account()
    new_acct = not ACCOUNT_PATH.exists()
    with ACCOUNT_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_acct:
            w.writerow(["snapshot_utc", "username", "followers_count", "media_count"])
        w.writerow([now.isoformat(), acct.get("username"), acct.get("followers_count"), acct.get("media_count")])
    print(f"[insights] @{acct.get('username')}: {acct.get('followers_count')} followers")

    rows = []
    for eid, rec in sorted(state["posted"].items()):
        if not rec.get("media_id") or not rec.get("posted_at"):
            continue
        hours = (now - dt.datetime.fromisoformat(rec["posted_at"])).total_seconds() / 3600
        if hours > cfg["insights"]["trackDays"] * 24:
            continue
        values = ig.insights(rec["media_id"], metrics)
        rows.append([now.isoformat(), eid, rec["media_id"], round(hours, 1)] + [values.get(m, "") for m in metrics])
        print(f"[insights] {eid} at {hours:.0f} h: " + ", ".join(f"{m}={values.get(m, '-')}" for m in metrics))

    if rows:
        new = not METRICS_PATH.exists()
        with METRICS_PATH.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["snapshot_utc", "episode", "media_id", "hours_since_post"] + metrics)
            w.writerows(rows)


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
    s = sub.add_parser("publish")
    s.add_argument("--episode-json", required=True)
    s.add_argument("--video-url", required=True)
    s.add_argument("--cover-url")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_publish)
    s = sub.add_parser("insights")
    s.set_defaults(fn=cmd_insights)
    args = p.parse_args()
    sys.path.insert(0, str(HERE))
    args.fn(args)


if __name__ == "__main__":
    main()
