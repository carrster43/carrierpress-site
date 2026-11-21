#!/usr/bin/env python3
"""
/audio/ -- the catalog performed by Cast, and what it costs to unlock.

    python3 make_audio.py --refresh    # re-read Cast's compile index, then render
    python3 make_audio.py              # render from the committed audio_data.json

WHY THE DATA IS COMMITTED. Cast lives in ~/Projects/Cast and is not a dependency
of this site. --refresh reads its scripts/index.json and writes audio_data.json
here; every ordinary build reads the committed copy, so the site still builds on
a machine that has never seen Cast.

*** THERE IS NO AUDIO FILE ON THIS PAGE, AND THERE MUST NOT BE. ***

KDP Virtual Voice is the only free route onto Audible, it requires that no
audiobook edition exists, and a wide audio release forfeits it for that title
PERMANENTLY. Cast is built around that: the compiler produces a script.json --
who speaks each line, where the music sits -- and the PLAYER performs it on the
listener's own device. No audiobook edition, no ASIN, no change to the Amazon
product record, so the rail survives on all 48 titles.

So this page is a storefront, not a player. It publishes the measurements and
sends people to the app. A sample .m4a hosted here would be a rendered audio
file of a Carrier Press title on the open web, and that is the side of the door
we do not want to be standing on to find out.

THE SALE IS IN CAST, NOT ON THIS PAGE. Cast runs on the web at /cast/app/,
where every book's opening plays before anyone pays (gate 816191f, 2026-11-20),
and the books are sold through the gate's Gumroad keys. The price shown here is
read from commerce.py, the same source /apps/ and /apps/cast/ use; the
membership's price, trial and renewal sit beside its button on /apps/cast/.

COPY PASS 2026-11-21 (author "Yes"): the page sells the listening. The title
count comes from the data, the tables link every book and its opening, and the
synthesised-voice note is the last line of the page (house rule: the AI note
goes last, never first).
"""
import argparse, html, json, pathlib, sys, re, unicodedata, datetime
from urllib.parse import quote

import books
import commerce
import nav

DOMAIN = "carrierpress.com"
OUT = pathlib.Path("audio")
DATA = pathlib.Path("audio_data.json")
CAST_INDEX = pathlib.Path("/Users/jeffreycarrier/Projects/Cast/scripts/index.json")
SUPPORT = "support@carrierpress.com"

# Cast's model, author 2026-10-04: the shelf books are sold one at a time, the
# opening of each plays first; the subscription is only for the listener's own
# EPUBs. The web price comes from commerce.py (2026-11-21), not a constant here.
CAST_APP = "/cast/app/"

# Filenames that do not normalise onto a catalogue title. Three of forty-eight,
# each for its own reason, so they are named rather than pattern-matched.
ALIAS = {
    "28_Marjorie_Corey_Complete_Series": "The Complete Series",
    "36_Who_Wants_To_Be_Greek": "Who Wants To Be Greek? English Narrative Edition",
    "42_Side_Hustle_Jr": "Side Hustle Junior",
    "59_More_Ghost_Stories": "More Ghost Stories of an Antiquary",
    "84_The_Call_of_Cthulhu": "The Call of Cthulhu and Other Mythos Tales",
}

# In Cast but not yet in catalog.json, because the book is not on sale anywhere
# else yet (Mrs. Kehoe, American Firsts BK03, added to Cast 2026-10-04 while its
# Bowker record is unresolved). stem -> (title, series). Remove a row once the
# book is in catalog.json.
UNLISTED = {
    "51_Mrs_Kehoe": ("Mrs. Kehoe", "The American Firsts"),
}


def e(x):
    return html.escape(str(x), quote=True)


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"^\d+[_\s-]+", "", s).replace("_", " ").lower()
    s = re.sub(r"\b(the|a|an)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def refresh():
    """Join Cast's compile index onto the site catalogue and write audio_data.json."""
    if not CAST_INDEX.exists():
        sys.exit("no Cast index at %s -- run `python3 catalog.py` in ~/Projects/Cast"
                 % CAST_INDEX)
    cast = json.loads(CAST_INDEX.read_text())
    site = json.loads(pathlib.Path("catalog.json").read_text())

    by_title, order = {}, []
    for sec in site["sections"]:
        for b in sec.get("books", []):
            by_title[norm(b["t"])] = (b, sec.get("name"))
        order.append(sec.get("name"))

    titles, unmatched = [], []
    for r in cast["titles"]:
        stem = r["file"].rsplit(".", 1)[0]
        key = norm(ALIAS.get(stem, stem))
        if key not in by_title and stem in UNLISTED:
            t, sec = UNLISTED[stem]
            by_title[key] = ({"t": t}, sec)
        if key not in by_title:
            unmatched.append(stem)
            continue
        b, sec = by_title[key]
        titles.append({
            "title": b["t"], "asin": b.get("a"), "series": sec, "stem": stem,
            "spans": r["spans"], "dialogue": r["dialogue"], "rate": r["rate"],
            "voices": r["cast"], "cues": r["cues"], "mode": r["mode"],
        })
    if unmatched:
        sys.exit("unmatched, add to ALIAS: %s" % unmatched)

    DATA.write_text(json.dumps({
        "generated": cast.get("generated"),
        "series_order": order,
        "titles": titles,
    }, indent=1) + "\n")
    print("audio_data.json: %d titles, %d series" % (len(titles), len(order)))


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Audio: Every Book, Performed in Cast | Carrier Press</title>
<meta name="description" content="{blurb}">
<link rel="canonical" href="https://{domain}/audio/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="Every character, in their own voice">
<meta property="og:description" content="{blurb}">
<meta property="og:url" content="https://{domain}/audio/">
<meta property="og:image" content="https://{domain}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
/* Scoped to this page, same reasoning as /labs/ and /apps/: styles.css is hand
   edited and shared, and every colour below is an existing token so dark mode
   follows without a second block. */

.au-intro p{{margin:0 0 16px;line-height:1.66;max-width:70ch}}
.au-intro p:last-child{{margin-bottom:0}}

/* The gate. A single panel, stated once, because the honest version of a
   paywall on a static site is a sentence and not a script. */
.au-gate{{
  background:var(--paper-2);border:1px solid var(--line);border-left:3px solid var(--gold);
  border-radius:4px;padding:24px 26px;margin:34px 0 0;
}}
.au-gate h2{{
  font-family:var(--sans);font-size:11.5px;font-weight:700;letter-spacing:.18em;
  text-transform:uppercase;color:var(--gold);margin:0 0 12px;
}}
.au-gate .price{{display:block;font-size:1.45rem;line-height:1.25;margin:0 0 12px;letter-spacing:-.01em}}
.au-gate p{{margin:0 0 12px;line-height:1.62;font-size:1rem}}
.au-gate p:last-child{{margin:0}}

.au-stats{{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:16px;margin:34px 0 0;
}}
.au-stat{{border:1px solid var(--line);border-radius:5px;padding:18px 19px}}
.au-stat b{{display:block;font-size:1.7rem;line-height:1.1;letter-spacing:-.02em;margin:0 0 5px}}
.au-stat span{{
  font-family:var(--sans);font-size:11.5px;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted);
}}

.au-series{{margin:52px 0 18px;padding-top:26px;border-top:1px solid var(--line)}}
.au-series:first-of-type{{border-top:0;padding-top:0;margin-top:8px}}
.au-series h2{{font-size:clamp(1.15rem,2.4vw,1.42rem);margin:0 0 6px;font-weight:400;letter-spacing:-.01em}}
.au-series .count{{
  font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;color:var(--gold);display:block;margin-bottom:6px;
}}
.au-series p{{margin:0;color:var(--ink-soft);font-size:.96rem;max-width:66ch}}

table.au-tbl{{width:100%;border-collapse:collapse;margin:0;font-size:.94rem}}
table.au-tbl th{{
  font-family:var(--sans);font-size:10.5px;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);text-align:left;
  padding:0 10px 8px 0;border-bottom:1px solid var(--line);white-space:nowrap;
}}
/* Numeric columns are right aligned and keep their gutter. Zeroing the right
   padding ran "Music cues" straight into "Mode" in the header and "4" into
   "Full cast" in the body. */
table.au-tbl th.n,table.au-tbl td.n{{text-align:right;padding-right:18px}}
table.au-tbl th.m,table.au-tbl td.m{{text-align:right;padding-right:0;white-space:nowrap}}
table.au-tbl td{{padding:11px 10px 11px 0;border-bottom:1px solid var(--line);vertical-align:baseline}}
table.au-tbl tr:last-child td{{border-bottom:0}}
table.au-tbl td.t{{width:52%}}
.au-mode{{
  font-family:var(--sans);font-size:10px;font-weight:700;letter-spacing:.11em;
  text-transform:uppercase;white-space:nowrap;
}}
.au-mode.cast{{color:var(--gold)}}
.au-mode.narrator{{color:var(--muted)}}

.au-foot{{
  margin:56px 0 0;padding-top:26px;border-top:1px solid var(--line);
  font-size:.95rem;line-height:1.62;color:var(--muted);max-width:70ch;
}}
.au-foot a{{color:var(--ink-soft)}}
.au-foot.au-last{{margin-top:14px;padding-top:0;border-top:0}}
.au-gate .au-go{{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 14px}}
table.au-tbl td a{{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}}
table.au-tbl td a:hover{{color:var(--gold);border-bottom-color:var(--gold)}}

/* A table of five numeric columns does not survive a phone. Below 700px the
   three that are diagnostics rather than decisions drop out, leaving the title,
   how many voices, and whether it is cast at all. */
@media(max-width:700px){{
  table.au-tbl .drop{{display:none}}
  table.au-tbl td.t{{width:auto}}
  .au-gate{{padding:18px 19px}}
}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="/">
      <img class="mark-dark" src="/assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="/assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>Carrier Press</span>
    </a>
    <nav class="nav" aria-label="Main">
      <a href="/fiction/">Fiction</a>
      <a href="/classics/">Classics</a>
      <a href="/blog/">Journal</a>
      <a href="/labs/">Labs</a>
      <a href="/apps/">Apps</a>
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
  </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; {year} Jeffrey L. Carrier. All rights reserved.</span>
      <span><a href="/">Carrier Press LLC</a>, Diamondhead, Mississippi.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

# {n} is the number of books in audio_data.json, spelled out, so the count can
# never go stale the way "Sixty-one" did.
BLURB = ("{n} books performed in Cast: a narrator and a voice for every character, "
         "made right in your browser. Hear the opening of any of them before you buy.")


def count_words(n):
    """84 -> "Eighty-four". Capitalised, because it opens a sentence."""
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    if n < 20:
        w = ones[n]
    elif n < 100:
        w = tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")
    else:
        w = str(n)
    return w[:1].upper() + w[1:]

SERIES_NOTE = {
    # Each line checked against audio_data.json on 2026-11-21 (84 titles).
    "The Gadget Sandbox Chronicles":
        "The first six Cubemelon books, five with a full cast and Portal Park read "
        "by one narrator. Written for readers who would rather be handed a "
        "controller than a chapter, and performed so it can go on in the car with "
        "a grown-up listening too.",
    "The Glitch Blocks":
        "Cubemelon books seven to twelve, all six with a full cast. The same eight "
        "voices carry across from the first six, so a reader who started at book "
        "one keeps the same cast.",
    "The Marjorie Corey Files":
        "All six performed with a full cast, The Complete Series included.",
    "The Keystone Cycle":
        "All five read by one narrator, straight through, the way they are written.",
    "The Classics Line":
        "Restored editions of the classics, each performed with a full cast or, "
        "where the book is told without spoken dialogue, by one narrator.",
}


def build():
    if not DATA.exists():
        sys.exit("no audio_data.json -- run with --refresh first")
    d = json.loads(DATA.read_text())
    titles = d["titles"]
    cast = [t for t in titles if t["mode"] == "cast"]
    narr = [t for t in titles if t["mode"] == "narrator"]
    voices = max(t["voices"] for t in titles)
    weighted = (sum(t["rate"] * t["dialogue"] for t in cast)
                / max(1, sum(t["dialogue"] for t in cast)))

    blurb = BLURB.format(n=count_words(len(titles)))
    cast_buy = commerce.for_app("cast")
    price = cast_buy.get("buy_price", "")
    price = price[:1].upper() + price[1:]
    url = books.url_for(json.loads(pathlib.Path("catalog.json").read_text()))

    b = [HEAD.format(domain=DOMAIN, blurb=e(blurb))]
    b.append('<section class="wrap" style="padding-top:52px">')
    b.append('<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Cast &middot; %d books</span></p>'
             % len(titles))
    b.append('<h1 style="font-size:clamp(1.7rem,4vw,2.5rem);font-weight:400;'
             'letter-spacing:-.02em;margin:0 0 22px">Every character, in their own voice.</h1>')

    b.append('<div class="au-intro">')
    b.append("<p>Press play and the book is performed: a narrator, and a voice of its own "
             "for every character, the same voices every time you come back. %d books are "
             "on the shelf, the Carrier Press originals, the American Firsts and the restored "
             "classics, with every series in reading order.</p>" % len(titles))
    b.append("</div>")

    b.append('<div class="au-gate">')
    b.append("<h2>Start listening</h2>")
    if price:
        b.append('<span class="price">%s</span>' % e(price))
    b.append("<p><strong>Every opening plays before you buy.</strong> Open Cast, choose a "
             "book and press play.</p>")
    b.append("<p>Love it? The whole book is one payment, with nothing to renew: a license "
             "to hear that book in full in Cast. Have EPUB files of your own? The Your Own "
             "Books membership performs those too.</p>")
    b.append('<p class="au-go"><a class="btn btn-gold" href="%s">Open Cast</a> '
             '<a class="btn btn-ink" href="/apps/cast/">Prices and the membership</a></p>'
             % CAST_APP)
    b.append("<p><strong>Coming back?</strong> Open Cast in the same browser and Continue "
             "listening has your latest books, each at your place.</p>")
    b.append("</div>")

    b.append('<div class="au-stats">')
    for n, label in ((len(titles), "books on the shelf"),
                     (len(cast), "with a full cast"),
                     (len(narr), "with one narrator"),
                     (voices, "voices in a full cast")):
        b.append('<div class="au-stat"><b>%s</b><span>%s</span></div>' % (e(n), e(label)))
    b.append("</div>")

    b.append('<p class="au-intro" style="margin-top:26px"><span style="color:var(--ink-soft);'
             'font-size:.95rem;line-height:1.62">A full cast gives each speaking character a '
             'voice of their own. A book told with little spoken dialogue is read straight '
             'through by one narrator. Every book below says which it is; tap a title for the '
             'book, or Listen to hear its opening.</span></p>')

    for sec in d["series_order"]:
        rows = [t for t in titles if t["series"] == sec]
        if not rows:
            continue
        b.append('<div class="au-series"><span class="count">%d %s</span><h2>%s</h2>%s</div>'
                 % (len(rows), "book" if len(rows) == 1 else "books", e(sec),
                    ("<p>%s</p>" % e(SERIES_NOTE[sec])) if sec in SERIES_NOTE else ""))
        b.append('<table class="au-tbl"><thead><tr>'
                 '<th class="t">Title</th>'
                 '<th class="n">Performed as</th>'
                 '<th class="m">Hear it</th></tr></thead><tbody>')
        for t in rows:
            page = url.get(t.get("asin"))
            if page and pathlib.Path(page.strip("/"), "index.html").exists():
                name = '<a href="%s">%s</a>' % (e(page), e(t["title"]))
            else:
                name = e(t["title"])
            mode = ("Full cast, %d voices" % t["voices"] if t["mode"] == "cast"
                    else "One narrator")
            b.append('<tr><td class="t">%s</td>'
                     '<td class="n"><span class="au-mode %s">%s</span></td>'
                     '<td class="m"><a href="%splay?stem=%s">Listen</a></td></tr>'
                     % (name, t["mode"], e(mode), CAST_APP, quote(t["stem"])))
        b.append("</tbody></table>")

    b.append('<p class="au-foot">Next: <a href="%s">hear an opening in Cast</a>, '
             '<a href="/pick/">find your next book in two questions</a>, or get '
             '<a href="/sprout/">Sprout</a> every Friday for what is new. Questions to '
             '<a href="mailto:%s">%s</a>.</p>' % (CAST_APP, SUPPORT, SUPPORT))
    # The AI note, last line of the page (author 2026-11-14).
    b.append('<p class="au-foot au-last">These are synthesised performances, made on your '
             'own device, not human narration.</p>')
    b.append("</section>")
    b.append(FOOT.format(year=datetime.date.today().year))

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text("\n".join(b), encoding="utf-8")
    nav.patch(OUT / "index.html")
    print("wrote audio/index.html  --  %d titles, %d cast, %d single voice, %.1f%% attributed"
          % (len(titles), len(cast), len(narr), weighted * 100))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    if a.refresh:
        refresh()
    build()
