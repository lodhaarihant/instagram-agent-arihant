#!/usr/bin/env python3
"""
Render week 2 (schedule/week2.json) onto the artwork in backgrounds/.

  feed      1080x1350 JPEG (4:5)
  stories   1080x1920 JPEG, or an MP4 with flute and a spoken verse (05:00 and 00:00)
  reels     1080x1920 MP4: the artwork drifting slowly, one line at a time, flute under it;
            the 07:00 and 19:00 reels also carry the verse read aloud

Text sits on a soft frosted panel over the art, in the zone set for that image in bg.py.

Voice: macOS `say` (Rishi, Indian English; see VOICE, VOICE_RATE, VOICE_PITCH), a little lower, with room. It is a
synthetic voice, not a recording. To use a real or better voice, drop an audio file named
after the post id into voice/ (for example voice/d1-0700-reel_am7.mp3). Lines are then
timed to its length instead.

Usage:
  ../.venv/bin/python render_krishna.py schedule/week2.json
  ../.venv/bin/python render_krishna.py schedule/week2.json --only d1-0700-reel_am7
  ../.venv/bin/python render_krishna.py schedule/week2.json --jobs 4
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import tempfile
from multiprocessing import Pool

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import bg
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.join(HERE, "music")
VOICE_DIR = os.path.join(HERE, "voice")
FEED, STORY = R.FEED, R.STORY

_MODE = "dark"
PAL = {
    "dark": {"ink": (252, 246, 232), "accent": (240, 200, 120), "muted": (226, 216, 200), "tint": (0, 0, 0), "amt": 0.62},
    "light": {"ink": (36, 24, 18), "accent": (150, 70, 24), "muted": (84, 70, 62), "tint": (252, 246, 236), "amt": 0.70},
}
SAFE = {STORY: (250, 1600), FEED: (110, 1240)}


DEVA_FONT = "Kohinoor Devanagari Medium"
DEVA_TOOL = os.path.join(HERE, "tools", "deva")
DEVA_CACHE = os.path.join(HERE, ".cache", "deva")
PALATINO_IT = "/System/Library/Fonts/Palatino.ttc"          # index 1 is italic; has every diacritic we need


def translit_font(size):
    return ImageFont.truetype(PALATINO_IT, size, index=1)


def deva_img(text, size, color):
    """One line of Devanagari as an RGBA image, shaped by macOS CoreText (Pillow can't shape it here)."""
    if not os.path.exists(DEVA_TOOL):
        subprocess.run(["swiftc", "-O", os.path.join(HERE, "tools", "deva.swift"), "-o", DEVA_TOOL], check=True)
    key = hashlib.sha1(f"{text}|{size}|{color}".encode()).hexdigest()[:16]
    path = os.path.join(DEVA_CACHE, key + ".png")
    if not os.path.exists(path):
        os.makedirs(DEVA_CACHE, exist_ok=True)
        subprocess.run([DEVA_TOOL, DEVA_FONT, str(size), *map(str, color), path, text], check=True)
    return Image.open(path).convert("RGBA")


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


# ------------------------------------------------------------------ layout

def _probe():
    return ImageDraw.Draw(Image.new("RGB", (10, 10)))


def _build(e, probe):
    """One element -> dict(kind, lines, font, h)."""
    k = e[0]
    if k == "kicker":
        return {"k": k, "text": e[1], "font": R.sans(24, "demi"), "h": 40}
    if k == "credit":
        return {"k": k, "text": e[1], "font": R.sans(24, "demi"), "h": 40}
    if k == "src":
        return {"k": k, "text": e[1], "font": R.serif(26, italic=True), "h": 44}
    if k == "rule":
        return {"k": k, "h": 4}
    if k == "gap":
        return {"k": k, "h": e[1]}
    if k == "pill":
        return {"k": k, "text": e[1], "num": e[2], "font": R.serif(50), "h": 140}
    if k == "note":
        f = R.sans(28, "regular")
        lines = R.wrap(probe, e[1], f, 760)
        return {"k": k, "lines": lines, "font": f, "lh": 28 * 1.5, "h": len(lines) * 28 * 1.5}
    if k in ("quote", "serif"):
        italic = (k == "quote")
        if len(e) > 3 and e[3]:                       # fixed size
            f = R.serif(e[3], italic)
            lines = R.wrap(probe, e[1], f, e[2])
        else:
            f, lines = R.fit(probe, e[1], e[2], e[4] if len(e) > 4 else 560, e[5] if len(e) > 5 else 60, 36, italic, 1.4)
        return {"k": k, "lines": lines, "font": f, "lh": f.size * 1.4, "h": len(lines) * f.size * 1.4, "italic": italic}
    if k == "deva":
        lines, maxw, size = e[1], e[2], e[3]
        while True:
            imgs = [deva_img(l, size, PAL[_MODE]["accent"]) for l in lines]
            if max(i.width for i in imgs) <= maxw + 20 or size <= 30:
                break
            size -= 2
        return {"k": k, "imgs": imgs, "h": sum(i.height for i in imgs) - 8 * len(imgs)}
    if k == "translit":
        lines, maxw, size = e[1], e[2], (e[3] if len(e) > 3 else 29)
        f = translit_font(size)
        wrapped = []
        for l in lines:
            wrapped += R.wrap(probe, l, f, maxw)
        return {"k": k, "lines": wrapped, "font": f, "lh": size * 1.5, "h": len(wrapped) * size * 1.5}
    if k == "list":
        f = R.serif(46)
        return {"k": k, "lines": e[1], "font": f, "lh": 46 * 1.6, "h": len(e[1]) * 46 * 1.6}
    raise ValueError(k)


def plan(elems, size, zone, gap=30):
    """Stack elements around the zone's vertical centre. Returns (items, bbox)."""
    W, H = size
    probe = _probe()
    items = [_build(e, probe) for e in elems]
    total = sum(i["h"] for i in items) + gap * (len(items) - 1)
    lo, hi = SAFE[size]
    top = min(max(zone * H - total / 2, lo), max(lo, hi - total))
    y = top
    for it in items:
        it["y"] = y
        y += it["h"] + gap
    widest = 0
    for it in items:
        if "lines" in it:
            widest = max(widest, max(probe.textlength(l, font=it["font"]) for l in it["lines"]))
        elif it["k"] == "pill":
            widest = max(widest, 740)
        elif it["k"] == "deva":
            widest = max(widest, max(i.width for i in it["imgs"]))
        elif "text" in it:
            widest = max(widest, probe.textlength(it["text"].upper(), font=it["font"]) + 6 * len(it["text"]))
    half = min(W / 2 - 40, max(widest, 420) / 2 + 80)
    return items, (W / 2 - half, top - 70, W / 2 + half, top + total + 70)


def draw_item(d, it, size, pal, fill_override=None):
    W = size[0]
    ink, acc, mu = pal["ink"], pal["accent"], pal["muted"]
    k = it["k"]
    y = it["y"]
    if k == "deva":
        im = d._image
        for pic in it["imgs"]:
            x = int((W - pic.width) / 2)
            if im.mode == "RGBA":
                im.alpha_composite(pic, (x, int(y)))
            else:
                im.paste(pic.convert("RGB"), (x, int(y)), pic)
            y += pic.height - 8
        return
    if k in ("quote", "serif", "note", "list", "translit"):
        col = {"note": mu}.get(k, ink)
        for ln in it["lines"]:
            x = (W - d.textlength(ln, font=it["font"])) / 2
            d.text((x, y), ln, font=it["font"], fill=col + (255,))
            y += it["lh"]
    elif k in ("kicker", "credit"):
        text = it["text"].upper()
        f = it["font"]
        ws = [d.textlength(c, font=f) for c in text]
        tr = 5
        x = (W - sum(ws) - tr * (len(text) - 1)) / 2
        col = acc if k == "kicker" else ink
        for c, w in zip(text, ws):
            d.text((x, y), c, font=f, fill=col + (255,))
            x += w + tr
    elif k == "src":
        x = (W - d.textlength(it["text"], font=it["font"])) / 2
        d.text((x, y), it["text"], font=it["font"], fill=mu + (255,))
    elif k == "rule":
        d.line([(W / 2 - 40, y + 2), (W / 2 + 40, y + 2)], fill=acc + (255,), width=3)
    elif k == "pill":
        d.rounded_rectangle([170, y, W - 170, y + 130], radius=65, outline=acc + (255,), width=3)
        t = f"{it['num']}   {it['text']}"
        x = (W - d.textlength(t, font=it["font"])) / 2
        d.text((x, y + 28), t, font=it["font"], fill=ink + (255,))


def frost(img, bbox, mode, strength=1.0, hide=False):
    """A soft tinted panel behind the text. With hide=True the art under it is blurred first,
    to cover text that is baked into the picture."""
    if strength <= 0:
        return img
    pal = PAL[mode]
    W, H = img.size
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])], radius=70, fill=int(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(60))
    base = img.filter(ImageFilter.GaussianBlur(30)) if hide else img
    tinted = Image.blend(base, Image.new("RGB", img.size, pal["tint"]), pal["amt"] * (1.0 if hide else 0.85))
    return Image.composite(tinted, img, mask)


def handle_mark(img, handle, mode, y):
    pal = PAL[mode]
    d = ImageDraw.Draw(img, "RGBA")
    f = R.serif(32, italic=True)
    x = (img.size[0] - d.textlength(handle, font=f)) / 2
    d.text((x, y), handle, font=f, fill=pal["muted"] + (255,))


def base_image(key, size, elems, zone_idx, handle, gap=30, strength=1.0, soften=0.0):
    """Artwork + panel + handle. Returns (img, items, mode)."""
    global _MODE
    inf = bg.info(key)
    mode = inf["mode"]
    _MODE = mode
    img = bg.image(key, size)
    soften = max(soften, inf.get("soft", 0.0))
    if soften:
        blur = 12 if soften > 0.5 and not inf.get("soft") else 5
        img = Image.blend(img.filter(ImageFilter.GaussianBlur(blur)), Image.new("RGB", size, PAL[mode]["tint"]), soften)
    items, box = plan(elems, size, inf["zone"][zone_idx], gap)
    hide = inf.get("hide")
    if hide and not soften:
        box = (-90, min(box[1], hide[0] * size[1] - 50), size[0] + 90, max(box[3], hide[1] * size[1] + 50))
    img = frost(img, box, mode, 0.0 if soften else strength, bool(hide))
    handle_mark(img, handle, mode, size[1] - (320 if size == STORY else 105))
    return img, items, mode


def draw_all(img, items, mode, size):
    d = ImageDraw.Draw(img, "RGBA")
    for it in items:
        draw_item(d, it, size, PAL[mode])


def save(img, path):
    img.convert("RGB").save(path, "JPEG", quality=94, subsampling=0, optimize=True)
    return path


# ------------------------------------------------------------------- feed

def quote_card(p, handle, out):
    q = p["quote"]
    v = p.get("verse")
    elems = [("kicker", "bhagavad gita")]
    if v:
        elems += [("deva", v["deva"], 940, 60), ("translit", v["tr"], 940, 34), ("rule",)]
    elems += [("quote", q, 840, 0, 440 if v else 560, 58 if v else 64), ("rule",), ("credit", p["author"]), ("src", p["source"])]
    img, items, mode = base_image(p["bg"], FEED, elems, 1, handle)
    draw_all(img, items, mode, FEED)
    return [save(img, out + ".jpg")]


def carousel(p, handle, out):
    deck = p["deck"]
    pages = [("cover", deck["cover"], deck["sub"]), ("stake", deck["stake"], "")]
    pages += [("slide",) + tuple(s) for s in deck["slides"]]
    pages += [("recap", deck["recap"], ""), ("cta", deck["cta"], "")]
    n = len(pages)
    files = []
    for i, pg in enumerate(pages, 1):
        kind = pg[0]
        soften = 0.0 if kind == "cover" else 0.55
        if kind == "cover":
            elems = [("kicker", "swipe"), ("quote", pg[1], 820, 0, 420, 80), ("rule",), ("src", pg[2])]
        elif kind == "stake":
            elems = [("quote", pg[1], 800, 0, 560, 54)]
        elif kind == "slide":
            _, main, credit, note = pg
            v = (deck.get("verses") or [None] * len(deck["slides"]))[i - 3]
            if v:
                elems = [("deva", v["deva"], 940, 58), ("translit", v["tr"], 940, 32), ("rule",),
                         ("quote", main, 840, 0, 330, 54)]
            else:
                elems = [("quote", main, 800, 0, 480, 56)]
            if credit:
                elems.append(("credit", credit))
            elems += [("rule",), ("note", note)]
        elif kind == "recap":
            elems = [("kicker", "in short"), ("list", [f"{k}.  {t}" for k, t in enumerate(pg[1], 1)])]
        else:
            elems = [("serif", pg[1], 800, 0, 420, 60), ("rule",), ("kicker", "follow " + handle)]
        key = p["bg"]
        img, items, mode = base_image(key, FEED, elems, 1, handle, soften=soften)
        draw_all(img, items, mode, FEED)
        d = ImageDraw.Draw(img, "RGBA")
        f = R.sans(24, "medium")
        t = f"{i} / {n}"
        d.text((FEED[0] - 80 - d.textlength(t, font=f), 70), t, font=f, fill=PAL[mode]["muted"] + (255,))
        files.append(save(img, f"{out}-{i:02d}.jpg"))
    return files


# ---------------------------------------------------------------- stories

def story(p, handle, out):
    kind = p["story"]
    if kind == "text":
        elems = [("serif", p["text"], 800, 0, 620, 70)]
    elif kind == "quote":
        v = p.get("verse")
        elems = []
        if v:
            elems += [("deva", v["deva"], 940, 66), ("translit", v["tr"], 940, 34), ("rule",)]
        elems += [("quote", p["quote"], 840, 0, 520 if v else 640, 60 if v else 66), ("rule",), ("credit", p["author"])]
    elif kind == "choice":
        elems = [("quote", "This or that?", 800, 0, 120, 60), ("gap", 20), ("pill", p["a"], 1), ("pill", p["b"], 2), ("kicker", "reply 1 or 2")]
    else:                                              # prompt, pointer
        elems = [("serif", p["text"], 800, 0, 620, 66), ("rule",), ("kicker", p["note"])]
    img, items, mode = base_image(p["bg"], STORY, elems, 0, handle)
    draw_all(img, items, mode, STORY)
    return [save(img, out + ".jpg")]


# ------------------------------------------------------------------ audio

def tracks():
    out = []
    for f in sorted(glob.glob(os.path.join(MUSIC, "**", "*.mp3"), recursive=True)):
        if "native-american" in f.lower():
            continue                                    # wrong sound for Krishna: keep the bansuri-style flutes
        out.append(f)
    return out


MUSIC_BED = 0.30          # flute level under the voice
MUSIC_TEMPO = 0.80        # flute speed: 1.0 is the original recording, lower is slower


def track_for(post_id, need):
    need = need * MUSIC_TEMPO
    ts = tracks()
    if not ts:
        return None
    h = int(hashlib.sha1(post_id.encode()).hexdigest(), 16)
    path = ts[h % len(ts)]
    dur = duration(path)
    room = max(0, dur - need - 4)
    return path, min((h // len(ts)) % 40, room)


def duration(path):
    r = subprocess.run([ffmpeg(), "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0


VOICE = "Rishi"           # Indian-English male. Others: "Daniel" (British), "Eddy (English (US))", "Reed (English (US))"
VOICE_RATE = 105          # `say` rate. Rishi will not go much slower than this, so VOICE_SPEED slows it further
VOICE_SPEED = 0.85        # extra slowing with the pitch kept: 0.85x, as in the Voice B spec
VOICE_GAIN = 4.4          # voice level: 1.9 was the original reel level; 3.6 measures +5 dB louder
VOICE_PITCH = 0.93        # Rishi's natural median is 115 Hz; 0.93 puts it near the 107 Hz target (check with tools/pitch.py)
PAUSE = 1.0               # seconds between lines
LONG_PAUSE = 2.5          # before the last line, and after the Sanskrit before the English


def speak(text, wav, tmp):
    aiff = os.path.join(tmp, "s.aiff")
    subprocess.run(["say", "-v", VOICE, "-r", str(VOICE_RATE), "-o", aiff, text], check=True)
    sr = int(44100 * VOICE_PITCH)
    af = (f"aresample=44100,asetrate={sr},aresample=44100,atempo={round(44100 / sr * VOICE_SPEED, 4)},"
          "highpass=f=80,"                                      # rumble out
          "equalizer=f=170:t=q:w=1.0:g=2.5,"                    # warmth and body, 100 to 250 Hz
          "equalizer=f=400:t=q:w=1.0:g=-2,"                     # boxiness, 300 to 500 Hz
          "equalizer=f=3200:t=q:w=0.8:g=3,"                     # presence and clarity, 2 to 5 kHz
          "deesser=i=0.4:m=0.5:f=0.5,"                          # keep s and sh soft
          "treble=g=1:f=10000,"                                 # a touch of air
          "acompressor=threshold=-20dB:ratio=3,aecho=0.85:0.4:45:0.10,"
          f"volume={VOICE_GAIN},alimiter=limit=0.92")
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", aiff, "-af", af, wav], check=True)
    return duration(wav)


# ------------------------------------------------------------------ video

def video(p, handle, out, is_reel):
    lines = p["lines"]
    key = p["bg"]
    tmp = tempfile.mkdtemp()
    size = STORY
    n = len(lines)
    # Sanskrit, transliteration, then the English line by line
    v = p.get("verse")
    probe = _probe()
    sz = 60 if v else 68
    ref_label = f"gita {v['ref']}" if v else ("in plain words" if p.get("credit") == "in plain words" else "")
    label = " · ".join(x for x in (p.get("theme", ""), ref_label) if x)
    while True:
        while sz > 44 and any(len(R.wrap(probe, l, R.serif(sz, True), 840)) > 2 for l in lines):
            sz -= 2
        head = [("kick", ("kicker", label))] if label else []
        if v:
            head += [("deva", ("deva", v["deva"], 940, 64)), ("tr", ("translit", v["tr"], 940, 34)), ("rule", ("rule",))]
        elems = [e for _, e in head] + [("quote", l, 840, sz) for l in lines]
        if p.get("credit"):
            elems += [("rule",), ("credit", p["credit"])]
        its, _box = plan(elems, size, bg.info(key)["zone"][0], 24)
        if sz <= 44 or its[-1]["y"] + its[-1]["h"] - its[0]["y"] <= 1340:
            break
        sz -= 2
    off = len(head)
    img, items, mode = base_image(key, size, elems, 0, handle, gap=24)
    base_path = os.path.join(tmp, "base.png")
    img.save(base_path)
    t_eng = (5.0 if p.get("voice") else 4.4) if v else None

    # voice clips and timing
    clips, starts = [], []
    ext = [f for f in glob.glob(os.path.join(VOICE_DIR, p["id"] + ".*")) if f.lower().endswith((".mp3", ".wav", ".m4a"))]
    if p.get("voice") and ext:
        total_v = duration(ext[0])
        words = [max(1, len(l.split())) for l in lines]
        t = t_eng or 1.0
        for w in words:
            starts.append(t)
            t += total_v * w / sum(words)
        clips = [(ext[0], starts[0])]
        end = t
    elif p.get("voice"):
        t = t_eng or 1.2
        for k, l in enumerate(lines):
            wav = os.path.join(tmp, f"v{k}.wav")
            dur = speak(l, wav, tmp)
            clips.append((wav, t))
            starts.append(t)
            t += dur + (LONG_PAUSE if k == n - 2 and n > 2 else PAUSE)      # a long breath before the last line
        end = t
    else:
        t = t_eng or 0.9
        for k in range(n):
            starts.append(t)
            t += 2.0
        end = t
    credit_t = end + 0.2
    total = credit_t + (3.2 if p.get("credit") else 2.4)

    # overlays: one transparent PNG per element, fading in at its time
    overlay_files, fades = [], []
    for k, it in enumerate(items):
        if it["k"] == "gap":
            continue
        layer = Image.new("RGBA", size, (0, 0, 0, 0))
        draw_item(ImageDraw.Draw(layer), it, size, PAL[mode])
        path = os.path.join(tmp, f"o{k}.png")
        layer.save(path)
        overlay_files.append(path)
        if k < off:
            name = head[k][0]
            fades.append({"kick": 0.0, "deva": 0.6, "tr": 2.4, "rule": 2.4}[name])
        elif off <= k < off + n:
            fades.append(starts[k - off])
        else:
            fades.append(credit_t)

    # cover frame
    full = img.copy()
    draw_all(full, items, mode, size)
    cover = save(full, out + "-cover.jpg") if is_reel else None

    cmd = [ffmpeg(), "-y", "-loglevel", "error", "-framerate", "30", "-loop", "1", "-t", f"{total:.2f}", "-i", base_path]
    dust = None
    if mode == "dark":
        dust = dust_layer(tmp, p["id"])
        cmd += ["-framerate", "30", "-loop", "1", "-t", f"{total:.2f}", "-i", dust]
    d0 = 2 if dust else 1                                   # input index of the first text overlay
    for f in overlay_files:
        cmd += ["-framerate", "30", "-loop", "1", "-t", f"{total:.2f}", "-i", f]
    nv = d0 + len(overlay_files)
    music = track_for(p["id"], total)
    mi = nv
    if music:
        cmd += ["-ss", f"{music[1]}", "-i", music[0]]
    ci = nv + (1 if music else 0)
    for c, _ in clips:
        cmd += ["-i", c]

    fc = ["[0:v]scale=1166:2074,crop=1080:1920:x='43+43*sin(t*0.2)':y='77-min(t,25)*2.5',setsar=1[v0]"]
    last = "v0"
    if dust:
        fc.append("[1:v]format=rgba[dust]")
        fc.append("[v0][dust]overlay=x='18*sin(t*0.6)':y='-min(t,30)*30':format=auto[vd]")
        last = "vd"
    for i, ft in enumerate(fades, d0):
        dur = 0.9 if ft > 0 else 0.01
        fc.append(f"[{i}:v]format=rgba,fade=t=in:st={max(0, ft - 0.05):.2f}:d={dur}:alpha=1[o{i}]")
        fc.append(f"[{last}][o{i}]overlay=0:0:format=auto[v{i}]")
        last = f"v{i}"
    fc.append(f"[{last}]format=yuv420p[vout]")
    voice = bool(clips)
    mv = MUSIC_BED if voice else 0.85
    if music:
        fc.append(f"[{mi}:a]atempo={MUSIC_TEMPO},equalizer=f=3000:t=q:w=0.7:g=-5,volume={mv},afade=t=in:d=1.0,afade=t=out:st={total - 2.4:.2f}:d=2.4,aresample=44100[mus]")
    else:
        fc.append("anullsrc=channel_layout=stereo:sample_rate=44100[mus]")
    if voice:
        tags = []
        for j, (c, st) in enumerate(clips):
            ms = int(st * 1000)
            fc.append(f"[{ci + j}:a]aresample=44100,adelay={ms}|{ms}[c{j}]")
            tags.append(f"[c{j}]")
        if len(tags) > 1:
            fc.append("".join(tags) + f"amix=inputs={len(tags)}:normalize=0:dropout_transition=0[voice]")
        else:
            fc.append(f"{tags[0]}anull[voice]")
        # ducking: measured 19 dB between voice and flute while he speaks (the guide asks for 15 to 20); the flute rises about 12 dB in the pauses
        fc.append(f"[voice]apad=whole_dur={total:.2f},asplit=2[vs][vm]")
        fc.append("[mus][vs]sidechaincompress=threshold=0.05:ratio=3:attack=25:release=700:makeup=1[duck]")
        fc.append("[duck][vm]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[aout]")
    else:
        fc.append("[mus]loudnorm=I=-16:TP=-1.5:LRA=11[aout]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-profile:v", "high", "-crf", "19", "-preset", "medium", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-t", f"{total:.2f}", "-movflags", "+faststart", out + ".mp4"]
    subprocess.run(cmd, check=True)
    return [out + ".mp4", cover] if is_reel else [out + ".mp4"]


def dust_layer(tmp, seed):
    """Slow drifting motes of warm light, tall enough to scroll up through the whole reel."""
    import random
    rng = random.Random(seed)
    W, H = 1080, 3300
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(170):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.choice([2, 2, 3, 3, 4, 6])
        a = int(rng.uniform(40, 150))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 224, 160, a))
    layer = layer.filter(ImageFilter.GaussianBlur(1.6))
    path = os.path.join(tmp, "dust.png")
    layer.save(path)
    return path


def reel(p, handle, out):
    return video(p, handle, out, True)


def story_video(p, handle, out):
    return video(p, handle, out, False)


RENDER = {"quote": quote_card, "carousel": carousel, "reel": reel, "story": story, "story_video": story_video}


def work(args):
    p, handle, outdir = args
    files = RENDER[p["kind"]](p, handle, os.path.join(outdir, p["id"]))
    return p["id"], [os.path.relpath(f, HERE) for f in files]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("schedule")
    ap.add_argument("--only")
    ap.add_argument("--day", type=int, help="render one day (1-7)")
    ap.add_argument("--voiced", action="store_true", help="only the posts that carry the voice")
    ap.add_argument("--match", help="regex on the post id, e.g. 'reel_am7|reel_pm19|morning|night'")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    sched = json.load(open(a.schedule))
    week = os.path.splitext(os.path.basename(a.schedule))[0]
    outdir = os.path.join(HERE, "media", week)
    os.makedirs(outdir, exist_ok=True)
    mp = os.path.join(outdir, "manifest.json")
    manifest = json.load(open(mp)) if os.path.exists(mp) else {}
    jobs = [(p, sched["handle"], outdir) for p in sched["posts"] if (not a.only or p["id"] == a.only) and (not a.day or p["id"].startswith(f"d{a.day}-")) and (not a.voiced or p.get("voice")) and (not a.match or re.search(a.match, p["id"]))]
    with Pool(a.jobs if len(jobs) > 1 else 1) as pool:
        for pid, files in pool.imap_unordered(work, jobs):
            manifest[pid] = files
            print(f"{pid:28s} {len(files)} file(s)", flush=True)
    json.dump(manifest, open(mp, "w"), indent=1)
    print(f"manifest: {os.path.relpath(mp, HERE)} ({len(manifest)} posts)")


if __name__ == "__main__":
    main()
