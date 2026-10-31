# Instagram auto-posting

Posts one Worldcraft Shorts episode a day as an Instagram Reel, in order, starting after the last
episode you posted by hand (EP12). Runs entirely on GitHub Actions: nothing runs on your computer
and nothing depends on a Claude session staying open.

## How it works

Every day at **16:23 UTC** (00:23 Manila, 12:23 New York), `.github/workflows/instagram-post.yml`:

1. Picks the lowest episode number that isn't in `posting/state.json` yet (EP13 first).
   If that episode's branch (`claude/worldcraft-epNN`) doesn't exist yet, or the episode is still in
   progress (no `*_cover.jpg` and `epNN.srt` in its folder yet; both are made last), it posts nothing
   that day rather than skipping ahead, and says so in the run summary.
2. Renders it from that branch with the same steps as `render.yml`, runs `pipeline/qa.py`, re-encodes
   it to the H.264/AAC format Instagram's fetcher expects and runs QA again.
3. Uploads the MP4 and the episode cover to the public **`videos` release** of this repo. Instagram
   downloads the video from there.
4. Publishes the Reel with the **AI label on** (`is_ai_generated`), the episode cover as the
   thumbnail, and the caption below. Then it posts the episode's `pinnedComment` as the first comment.
5. Commits the post id and link to `posting/state.json`.

Before publishing it checks your recent posts for "Episode NN ·", so a retry never double-posts.

`.github/workflows/instagram-insights.yml` runs daily at 14:41 UTC. It appends follower count to
`posting/account.csv` and each Reel's views, reach, likes, comments, shares, saves, watch time and
skip rate for its first 14 days to `posting/metrics.csv`. Ask Claude to read those files for analysis.

## Caption

Built from `episode.json → metadata.instagram` and `posting/config.json`:

```
Same gift. Opposite insult.

Episode 13 · Every Culture Has Something It Considers Shameful

More valuable bite-sized worldbuilding/fantasy writing content? Give this small page a follow and come along :)

#worldbuilding #fantasywriting #writingcommunity #writingtips #fantasycultures
```

Instagram allows at most **5 hashtags** per post (since December 2025). That's four broad, popular
tags plus one topic tag taken from the episode. Change the CTA, tags or layout in `posting/config.json`.
Preview any episode's caption with `python3 posting/post.py caption --episode-json episodes/ep14/episode.json`.

## One-time setup

### 1. Make the account Professional
In the Instagram app: **Settings → Account type and tools → Switch to professional account**
(Creator or Business). The API only works with professional accounts.

### 2. Get an access token (about 10 minutes, no app review needed for your own account)
1. Go to <https://developers.facebook.com/apps> and click **Create app**. Pick the use case
   **"Manage messaging & content on Instagram"**, then finish creating the app.
2. In the app: **Use cases → Customize → API setup with Unified login**. This needs a
   **business portfolio**: click **+ Business portfolio** and create one (any name; no company or
   verification needed).
3. Connect the Instagram account to it, approving the permissions it asks for (basic, content publish,
   manage comments, manage insights), then **Generate token**. The token starts with `EAA`.
4. Copy the token and the **Instagram account ID** (a long number shown next to the account; also under
   business.facebook.com → **Settings → Accounts → Instagram accounts**).

Older apps may show **API setup with Instagram login** instead; it works too, and its token starts with
`IGAA`. The scripts pick the right Meta API host from the token prefix.

If the account doesn't appear or the token is refused: in the app, open **App roles → Roles → Add people → Instagram Tester**, add
your username, then accept it in Instagram (**Settings → Website permissions → Apps and websites → Tester invites**).

### 3. Save them as GitHub secrets
In this repo: **Settings → Secrets and variables → Actions → New repository secret**

| Name | Value |
|---|---|
| `IG_ACCESS_TOKEN` | the `EAA...` (or `IGAA...`) token |
| `IG_USER_ID` | the Instagram account ID |

### 4. Test, then go live
**Actions → Instagram daily post → Run workflow**:
1. With **dry_run** ticked. This renders EP13, uploads it to the `videos` release and prints the
   caption, but doesn't post. Watch the video on the release page.
2. Run it again with **dry_run** unticked. EP13 goes live now; from then on it posts daily on its own.

## Day-to-day

| You want to... | Do this |
|---|---|
| Post right now | Actions → Instagram daily post → Run workflow (tick **force** if something was already posted in the last 20 h) |
| Post a specific episode | Run workflow with **episode** = `ep15` |
| Skip or delay an episode | Add it to `"hold"` in `posting/state.json`, e.g. `"hold": ["ep16"]` |
| Use your own render instead of the CI one | Upload it to the `videos` release as `epNN.mp4` before it's posted |
| Change the time | Edit the `cron` line in `.github/workflows/instagram-post.yml` (UTC) |
| Pause everything | Actions → Instagram daily post → ⋯ → Disable workflow |

New episodes are picked up automatically as long as they're on a `claude/worldcraft-epNN` branch.

## Limits to know

- **Token lifetime:** `IGAA` tokens expire after 60 days. `EAA` tokens from Unified login are reported
  not to expire, but check the expiry Meta shows when generating it. Either way, posting through EP50
  at one a day takes 38 days, so one token covers the test. If a run fails with an expired-token error,
  generate a new one (step 2) and replace the secret.
- Instagram allows up to 100 API posts a day; this posts one.
- GitHub can start scheduled runs a few minutes late, and it pauses schedules in repos with no
  activity for 60 days. The daily commits from these workflows count as activity.
- If a run fails, GitHub emails you. The run log shows Instagram's error message.
