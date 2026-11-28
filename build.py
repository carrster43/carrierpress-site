#!/usr/bin/env python3
"""Build index.html for carrierpress.com from catalog.json.

Usage:  python3 build.py
No dependencies. Edit catalog.json to add or change titles, then re-run.
"""
import magnet as _magnet  # the free sample signup form, shared
import commerce
import apps_data
import app_search
import json, html, pathlib, datetime, hashlib
import nav, play_data
import home_data as H
import books as _books
import merch as _merch
import weird_data as W

D = json.load(open("catalog.json"))
S = D["site"]
AMZ = commerce.AMZ_URL   # tag lives in commerce.AMZ_TAG; empty until approved
# Amazon's own one-tap review composer. Wording stays neutral: soliciting a specific
# star rating is review manipulation under Amazon's Community Guidelines.
REVIEW = "https://www.amazon.com/review/create-review?asin={}"

def e(x): return html.escape(str(x), quote=True)

# Every title has its own page at /books/<slug>/ (books.py). The cover and the
# title on a card go there, so a reader and a crawler both reach a page that is
# about that one book; the buy button still goes straight to Amazon.
BOOK_URL = _books.url_for(D)

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = ("", "", "twenty", "thirty", "forty", "fifty",
         "sixty", "seventy", "eighty", "ninety")

def spell(n):
    """Spell a catalogue count in words, for prose copy where a sentence must not
    open on a numeral. Covers 0-99, which is the only range a single shelf page
    will ever hold; anything larger falls back to the numeral rather than
    guessing, because a wrong word is worse than a bare digit."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return _TENS[t] + ("-" + _ONES[o] if o else "")
    return str(n)

# ---------------------------------------------------------------- copy blocks
BIO = [
 "Jeffrey L. Carrier writes fiction about the things families leave unsaid: inheritance, "
 "memory, and the quiet cost of a choice that looked simple from the outside.",

 "His novels run from literary suspense (<em>The Sponge Cache</em> and the Greek diaspora "
 "<em>Things Left Open</em> series) to small town cozy mystery (<em>The Marjorie Corey Files</em>) "
 "to the literary <em>Keystone Cycle</em>. Whatever the shelf, the pull is the same: a documented "
 "record, a family secret, and someone who decides to keep reading when it would be easier to stop.",

 "Before he wrote fiction he served in the U.S. Navy and the U.S. Air Force.",

 "He lives on the Mississippi Gulf Coast with his two sons.",
]

def _guard_select():
    """A KDP Select ebook sold here breaks Amazon's exclusivity terms."""
    for asin in set(commerce.EBOOKS) | set(commerce.ACCESS_EBOOKS):
        if asin in commerce.KDP_SELECT:
            raise SystemExit(f"{asin} is in KDP Select and cannot be sold direct")
        if asin in commerce.NEVER_DIRECT:
            raise SystemExit(f"{asin} is public domain in the US only and cannot be sold direct")

def _lbl(asin):
    """The Buy button's words for this title's print edition ("Buy the hardcover")."""
    return _books.buy_label(_books.print_edition(asin)[0])


def book_card(b, kind, anchor=True):
    asin = b["a"]
    page = BOOK_URL[asin]
    bits = []
    # Stable per-title anchor. Lets a post or a social link point at one book on
    # this site, and gives the Book structured data below a real url to claim.
    # Minted on the shelf card ONLY: the Start Here band re-renders five of these
    # same records, and a duplicated id is invalid HTML and an ambiguous deep link.
    bits.append(f'<article class="book" id="b-{asin}">' if anchor
                else '<article class="book">')
    # Audiobook art is square. Rendering it through the 1/1.6 book ratio crops
    # about a third away, and on this cover that is the title and the byline.
    sq = bool(b.get("square"))
    w, hgt = (500, 500) if sq else (313, 500)
    bits.append(f'<a class="cover{" sq" if sq else ""}" href="{page}">'
                f'<img src="assets/covers/{asin}.jpg" loading="lazy" decoding="async" '
                f'width="{w}" height="{hgt}" alt="Cover of {e(b["t"])}"></a>')
    bits.append('<div class="meta">')
    if b.get("omnibus"):
        bits.append('<span class="num">Complete series</span>')
    elif b.get("n"):
        bits.append(f'<span class="num">Book {b["n"]}</span>')
    bits.append(f'<h3><a href="{page}">{e(b["t"])}</a></h3>')
    if b.get("by"):
        bits.append(f'<p class="by">{e(b["by"])}</p>')
    if b.get("hook"):
        bits.append(f'<p class="hook">{e(b["hook"])}</p>')
    if b.get("note"):
        bits.append(f'<p class="fmt">{e(b["note"])}</p>')
    # Verified rating. Requires BOTH a star value and a count: a star average with
    # no count is Amazon page furniture, not an aggregate, and shipping one would
    # be social proof we cannot stand behind. Reporting a real rating is fine;
    # asking for a particular one is review manipulation, so nothing here solicits.
    r = b.get("rating") or {}
    if r.get("stars") and r.get("count"):
        bits.append(f'<p class="rating"><span class="stars" aria-hidden="true">&#9733;</span>'
                    f'{e(r["stars"])} <span class="rcount">on {e(r["count"])} Amazon ratings</span></p>')
    # Reader quote. Words only, never stars: an ARC reviewer's score is not a
    # public rating and must not read as one. Held back until "approved" is true,
    # which means the reviewer said yes to being quoted. The free-copy line is
    # the FTC material-connection disclosure and is not optional.
    q = b.get("quote") or {}
    if q.get("approved") and q.get("text") and q.get("by"):
        bits.append(f'<blockquote class="quote"><p>&ldquo;{e(q["text"])}&rdquo;</p>'
                    f'<footer>{e(q["by"])}, advance reader. '
                    f'The reviewer received a free copy.</footer></blockquote>')
    # CTA label is "Buy on Amazon" (author 2026-11-01, adopting the ChatGPT site
    # review). It replaced "Add to cart" (09-03): the link leaves for Amazon's
    # product page, and a cart label promised an on-site cart that does not exist.
    # No price on the card (author 2026-11-20); the Buy button opens the hardcover.
    if b.get("soon"):
        bits.append('<p class="price">Coming soon</p>')
        bits.append('</div></article>')
        return "".join(bits)
    fmt, buy_asin, _ = _books.print_edition(asin)
    url = AMZ.format(buy_asin)
    label = _books.buy_label(fmt)
    bits.append(f'<p class="actions">'
                f'<a class="buy" href="{url}" target="_blank" rel="noopener" '
                f'aria-label="{e(label)}, {e(b["t"])}, on Amazon">{e(label)}</a>'
                f'<a class="rev" href="{REVIEW.format(asin)}" target="_blank" rel="noopener" '
                f'aria-label="Leave a review of {e(b["t"])} on Amazon">Leave a review</a></p>')
    # Ebook direct and the Cast audiobook, under the hardcover (author 2026-11-20).
    bits.append(_books.other_formats_html(asin, b["t"], BOOK_URL[asin]))
    bits.append('</div></article>')
    return "".join(bits)

# "young" is not here: that anchor now belongs to the Kids' Shelf divider, which
# opens the whole young readers zone rather than just its first series.
ANCHORS = {"things-left-open": "fiction", "classics": "classics"}

# CATEGORY PAGES (author 2026-11-01, adopting the ChatGPT site review #1 and #9):
# the home page shows HOME_LIMIT books per shelf and routes shoppers by category;
# each category gets its own page with every shelf in full and its own title tag.
HOME_LIMIT = 6
CATEGORIES = [
    dict(slug="fiction", label="Fiction", eyebrow="Novels",
         title="Literary Suspense, Cozy Mystery and Historical Novels | Carrier Press",
         h1="Fiction",
         intro="Literary suspense, cozy mystery and historical fiction by Jeffrey L. Carrier. Every series in order, and every standalone novel.",
         card="Literary suspense, cozy mystery and historical fiction.",
         test=lambda s: not s.get("kids") and not s.get("nonfic") and s["id"] != "classics"),
    dict(slug="classics", label="Classics", eyebrow="Restored and annotated",
         title="Restored and Annotated Classics | Carrier Press",
         h1="The Classics Line",
         intro="Public domain works rebuilt as real editions: newly set interiors, original covers, and new apparatus written for each edition.",
         card="Newly set, annotated editions of the classics.",
         test=lambda s: s["id"] == "classics"),
    dict(slug="young-readers", label="Young Readers", eyebrow="Ages 7 to 14",
         title="Children's Books, Adventure Series and Comics | Carrier Press",
         h1="Books for Young Readers",
         intro="Adventure series, money skills and making things, and comics for young readers.",
         card="Adventure series, money skills and comics for kids.",
         test=lambda s: bool(s.get("kids"))),
    # Adult personal finance. These four sat on the young readers shelf as "grown-up
    # companions" under an "Ages 7 to 14" banner (ChatGPT site review 2, #6).
    dict(slug="money", label="Money and Income", eyebrow="Personal finance for adults",
         title="Personal Finance and Income Books | Carrier Press",
         h1="Money and Income",
         intro="Plain guides to dividend investing, side income and automation, written for adult readers. No income guarantees.",
         card="Personal finance guides for adult readers.",
         test=lambda s: bool(s.get("nonfic"))),
]
CAT_OF = {s["id"]: c for c in CATEGORIES for s in D["sections"] if c["test"](s)}
# Titles the home page no longer shows. An old deep link (/#b-<asin>, used in
# journal posts and shared on social) forwards to the book's own page instead.
TRIMMED = {}


def section(sec, limit=None, head=True):
    anchor = ANCHORS.get(sec["id"])
    idattr = f' id="{anchor}"' if anchor else ""
    if not head:
        # A one-shelf category page: its own hero already names the shelf.
        out = [f'<section{idattr} aria-label="{e(sec["name"])}">', f'<div class="wrap" id="h-{sec["id"]}">',
               '<div class="shelf">']
        out += [book_card(b, sec["kind"]) for b in sec["books"]]
        out += ['</div>', '</div>', '</section>']
        return "\n".join(out)
    out = [f'<section{idattr} aria-labelledby="h-{sec["id"]}">', '<div class="wrap">',
           '<div class="sec-head">',
           f'<p class="eyebrow">{e(sec["shelf"])}</p>',
           f'<h2 id="h-{sec["id"]}">{e(sec["name"])}</h2>']
    # A shelf blurb is optional. Emptying one in the catalogue must drop the
    # paragraph, not ship an empty <p></p> that opens a gap under the heading.
    if (sec.get("blurb") or "").strip():
        out.append(f'<p>{e(sec["blurb"])}</p>')
    if sec.get("series_asin"):
        out.append(f'<p class="series-link"><a href="{AMZ.format(sec["series_asin"])}" '
                   f'target="_blank" rel="noopener">The complete series on Amazon</a></p>')
    out += ['</div>',
           '<div class="shelf">']
    shown = sec["books"][:limit] if limit else sec["books"]
    out += [book_card(b, sec["kind"]) for b in shown]
    out.append('</div>')
    if len(shown) < len(sec["books"]):
        for b in sec["books"][len(shown):]:
            TRIMMED[b["a"]] = BOOK_URL[b["a"]]
        cat = CAT_OF[sec["id"]]
        out.append(f'<p class="see-all"><a href="/{cat["slug"]}/">See all {len(sec["books"])} '
                   f'in {e(sec["name"])}</a></p>')
    out += ['</div>', '</section>']
    return "\n".join(out)


def shop_html():
    """Shop by category, straight under the hero: one card per way in."""
    first = {c["slug"]: next(s["books"][0]["a"] for s in D["sections"] if c["test"](s))
             for c in CATEGORIES}
    first["classics"] = "B0H7W7VY7S"   # The King in Yellow, the classics line's best seller
    cards = []
    for c in CATEGORIES:
        n = sum(1 for s in D["sections"] if c["test"](s) for b in s["books"] if not b.get("soon"))
        cards.append(f'<a class="shop-card" href="/{c["slug"]}/">'
                     f'<img src="assets/covers/{first[c["slug"]]}.jpg" width="313" height="500" '
                     f'loading="lazy" decoding="async" alt="">'
                     f'<span><strong>Shop {e(c["label"])}</strong>{e(c["card"])}'
                     f'<small>{n} titles</small></span></a>')
    cards.append(f'<a class="shop-card" href="/{W.SLUG}/">'
                 f'<img src="assets/covers/{W.KIY}.jpg" width="313" height="500" '
                 f'loading="lazy" decoding="async" alt="">'
                 f'<span><strong>Shop Weird Fiction</strong>Cosmic horror and gothic classics, '
                 f'from The King in Yellow.<small>{len(W.NEXT)} titles</small></span></a>')
    # 2026-11-27 (author: "Printful Quick Store"): the merch shop, posters, cards, the 2027 calendar.
    cards.append('<a class="shop-card" href="/shop/">'
                 '<img src="assets/shop-card.jpg" width="313" height="500" '
                 'loading="lazy" decoding="async" alt="">'
                 '<span><strong>Shop Posters and Cards</strong>Book covers for your walls and desk, '
                 'and the 2027 calendar.<small>Printed to order</small></span></a>')
    # 2026-11-08 (author, book fair brand review): no Web Apps card here. This strip
    # is how a book buyer chooses a shelf; the apps sit in the footer's "More from
    # Carrier Press" row (nav.py MORE).
    return ('<section id="shop" class="shop" aria-labelledby="h-shop"><div class="wrap">'
            '<div class="sec-head"><p class="eyebrow">Or browse the shelves</p>'
            '<h2 id="h-shop">Shop by category</h2></div>'
            '<div class="shop-grid">' + "".join(cards) + '</div></div></section>')

def all_books_html():
    """Every book on the home page, under its category (author 2026-11-20: "all
    the books categorized on the home page"). Categories in CATEGORIES order, each
    shelf in full in catalogue order. Cards are minted without the b-<asin> id:
    /#b-<asin> forwards to the book's own page (HOME_FWD), and must keep doing so."""
    out = ['<div id="all-books" class="all-books">']
    for c in CATEGORIES:
        shelves = [sec for sec in D["sections"] if c["test"](sec)]
        n = sum(1 for sec in shelves for b in sec["books"] if not b.get("soon"))
        out += [f'<section id="cat-{c["slug"]}" class="cat-block" aria-labelledby="h-cat-{c["slug"]}">',
                '<div class="wrap"><div class="sec-head">',
                f'<p class="eyebrow">{e(c["eyebrow"])}</p>',
                f'<h2 id="h-cat-{c["slug"]}">{e(c["label"])}</h2>',
                f'<p>{e(c["card"])} {n} titles.</p></div>']
        for sec in shelves:
            if len(shelves) > 1:
                out.append(f'<h3 class="cat-shelf">{e(sec["name"])}</h3>')
            out.append('<div class="shelf">'
                       + "".join(book_card(b, sec["kind"], anchor=False) for b in sec["books"])
                       + '</div>')
        out += ['</div></section>']
    out.append('</div>')
    return "\n".join(out)


def _search_items():
    """Every product the search box offers: each book (catalogue order) and each
    listed app with a page. [{t, s, k, u, i, x}] = title, subline, kind, url,
    image, and extra words searched but not shown (a book's hook, an app's blurb
    and search title), so "taxes" finds Books for One."""
    items = []
    for c in CATEGORIES:
        for sec in D["sections"]:
            if not c["test"](sec):
                continue
            for b in sec["books"]:
                sub = " · ".join(x for x in (b.get("by"), sec["name"] if sec["name"] != c["label"] else "",
                                            "Coming soon" if b.get("soon") else "") if x)
                items.append({"t": _books.display_title(b, sec), "s": sub, "k": c["label"],
                              "u": BOOK_URL[b["a"]], "i": f'/assets/covers/{b["a"]}.jpg',
                              "x": " ".join(x for x in (b.get("hook"), b.get("note"), sec.get("shelf")) if x)})
    for a in apps_data.LISTED:
        slug = a.get("slug")
        if not slug or not pathlib.Path("apps", slug, "index.html").exists():
            continue
        # as_posix(), not str(): on Windows str(Path) is "apps\icons\x.webp" and
        # the search index shipped "/apps\icons\x.webp" for all 31 app rows
        # (found 2026-11-23). The Path is for exists(); the URL is always posix.
        icon = pathlib.Path("apps", "icons", f"{slug}.webp")
        items.append({"t": a["name"], "s": (a.get("blurb") or "").split(". ")[0][:90], "k": "App",
                      "u": f"/apps/{slug}/", "i": f"/{icon.as_posix()}" if icon.exists() else "",
                      "x": " ".join(x for x in ((app_search.SEARCH.get(slug) or ("",))[0],
                                                a.get("blurb")) if x)})
    return items


def search_html():
    """The search bar under the header: type, or just click, and a dropdown lists
    every product (author 2026-11-20). Without scripting the form opens /catalog/."""
    items = _search_items()
    data = json.dumps(items, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    return ('<section class="site-search" aria-label="Search">'
            '<div class="wrap">'
            '<form class="ss-form" action="/catalog/" role="search" autocomplete="off">'
            '<label class="ss-label" for="ss-q">Search every book and app</label>'
            '<div class="ss-box">'
            '<svg class="ss-ico" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">'
            '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/>'
            '<path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
            f'<input id="ss-q" name="q" type="search" placeholder="Search {len(items)} books and apps"'
            ' role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="ss-list"'
            ' spellcheck="false" enterkeyhint="go">'
            '</div>'
            '<ul id="ss-list" class="ss-list" role="listbox" aria-label="Products" hidden></ul>'
            '<p class="ss-status" id="ss-status" role="status" aria-live="polite"></p>'
            '</form></div></section>\n'
            f'<script id="ss-data" type="application/json">{data}</script>\n'
            '<script src="/assets/search.js" defer></script>')


def featured_html():
    """Render the Start Here band. Entries carry only an ASIN plus an editorial
    line; title, author and cover resolve from the catalog so nothing can drift."""
    F = D.get("featured")
    if not F or not F.get("books"):
        return ""
    index = {b["a"]: b for s in D["sections"] for b in s["books"]}
    # {count} in the blurb resolves to the live catalogue size, spelled out. The
    # hero and meta description already derive their count; this was the one place
    # it was typed by hand, and it went stale the moment book 79 landed.
    n = sum(1 for s in D["sections"] for b in s["books"] if not b.get("soon"))
    blurb = F["blurb"].replace("{count}", spell(n)).replace("{COUNT}", spell(n).capitalize())
    out = ['<section id="start" class="featured" aria-labelledby="h-featured">',
           '<div class="wrap">', '<div class="sec-head">',
           f'<p class="eyebrow">{e(F["shelf"])}</p>',
           f'<h2 id="h-featured">{e(F["name"])}</h2>',
           f'<p>{e(blurb)}</p>', '</div>', '<div class="shelf">']
    for f in F["books"]:
        src = index.get(f["a"])
        if src is None:
            raise SystemExit(f'featured ASIN {f["a"]} is not in any section')
        card = dict(src)
        card.pop("n", None)          # "Book 1" is already said in the why line
        card.pop("omnibus", None)
        if f.get("why"):
            card["hook"] = f["why"]
        out.append(book_card(card, "group", anchor=False))
    out += ['</div>', '</div>', '</section>']
    return "\n".join(out)

def bestseller_html():
    """The catalogue's best selling title, and the titles that connect to it.

    THE CLAIM IS MEASURED AND SOURCED. "Our best selling title" is a
    catalogue-relative statement of fact, backed by a live two rail pull on
    2026-09-03 filed at SALES_PUSH/SALES_REPORT_30DAY_2026-09-03.md. Window Aug 4
    to Sep 3 2026: The King in Yellow took 31 of the catalogue's 52 units, 22 on
    IngramSpark and 9 on Amazon, against 7 for the next title. Both rails rank it
    first independently.
    ▶ THE HISTORY MATTERS. This band shipped that morning carrying the same words
      on the strength of an undated project note, and had to be pulled within the
      hour because no report backed it. It is back only because the report now
      exists. Do not restore or reword a ranking claim here from a memory note,
      a summary, or an Amazon-only check: IngramSpark ran 2.4x Amazon in this very
      window, so Amazon alone understates the catalogue badly.
    ▶ If a later pull crowns a different title, change `lead` in catalog.json. If
      no pull is current, set `enabled` false or fall back to the neutral eyebrow
      "Where the mythos starts", which needs no data.
    It is deliberately NOT worded as an Amazon bestseller badge, which would be a
    claim about a list we are not on, and the unit count is never printed, because
    a live number typed as prose goes stale silently and nothing here would say so.
    [[do-not-claim-best-seller-without-data]]

    This band also closes a real gap in the line: Carcosa sells into King in
    Yellow, but King in Yellow pointed at nothing, so the one book with organic
    demand was a dead end. On the printed page that needs an interior re-upload.
    Here it is four cards.

    Entries carry only an ASIN plus an editorial line, exactly like Start Here, so
    title, author and cover resolve from the catalogue and cannot drift out of
    step with the shelves. An ASIN that is in no section fails the build loudly.
    """
    B = D.get("bestseller") or {}
    if not B.get("enabled") or not B.get("lead"):
        return ""
    index = {b["a"]: b for s in D["sections"] for b in s["books"]}
    lead = index.get(B["lead"])
    if lead is None:
        raise SystemExit(f'bestseller lead {B["lead"]} is not in any section')
    connected = B.get("connected") or []
    # {N} resolves to the number of connected titles, spelled and capitalised
    # because it opens a sentence. Deriving it is the whole point: adding a fifth
    # volume to the line must not leave the prose reading "four".
    # NOTE the token differs from the Start Here band's {COUNT}, which is the whole
    # catalogue size. Two bands, two counts, so they do not share a placeholder.
    n = spell(len(connected))
    url = AMZ.format(_books.print_edition(lead["a"])[1])
    out = ['<section id="bestseller" class="bestseller" aria-labelledby="h-bestseller">',
           '<div class="wrap">', '<div class="sec-head">',
           f'<p class="eyebrow">{e(B["shelf"])}</p>',
           f'<h2 id="h-bestseller">{e(B.get("name") or lead["t"])}</h2>', '</div>',
           '<div class="lead">',
           f'<a class="lead-cover" href="{BOOK_URL[lead["a"]]}">'
           f'<img src="assets/covers/{lead["a"]}.jpg" decoding="async" '
           f'width="313" height="500" alt="Cover of {e(lead["t"])}"></a>',
           '<div class="lead-meta">']
    if lead.get("by"):
        out.append(f'<p class="by">{e(lead["by"])}</p>')
    out.append(f'<p class="lead-hook">{e(B["blurb"])}</p>')
    out.append(f'<p class="actions">'
               f'<a class="buy" href="{url}" target="_blank" rel="noopener" '
               f'aria-label="{e(_lbl(lead["a"]))}, {e(lead["t"])}, on Amazon">{e(_lbl(lead["a"]))}</a>'
               f'<a class="rev" href="{REVIEW.format(lead["a"])}" target="_blank" '
               f'rel="noopener" aria-label="Leave a review of {e(lead["t"])} on Amazon">'
               f'Leave a review</a></p>')
    # The book in 3D and on the table, filled by assets/xr/book3d.js.
    out.append(f'<p {_books.b3_attrs("dialog", lead["a"], lead["t"])}></p>')
    out += ['</div>', '</div>']
    if connected:
        blurb = B.get("connected_blurb", "").replace("{n}", n).replace("{N}", n.capitalize())
        out += ['<div class="sec-head sec-sub">',
                f'<h3>{e(B.get("connected_name") or "Connected titles")}</h3>']
        if blurb.strip():
            out.append(f'<p>{e(blurb)}</p>')
        out += ['</div>', '<div class="shelf">']
        for c in connected:
            src = index.get(c["a"])
            if src is None:
                raise SystemExit(f'bestseller connected ASIN {c["a"]} is not in any section')
            card = dict(src)
            card.pop("n", None)
            card.pop("omnibus", None)
            if c.get("why"):
                card["hook"] = c["why"]
            # anchor=False: these five records already minted their id on the
            # Classics shelf, and a duplicated id is invalid HTML.
            out.append(book_card(card, "group", anchor=False))
        out.append('</div>')
        out.append(f'<p class="see-all"><a href="/{W.SLUG}/">See all weird fiction and cosmic '
                   f'horror from Carrier Press</a></p>')
    out += ['</div>', '</section>']
    return "\n".join(out)

def kids_divider_html():
    """The break between the grown-up catalogue and the young readers zone.

    Everything flagged `"kids": true` in catalog.json, plus the comics, renders
    AFTER this band, at the foot of the page. The band carries the #young anchor
    the nav points at, and a scattered strip of cover photos so the change of
    audience reads at a glance, before a single heading is read.

    Book photos carry only an ASIN and resolve from the catalogue like every
    other band, so an ASIN in no section fails the build. A `comic` entry points
    at assets/comics/, and an `img` entry at any other image under assets/.
    """
    K = D.get("kids_divider") or {}
    if not K.get("enabled"):
        return '<div id="young"></div>'
    index = {b["a"]: b for s in D["sections"] for b in s["books"]}
    photos = []
    for p in K.get("photos", []):
        if p.get("a"):
            src = index.get(p["a"])
            if src is None:
                raise SystemExit(f'kids divider ASIN {p["a"]} is not in any section')
            photos.append((BOOK_URL[p["a"]], f'assets/covers/{p["a"]}.jpg',
                           f'Cover of {src["t"]}'))
        elif p.get("comic"):
            photos.append(("#comics", f'assets/comics/{p["comic"]}.jpg', p.get("alt", "")))
        elif p.get("img"):
            photos.append(("#young", p["img"], p.get("alt", "")))
    out = ['<section id="young" class="kids-divider" aria-labelledby="h-young">',
           '<div class="wrap kids-divider-in">', '<div class="sec-head">',
           f'<p class="eyebrow">{e(K["shelf"])}</p>',
           f'<h2 id="h-young">{e(K["name"])}</h2>']
    if (K.get("blurb") or "").strip():
        out.append(f'<p>{e(K["blurb"])}</p>')
    out.append('</div>')
    if photos:
        out.append('<div class="kids-photos">')
        for href, img, alt in photos:
            out.append(f'<a class="kids-photo" href="{e(href)}"><img src="{e(img)}" '
                       f'loading="lazy" decoding="async" alt="{e(alt)}"></a>')
        out.append('</div>')
    out += ['</div>', '</section>']
    return "\n".join(out)

def support_html():
    """Direct-support band. Renders nothing unless `enabled` is true AND at least one
    entry is actually configured, so a half configured block can never ship a dead
    button. An `eth` entry is validated against EIP-55 and a bad address FAILS THE
    BUILD, because a mistyped receive address burns every donation irreversibly."""
    S2 = D.get("support") or {}
    if not S2.get("enabled"):
        return ""
    links, eth = [], None
    for l in S2.get("links", []):
        if l.get("kind") == "eth":
            addr = (l.get("address") or "").strip()
            if not addr:
                continue
            from _eth_checksum import validate as _eth_ok
            ok, msg = _eth_ok(addr)
            if not ok:
                raise SystemExit(f"BUILD STOPPED: ethereum address {addr!r} {msg}")
            eth = (l.get("label") or "Ethereum", addr)
        elif l.get("url", "").strip():
            links.append(l)
    if not links and not eth:
        return ""
    out = ['<section id="support" class="support" aria-labelledby="h-support">',
           '<div class="wrap">', '<div class="sec-head">',
           f'<p class="eyebrow">{e(S2["shelf"])}</p>',
           f'<h2 id="h-support">{e(S2["name"])}</h2>',
           f'<p>{e(S2["blurb"])}</p>', '</div>',
           '<p class="support-links">']
    for l in links:
        out.append(f'<a class="btn btn-ink" href="{e(l["url"])}" target="_blank" '
                   f'rel="noopener">{e(l["label"])}</a>')
    out.append('</p>')
    if eth:
        out.append(f'<p class="eth"><span class="eth-label">{e(eth[0])}</span>'
                   f'<code>{e(eth[1])}</code></p>')
    out += ['</div>', '</section>']
    return "\n".join(out)

def music_html():
    """Featured music band. Not books, and labelled as such.

    Same guard as the support band: an entry with an empty url is skipped, so a
    release that is not linkable cannot ship as a dead tile, and the whole band
    disappears if nothing is configured.

    FEATURED, NOT COMPLETE, and that is deliberate. There are six live releases,
    but the three Bing Bong covers are near identical variants of one robot and
    the Velvet Frequency album shares its cover with the Through the Ages single,
    so listing all six renders as roughly three distinct images and reads as a
    bug rather than a catalogue.
    """
    M = D.get("music") or {}
    if not M.get("enabled"):
        return ""
    items = [i for i in M.get("items", []) if i.get("url", "").strip() and i.get("img")]
    if not items:
        return ""
    out = ['<section id="music" class="music" aria-labelledby="h-music">',
           '<div class="wrap">', '<div class="sec-head">',
           f'<p class="eyebrow">{e(M["shelf"])}</p>',
           f'<h2 id="h-music">{e(M["name"])}</h2>',
           f'<p>{e(M["blurb"])}</p>', '</div>', '<div class="records">']
    for i in items:
        out.append(
            f'<article class="record">'
            f'<a href="{e(i["url"])}" target="_blank" rel="noopener">'
            f'<img src="assets/music/{e(i["img"])}.jpg" loading="lazy" decoding="async" '
            f'width="600" height="600" alt="Cover of {e(i["title"])} by {e(i["act"])}"></a>'
            f'<div class="meta"><span class="num">{e(i["act"])}</span>'
            f'<h3><a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["title"])}</a></h3>'
            + (f'<p class="fmt">{e(i["note"])}</p>' if i.get("note") else '')
            + f'<p class="actions"><a class="buy" href="{e(i["url"])}" target="_blank" '
              f'rel="noopener">Listen</a></p>'
            + (('<p class="plat">' + "".join(
                   f'<a href="{e(u)}" target="_blank" rel="noopener">{e(k)}</a>'
                   for k, u in (i.get("links") or {}).items() if u.strip()) + '</p>')
               if any((u or "").strip() for u in (i.get("links") or {}).values()) else '')
            + '</div></article>')
    out += ['</div>', '</div>', '</section>']
    return "\n".join(out)

def comics_html():
    """Featured comics band. Not books either, and labelled the same way.

    Same guard as the music and support bands: an entry with no usable link is
    skipped and the whole band disappears if nothing is configured, so a store
    that does not exist yet cannot ship as a dead tile.

    TWO SEPARATE RAILS PER ISSUE, and they are not interchangeable. `url` is the
    Gumroad digital edition, which is the live paid channel. `print` is the
    IndyPlanet print on demand listing, which is submitted but not yet public, so
    every `print` is currently empty and simply does not render. Filling one in
    catalog.json is the entire job of publishing it.

    `printnote` is shown ONLY while no issue has a print url. The day the first
    IndyPlanet listing goes live the note retires itself, so the page can never
    promise a print edition it is already selling.
    """
    C = D.get("comics") or {}
    if not C.get("enabled"):
        return ""
    items = [i for i in C.get("items", [])
             if i.get("img") and (i.get("url", "").strip() or i.get("print", "").strip())]
    if not items:
        return ""
    any_print = any(i.get("print", "").strip() for i in items)
    out = ['<section id="comics" class="comics" aria-labelledby="h-comics">',
           '<div class="wrap">', '<div class="sec-head">',
           f'<p class="eyebrow">{e(C["shelf"])}</p>',
           f'<h2 id="h-comics">{e(C["name"])}</h2>',
           f'<p>{e(C["blurb"])}</p>']
    if C.get("printnote") and not any_print:
        out.append(f'<p class="fine">{e(C["printnote"])}</p>')
    out += ['</div>', '<div class="records">']
    for i in items:
        digital, printed = i.get("url", "").strip(), i.get("print", "").strip()
        primary = digital or printed
        out.append(
            f'<article class="record">'
            f'<a href="{e(primary)}" target="_blank" rel="noopener">'
            f'<img src="assets/comics/{e(i["img"])}.jpg" loading="lazy" decoding="async" '
            f'width="600" height="928" alt="Cover of Captain Cubemelon and Friends, '
            f'{e(i["num"])}, {e(i["title"])}"></a>'
            f'<div class="meta"><span class="num">{e(i["num"])}</span>'
            f'<h3><a href="{e(primary)}" target="_blank" rel="noopener">{e(i["title"])}</a></h3>'
            + (f'<p class="fmt">{e(i["note"])}</p>' if i.get("note") else '')
            + '<p class="actions">'
            + (f'<a class="buy" href="{e(digital)}" target="_blank" rel="noopener">'
               'Digital edition</a>' if digital else '')
            + '</p>'
            + (f'<p class="plat"><a href="{e(printed)}" target="_blank" rel="noopener">'
               'Print edition</a></p>' if printed else '')
            + '</div></article>')
    # Captain Cubemelon tees, stickers and comic posters on the Quick Store (merch.py, 2026-11-27).
    out += ['</div>', _merch.comics_strip(), '</div>', '</section>']
    return "\n".join(out)

def excerpt_html():
    """On page reading excerpt.

    The magnet band offers five chapters for an email address. This gives the
    opening away with no gate at all, then asks. Reading first and asking second
    converts better than asking cold, and it costs nothing we were selling.

    The prose is HIS OWN WORK, quoted verbatim. It is never restyled, never
    repunctuated, and never trimmed to satisfy a house rule. Escaped on output
    like everything else, so the manuscript cannot inject markup.
    """
    X = D.get("excerpt") or {}
    if not X.get("enabled") or not X.get("paragraphs"):
        return ""
    body = "".join(f'<p>{e(p)}</p>' for p in X["paragraphs"] if p.strip())
    if not body:
        return ""
    buy = AMZ.format(_books.print_edition(X["asin"])[1]) if X.get("asin") else ""
    out = ['<section id="excerpt" class="excerpt" aria-labelledby="h-excerpt">',
           '<div class="wrap wrap-narrow">', '<div class="sec-head">',
           f'<p class="eyebrow">{e(X["shelf"])}</p>',
           f'<h2 id="h-excerpt">{e(X["name"])}</h2>']
    if X.get("sub"):
        out.append(f'<p>{e(X["sub"])}</p>')
    out += ['</div>', f'<div class="excerpt-body">{body}</div>']
    if X.get("cta"):
        out.append(f'<p class="excerpt-cta">{e(X["cta"])}</p>')
    out.append('<p class="excerpt-actions">'
               f'<a class="btn btn-ink" href="{e(S["magnet_url"])}">'
               'Free sample: The King in Yellow</a>'
               + (f'<a class="excerpt-buy" href="{buy}" target="_blank" rel="noopener" '
                  f'aria-label="{e(_lbl(X["asin"]))}, {e(X["name"])}, on Amazon">{e(_lbl(X["asin"]))}</a>'
                  if buy else '') + '</p>')
    out += ['</div>', '</section>']
    return "\n".join(out)

import blog as _blog_probe
# Footer platform list. Entries with an empty url are skipped, so a store that does
# not exist yet cannot ship as a dead link.
platforms_html = "".join(
    f'<li><a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["label"])}</a></li>'
    for i in (D.get("platforms") or {}).get("items", []) if i.get("url","").strip())

POSTS = _blog_probe._load()
journal_nav = '\n      <a href="/blog/">Journal</a>' if POSTS else ''
def top10_html():
    """Top 10 best sellers plus the complete sellers list, catalogue-relative.

    MEASURED AND SOURCED: `items` in catalog.json is EVERY title that sold in the
    window, ranked, from a two rail pull (KDP royalty report + IngramSpark Print
    Bestsellers) filed at the `source` path. The Top 10 is ranks 1-10 of that one
    list and the complete list is all of it, so the two can never disagree. Ties
    share a rank, so a tie at 10 shows more than ten titles; that is the honest
    reading, and the heading counts them ("Top 12"). The window is PRINTED; unit counts are never printed.
    To refresh: re-pull both rails, file a new report, replace `items`, `window`
    and `source`. With no current pull, set `enabled` false.
    An item may carry `name` to override the shelf title where it is ambiguous
    out of its series context ("The Complete Series").
    [[do-not-claim-best-seller-without-data]]
    """
    T = D.get("top10") or {}
    if not T.get("enabled") or not T.get("items"):
        return ""
    index = {b["a"]: b for s in D["sections"] for b in s["books"]}

    def resolve(it):
        b = index.get(it["a"])
        if b is None:
            raise SystemExit(f'top10 ASIN {it["a"]} is not in any section')
        return b, it.get("name") or b["t"], AMZ.format(_books.print_edition(b["a"])[1])

    top = [i for i in T["items"] if int(i["rank"]) <= 10]
    # 2026-10-20 (author): the heading names how many titles it shows ("Top 12"
    # while three tie at 10), so `name` carries {N} rather than a fixed ten.
    out = ['<section id="top10" class="top10" aria-labelledby="h-top10">',
           '<div class="wrap">', '<div class="sec-head">',
           f'<p class="eyebrow">{e(T["shelf"])}</p>',
           f'<h2 id="h-top10">{e(T["name"].replace("{N}", str(len(top))))}</h2>',
           f'<p>{e(T["blurb"])} Sales from {e(T["window"])}.</p>', '</div>',
           '<ol class="top10-list">']
    for it in top:
        b, name, url = resolve(it)
        out.append(
            f'<li><span class="rank">{int(it["rank"])}</span>'
            f'<a class="t10-cover" href="{BOOK_URL[b["a"]]}">'
            f'<img src="assets/covers/{b["a"]}.jpg" loading="lazy" decoding="async" '
            f'width="313" height="500" alt="Cover of {e(name)}"></a>'
            f'<span class="t10-meta"><a class="t10-title" href="{BOOK_URL[b["a"]]}">'
            f'{e(name)}</a>'
            + (f'<span class="by">{e(b["by"])}</span>' if b.get("by") else '')
            + f'<span {_books.b3_attrs("mini", b["a"], name)}></span>'
            + f'</span><a class="buy" href="{url}" target="_blank" rel="noopener" '
              f'aria-label="{e(_lbl(b["a"]))}, {e(name)}, on Amazon">{e(_lbl(b["a"]))}</a></li>')
    out.append('</ol>')
    # The complete list: every title that sold, collapsed by default so the
    # landing page still opens on the ten. Text only, no covers, so 30+ rows
    # stay light; each row deep-links to the title's card on the shelves.
    allit = T["items"]
    out += ['<details class="sellers-all">',
            f'<summary>{e(T.get("all_name") or "Every title that sold")} '
            f'<span class="n">({len(allit)})</span></summary>',
            '<ol class="sellers-list">']
    for it in allit:
        b, name, url = resolve(it)
        out.append(f'<li><span class="rank">{int(it["rank"])}</span>'
                   f'<a href="{BOOK_URL[b["a"]]}">{e(name)}</a>'
                   + (f' <span class="by">{e(b["by"])}</span>' if b.get("by") else '')
                   + '</li>')
    out += ['</ol>', '</details>', '</div>', '</section>']
    return "\n".join(out)

# Deals five covers on every visit: three of the month's sellers and two
# wildcards from the rest of the grown-up catalogue (author 2026-11-18, "3 + 2").
# Runs inline right after the fan, before first paint, so there is no flash of
# the default hand. Sellers are a weighted draw without replacement, each
# cover's chance the square root of its royalties, so the month's leader turns
# up most but the smaller sellers still get dealt. Wildcards are an even draw.
# Hand order is seller, seller, seller, wild, wild, and the slot map below puts
# ranks 0-2 in the middle, so the sellers hold the front and the wildcards the
# two outer edges. Too few wildcards and the sellers fill the gap.
DEAL_JS = (
    "(function(){var s=document.currentScript,f=s&&s.previousElementSibling;"
    "if(!f||!f.classList.contains('fan'))return;"
    "var all=[].slice.call(f.querySelectorAll('.fan-book'));if(all.length<6)return;"
    "function draw(pool,n,out){while(out.length<n&&pool.length){var t=0,i;pool.forEach(function(p){t+=p.w});"
    "var r=Math.random()*t;for(i=0;i<pool.length-1;i++){r-=pool[i].w;if(r<0)break}"
    "out.push(pool.splice(i,1)[0].a)}return out}"
    "var sell=[],wild=[];all.forEach(function(a){"
    "if(a.getAttribute('data-pool')==='wild')wild.push({a:a,w:1});"
    "else sell.push({a:a,w:Math.sqrt(parseFloat(a.getAttribute('data-w'))||1)})});"
    "var hand=draw(sell,3,[]);draw(wild,5,hand);draw(sell,5,hand);"
    "all.forEach(function(a){a.hidden=true;var m=a.querySelector('img');m.removeAttribute('fetchpriority')});"
    "[3,1,0,2,4].forEach(function(k,pos){var a=hand[k];if(!a)return;a.hidden=false;"
    "a.style.setProperty('--p',pos-2);a.style.setProperty('--d',k);"
    "var m=a.querySelector('img');m.loading='eager';if(k===0)m.setAttribute('fetchpriority','high')});"
    "})();"
)


def hero_html():
    """The first screen: a short headline, two calls to action, and the five best
    selling covers fanned on the right, #1 in front.

    2026-10-26 (author): something eye catching before the Top 12. The fan is
    read from the same `top10.items` as the list on /catalog/, so the two can
    never disagree, and it drops out (copy goes full width) when the list is off.
    2026-11-17 (author brief): the copy comes from home_data.HERO, and the
    season's own hero (home_data.SEASONS) replaces it while a season is on.
    """
    T = D.get("top10") or {}
    picks = T["items"][:5] if T.get("enabled") and T.get("items") else []
    fan_label = "This year's best sellers"
    # 2026-11-18 (author: "review top sellers and update landing page with
    # revolving books every time someone visits", KDP and IS data, November).
    # catalog.json `selling_now` is this month's sellers, each with its weight
    # (royalties in the window). The page carries every one of them and the
    # script after the fan deals five per visit, weighted, so a returning
    # visitor sees a different hand. Without JavaScript the first five show, in
    # sales order. Source and window live beside the list in catalog.json; when
    # the window goes stale, refresh it or set `enabled` false and the fan falls
    # back to the year's Top 10.
    S = D.get("selling_now") or {}
    rotate = bool(S.get("enabled") and S.get("items"))
    if rotate:
        picks = S["items"]
        fan_label = S.get("label") or fan_label
    # A season may fan out its own five books (home_data.SEASONS `fan`), so
    # October shows cosmic horror and February the love stories. Without one the
    # fan stays the best sellers.
    fan = (H.SEASON or {}).get("fan")
    if fan:
        picks = [{"a": a} for a in fan[:5]]
        fan_label = H.SEASON["feature"]["title"]
        rotate = False
    index = {b["a"]: b for s in D["sections"] for b in s["books"]}
    for p in picks:
        if p["a"] not in index or index[p["a"]].get("soon"):
            raise SystemExit(f'hero fan: {p["a"]} is not a buyable catalogue title')
    # Slot order left to right puts rank 1 in the middle, 2 and 3 beside it.
    slots = [3, 1, 0, 2, 4]
    fan = []
    for pos, k in enumerate(slots):
        if k >= len(picks):
            continue
        b = index[picks[k]["a"]]
        pri = ' fetchpriority="high"' if k == 0 else ''
        w = f' data-w="{picks[k].get("w", 1)}"' if rotate else ''
        fan.append(
            f'<a class="fan-book" style="--p:{pos - 2};--d:{k}"{w} href="{BOOK_URL[b["a"]]}">'
            f'<img src="assets/covers/{b["a"]}.jpg" width="313" height="500" '
            f'decoding="async"{pri} '
            f'alt="Cover of {e(b["t"])}"></a>')
    # The rest of the month's sellers wait hidden and lazy, so a visitor's
    # browser only fetches the five covers it is dealt.
    # 2026-11-18 (author: "Yes, 3 + 2 mix"): every buyable grown-up title that
    # is not a seller this month joins as a WILDCARD (data-pool="wild"). Each
    # visit is dealt three sellers and two wildcards, so the whole adult
    # catalogue gets turns in the hero while the month's sellers keep the front.
    # Kids' sections stay out: the hero speaks to the adult buyer.
    wild = []
    if rotate:
        sellers = {p["a"] for p in picks}
        seen = set()
        for s_ in D["sections"]:
            if s_.get("kids"):
                continue
            for b in s_["books"]:
                if b.get("soon") or b["a"] in sellers or b["a"] in seen:
                    continue
                seen.add(b["a"])
                wild.append(b)
        for p in picks[5:]:
            b = index[p["a"]]
            fan.append(
                f'<a class="fan-book" hidden style="--p:0;--d:4" data-w="{p.get("w", 1)}" '
                f'href="{BOOK_URL[b["a"]]}">'
                f'<img src="assets/covers/{b["a"]}.jpg" width="313" height="500" '
                f'loading="lazy" decoding="async" alt="Cover of {e(b["t"])}"></a>')
        for b in wild:
            fan.append(
                f'<a class="fan-book" hidden style="--p:0;--d:4" data-pool="wild" '
                f'href="{BOOK_URL[b["a"]]}">'
                f'<img src="assets/covers/{b["a"]}.jpg" width="313" height="500" '
                f'loading="lazy" decoding="async" alt="Cover of {e(b["t"])}"></a>')
    fan_html = (f'<div class="fan" role="group" aria-label="{e(fan_label)}">'
                + "".join(fan) + '</div>') if fan else ''
    if fan_html and rotate:
        fan_html += "<script>" + DEAL_JS + "</script>"
    cue = ('<a class="marquee-cue" href="#threads">Where to start'
           '<span aria-hidden="true">&#8595;</span></a>') if fan else ''
    C = H.SEASON["hero"] if H.SEASON else H.HERO
    (p_label, p_href), (s_label, s_href) = C["primary"], C["secondary"]
    # h1 carries one <em> by design, so it is the one field not escaped here.
    return f"""<section class="marquee{'' if fan else ' marquee-solo'}" aria-labelledby="h-hero">
  <div class="wrap marquee-in">
    <div class="marquee-copy">
      <p class="marquee-kicker"><img src="assets/logo-mark-light-small.png" alt="" width="34" height="24">{e(C['kicker'])}</p>
      <h1 id="h-hero">{C['h1']}</h1>
      <p>{e(C['sub'])}</p>
      <div class="hero-actions">
        <a class="btn btn-gold" href="{e(p_href)}">{e(p_label)}</a>
        <a class="btn btn-ghost" href="{e(s_href)}">{e(s_label)}</a>
      </div>
    </div>
    {fan_html}
  </div>
  {cue}
</section>"""


def picker_cta_html():
    """The way into /pick/ (make_picker.py, author 2026-11-18): an opt-in card,
    never a pop-up, so a visitor who wants help asks for it. Sits between the
    threads and the category strip."""
    return ('<section class="pick-cta" aria-labelledby="h-pick"><div class="wrap">'
            '<a class="pick-card" href="/pick/"><span class="pick-copy">'
            '<span class="eyebrow">Not sure where to start?</span>'
            '<strong id="h-pick">Find your next book in two questions</strong>'
            '<span class="pick-sub">Tell us who it is for and what they like. We pick one book '
            'to start with and two more if that one is not quite it.</span></span>'
            '<span class="pick-go">Start<span aria-hidden="true"> &#8594;</span></span></a>'
            '</div></section>')


def sprout_band_html():
    """Sprout, the weekly magazine (make_sprout.py, author 2026-11-20), as a card
    low on the home page, after the free sample and before the author. Never at
    the top: the season ribbon owns the top of the page, and two bands stacked
    there read as clutter. The form is make_sprout.form_html(), so the home page
    and /sprout/ cannot drift apart. Without a MailerLite form it links only."""
    import make_sprout as _sp, sprout_data as _sd
    return ('<section class="sprout-band" aria-labelledby="h-sprout"><div class="wrap">'
            '<div class="sprout-card"><div class="sprout-copy">'
            f'<p class="eyebrow">{e(_sd.CADENCE)}, the weekly magazine</p>'
            f'<h2 id="h-sprout">{e(_sd.NAME)}</h2>'
            f'<p>{_sp.pitch()} <a href="/{_sd.PATH}/">Read this week&#8217;s issue</a>.</p>'
            '</div>' + _sp.form_html() + '</div></div></section>')


def threads_html():
    """The home page's hooks: one book, series, app or gift idea per card, each
    with its buy button on the card and a link onward (home_data.THREADS).

    Everything a card prints about a product resolves from the same records the
    shelves and app pages use, so a thread cannot drift: title, cover and the
    paperback buy link from catalog.json and formats.json, the app name, price
    and Gumroad link from apps_data.py and commerce.py. A thread pointing at
    nothing fails the build rather than shipping a dead card.
    """
    import apps_data as _A
    from folds import FOLDED
    index = {b["a"]: b for s_ in D["sections"] for b in s_["books"]}
    apps = {a["slug"]: a for a in _A.APPS if a.get("slug")}
    best = (D.get("bestseller") or {})
    cards = []
    threads = list(H.THREADS)
    if H.SEASON and H.SEASON.get("feature"):
        threads.insert(0, dict(H.SEASON["feature"], kind="feature"))
    for t in threads:
        eyebrow = (t.get("seasonal") or {}).get(H.SEASON_KEY) or t["eyebrow"]
        nlabel, nhref = t["next"]
        if nhref.startswith("book:"):
            nhref = BOOK_URL[nhref[5:]]
        kind = t["kind"]
        if kind == "feature":
            for a in t["covers"]:
                if a not in index:
                    raise SystemExit(f"home thread: feature cover {a} is not in the catalogue")
            art = (f'<a class="thread-art thread-stack" href="{e(nhref)}" tabindex="-1" aria-hidden="true">'
                   + "".join(f'<img src="assets/covers/{a}.jpg" width="313" height="500" '
                             f'loading="lazy" decoding="async" alt="">' for a in t["covers"])
                   + '</a>')
            title, title_href = t["title"], nhref
            actions = (f'<a class="btn btn-gold" href="{e(nhref)}">{e(nlabel)}</a>')
        elif kind == "book":
            b = index.get(t["a"])
            if b is None or b.get("soon"):
                raise SystemExit(f"home thread: {t['a']} is not a buyable catalogue title")
            # The best seller claim is only as current as the sales pull behind
            # it: with the band switched off in catalog.json, the label falls back.
            if eyebrow == "Our best selling title" and not (best.get("enabled") and best.get("lead") == t["a"]):
                eyebrow = "Where cosmic horror starts"
            title, title_href = t.get("title") or b["t"], BOOK_URL[t["a"]]
            art = (f'<a class="thread-art" href="{title_href}" tabindex="-1" aria-hidden="true">'
                   f'<img src="assets/covers/{t["a"]}.jpg" width="313" height="500" '
                   f'loading="lazy" decoding="async" alt=""></a>')
            buy = AMZ.format(_books.print_edition(t["a"])[1])
            actions = (f'<a class="buy" href="{buy}" target="_blank" rel="noopener" '
                       f'aria-label="{e(_lbl(t["a"]))}, {e(b["t"])}, on Amazon">{e(_lbl(t["a"]))}</a>'
                       f'<a class="next" href="{e(nhref)}">{e(nlabel)}</a>')
        elif kind == "app":
            slug = t["slug"]
            a = apps.get(slug)
            w = commerce.for_app(slug)
            if a is None or slug in FOLDED or not w.get("buy"):
                raise SystemExit(f"home thread: app {slug} is not on sale on the web")
            shot = next(iter(sorted((pathlib.Path("apps/shots") / slug).glob("*-sm.webp"))), None)
            if shot is None:
                raise SystemExit(f"home thread: app {slug} has no screenshot in apps/shots/")
            title, title_href = t.get("title") or a["name"], nhref
            art = (f'<a class="thread-art thread-shot" href="{e(nhref)}" tabindex="-1" aria-hidden="true">'
                   f'<img src="{shot.as_posix()}" width="360" height="780" loading="lazy" '
                   f'decoding="async" alt=""></a>')
            # A "from $14.99 a book" price (Cast) is a starting price, not one
            # payment for the app, so it never takes " once".
            price = w["buy_price"] + ("" if w.get("sub") or w["buy_price"].startswith("from ") else " once")
            actions = (f'<a class="buy" href="{e(w["buy"])}" target="_blank" rel="noopener" '
                       f'aria-label="Buy {e(a["name"])}, {e(price)}">Buy {e(a["name"])}, {e(price)}</a>'
                       f'<a class="next" href="{e(nhref)}">{e(nlabel)}</a>')
        else:
            raise SystemExit(f"home thread: unknown kind {kind!r}")
        cards.append(
            f'<article class="thread thread-{kind}">{art}<div class="thread-meta">'
            f'<p class="eyebrow">{e(eyebrow)}</p>'
            f'<h3><a href="{e(title_href)}">{e(title)}</a></h3>'
            f'<p class="thread-line">{e(t["line"])}</p>'
            f'<p class="thread-actions">{actions}</p></div></article>')
    if not cards:
        return ""
    return ('<section id="threads" class="threads" aria-labelledby="h-threads"><div class="wrap">'
            '<div class="sec-head"><p class="eyebrow">Start here</p>'
            '<h2 id="h-threads">Pull a thread</h2>'
            '<p>Each card is one book, series or app, ready to buy right there. Follow the '
            'thread and the next one is waiting.</p></div>'
            '<div class="thread-grid">' + "".join(cards) + '</div>'
            f'<p class="see-all"><a href="/catalog/">Browse all {total} books</a> &middot; '
            '<a href="/apps/">See every app</a></p>'
            '</div></section>')

# Only advertise the feed once something is in it. An empty feed offered to a
# reader is a worse first impression than no feed at all.
feed_link = ('\n<link rel="alternate" type="application/rss+xml" '
             'title="Carrier Press journal" href="/feed.xml">') if POSTS else ''

# PAGE ORDER, by author direction (2026-09-25): the best seller leads the page,
# then the Start Here picks, then the full grown-up catalogue, and the young
# readers zone last of all, behind its own divider. The hero and the free
# sample open the catalogue rather than the page.
# 2026-10-20 (author): the Top 10 + complete sellers list now LEAD the page.
# 2026-11-01 (author, ChatGPT review #1): Shop by category now sits ABOVE the
# Top 10, so a shopper is routed first and shown the sellers second.
# 2026-11-06 (author, ChatGPT review 3): Start Here now sits above the Top 10, so
# a first visitor gets a short list of ways in before the sales ranking.
# 2026-11-17 (author brief, holiday rework): the home page no longer carries the
# catalogue. It opens on the hero and the threads (home_data.py), then the
# category strip, the free sample and About. Everything below moved, in its old
# order, to /catalog/ (write_catalog), and old deep links are forwarded there.
# The stylesheet's content hash on the home page link: Pages lets a browser keep
# styles.css for four hours, so a returning visitor would otherwise see new
# markup (the search box, 2026-11-20) with the old styles until it expired.
CSS_V = hashlib.sha256(pathlib.Path("styles.css").read_bytes()).hexdigest()[:10]
top_html = featured_html() + "\n" + top10_html() + "\n" + bestseller_html()
# 2026-11-08 (author, book fair brand review): music and the support band no
# longer sit between the grown-up shelves and the kids' shelves. They follow the
# kids' zone, last before About, so the page reads as books from top to bottom.
sections_html = (excerpt_html() + "\n"
                 + "\n".join(section(s, HOME_LIMIT) for s in D["sections"] if not s.get("kids")))
after_books_html = music_html() + "\n" + support_html()
kids_html = ('<div class="kids-zone">\n' + kids_divider_html() + "\n"
             + "\n".join(section(s, HOME_LIMIT) for s in D["sections"] if s.get("kids"))
             + "\n" + comics_html() + "\n</div>")
total = sum(1 for s in D["sections"] for b in s["books"] if not b.get("soon"))
# Old deep links into the home page. /#b-<asin> (journal posts, social) goes to
# the book's own page; a moved band (/#top10, /#young, ...) goes to /catalog/.
HOME_FWD = dict(sorted(BOOK_URL.items()))
MOVED = ["start", "top10", "bestseller", "excerpt", "fiction", "classics",
         "young", "comics", "music", "support"]

# The sameAs links tell Google which "Jeffrey L. Carrier" this is. At least two namesakes
# publish on Amazon, and Goodreads holds three records under the name: 71232009 is his.
# WebSite is what Google reads for the site name it prints above a search result.
ld = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": f"https://{S['domain']}/#organization",
      "name": "Carrier Press",
      "legalName": "Carrier Press LLC",
      "address": {"@type": "PostalAddress", "addressLocality": "Diamondhead", "addressRegion": "MS", "addressCountry": "US"},
      "url": f"https://{S['domain']}/",
      "logo": f"https://{S['domain']}/assets/logo-mark.png",
      "description": S["tagline"],
      "sameAs": ["https://www.tiktok.com/@carrierpress"],
      "founder": {"@type": "Person", "name": S["author"], "url": f"https://{S['domain']}/",
                  "sameAs": [S["amazon_author"], S["bookbub_profile"],
                             "https://www.goodreads.com/author/show/71232009.Jeffrey_L_Carrier"]},
    },
    {
      "@type": "WebSite",
      "@id": f"https://{S['domain']}/#website",
      "name": "Carrier Press",
      "url": f"https://{S['domain']}/",
      "publisher": {"@id": f"https://{S['domain']}/#organization"},
    },
  ],
}

# ------------------------------------------------------------ book structured data
# One ItemList naming every title, so a crawler reading this page sees 78 discrete
# books rather than one long blob of text.
#
# Deliberately NOT claimed, each for a reason:
#   aggregateRating / reviewCount - there are 2 reviews across the whole catalogue.
#     Marking up a rating we do not have is a false claim and a manual-action risk.
#   offers / price - prices are not in catalog.json and they move. Stale price
#     markup is worse than none.
#   isbn - the catalogue keys on ASIN, which is not an ISBN and must not be passed
#     off as one.
#
# `by` carries the original author on the 26 classics. Falling back to the site
# author for those would credit Jeffrey with Machen and Blackwood, so it is honoured
# first and only absent titles fall through to him.
def book_ld(b, pos):
    d = {
      "@type": "Audiobook" if b.get("narrator") else "Book",
      "position": pos,
      "name": b["t"],
      "author": {"@type": "Person", "name": b.get("by") or S["author"]},
      "publisher": {"@type": "Organization", "name": "Carrier Press"},
      "inLanguage": "en",
      "url": f"https://{S['domain']}{BOOK_URL[b['a']]}",
      "image": f"https://{S['domain']}/assets/covers/{b['a']}.jpg",
    }
    if not b.get("soon"):
        d["sameAs"] = AMZ.format(b["a"])
    if b.get("hook"):
        d["description"] = b["hook"]
    if b.get("narrator"):
        d["readBy"] = {"@type": "Person", "name": b["narrator"]}
    return d

books_ld = {
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "The Carrier Press catalogue",
  "numberOfItems": sum(len(sec["books"]) for sec in D["sections"]),
  "itemListElement": [book_ld(b, i) for i, b in enumerate(
      (b for sec in D["sections"] for b in sec["books"]), start=1)],
}

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carrier Press | Books by Jeffrey L. Carrier</title>
<meta name="description" content="Carrier Press publishes the fiction of Jeffrey L. Carrier, books for young readers, and a line of restored classics. {total} titles, available now.">
<link rel="canonical" href="https://{S['domain']}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="Carrier Press | Books by Jeffrey L. Carrier">
<meta property="og:description" content="Literary suspense, cozy mystery, books for young readers, and restored classics.">
<meta property="og:url" content="https://{S['domain']}/">
<meta property="og:image" content="https://{S['domain']}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="stylesheet" href="styles.css?v={CSS_V}">{feed_link}
<script type="application/ld+json">{json.dumps(ld)}</script>
<script type="application/ld+json">{json.dumps(books_ld)}</script>
{_books.BOOK3D}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="/">
      <img class="mark-dark" src="assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>Carrier Press</span>
    </a>
    <nav class="nav" aria-label="Main">
      <a href="/fiction/">Fiction</a>
      <a href="/young-readers/">Young Readers</a>
      <a href="/classics/">Classics</a>{journal_nav}
      <a href="#about">About</a>
      <a href="/labs/">Labs</a>
      <a class="nav-cta" href="#free">Free Sample</a>
    </nav>
  </div>
</header>

<main id="main">

{search_html()}

{hero_html()}

{threads_html()}

{picker_cta_html()}

{shop_html()}

{all_books_html()}

<!-- ============================ READER MAGNET ============================
     The button below points at /free/ (write_free, MAGNET_FORM), our own
     signup page, which adds signups to the group "TLO Readers". The welcome
     automation fires on group join and sends The King in Yellow sample.
     ====================================================================== -->
<section id="free" class="magnet" aria-labelledby="h-free">
  <div class="wrap magnet-in">
    <div>
      <p class="eyebrow">Free sample</p>
      <h2 id="h-free">Read the opening of <em>The King in Yellow</em></h2>
      <p>Chambers never lets you read the cursed play at the centre of this book. You only meet
         the people it has already ruined. Get the opening of the restored, annotated Carrier Press
         edition free, sent straight to your inbox as EPUB and PDF.</p>
      <p>Then a short welcome note from me, and word when the next book is out.</p>
      <p style="margin-top:22px">
        <a class="btn btn-ink" href="{e(S['magnet_url'])}">Send me the free sample</a>
      </p>
      <p class="fine">No spam. One click unsubscribe any time. The sample is yours to keep.</p>
    </div>
    <div class="magnet-cover"><img src="assets/covers/B0H7W7VY7S.jpg" width="313" height="500" alt="Cover of The King in Yellow"></div>
  </div>
</section>

{sprout_band_html()}

<section id="about" aria-labelledby="h-about">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">The author</p><h2 id="h-about">{e(S['author'])}</h2></div>
    <div class="about-in">
      <img src="assets/portrait.jpg" width="210" height="207" alt="{e(S['author'])}" loading="lazy">
      <div>{"".join(f"<p>{p}</p>" for p in BIO)}
        <p style="margin-top:22px">
          <a class="btn btn-ink" href="{e(S['bookbub_profile'])}" target="_blank" rel="noopener">Follow on BookBub</a>
        </p>
      </div>
    </div>
  </div>
</section>

</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="brandline">
          <img src="assets/logo-mark-light.png" alt="" width="40" height="28">
          <strong>Carrier Press</strong>
        </div>
        <p class="note">Carrier Press LLC is an independent publisher in Diamondhead, Mississippi.
           Literary suspense, cozy mystery, books for young readers, and restored classics.</p>
      </div>
      <div>
        <h4>Read</h4>
        <ul>
          <li><a href="#free">Free sample</a></li>
          <li><a href="/catalog/">Every book</a></li>
          <li><a href="/gifts/">Gift guide</a></li>
          <li><a href="{e(S['amazon_author'])}" target="_blank" rel="noopener">All books on Amazon</a></li>
          <li><a href="{e(S['bookbub_profile'])}" target="_blank" rel="noopener">Follow on BookBub</a></li>
          <li><a href="/support/">Support the build</a></li>
        </ul>
      </div>
      <div>
        <h4>{e(D.get("platforms",{}).get("heading","Where to find the books"))}</h4>
        <ul>{platforms_html}</ul>
      </div>
      <div>
        <h4>Elsewhere</h4>
        <ul>
          <li><a href="{e(S['bookbub_site'])}" target="_blank" rel="noopener">Author page on BookBub</a></li>
          <li><a href="https://www.tiktok.com/@carrierpress" target="_blank" rel="noopener">TikTok</a></li>
        </ul>
      </div>
    </div>
    <div class="colophon">
      <span>&copy; {datetime.date.today().year} {e(S['author'])}. All rights reserved.</span>
      <span>Carrier Press LLC, Diamondhead, Mississippi.</span>
    </div>
  </div>
</footer>
<script>(function(){{var m=location.hash.match(/^#b-([A-Z0-9]{{10}})$/),t={json.dumps(HOME_FWD, separators=(",", ":"))},
h=location.hash.slice(1),c={json.dumps(MOVED, separators=(",", ":"))};if(!h||document.getElementById(h))return;
if(m&&t[m[1]])location.replace(t[m[1]]);else if(c.indexOf(h)>=0)location.replace("/catalog/#"+h);}})();</script>
</body>
</html>
"""

_guard_select()
pathlib.Path("index.html").write_text(HTML, encoding="utf-8")
# The product-section links are owned by nav.py, in one place, because this
# nav also lives in three hand-written or separately-templated pages and has
# already been edited in more files each time it changed.
nav.patch("index.html")
print(f"index.html written: {total} titles across {len(D['sections'])} sections, "
      f"{len(HTML):,} bytes")


def write_category(c):
    """One category page, cut from the home page's own head, header and footer so
    the chrome can never drift. Every shelf in full, its own title and canonical."""
    import re
    secs = [s for s in D["sections"] if c["test"](s)]
    n = sum(1 for s in secs for b in s["books"] if not b.get("soon"))
    body = (f'<section class="cat-hero"><div class="wrap"><p class="eyebrow">{e(c["eyebrow"])}</p>'
            f'<h1>{e(c["h1"])}</h1><p>{e(c["intro"])}</p><p class="cat-count">{n} titles</p>'
            f'</div></section>\n' + "\n".join(section(s, head=len(secs) > 1) for s in secs))
    if c["slug"] == "young-readers":
        body += "\n" + comics_html()
    if c["slug"] == "classics":
        # The hub is a way into this line, so the line's own page points at it.
        body = body.replace('</div></section>\n', f'<p class="see-all"><a href="/{W.SLUG}/">New to the line? '
                            f'Start with weird fiction and cosmic horror, from The King in Yellow.</a></p>'
                            '</div></section>\n', 1)
    if c["slug"] == "classics":
        body += ('\n<section aria-label="Free sample"><div class="wrap">'
                 + _magnet.block("classics", "The introduction and two complete stories from the restored, "
                                 "annotated edition, sent to your inbox as EPUB and PDF.")
                 + '</div></section>')
    canon = f"https://{S['domain']}/{c['slug']}/"
    page = HTML
    page = re.sub(r'<main id="main">.*</main>', lambda m: f'<main id="main">\n{body}\n</main>', page, flags=re.S)
    page = re.sub(r'<title>[^<]*</title>', f'<title>{e(c["title"])}</title>', page, count=1)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(c["title"]), page, count=1)
    page = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(c["intro"]), page, count=1)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(c["intro"]), page, count=1)
    page = page.replace(f'<link rel="canonical" href="https://{S["domain"]}/">', f'<link rel="canonical" href="{canon}">')
    page = page.replace(f'<meta property="og:url" content="https://{S["domain"]}/">', f'<meta property="og:url" content="{canon}">')
    page = page.replace(f'<script type="application/ld+json">{json.dumps(books_ld)}</script>\n', '')
    page = re.sub(r'<script>\(function\(\)\{var m=location\.hash.*?</script>\n', '', page, flags=re.S)
    page = re.sub(r'(src|href)="(assets/|styles\.css)', r'\1="/\2', page)
    page = re.sub(r'href="#(?!main")', 'href="/#', page)
    out = pathlib.Path(c["slug"]) / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    nav.patch(out)
    return out


for _c in CATEGORIES:
    print(f"category: {write_category(_c)}")


def _subpage(slug, body, title, desc, keep=()):
    """A page cut from the home page's own head, header and footer, like
    write_category, so the chrome cannot drift. `keep` lists the in-page anchors
    this page owns; every other same-page link points back at the home page."""
    import re
    canon = f"https://{S['domain']}/{slug}/"
    page = HTML
    page = re.sub(r'<main id="main">.*</main>', lambda m: f'<main id="main">\n{body}\n</main>', page, flags=re.S)
    page = re.sub(r'<title>[^<]*</title>', lambda m: f'<title>{e(title)}</title>', page, count=1)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(title), page, count=1)
    page = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(desc), page, count=1)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(desc), page, count=1)
    page = page.replace(f'<link rel="canonical" href="https://{S["domain"]}/">', f'<link rel="canonical" href="{canon}">')
    page = page.replace(f'<meta property="og:url" content="https://{S["domain"]}/">', f'<meta property="og:url" content="{canon}">')
    page = re.sub(r'<script>\(function\(\)\{var m=location\.hash.*?</script>\n', '', page, flags=re.S)
    page = re.sub(r'(src|href)="(assets/|apps/shots/|styles\.css)', r'\1="/\2', page)
    own = "|".join(["main"] + [re.escape(k) for k in keep] + ["b-[A-Z0-9]{10}"])
    page = re.sub(r'href="#(?!(?:%s)")' % own, 'href="/#', page)
    out = pathlib.Path(slug) / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    nav.patch(out)
    return out


def write_catalog():
    """/catalog/: everything the home page used to carry below the hero, in the
    same order, so nothing was lost when the home page moved to threads. Shelves
    still show HOME_LIMIT books each and link to their category page in full."""
    jumps = [("start", "Start here"), ("top10", "Best sellers"), ("fiction", "Fiction"),
             ("classics", "Classics"), ("young", "Young readers"), ("music", "Music")]
    body = (f'<section class="cat-hero"><div class="wrap"><p class="eyebrow">The whole catalogue</p>'
            f'<h1>Every Carrier Press book</h1>'
            f'<p>Fiction by {e(S["author"])}, restored classics, books for young readers and '
            f'personal finance, all available on Amazon. Start with the best sellers, or jump to a shelf.</p>'
            f'<p class="cat-count">{total} titles &middot; '
            + " &middot; ".join(f'<a href="#{a}">{e(l)}</a>' for a, l in jumps)
            + '</p></div></section>\n'
            + top_html + "\n" + sections_html + "\n" + kids_html + "\n" + after_books_html)
    return _subpage("catalog", body, f"Every Book | Carrier Press",
                    f"The whole Carrier Press catalogue: {total} titles of fiction, restored classics, "
                    "books for young readers and personal finance, with this year's best sellers.",
                    keep=MOVED + ["h-" + sec["id"] for sec in D["sections"]])


def write_gifts():
    """/gifts/: the gift guide (home_data.GIFTS). One shelf per kind of reader,
    every card from book_card(), so each gift has its print price and its Buy on
    Amazon button. It stays up between seasons; a gift season may give it its own
    title, heading, intro and shelves (home_data.SEASONS `gifts`)."""
    G = (H.SEASON or {}).get("gifts") or {}
    title, h1, intro = (G.get("title", H.GIFTS_TITLE), G.get("h1", H.GIFTS_H1),
                        G.get("intro", H.GIFTS_INTRO))
    shelves = G.get("shelves") or H.GIFTS
    index = {b["a"]: b for s_ in D["sections"] for b in s_["books"]}
    out = ['<section class="cat-hero"><div class="wrap"><p class="eyebrow">Gift guide</p>',
           f'<h1>{e(h1)}</h1><p>{e(intro)}</p></div></section>']
    for n_, (heading, blurb, asins) in enumerate(shelves, 1):
        out += [f'<section class="gift-shelf" aria-labelledby="g-{n_}"><div class="wrap"><div class="sec-head">',
                f'<h2 id="g-{n_}">{e(heading)}</h2><p>{e(blurb)}</p></div><div class="shelf">']
        for a in asins:
            a, name = a if isinstance(a, tuple) else (a, None)
            b = index.get(a)
            if b is None or b.get("soon"):
                raise SystemExit(f"gift guide: {a} is not a buyable catalogue title")
            card = dict(b)
            if name:
                card["t"] = name
                card.pop("omnibus", None)
            out.append(book_card(card, "group", anchor=False))
        out += ['</div></div></section>']
    if H.HOLIDAY_CODE:
        # Gumroad only: the apps and Cast. Never placed on a book card.
        code, first, last = H.HOLIDAY_CODE
        span = (f"{first.day} to {last.day} {last:%B}" if first.month == last.month
                else f"{first.day} {first:%B} to {last.day} {last:%B}")
        out.append(f'<section class="gift-code" aria-label="Holiday code for the apps and Cast"><div class="wrap">'
                   f'<p class="see-all"><strong>For the apps and Cast:</strong> code <strong>{e(code)}</strong> '
                   f'takes 25% off at checkout, {e(span)} (on a subscription, the first payment). '
                   f'<a href="/apps/">See the apps</a> &middot; <a href="/cast/">See Cast</a></p></div></section>')
    out.append(f'<section><div class="wrap"><p class="see-all"><a href="/catalog/">Browse all {total} books</a>'
               f' &middot; <a href="/#threads">Back to the home page</a></p></div></section>')
    return _subpage("gifts", "\n".join(out), title, intro)


print(f"catalog: {write_catalog()}")
print(f"gifts: {write_gifts()}")


# THE FREE SAMPLE SIGNUP (author 2026-11-21, "Yes, swap it"). The signup used to
# be a MailerLite-hosted landing page that still pitched The Sponge Cache while
# the welcome email sent The King in Yellow. The form now lives here, on our own
# page, so the pitch and the email cannot drift apart again. MAGNET_FORM is the
# embedded form "Free sample: The King in Yellow (carrierpress.com/free)"; it
# adds signups to the group TLO Readers (192738353903305745), whose welcome
# automation (192738278727747164) sends the sample from /free/*.epub and *.pdf.
# Double opt-in is on, so the first email is the confirmation.
# The form itself, and its MailerLite ids, now live in magnet.py (2026-11-27),
# shared with the journal posts, /weird-fiction/ and /classics/ (imported at the top).


def write_free():
    form = _magnet.form("free")
    body = ('<section id="free" class="magnet" aria-labelledby="h-free"><div class="wrap magnet-in"><div>'
            '<p class="eyebrow">Free sample</p>'
            '<h1 id="h-free">Read the opening of <em>The King in Yellow</em></h1>'
            '<p>A forbidden play ruins everyone who reads it to the end. Chambers never lets you see it; '
            'you only meet the people it has already claimed. Weird fiction has been borrowing from these '
            'stories since 1895: the cursed play, the lost city of Carcosa, the Yellow Sign.</p>'
            '<p>Your sample is the opening of the restored, annotated Carrier Press edition: the '
            'introduction and two complete stories, "The Repairer of Reputations" and "The Mask," with '
            'three of its illustrations. It arrives in your inbox as EPUB and PDF, yours to keep.</p>'
            f'<div style="margin-top:22px">{form}</div>'
            '<p>Then a short welcome note from me, and word when the next book is out.</p>'
            '</div><div class="magnet-cover"><img src="/assets/covers/B0H7W7VY7S.jpg" width="313" '
            'height="500" alt="Cover of The King in Yellow"></div></div></section>')
    return _subpage("free", body, "Free Sample: The King in Yellow | Carrier Press",
                    "Read the opening of the restored, annotated King in Yellow free: the introduction "
                    "and two complete stories, sent to your inbox as EPUB and PDF.", keep=["free"])


print(f"free: {write_free()}")


def write_weird():
    """/weird-fiction/: the weird fiction and cosmic horror hub. Cut from the home
    page's own head, header and footer exactly like write_category, so the chrome
    cannot drift. Copy and title list come from weird_data.py; every card, price and
    buy link comes from the catalogue and formats.json through book_card(), so the
    hub shows the same paperback-first "Buy on Amazon" as every other shelf."""
    import re
    index = {b["a"]: b for s_ in D["sections"] for b in s_["books"]}
    lines = dict(W.LINES)
    for conn in (D.get("bestseller") or {}).get("connected") or []:
        if conn.get("why"):
            lines.setdefault(conn["a"], conn["why"])
    lines[W.KIY] = W.LEAD
    for asin in W.NEXT:
        if asin not in index:
            raise SystemExit(f"weird hub: {asin} is not in the catalogue")
        if asin not in lines:
            raise SystemExit(f"weird hub: {asin} ({index[asin]['t']}) has no card line")

    def card(asin):
        c = dict(index[asin])
        c.pop("n", None)
        c.pop("omnibus", None)
        c["hook"] = lines[asin]
        return c

    dom = S["domain"]
    canon = f"https://{dom}/{W.SLUG}/"
    lead = index[W.KIY]
    fmt, buy_asin, _ = _books.print_edition(W.KIY)

    out = ['<section class="cat-hero"><div class="wrap">',
           f'<p class="eyebrow">{e(W.EYEBROW)}</p>', f'<h1>{e(W.H1)}</h1>']
    out += [f'<p>{e(p_)}</p>' for p_ in W.INTRO]
    out.append(f'<p class="cat-count">{len(W.NEXT)} titles &middot; '
               f'<a href="#reading-order">Jump to the reading order</a></p></div></section>')

    # The lead: The King in Yellow, with the 3D book slot book3d.js fills.
    out += ['<section id="start-here" class="wk-lead" aria-labelledby="h-wk-lead">',
            '<div class="wrap"><div class="sec-head"><p class="eyebrow">Start here</p>',
            f'<h2 id="h-wk-lead">{e(lead["t"])} by {e(lead["by"])}</h2></div>',
            '<div class="lead">',
            f'<a class="lead-cover" href="{BOOK_URL[W.KIY]}"><img src="assets/covers/{W.KIY}.jpg" '
            f'decoding="async" width="313" height="500" alt="Cover of {e(lead["t"])}"></a>',
            '<div class="lead-meta">',
            f'<p class="lead-hook">{e(W.LEAD)}</p>',
            '<p><a href="/weird-fiction/the-king-in-yellow/">The King in Yellow, explained: the play, the reading order, the Yellow Sign and Carcosa</a></p>',
            '<p class="actions">'
            f'<a class="buy" href="{AMZ.format(buy_asin)}" target="_blank" rel="noopener" '
            f'aria-label="{e(_books.buy_label(fmt))}, {e(lead["t"])}, on Amazon">{e(_books.buy_label(fmt))}</a>'
            + f'<a class="rev" href="{BOOK_URL[W.KIY]}">About this edition</a></p>',
            f'<p {_books.b3_attrs("dialog", W.KIY, lead["t"])}></p>',
            '</div></div></div></section>']

    # What the edition holds, from its own catalogue record: the page that answers
    # "robert w chambers king in yellow edition".
    adds = [a for a in (lead.get("adds") or []) if str(a).strip()]
    if adds:
        out += ['<section class="wk-edition" aria-labelledby="h-wk-ed"><div class="wrap">',
                '<div class="sec-head">',
                '<h2 id="h-wk-ed">The King in Yellow by Robert W. Chambers: this edition</h2>',
                '<p>A restored, annotated edition from Carrier Press. It includes:</p></div>',
                '<ul class="wk-adds">' + "".join(f'<li>{e(a)}</li>' for a in adds) + '</ul>',
                f'<p class="see-all"><a href="{BOOK_URL[W.KIY]}">Formats and the full '
                f'listing</a></p></div></section>']

    # The reading order, three steps and then the rest.
    out += ['<section id="reading-order" class="wk-order" aria-labelledby="h-wk-order"><div class="wrap">',
            '<div class="sec-head"><p class="eyebrow">Reading order</p>',
            '<h2 id="h-wk-order">Where to start with classic cosmic horror</h2>',
            '<p>Read The King in Yellow, then Carcosa, then the rest in any order. The list runs '
            'from the closest books to the furthest.</p></div><ol class="wk-list">']
    for n_, (asin, why) in enumerate(W.ORDER, 1):
        b = index[asin]
        out.append(f'<li><span class="wk-n">{n_}</span><div><a href="{BOOK_URL[asin]}">{e(b["t"])}</a> '
                   f'<span class="wk-by">{e(b["by"])}</span><p>{e(why)}</p></div></li>')
    out += ['</ol></div></section>']
    out += ['<section aria-label="Free sample"><div class="wrap">',
            _magnet.block("weird", "Start the reading order free: the introduction and two complete stories, "
                          "sent to your inbox as EPUB and PDF."),
            '</div></section>']

    ids = []
    for n_, (heading, intro, asins) in enumerate(W.SHELVES, 1):
        sid = f"wk-shelf-{n_}"
        ids += asins
        out += [f'<section aria-labelledby="{sid}"><div class="wrap"><div class="sec-head">',
                f'<h2 id="{sid}">{e(heading)}</h2><p>{e(intro)}</p></div><div class="shelf">']
        out += [book_card(card(a), "group", anchor=False) for a in asins]
        out += ['</div></div></section>']
    missing = (set(W.NEXT) - {W.KIY}) - set(ids)
    if missing:
        raise SystemExit(f"weird hub: titles in NEXT but on no shelf: {sorted(missing)}")

    # Visible FAQ; the FAQPage markup below is read from the same list.
    kiy_prices = ""   # no prices on the site (author 2026-11-20)
    faq = [(q, a.replace("{kiy_prices}", kiy_prices).strip()) for q, a in W.FAQ]
    out += ['<section class="wk-faq" aria-labelledby="h-wk-faq"><div class="wrap">',
            '<div class="sec-head"><h2 id="h-wk-faq">Questions about weird fiction and these editions</h2></div>']
    out += [f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in faq]
    out += [f'<p class="see-all"><a href="/classics/">The whole Classics Line</a> &middot; '
            f'<a href="/catalog/">All {total} Carrier Press titles</a></p></div></section>']
    body = "\n".join(out)

    item_list = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "Classic weird fiction and cosmic horror from Carrier Press",
        "url": canon, "numberOfItems": len(W.NEXT),
        "itemListElement": [book_ld(card(a), i) for i, a in enumerate([W.KIY] + ids, 1)],
    }
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Carrier Press", "item": f"https://{dom}/"},
        {"@type": "ListItem", "position": 2, "name": "Classics", "item": f"https://{dom}/classics/"},
        {"@type": "ListItem", "position": 3, "name": "Weird fiction", "item": canon}]}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faq]}
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n'
                      for x in (item_list, crumbs, faq_ld))

    page = HTML
    page = re.sub(r'<main id="main">.*</main>', lambda m: f'<main id="main">\n{body}\n</main>', page, flags=re.S)
    page = re.sub(r'<title>[^<]*</title>', lambda m: f'<title>{e(W.TITLE)}</title>', page, count=1)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(W.TITLE), page, count=1)
    page = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(W.DESC), page, count=1)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(W.DESC), page, count=1)
    page = page.replace(f'<link rel="canonical" href="https://{dom}/">', f'<link rel="canonical" href="{canon}">')
    page = page.replace(f'<meta property="og:url" content="https://{dom}/">', f'<meta property="og:url" content="{canon}">')
    # The og card is the lead cover, the same image a book page offers.
    page = page.replace(f'content="https://{dom}/assets/og-image.png"',
                        f'content="https://{dom}/assets/covers/{W.KIY}.jpg"')
    page = page.replace('<meta property="og:image:width" content="1200">', '<meta property="og:image:width" content="313">')
    page = page.replace('<meta property="og:image:height" content="630">', '<meta property="og:image:height" content="500">')
    page = page.replace('<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:card" content="summary">')
    page = page.replace(f'<script type="application/ld+json">{json.dumps(books_ld)}</script>\n', ld_html)
    assert ld_html in page, "weird hub: could not place its structured data"
    page = re.sub(r'<script>\(function\(\)\{var m=location\.hash.*?</script>\n', '', page, flags=re.S)
    page = re.sub(r'(src|href)="(assets/|styles\.css)', r'\1="/\2', page)
    page = re.sub(r'href="#(?!main"|reading-order")', 'href="/#', page)
    out_path = pathlib.Path(W.SLUG) / "index.html"
    _books._guard(str(out_path), page)
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    nav.patch(out_path)
    return out_path


print(f"weird hub: {write_weird()}")

import blog as _blog
_n = _blog.build(S)
print(f"blog: {_n} published post(s) -> blog/index.html, feed.xml")

# ------------------------------------------------------------------------ sitemap
# Generated, not hand kept. The old static sitemap listed only "/" and was frozen at
# the day it was typed, so the journal pages would never have appeared in it and
# nothing would have reported the omission.
#
# changefreq and priority are omitted on purpose: Google ignores both, and a hint it
# ignores is just a line that can drift out of date.
# Hand-written pages that live in their own directory and are never regenerated
# here. build.py only rewrites index.html and sitemap.xml, so these would
# otherwise be invisible to a crawler that only reads the sitemap.
#
# ▶ DERIVED, NOT TYPED (2026-10-20). This list used to be seven hand-typed
# paths, so the forty app landing pages and their /apps/<slug>/ listings never
# reached the sitemap: 13 urls listed out of ~90 public pages. It is now every
# index.html on disk that declares ITSELF as canonical and is not noindex,
# which is the page's own statement that it wants to be found. A redirect stub
# (/homerule/, canonical to /whoserves/) excludes itself that way.
# Excluded outright, whatever they declare:
#   privacy pages            reached from App Store records, not search
#   support_bodies/          fragments, not pages
#   _patreon/                not public
#   any /<slug>/app/ bundle  the exported web apps; the landing page is the entry
#   /blog/ and /books/       listed below with their own dates
#   /play/                   only once play_data.ITCH_URL is set, see make_play.py
_SKIP_TOP = {"support_bodies", "_patreon", "blog", "books", "vendor", "assets", ".git"}


def _landing_pages():
    import re
    found = []
    for f in sorted(pathlib.Path(".").glob("**/index.html")):
        parts = f.parent.parts
        if not parts:
            continue                      # the homepage, listed first on its own
        if (parts[0] in _SKIP_TOP or "privacy" in parts or "app" in parts
                or any(p.startswith(".") for p in parts)):
            continue
        if parts[0] == "play" and not play_data.ITCH_URL:
            continue
        path = "/" + "/".join(parts) + "/"
        s = f.read_text(encoding="utf-8", errors="replace")
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not canon or canon.group(1) != f"https://{S['domain']}{path}":
            continue
        if re.search(r'<meta name="robots" content="[^"]*noindex', s):
            continue
        found.append(path)
    return sorted(found)


import make_fair as _fair   # /fair/, the book fair QR page (2026-11-08); before the sitemap reads the pages
_fair.build()
import make_picker as _picker   # /pick/, find your next book (2026-11-18); before the sitemap
_picker.build()
import make_shop as _shop   # /shop/, merch via the Printful Quick Store (author 2026-11-27); before the sitemap
_shop.build()
import make_kiy_pages as _kiy_pages   # /weird-fiction/the-king-in-yellow/ (2026-11-27); before the sitemap
_kiy_pages.build()
import make_app_help as _app_help   # /apps/endorsed/practice/, /apps/boatready/requirements/ (2026-11-27); before the sitemap
_app_help.build()
import make_guides as _guides   # /guides/, reader's guides (2026-11-27); before the sitemap
_guides.build()
import make_officials as _officials   # /officials/<state>/ (2026-11-23); before the sitemap
print("officials: %d state page(s) -> officials/<state>/" % len(_officials.build()))

# MIRROR THE STATEWIDE FILE TO THE OLD PATH (2026-11-24).
#
# Who Serves app builds up to 19 still fetch /homerule/data/, so that directory
# is published as a copy and must keep being written; the weekly
# whoserves-officeholders workflow already mirrors officeholders.json there.
# statewide.json was never mirrored, because unlike officeholders.json it has
# no builder and no workflow -- it is hand-maintained, with check_statewide.py
# writing only verifiedAt. So nothing ever copied it, and the two drifted for
# two months: on 2026-11-24 the live file had every row rechecked that day
# while the published copy still carried September dates AND fifteen source
# URLs since found dead -- a domain that had moved, an apex with no DNS record,
# several pages that had been reorganised. Readers on an old build were being
# handed those links.
#
# Mirroring here rather than in check_statewide.py is deliberate: this runs on
# every build, so it catches a hand edit to the data file as well as a verify
# pass, and test.yml's `git diff --exit-code` then makes any divergence a red
# run rather than something to notice two months later.
#
# NOT A BYTE COPY. The live file is pretty-printed at 124 KB; the old path has
# always served the same data minified, at 92 KB. An app on an old build
# fetching this on launch should not start paying 34% more for the privilege of
# correct links, so the mirror is re-rendered in the format that path already
# uses. Verified on 2026-11-24 that these exact arguments reproduce the
# published legacy file byte for byte, so this converges instead of rewriting
# the file on every run. A single line with no trailing newline also has no
# line endings to convert, which keeps it identical on Windows and on CI.
#
# TO RETIRE THE OLD PATH, delete homerule/data/statewide.json. This writes the
# mirror only when it is already there, so removing the file ends the mirror
# instead of resurrecting it on the next build.
_SW_LIVE = pathlib.Path("whoserves") / "data" / "statewide.json"
_SW_COPY = pathlib.Path("homerule") / "data" / "statewide.json"
if not _SW_COPY.exists():
    print("homerule mirror: old path retired, statewide.json not written")
else:
    _sw = json.dumps(json.loads(_SW_LIVE.read_text(encoding="utf-8")),
                     separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if _SW_COPY.read_bytes() == _sw:
        print("homerule mirror: statewide.json already matches whoserves/data/")
    else:
        _SW_COPY.write_bytes(_sw)
        print("homerule mirror: statewide.json refreshed from whoserves/data/"
              " (%s bytes)" % format(len(_sw), ","))

STATIC_PAGES = _landing_pages()
for _must in ("/labs/", "/apps/", "/audio/", "/progress/", "/reviews/", "/support/", "/links/"):
    if _must not in STATIC_PAGES:
        raise SystemExit(f"sitemap: {_must} dropped out of the derived page list; check its canonical")

BOOK_PAGES = _books.build(D, S)
print(f"books: {len(BOOK_PAGES)} title page(s) -> books/<slug>/index.html")

# ⛔ lastmod IS DERIVED FROM CONTENT, NOT FROM THE CLOCK. It used to be
# datetime.date.today() for the homepage and every static page, on every build.
# Two things were wrong with that. A lastmod that always reads "today" is a
# signal a crawler learns to discount, so it did not merely fail to help, it
# devalued the field. And it made the build unreproducible: regenerate a clean
# checkout tomorrow and sitemap.xml changes although not one page did, which is
# precisely the check CI needs to be able to run.
#
# So each page's content is hashed and the hash is remembered with the date it
# was first seen. An unchanged page keeps its old date; a changed page takes
# today's. The journal already did this correctly by using each post's own date,
# and that is left alone.
STATE = pathlib.Path("sitemap_state.json")


def _digest(f):
    """The hash of a page, with its line endings normalised first.

    NORMALISE BEFORE HASHING. The hash asks whether the content changed, and a
    line ending is not content. git stores these files with LF and checks them
    out with CRLF on Windows, so hashing the bytes on disk asked a different
    question on each machine: one unchanged page hashed one way on a Windows
    build and another on the Linux runner, and whichever ran last stamped
    today's date on pages nobody had touched. On 2026-11-24 a single push had
    to put such dates back by hand twice, 14 pages each time, before the
    sitemap was honest enough to ship. Normalising makes the two machines
    agree, and the date moves only when the page really changes.

    The bytes are patched rather than read as text, so this cannot also fold
    away an encoding difference, which WOULD be a real change.

    Changing this invalidates every sha256 in sitemap_state.json at once. If it
    ever changes again, rehash every entry in that file in the same commit and
    leave each lastmod alone, or the next build dates the whole site today.
    """
    return hashlib.sha256(f.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _page_dates(paths):
    """{url path: lastmod} for pages whose date comes from their file content.

    Seeded by hand from `git log` when this was introduced, so the first build
    did not stamp today's date on four pages that had not changed that day.
    """
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    today = datetime.date.today().isoformat()
    out, new_state = {}, {}
    for path in paths:
        f = pathlib.Path((path.strip("/") or ".") , "index.html")
        if not f.exists():
            continue
        digest = _digest(f)
        prior = state.get(path) or {}
        # Same bytes as last time means the page did not change, whatever the
        # calendar says. Only a real content change moves the date.
        date = prior["lastmod"] if prior.get("sha256") == digest else today
        out[path] = date
        new_state[path] = {"sha256": digest, "lastmod": date}
    # Sorted, so the file is stable and a diff shows a real change rather than
    # a reordering.
    STATE.write_text(json.dumps(new_state, indent=2, sort_keys=True) + "\n",
                     encoding="utf-8")
    return out


def write_sitemap(posts):
    dates = _page_dates(["/"] + STATIC_PAGES + BOOK_PAGES)
    urls = [(f"https://{S['domain']}/", dates["/"])]
    urls += [(f"https://{S['domain']}{path}", dates[path])
             for path in STATIC_PAGES + BOOK_PAGES if path in dates]
    if posts:
        urls.append((f"https://{S['domain']}/blog/", max(p["date"] for p in posts).isoformat()))
        urls += [(f"https://{S['domain']}/blog/{p['slug']}.html", p["date"].isoformat())
                 for p in posts]
    body = "".join(f"  <url><loc>{html.escape(u)}</loc><lastmod>{d}</lastmod></url>\n"
                   for u, d in urls)
    pathlib.Path("sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!-- GENERATED by build.py. Do not hand-edit, it is overwritten. -->\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body + "</urlset>\n", encoding="utf-8")
    return len(urls)

print(f"sitemap.xml written: {write_sitemap(_blog._load())} url(s)")
