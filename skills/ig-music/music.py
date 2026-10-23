#!/usr/bin/env python3
"""
music.py - put background music on reels and images that have none.

For every video it checks for a real audio track (not just a silent one). If
the video already has sound it is left alone. Silent videos, and images, get a
random track from the music folder. The part of the track used is chosen to
fit the clip's length: it skips the intro and outro and takes the steadiest,
fullest stretch, so a 7-second clip doesn't open on a quiet fade-in. Volume is
evened out across tracks, with a short fade at both ends.

Images become MP4s (default 7 seconds, width 1080, aspect ratio kept), ready
to post as a reel.

Usage
  python3 music.py media/week1                    # every video/image in a folder
  python3 music.py clip.mp4 photo.jpg             # specific files
  python3 music.py media/week1 --check            # report only, change nothing
  python3 music.py photo.jpg --duration 10        # longer image video
  python3 music.py clip.mp4 --force               # replace audio that exists
  python3 music.py media/week1 --inplace          # overwrite videos, not -music.mp4
  python3 music.py clip.mp4 --music path/to/music --seed 7

Music folder: --music, else $IG_MUSIC_DIR, else the first music/ or
thoughts4us/music/ found walking up from the current folder. Any .mp3, .m4a,
.wav or .ogg inside it (subfolders too) is a candidate.

Needs ffmpeg: imageio-ffmpeg if installed (pip install imageio-ffmpeg), else
ffmpeg on PATH.
"""

import argparse
import glob
import json
import os
import random
import re
import shutil
import subprocess
import sys

VIDEO = (".mp4", ".mov", ".m4v", ".webm")
IMAGE = (".jpg", ".jpeg", ".png", ".webp")
AUDIO = (".mp3", ".m4a", ".wav", ".ogg")
SILENT_DB = -70.0     # max volume below this counts as no sound
SKIP_EDGE = 6.0       # seconds of intro/outro to avoid when the track allows
RATE = 4000           # analysis sample rate, plenty for loudness


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ff = shutil.which("ffmpeg")
        if not ff:
            sys.exit("ffmpeg not found: pip install imageio-ffmpeg, or install ffmpeg")
        return ff


FF = None


def run(args, **kw):
    return subprocess.run([FF, "-hide_banner"] + args, capture_output=True, **kw)


def probe(path):
    """(duration seconds, has audio stream, max volume dB or None)."""
    err = run(["-i", path, "-af", "volumedetect", "-f", "null", "-"], text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0
    has = bool(re.search(r"Stream #.*Audio:", err))
    mv = re.search(r"max_volume: (-?[\d.]+|-inf) dB", err)
    vol = None if not mv else (-999.0 if mv.group(1) == "-inf" else float(mv.group(1)))
    return dur, has, vol


def find_music(arg):
    if arg:
        return arg
    if os.environ.get("IG_MUSIC_DIR"):
        return os.environ["IG_MUSIC_DIR"]
    d = os.path.abspath(os.getcwd())
    while True:
        for cand in ("music", os.path.join("thoughts4us", "music")):
            if os.path.isdir(os.path.join(d, cand)):
                return os.path.join(d, cand)
        up = os.path.dirname(d)
        if up == d:
            sys.exit("no music folder found: pass --music or set IG_MUSIC_DIR")
        d = up


def tracks_in(folder):
    out = [p for p in glob.glob(os.path.join(folder, "**", "*"), recursive=True)
           if p.lower().endswith(AUDIO)]
    if not out:
        sys.exit(f"no audio files in {folder}")
    return sorted(out)


_env = {}
_len = {}


def track_len(track):
    if track not in _len:
        err = run(["-i", track], text=True).stderr
        m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
        _len[track] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0
    return _len[track]


def envelope(track):
    """Loudness per 0.5 s window, as a list of linear RMS values. Cached per track."""
    if track not in _env:
        # ffmpeg measures each 0.5 s block itself; parsing its output is far
        # faster than squaring samples in Python.
        af = (f"aresample={RATE},asetnsamples={RATE // 2},"
              "astats=metadata=1:reset=1,"
              "ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-")
        out = run(["-loglevel", "error", "-i", track, "-ac", "1", "-af", af, "-f", "null", "-"],
                  text=True).stdout
        vals = re.findall(r"RMS_level=(-?[\d.]+|-inf)", out)
        _env[track] = [0.0 if v == "-inf" else 10 ** (float(v) / 20) for v in vals]
    return _env[track]


def best_start(track, dur, rng):
    """Pick where in the track to start so the clip gets a full, steady section."""
    env = envelope(track)
    total = len(env) / 2.0
    win = max(1, int(round(dur * 2)))
    if total <= dur + 1:
        return 0.0, total
    edge = SKIP_EDGE if total > dur + 2 * SKIP_EDGE else max(0.0, (total - dur) / 2 - 0.5)
    lo, hi = int(edge * 2), len(env) - win - int(edge * 2)
    if hi <= lo:
        return 0.0, total
    peak = max(env) or 1.0
    scored = []
    for s in range(lo, hi + 1):
        seg = env[s:s + win]
        mean = sum(seg) / win
        spread = (sum((v - mean) ** 2 for v in seg) / win) ** 0.5
        # Loud enough to carry the clip, and not lurching between quiet and loud.
        scored.append((mean / peak - 0.6 * spread / peak, s))
    scored.sort(reverse=True)
    # Pick among the best few, spaced apart, so repeat runs don't all sound the same.
    picks = []
    for _, s in scored:
        if all(abs(s - p) >= win for p in picks):
            picks.append(s)
        if len(picks) == 3:
            break
    return rng.choice(picks) / 2.0, total


def output_for(path, inplace):
    stem, ext = os.path.splitext(path)
    if inplace and ext.lower() in VIDEO:
        return path
    return stem + "-music.mp4"


def add_music(src, track, start, dur, is_image, dst):
    fade_out = min(1.5, dur / 5)
    af = (f"loudnorm=I=-16:TP=-1.5:LRA=11,"
          f"afade=t=in:d=0.6,afade=t=out:st={max(0.0, dur - fade_out):.2f}:d={fade_out:.2f},"
          f"aresample=44100")
    tmp = dst + ".tmp.mp4"
    if is_image:
        inputs = ["-loop", "1", "-framerate", "30", "-t", f"{dur:.2f}", "-i", src]
        vcodec = ["-vf", "scale=1080:-2:out_range=tv,format=yuv420p", "-c:v", "libx264",
                  "-profile:v", "high", "-crf", "18", "-r", "30"]
    else:
        inputs = ["-i", src]
        vcodec = ["-c:v", "copy"]
    cmd = ["-y", "-loglevel", "error"] + inputs + [
        "-ss", f"{start:.2f}", "-i", track,
        "-map", "0:v:0", "-map", "1:a:0"] + vcodec + [
        "-af", af, "-ac", "2", "-c:a", "aac", "-b:a", "128k",
        "-t", f"{dur:.2f}", "-movflags", "+faststart", tmp]
    r = run(cmd, text=True)
    if r.returncode:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise RuntimeError(r.stderr.strip() or "ffmpeg failed")
    os.replace(tmp, dst)


def collect(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "**", "*"), recursive=True)):
                low = f.lower()
                if low.endswith(VIDEO + IMAGE) and "-music." not in low and not low.endswith("-cover.jpg"):
                    out.append(f)
        elif os.path.isfile(p):
            out.append(p)
        else:
            print(f"  ! not found: {p}", file=sys.stderr)
    return out


def main():
    global FF
    ap = argparse.ArgumentParser(description="Add background music to silent videos and images.")
    ap.add_argument("paths", nargs="+", help="files or folders")
    ap.add_argument("--music", help="music folder")
    ap.add_argument("--duration", type=float, default=7.0, help="seconds for image videos (default 7)")
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    ap.add_argument("--force", action="store_true", help="replace audio even when the video has sound")
    ap.add_argument("--inplace", action="store_true", help="overwrite videos instead of writing -music.mp4")
    ap.add_argument("--images", action="store_true", help="when given folders, include images (off by default)")
    ap.add_argument("--seed", type=int, help="fix the random picks")
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    a = ap.parse_args()

    FF = ffmpeg()
    rng = random.Random(a.seed)
    music = find_music(a.music)
    tracks = tracks_in(music)

    files = collect(a.paths)
    explicit = {os.path.abspath(p) for p in a.paths if os.path.isfile(p)}
    results = []
    for f in files:
        low = f.lower()
        is_image = low.endswith(IMAGE)
        if is_image and not (a.images or os.path.abspath(f) in explicit):
            continue
        row = {"file": f}
        if is_image:
            dur, row["status"] = a.duration, "image"
        else:
            dur, has, vol = probe(f)
            if has and vol is not None and vol > SILENT_DB and not a.force:
                row.update(status="has sound", max_db=vol)
                results.append(row)
                continue
            row["status"] = "silent" if has else "no audio track"
        row["duration"] = round(dur, 2)

        long_enough = [t for t in tracks if track_len(t) >= dur]
        track = rng.choice(long_enough or tracks)
        start, total = best_start(track, dur, rng)
        row.update(track=os.path.relpath(track, music), start=round(start, 1), track_len=round(total, 1))

        if not a.check:
            dst = output_for(f, a.inplace)
            try:
                add_music(f, track, start, dur, is_image, dst)
                row["out"] = dst
            except RuntimeError as e:
                row["error"] = str(e)
        results.append(row)

    if a.json:
        print(json.dumps(results, indent=1))
        return
    print(f"music: {music}  ({len(tracks)} tracks)\n")
    for r in results:
        name = os.path.basename(r["file"])
        if r["status"] == "has sound":
            print(f"  keep   {name:36s} already has sound ({r['max_db']} dB peak)")
            continue
        what = f"{r['track']} @ {r['start']}s for {r['duration']}s"
        if "error" in r:
            print(f"  FAIL   {name:36s} {r['error']}")
        elif a.check:
            print(f"  would  {name:36s} {r['status']:15s} -> {what}")
        else:
            print(f"  added  {name:36s} {r['status']:15s} -> {what}")
            if r["out"] != r["file"]:
                print(f"         -> {r['out']}")
    done = sum(1 for r in results if r.get("out") or (a.check and "track" in r))
    kept = sum(1 for r in results if r["status"] == "has sound")
    print(f"\n{done} {'would get' if a.check else 'given'} music, {kept} already had sound" + ("  (check only)" if a.check else ""))


if __name__ == "__main__":
    main()
