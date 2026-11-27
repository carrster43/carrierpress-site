#!/usr/bin/env python3
"""
/guides/ and /guides/<book-slug>/: the Reader's Guide from each annotated
classic, as its own page (2026-11-27, "start building" the search pages).

    python3 make_guides.py      # build.py runs it too, before the sitemap

WHY THESE PAGES EXIST. Book clubs, teachers and students search for
"<title> discussion questions" and "<title> study guide". Those searches are
won by small pages that answer exactly that, not by Wikipedia or Amazon, and
the questions are already written: every annotated classic carries a Reader's
Guide in its back matter. Each page links to the edition it comes from.

SOURCE. guides_src/<book-slug>.md, copied verbatim from the edition's
2_EDITION/READERS_GUIDE.md under A_Publishing_House/Classics/Classics_Republish.
The slug is the book's own /books/<slug>/ slug, so a guide whose book leaves
the catalogue fails the build instead of linking to a missing page. books.py
reads the same folder to put a link on the book page.

WHAT IS CHANGED FROM THE SOURCE, AND ONLY THIS:
  - the "# A Reader's Guide" title line is dropped (the page has its own h1);
  - the questions section is moved first, because that is what was searched;
  - timeline lines become a year column and a text column, which drops the
    dash some guides use between the two, and a year range's dash is written
    "to" (1791 to 1792). No other words change. A dash left anywhere else
    fails the build, so a new guide with a dash in its prose gets a human
    decision rather than a silent edit.

Rules kept here: no em or en dashes; never name the public domain source.
"""
import datetime, html, json, pathlib, re

import _md
import books
import nav

DOMAIN = "carrierpress.com"
SRC = pathlib.Path("guides_src")
OUT = pathlib.Path("guides")

# Titles too long for "<title> Discussion Questions | Carrier Press" in 65 chars.
SHORT = {
    "the-extraordinary-adventures-of-arsene-lupin": "Arsène Lupin",
    "sweeney-todd-volume-two": "Sweeney Todd: The String of Pearls",
}
# The edition a guide sits in, when the page title should not be the volume's.
NAME = {"sweeney-todd-volume-two": "Sweeney Todd: The String of Pearls"}


def e(x):
    return html.escape(str(x), quote=True)


def slugs():
    return sorted(p.stem for p in SRC.glob("*.md"))


def _sections(md):
    """[(heading, body)] from a guide, the title line dropped. Text before the
    first heading comes back with heading None."""
    out, head, buf = [], None, []
    for ln in md.replace("\r\n", "\n").split("\n"):
        if ln.startswith("# ") and not ln.startswith("## "):
            continue
        m = re.match(r"^##\s+(.*)$", ln)
        if m:
            if head is not None or "".join(buf).strip():
                out.append((head, "\n".join(buf).strip()))
            head, buf = m.group(1).strip(), []
        else:
            buf.append(ln)
    if head is not None or "".join(buf).strip():
        out.append((head, "\n".join(buf).strip()))
    return out


def _range(t):
    return re.sub(r"(\w)\s*[–—]\s*(\w)", r"\1 to \2", t)


def _timeline(body):
    rows = []
    for ln in body.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        m = re.match(r"^(?:[-*]\s+)?(\*\*|\*)(.+?)\1\s*(?:[—–]\s*)?(.*)$", ln)
        if not m:
            raise SystemExit("make_guides: timeline line not understood: %r" % ln)
        rows.append('<dt>%s</dt><dd>%s</dd>' % (_md._inline(_range(m.group(2))),
                                                  _md._inline(m.group(3))))
    return '<dl class="gd-tl">' + "".join(rows) + "</dl>"


def _questions(body):
    """Numbered questions, which some guides separate with blank lines. Any
    other text in the section is kept as a paragraph, in place."""
    items, out = [], []
    for block in re.split(r"\n\s*\n", body):
        for ln in block.split("\n"):
            m = re.match(r"^\s*\d+\.\s+(.*)$", ln)
            if m:
                items.append(m.group(1).strip())
            elif ln.strip() and items:
                items[-1] += " " + ln.strip()
            elif ln.strip():
                out.append("<p>%s</p>" % _md._inline(ln.strip()))
    return "".join(out) + '<ol class="gd-q">' + "".join(
        "<li>%s</li>" % _md._inline(q) for q in items) + "</ol>", len(items)


def _who(heading):
    """'L. M. Montgomery: a brief timeline' -> 'L. M. Montgomery'."""
    m = re.match(r"^(.*?):\s*a brief timeline", heading, re.I)
    return m.group(1).strip() if m else None


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{domain}{path}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://{domain}{path}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{ld}</script>
<style>
.gd h1{{font-size:clamp(1.8rem,6vw,2.5rem);font-weight:400;letter-spacing:-.02em;margin:0 0 12px}}
.gd .lede{{font-size:1.08rem;line-height:1.6;color:var(--ink-soft);max-width:64ch;margin:0 0 18px}}
.gd h2{{font-size:clamp(1.3rem,4vw,1.6rem);font-weight:400;margin:34px 0 10px;padding-top:26px;border-top:1px solid var(--line)}}
.gd p,.gd li,.gd dd{{line-height:1.65;max-width:68ch}}
.gd-q{{padding-left:1.4em}} .gd-q li{{margin:0 0 14px}}
.gd-tl{{display:grid;grid-template-columns:max-content 1fr;gap:8px 18px;margin:0}}
.gd-tl dt{{font-family:var(--sans);font-weight:600;font-size:14px;color:var(--ink-soft);padding-top:3px}}
.gd-tl dd{{margin:0}}
.gd-book{{display:flex;gap:18px;align-items:flex-start;margin:22px 0 8px;padding:16px;border:1px solid var(--line);border-radius:8px;max-width:640px}}
.gd-book img{{width:96px;height:auto;border-radius:4px;box-shadow:var(--shadow);flex:none}}
.gd-book p{{margin:0 0 10px}}
.gd-acts{{display:flex;flex-wrap:wrap;gap:10px;align-items:center}}
.gd-acts a{{font-family:var(--sans);font-size:14px;font-weight:600}}
.gd-acts .go{{background:var(--gold);color:#151a33;text-decoration:none;padding:11px 18px;border-radius:6px}}
.gd-print{{font-family:var(--sans);font-size:14px;font-weight:600;background:none;color:var(--ink);
  border:1px solid var(--line);border-radius:6px;padding:10px 14px;cursor:pointer}}
.gd-more ul,.gd-list{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}}
.gd-more a,.gd-list a{{display:flex;gap:12px;align-items:center;text-decoration:none;color:var(--ink)}}
.gd-more img,.gd-list img{{width:52px;height:auto;border-radius:3px;box-shadow:var(--shadow);flex:none}}
.gd-more span,.gd-list span{{line-height:1.35}} .gd-list small{{display:block;color:var(--muted);font-family:var(--sans);font-size:13px}}
.gd-more a:hover span,.gd-list a:hover span{{text-decoration:underline;text-decoration-color:var(--gold)}}
@media print{{.site-head,.site-foot,.season-bar,.skip,.gd-book,.gd-more,.gd-print,.kicker{{display:none!important}}
  .gd h2{{border:0;padding-top:0}} body{{background:#fff;color:#000}}}}
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
      <span><a href="/">Carrier Press LLC</a>, Diamondhead, Mississippi.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def _fit(*options, limit):
    for o in options:
        if len(o) <= limit:
            return o
    raise SystemExit("make_guides: nothing fits %d characters: %r" % (limit, options[-1]))


def _crumbs(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": "https://%s%s" % (DOMAIN, u)}
        for i, (n, u) in enumerate(trail)]}


def _write(path, s):
    for bad in ("—", "–", "&mdash;", "&ndash;"):
        if bad in s:
            raise SystemExit("make_guides: a dash reached %s; see the docstring" % path)
    if re.search(r"gutenberg", s, re.I):
        raise SystemExit("make_guides: the public domain source is named in %s" % path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(s, encoding="utf-8")
    nav.patch(path)


def _cover(b, slug):
    card = pathlib.Path("assets/og/books/%s.jpg" % slug)
    return ("https://%s/%s" % (DOMAIN, card.as_posix()) if card.exists()
            else "https://%s/assets/covers/%s.jpg" % (DOMAIN, b["a"]))


def build():
    D = json.loads(pathlib.Path("catalog.json").read_text(encoding="utf-8"))
    recs = {slug: (b, sec) for b, sec, slug in books.records(D)}
    year = datetime.date.today().year
    pages = []
    for slug in slugs():
        if slug not in recs:
            raise SystemExit("make_guides: guides_src/%s.md has no book at /books/%s/" % (slug, slug))
        b, sec = recs[slug]
        pages.append((slug, b, sec, NAME.get(slug) or books.display_title(b, sec),
                      b.get("by") or D["site"]["author"]))

    for slug, b, sec, title, author in pages:
        secs = _sections((SRC / (slug + ".md")).read_text(encoding="utf-8"))
        intro = [body for h, body in secs if h is None]
        qs = [(h, body) for h, body in secs if h and "question" in h.lower()]
        rest = [(h, body) for h, body in secs if h and "question" not in h.lower()]
        if len(qs) != 1:
            raise SystemExit("make_guides: %s needs exactly one questions section" % slug)
        q_html, n = _questions(qs[0][1])
        who = next((_who(h) for h, _ in rest if "timeline" in h.lower() and _who(h)), None)
        short = SHORT.get(slug, title)
        path = "/guides/%s/" % slug
        page_title = _fit("%s Discussion Questions | Carrier Press" % title,
                          "%s Discussion Questions" % title,
                          "%s Discussion Questions | Carrier Press" % short, limit=65)
        tl = " and a %s timeline" % who if who else " and a timeline"
        desc = _fit("%d discussion questions for %s by %s, for book clubs, classrooms and solo readers,"
                    "%s. Free to read and print." % (n, title, author, tl),
                    "%d discussion questions for %s by %s, for book clubs and classrooms,%s." % (n, title, author, tl),
                    "%d discussion questions for %s by %s, for book clubs and classrooms." % (n, short, author),
                    limit=160)
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "name": "%s: discussion questions" % title, "url": "https://%s%s" % (DOMAIN, path),
             "description": desc, "publisher": {"@type": "Organization", "name": "Carrier Press LLC"},
             "about": {"@type": "Book", "name": title, "author": {"@type": "Person", "name": author},
                       "url": "https://%s/books/%s/" % (DOMAIN, slug)}},
            _crumbs([("Home", "/"), ("Reader's guides", "/guides/"), (title, path)])]}
        bk = [
            '<section class="wrap gd" style="padding-top:44px;padding-bottom:64px">',
            '<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Reader\'s guide</span></p>',
            "<h1>%s: discussion questions</h1>" % e(title),
            '<p class="lede">%d questions for book clubs, classrooms and solo readers, with %s, from the '
            'Reader\'s Guide in the Carrier Press annotated edition of <em>%s</em> by %s.</p>'
            % (n, ("a %s timeline" % e(who)) if who else "a timeline", e(title), e(author)),
            '<div class="gd-book"><img src="/assets/covers/%s.jpg" alt="" width="96" height="144" loading="lazy">'
            '<div><p>This guide is printed at the back of the Carrier Press annotated edition.</p><div class="gd-acts">%s<a href="/books/%s/">About this edition</a>'
            '<button class="gd-print" type="button" onclick="window.print()">Print the questions</button>'
            "</div></div></div>" % (b["a"], books._buy_link(b["a"], title), slug),
        ]
        bk += ["<p>%s</p>" % _md._inline(p.strip()) for i in intro for p in re.split(r"\n\s*\n", i) if p.strip()]
        bk += ['<h2 id="questions">%s</h2>' % _md._inline(qs[0][0]), q_html]
        for h, body in rest:
            bk.append("<h2>%s</h2>" % _md._inline(h))
            bk.append(_timeline(body) if "timeline" in h.lower() else _md.render(body))
        others = [p for p in pages if p[0] != slug]
        bk += ['<nav class="gd-more" aria-labelledby="h-more"><h2 id="h-more">More reader\'s guides</h2><ul>']
        bk += ['<li><a href="/guides/%s/"><img src="/assets/covers/%s.jpg" alt="" width="52" height="78" '
               'loading="lazy"><span>%s</span></a></li>' % (s, ob["a"], e(t)) for s, ob, _, t, _ in others]
        bk += ['</ul><p><a href="/guides/">All reader\'s guides</a></p></nav>', "</section>"]
        s = (HEAD.format(title=e(page_title), desc=e(desc), domain=DOMAIN, path=path,
                         og_title=e("%s: discussion questions" % title), og_img=_cover(b, slug),
                         ld=json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))
             + "\n".join(bk) + FOOT.format(year=year))
        _write(OUT / slug / "index.html", s)

    desc = ("Free discussion questions and reader's guides for %d classic novels, including The Blue Castle, "
            "The Monk and The Murder of Roger Ackroyd. For book clubs and classrooms." % len(pages))
    desc = _fit(desc, "Free discussion questions and reader's guides for %d classic novels, for book clubs and "
                "classrooms." % len(pages), limit=160)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Reader's guides", "url": "https://%s/guides/" % DOMAIN,
         "description": desc, "hasPart": [{"@type": "WebPage", "name": "%s: discussion questions" % t,
                                            "url": "https://%s/guides/%s/" % (DOMAIN, s)} for s, _, _, t, _ in pages]},
        _crumbs([("Home", "/"), ("Reader's guides", "/guides/")])]}
    bk = ['<section class="wrap gd" style="padding-top:44px;padding-bottom:64px">',
          '<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Reader\'s guides</span></p>',
          "<h1>Discussion questions for classic novels</h1>",
          '<p class="lede">Every annotated classic from Carrier Press ends with a Reader\'s Guide: questions for '
          'book clubs, classrooms and solo readers, and a short timeline of the author\'s life. Here they are '
          'to read and print for free.</p>', '<ul class="gd-list">']
    bk += ['<li><a href="/guides/%s/"><img src="/assets/covers/%s.jpg" alt="" width="52" height="78">'
           '<span>%s<small>%s</small></span></a></li>' % (s, b["a"], e(t), e(a)) for s, b, _, t, a in pages]
    bk += ["</ul>", "</section>"]
    s = (HEAD.format(title="Book Club Discussion Questions for Classic Novels | Carrier Press", desc=e(desc),
                     domain=DOMAIN, path="/guides/", og_title="Discussion questions for classic novels",
                     og_img="https://%s/assets/og-image.png" % DOMAIN,
                     ld=json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))
         + "\n".join(bk) + FOOT.format(year=year))
    _write(OUT / "index.html", s)
    print("guides: %d reader's guide page(s) -> guides/<slug>/, plus guides/index.html" % len(pages))
    return [p[0] for p in pages]


if __name__ == "__main__":
    build()
