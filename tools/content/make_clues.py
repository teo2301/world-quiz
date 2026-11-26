#!/usr/bin/env python3
"""Write docs/clues.json, the Mystery country data (Phase 1 placeholder; Phase 3 builds it properly).

Each item: id, n (the answer), al (other accepted names), clues (exactly 5, hardest first,
the last one close to a giveaway). `decoys` are other real country names: a guess that is
exactly one of them never counts as a typo of an answer ("Austria" is not "Australia").
    python3 tools/content/make_clues.py && python3 validate.py
"""
import json
import os

ITEMS = [
    ("Japan", ["Nippon", "Nihon"], [
        "Its national parliament is called the Diet.",
        "It is made up of four main islands and thousands of smaller ones.",
        "Its high-speed bullet trains are called Shinkansen.",
        "Its highest mountain, a volcano, last erupted in 1707.",
        "Its capital is Tokyo."]),
    ("Brazil", [], [
        "Its official language is Portuguese.",
        "It borders every South American country except Chile and Ecuador.",
        "Its capital was moved inland to a brand-new city in 1960.",
        "Most of the Amazon rainforest is inside its borders.",
        "Rio de Janeiro is one of its best-known cities."]),
    ("Egypt", [], [
        "The Suez Canal runs through it.",
        "More than nine in ten of its people live close to one river.",
        "Its ancient writing was deciphered with the help of the Rosetta Stone.",
        "Its biggest city is Cairo.",
        "It is home to the Great Pyramid of Giza."]),
    ("Canada", [], [
        "It has the longest coastline of any country.",
        "It has two official languages, English and French.",
        "Its capital, Ottawa, was chosen by Queen Victoria.",
        "It is the second-largest country in the world by area.",
        "A red maple leaf is on its flag."]),
    ("Italy", [], [
        "Two independent countries, San Marino and Vatican City, lie inside it.",
        "Its two biggest islands are Sicily and Sardinia.",
        "Mount Etna and Mount Vesuvius are both here.",
        "Its flag is a green, white and red tricolour.",
        "Its capital is Rome, home of the Colosseum."]),
    ("Australia", [], [
        "Its capital was built as a compromise between its two biggest cities.",
        "The Great Barrier Reef lies off its north-east coast.",
        "Wild koalas live here and nowhere else.",
        "It is the only country that covers a whole continent.",
        "Sydney Opera House is its most famous building."]),
    ("India", ["Bharat"], [
        "Its flag has a navy-blue wheel with 24 spokes.",
        "According to the UN it passed China as the most populous country in 2023.",
        "The Ganges flows through it.",
        "The Taj Mahal is in its city of Agra.",
        "Its capital is New Delhi."]),
    ("Mexico", [], [
        "Its flag shows an eagle eating a snake on a cactus.",
        "Chichén Itzá, a great Maya city, is here.",
        "It has more Spanish speakers than any other country.",
        "It shares a long land border with the United States to its north.",
        "Its capital and largest city share the country's name."]),
    ("Iceland", [], [
        "It sits on the Mid-Atlantic Ridge, where two tectonic plates pull apart.",
        "Its parliament, the Althing, was founded in 930.",
        "It has no army of its own.",
        "Its capital is the northernmost capital of any sovereign state.",
        "Its capital is Reykjavík."]),
    ("Peru", [], [
        "Lake Titicaca is on its border with Bolivia.",
        "The Nazca Lines were scratched into its desert.",
        "Its capital, Lima, is on the Pacific coast.",
        "The Inca Empire was centred here, with its capital at Cusco.",
        "Machu Picchu is here."]),
    ("Kenya", [], [
        "The equator runs through it.",
        "Lake Victoria is on its western edge.",
        "Huge wildebeest herds cross its Maasai Mara every year.",
        "Its capital is Nairobi.",
        "Its distance runners have won many Olympic medals; its flag has a Maasai shield."]),
    ("Norway", [], [
        "Its coastline is cut by deep fjords carved by glaciers.",
        "The Svalbard islands in the Arctic belong to it.",
        "It voted twice against joining the European Union.",
        "Its flag is a blue-and-white Nordic cross on red.",
        "Its capital is Oslo."]),
]

DECOYS = """Afghanistan Albania Algeria Andorra Angola Argentina Armenia Austria Azerbaijan Bahamas Bahrain Bangladesh
Barbados Belarus Belgium Belize Benin Bhutan Bolivia Botswana Bulgaria Burundi Cambodia Cameroon Chad Chile China
Colombia Comoros Croatia Cuba Cyprus Denmark Djibouti Dominica Ecuador Eritrea Estonia Eswatini Ethiopia Fiji
Finland France Gabon Gambia Georgia Germany Ghana Greece Grenada Guatemala Guinea Guyana Haiti Honduras Hungary
Indonesia Iran Iraq Ireland Israel Jamaica Jordan Kazakhstan Kiribati Kuwait Kyrgyzstan Laos Latvia Lebanon
Lesotho Liberia Libya Liechtenstein Lithuania Luxembourg Madagascar Malawi Malaysia Maldives Mali Malta Mauritania
Mauritius Moldova Monaco Mongolia Montenegro Morocco Mozambique Myanmar Namibia Nauru Nepal Netherlands Nicaragua
Niger Nigeria Oman Pakistan Palau Panama Paraguay Philippines Poland Portugal Qatar Romania Russia Rwanda Samoa
Senegal Serbia Seychelles Singapore Slovakia Slovenia Somalia Spain Sudan Suriname Sweden Switzerland Syria
Tajikistan Tanzania Thailand Togo Tonga Tunisia Turkey Turkmenistan Tuvalu Uganda Ukraine Uruguay Uzbekistan
Vanuatu Venezuela Vietnam Yemen Zambia Zimbabwe""".split() + [
    "New Zealand", "South Africa", "South Korea", "North Korea", "United States", "United Kingdom", "Sri Lanka",
    "Saudi Arabia", "United Arab Emirates", "Costa Rica", "El Salvador", "Czech Republic", "North Macedonia",
    "Bosnia and Herzegovina", "Papua New Guinea", "Sierra Leone", "Burkina Faso", "Ivory Coast", "Cape Verde",
    "Equatorial Guinea", "Guinea-Bissau", "South Sudan", "Central African Republic", "Democratic Republic of the Congo",
    "Republic of the Congo", "San Marino", "Vatican City", "Timor-Leste", "Brunei", "Dominican Republic",
    "Trinidad and Tobago", "Saint Lucia", "Antigua and Barbuda", "Marshall Islands", "Solomon Islands",
    "Sao Tome and Principe", "Saint Kitts and Nevis", "Saint Vincent and the Grenadines", "Micronesia"]

if __name__ == "__main__":
    items = [{"id": "m%03d" % (i + 1), "n": n, "al": al, "clues": c} for i, (n, al, c) in enumerate(ITEMS)]
    answers = {n for n, _, _ in ITEMS}
    doc = {"about": "Mystery country (Phase 1 placeholder). Five clues each, hardest first; 5 points from the "
                    "first clue down to 1. Decoys are other real countries, so they never count as typos.",
           "items": items, "decoys": [d for d in DECOYS if d not in answers]}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "clues.json")
    with open(out, "w", encoding="utf-8") as f:
        f.write(json.dumps(doc, indent=0, ensure_ascii=False) + "\n")
    print(len(items), "items,", len(doc["decoys"]), "decoys ->", out)
