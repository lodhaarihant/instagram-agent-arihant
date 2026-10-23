#!/usr/bin/env python3
"""Median pitch and range of a voice clip, to check it sits in the Voice B band (about 107 Hz, 86 to 130 Hz).
usage: pitch.py clip.wav [more.wav ...]"""
import sys
import parselmouth


def stats(path):
    snd = parselmouth.Sound(path)
    pit = snd.to_pitch(time_step=0.01, pitch_floor=60, pitch_ceiling=300)
    f = pit.selected_array["frequency"]
    f = f[f > 0]
    f.sort()
    n = len(f)
    return {"median": float(f[n // 2]), "p10": float(f[n // 10]), "p90": float(f[9 * n // 10])}


if __name__ == "__main__":
    for p in sys.argv[1:]:
        s = stats(p)
        print(f"{p}: median {s['median']:.0f} Hz, 10-90% {s['p10']:.0f}-{s['p90']:.0f} Hz")
