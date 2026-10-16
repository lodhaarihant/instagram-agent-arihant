#!/usr/bin/env python3
"""
Render every post in a schedule file to the images and reels Instagram wants.

  feed      1080x1350 JPEG (4:5)
  stories   1080x1920 JPEG, text kept between y=250 and y=1600
  reels     1080x1920 H.264 MP4 with a silent audio track, plus a cover JPEG

Usage:
  ../.venv/bin/python render.py schedule/week1.json
  ../.venv/bin/python render.py schedule/week1.json --only d1-f3-carousel

Needs Pillow and imageio-ffmpeg (pip install Pillow imageio-ffmpeg).
Fonts are the macOS system serifs; set T4U_SERIF / T4U_SANS to override.
"""
import argparse
import json
import math
import os
import random
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FEED = (1080, 1350)
STORY = (1080, 1920)

SERIF = os.environ.get("T4U_SERIF", "/System/Library/Fonts/Supplemental/Georgia.ttf")
SERIF_I = os.environ.get("T4U_SERIF_ITALIC", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf")
SANS = os.environ.get("T4U_SANS", "/System/Library/Fonts/Avenir Next.ttc")


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def sans(size, bold=False):
    # Avenir Next.ttc: 0 Bold, 7 Regular, 2 Demi Bold. Fall back quietly.
    try:
        return font(SANS, size, 2 if bold else 7)
    except OSError:
        return font(SERIF, size)


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            test = (line + " " + w).strip()
            if draw.textlength(test, font=fnt) <= width or not line:
                line = test
            else:
                lines.append(line)
                line = w
        lines.append(line)
    return lines


def fit(draw, text, path, width, max_h, start, low=34, italic=False):
    """Largest font size at which the wrapped text fits the box.

    Prefers a size where the author's own line breaks survive unbroken, so a
    three-line thought stays three lines instead of five ragged ones."""
    want = len(text.split("\n"))
    if want > 1:
        size = start
        while size >= max(low, 44):
            f = font(SERIF_I if italic else path, size)
            lines = wrap(draw, text, f, width)
            if len(lines) == want and len(lines) * size * 1.32 <= max_h:
                return f, lines
            size -= 2
    size = start
    while size > low:
        f = font(SERIF_I if italic else path, size)
        lines = wrap(draw, text, f, width)
        if len(lines) * size * 1.32 <= max_h:
            return f, lines
        size -= 4
    f = font(SERIF_I if italic else path, low)
    return f, wrap(draw, text, f, width)


def block(draw, lines, fnt, x, y, fill, spacing=1.32, align="left", width=None):
    size = fnt.size
    for ln in lines:
        lx = x
        if align == "center" and width:
            lx = x + (width - draw.textlength(ln, font=fnt)) / 2
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += size * spacing
    return y


def dots(img, pal, seed, corner="br", count=140, spread=360):
    """The Thoughts4us motif: a loose cluster of coloured dots in one corner."""
    rnd = random.Random(seed)
    w, h = img.size
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = w - 40 if "r" in corner else 40
    cy = h - 40 if "b" in corner else 40
    for _ in range(count):
        r = abs(rnd.gauss(0, spread * 0.55))
        a = rnd.uniform(0, 6.283)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        s = max(3, int(rnd.uniform(4, 16) * (1 - min(r / (spread * 1.6), 0.8))))
        alpha = int(255 * max(0.18, 1 - r / (spread * 1.5)))
        col = rgb(rnd.choice(pal["dots"])) + (alpha,)
        d.ellipse([x - s, y - s, x + s, y + s], fill=col)
    img.alpha_composite(layer)


def canvas(size, pal):
    return Image.new("RGBA", size, rgb(pal["bg"]) + (255,))


def footer(draw, size, pal, handle, page=None):
    w, h = size
    f = sans(30, bold=True)
    draw.text((90, h - 110), handle, font=f, fill=rgb(pal["ink"]) + (170,))
    if page:
        pf = sans(30)
        tw = draw.textlength(page, font=pf)
        draw.text((w - 90 - tw, 80), page, font=pf, fill=rgb(pal["ink"]) + (150,))


def save(img, path):
    img.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
    return path


# ---------------------------------------------------------------- feed posts

def quote_card(p, pal, handle, out):
    img = canvas(FEED, pal)
    dots(img, pal, p["id"], "br", 120, 320)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((80, 90), "“", font=font(SERIF, 260), fill=rgb(pal["accent"]))
    f, lines = fit(d, p["quote"], SERIF, 900, 640, 76)
    y = block(d, lines, f, 90, 360, rgb(pal["ink"]))
    y += 40
    d.rectangle([90, y, 170, y + 5], fill=rgb(pal["accent"]))
    y += 34
    d.text((90, y), p["author"].upper(), font=sans(36, bold=True), fill=rgb(pal["accent"]))
    d.text((90, y + 52), p["source"], font=font(SERIF_I, 30), fill=rgb(pal["ink"]) + (190,))
    footer(d, FEED, pal, handle)
    return [save(img, out + ".jpg")]


def thought_card(p, pal, handle, out):
    img = canvas(FEED, pal)
    dots(img, pal, p["id"], "tl", 110, 300)
    d = ImageDraw.Draw(img, "RGBA")
    f, lines = fit(d, p["text"], SERIF, 880, 700, 84)
    total = len(lines) * f.size * 1.32
    y = (FEED[1] - total) / 2
    block(d, lines, f, 100, y, rgb(pal["ink"]), align="center", width=880)
    label = "THOUGHT'S"
    lf = sans(30, bold=True)
    d.text(((FEED[0] - d.textlength(label, font=lf)) / 2, FEED[1] - 230), label, font=lf, fill=rgb(pal["accent"]))
    footer(d, FEED, pal, handle)
    return [save(img, out + ".jpg")]


def carousel(p, pal, handle, out):
    deck = p["deck"]
    pages = []
    ink, acc = rgb(pal["ink"]), rgb(pal["accent"])

    # cover
    pages.append(("cover", deck["cover"], deck["sub"]))
    pages.append(("stake", deck["stake"], ""))
    for s in deck["slides"]:
        pages.append(("slide",) + tuple(s))
    if deck.get("recap_poem"):
        pages.append(("poem", deck["recap_poem"], deck["recap_credit"]))
    else:
        pages.append(("recap", deck["recap"], ""))
    pages.append(("cta", deck["cta"], ""))

    files, n = [], len(pages)
    for i, pg in enumerate(pages, 1):
        img = canvas(FEED, pal)
        kind = pg[0]
        dots(img, pal, f"{p['id']}-{i}", "br" if i % 2 else "tl", 90 if kind != "cover" else 170, 300 if kind != "cover" else 420)
        d = ImageDraw.Draw(img, "RGBA")
        if kind == "cover":
            f, lines = fit(d, pg[1], SERIF, 840, 620, 120)
            y = block(d, lines, f, 120, 340, ink, spacing=1.18)
            d.rectangle([120, y + 30, 220, y + 36], fill=acc)
            sf = font(SERIF_I, 40)
            block(d, wrap(d, pg[2], sf, 840), sf, 120, y + 70, ink + (200,))
            d.text((120, FEED[1] - 230), "SWIPE FOR MORE", font=sans(32, bold=True), fill=acc)
        elif kind == "stake":
            f, lines = fit(d, pg[1], SERIF, 860, 700, 70)
            total = len(lines) * f.size * 1.32
            block(d, lines, f, 110, (FEED[1] - total) / 2, ink)
        elif kind == "slide":
            _, main, credit, note = pg
            italic = p["deck"].get("kind") == "poem"
            f, lines = fit(d, main, SERIF, 860, 560, 76, italic=italic)
            y = block(d, lines, f, 110, 260, ink)
            if credit:
                d.text((110, y + 30), credit.upper(), font=sans(30, bold=True), fill=acc)
                y += 70
            nf = sans(38)
            y = max(y + 70, 900)
            d.rectangle([110, y - 30, 190, y - 25], fill=acc)
            block(d, wrap(d, note, nf, 860), nf, 110, y, ink + (215,), spacing=1.4)
        elif kind == "recap":
            d.text((110, 200), "IN SHORT", font=sans(34, bold=True), fill=acc)
            items = pg[1]
            size = 58 if len(items) <= 5 else 52
            f = font(SERIF, size)
            y = 290
            for k, it in enumerate(items, 1):
                d.text((110, y), f"{k}.", font=f, fill=acc)
                block(d, wrap(d, it, f, 780), f, 200, y, ink)
                y += size * 1.32 * len(wrap(d, it, f, 780)) + 34
        elif kind == "poem":
            f, lines = fit(d, pg[1], SERIF, 860, 640, 60, italic=True)
            y = block(d, lines, f, 110, 300, ink, spacing=1.45)
            d.text((110, y + 40), pg[2].upper(), font=sans(30, bold=True), fill=acc)
        elif kind == "cta":
            f, lines = fit(d, pg[1], SERIF, 840, 560, 80)
            total = len(lines) * f.size * 1.32
            y = block(d, lines, f, 120, (FEED[1] - total) / 2 - 60, ink)
            d.text((120, y + 50), "Follow " + handle + " for more", font=sans(34, bold=True), fill=acc)
        footer(d, FEED, pal, handle, f"{i}/{n}")
        files.append(save(img, f"{out}-{i:02d}.jpg"))
    return files


def reel(p, pal, handle, out):
    lines = p["lines"]
    tmp = tempfile.mkdtemp()
    frames = []
    for k in range(len(lines) + 1):
        img = canvas(STORY, pal)
        dots(img, pal, p["id"], "br", 160, 460)
        d = ImageDraw.Draw(img, "RGBA")
        f = font(SERIF_I, 78)
        wrapped = [wrap(d, ln, f, 880) for ln in lines]
        total = sum(len(w) for w in wrapped) * 78 * 1.4 + (len(lines) - 1) * 40
        y = (STORY[1] - total) / 2 - 60
        for j, wl in enumerate(wrapped):
            if j < k:
                block(d, wl, f, 100, y, rgb(pal["ink"]), spacing=1.4, align="center", width=880)
            y += len(wl) * 78 * 1.4 + 40
        lf = sans(32, bold=True)
        lab = handle
        d.text(((STORY[0] - d.textlength(lab, font=lf)) / 2, 1560), lab, font=lf, fill=rgb(pal["accent"]))
        path = os.path.join(tmp, f"f{k}.png")
        img.convert("RGB").save(path)
        frames.append(path)
    cover = save(Image.open(frames[-1]).convert("RGBA"), out + "-cover.jpg")

    # concat demuxer: one line appears every 1.8s, then hold the full poem
    durations = [0.8] + [1.8] * (len(lines) - 1) + [4.0]
    listing = os.path.join(tmp, "list.txt")
    with open(listing, "w") as fh:
        for fr, du in zip(frames, durations):
            fh.write(f"file '{fr}'\nduration {du}\n")
        fh.write(f"file '{frames[-1]}'\n")
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = out + ".mp4"
    total = sum(durations)
    subprocess.run([
        ff, "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", listing,
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-profile:v", "high", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k", "-t", f"{total:.1f}", "-movflags", "+faststart", mp4,
    ], check=True)
    return [mp4, cover]


# ------------------------------------------------------------------- stories

def story(p, pal, handle, out):
    img = canvas(STORY, pal)
    dots(img, pal, p["id"], "tr" if p["story"] in ("morning", "night") else "bl", 150, 420)
    d = ImageDraw.Draw(img, "RGBA")
    ink, acc = rgb(pal["ink"]), rgb(pal["accent"])
    kind = p["story"]
    top, bottom = 250, 1600

    def centered(text, size, y, fnt_path=SERIF, colour=ink, italic=False):
        f, lines = fit(d, text, fnt_path, 860, bottom - y, size, italic=italic)
        return block(d, lines, f, 110, y, colour, align="center", width=860)

    if kind in ("morning", "night", "fragment"):
        f, lines = fit(d, p["text"], SERIF, 860, 800, 88, italic=(kind == "fragment"))
        total = len(lines) * f.size * 1.32
        block(d, lines, f, 110, (STORY[1] - total) / 2 - 80, ink, align="center", width=860)
    elif kind == "quote":
        d.text((110, 380), "“", font=font(SERIF, 220), fill=acc)
        f, lines = fit(d, p["quote"], SERIF, 860, 700, 70)
        y = block(d, lines, f, 110, 620, ink)
        d.text((110, y + 50), p["author"].upper(), font=sans(32, bold=True), fill=acc)
    elif kind == "choice":
        centered("This or that?", 64, 420, colour=acc)
        bf = font(SERIF, 76)
        for k, (label, y) in enumerate(((p["a"], 700), (p["b"], 1020)), 1):
            d.rounded_rectangle([140, y, 940, y + 220], radius=40, outline=acc, width=5)
            txt = f"{k}  {label}"
            lines = wrap(d, txt, bf, 720)
            ly = y + (220 - len(lines) * 76 * 1.2) / 2
            block(d, lines, bf, 140, ly, ink, spacing=1.2, align="center", width=800)
        f = sans(40)
        t = "Reply 1 or 2"
        d.text(((STORY[0] - d.textlength(t, font=f)) / 2, 1360), t, font=f, fill=ink + (210,))
    elif kind in ("prompt", "pointer"):
        y = centered(p["text"], 84, 560)
        f = sans(40, bold=True)
        t = p["note"]
        d.text(((STORY[0] - d.textlength(t, font=f)) / 2, max(y + 80, 1250)), t, font=f, fill=acc)

    lf = sans(30, bold=True)
    d.text(((STORY[0] - d.textlength(handle, font=lf)) / 2, 1500), handle, font=lf, fill=ink + (150,))
    return [save(img, out + ".jpg")]


RENDER = {"quote": quote_card, "thought": thought_card, "carousel": carousel, "reel": reel, "story": story}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("schedule")
    ap.add_argument("--only", help="render a single post id")
    a = ap.parse_args()

    sched = json.load(open(a.schedule))
    week = os.path.splitext(os.path.basename(a.schedule))[0]
    outdir = os.path.join(HERE, "media", week)
    os.makedirs(outdir, exist_ok=True)
    manifest_path = os.path.join(outdir, "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}

    for p in sched["posts"]:
        if a.only and p["id"] != a.only:
            continue
        pal = sched["palettes"][p["palette"]]
        files = RENDER[p["kind"]](p, pal, sched["handle"], os.path.join(outdir, p["id"]))
        manifest[p["id"]] = [os.path.relpath(f, HERE) for f in files]
        print(f"{p['id']:24s} {len(files)} file(s)")

    json.dump(manifest, open(manifest_path, "w"), indent=1)
    print(f"manifest: {os.path.relpath(manifest_path, HERE)}  ({len(manifest)} posts)")


if __name__ == "__main__":
    main()
