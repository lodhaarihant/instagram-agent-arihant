# Thoughts4us autopilot

A week of Instagram content for **@thoughts4us.official**, built with the ig-* skills in
this repo, plus the scripts that publish it automatically.

**Every day, 12 pieces (IST):**

| time | what | format |
| --- | --- | --- |
| 07:30 | good-morning line | story |
| 08:00 | famous quote, with its real source | feed image |
| 09:30 | old-book quote | story |
| 11:30 | "this or that?" reply 1 or 2 | story |
| 13:00 | original thought | feed image |
| 14:30 | points to the 13:00 post | story |
| 16:30 | "one word" prompt | story |
| 18:30 | carousel (quotes, poems, life lists) | carousel, 8 to 10 slides |
| 19:30 | two-line poem | story |
| 20:30 | "finish this" prompt | story |
| 21:30 | original four-line poem | reel, 10s |
| 22:30 | goodnight line | story |

Week 1 runs **Mon 19 Oct to Sun 25 Oct 2026**. Open `preview.html` to see
every post and caption before it goes live.

## Files

| file | job |
| --- | --- |
| `content.py` | all the words: quotes, poems, captions, stories. Edit here. |
| `config.json` | handle, week start, timezone, media URL, reply mode |
| `render.py` | turns the schedule into JPEGs and MP4s in `media/week1/` |
| `preview.py` | writes `preview.html` |
| `autopost.py` | publishes due posts through the Instagram Graph API |
| `replybot.py` | hides spam, thanks supporters, queues real comments to `state/review.md` |
| `../.github/workflows/thoughts4us.yml` | runs both, 12 times a day, on GitHub |
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
- **No music on reels.** The API can't attach licensed audio. The reels are
  silent text reels.
- **No engagement on other accounts.** Commenting, liking, following or DMing
  other people by bot breaks Instagram's terms and gets accounts blocked.
  `engagement.md` is the 20-minute daily routine for that, with Claude drafting.
- **DMs** are answered by you. Paste them into Claude with `/ig-dm`.
