---
name: ig-music
description: >-
  Check reels and images for missing sound and add background music from the
  music folder - a random track, with the stretch of it that best fits the
  clip's length, levelled and faded. Use when the user says "add music", "this
  reel is silent", "put audio on this", "does this video have sound", "turn
  this image into a reel with music", or before posting media that might go
  out silent.
---

# ig-music

One tool lives in this folder and it runs:

```bash
python3 music.py media/week1 --check          # what has sound, what would get music
python3 music.py media/week1                  # add music to every silent video
python3 music.py media/week1 --images         # ...and turn images into music videos
python3 music.py photo.jpg --duration 10      # one image, 10-second video
python3 music.py clip.mp4 --force             # replace sound that's already there
python3 music.py media/week1 --inplace        # overwrite videos, no -music.mp4 copies
```

Always run `--check` first and show the user the table before writing
anything. It changes nothing and says, file by file, which ones have sound,
which don't, and which track and start point each would get.

## What it decides

**Has sound or not.** A video counts as silent if it has no audio track, or if
its loudest moment is below -70 dB (a silent track added only so the upload is
accepted). Videos with real sound are kept as they are unless `--force` is
passed. Never `--force` a video that has a voiceover without asking the user:
it replaces the voice, it doesn't mix under it.

**Which track.** A random pick from every .mp3, .m4a, .wav or .ogg under the
music folder, preferring tracks at least as long as the clip. `--seed N`
makes the picks repeatable.

**Which part of the track.** The script measures the track's loudness every
half second, skips the first and last 6 seconds (intros and fade-outs), and
scores every window the length of the clip on two things: loud enough to carry
it, and steady rather than lurching between quiet and loud. It takes one of
the best three, spaced apart, so two clips on the same track don't start in
the same place. A 7-second clip gets a 7-second stretch, a 30-second reel gets
a 30-second stretch.

**How it sounds.** Every track is normalised to -16 LUFS so a quiet track and
a loud one sound the same in the feed, fades in over 0.6 s, and fades out over
the last 1.5 s (less on very short clips).

## Images

Folders: images are skipped unless `--images` is passed, because feed photos
and carousel slides usually go up as photos. Images named directly on the
command line are always converted. Each becomes an H.264 MP4 at width 1080,
same aspect ratio, 30 fps, `--duration` seconds long (default 7). Cover
images (`*-cover.jpg`) and files that already end in `-music` are always
skipped.

A 1080x1350 image becomes a 4:5 video. That posts fine as a feed video, but a
reel shows it letterboxed. For a full-screen reel, start from a 1080x1920
image.

## Where the music comes from

`--music <folder>`, else `$IG_MUSIC_DIR`, else the first `music/` or
`thoughts4us/music/` found walking up from the current folder. To add tracks,
drop files into that folder (subfolders are fine, e.g. `music/flute/`).

Royalty-free music (Pixabay and similar) can be baked into the video. It
posts as "original audio", not as a song from Instagram's library, so it
won't show up as a trend. Don't use commercial songs: Instagram mutes or
removes them.

## Needs

ffmpeg: `imageio-ffmpeg` if it's installed (`pip install imageio-ffmpeg`),
otherwise `ffmpeg` on PATH. Nothing else.
