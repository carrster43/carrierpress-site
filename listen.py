#!/usr/bin/env python3
"""
Listening: a block on each /books/<slug>/ page, and the /podcast/ page.

    python3 listen.py --refresh   # re-read Cast's web shelf into cast_shelf.json
    python3 listen.py             # write podcast/index.html

Two things, each present only where a title has it.

CAST. A book Cast performs gets a line under its Buy row: buy the performance
in the web app, or buy that book's performance. The buy link is the one Cast's
own shelf builds, /l/cast?variant=<NN · Title>&wanted=true, so it opens that
book's Gumroad checkout. Prices and version names live in Cast, in
~/Projects/Cast/player/lib/web-shelf.ts; --refresh copies them here so this site
still builds on a machine that has never seen Cast. Renaming a Gumroad version
without re-running --refresh breaks that one book's link.

THE PODCAST. Twenty minute conversations about a book, made with Google
NotebookLM from our own edition, labelled as AI voices wherever they play.

*** AN EPISODE IS A DISCUSSION, NEVER A READING. ***
make_audio.py explains why the site hosts no audiobook: KDP Virtual Voice needs
a title with no audiobook edition, and a wide audio release forfeits it for good.
An episode reads no chapter, has no ASIN and is not attached to the Amazon
record, so it is not an audiobook edition. Never put a reading of the text in
EPISODES. Twelve Minutes on River Road stays in SOON until its legal pass is
done (author 2026-11-02); the episode exists and is not published.
"""
import argparse, datetime, html, json, pathlib, re, sys, unicodedata
from urllib.parse import quote

import commerce
import nav

DOMAIN = "carrierpress.com"
SHELF = pathlib.Path("cast_shelf.json")
CAST_TS = pathlib.Path("/Users/jeffreycarrier/Projects/Cast/player/lib/web-shelf.ts")
GUMROAD_CAST = "https://jeffreycarrier.gumroad.com/l/cast"
CAST_APP = "/cast/app/"
AMZ = "https://www.amazon.com/dp/{}"

# asin, audio file stem under /podcast/audio/, episode title, runtime, book title.
# `amazon` is set only for a book with no /books/ page yet, so the episode can
# still link somewhere real. Runtimes are afinfo's, rounded down to the second.
EPISODES = [
    dict(asin="B0H7W7VY7S", file="the-king-in-yellow", book="The King in Yellow",
         title="The Mind Virus Behind True Detective", runtime="21:29"),
    dict(asin="B0HGG934BB", file="carcosa", book="Carcosa",
         title="How Hastur Became Cosmic Horror", runtime="22:47"),
    dict(asin="B0HQ55DVX2", file="lovecraft-volume-one",
         book="The Call of Cthulhu and Other Mythos Tales",
         title="How Lovecraft Built Cosmic Horror", runtime="21:44"),
    dict(asin="B0H7LYK2QQ", file="dr-mabuse-the-gambler", book="Dr. Mabuse the Gambler",
         title="The Uncensored Return of Dr. Mabuse", runtime="22:06"),
    dict(asin="B0HHJSF9SP", file="one-minute-past-noon", book="One Minute Past Noon",
         title="The 1920 Bombing Wall Street Erased", runtime="19:02"),
    dict(asin="B0HMK4LL3B", file="mrs-kehoe", book="Mrs. Kehoe",
         title="The Seven Words of Nellie Kehoe", runtime="18:52"),
    dict(asin="B0H483NLCV", file="the-starlight-secret-society",
         book="The Starlight Secret Society",
         title="Puzzle Design in The Starlight Secret Society", runtime="21:27"),
    dict(asin="B0H7QFWVXG", file="the-blue-castle", book="The Blue Castle",
         title="L.M. Montgomery's Hidden Masterpiece The Blue Castle", runtime="20:36"),
]

# Episodes made or being made, not yet published here.
SOON = [
    dict(asin="B0HHJK9GMT", book="Twelve Minutes on River Road"),
]

# Author 2026-11-08: no podcast is free unless it is a promotion or limited-time
# offer. The episodes below are free only until this date (end of day, the
# listener's clock); after it the script in _free_offer() hides each player.
# Change the date here, then rebuild. Never add an episode as free past it.
FREE_UNTIL = datetime.date(2026, 11, 30)
FREE_LABEL = "Free for a limited time, until %s." % FREE_UNTIL.strftime("%B %-d, %Y")
FREE_ENDED = "The free listening offer has ended."


def _free_offer():
    """Limited-time label plus a script that retires the players after FREE_UNTIL."""
    end = (FREE_UNTIL + datetime.timedelta(days=1)).isoformat()
    return ('<p class="ls-free" data-until="%s">%s</p>'
            '<script>(function(){var n=document.currentScript.previousElementSibling;'
            'if(new Date()>=new Date(n.getAttribute("data-until")+"T00:00:00")){'
            'n.textContent=%s;var r=n.parentNode;'
            'r.querySelectorAll("audio").forEach(function(a){a.remove()});}})();</script>'
            % (end, e(FREE_LABEL), json.dumps(FREE_ENDED)))

# Members' episodes (author 2026-11-06): Books and All Access tiers of Carrier
# Press Access. The audio lives in the gate's bundles, never in this public repo;
# make_member_episodes.py writes this file. The 8 EPISODES above stay free.
_MEMBERS = pathlib.Path("podcast_members.json")
MEMBERS = json.loads(_MEMBERS.read_text()) if _MEMBERS.exists() else {"episodes": [], "coming": []}
SPOILER_NOTE = "It may discuss the plot, so you may want to read the book first."
ACCESS_LINE = ("Included with the Books and All Access tiers of "
               "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">Carrier Press Access</a>, %s."
               % (commerce.ACCESS_URL, commerce.ACCESS_PRICE))

AI_NOTE = ("Two AI hosts talk through this edition. Made with Google NotebookLM "
           "from the book itself.")


def e(x):
    return html.escape(str(x), quote=True)


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\b(the|a|an)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def refresh():
    """Join Cast's web shelf onto the site catalogue by title; write cast_shelf.json."""
    if not CAST_TS.exists():
        sys.exit("no Cast web shelf at %s" % CAST_TS)
    rows = re.findall(r'\{ n: "(\d\d)", title: "((?:[^"\\]|\\.)*)", cents: (\d+) \}',
                      CAST_TS.read_text())
    cat = {}
    for sec in json.loads(pathlib.Path("catalog.json").read_text())["sections"]:
        for b in sec["books"]:
            cat.setdefault(norm(b["t"]), b["a"])
    # Whether Cast casts a book or reads it in one voice is measured by its
    # compiler and committed in audio_data.json, keyed by the same NN.
    mode = {t["stem"][:2]: t["mode"] for t in
            json.loads(pathlib.Path("audio_data.json").read_text())["titles"]}
    out, unmatched = {}, []
    for n, title, cents in rows:
        title = title.replace('\\"', '"')
        asin = cat.get(norm(title))
        if not asin:
            unmatched.append("%s %s" % (n, title))
            continue
        out[asin] = {"n": n, "title": title, "cents": int(cents), "mode": mode.get(n, "cast")}
    SHELF.write_text(json.dumps({"read": datetime.date.today().isoformat(),
                                 "books": out}, indent=1, sort_keys=True) + "\n")
    print("cast_shelf.json: %d of %d books matched" % (len(out), len(rows)))
    if unmatched:
        print("not on the site, no link:", "; ".join(unmatched))


def _shelf():
    return json.loads(SHELF.read_text())["books"] if SHELF.exists() else {}


CAST = _shelf()


def cast_buy_url(c):
    return "%s?variant=%s&wanted=true" % (GUMROAD_CAST, quote("%s · %s" % (c["n"], c["title"])))


def price(cents):
    return "$%d.%02d" % divmod(cents, 100)


def episode(asin):
    return next((x for x in EPISODES if x["asin"] == asin), None)


def member(asin):
    return next((x for x in MEMBERS["episodes"] if x["asin"] == asin), None)


def _member_player(ep):
    """No src until the server says yes: podcastgate.js fills it in for a member."""
    return ('<audio controls preload="none" hidden data-src="/podcast/app/%s.m4a" '
            'aria-label="Podcast episode: %s"></audio>' % (e(ep["slug"]), e(ep["title"])))


def gate_form():
    """The one key box on a page. assets/podcastgate.js sends the key to the gate."""
    return ('<div class="gate pc-gate" id="pc-gate">'
            '<form novalidate><label for="pc-key">Already a member?</label> '
            '<input id="pc-key" name="key" autocomplete="off" spellcheck="false" '
            'placeholder="Paste your license key"> <button type="submit">Unlock the podcast</button></form>'
            '<div class="pc-open" hidden><button type="button" class="pc-forget">Remove my key from this browser</button></div>'
            '<p class="gate-note" role="status"></p></div>'
            '<script src="/assets/podcastgate.js" defer></script>')


def _player(ep):
    return ('<audio controls preload="none" src="/podcast/audio/%s.m4a" '
            'aria-label="Podcast episode: %s"></audio>' % (e(ep["file"]), e(ep["title"])))


CSS = """.bk .listen{margin:36px 0 0;padding:26px 0 0;border-top:1px solid var(--line);max-width:760px}
.bk .listen>h2{font-family:var(--sans);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin:0 0 14px}
.ls-row{background:var(--paper-2);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:4px;padding:18px 20px;margin:0 0 14px}
.ls-k{font-family:var(--sans);font-size:11.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0 0 6px}
.ls-t{font-size:1.08rem;margin:0 0 10px;color:var(--ink)}
.ls-t span{font-family:var(--sans);font-size:13px;color:var(--muted);margin-left:8px}
.ls-row audio{width:100%;margin:2px 0 8px}
.ls-row p{margin:0 0 8px;line-height:1.55}
.ls-row p:last-child{margin-bottom:0}
.ls-free{font-family:var(--sans);font-size:13px;font-weight:600;color:var(--gold);margin:0 0 8px}
.ls-note{font-family:var(--sans);font-size:13px;color:var(--muted)}
.ls-note a{color:var(--ink-soft)}
.ls-acts{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}
.ls-acts a{font-family:var(--sans);font-size:15px;font-weight:600;text-decoration:none}
.ls-acts .go{background:var(--gold);color:#151a33;padding:9px 16px;border-radius:6px}
.ls-acts .go:hover{background:var(--gold-bright)}
.ls-acts .alt{color:var(--ink-soft);border-bottom:1px solid var(--line)}
.ls-acts .alt:hover{color:var(--ink)}
.pc-gate{margin:10px 0 8px;font-family:var(--sans);font-size:14px}
.pc-gate label{display:block;margin:0 0 6px;color:var(--ink-soft)}
.pc-gate input{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:6px;width:min(100%,300px);background:var(--card);color:var(--ink)}
.pc-gate button{font:inherit;font-weight:600;padding:8px 14px;border:1px solid var(--line);border-radius:6px;background:transparent;color:var(--ink);cursor:pointer}
.pc-gate .gate-note{margin:6px 0 0}
.pc-gate .gate-note.bad{color:#b3261e}"""


def book_block(asin, title):
    """The Listen section for one book page, or [] when the book has neither."""
    ep, c = episode(asin), CAST.get(asin)
    soon = any(s["asin"] == asin for s in SOON)
    mem = member(asin)
    coming = any(s["asin"] == asin for s in MEMBERS["coming"])
    if not (ep or c or soon or mem or coming):
        return []
    out = ['<section class="listen" aria-labelledby="h-listen">',
           '<h2 id="h-listen">Listen</h2>']
    if c:
        out += ['<div class="ls-row">', '<p class="ls-k">The whole book, performed in Cast</p>',
                '<p>%s, played in your browser. The full '
                'performance is yours to keep.</p>'
                % ("A narrator and a voice for each character" if c.get("mode") != "narrator"
                   else "Read in one voice from start to finish"),
                '<p class="ls-acts">'
                '<a class="go" href="%s" target="_blank" rel="noopener" '
                'aria-label="Buy the Cast performance of %s, %s">Buy the performance, %s</a>'
                '</p>'
                % (e(cast_buy_url(c)), e(title), price(c["cents"]), price(c["cents"])),
                '<p class="ls-note">Checkout on Gumroad, license key by email. '
                '<a href="/apps/cast/">About Cast</a></p>', '</div>']
    if ep:
        out += ['<div class="ls-row">', '<p class="ls-k">The Carrier Press podcast</p>',
                '<p class="ls-t">%s<span>%s</span></p>' % (e(ep["title"]), e(ep["runtime"])),
                _free_offer(),
                _player(ep),
                '<p class="ls-note">%s <a href="/podcast/">All episodes</a></p>' % e(AI_NOTE),
                '</div>']
    elif mem:
        out += ['<div class="ls-row">', '<p class="ls-k">The Carrier Press podcast, for members</p>',
                '<p class="ls-t">%s<span>%s</span></p>' % (e(mem["title"]), e(mem["runtime"])),
                _member_player(mem),
                '<p class="pc-lock">%s</p>' % ACCESS_LINE,
                gate_form(),
                '<p class="ls-note">%s %s <a href="/podcast/">All episodes</a></p>' % (e(SPOILER_NOTE), e(AI_NOTE)),
                '</div>']
    elif coming:
        out += ['<div class="ls-row">', '<p class="ls-k">The Carrier Press podcast, for members</p>',
                '<p>An episode on this book is on its way. %s '
                '<a href="/podcast/">See the podcast</a></p>' % ACCESS_LINE, '</div>']
    elif soon:
        out += ['<div class="ls-row">', '<p class="ls-k">The Carrier Press podcast</p>',
                '<p>An episode on this book is coming soon. '
                '<a href="/podcast/">Hear the episodes already out</a></p>', '</div>']
    out.append('</section>')
    return out


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Podcast | Carrier Press</title>
<meta name="description" content="{blurb}">
<link rel="canonical" href="https://{domain}/podcast/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="The Carrier Press podcast">
<meta property="og:description" content="{blurb}">
<meta property="og:url" content="https://{domain}/podcast/">
<meta property="og:image" content="https://{domain}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
.pc-intro p{{margin:0 0 16px;line-height:1.66;max-width:70ch}}
.pc-ep{{display:grid;grid-template-columns:96px minmax(0,1fr);gap:22px;align-items:start;
  padding:26px 0;border-top:1px solid var(--line)}}
.pc-ep img{{width:96px;height:auto;border-radius:3px;box-shadow:var(--shadow)}}
.pc-ep h2{{font-size:clamp(1.1rem,2.4vw,1.35rem);font-weight:400;margin:0 0 4px;letter-spacing:-.01em}}
.pc-ep .bk-of{{font-family:var(--sans);font-size:14px;color:var(--ink-soft);margin:0 0 10px}}
.pc-ep .bk-of a{{color:inherit}}
.pc-ep .rt{{font-family:var(--sans);font-size:13px;color:var(--muted);margin-left:8px}}
.pc-ep audio{{width:100%;margin:4px 0 0}}
.pc-ep .ls-free{{font-family:var(--sans);font-size:13px;font-weight:600;color:var(--gold);margin:0 0 6px}}
.pc-soon{{margin:44px 0 0;padding-top:26px;border-top:1px solid var(--line)}}
.pc-soon h2{{font-family:var(--sans);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin:0 0 10px}}
.pc-soon ul{{margin:0;padding-left:18px;line-height:1.8}}
.pc-foot{{margin:44px 0 0;padding-top:22px;border-top:1px solid var(--line);font-size:.95rem;
  line-height:1.62;color:var(--muted);max-width:70ch}}
@media(max-width:560px){{.pc-ep{{grid-template-columns:64px minmax(0,1fr);gap:14px}}.pc-ep img{{width:64px}}}}
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

BLURB = ("Twenty minute conversations about Carrier Press books: where each one came "
         "from and what this edition adds.")


def book_url(asin):
    import books  # late: books imports this module
    for b, sec, slug in books.records(json.loads(pathlib.Path("catalog.json").read_text())):
        if b["a"] == asin:
            return "/books/%s/" % slug
    return None


def build():
    b = [HEAD.format(domain=DOMAIN, blurb=e(BLURB))]
    b.append('<section class="wrap" style="padding-top:52px;padding-bottom:64px">')
    b.append('<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Podcast</span></p>')
    b.append('<h1 style="font-size:clamp(1.7rem,4vw,2.5rem);font-weight:400;'
             'letter-spacing:-.02em;margin:0 0 22px">The Carrier Press podcast</h1>')
    b.append('<div class="pc-intro"><p>%s</p><p>%s</p></div>' % (e(BLURB), e(AI_NOTE.replace(
                 "this edition", "each edition"))))
    for ep in EPISODES:
        url = book_url(ep["asin"])
        href, ext = (url, "") if url else (ep["amazon"], ' target="_blank" rel="noopener"')
        cover = ("/assets/covers/%s.jpg" % ep["asin"]
                 if pathlib.Path("assets/covers/%s.jpg" % ep["asin"]).exists() else None)
        b.append('<article class="pc-ep">')
        b.append('<a href="%s"%s>%s</a>' % (e(href), ext, '<img src="%s" alt="Cover of %s" '
                 'loading="lazy" width="96" height="153">' % (cover, e(ep["book"]))
                 if cover else ''))
        b.append('<div><h2>%s<span class="rt">%s</span></h2>' % (e(ep["title"]), e(ep["runtime"])))
        b.append('<p class="bk-of">On <a href="%s"%s><em>%s</em></a>%s</p>'
                 % (e(href), ext, e(ep["book"]), "" if url else ", available on Amazon"))
        b.append(_free_offer())
        b.append(_player(ep))
        b.append('</div></article>')
    if MEMBERS["episodes"]:
        b.append('<div class="pc-soon"><h2>For Carrier Press Access members</h2>')
        b.append('<p class="pc-lock">%s %s</p>' % (ACCESS_LINE, e(SPOILER_NOTE)))
        b.append(gate_form())
        b.append('</div>')
    for ep in MEMBERS["episodes"]:
        url = book_url(ep["asin"])
        cover = ("/assets/covers/%s.jpg" % ep["asin"]
                 if pathlib.Path("assets/covers/%s.jpg" % ep["asin"]).exists() else None)
        b.append('<article class="pc-ep">')
        b.append('<a href="%s">%s</a>' % (e(url), '<img src="%s" alt="Cover of %s" loading="lazy" '
                 'width="96" height="153">' % (cover, e(ep["book"])) if cover else ''))
        b.append('<div><h2>%s<span class="rt">%s</span></h2>' % (e(ep["title"]), e(ep["runtime"])))
        b.append('<p class="bk-of">On <a href="%s"><em>%s</em></a></p>' % (e(url), e(ep["book"])))
        b.append(_member_player(ep))
        b.append('</div></article>')
    b.append('<div class="pc-soon"><h2>Coming soon</h2><ul>')
    for s in SOON + MEMBERS["coming"]:
        url = book_url(s["asin"])
        b.append('<li>%s</li>' % ('<a href="%s"><em>%s</em></a>' % (url, e(s["book"]))
                                  if url else '<em>%s</em>' % e(s["book"])))
    b.append('</ul></div>')
    b.append('<p class="pc-foot">These are discussions of the books, not readings of them. '
             'To hear a whole book performed, a voice for each character, see '
             '<a href="/audio/">Audio</a>. Questions to '
             '<a href="mailto:support@carrierpress.com">support@carrierpress.com</a>.</p>')
    b.append('</section>')
    b.append(FOOT.format(year=datetime.date.today().year))
    out = pathlib.Path("podcast")
    out.mkdir(exist_ok=True)
    s = "\n".join(b)
    for bad in ("—", "–", "&mdash;", "&ndash;"):
        assert bad not in s, "dash in podcast page"
    (out / "index.html").write_text(s, encoding="utf-8")
    nav.patch(out / "index.html")
    for ep in EPISODES:
        assert (out / "audio" / (ep["file"] + ".m4a")).exists(), "missing audio " + ep["file"]
    print("wrote podcast/index.html  --  %d episodes, %d coming soon" % (len(EPISODES), len(SOON)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    if ap.parse_args().refresh:
        refresh()
        CAST = _shelf()
    build()
