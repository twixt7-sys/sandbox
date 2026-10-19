# Distribution, experiments, metrics

Per-episode titles, captions, hashtags and pinned comments live in `episodes/<ep>/episode.json → metadata` and are printed into `STORYBOARD.md`.

## Episode 01 captions (ready to paste)

Source of truth: `episodes/ep01/episode.json` → `metadata`. Limits below were checked against the actual text.

### YouTube Shorts
- **Title** (44/100 chars): `1,000 years of lore and it still feels empty`
- **Alternate title for an A/B test** (34 chars): `Why your fantasy world feels empty`
- **Description** (551/5,000 chars):

> Lore is what happened. A living world is what it changed.
>
> Say a war destroyed the only bridge across a river. Centuries later, merchants still pay the ferry toll, the ferry family rules the valley, and kids on each bank grow up with different accents. Every spring, both banks float lanterns where the bridge once stood. That is the difference between history and worldbuilding.
>
> Episode 1 of 50 in Worldbuilding, from the ground up: short lessons for fantasy writers, novelists and tabletop RPG creators.
>
> #worldbuilding #fantasywriting #writingtips

- **Pinned comment:** What's one event in your world's history that people still feel today? Tell me the consequence, not the event.
- **Upload settings:** AI use: Yes (see docs/DISTRIBUTION.md). Not made for kids. Category: Education.

### Instagram Reels
- **Caption** (433/2,200 chars; hook line is 46 chars):

> A thousand years of lore can still feel empty.
>
> Lore is what happened. A living world is what it changed.
>
> One broken bridge and suddenly there are ferry tolls, a ruling family, two accents and a spring festival.
>
> What's one event in your world that people still feel today? Tell me the consequence, not the event.
>
> Follow for 49 more worldbuilding lessons.
>
> #worldbuilding #fantasywriting #writingcommunity #worldbuildingtips #ttrpg

- **Pinned comment:** Your turn: name one war, disaster or treaty in your world. What do ordinary people still pay, avoid or celebrate because of it?
- **Upload settings:** Turn on the AI label in the post's advanced settings (see docs/DISTRIBUTION.md).

### Facebook Reels
- **Caption** (398 chars; hook line is 77 chars):

> Your fantasy world can have a thousand years of history and still feel empty.
>
> History only matters when it changes how people live. Break one bridge and a whole valley's trade, power and culture bend around it.
>
> Writers and GMs: what's a tradition in your world that only exists because something went wrong?
>
> Episode 1 of 50. Follow for the rest.
>
> #worldbuilding #fantasywriting #writingcommunity

- **Pinned comment:** If the bridge were rebuilt tomorrow, who in this valley would try to stop it?
- **Upload settings:** Turn on the AI label when posting (see docs/DISTRIBUTION.md).

(TikTok copy is unchanged in `episode.json`.)

## Research notes behind the captions (checked 2026-10-19)

Official sources first; blog figures are marked and should be treated as estimates.

| Topic | Finding | Confidence |
|---|---|---|
| YouTube hashtags | Up to 3 description hashtags appear above the title; more than 60 hashtags and all are ignored; hashtags can sit in the title or description ([YouTube Help](https://support.google.com/youtube/answer/6390658)). | Official |
| YouTube title and description | Limits are 100 and 5,000 characters. Only roughly 40 to 70 title characters show in feeds, so the title front-loads the hook. | Blogs, consistent ([hashtagtools.io](https://hashtagtools.io/blog/youtube-shorts-character-limits-title-description-hashtags-2026), [limitora](https://limitora.com/blog/youtube-character-limits-2026.html)) |
| `#Shorts` | One 2026 guide says it is no longer needed because YouTube classifies by shape and length. I left it out. Adding it costs nothing if you prefer it. | Single blog |
| Instagram caption | Limit is 2,200 characters. Sources disagree on the fold: about 125 characters in feed, as few as about 55 on Reels. The hook is 46 characters so it survives either. | Blogs, conflicting ([Sendible](https://www.sendible.com/insights/instagram-character-limit), [Kompozy](https://kompozy.io/specs/instagram-reels-caption-character-limit)) |
| Instagram hashtags | Several sources say Instagram moved to a cap of 5 per post from December 2025, and one says it recommends 3 to 5. I could not find Meta's own announcement, so I used exactly 5. If the app rejects the fifth, drop `#ttrpg`. | Unverified ([posttruncate](https://posttruncate.com/en/blog/instagram-caption-limits-and-hashtag-rules-2026/)) |
| Facebook Reels | Sources agree on 2 to 5 hashtags and a short hook up front, and say discovery leans on AI recommendations more than on hashtags. The stated limits conflict (2,200 vs 63,206), so the caption is short. | Blogs, conflicting ([OpusClip](https://www.opus.pro/blog/facebook-reels-caption-subtitle-best-practices), [Lilach Bullock](https://www.lilachbullock.com/how-many-hashtags-facebook-reels/)) |
| Niche hashtags | `#worldbuilding` and `#fantasywriting` are the established topic tags, `#writingcommunity` is the large community tag (about 10.7M posts per a tag-tool list). Counts are undated snapshots. | Third-party tools ([best-hashtags.com](https://best-hashtags.com/hashtag/worldbuilding/)) |

## AI disclosure: set it on all three

This episode uses AI-generated stills and a synthetic (text-to-speech) narrator. I recommend switching the AI label on for every platform. This is my reading of the policies, not legal advice.

- **YouTube:** realistic AI content needs the "AI use" toggle in Studio. Clearly fantastical scenes are exempt, and the page says disclosure does not limit reach or monetization. The stills look photographic, and the policy page does not say how a non-cloned synthetic voice is treated, so Yes is the safe answer ([YouTube Help](https://support.google.com/youtube/answer/14328491)).
- **Instagram and Facebook:** Meta asks creators to flag organic posts with photorealistic video or realistic-sounding digitally created audio, and may penalize those that skip it. Its automatic "AI info" label also triggers on industry-standard AI indicators, so being labeled anyway is plausible ([Meta newsroom](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/), [Meta midterms update, 2026](https://about.fb.com/news/2026/02/meta-prepares-for-2026-us-midterms/)). I could not open Meta's help-center pages to confirm the exact toggle wording, so look for it in the post's advanced settings.
- Nothing in the captions claims the scenes are real places. Keep it that way.

## Creative choices meant to help retention

These are hypotheses to test, not guarantees:
- The strongest line comes at frame 0, over a finished image. There is no logo intro.
- A visible change about every 1–3 s (counter → oversized word → statement → bridge → map beats). Each change carries new information rather than motion for its own sake.
- Payoff before the CTA: the lantern shot answers "empty" with "not empty."
- The end crossfades into the first frame and the CTA line rhymes with the hook, so the video can loop cleanly.
- The captions carry the full meaning with the sound off. Only lesson words are highlighted.

## Experiments for later episodes

Run each for at least 6 episodes per variant, alternating, with topics of similar appeal. Compare medians, not single videos.

| # | Variable | A (current) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook structure | Challenge an assumption ("…still feel completely empty") | Concrete image first ("This bridge fell 300 years ago. It still runs the valley.") | YouTube "viewed vs swiped away"; TikTok 2-s retention |
| 2 | Caption density | Phrase captions, ≤20 chars, selective highlights | One word at a time, kinetic | Average % viewed; rewatch (avg % > 100) |
| 3 | CTA placement | Spoken CTA at the end + end card | Soft mid-roll line at ~19 s ("episode 1 of 50"), silent end card | Subscribers/followers per 1,000 views; completion rate |

## What to watch

| Platform | Metrics |
|---|---|
| YouTube Studio (Shorts) | Viewed vs swiped away, average view duration, average % viewed (above 100% means loops), subscribers gained, shares, likes |
| TikTok Analytics | Average watch time, watched full video %, retention curve, new followers, shares, saves |
| Meta Business Suite (Reels) | 3-second views, average watch time, reach, follows, shares, saves |

Log each episode's numbers at 48 h and 7 days in one sheet, with the variant labels. Don't judge a variant from a single episode.
