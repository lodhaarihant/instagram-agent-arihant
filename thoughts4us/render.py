#!/usr/bin/env python3
"""
Render every post in a schedule file to the images and reels Instagram wants.

Look: light paper, a small drawn motif, centred book serif, lots of air.
Print-quote style, one motif per weekday so the grid stays varied.

  feed      1080x1350 JPEG (4:5)
  stories   1080x1920 JPEG, text kept between y=250 and y=1600
  reels     1080x1920 H.264 MP4 with a silent audio track, plus a cover JPEG

Usage:
  ../.venv/bin/python render.py schedule/week1.json
  ../.venv/bin/python render.py schedule/week1.json --only d1-f3-carousel

Needs Pillow and imageio-ffmpeg (pip install Pillow imageio-ffmpeg).
Fonts are macOS system fonts (Baskerville, Avenir Next).
"""
import argparse
import datetime as dt
import json
import math
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FEED = (1080, 1350)
STORY = (1080, 1920)

SERIF = "/System/Library/Fonts/Supplemental/Baskerville.ttc"   # 0 Regular, 2 Italic
SANS = "/System/Library/Fonts/Avenir Next.ttc"                 # 2 Demi Bold, 5 Medium, 7 Regular

# Indexed by weekday (0 = Monday), same as content.py.
THEMES = [
    {"bg": "#F7F3EC", "motif": "butterfly", "a": "#E6ABA8", "b": "#C4807D"},
    {"bg": "#EFE8DD", "motif": "sprig", "a": "#A3B595", "b": "#6F8A63"},
    {"bg": "#F8F7F3", "motif": "moon", "a": "#DDB774", "b": "#B8904A"},
    {"bg": "#F6EEE9", "motif": "flower", "a": "#E9A9A3", "b": "#8FA585"},
    {"bg": "#F4F0E5", "motif": "birds", "a": "#6F6964", "b": "#9B948E"},
    {"bg": "#F2F1ED", "motif": "feather", "a": "#BCC7CF", "b": "#7F92A1"},
    {"bg": "#F2EADC", "motif": "sun", "a": "#E5AE72", "b": "#C98A4E"},
]
INK = (46, 41, 37)
MUTED = (138, 128, 121)


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def serif(size, italic=False):
    return ImageFont.truetype(SERIF, size, index=2 if italic else 0)


def sans(size, weight="demi"):
    return ImageFont.truetype(SANS, size, index={"demi": 2, "medium": 5, "regular": 7}[weight])


# ------------------------------------------------------------------- paper

_PAPER = {}


def paper(size, theme):
    """Flat paper colour, a soft lighter centre and fine grain, like a print."""
    key = (size, theme["bg"])
    if key not in _PAPER:
        w, h = size
        base = Image.new("RGB", size, rgb(theme["bg"]))
        glow = Image.new("L", size, 0)
        ImageDraw.Draw(glow).ellipse([-w * 0.2, -h * 0.1, w * 1.2, h * 1.1], fill=40)
        glow = glow.filter(ImageFilter.GaussianBlur(w // 4))
        base = Image.composite(Image.new("RGB", size, (255, 255, 255)), base, glow)
        grain = Image.effect_noise(size, 28).convert("RGB")
        _PAPER[key] = Image.blend(base, grain, 0.04)
    return _PAPER[key].convert("RGBA")


# ------------------------------------------------------------------ motifs
# Drawn at 4x on a transparent square, then scaled down, so edges are smooth.

def _ellipse(layer, cx, cy, w, h, angle, fill, outline=None, width=0):
    pad = width + 6
    tmp = Image.new("RGBA", (int(w) + pad * 2, int(h) + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).ellipse([pad, pad, pad + w, pad + h], fill=fill, outline=outline, width=width)
    tmp = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
    layer.alpha_composite(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)))


def m_butterfly(L, S, a, b):
    d = ImageDraw.Draw(L)
    cx, cy = S / 2, S / 2 + S * 0.04
    for side in (1, -1):
        _ellipse(L, cx + side * S * 0.2, cy - S * 0.12, S * 0.42, S * 0.26, side * 32, a + (235,), b + (255,), int(S * 0.008))
        _ellipse(L, cx + side * S * 0.15, cy + S * 0.11, S * 0.3, S * 0.2, -side * 38, a + (215,), b + (255,), int(S * 0.008))
        d.line([(cx, cy - S * 0.16), (cx + side * S * 0.12, cy - S * 0.36)], fill=INK + (200,), width=int(S * 0.007))
        r = S * 0.012
        d.ellipse([cx + side * S * 0.12 - r, cy - S * 0.36 - r, cx + side * S * 0.12 + r, cy - S * 0.36 + r], fill=INK + (220,))
    _ellipse(L, cx, cy, S * 0.035, S * 0.3, 0, INK + (235,))


def m_sprig(L, S, a, b):
    d = ImageDraw.Draw(L)
    pts = [(S * 0.5 + S * 0.12 * math.sin(t * 2.4), S * 0.88 - t * S * 0.76) for t in [i / 40 for i in range(41)]]
    d.line(pts, fill=b + (255,), width=int(S * 0.012), joint="curve")
    for k in range(1, 9):
        x, y = pts[k * 4]
        side = 1 if k % 2 else -1
        _ellipse(L, x + side * S * 0.08, y - S * 0.02, S * 0.17, S * 0.075, 35 * side, a + (235,), b + (255,), int(S * 0.006))
    x, y = pts[-1]
    _ellipse(L, x, y - S * 0.03, S * 0.075, S * 0.15, 0, a + (235,), b + (255,), int(S * 0.006))


def m_moon(L, S, a, b):
    mask = Image.new("L", L.size, 0)
    md = ImageDraw.Draw(mask)
    r = S * 0.3
    cx, cy = S * 0.48, S * 0.52
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=240)
    md.ellipse([cx - r + S * 0.16, cy - r - S * 0.08, cx + r + S * 0.16, cy + r - S * 0.08], fill=0)
    L.paste(Image.new("RGBA", L.size, a + (255,)), (0, 0), mask)
    d = ImageDraw.Draw(L)
    for (x, y, s) in ((0.78, 0.22, 0.03), (0.86, 0.46, 0.02), (0.7, 0.72, 0.016)):
        x, y, s = x * S, y * S, s * S
        d.polygon([(x, y - s * 2), (x + s * 0.5, y - s * 0.5), (x + s * 2, y), (x + s * 0.5, y + s * 0.5),
                   (x, y + s * 2), (x - s * 0.5, y + s * 0.5), (x - s * 2, y), (x - s * 0.5, y - s * 0.5)], fill=b + (255,))


def m_flower(L, S, a, b):
    d = ImageDraw.Draw(L)
    cx, cy = S / 2, S * 0.4
    d.line([(cx, cy), (cx - S * 0.03, S * 0.92)], fill=b + (255,), width=int(S * 0.012))
    _ellipse(L, cx - S * 0.12, S * 0.72, S * 0.2, S * 0.08, 25, b + (220,))
    _ellipse(L, cx + S * 0.1, S * 0.62, S * 0.2, S * 0.08, -30, b + (220,))
    darker = tuple(max(0, c - 40) for c in a)
    for k in range(6):
        ang = k * 60
        rad = math.radians(ang)
        _ellipse(L, cx + math.cos(rad) * S * 0.12, cy - math.sin(rad) * S * 0.12, S * 0.24, S * 0.13, ang,
                 a + (230,), darker + (255,), int(S * 0.006))
    r = S * 0.05
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(236, 192, 110, 255))


def m_birds(L, S, a, b):
    d = ImageDraw.Draw(L)
    w = int(S * 0.014)
    for (x, y, s, col) in ((0.36, 0.42, 0.26, a), (0.66, 0.3, 0.18, b), (0.6, 0.6, 0.13, b)):
        x, y, s = x * S, y * S, s * S
        d.arc([x - s, y - s * 0.5, x, y + s * 0.5], 200, 330, fill=col + (255,), width=w)
        d.arc([x, y - s * 0.5, x + s, y + s * 0.5], 210, 340, fill=col + (255,), width=w)


def m_feather(L, S, a, b):
    tmp = Image.new("RGBA", L.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    cx = S / 2
    d.ellipse([cx - S * 0.13, S * 0.1, cx + S * 0.13, S * 0.8], fill=a + (235,))
    d.line([(cx, S * 0.06), (cx, S * 0.94)], fill=b + (255,), width=int(S * 0.012))
    for k in range(12):
        y = S * (0.18 + k * 0.05)
        for side in (1, -1):
            d.line([(cx, y + S * 0.04), (cx + side * S * 0.11, y)], fill=b + (150,), width=int(S * 0.005))
    L.alpha_composite(tmp.rotate(-35, resample=Image.BICUBIC))


def m_sun(L, S, a, b):
    d = ImageDraw.Draw(L)
    cx, cy, r = S / 2, S / 2, S * 0.17
    for k in range(12):
        ang = math.radians(k * 30)
        d.line([(cx + math.cos(ang) * r * 1.45, cy + math.sin(ang) * r * 1.45),
                (cx + math.cos(ang) * r * 2.1, cy + math.sin(ang) * r * 2.1)], fill=b + (255,), width=int(S * 0.016))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a + (245,))


MOTIFS = {"butterfly": m_butterfly, "sprig": m_sprig, "moon": m_moon, "flower": m_flower,
          "birds": m_birds, "feather": m_feather, "sun": m_sun}
_MOTIF_CACHE = {}


def motif(img, theme, cx, cy, size):
    key = (theme["motif"], size)
    if key not in _MOTIF_CACHE:
        S = size * 4
        L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        MOTIFS[theme["motif"]](L, S, rgb(theme["a"]), rgb(theme["b"]))
        _MOTIF_CACHE[key] = L.resize((size, size), Image.LANCZOS)
    img.alpha_composite(_MOTIF_CACHE[key], (int(cx - size / 2), int(cy - size / 2)))


# -------------------------------------------------------------------- text

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


def fit(draw, text, width, max_h, start, low=34, italic=False, spacing=1.42):
    """Largest size that fits; prefers sizes where the author's line breaks survive."""
    want = len(text.split("\n"))
    sizes = range(start, low - 1, -2)
    if want > 1:
        for s in sizes:
            f = serif(s, italic)
            lines = wrap(draw, text, f, width)
            if len(lines) == want and len(lines) * s * spacing <= max_h:
                return f, lines
    for s in sizes:
        f = serif(s, italic)
        lines = wrap(draw, text, f, width)
        if len(lines) * s * spacing <= max_h:
            return f, lines
    f = serif(low, italic)
    return f, wrap(draw, text, f, width)


def centre(draw, lines, fnt, y, fill=INK, spacing=1.42):
    W = draw.im.size[0]
    for ln in lines:
        draw.text(((W - draw.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=fill)
        y += fnt.size * spacing
    return y


def spaced(draw, text, fnt, y, fill=MUTED, track=4):
    """Letter-spaced capitals, centred."""
    text = text.upper()
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    x = (draw.im.size[0] - total) / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + track
    return y + fnt.size * 1.5


def handle_mark(draw, size, handle, y=None):
    f = serif(28, italic=True)
    y = y if y is not None else size[1] - 120
    draw.text(((size[0] - draw.textlength(handle, font=f)) / 2, y), handle, font=f, fill=MUTED)


def page_no(draw, size, txt):
    f = sans(24, "medium")
    draw.text((size[0] - 80 - draw.textlength(txt, font=f), 70), txt, font=f, fill=MUTED)


def save(img, path):
    img.convert("RGB").save(path, "JPEG", quality=95, subsampling=0, optimize=True)
    return path


def stack(size, parts, motif_size, centre_y, gap=64):
    """Lay out [motif] + parts as one block centred on centre_y. Returns each part's top y."""
    heights = ([motif_size] if motif_size else [])
    for kind, payload in parts:
        heights.append(len(payload[1]) * payload[0].size * payload[2] if kind == "text" else payload)
    total = sum(heights) + gap * (len(heights) - 1)
    y = centre_y - total / 2
    ys = []
    for h in heights:
        ys.append(y)
        y += h + gap
    return ys


# -------------------------------------------------------------- feed posts

def quote_card(p, th, handle, out):
    img = paper(FEED, th)
    d = ImageDraw.Draw(img, "RGBA")
    f, lines = fit(d, p["quote"], 820, 520, 58, 38)
    ys = stack(FEED, [("text", (f, lines, 1.42)), ("space", 80)], 190, FEED[1] / 2 + 10)
    motif(img, th, FEED[0] / 2, ys[0] + 95, 190)
    centre(d, lines, f, ys[1])
    y = spaced(d, p["author"], sans(24, "demi"), ys[2] - 20, INK, 5)
    centre(d, [p["source"]], serif(24, italic=True), y - 4, MUTED)
    handle_mark(d, FEED, handle)
    return [save(img, out + ".jpg")]


def thought_card(p, th, handle, out):
    img = paper(FEED, th)
    d = ImageDraw.Draw(img, "RGBA")
    f, lines = fit(d, p["text"], 840, 560, 64, 40)
    ys = stack(FEED, [("text", (f, lines, 1.42))], 170, FEED[1] / 2)
    motif(img, th, FEED[0] / 2, ys[0] + 85, 170)
    centre(d, lines, f, ys[1])
    handle_mark(d, FEED, handle)
    return [save(img, out + ".jpg")]


def carousel(p, th, handle, out):
    deck = p["deck"]
    poem = deck.get("kind") == "poem"
    pages = [("cover", deck["cover"], deck["sub"]), ("stake", deck["stake"], "")]
    pages += [("slide",) + tuple(s) for s in deck["slides"]]
    pages.append(("poem", deck["recap_poem"], deck["recap_credit"]) if deck.get("recap_poem") else ("recap", deck["recap"], ""))
    pages.append(("cta", deck["cta"], ""))

    files, n = [], len(pages)
    for i, pg in enumerate(pages, 1):
        img = paper(FEED, th)
        d = ImageDraw.Draw(img, "RGBA")
        kind = pg[0]
        if kind == "cover":
            f, lines = fit(d, pg[1], 820, 420, 84, 56, spacing=1.25)
            sf = serif(34, italic=True)
            sub = wrap(d, pg[2], sf, 780)
            ys = stack(FEED, [("text", (f, lines, 1.25)), ("text", (sf, sub, 1.4))], 210, FEED[1] / 2 - 30, 56)
            motif(img, th, FEED[0] / 2, ys[0] + 105, 210)
            centre(d, lines, f, ys[1], spacing=1.25)
            centre(d, sub, sf, ys[2], MUTED, spacing=1.4)
            spaced(d, "swipe  >", sans(22, "demi"), FEED[1] - 190, MUTED, 6)
        elif kind == "stake":
            f, lines = fit(d, pg[1], 800, 600, 56, 38)
            ys = stack(FEED, [("text", (f, lines, 1.42))], 110, FEED[1] / 2 - 20)
            motif(img, th, FEED[0] / 2, ys[0] + 55, 110)
            centre(d, lines, f, ys[1])
        elif kind == "slide":
            _, main, credit, note = pg
            f, lines = fit(d, main, 820, 520, 60, 38, italic=poem)
            nf = sans(30, "regular")
            nl = wrap(d, note, nf, 760)
            parts = [("text", (f, lines, 1.42))]
            if credit:
                parts.append(("space", 30))
            parts.append(("text", (nf, nl, 1.5)))
            ys = stack(FEED, parts, 90, FEED[1] / 2 - 10, 54)
            motif(img, th, FEED[0] / 2, ys[0] + 45, 90)
            centre(d, lines, f, ys[1])
            if credit:
                spaced(d, credit, sans(22, "demi"), ys[2] - 6, INK, 4)
            yr = ys[-1] - 28
            d.line([(FEED[0] / 2 - 40, yr), (FEED[0] / 2 + 40, yr)], fill=rgb(th["b"]) + (255,), width=3)
            centre(d, nl, nf, ys[-1], MUTED, spacing=1.5)
        elif kind == "recap":
            items = [f"{k}.  {it}" for k, it in enumerate(pg[1], 1)]
            f = serif(50 if len(items) <= 5 else 46)
            ys = stack(FEED, [("space", 36), ("text", (f, items, 1.6))], 0, FEED[1] / 2)
            spaced(d, "in short", sans(24, "demi"), ys[0], rgb(th["b"]), 6)
            centre(d, items, f, ys[1], spacing=1.6)
        elif kind == "poem":
            f, lines = fit(d, pg[1], 820, 640, 52, 36, italic=True, spacing=1.55)
            ys = stack(FEED, [("text", (f, lines, 1.55)), ("space", 30)], 120, FEED[1] / 2 - 20)
            motif(img, th, FEED[0] / 2, ys[0] + 60, 120)
            centre(d, lines, f, ys[1], spacing=1.55)
            spaced(d, pg[2], sans(22, "demi"), ys[2], INK, 4)
        elif kind == "cta":
            f, lines = fit(d, pg[1], 800, 420, 62, 40)
            ys = stack(FEED, [("text", (f, lines, 1.42)), ("space", 30)], 170, FEED[1] / 2 - 30)
            motif(img, th, FEED[0] / 2, ys[0] + 85, 170)
            centre(d, lines, f, ys[1])
            spaced(d, "follow " + handle, sans(24, "demi"), ys[2], rgb(th["b"]), 3)
        page_no(d, FEED, f"{i} / {n}")
        handle_mark(d, FEED, handle)
        files.append(save(img, f"{out}-{i:02d}.jpg"))
    return files


def reel(p, th, handle, out):
    lines = p["lines"]
    tmp = tempfile.mkdtemp()
    frames = []
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = serif(66, italic=True)
    wrapped = [wrap(probe, ln, f, 860) for ln in lines]
    block = sum(len(w) for w in wrapped) * 66 * 1.45 + (len(lines) - 1) * 34
    ys = stack(STORY, [("space", block)], 220, STORY[1] / 2 - 60, 90)
    for k in range(len(lines) + 1):
        img = paper(STORY, th)
        d = ImageDraw.Draw(img, "RGBA")
        motif(img, th, STORY[0] / 2, ys[0] + 110, 220)
        y = ys[1]
        for j, wl in enumerate(wrapped):
            if j < k:
                centre(d, wl, f, y, spacing=1.45)
            y += len(wl) * 66 * 1.45 + 34
        handle_mark(d, STORY, handle, 1560)
        path = os.path.join(tmp, f"f{k}.png")
        img.convert("RGB").save(path)
        frames.append(path)
    cover = save(Image.open(frames[-1]).convert("RGBA"), out + "-cover.jpg")

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
        "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-profile:v", "high", "-crf", "18",
        "-c:a", "aac", "-b:a", "128k", "-t", f"{total:.1f}", "-movflags", "+faststart", mp4,
    ], check=True)
    return [mp4, cover]


# ----------------------------------------------------------------- stories

def story(p, th, handle, out):
    img = paper(STORY, th)
    d = ImageDraw.Draw(img, "RGBA")
    kind = p["story"]
    mid = STORY[1] / 2 - 60

    if kind in ("morning", "night", "fragment"):
        f, lines = fit(d, p["text"], 820, 700, 72, 44, italic=(kind == "fragment"))
        ys = stack(STORY, [("text", (f, lines, 1.42))], 200, mid, 80)
        motif(img, th, STORY[0] / 2, ys[0] + 100, 200)
        centre(d, lines, f, ys[1])
    elif kind == "quote":
        f, lines = fit(d, p["quote"], 820, 640, 62, 40)
        ys = stack(STORY, [("text", (f, lines, 1.42)), ("space", 30)], 160, mid, 70)
        motif(img, th, STORY[0] / 2, ys[0] + 80, 160)
        centre(d, lines, f, ys[1])
        spaced(d, p["author"], sans(24, "demi"), ys[2], INK, 4)
    elif kind == "choice":
        title = serif(56, italic=True)
        bf = serif(56)
        ys = stack(STORY, [("space", 60), ("space", 190), ("space", 190), ("space", 40)], 160, mid, 50)
        motif(img, th, STORY[0] / 2, ys[0] + 80, 160)
        centre(d, ["This or that?"], title, ys[1])
        for k, (label, y) in enumerate(((p["a"], ys[2]), (p["b"], ys[3])), 1):
            d.rounded_rectangle([170, y, 910, y + 190], radius=95, outline=rgb(th["b"]) + (255,), width=3)
            lines = wrap(d, f"{k}   {label}", bf, 640)
            ly = y + (190 - len(lines) * 56 * 1.2) / 2 - 6
            centre(d, lines, bf, ly, spacing=1.2)
        spaced(d, "reply 1 or 2", sans(24, "demi"), ys[4], MUTED, 5)
    elif kind in ("prompt", "pointer"):
        f, lines = fit(d, p["text"], 820, 640, 70, 44)
        ys = stack(STORY, [("text", (f, lines, 1.42)), ("space", 30)], 160, mid, 70)
        motif(img, th, STORY[0] / 2, ys[0] + 80, 160)
        centre(d, lines, f, ys[1])
        spaced(d, p["note"], sans(24, "demi"), ys[2], rgb(th["b"]), 3)

    handle_mark(d, STORY, handle, 1540)
    return [save(img, out + ".jpg")]


RENDER = {"quote": quote_card, "thought": thought_card, "carousel": carousel, "reel": reel, "story": story}


def theme_for(p):
    return THEMES[dt.datetime.fromisoformat(p["at"]).weekday()]


def main():
    ap = argparse.ArgumentParser(description="Render a schedule to images and reels.")
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
        files = RENDER[p["kind"]](p, theme_for(p), sched["handle"], os.path.join(outdir, p["id"]))
        manifest[p["id"]] = [os.path.relpath(f, HERE) for f in files]
        print(f"{p['id']:24s} {len(files)} file(s)")

    json.dump(manifest, open(manifest_path, "w"), indent=1)
    print(f"manifest: {os.path.relpath(manifest_path, HERE)}  ({len(manifest)} posts)")


if __name__ == "__main__":
    main()
