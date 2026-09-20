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

THE PAYWALL IS IN THE APP, AND THE PAGE SAYS SO. This site is static GitHub
Pages and can enforce nothing; a gate written in JavaScript here is a gate with
the key taped to it. The real gate is a StoreKit unlock in Cast. Stating that
plainly is better than a fake one, and it is the same position /apps/ takes.
"""
import argparse, html, json, pathlib, sys, re, unicodedata, datetime

DOMAIN = "carrierpress.com"
OUT = pathlib.Path("audio")
DATA = pathlib.Path("audio_data.json")
CAST_INDEX = pathlib.Path("/Users/jeffreycarrier/Projects/Cast/scripts/index.json")
SUPPORT = "support@carrierpress.com"

UNLOCK = "$19.99 once"

# Filenames that do not normalise onto a catalogue title. Three of forty-eight,
# each for its own reason, so they are named rather than pattern-matched.
ALIAS = {
    "28_Marjorie_Corey_Complete_Series": "The Complete Series",
    "36_Who_Wants_To_Be_Greek": "Who Wants To Be Greek? English Narrative Edition",
    "42_Side_Hustle_Jr": "Side Hustle Junior",
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
<title>Audio | Carrier Press</title>
<meta name="description" content="{blurb}">
<link rel="canonical" href="https://{domain}/audio/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="The catalogue, performed">
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
      <a href="/#fiction">Fiction</a>
      <a href="/#classics">Classics</a>
      <a href="/blog/">Journal</a>
      <a href="/labs/">Labs</a>
      <a href="/apps/">Apps</a>
      <a href="/audio/">Audio</a>
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
      <span><a href="/">Carrier Press</a> is an imprint of Jeffrey L. Carrier.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

BLURB = ("Forty-eight books compiled into performance scripts: a voice per character, "
         "narrator, and music under the scenes that earn it. Performed on your device "
         "by Cast. One unlock opens the catalogue.")

SERIES_NOTE = {
    "The Gadget Sandbox Chronicles":
        "Twelve books, eight voices each, and the highest cast density in the "
        "catalogue. Written for readers who would rather be handed a controller "
        "than a chapter, and performed so a parent can put it on in the car.",
    "The Marjorie Corey Files":
        "Conventionally tagged prose, which is what the attribution pass is best at.",
    "The Classics Line":
        "Restored public-domain editions. Where a book has no quotation marks at "
        "all it is performed as a single voice, which is what it is.",
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

    b = [HEAD.format(domain=DOMAIN, blurb=e(BLURB))]
    b.append('<section class="wrap" style="padding:52px 0 0">')
    b.append('<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Cast</span></p>')
    b.append('<h1 style="font-size:clamp(1.7rem,4vw,2.5rem);font-weight:400;'
             'letter-spacing:-.02em;margin:0 0 22px">The catalogue, performed</h1>')

    b.append('<div class="au-intro">')
    b.append("<p>Every book in the catalogue has been compiled into a performance "
             "script: who speaks each line, which voice they carry, and where music "
             "sits under the scene. The reading of the book happens once, offline, on "
             "the machine these were written on. The performance happens on your "
             "device, at the moment you press play.</p>")
    b.append("<p><strong>There is no audio file on this page, and that is deliberate.</strong> "
             "Amazon will generate a free Audible edition of a book only while no "
             "audiobook edition exists, and releasing audio anywhere else forfeits that "
             "permanently, per title. Cast performs inside the app and creates no "
             "audiobook edition, so the door stays open on all "
             "%d of these.</p>" % len(titles))
    b.append("</div>")

    b.append('<div class="au-gate">')
    b.append("<h2>What it costs</h2>")
    b.append('<span class="price">%s, for the whole catalogue</span>' % e(UNLOCK))
    b.append("<p><strong>The first chapter of any title is free, in full cast.</strong> "
             "Not a clip and not a countdown: the opening chapter, performed the way "
             "the rest of the book is performed, so what you are deciding about is the "
             "thing itself.</p>")
    b.append("<p>One payment then opens every title here, including the ones added "
             "later. It is not a subscription, and there is no per-book price, because "
             "the expensive part was compiling the catalogue once rather than serving "
             "it many times.</p>")
    b.append("<p><strong>The unlock happens inside Cast, not on this page.</strong> "
             "This site is a set of static files and can enforce nothing; a paywall "
             "written in JavaScript here would be a lock with the key taped to it. "
             "Saying so is better than pretending otherwise.</p>")
    b.append("</div>")

    b.append('<div class="au-stats">')
    for n, label in ((len(titles), "books compiled"),
                     (len(cast), "full cast"),
                     (len(narr), "single voice"),
                     (voices, "voices at most"),
                     ("%.0f%%" % (weighted * 100), "lines attributed")):
        b.append('<div class="au-stat"><b>%s</b><span>%s</span></div>' % (e(n), e(label)))
    b.append("</div>")

    b.append('<p class="au-intro" style="margin-top:26px"><span style="color:var(--ink-soft);'
             'font-size:.95rem;line-height:1.62">Attribution is the share of spoken lines '
             'the compiler can assign to a named character with confidence. It tracks the '
             'way a book is written rather than how hard the compiler tries: prose that '
             'tags its dialogue reaches the nineties, and prose that does not is honest '
             'about being a single voice. Both are listed below, and which one a book is '
             'shown as is measured, not chosen.</span></p>')

    for sec in d["series_order"]:
        rows = [t for t in titles if t["series"] == sec]
        if not rows:
            continue
        b.append('<div class="au-series"><span class="count">%d %s</span><h2>%s</h2>%s</div>'
                 % (len(rows), "book" if len(rows) == 1 else "books", e(sec),
                    ("<p>%s</p>" % e(SERIES_NOTE[sec])) if sec in SERIES_NOTE else ""))
        b.append('<table class="au-tbl"><thead><tr>'
                 '<th class="t">Title</th>'
                 '<th class="n">Voices</th>'
                 '<th class="n drop">Spoken lines</th>'
                 '<th class="n drop">Attributed</th>'
                 '<th class="n drop">Music cues</th>'
                 '<th class="m">Mode</th></tr></thead><tbody>')
        for t in rows:
            b.append('<tr><td class="t">%s</td>'
                     '<td class="n">%d</td>'
                     '<td class="n drop">%s</td>'
                     '<td class="n drop">%.0f%%</td>'
                     '<td class="n drop">%d</td>'
                     '<td class="m"><span class="au-mode %s">%s</span></td></tr>'
                     % (e(t["title"]), t["voices"], "{:,}".format(t["dialogue"]),
                        t["rate"] * 100, t["cues"], t["mode"],
                        "Full cast" if t["mode"] == "cast" else "Single voice"))
        b.append("</tbody></table>")

    b.append('<p class="au-foot">Cast is not on a store yet, so nothing here can be '
             'bought today and there is no button that pretends otherwise. '
             '<a href="/apps/">Apps</a> carries its status alongside the rest of the '
             'tools. These are synthesised performances rendered on your own device, '
             'not human narration, and the page says which books are genuinely cast '
             'and which are one voice so that is not a surprise. Questions to '
             '<a href="mailto:%s">%s</a>.</p>' % (SUPPORT, SUPPORT))
    b.append("</section>")
    b.append(FOOT.format(year=datetime.date.today().year))

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text("\n".join(b), encoding="utf-8")
    print("wrote audio/index.html  --  %d titles, %d cast, %d single voice, %.1f%% attributed"
          % (len(titles), len(cast), len(narr), weighted * 100))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    if a.refresh:
        refresh()
    build()
