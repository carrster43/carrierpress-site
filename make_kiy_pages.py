#!/usr/bin/env python3
"""
/weird-fiction/the-king-in-yellow/ and three answer pages under it (2026-11-27):

  /weird-fiction/the-king-in-yellow/                 what the book is, and why it lasts
  /weird-fiction/the-king-in-yellow/reading-order/   the ten stories, in order, no spoilers
  /weird-fiction/the-king-in-yellow/the-yellow-sign/ the Sign, and the Yellow Mythos A to Z
  /weird-fiction/the-king-in-yellow/carcosa/         Bierce to Chambers to Lovecraft to True Detective

    python3 make_kiy_pages.py      # build.py runs it too, before the sitemap

WHY. The King in Yellow is about half of all Carrier Press sales, and people
search the questions these pages answer: the reading order, what the Yellow
Sign is, where Carcosa and Hastur come from, the True Detective connection.

SOURCES. Every fact here is in one of the two editions' own apparatus:
PRODUCTION/02_King_in_Yellow/2_EDITION/INTRODUCTION.md and
ANNOTATIONS_AND_GLOSSARY.md, and PRODUCTION/05_Carcosa_Omnibus/2_EDITION/
INTRODUCTION.md. Quotations from the 1895 text were checked against
King_in_Yellow_CLEAN.txt on 2026-11-27. Where the two editions disagree, the
Carcosa introduction (the later, closer study) wins: "Haita the Shepherd" is
1891, not 1886. No sales claims, no rankings.

Rules kept here: no em or en dashes; never name the public domain source.
"""
import datetime, html, json, pathlib, re

import books
import nav

DOMAIN = "carrierpress.com"
BASE = "/weird-fiction/the-king-in-yellow/"
KIY, CARCOSA = "B0H7W7VY7S", "B0HGG934BB"


def e(x):
    return html.escape(str(x), quote=True)


# A paragraph may carry *italics* and [links](/path/); nothing else.
def md(t):
    t = e(t)
    t = re.sub(r"\[([^\]]+)\]\((/[^)\s]*)\)", r'<a href="\2">\1</a>', t)
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)


SONG = ("Along the shore the cloud waves break,\nThe twin suns sink behind the lake,\n"
        "The shadows lengthen\nIn Carcosa.")

PAGES = [
    dict(
        path=BASE,
        title="The King in Yellow Explained: The Play, the Stories, the Sign",
        h1="The King in Yellow, explained",
        desc="What The King in Yellow is: Robert W. Chambers's 1895 book, the play inside it that ruins "
             "its readers, the Yellow Sign, Carcosa, and why it still frightens.",
        short="*The King in Yellow* is a book of ten stories by Robert W. Chambers, published in 1895. "
              "The first four turn around a play, also called *The King in Yellow*, whose second act "
              "drives its readers mad. Chambers never lets you read it.",
        body=[
            ("A book about a play you never get to read", [
                "Inside the stories, *The King in Yellow* is a play in two acts. The first act is "
                "harmless, even lovely. Anyone who reads on into the second act is ruined: driven mad, "
                "damned, or changed past recovery. The play is banned and burned across Europe, and it "
                "keeps turning up anyway, and every character who finds a copy reads it.",
                "Chambers quotes only a handful of lines: Cassilda's song, a few stage directions, and "
                "one exchange at a masked ball, where Camilla asks a stranger to unmask. He answers that "
                "he wears no mask, and she whispers in terror, “No mask? No mask!” The rest is a "
                "hole in the middle of the book, and the reader fills it.",
                "That restraint is the whole trick. Because you never read the play, it can never "
                "disappoint you. Every reader writes their own second act.",
            ]),
            ("Who wrote it", [
                "Robert W. Chambers (1865 to 1933) trained as a painter, at the Art Students League in "
                "New York and then at the Académie Julian in Paris, and showed at the Paris Salon "
                "before he published a word. The Latin Quarter of the late 1880s is all through the book: "
                "half its stories follow American art students in Paris.",
                "*The King in Yellow* was his second book, and it holds nearly all the weird fiction he "
                "ever wrote. He went on to become one of the best paid popular novelists in America, "
                "writing romances that are now forgotten. H. P. Lovecraft ranked the best of these "
                "stories among the finest horror in the language, and mourned that Chambers abandoned "
                "the vein.",
            ]),
            ("Where it went next", [
                "Lovecraft took up the names: Hastur, the Lake of Hali and the Yellow Sign surface in "
                "“The Whisperer in Darkness,” and his circle wove them into what became the "
                "Cthulhu Mythos. Raymond Chandler borrowed the title for a story of his own. Role-playing "
                "games, comics and bands kept the Sign in circulation, and in 2014 the first season of "
                "*True Detective* sent a new generation looking for Carcosa and the Yellow King.",
                "The pages below answer the questions those readers ask most.",
            ]),
        ],
    ),
    dict(
        path=BASE + "reading-order/",
        title="The King in Yellow Reading Order: All 10 Stories, in Order",
        h1="The King in Yellow reading order",
        desc="The ten stories of The King in Yellow in the order Chambers set them, what each one is, "
             "where the book changes key, and what to read next. No spoilers.",
        short="Read all ten stories in the order Chambers set them, starting with “The Repairer of "
              "Reputations.” If you only want the weird tales, they are the first four. If you read "
              "only one, make it “The Yellow Sign.”",
        stories=[
            ("The Repairer of Reputations",
             "New York in 1920, which was the future when Chambers wrote it: government suicide chambers "
             "in the parks, and a narrator just out of an asylum who is sure he is heir to the Imperial "
             "Dynasty of America. Trust nothing he tells you."),
            ("The Mask",
             "Paris. A sculptor has found a solution that turns living things into flawless marble. "
             "Around it, three friends and a tender love triangle, and the play's most famous line."),
            ("In the Court of the Dragon",
             "The shortest of the weird tales. A man who has spent the night reading the play sits in a "
             "Paris church and notices the organist looking at him with hatred. Read it in one sitting."),
            ("The Yellow Sign",
             "An artist, his model, a church watchman with a face like a grave worm, a recurring dream of "
             "a hearse, and a small black clasp. The closest Chambers lets you come to the King."),
            ("The Demoiselle d'Ys",
             "A sudden change of air: an American lost on the moors of Brittany is rescued by a young "
             "woman whose French is three centuries old. The gentlest story in the book."),
            ("The Prophets' Paradise",
             "Eight short prose poems, the hinge of the book, where the fever of the weird tales starts "
             "to dissolve into the Paris stories."),
            ("The Street of the Four Winds",
             "A poor artist in a Latin Quarter garret follows a battered cat home. The last time the "
             "King's shadow falls across the book; watch for it."),
            ("The Street of the First Shell",
             "The longest story, and straight historical fiction: art students starving through the "
             "Prussian siege of Paris in the winter of 1870 to 1871."),
            ("The Street of Our Lady of the Fields",
             "The most autobiographical story: American art students in Paris and a love affair "
             "Victorian reviewers found too frank. Read it beside the next one."),
            ("Rue Barrée",
             "The book closes on unrequited love, and on the discovery that some doors stay shut."),
        ],
        body=[
            ("Two books under one cover", [
                "First time readers deserve fair warning: the book changes key halfway. The first four "
                "stories circle the play at closer and closer range. Then comes a gentle Breton ghost "
                "story, then the prose poems, and then four stories of art students in Paris with "
                "almost no King at all.",
                "Read them anyway, and in order. The Paris stories share the book's real subject, young "
                "people at a threshold they cannot step back across, and the last glimpse of yellow sits "
                "exactly where the two halves meet.",
            ]),
            ("What to read after it", [
                "Next, [Carcosa](/books/carcosa/), which prints the two Ambrose Bierce stories Chambers "
                "took his names from, then the four Chambers stories that used them, in the order they "
                "were published, so you can watch the mythology being put together. Then "
                "[The Mystery of Choice](/books/the-mystery-of-choice/), Chambers back in weird country "
                "two years later. The [weird fiction shelf](/weird-fiction/) carries the reading order "
                "on from there.",
            ]),
        ],
    ),
    dict(
        path=BASE + "the-yellow-sign/",
        title="What Is the Yellow Sign? The King in Yellow's Symbol Explained",
        h1="What is the Yellow Sign?",
        desc="The Yellow Sign in Chambers's The King in Yellow: what the book says, why the famous "
             "spiral is a later invention, and the Yellow Mythos A to Z.",
        short="In *The King in Yellow* (1895), the Yellow Sign is a symbol tied to the forbidden play. "
              "In the story “The Yellow Sign” it is inlaid in gold on a clasp of black onyx. "
              "Chambers never describes its shape. To have it, or perhaps only to have seen it, is to "
              "be found.",
        body=[
            ("What the book actually says", [
                "The narrator of “The Yellow Sign” opens a small box: “On the pink cotton "
                "inside lay a clasp of black onyx, on which was inlaid a curious symbol or letter in "
                "gold. It was neither Arabic nor Chinese, nor, as I found afterwards, did it belong to "
                "any human script.” That is nearly all Chambers gives you. He names the Sign and "
                "never draws it.",
                "The story itself is the strongest in the book: an artist, his model, a watchman in the "
                "churchyard opposite, and a dream of a hearse that both of them keep having. Lovecraft "
                "counted it among the greatest weird tales ever written.",
            ]),
            ("The spiral is not Chambers's", [
                "The three armed spiral most people now call the Yellow Sign was designed by Kevin Ross "
                "for a 1989 role-playing game. It is a fine design, and it is not in the book. Neither "
                "is Hastur as a tentacled Great Old One (that came from August Derleth), Yhtill as a "
                "city (James Blish), or Carcosa as a ruin in Louisiana (*True Detective*). Each one "
                "shows how far the book has travelled. None of them is in it.",
            ]),
        ],
        glossary=[
            ("Aldebaran", "The red star in Taurus that follows the Hyades. Cassilda's song sets the "
             "play beneath it."),
            ("Camilla", "A character in the play, who asks the Stranger to unmask and gets the book's "
             "most quoted answer."),
            ("Carcosa", "The lost city on the Lake of Hali, under twin suns and black stars, where the "
             "King reigns. Chambers took the name from Ambrose Bierce, for whom it was a ruin. See "
             "[where the names come from](%scarcosa/)." % BASE),
            ("Cassilda", "A character in the play and the singer of Cassilda's song, the largest piece "
             "of the play the book lets you read. It opens the book."),
            ("Hali", "The lake of cloud waves beside Carcosa. In Bierce, Hali was a sage quoted in an "
             "epigraph; Chambers made the sage into a lake."),
            ("Hastur", "In Bierce, a kindly god of shepherds. In Chambers, a word that will not hold "
             "still: a place, a person or a power in one story, a falconer's name in another."),
            ("The Hyades", "A star cluster in Taurus, the rainy stars of Greek poetry. In the play, their "
             "songs die unheard in Carcosa."),
            ("The King in Yellow (the play)", "A drama in two acts, banned and burned. The first act is "
             "harmless bait; no one who starts the second can stop. Chambers quotes perhaps a dozen "
             "lines of it."),
            ("The King in Yellow (the figure)", "The tattered King himself, whose scalloped robes must "
             "never be lifted. No one in the book who sees him clearly survives to describe him."),
            ("The Pallid Mask", "From the play: the mask that is no mask."),
            ("The Phantom of Truth", "A figure from the play, named in “The Repairer of "
             "Reputations” and in the shared dream of “The Yellow Sign.”"),
            ("The Stranger", "The unmasked visitor at the play's masquerade."),
            ("Yhtill", "Named once, in “The Repairer of Reputations,” as the thing the King's "
             "tatters must hide forever. Chambers never explains it."),
        ],
    ),
    dict(
        path=BASE + "carcosa/",
        title="Carcosa and Hastur: From Bierce to True Detective",
        h1="Carcosa, Hastur and Hali: where the names come from",
        desc="Carcosa, Hali and Hastur began with Ambrose Bierce, not Chambers. How the names passed to "
             "The King in Yellow, then Lovecraft and Derleth, then True Detective.",
        short="Chambers did not invent Carcosa. He took the name from Ambrose Bierce's 1886 story "
              "“An Inhabitant of Carcosa,” where it is a ruin. He took Hali from the same story, "
              "where Hali is a sage, and Hastur from Bierce's “Haïta the Shepherd” (1891), "
              "where Hastur is a kindly god of shepherds.",
        body=[
            ("Bierce, 1886: Carcosa is a ruin", [
                "“An Inhabitant of Carcosa” is a very short story about a man walking through a "
                "desolate country, trying to find his way back to the city of Carcosa, and slowly "
                "understanding what has happened to him. In Bierce, Carcosa is an ancient city fallen so "
                "long ago that the forest has eaten it. Nothing lives there. The story's epigraph is "
                "credited to Hali, a sage: a voice, not a place.",
            ]),
            ("Bierce, 1891: Hastur is kind", [
                "“Haïta the Shepherd” is a fable about a young shepherd visited by Happiness, "
                "who loses her each time he tries to hold her or ask her to explain herself. Haïta "
                "prays to Hastur, and Bierce's Hastur is a benign god who looks after flocks and simple "
                "men. A reader who expects the Hastur of later horror is usually startled by how gentle "
                "he is.",
            ]),
            ("Chambers, 1895: the names turned inside out", [
                "Chambers took the names and none of their meanings. Carcosa stopped being a ruin and "
                "became a destination, where the King reigns under black stars. Hali stopped being a "
                "sage and became the lake beside it. Hastur appears in a list of dynastic ravings with "
                "no hint whether it is a person, a place or a title. Then Chambers added the thing that "
                "was all his own: the play.",
            ]),
            ("Lovecraft and Derleth: Hastur gets a biography", [
                "Lovecraft read Chambers in 1927 and dropped Hastur into “The Whisperer in "
                "Darkness” as one name in a list, beside Yuggoth and the Lake of Hali. After "
                "Lovecraft's death, August Derleth tidied the Mythos and made Hastur a Great Old One, a "
                "half brother to Cthulhu, with a place in a hierarchy. None of that is in Lovecraft, "
                "still less in Chambers, and it is the opposite of Bierce.",
                "So there are three Hasturs: Bierce's kindly god, Chambers's word that will not hold "
                "still, and Derleth's monster. Most readers meet the last one first.",
            ]),
            ("True Detective and The King in Yellow", [
                "In 2014 the first season of *True Detective*, written by Nic Pizzolatto, put Carcosa and "
                "the Yellow King into the Louisiana bayou and never explained the reference. It did to "
                "Chambers what Chambers did to Bierce: took the shine, left the old meaning behind, and "
                "built something new in the gap. Viewers went looking, and found their way back to a "
                "book from 1895.",
                "Carcosa as a place in Louisiana is the show's own. In Chambers it is a city on a lake "
                "under twin suns, which is stranger.",
            ]),
        ],
    ),
]


CSS = """
.ky h1{font-size:clamp(1.8rem,6vw,2.6rem);font-weight:400;letter-spacing:-.02em;margin:0 0 14px}
.ky h2{font-size:clamp(1.3rem,4vw,1.6rem);font-weight:400;margin:34px 0 10px;padding-top:26px;border-top:1px solid var(--line)}
.ky p,.ky li,.ky dd{line-height:1.7;max-width:68ch}
.ky-short{font-size:1.1rem;line-height:1.65;border-left:3px solid var(--gold);padding:4px 0 4px 16px;max-width:66ch;margin:0 0 22px}
.ky-song{font-style:italic;white-space:pre-line;margin:0 0 18px;padding-left:16px;color:var(--ink-soft)}
.ky-stories{padding-left:1.4em}.ky-stories li{margin:0 0 14px}.ky-stories strong{display:block}
.ky-gl{margin:0}.ky-gl dt{font-weight:600;margin-top:14px}.ky-gl dd{margin:2px 0 0}
.ky-book{display:flex;gap:18px;align-items:flex-start;margin:30px 0 8px;padding:16px;border:1px solid var(--line);border-radius:8px;max-width:660px}
.ky-book img{width:96px;height:auto;border-radius:4px;box-shadow:var(--shadow);flex:none}
.ky-book p{margin:0 0 10px}
.ky-acts{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.ky-acts a{font-family:var(--sans);font-size:14px;font-weight:600}
.ky-acts .go{background:var(--gold);color:#151a33;text-decoration:none;padding:11px 18px;border-radius:6px}
.ky-more{list-style:none;padding:0;margin:0}.ky-more li{margin:6px 0}
"""

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
<meta property="og:title" content="{h1}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://{domain}{path}">
<meta property="og:image" content="https://{domain}/assets/og/books/the-king-in-yellow.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{ld}</script>
<style>{css}</style>
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
<article class="wrap ky" style="padding-top:44px;padding-bottom:64px">
"""

FOOT = """</article>
</main>
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


def _book_box(asin, slug, title, what):
    return ('<div class="ky-book"><img src="/assets/covers/%s.jpg" alt="" width="96" height="144" loading="lazy">'
            '<div><p>%s</p><div class="ky-acts">%s<a href="/books/%s/">About this edition</a></div></div></div>'
            % (asin, what, books._buy_link(asin, title), slug))


KIY_BOX = ("The Carrier Press edition of <em>The King in Yellow</em> has the complete book, an introduction "
           "with an honest map of how to read it, headnotes for the stories, a glossary of the Yellow Mythos "
           "and 11 new illustrations.")
CARCOSA_BOX = ("<em>Carcosa</em> gathers the two Bierce stories and the Chambers pieces that took their names, "
               "in publication order, with a dated headnote for each and Lovecraft's essay on Bierce and "
               "Chambers.")


def build():
    D = json.loads(pathlib.Path("catalog.json").read_text(encoding="utf-8"))
    recs = {b["a"]: (b, sec, slug) for b, sec, slug in books.records(D)}
    for a in (KIY, CARCOSA):
        if a not in recs:
            raise SystemExit("make_kiy_pages: %s is not in the catalogue" % a)
    year = datetime.date.today().year
    for p in PAGES:
        for k in ("title", "desc"):
            lim = 65 if k == "title" else 160
            if len(p[k]) > lim:
                raise SystemExit("make_kiy_pages: %s over %d characters on %s" % (k, lim, p["path"]))
        b = ['<p class="sec-head" style="margin:0 0 10px"><span class="kicker">'
             '<a href="%s">The King in Yellow</a></span></p>' % BASE if p["path"] != BASE else
             '<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Weird fiction</span></p>',
             "<h1>%s</h1>" % e(p["h1"]), '<p class="ky-short">%s</p>' % md(p["short"])]
        if p["path"] == BASE:
            b.append('<p class="ky-song">%s</p>' % e(SONG))
        if p.get("stories"):
            b.append('<h2 id="stories">The ten stories, in order</h2><ol class="ky-stories">')
            b += ["<li><strong>%s</strong>%s</li>" % (e(t), md(x)) for t, x in p["stories"]]
            b.append("</ol>")
        for h, paras in p.get("body", []):
            hid = ' id="true-detective"' if h.startswith("True Detective") else ""
            b.append("<h2%s>%s</h2>" % (hid, md(h)))
            b += ["<p>%s</p>" % md(x) for x in paras]
        if p.get("glossary"):
            b.append('<h2 id="mythos">The Yellow Mythos, A to Z</h2><dl class="ky-gl">')
            b += ["<dt>%s</dt><dd>%s</dd>" % (e(t), md(x)) for t, x in p["glossary"]]
            b.append("</dl>")
        kb, _, kslug = recs[KIY]
        b.append(_book_box(KIY, kslug, books.display_title(kb, recs[KIY][1]), KIY_BOX))
        if p["path"].endswith(("carcosa/", "reading-order/")):
            cb, csec, cslug = recs[CARCOSA]
            b.append(_book_box(CARCOSA, cslug, books.display_title(cb, csec), CARCOSA_BOX))
        b.append('<h2>More on The King in Yellow</h2><ul class="ky-more">')
        b += ['<li><a href="%s">%s</a></li>' % (o["path"], e(o["h1"])) for o in PAGES if o is not p]
        b += ['<li><a href="/guides/">Reader\'s guides and discussion questions for other classics</a></li>',
              '<li><a href="/weird-fiction/">All classic weird fiction and cosmic horror</a></li>', "</ul>"]
        crumbs = [("Home", "/"), ("Weird fiction", "/weird-fiction/"), ("The King in Yellow", BASE)]
        if p["path"] != BASE:
            crumbs.append((p["h1"], p["path"]))
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "headline": p["h1"], "description": p["desc"],
             "url": "https://%s%s" % (DOMAIN, p["path"]),
             "publisher": {"@type": "Organization", "name": "Carrier Press LLC"},
             "about": {"@type": "Book", "name": "The King in Yellow",
                       "author": {"@type": "Person", "name": "Robert W. Chambers"},
                       "url": "https://%s/books/%s/" % (DOMAIN, kslug)}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": "https://%s%s" % (DOMAIN, u)}
                for i, (n, u) in enumerate(crumbs)]}]}
        s = (HEAD.format(title=e(p["title"]), desc=e(p["desc"]), domain=DOMAIN, path=p["path"], h1=e(p["h1"]),
                         css=CSS, ld=json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))
             + "\n".join(b) + FOOT.format(year=year))
        for bad in ("—", "–", "&mdash;", "&ndash;"):
            if bad in s:
                raise SystemExit("make_kiy_pages: a dash reached %s" % p["path"])
        if re.search(r"gutenberg|best ?sell", s, re.I):
            raise SystemExit("make_kiy_pages: a forbidden word reached %s" % p["path"])
        out = pathlib.Path(p["path"].strip("/")) / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(s, encoding="utf-8")
        nav.patch(out)
    print("king in yellow: %d page(s) -> %s" % (len(PAGES), BASE.strip("/")))


if __name__ == "__main__":
    build()
