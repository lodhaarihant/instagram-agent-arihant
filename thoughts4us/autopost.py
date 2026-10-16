#!/usr/bin/env python3
"""
Publish every scheduled post that is due and not yet posted.

Runs on a timer (GitHub Actions, see .github/workflows/thoughts4us.yml). Each
run looks at schedule/*.json, finds posts whose time has passed, publishes
them through the Instagram Graph API and records the result in
state/posted.json so nothing goes out twice.

  python3 autopost.py --dry-run                  # what would go out right now
  python3 autopost.py --dry-run --now 2026-10-19T13:05:00+05:30
  python3 autopost.py                            # publish for real

Media must be reachable at a public URL: media_base_url in config.json (or the
MEDIA_BASE_URL env var) + the path in media/<week>/manifest.json.
"""
import argparse
import datetime as dt
import glob
import os
import sys

from graph import CONFIG, HERE, Graph, GraphError, load_json, save_json

STATE = os.path.join(HERE, "state", "posted.json")
MAX_LATE = {"STORIES": dt.timedelta(hours=2), "default": dt.timedelta(hours=6)}
MAX_ATTEMPTS = 3


def due_posts(now):
    for sched_path in sorted(glob.glob(os.path.join(HERE, "schedule", "*.json"))):
        week = os.path.splitext(os.path.basename(sched_path))[0]
        sched = load_json(sched_path, {"posts": []})
        manifest = load_json(os.path.join(HERE, "media", week, "manifest.json"), {})
        for p in sched["posts"]:
            at = dt.datetime.fromisoformat(p["at"])
            if at <= now:
                yield p, at, manifest.get(p["id"], [])


def url_for(base, rel):
    return base.rstrip("/") + "/" + "/".join(rel.split(os.sep))


def publish(g, p, files, base):
    urls = [url_for(base, f) for f in files]
    m = p["media"]
    if m == "IMAGE":
        c = g.image(urls[0], caption=p["caption"])
    elif m == "STORIES":
        c = g.image(urls[0], story=True)
    elif m == "CAROUSEL":
        c = g.carousel(urls, p["caption"])
    elif m == "REELS":
        video = next(u for u in urls if u.endswith(".mp4"))
        cover = next((u for u in urls if u.endswith(".jpg")), None)
        c = g.reel(video, p["caption"], cover)
    else:
        raise GraphError(f"unknown media type {m}")
    return g.publish(c)


def main():
    ap = argparse.ArgumentParser(description="Publish due Instagram posts.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--now", help="pretend the time is this ISO timestamp")
    ap.add_argument("--limit", type=int, default=6, help="max posts per run")
    a = ap.parse_args()

    now = dt.datetime.fromisoformat(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
    base = os.environ.get("MEDIA_BASE_URL") or CONFIG.get("media_base_url", "")
    state = load_json(STATE, {})

    todo, skipped = [], 0
    for p, at, files in due_posts(now):
        rec = state.get(p["id"], {})
        if rec.get("media_id") or rec.get("skipped") or rec.get("attempts", 0) >= MAX_ATTEMPTS:
            continue
        if now - at > MAX_LATE.get(p["media"], MAX_LATE["default"]):
            # A good-morning story at 3pm is worse than no story.
            state[p["id"]] = {"skipped": "too late", "at": now.isoformat()}
            skipped += 1
            continue
        if not files:
            print(f"  ! {p['id']}: no rendered files, run render.py", file=sys.stderr)
            continue
        todo.append((p, files))

    todo = todo[: a.limit]
    print(f"{now.isoformat()}  due: {len(todo)}  skipped as late: {skipped}")
    if a.dry_run:
        for p, files in todo:
            print(f"  would post {p['id']:24s} {p['media']:9s} {', '.join(url_for(base or '<MEDIA_BASE_URL>', f) for f in files[:2])}")
        return 0
    if not todo:
        save_json(STATE, state)
        return 0
    if not base:
        print("media_base_url is empty. Set it in config.json or MEDIA_BASE_URL.", file=sys.stderr)
        return 2

    g = Graph()
    try:
        used, total = g.quota()
        print(f"publishing quota: {used} used of {total} in the last 24h")
    except GraphError as e:
        print(f"  (quota check failed: {e})")

    failures = 0
    for p, files in todo:
        rec = state.setdefault(p["id"], {})
        try:
            media_id, link = publish(g, p, files, base)
            rec.update({"media_id": media_id, "permalink": link, "media": p["media"],
                        "posted_at": dt.datetime.now(dt.timezone.utc).isoformat()})
            rec.pop("error", None)
            print(f"  posted {p['id']:24s} {link}")
        except (GraphError, OSError) as e:
            rec["attempts"] = rec.get("attempts", 0) + 1
            rec["error"] = str(e)[:500]
            failures += 1
            print(f"  FAILED {p['id']}: {e}", file=sys.stderr)
        save_json(STATE, state)
    return 1 if failures and failures == len(todo) else 0


if __name__ == "__main__":
    sys.exit(main())
