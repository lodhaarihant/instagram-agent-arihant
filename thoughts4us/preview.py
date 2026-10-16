#!/usr/bin/env python3
"""Write preview.html: the whole week, day by day, to check before it goes live."""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main(path):
    week = os.path.splitext(os.path.basename(path))[0]
    sched = json.load(open(path))
    manifest = json.load(open(os.path.join(HERE, "media", week, "manifest.json")))
    days = {}
    for p in sched["posts"]:
        days.setdefault(p["at"][:10], []).append(p)

    out = ["<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>",
           f"<title>Thoughts4us {week}</title><style>",
           "body{font:15px/1.45 -apple-system,system-ui,sans-serif;margin:0;padding:24px;background:#f6f3ee;color:#222}",
           "h2{margin:32px 0 8px}.row{display:flex;gap:14px;overflow-x:auto;padding-bottom:10px}",
           ".card{flex:0 0 260px;background:#fff;border-radius:10px;padding:10px;box-shadow:0 1px 3px #0002}",
           ".card img,.card video{width:100%;border-radius:6px;display:block}.strip{display:flex;gap:4px;overflow-x:auto}",
           ".strip img{width:120px;flex:0 0 120px}.meta{font-weight:600;margin:6px 0}.cap{white-space:pre-wrap;font-size:13px;color:#444}",
           ".story{flex-basis:160px}</style>",
           f"<h1>{html.escape(sched['handle'])} &middot; {week}</h1>",
           "<p>Feed posts and stories in posting order (IST). Captions are exactly what gets published.</p>"]
    for day, posts in days.items():
        out.append(f"<h2>{day}</h2><div class=row>")
        for p in posts:
            files = manifest.get(p["id"], [])
            story = p["media"] == "STORIES"
            out.append(f"<div class='card{' story' if story else ''}'><div class=meta>{p['at'][11:16]} &middot; {p['media'].lower()}</div>")
            if p["media"] == "REELS":
                out.append(f"<video src='{files[0]}' poster='{files[1]}' controls muted playsinline></video>")
            elif p["media"] == "CAROUSEL":
                out.append("<div class=strip>" + "".join(f"<img src='{f}' loading=lazy>" for f in files) + "</div>")
            elif files:
                out.append(f"<img src='{files[0]}' loading=lazy>")
            if "caption" in p:
                out.append(f"<div class=cap>{html.escape(p['caption'])}</div>")
            out.append("</div>")
        out.append("</div>")
    dest = os.path.join(HERE, "preview.html")
    open(dest, "w").write("\n".join(out))
    print(dest)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "schedule", "week1.json"))
