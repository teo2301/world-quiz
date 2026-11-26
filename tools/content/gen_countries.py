#!/usr/bin/env python3
"""Build docs/data/countries.json and the generated capital + flag questions.

    python3 tools/content/gen_countries.py [--dry]

Source: tools/content/countries_src.py. Generated questions have stable ids made from the
ISO code: "cap" + code (capfr) and "flg" + code (flgfr). Re-running replaces every generated
question in docs/questions.json and leaves the hand-written ones (cap001, flg001, geo001...) alone.
Wrong options are picked with random.Random(seeded by the code), so output is the same each run.
"""
import json, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import countries_src as S  # noqa: E402
ROOT = os.path.join(HERE, "..", "..")
QP = os.path.join(ROOT, "docs", "questions.json")
CP = os.path.join(ROOT, "docs", "data", "countries.json")
GEN_RE = re.compile(r"^(cap|flg)[a-z]{2}$")
FLAG_Q = "Which country does this flag belong to?"

countries = []
for iso, name, al, cap, cont, pop, area, tier, facts, extra in S.C:
    c = {"iso2": iso, "name": name, "aliases": al, "capital": cap or None, "continent": cont,
         "pop_m": pop, "pop_year": S.POP_YEAR if pop is not None else None, "area_km2": area,
         "tier": tier, "facts": facts}
    if extra.get("capnote"): c["capital_note"] = extra["capnote"]
    countries.append((c, extra))
by = {c["iso2"]: (c, e) for c, e in countries}
look = {}
for g in S.LOOKALIKES:
    for k in g:
        look.setdefault(k, set()).update(x for x in g if x != k)


def pick(rng, pool, n, prefer=None):
    """n distinct items from pool, taking from `prefer` (a subset) first."""
    out = []
    for src in ([p for p in pool if p in (prefer or [])], pool):
        src = [p for p in src if p not in out]
        rng.shuffle(src)
        out += src[:n - len(out)]
        if len(out) >= n: break
    assert len(out) == n, (pool, n)
    return out


LOWER = set("The A An Its Home Has Have Famous Known Made Shares Named Lies Mostly Birthplace Became Called Said Almost One Often Widely Most More Measures Sits Spans Hosted Hosts Divided Abolished Landlocked Completely Founded Scene Made Landlocked, Volcanic Mainland About Won Both Borders Formerly Land".split())


THE = {"cf", "km", "cg", "sc", "mv", "ph", "ae", "nl", "gb", "bs", "do", "us", "mh", "sb", "gm"}


def the(c):
    """'the United Kingdom' inside a sentence; plain name otherwise."""
    return ("the " + c["name"]) if c["iso2"] in THE else c["name"]


def about(c, fact):
    """'Cuba: the largest island in the Caribbean.' (keeps proper nouns capitalised)"""
    w = fact.split(" ", 1)[0]
    return "%s: %s" % (c["name"], fact[0].lower() + fact[1:] if w in LOWER else fact)


gen = []
cap_pool = [c for c, e in countries if c["capital"] and not e.get("nocap")]
for c, e in countries:
    iso = c["iso2"]
    # ---------------------------------------------------------- capital
    if c["capital"] and not e.get("nocap"):
        rng = random.Random("cap" + iso)
        if e.get("capw"):
            wrong = list(e["capw"])
        else:
            same = [o for o in cap_pool if o["continent"] == c["continent"] and o is not c]
            near = [o for o in same if abs(o["tier"] - c["tier"]) <= 1]
            wrong = [o["capital"] for o in pick(rng, same, 3, near)]
        x = e.get("capx") or "%s is the capital of %s. %s" % (c["capital"], the(c), about(c, c["facts"][0]))
        gen.append({"id": "cap" + iso, "l": "cap", "d": S.CAP_D.get(iso, c["tier"]),
                    "q": e.get("capq") or "What is the capital of %s?" % the(c),
                    "a": c["capital"], "w": wrong, "x": x})
    # ---------------------------------------------------------- flag
    d = S.FLAG_D.get(iso, c["tier"])
    rng = random.Random("flg" + iso)
    same = [o for o, _ in countries if o["continent"] == c["continent"] and o is not c and o["iso2"] not in look.get(iso, ())]
    if len(same) < 3:
        same = [o for o, _ in countries if o is not c and o["iso2"] not in look.get(iso, ())]
    decoy = []
    if d == 3 and look.get(iso):
        decoy = [by[sorted(look[iso])[rng.randrange(len(look[iso]))]][0]]
    rest = [o for o in same if o not in decoy and not (look.get(o["iso2"], set()) & {x["iso2"] for x in decoy})]
    wrong = [o["name"] for o in decoy + pick(rng, rest, 3 - len(decoy))]
    x = "That's the flag of %s. %s" % (the(c), about(c, c["facts"][-1]))
    gen.append({"id": "flg" + iso, "l": "flg", "d": d, "q": FLAG_Q, "img": "flags/%s.svg" % iso,
                "a": c["name"], "w": wrong, "x": x})

qs = json.load(open(QP, encoding="utf-8"))
gen_caps = {q["a"] for q in gen if q["l"] == "cap"}
# hand-written capital questions from Phase 1 are now generated (their wording lives in countries_src)
keep = [q for q in qs if not GEN_RE.match(q["id"]) and not (q["l"] == "cap" and q["a"] in gen_caps)]
dropped = len(qs) - len(keep) - sum(1 for q in qs if GEN_RE.match(q["id"]))
out = keep + gen
print("countries", len(countries), "| generated", len(gen), "| dropped old hand-written capitals", dropped, "| bank", len(out))
if "--dry" not in sys.argv:
    os.makedirs(os.path.dirname(CP), exist_ok=True)
    with open(CP, "w", encoding="utf-8") as f:
        f.write(json.dumps([c for c, _ in countries], indent=0, ensure_ascii=False) + "\n")
    with open(QP, "w", encoding="utf-8") as f:
        f.write(json.dumps(out, indent=0, ensure_ascii=False) + "\n")
