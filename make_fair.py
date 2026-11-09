#!/usr/bin/env python3
"""
/fair/: the page a QR code on the book fair table opens (author 2026-11-08).

    python3 make_fair.py      # build.py runs it too, before the sitemap

WHO IT IS FOR. Someone who just held one of the books, now on a phone, often
with a child beside them. They want to find that book again, see what it is
about and where to buy it, and they want it fast. So the page is covers only,
grouped the way a table is laid out (young readers, mystery and suspense,
classics, money), one tap from each cover to its /books/ page, which carries
the story and the Buy buttons. No apps, music or support asks here: a fair
visitor came for books.

Booksellers, librarians and teachers also walk past a table, so the page ends
with one plain line on how they order. It promises nothing the press does not
do: no discounts, returns, free copies or author visits.

Everything shown is the catalogue's own data (titles, series, ages from the
shelf copy or the book's note). Nothing is written here about a book.
"""
import datetime, html, json, pathlib, re

import books
import nav

DOMAIN = "carrierpress.com"
TRADE_EMAIL = "jeffrey@carrierpress.com"

# The table's four groups, in the order a family usually meets them.
GROUPS = [
    ("young", "For young readers",
     "Mysteries, building adventures and money skills."),
    ("suspense", "Mystery and suspense",
     "Literary suspense, cozy mystery and historical crime fiction."),
    ("classics", "Restored classics",
     "Restored and annotated editions."),
    ("money", "Money and income",
     "Personal finance for adults."),
]


def e(x):
    return html.escape(str(x), quote=True)


def _ages(b, sec):
    m = re.search(r"ages? (\d+ to \d+)", b.get("note") or "")
    return m.group(1) if m else sec.get("ages")


def _group(b, sec):
    if b.get("soon"):
        return None
    if sec.get("kids") or "young readers" in (b.get("note") or "").lower():
        return "young"
    if sec["id"] == "classics":
        return "classics"
    if sec.get("nonfic"):
        return "money"
    return "suspense"


def shelves(D):
    """{group: [(heading, ages or None, [(book, sec, slug)])]} in catalogue order."""
    out = {g: [] for g, _, _ in GROUPS}
    index = {}
    for b, sec, slug in books.records(D):
        g = _group(b, sec)
        if not g:
            continue
        # The Atherton books sit on the Standalone shelf but form their own series.
        series = ("The Atherton Manor Mysteries" if g == "young" and not sec.get("kids")
                  else sec["name"])
        key = (g, series)
        if key not in index:
            index[key] = (series, [])
            out[g].append(index[key])
        index[key][1].append((b, sec, slug))
    return out


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Find your book | Carrier Press</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{domain}/fair/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="Find the book from our table">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://{domain}/fair/">
<meta property="og:image" content="https://{domain}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
.fr h1{{font-size:clamp(1.8rem,6vw,2.6rem);font-weight:400;letter-spacing:-.02em;margin:0 0 12px}}
.fr .lede{{font-size:1.08rem;line-height:1.6;color:var(--ink-soft);max-width:60ch;margin:0 0 20px}}
.fr-jump{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 8px;padding:0;list-style:none}}
.fr-jump a{{display:inline-block;font-family:var(--sans);font-size:14px;font-weight:600;text-decoration:none;
  color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:9px 14px}}
.fr-jump a:hover,.fr-jump a:focus-visible{{border-color:var(--gold)}}
.fr-g{{padding:34px 0 6px;border-top:1px solid var(--line);margin-top:30px}}
.fr-g>h2{{font-size:clamp(1.35rem,4vw,1.7rem);font-weight:400;margin:0 0 4px}}
.fr-g>p{{font-family:var(--sans);font-size:14px;color:var(--muted);margin:0 0 18px}}
.fr-s h3{{font-family:var(--sans);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin:20px 0 10px}}
.fr-s h3 span{{color:var(--gold);letter-spacing:.04em;text-transform:none;font-weight:600;margin-left:6px}}
.fr-row{{display:grid;grid-template-columns:repeat(auto-fill,minmax(92px,1fr));gap:16px 14px;margin:0;padding:0;list-style:none}}
.fr-row a{{display:block;text-decoration:none;color:var(--ink)}}
.fr-row img{{width:100%;height:auto;aspect-ratio:2/3;object-fit:cover;border-radius:4px;box-shadow:var(--shadow)}}
.fr-row span{{display:block;font-size:14px;line-height:1.3;margin-top:7px}}
.fr-row a:hover span,.fr-row a:focus-visible span{{text-decoration:underline;text-decoration-color:var(--gold)}}
.fr-box{{margin:40px 0 0;padding:22px;border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:6px;background:var(--paper-2)}}
.fr-box h2{{font-size:1.25rem;font-weight:400;margin:0 0 8px}}
.fr-box p{{margin:0 0 10px;line-height:1.6}}
.fr-box p:last-child{{margin:0}}
.fr-box .go{{display:inline-block;background:var(--gold);color:#151a33;font-family:var(--sans);font-weight:600;
  text-decoration:none;padding:11px 18px;border-radius:6px}}
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

DESC = ("Every Carrier Press book: young readers, mystery and suspense, "
        "restored classics and money guides. Tap a cover for the story and where to buy it.")


def build():
    D = json.loads(pathlib.Path("catalog.json").read_text())
    S = shelves(D)
    b = [HEAD.format(domain=DOMAIN, desc=e(DESC)),
         '<section class="wrap fr" style="padding-top:44px;padding-bottom:64px">',
         '<p class="sec-head" style="margin:0 0 10px"><span class="kicker">From our table</span></p>',
         '<h1>Find the book you picked up</h1>',
         '<p class="lede">All %d Carrier Press books are here, grouped the way the table is. '
         'Tap a cover to read what the book is about, see its formats and buy it.</p>'
         % sum(len(r) for g in S.values() for _, r in g),
         '<ul class="fr-jump">']
    b += ['<li><a href="#%s">%s</a></li>' % (g, e(name)) for g, name, _ in GROUPS if S[g]]
    b.append('</ul>')
    for g, name, line in GROUPS:
        if not S[g]:
            continue
        b += ['<section class="fr-g" id="%s" aria-labelledby="h-%s">' % (g, g),
              '<h2 id="h-%s">%s</h2>' % (g, e(name)), '<p>%s</p>' % e(line)]
        for series, rows in S[g]:
            ages = {_ages(bk, sec) for bk, sec, _ in rows} - {None}
            tag = (' <span>Ages %s</span>' % e(" / ".join(sorted(ages)))) if ages else ''
            b += ['<div class="fr-s">', '<h3>%s%s</h3>' % (e(series), tag), '<ul class="fr-row">']
            for bk, sec, slug in rows:
                t = books.display_title(bk, sec)
                b.append('<li><a href="/books/%s/"><img src="/assets/covers/%s.jpg" alt="" loading="lazy" '
                         'decoding="async" width="104" height="156"><span>%s</span></a></li>'
                         % (slug, bk["a"], e(t)))
            b += ['</ul>', '</div>']
        b.append('</section>')
    b += ['<div class="fr-box">', '<h2>Read the opening first</h2>',
          '<p>The first chapters of The King in Yellow, free by email.</p>',
          '<p><a class="go" href="/#free">Get the free sample</a></p>', '</div>',
          '<div class="fr-box">', '<h2>Booksellers, librarians and teachers</h2>',
          '<p>Each book\'s page lists the ISBN for every format. To order for a store, a library '
          'or a classroom, write to <a href="mailto:%s">%s</a>.</p>' % (TRADE_EMAIL, TRADE_EMAIL),
          '</div>', '</section>', FOOT.format(year=datetime.date.today().year)]
    s = "\n".join(b)
    for bad in ("—", "–", "&mdash;", "&ndash;"):
        assert bad not in s, "dash in fair page"
    out = pathlib.Path("fair")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(s, encoding="utf-8")
    nav.patch(out / "index.html")
    n = sum(len(r) for g in S.values() for _, r in g)
    print("wrote fair/index.html  --  %d books in %d groups" % (n, sum(1 for g in S.values() if g)))


if __name__ == "__main__":
    build()
