# TikTok auto-posting (through Buffer)

Posts one Worldcraft Shorts episode a day to TikTok, the same episode Instagram gets that day,
starting with **EP14**. Like the Instagram flow, it runs entirely on GitHub Actions.

## Why Buffer and not TikTok's own API

TikTok's own API (the "Content Posting API", checked November 2026) doesn't fit a personal auto-poster:

- An app that hasn't passed TikTok's **audit** can only post **private (SELF_ONLY)** videos, and only
  while the whole account is set to private.
- TikTok's audit guidelines list *"a utility tool to help upload contents to the account(s) you or
  your team manages"* as **not acceptable**, so an audit for this would very likely be rejected.
- The no-audit alternative ("upload to inbox") can't set the caption or the AI label. You'd still
  have to finish every post by hand in the app.

[Buffer](https://buffer.com) is a scheduler that TikTok has already approved. Its API lets this repo
post publicly, with the caption and TikTok's **AI-generated content** label set automatically. You
don't need a TikTok developer account, a business account or an ads account.

## How it works

`.github/workflows/tiktok-post.yml` starts as soon as the scheduled **Instagram daily post** run
finishes. It also has its own daily fallback run at 22:47 UTC in case the Instagram run didn't happen.

1. Picks the lowest episode, from EP14 on, that isn't in `posting/tiktok_state.json` yet. TikTok keeps
   its own record. Instagram's `state.json` is never touched. Same rules as Instagram: it waits if
   the episode isn't finished, and it posts at most once every 12 hours.
2. Reuses `epNN.mp4` from the `videos` release, which the Instagram run has just uploaded. It only
   renders the video if it's missing.
3. Checks Buffer for an existing "Episode NN ·" post, so a retry never double-posts.
4. Sends it to Buffer with **"publish now"** and the AI-generated label on, then waits until Buffer
   reports TikTok accepted it. If Buffer reports an error, the run fails and GitHub emails you.
5. Commits the result to `posting/tiktok_state.json`. The run's summary page shows the TikTok link
   and the **comment to pin**: TikTok's API can't post or pin comments, so that one step is yours.

Manual Instagram runs (tests, dry runs, reposts) never trigger a TikTok post.

## Caption

Built from `episode.json → metadata.tiktok.caption`, with the same "Episode NN · Title" line Instagram uses:

```
She broke her oath. Hero or traitor? Depends whose side of the levee you're on ⚖️ Give both sides
real reasons and let neither be entirely right. Freedom or duty: which wins?

Episode 14 · Give Every Nation a Different Definition of Honor

#Worldbuilding #FantasyWriting #WritingTips #FantasyCultures #WorldcraftShorts
```

TikTok allows 2,200 characters (emoji count as two). TikTok documents no separate hashtag limit; this
keeps the episode's own tags, at most 5. Change it under `"tiktok"` in `posting/config.json`. Preview:
`python3 posting/tiktok_post.py caption --episode-json episodes/ep15/episode.json`.

## One-time setup (about 10 minutes)

Send a screenshot whenever a screen doesn't match these steps. Buffer changes its menus now and then.

### 1. Create a Buffer account
1. Go to <https://buffer.com> and click **Get started now**. Sign up with your email or Google.
2. When it asks for a plan, choose **Free**. It's enough here: the API is included and each video
   is published immediately, so nothing waits in a queue.

### 2. Connect TikTok to Buffer
1. In Buffer, click **Connect channels** (or **Channels → + Connect channel**), then **TikTok**.
2. TikTok's login page opens. Log in to the TikTok account the show posts to.
3. TikTok shows what Buffer is allowed to do. Click **Authorize** / **Continue**.
4. You're back in Buffer with the TikTok account listed as a channel. Personal TikTok accounts
   work; you don't need to switch to a business account.

### 3. Create a Buffer API key and save it in GitHub
1. In Buffer, open **Settings** (from your profile picture, top right), then **API**.
2. Click **Create API key** (any name, e.g. `github-worldcraft`). Copy the key. Don't paste it into a chat.
3. In this GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**.
   - Name: `BUFFER_API_KEY`
   - Secret: paste the key → **Add secret**.

The key doesn't expire on a timer. If you ever delete it in Buffer, create a new one and replace the secret.

(Only if you connect **more than one** TikTok account to Buffer: the dry run in step 4 lists each
channel's id. Add the right one under **Settings → Secrets and variables → Actions → Variables →
New repository variable** as `BUFFER_CHANNEL_ID`.)

### 4. Test, then go live
**Actions → TikTok daily post → Run workflow**:
1. Leave **dry_run** ticked (the default) and set **episode** to `ep14`, then **Run workflow**. It
   finds EP14's video, prints the caption, logs in to Buffer and names the TikTok channel it would
   post to, but posts nothing. Open the run and read the summary.
2. You're done. From now on it posts after each scheduled Instagram run. To post right away instead
   of waiting, run it again with **dry_run** unticked.
3. After the first real post, open it in TikTok and check that it says **"Creator labeled as
   AI-generated"**, the caption is right, and comments are on. Then pin the comment from the run summary.

## Day-to-day

| You want to... | Do this |
|---|---|
| Post right now | Actions → TikTok daily post → Run workflow, untick **dry_run** (tick **force** if TikTok got a post in the last 12 h) |
| Post a specific episode | Run workflow with **episode** = `ep16`, **dry_run** unticked |
| Skip or delay an episode on TikTok only | Add it to `"hold"` in `posting/tiktok_state.json` |
| Start from a different episode | Change `"startEpisode"` under `"tiktok"` in `posting/config.json` |
| Use your own video | Upload it to the `videos` release as `epNN.mp4` before it's posted (shared with Instagram) |
| Pause TikTok only | Actions → TikTok daily post → ⋯ → Disable workflow |

## Limits to know

- Buffer's free API allows 600 requests a day; a post uses about 10–60 (most of them waiting for
  TikTok to finish processing).
- TikTok can still refuse a video (for example, music it detects as copyrighted). Buffer then reports
  the error, the run fails, and the log shows the reason.
- Buffer fetches the video from the GitHub release link. If it ever refuses the redirect that GitHub
  uses, the script retries once with the direct download link.
- If Instagram's workflow is paused or failing, TikTok carries on by itself using the fallback schedule.
