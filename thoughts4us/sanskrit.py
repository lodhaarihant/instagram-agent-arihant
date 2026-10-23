"""
Sanskrit and transliteration for every verse used in week 2, read from sanskrit.json
(fetched from srimadgita.com/verse/chapter-C-verse-V, the same source as the quotes page).

  get("2.47")        {"deva": [line, ...], "tr": [line, ...]}
  part("2.47", 3)    the half of the verse that "part 3 of 4" belongs to
  ref_in(text)       first "C.V" reference found in a string, or None
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = json.load(open(os.path.join(HERE, "sanskrit.json"), encoding="utf8"))


def _lines(text, speaker):
    text = re.sub(r"[।॥|]+\s*\d+\.\d+\s*[।॥|]*", "", text)
    out = []
    for l in text.split("\n"):
        l = re.sub(r"^\s*(\S+\s+){0,2}?\S*%s\S*\s*" % speaker, "", l.strip())
        if l.strip() and not re.fullmatch(r"[।॥|\s]*", l):
            out.append(l.strip())
    if len(out) == 1 and "।" in out[0].rstrip("।"):
        a, b = out[0].rstrip("।").split("।", 1)
        out = [a.strip() + "।", b.strip()]
    return out


def get(ref):
    d = _DATA[ref]
    deva = _lines(d["sa"], "वाच")
    deva[:-1] = [l.rstrip("।") + " ।" for l in deva[:-1]]
    deva[-1] = deva[-1].rstrip("।").strip() + " ॥"
    tr = _lines(d["tr"], "uvāch")
    return {"ref": ref, "deva": deva, "tr": tr}


def part(ref, n, of=4):
    """Lines of the verse for slide n of `of`, when a verse is split across slides."""
    v = get(ref)
    k = len(v["deva"])
    i = min(k - 1, (n - 1) * k // of)
    kt = len(v["tr"])
    j = min(kt - 1, (n - 1) * kt // of)
    return {"ref": ref, "deva": [v["deva"][i]], "tr": [v["tr"][j]]}


def ref_in(text):
    m = re.search(r"(?<![\d.])(\d{1,2})\.(\d{1,2})(?![\d.])", text or "")
    return f"{m[1]}.{m[2]}" if m else None
