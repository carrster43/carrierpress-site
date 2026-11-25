"""The house promo feed at /promos/v1.json, read by the three free apps.

WHY A FEED. The slot in Spellbright, Who Serves and Conception Zodiac used to
hold a Google ad unit. The publisher account is closed, so the slot requested an
ad, got nothing, and rendered empty while the script still loaded. Author
decision 2026-11-25: no third party ads until that account is resolved, and the
only ads are for our own books and products. "Books first" (author, same day).

The three apps live in three repos. If each one held its own promo copy, the copy
would drift, which is exactly what happened to the funding claim: /progress/ went
on saying Spellbright was "paid for by a short ad" for a day after that line left
its own source, because make_progress.py was in no workflow. One generated feed
means promo copy changes in catalog.json and nowhere else.

WHAT A PROMO IS. A cover, one line, one link, one audience tag. The app renders an
<a> with an <img> in it. No script, no iframe, no third party request, no pixel.
That is what lets the privacy copy say a free app sends the visitor's browser to
nobody, once the app repos drop Google's script.

THE COPY IS THE CATALOGUE'S, NEVER NEW, the same rule books.py enforces on book
pages. A promo line is the first sentence of the shelf's own blurb, verbatim.
Nothing here is written, paraphrased or shortened by hand. A shelf whose blurb
opens with a sentence too long for a slot FAILS THIS BUILD rather than being
silently cut, so the fix happens in the catalogue where the words live.

AGE. Spellbright is for children aged 4 to 12. The catalogue says The Gadget
Sandbox Chronicles is for ages 10 to 14 and The Glitch Blocks for 8 to 12, so
neither belongs in front of a five year old. Those bounds ride on the promo and
Spellbright shows only promos whose band contains the child's age. A shelf with
no stated age has no bound.

THE HARD RULE. Only a section the catalogue marks kids:true is ever tagged kids.
The Classics Line is ghost stories and weird fiction, The American Firsts is
historical crime, Money and Income is for adults. An audience tag is asserted
against the catalogue below, not trusted to a list kept by hand.
"""
import io, json, os, re, sys

import books

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(io.open(os.path.join(HERE, "catalog.json"), encoding="utf-8"))

BASE = "https://carrierpress.com"
OUT = os.path.join(HERE, "promos", "v1.json")
LINE_MAX = 185          # a slot on a phone; over this, shorten the blurb in catalog.json
BOOK_WEIGHT = 10        # books first (author 2026-11-25)
ACCESS_WEIGHT = 2

# The shelves that may be promoted, and the category page each one sits on.
# audience: kids (Spellbright), parents (Conception Zodiac), adult (Who Serves,
# Conception Zodiac). A kids tag is checked against section["kids"] below.
SHELVES = [
    ("gadget-sandbox",  "young-readers", ["kids", "parents"]),
    ("glitch-blocks",   "young-readers", ["kids", "parents"]),
    ("young-money",     "young-readers", ["kids", "parents"]),
    ("keystone-cycle",  "fiction",       ["adult"]),
    ("american-firsts", "fiction",       ["adult"]),
    ("classics",        "classics",      ["adult"]),
]

SECTION = {s["id"]: s for s in D["sections"]}
RANK = {it["a"]: it["rank"] for it in (D.get("top10") or {}).get("items", [])}
URL = books.url_for(D)


def first_sentence(blurb, sid):
    """The shelf's own opening sentence, verbatim. No hand shortening."""
    m = re.match(r"(.+?[.!?])(\s|$)", blurb.strip(), re.S)
    line = " ".join((m.group(1) if m else blurb).split())
    if len(line) > LINE_MAX:
        sys.exit("make_promos.py: %s opens with %d characters, over %d. Shorten the "
                 "blurb in catalog.json; this file never cuts the author's copy.\n  %r"
                 % (sid, len(line), LINE_MAX, line))
    return line


def lead(sec):
    """The cover people recognise: the shelf's best selling title, else book one."""
    ranked = sorted((b for b in sec["books"] if b["a"] in RANK), key=lambda b: RANK[b["a"]])
    return ranked[0] if ranked else sec["books"][0]


def ages(sec):
    """(min, max) from the catalogue's own `ages`, e.g. "10 to 14", else (None, None)."""
    a = sec.get("ages")
    m = re.match(r"\s*(\d+)\s*(?:to|-|–)\s*(\d+)\s*$", a or "")
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def build():
    out = []
    for sid, cat, audience in SHELVES:
        sec = SECTION.get(sid)
        if not sec:
            sys.exit("make_promos.py: catalog.json has no section %r" % sid)
        if "kids" in audience and not sec.get("kids"):
            sys.exit("make_promos.py: %r is tagged kids but the catalogue does not "
                     "mark it kids:true. A child must never be shown an adult shelf." % sid)
        if "kids" not in audience and sec.get("kids"):
            sys.exit("make_promos.py: %r is a kids shelf but carries no kids tag" % sid)
        b = lead(sec)
        p = dict(id=sid, kind="shelf", audience=audience, weight=BOOK_WEIGHT,
                 name=sec["name"], line=first_sentence(sec["blurb"], sid),
                 img="/assets/covers/%s.jpg" % b["a"],
                 href="/%s/#h-%s" % (cat, sid))
        lo, hi = ages(sec)
        if lo:
            p["age_min"], p["age_max"] = lo, hi
        if not os.path.exists(os.path.join(HERE, "assets", "covers", b["a"] + ".jpg")):
            sys.exit("make_promos.py: no cover for %s (%s)" % (b["t"], b["a"]))
        out.append(p)

    # The one product promo. Adults only: a child is never asked to buy anything.
    # The line is the words /progress/ already uses for Access, composed from
    # commerce.ACCESS_PRICE so the price cannot drift away from the rest of the site.
    import commerce
    out.append(dict(id="access", kind="product", audience=["adult"], weight=ACCESS_WEIGHT,
                    name="Carrier Press Access",
                    line="Every web app, the ebooks, or both, " + commerce.ACCESS_PRICE + ".",
                    img="/assets/logo-mark.png", href="/apps/#access"))

    # Every destination is checked against the built page, because /access/ looked
    # like the obvious url for the Access promo and is a 404.
    for p in out:
        path, _, frag = p["href"].partition("#")
        page = os.path.join(HERE, path.strip("/"), "index.html")
        if not os.path.exists(page):
            sys.exit("make_promos.py: %s points at %s, which is not a built page"
                     % (p["id"], p["href"]))
        if frag and ('id="%s"' % frag) not in io.open(page, encoding="utf-8").read():
            sys.exit("make_promos.py: %s points at #%s, which is not on %s"
                     % (p["id"], frag, path))

    feed = dict(v=1, built=__import__("datetime").date.today().isoformat(),
                base=BASE, mix="books-first", spellbright_kids_only=True, promos=out)

    text = json.dumps(feed, indent=1, ensure_ascii=False, sort_keys=False) + "\n"
    bad = re.findall(r".{0,40}[–—].{0,40}", text)
    if bad:
        sys.exit("make_promos.py: house dash rule, em or en dash in the feed:\n  %s" % bad[0])
    os.path.exists(os.path.dirname(OUT)) or os.makedirs(os.path.dirname(OUT))
    old = io.open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if re.sub(r'"built": "[^"]*"', "", old) == re.sub(r'"built": "[^"]*"', "", text):
        print("promos: no change (%d promos)" % len(out))
        return
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print("promos: wrote %s (%d promos)" % (OUT, len(out)))


if __name__ == "__main__":
    build()
