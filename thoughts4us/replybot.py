#!/usr/bin/env python3
"""
Handle comments on our own posts, the ig-reply way: sort first, then answer.

  SPAM      links, "promote", "collab", follower selling      -> hidden
  HOSTILE   abuse                                              -> hidden, no reply
  SUPPORT   emoji, "beautiful", "so true", short praise        -> short reply
  PICK      a number answering "comment the number"            -> short reply
  REVIEW    questions, disagreement, anything longer            -> state/review.md

REVIEW comments are the valuable ones and never get a canned answer. Paste
state/review.md into Claude with /ig-reply and send those replies by hand,
or ask Claude to draft them.

This only touches comments under @thoughts4us.official posts, through the official API.
It never comments on, likes, follows or DMs other accounts: that is the kind
of automation that gets accounts restricted.

  python3 replybot.py --dry-run
  python3 replybot.py              # reply_mode in config.json: auto | draft
"""
import argparse
import datetime as dt
import hashlib
import os
import re
import sys

from graph import CONFIG, HERE, Graph, GraphError, load_json, save_json

POSTED = os.path.join(HERE, "state", "posted.json")
HANDLED = os.path.join(HERE, "state", "comments.json")
REVIEW = os.path.join(HERE, "state", "review.md")
LOOKBACK_DAYS = 7

SPAM = re.compile(
    r"(?i)(https?://|www\.|\.com\b|promot|collab|dm (us|me) for|send (us|me) a dm|check (my|our) (page|profile|bio)"
    r"|buy followers|followers? fast|crypto|bitcoin|forex|investment|earn \$|cash ?app|onlyfans|giveaway|brand ambassador)")
HOSTILE = re.compile(r"(?i)\b(idiot|stupid|fuck|bitch|bastard|loser|shut up|kill yourself|kys|chutiya|madarchod|bhenchod)\b")
PRAISE = re.compile(
    r"(?i)^(so )?(true|truth|facts|beautiful|lovely|nice|amazing|wow|so true|well said|this|needed this|love (this|it)"
    r"|awesome|great|perfect|deep|relatable|wonderful|superb|nice one|beautifully (said|written)|exactly|yes+|agreed?)\b")
EMOJI_ONLY = re.compile(r"^[\W_\s‍️]+$")
NUMBER = re.compile(r"^\s*#?([1-9])\s*[.!]*\s*$")

THANKS = [
    "Thank you, {n}.",
    "{n}, glad it found you today.",
    "So glad this landed, {n}.",
    "{n}, thank you for reading.",
    "Means a lot, {n}.",
    "{n}, happy you're here.",
    "Thank you for being here, {n}.",
    "{n}, that makes my day.",
    "Glad it spoke to you, {n}.",
    "{n}, keep it close.",
]
PICKS = [
    "{n}, number {k} is a good one to carry.",
    "Good pick, {n}. {k} stays with me too.",
    "{n}, {k} it is. Thank you for picking.",
]


def classify(text):
    t = text.strip()
    if SPAM.search(t):
        return "SPAM"
    if HOSTILE.search(t):
        return "HOSTILE"
    if NUMBER.match(t):
        return "PICK"
    if "?" in t:
        return "REVIEW"
    if EMOJI_ONLY.match(t) or (PRAISE.search(t) and len(t.split()) <= 6):
        return "SUPPORT"
    return "REVIEW"


def pick(pool, key):
    return pool[int(hashlib.sha1(key.encode()).hexdigest(), 16) % len(pool)]


def name_of(username):
    # "@priya.writes_23" -> "Priya". Falls back to the handle.
    first = re.split(r"[._\d]", username.lstrip("@"))[0]
    return first.capitalize() if len(first) >= 3 else "@" + username


def main():
    ap = argparse.ArgumentParser(description="Sort and answer comments on our own posts.")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    mode = os.environ.get("REPLY_MODE") or CONFIG.get("reply_mode", "draft")
    cap = int(CONFIG.get("max_replies_per_run", 25))
    posted = load_json(POSTED, {})
    handled = load_json(HANDLED, {})
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=LOOKBACK_DAYS)

    media = [(pid, r["media_id"]) for pid, r in posted.items()
             if r.get("media_id") and r.get("media") != "STORIES"
             and dt.datetime.fromisoformat(r["posted_at"]) >= cutoff]
    if not media:
        print("no recent feed posts to check")
        return 0

    g = Graph()
    me = g.get(g.user, fields="username").get("username", "")
    counts, replies, review = {}, 0, []

    for pid, mid in media:
        try:
            data = g.get(f"{mid}/comments", fields="id,text,username,timestamp,replies{username}", limit=50).get("data", [])
        except GraphError as e:
            print(f"  ! {pid}: {e}", file=sys.stderr)
            continue
        for c in data:
            cid, user, text = c["id"], c.get("username", ""), c.get("text", "")
            if cid in handled or user == me:
                continue
            if any(r.get("username") == me for r in c.get("replies", {}).get("data", [])):
                handled[cid] = {"bucket": "ALREADY", "post": pid}
                continue
            bucket = classify(text)
            counts[bucket] = counts.get(bucket, 0) + 1
            action, reply = "none", None
            if bucket in ("SPAM", "HOSTILE"):
                action = "hide"
            elif bucket == "SUPPORT":
                reply = pick(THANKS, cid).format(n=name_of(user))
            elif bucket == "PICK":
                k = NUMBER.match(text).group(1)
                reply = pick(PICKS, cid).format(n=name_of(user), k=k)
            else:
                review.append(f"- **{pid}** @{user}: {text.strip()}  \n  comment id `{cid}`")

            if reply and (mode != "auto" or replies >= cap):
                review.append(f"- **{pid}** @{user}: {text.strip()}  \n  suggested: {reply}  \n  comment id `{cid}`")
                reply, action = None, "queued"

            print(f"  {bucket:8s} @{user}: {text[:60]!r}" + (f"  -> {reply}" if reply else f"  -> {action}"))
            if a.dry_run:
                continue
            try:
                if action == "hide":
                    g.post(cid, hide="true")
                elif reply:
                    g.post(f"{cid}/replies", message=reply)
                    replies += 1
                handled[cid] = {"bucket": bucket, "post": pid, "reply": reply, "action": action}
            except GraphError as e:
                print(f"  ! {cid}: {e}", file=sys.stderr)

    summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "nothing new"
    print(f"comments: {summary}  ·  replied: {replies}")
    if not a.dry_run:
        save_json(HANDLED, handled)
        if review:
            stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            with open(REVIEW, "a") as fh:
                fh.write(f"\n## {stamp}\n\n" + "\n".join(review) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
