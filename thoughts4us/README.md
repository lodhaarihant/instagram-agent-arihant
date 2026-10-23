# Thoughts4us autopilot

A week of Instagram content for **@thoughts4us.official**, built with the ig-* skills in
this repo, plus the scripts that publish it automatically.

**Every day, 20 pieces, one an hour from 05:00 to 00:00 IST:**

| time | what | format |
| --- | --- | --- |
| 05:00 | good-morning line | story |
| 06:00 | affirmation | story |
| 07:00 | original thought, line by line | reel |
| 08:00 | famous quote, with its real source | feed image |
| 09:00 | old-book quote | story |
| 10:00 | "this or that?" reply 1 or 2 | story |
| 11:00 | famous quote, line by line | reel |
| 12:00 | points to the 07:00 reel | story |
| 13:00 | list carousel (habits, friendship, healing) | carousel |
| 14:00 | "one word" prompt | story |
| 15:00 | original line | reel |
| 16:00 | reminder (water, stretch, call someone) | story |
| 17:00 | second "this or that?" | story |
| 18:00 | quote or poem carousel | carousel |
| 19:00 | famous quote, line by line | reel |
| 20:00 | points to the 18:00 carousel | story |
| 21:00 | two-line poem | story |
| 22:00 | original four-line poem | reel |
| 23:00 | "finish this" prompt | story |
| 00:00 | goodnight line | story |

5 reels, 3 feed posts and 12 stories. Reels are at the peak hours because
they're the format Instagram shows to people who don't follow you yet.

Week 1 runs **Sat 17 Oct to Fri 23 Oct 2026**. Open `preview.html` to see
every post and caption before it goes live.

## Files

| file | job |
| --- | --- |
| `content.py`, `content_extra.py` | all the words: quotes, poems, captions, stories. Edit here. |
| `config.json` | handle, week start, timezone, media URL, reply mode |
| `render.py` | turns the schedule into JPEGs and MP4s in `media/week1/` |
| `preview.py` | writes `preview.html` |
| `pack.py` | day-by-day upload folders for scheduling by hand in Meta Business Suite |
| `autopost.py` | publishes due posts through the Instagram Graph API |
| `replybot.py` | hides spam, thanks supporters, queues real comments to `state/review.md` |
| `../.github/workflows/thoughts4us.yml` | runs both every hour, 05:00 to 00:00 IST, on GitHub |
| `voice.md`, `profile.md`, `engagement.md` | voice, bio and growth playbook |

Rebuild after editing words:

```bash
cd thoughts4us && python3 content.py && ../.venv/bin/python render.py schedule/week1.json && python3 preview.py
```

## Going live: one-time setup (about 30 min, you do these)

**1. Professional account.** On Instagram: Settings > Account type and tools >
Switch to professional > Creator. Optionally link it to the Facebook page.

**2. A Meta app and a token.** At developers.facebook.com: My Apps > Create
app > use case "Manage messaging & content on Instagram". Open *API setup with
Instagram login*, add your Instagram account, and press *Generate token*.
Permissions needed: `instagram_business_basic`,
`instagram_business_content_publish`, `instagram_business_manage_comments`.
The app can stay in development mode because you're only posting to your own
account. The page shows your Instagram user ID next to the token.

The token is long-lived (60 days). Generate a new one before it expires and
update the secret, or the posts stop.

**3. Public media URL.** Instagram downloads each image and video from a URL,
so the files must be public. This repo is private, so either:

- make this repo public and turn on GitHub Pages (Settings > Pages > Deploy
  from branch `main`, folder `/`). The media URL is then
  `https://lodhaarihant.github.io/instagram-agent-arihant/thoughts4us`. Or
- put `thoughts4us/media/` in a separate public repo with Pages on, and point
  the URL at that.

**4. GitHub secrets and variables.** Repo > Settings > Secrets and variables > Actions:

| kind | name | value |
| --- | --- | --- |
| secret | `IG_USER_ID` | your Instagram user ID from step 2 |
| secret | `IG_ACCESS_TOKEN` | the token from step 2 |
| variable | `MEDIA_BASE_URL` | the URL from step 3 |
| variable | `GRAPH_HOST` | `https://graph.instagram.com` |

Never paste the token into a file in the repo.

**5. Test.** Actions > *thoughts4us autopost* > Run workflow, with dry run
ticked. It prints what would go out. Untick it to post for real.

After that it runs on its own. Scheduled runs on GitHub can start 5 to 20
minutes late; posts go out on the next run that sees them due.

## What it can't do (by design or by API)

- **No stickers.** The API can't add polls, question boxes or links to
  stories, so the story prompts say "reply here", which lands in your DMs.
  Add a poll by hand on any day you're around.
- **No Instagram-library music.** The API can't attach songs from Instagram's
  library. Instead `render.py` bakes a track from `music/` into every reel
  (one per reel, chosen from its post id). Drop more MP3s into `music/` and
  re-render to use them.
- **No engagement on other accounts.** Commenting, liking, following or DMing
  other people by bot breaks Instagram's terms and gets accounts blocked.
  `engagement.md` is the 20-minute daily routine for that, with Claude drafting.
- **DMs** are answered by you. Paste them into Claude with `/ig-dm`.

## Week 2: the Bhagavad Gita (Sat 24 to Fri 30 Oct 2026)

Same 20-a-day schedule, one theme a day: Karma, the mind and rest, staying steady,
the soul, devotion, knowledge, peace. Every verse is cited by chapter and verse, in
plain wording of ours; check it against the translation you prefer before it goes out.

| file | job |
| --- | --- |
| `content_krishna.py` | all week 2 words. Edit here, then rerun. |
| `bg.py` | which artwork each day uses, and where the text sits on it |
| `backgrounds/` | the artwork (from the reference pins). Swap a file to change a look |
| `render_krishna.py` | renders `schedule/week2.json` to `media/week2/` |

```bash
cd thoughts4us && ../.venv/bin/python content_krishna.py && ../.venv/bin/python render_krishna.py schedule/week2.json && python3 preview.py schedule/week2.json && python3 pack.py schedule/week2.json
```

- **Music:** every reel and the 05:00 and 00:00 story videos carry a flute track from
  `music/flute/`. The two "native american" flutes are skipped on purpose.
- **No voice-over in week 2.** Reels and the 05:00 and 00:00 stories are flute only, slowed to 80% (`MUSIC_TEMPO` in
  `render_krishna.py`). The voice code is still there: set `VOICE_OVER = True` in `content_krishna.py`, rerun it, and re-render
  to read the English aloud again, or save a recording as `voice/<post id>.mp3`.
- **Artwork:** the images come from Pinterest pins and belong to their artists. Get
  permission or licences before posting them on a page you plan to earn from.
