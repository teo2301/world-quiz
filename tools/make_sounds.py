#!/usr/bin/env python3
"""Synthesise the app's three sound effects (no recordings, nothing downloaded).

    python3 tools/make_sounds.py      -> docs/sounds/{right,wrong,finish}.mp3

right   ~0.7 s  bright two-note chime (bell partials, a fifth apart going up)
wrong   ~0.5 s  soft low "bonk" sliding down, no harshness
finish  ~1.3 s  short rising arpeggio (C-E-G-C) with a bell tail

Needs numpy and ffmpeg (libmp3lame). Deterministic, so reruns give the same files.
"""
import os
import subprocess
import tempfile
import wave

import numpy as np

SR = 22050
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "sounds")


def t_of(secs):
    return np.arange(int(SR * secs)) / SR


def norm(x, peak=0.8):
    m = np.max(np.abs(x)) or 1.0
    return x / m * peak


def bell(f, secs, decay=4.0, attack=0.004):
    """A bell-ish note: fundamental + a few inharmonic partials, fast attack, exponential decay."""
    t = t_of(secs)
    x = (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 3)
         + 0.25 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)
         + 0.12 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 10))
    e = np.exp(-t * decay) * np.minimum(1, t / attack)
    return x * e


def place(total, parts):
    x = np.zeros(int(SR * total))
    for start, sig in parts:
        i = int(SR * start)
        n = min(len(sig), len(x) - i)
        x[i:i + n] += sig[:n]
    return x


def right():
    return norm(place(0.75, [(0, bell(784, 0.5, 6)), (0.09, bell(1175, 0.66, 5))]), .7)


def wrong():
    t = t_of(0.5)
    f = 220 * np.exp(-t * 1.6)                      # 220 Hz sliding down
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)
    e = np.minimum(1, t / 0.01) * np.exp(-t * 7)
    return norm(x * e, .6)


def finish():
    notes = [523.25, 659.25, 783.99, 1046.5]
    parts = [(i * 0.12, bell(f, 0.9 if i == 3 else 0.45, 3 if i == 3 else 6)) for i, f in enumerate(notes)]
    return norm(place(1.35, parts), .7)


def write(name, x):
    os.makedirs(OUT, exist_ok=True)
    fade = min(len(x), int(SR * 0.02))
    x = x.copy()
    x[-fade:] *= np.linspace(1, 0, fade)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        path = tmp.name
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm)
    dst = os.path.join(OUT, name + ".mp3")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ac", "1", "-codec:a", "libmp3lame",
                    "-b:a", "48k", "-map_metadata", "-1", dst], check=True)
    os.remove(path)
    print(dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    write("right", right())
    write("wrong", wrong())
    write("finish", finish())
