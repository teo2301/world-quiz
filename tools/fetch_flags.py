#!/usr/bin/env python3
"""Self-hosted flags from the MIT-licensed flag-icons project, pinned to one release.

    python3 tools/fetch_flags.py           # download any missing flags for docs/data/countries.json
    python3 tools/fetch_flags.py --check   # re-download every flag and compare (no writes)

Files go to docs/flags/<iso2>.svg (4:3 versions) with the project's LICENSE next to them.
The app shows them with <img>, so any script inside an SVG would never run; this also refuses
files that contain <script or external references, just in case."""
import json, os, sys, urllib.request
VERSION = "7.6.0"
BASE = "https://cdn.jsdelivr.net/npm/flag-icons@%s/" % VERSION
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "docs", "flags")


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return r.read()


def main():
    check = "--check" in sys.argv
    codes = [c["iso2"] for c in json.load(open(os.path.join(ROOT, "docs", "data", "countries.json"), encoding="utf-8"))]
    os.makedirs(OUT, exist_ok=True)
    bad = []
    for name, path in [("LICENSE", "LICENSE")] + [("%s.svg" % c, "flags/4x3/%s.svg" % c) for c in codes]:
        dest = os.path.join(OUT, name)
        if not check and os.path.exists(dest):
            continue
        data = get(path)
        low = data.lower()
        if name.endswith(".svg") and (b"<script" in low or b"href=\"http" in low or b"<foreignobject" in low):
            bad.append(name + ": unsafe content"); continue
        if check:
            if not os.path.exists(dest) or open(dest, "rb").read() != data: bad.append(name + ": differs from " + VERSION)
        else:
            with open(dest, "wb") as f: f.write(data)
    extra = sorted(set(os.listdir(OUT)) - {"LICENSE"} - {"%s.svg" % c for c in codes})
    bad += ["%s: not a country in countries.json" % e for e in extra]
    print("\n".join(bad) or "OK: %d flags match flag-icons %s" % (len(codes), VERSION))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
