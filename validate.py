#!/usr/bin/env python3
"""Check the game data.  python3 validate.py   (run from the repo root)

questions.json: unique ids, 3 distinct wrong answers, answer not among them, valid topic/difficulty.
                (topic codes in field `l`: cap flg geo pop lmk gk); flag images exist.
countries.json: unique codes/names, a flag file per country, generated cap/flg questions match it.
stats.json:     higher-or-lower items: unique ids, known category, positive number, a source note.
clues.json:     mystery-country items: unique ids, exactly 5 clues, the answer not given away in a clue
                before the last, names/aliases unambiguous (also against the decoys).
"""
import json, sys, collections, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "server"))
import modes  # noqa: E402

bad = []

# ---------------------------------------------------------------- questions
Q = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "docs/questions.json"))
ids = collections.Counter(q["id"] for q in Q)
bad += [f"duplicate id {i}" for i, n in ids.items() if n > 1]
texts = collections.Counter((q["q"], q.get("img")) for q in Q)     # flag questions share a text, not an image
bad += [f"duplicate question: {t}" for t, n in texts.items() if n > 1]
for q in Q:
    if not re.match(r"^(cap|flg|geo|pop|lmk|gk)(\d{3}|[a-z]{2})$", q["id"]): bad.append(f"{q['id']}: bad id")
    if q["a"] in q["w"]: bad.append(f"{q['id']}: answer is among the wrong options")
    if q.get("img"):
        if q["l"] != "flg" or not re.match(r"^flags/[a-z]{2}\.svg$", q["img"]): bad.append(f"{q['id']}: bad img {q['img']}")
        elif not os.path.isfile(os.path.join("docs", q["img"])): bad.append(f"{q['id']}: missing flag file {q['img']}")
    if any(len(o) > 44 for o in [q["a"], *q["w"]]): bad.append(f"{q['id']}: option too long for the buttons")
    opts = [q["a"], *q["w"]]
    if len(q["w"]) != 3: bad.append(f"{q['id']}: needs 3 wrong answers")
    if len({o.casefold() for o in opts}) != 4: bad.append(f"{q['id']}: repeated option")
    if q["l"] not in {"cap", "flg", "geo", "pop", "lmk", "gk"}: bad.append(f"{q['id']}: bad topic")
    if not q["id"].startswith(q["l"]): bad.append(f"{q['id']}: id doesn't start with its topic")
    if q["d"] not in (1, 2, 3): bad.append(f"{q['id']}: bad difficulty")
    if not q.get("x"): bad.append(f"{q['id']}: no explanation")

# ---------------------------------------------------------------- countries.json + flags
K = json.load(open("docs/data/countries.json", encoding="utf-8"))
kc = collections.Counter(c["iso2"] for c in K)
bad += [f"countries: duplicate code {i}" for i, n in kc.items() if n > 1]
names = collections.Counter(n.casefold() for c in K for n in [c["name"], *c["aliases"]])
bad += [f"countries: name/alias '{n}' used twice" for n, k in names.items() if k > 1]
conts = {"Africa", "Asia", "Europe", "North America", "South America", "Oceania"}
for c in K:
    if c["continent"] not in conts: bad.append(f"countries {c['iso2']}: bad continent")
    if not os.path.isfile(f"docs/flags/{c['iso2']}.svg"): bad.append(f"countries {c['iso2']}: no flag file")
    if c["pop_m"] is not None and not (c["pop_m"] > 0 and c["pop_year"]): bad.append(f"countries {c['iso2']}: bad population")
    if c["area_km2"] is not None and not c["area_km2"] > 0: bad.append(f"countries {c['iso2']}: bad area")
    if not 1 <= len(c["facts"]) <= 2: bad.append(f"countries {c['iso2']}: needs 1-2 facts")
    if c["tier"] not in (1, 2, 3): bad.append(f"countries {c['iso2']}: bad tier")
if not os.path.isfile("docs/flags/LICENSE"): bad.append("flags: LICENSE missing")
byiso = {c["iso2"]: c for c in K}
for q in Q:
    if re.match(r"^(cap|flg)[a-z]{2}$", q["id"]):
        c = byiso.get(q["id"][3:])
        if not c: bad.append(f"{q['id']}: no such country"); continue
        if q["l"] == "flg" and (q["a"] != c["name"] or q.get("img") != f"flags/{c['iso2']}.svg"): bad.append(f"{q['id']}: answer/flag mismatch")
        if q["l"] == "cap" and q["a"] != c["capital"]: bad.append(f"{q['id']}: capital mismatch")
        if q["l"] == "flg" and set(q["w"]) - {k["name"] for k in K}: bad.append(f"{q['id']}: wrong option isn't a country")

# ---------------------------------------------------------------- stats (higher or lower)
S = json.load(open("docs/stats.json", encoding="utf-8"))
cats = S["cats"]
sids = collections.Counter(i["id"] for i in S["items"])
bad += [f"stats: duplicate id {i}" for i, n in sids.items() if n > 1]
same = collections.Counter((i["c"], i["n"], i["d"]) for i in S["items"])
bad += [f"stats: duplicate item {k}" for k, n in same.items() if n > 1]
for i in S["items"]:
    if i["c"] not in cats: bad.append(f"stats {i['id']}: unknown category {i['c']}")
    if isinstance(i["v"], bool) or not isinstance(i["v"], (int, float)) or i["v"] <= 0: bad.append(f"stats {i['id']}: bad value")
    for k in ("n", "d", "note"):
        if not str(i.get(k) or "").strip(): bad.append(f"stats {i['id']}: missing {k}")
per_cat = collections.Counter(i["c"] for i in S["items"])
for c in cats:
    vals = [i["v"] for i in S["items"] if i["c"] == c]
    # the game only pairs numbers at least 10% apart; each category needs plenty of those
    pairs = sum(1 for a in vals for b in vals if a < b and (b - a) / b >= 0.1)
    if per_cat[c] < 8 or pairs < 20: bad.append(f"stats: category {c} too small ({per_cat[c]} items, {pairs} pairs)")

# ---------------------------------------------------------------- mystery country (clues.json)
CD = json.load(open("docs/clues.json", encoding="utf-8"))
C = CD["items"]
cids = collections.Counter(p["id"] for p in C)
bad += [f"clues: duplicate id {i}" for i, n in cids.items() if n > 1]
owner = collections.defaultdict(set)
for p in C:
    for k in [modes.key(p["n"])] + [modes.key(a) for a in p.get("al", [])]:
        owner[k].add(p["n"])
    if len(p["clues"]) != 5: bad.append(f"clues {p['id']}: needs exactly 5 clues")
    if len(set(p["clues"])) != len(p["clues"]): bad.append(f"clues {p['id']}: repeated clue")
    names = [p["n"]] + p.get("al", [])
    for c in p["clues"][:-1]:
        for nm in names:
            if modes.key(nm) and modes.key(nm) in modes.key(c): bad.append(f"clues {p['id']}: '{nm}' given away in '{c}'")
bad += [f"clues: '{k}' is a name or alias of {sorted(v)}" for k, v in owner.items() if len(v) > 1]
for d in CD.get("decoys", []):
    if modes.key(d) in owner: bad.append(f"clues: decoy '{d}' is also an answer")
forms = modes.build_forms(C)
taken = modes.taken_keys(C, CD.get("decoys", []))
for p in C:
    if not modes.is_match(p["n"], forms[p["id"]], taken): bad.append(f"clues {p['id']}: own name doesn't match")

print("\n".join(bad) or "OK")
print(len(K), "countries,", sum(1 for q in Q if q.get("img")), "flag questions")
print(len(Q), "questions:", dict(collections.Counter(q["l"] for q in Q)), "difficulty", dict(sorted(collections.Counter(q["d"] for q in Q).items())))
print(len(S["items"]), "higher-or-lower items:", dict(per_cat))
print(len(C), "mystery countries,", len(CD.get("decoys", [])), "decoys")
sys.exit(1 if bad else 0)
