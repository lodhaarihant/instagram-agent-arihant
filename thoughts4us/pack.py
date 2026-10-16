#!/usr/bin/env python3
"""
Build an upload pack for scheduling by hand in Meta Business Suite.

  python3 pack.py schedule/week1.json

Writes upload/<week>/<NN-Day-DDMon>/ with every file renamed in posting order
(01-0730-story.jpg, 02-0800-post.jpg, ...) and a SCHEDULE.txt that lists
each item's time, type, files and caption, ready to copy and paste.
"""
import datetime as dt
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = {"IMAGE": "post", "CAROUSEL": "carousel", "REELS": "reel", "STORIES": "story"}
HOW = {
    "IMAGE": "Create post > Instagram > add photo",
    "CAROUSEL": "Create post > Instagram > add all slides in order",
    "REELS": "Create reel > Instagram > add video (cover: the -cover.jpg)",
    "STORIES": "Create story > Instagram > add photo",
}


def main(path):
    week = os.path.splitext(os.path.basename(path))[0]
    sched = json.load(open(path))
    manifest = json.load(open(os.path.join(HERE, "media", week, "manifest.json")))
    root = os.path.join(HERE, "upload", week)
    shutil.rmtree(root, ignore_errors=True)

    days = {}
    for p in sched["posts"]:
        days.setdefault(p.get("day") or p["at"][:10], []).append(p)

    for n, (day, posts) in enumerate(sorted(days.items()), 1):
        d = dt.date.fromisoformat(day)
        folder = os.path.join(root, f"{n:02d}-{d:%a-%d%b}")
        os.makedirs(folder)
        lines = [f"{sched['handle']}  ·  {d:%A %d %B %Y}  ·  times are IST", "=" * 64, ""]
        for i, p in enumerate(posts, 1):
            hhmm = p["at"][11:16]
            kind = LABEL[p["media"]]
            names = []
            for k, src in enumerate(manifest[p["id"]], 1):
                ext = os.path.splitext(src)[1]
                suffix = ""
                if p["media"] == "CAROUSEL":
                    suffix = f"-slide{k:02d}"
                elif src.endswith("-cover.jpg"):
                    suffix = "-cover"
                name = f"{i:02d}-{hhmm.replace(':', '')}-{kind}{suffix}{ext}"
                shutil.copy(os.path.join(HERE, src), os.path.join(folder, name))
                names.append(name)
            lines.append(f"[{i:02d}]  {hhmm}  {kind.upper()}")
            lines.append(f"      how:   {HOW[p['media']]}")
            lines.append(f"      files: {', '.join(names)}")
            if p.get("caption"):
                lines += ["      caption (copy everything between the lines):", "      " + "-" * 50]
                lines += [p["caption"], "      " + "-" * 50]
            lines.append("")
        open(os.path.join(folder, "SCHEDULE.txt"), "w").write("\n".join(lines))
        print(f"{os.path.relpath(folder, HERE)}  {len(posts)} items")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "schedule", "week1.json"))
