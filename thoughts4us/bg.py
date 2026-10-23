#!/usr/bin/env python3
"""
Backgrounds for week 2: the artwork in backgrounds/, nothing generated.

Each image has a text zone (where the words sit, as a fraction of height, for story
and feed crops), a mode (light art gets dark ink, dark art gets cream ink) and a
focus point for cropping to 9:16 and 4:5. DAYS says which images a day uses; posts
rotate through them.

To swap an image, replace the file in backgrounds/ and keep its name, or edit IMAGES.
"""
import os

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(HERE, "backgrounds")

# hide = (top, bottom) fractions of a band with text baked into the picture; it gets blurred under a full-width panel.
# zone = (story, feed): vertical centre of the text block. focus = crop centre (x, y).
IMAGES = {
    "a1": {"file": "a1_kurukshetra.jpg",  "hide": (0.455, 0.57), "mode": "dark",  "zone": (0.52, 0.515), "focus": (0.5, 0.5)},
    "a2": {"file": "a2_wheel.jpg",        "hide": (0.47, 0.60), "mode": "dark",  "zone": (0.53, 0.53), "focus": (0.62, 0.5)},
    "a3": {"file": "a3_clouds.jpg",       "mode": "dark",  "zone": (0.80, 0.78), "focus": (0.5, 0.5)},
    "a4": {"file": "a4_cosmic.jpg",       "mode": "dark",  "zone": (0.72, 0.70), "focus": (0.5, 0.5)},
    "a5": {"file": "a5_kalki.jpg",        "mode": "dark",  "zone": (0.22, 0.20), "focus": (0.5, 0.5)},
    "a6": {"file": "a6_collage.jpg",      "mode": "dark",  "zone": (0.78, 0.76), "focus": (0.5, 0.5)},
    "b1": {"file": "b1_cows.jpg",         "mode": "light", "soft": 0.55, "zone": (0.42, 0.40), "focus": (0.5, 0.5)},
    "b2": {"file": "b2_watercolour.jpg",  "mode": "light", "soft": 0.55, "zone": (0.42, 0.40), "focus": (0.5, 0.5)},
    "b3": {"file": "b3_lotus.jpg",        "mode": "dark",  "zone": (0.78, 0.74), "focus": (0.45, 0.5)},
    "b4": {"file": "b4_boat.jpg",         "mode": "dark",  "zone": (0.80, 0.78), "focus": (0.5, 0.5)},
    "b5": {"file": "b5_krishnaboat.jpg",  "mode": "dark",  "zone": (0.84, 0.82), "focus": (0.5, 0.5)},
    "b6": {"file": "b6_shesha.jpg",       "mode": "dark",  "zone": (0.17, 0.17), "focus": (0.5, 0.5)},
    "b7": {"file": "b7_illustration.jpg", "mode": "dark",  "zone": (0.86, 0.84), "focus": (0.5, 0.5)},
}

# Day number (1 = first day of the week) -> its images.
DAYS = {
    1: ["a1", "a5"],          # Karma: Kurukshetra, the standing figure
    2: ["b7", "b1", "b2"],    # Mind and rest: flute on the moon, cows at dawn, watercolour
    3: ["a2", "a6"],          # Steadiness: the wheel, the collage
    4: ["a4", "b6"],          # The soul: the cosmos, Vishnu on Shesha
    5: ["b4", "b5"],          # Devotion: the boat on teal water
    6: ["b3", "a6"],          # Knowledge: lotus pond
    7: ["a3", "a5"],          # Peace: golden clouds
}

_CACHE = {}


def info(key):
    return IMAGES[key]


def image(key, size):
    """The artwork cover-cropped to size (cached)."""
    k = (key, size)
    if k not in _CACHE:
        im = Image.open(os.path.join(FOLDER, IMAGES[key]["file"])).convert("RGB")
        _CACHE[k] = ImageOps.fit(im, size, Image.LANCZOS, centering=IMAGES[key]["focus"])
    return _CACHE[k].copy()


def for_day(day, n):
    """Key of the n-th image choice for a day (rotates through its images)."""
    keys = DAYS[day]
    return keys[n % len(keys)]
