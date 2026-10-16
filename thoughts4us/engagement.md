# Growth and engagement (the part the bot does not do)

The bot posts, hides spam and thanks people on our own posts. Growth comes
from you showing up on other people's posts, and Instagram does not allow
that part to be automated. Bots that comment, like, follow or DM other
accounts get action-blocked or banned, and it takes the page with them.
So this part is 20 minutes a day, by hand, with Claude drafting.

## Daily (20 min, before the 18:30 post)

1. **Comment on 10 posts** (`/ig-comment`): paste the post, get a real comment.
   - 5 *reach*: big quote and poetry pages, comment in the first hour.
   - 3 *peers*: pages your size (1k to 20k) in quotes, poetry, Hindi/Urdu shayari, books.
   - 2 *readers*: bookstagram and journaling accounts whose followers are our readers.
2. **Open `state/review.md`** (the bot writes questions and long comments there).
   Paste them into Claude with `/ig-reply`, then post the replies.
3. **Answer story replies in DMs.** The "reply here" and "finish this" frames send
   replies to the inbox. Answer every one, a line each. This is the funnel.

## Weekly (Sunday, 30 min)

1. Paste the week's insights into `/ig-audit`: which posts got shares and saves.
2. Run `/ig-viral` on 3 quote or poetry pages to see which hooks are working now.
3. Run `/ig-plan` for next week, then ask Claude to write `schedule/week2.json`
   (edit `content.py` with new posts, set `week_start` in config.json, then run
   `content.py` and `render.py`).
4. Pick one cross-post for the Facebook page so the 596 people there follow you over.

## Accounts to find for the list (search these)

`#poetrycommunity`, `#shortpoems`, `#tagore`, `#stoicism`, `#bookstagramindia`,
`#hindipoetry`, `#journaling`. Write down 30 handles you like and rotate them.

## Collabs that work for quote pages

- **Collab posts** (Instagram's invite-collaborator feature) with a poetry page
  your size: one poem, two audiences.
- **Shout-out swaps** with peer pages, story to story.
- **"Add yours"** story prompt once a week ("a line that saved you"), reaches
  beyond followers. Add it by hand: the API can't add stickers.
