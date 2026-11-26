#!/usr/bin/env python3
"""Append a batch of new questions to docs/questions.json.

    python3 tools/content/merge_batch.py tools/content/p5_eu.py [--dry]

A batch file defines NEW = [(topic, difficulty, question, answer, [3 wrong], explanation), ...]
with topic one of cap flg geo pop lmk gk. Ids ("cap001", "gk014") continue per topic after the current max; a question text that's already in the bank
is skipped. Output format is json.dumps(indent=0, ensure_ascii=False) + newline, like the file.
Run validate.py and near_dups.py around it."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from near_dups import load_new  # noqa: E402
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
P = os.path.join(ROOT, "docs", "questions.json")

new = load_new(sys.argv[1])
qs = json.load(open(P, encoding="utf-8")) if os.path.exists(P) else []
have = {q["q"] for q in qs}
top = {t: 0 for t in ("cap", "flg", "geo", "pop", "lmk", "gk")}
for q in qs:
    num = q["id"][len(q["l"]):]
    if num.isdigit():           # generated ids (capfr, flgfr) don't take part in the numbering
        top[q["l"]] = max(top[q["l"]], int(num))
added = 0
for n in new:
    if n["q"] in have:
        print("skip (already there):", n["q"])
        continue
    assert n["l"] in top and n["d"] in (1, 2, 3) and len(n["w"]) == 3 and n["x"], n
    top[n["l"]] += 1
    qs.append({"id": "%s%03d" % (n["l"], top[n["l"]]), "l": n["l"], "d": n["d"], "q": n["q"], "a": n["a"],
               "w": list(n["w"]), "x": n["x"]})
    have.add(n["q"])
    added += 1
if "--dry" not in sys.argv:
    with open(P, "w", encoding="utf-8") as f:
        f.write(json.dumps(qs, indent=0, ensure_ascii=False) + "\n")
print("added", added, "->", len(qs))
