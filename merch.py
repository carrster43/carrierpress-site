#!/usr/bin/env python3
"""
"From this book": the merch strip on a book page, and the Captain Cubemelon
strip under the comics band (author 2026-11-27: link merch where a reader
would want it).

The products are shop_data.json, the same records /shop/ is built from
(make_shop.py), so a product removed there leaves every strip by itself.
Nothing here invents a product: a strip only ever shows records that exist.

MATCHING, by title, never by guess:
  1. A product title is "<name>: <kind>". When slugify(<name>) is a book page's
     slug, the product belongs to that book ("The Golem: Book Cover Poster, 12x18"
     goes on /books/the-golem/).
  2. EXTRA names the products whose <name> is not a book title: quote cards,
     plates and the line tees. Each line's source is the merch kit's quote table
     (B2/Brand/merch/ETSY_PRINTFUL_SETUP.md), where every quote was checked
     against that edition's own text.
  3. The Captain Cubemelon group goes on the twelve Captain Cubemelon & Friends
     books (The Gadget Sandbox Chronicles and The Glitch Blocks) and under the
     comics band.
Products with no page stay on /shop/ only: the At the Mountains of Madness
pieces (that volume has no book page yet) and the 2027 calendar, which spans
twelve books.
"""
import html
import json
import os
import re
import unicodedata


def slugify(s):
    # Same as books.slugify (books.py imports this module, so it cannot import books).
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower().replace(",", ""))
    return s.strip("-")


HERE = os.path.dirname(os.path.abspath(__file__))
SHOP = "/shop/"

# product title (exact, as in shop_data.json) -> book page slug
EXTRA = {
    # The King in Yellow: its two interior plates, and the two tees that carry
    # Cassilda's Song from the book.
    "Carcosa, Cassilda's Song: King in Yellow Plate Poster, 12x18": "the-king-in-yellow",
    "Carcosa, Cassilda's Song: King in Yellow Plate Canvas, 12x18": "the-king-in-yellow",
    "Carcosa, Cassilda's Song: King in Yellow Plate Note Card": "the-king-in-yellow",
    "Have You Found the Yellow Sign?: King in Yellow Plate Poster, 12x18": "the-king-in-yellow",
    "Have You Found the Yellow Sign?: King in Yellow Plate Canvas, 12x18": "the-king-in-yellow",
    "Have You Found the Yellow Sign?: King in Yellow Plate Note Card": "the-king-in-yellow",
    "Strange Is the Night Where Black Stars Rise T-Shirt": "the-king-in-yellow",
    "But Stranger Still Is Lost Carcosa T-Shirt": "the-king-in-yellow",
    # Blackwood: all five lines are from The Willows edition (The Willows,
    # The Wendigo, Ancient Sorceries).
    "The Willows Were Against Us: Algernon Blackwood Quote Card": "the-willows",
    "We Had Strayed: Algernon Blackwood Quote Card": "the-willows",
    "The Willows Mask the Others: Algernon Blackwood Quote Card": "the-willows",
    "This Fiery Height: Algernon Blackwood Quote Card": "the-willows",
    "The Souls of Night-Things: Algernon Blackwood Quote Card": "the-willows",
    # Machen: two lines from The Great God Pan edition (the title story and
    # The White People), two from The Three Impostors.
    "Seeing the God Pan: Arthur Machen Quote Card": "the-great-god-pan",
    "Sorcery and Sanctity: Arthur Machen Quote Card": "the-great-god-pan",
    "Battled for the Marvellous: Arthur Machen Quote Card": "the-three-impostors",
    "London Is a Fortified Place: Arthur Machen Quote Card": "the-three-impostors",
    # Lovecraft Volume One: its cover pieces and the three lines from The Call
    # of Cthulhu. The other three Lovecraft lines are from Volume Two.
    "The Call of Cthulhu: Book Cover Poster, 12x18": "the-call-of-cthulhu-and-other-mythos-tales",
    "The Call of Cthulhu: Book Cover Note Card": "the-call-of-cthulhu-and-other-mythos-tales",
    "A Placid Island of Ignorance: H. P. Lovecraft Quote Card": "the-call-of-cthulhu-and-other-mythos-tales",
    "Dead Cthulhu Waits Dreaming: H. P. Lovecraft Quote Card": "the-call-of-cthulhu-and-other-mythos-tales",
    "That Is Not Dead: H. P. Lovecraft Quote Card": "the-call-of-cthulhu-and-other-mythos-tales",
    # The Gadget Sandbox Chronicles pieces carry the cover of Book 1.
    "The Gadget Sandbox Chronicles: Book Cover Poster, 11x17": "the-first-build",
    "The Gadget Sandbox Chronicles: Book Cover Note Card": "the-first-build",
}

# The twelve Captain Cubemelon & Friends books (catalog sections The Gadget
# Sandbox Chronicles and The Glitch Blocks).
CUBEMELON_BOOKS = {
    "the-first-build", "the-runaway-crate", "the-frost-cave-reset", "sky-islands-save-file",
    "the-mech-workshop-machine", "portal-park",
    "the-first-flicker", "static-orchard", "the-loop-that-spoke", "the-broken-save",
    "the-moving-line", "the-between-badge",
}
# What a Cubemelon book page shows from that group: the tees and the sheet.
CUBEMELON_ON_BOOKS = ("Tee (Adult)", "Tee (Youth)", "Crew Sticker Sheet")

MAX = 8  # tiles in one strip; the rest are a tap away on /shop/


def e(x):
    return html.escape(str(x), quote=True)


def _items():
    with open(os.path.join(HERE, "shop_data.json"), encoding="utf-8") as f:
        return json.load(f)


def _rank(title):
    """The book's own cover first, then plates, lines and wear."""
    t = title.lower()
    for i, k in enumerate(("book cover poster", "book cover canvas", "book cover note card",
                           "t-shirt", "quote card", "plate poster", "plate canvas", "plate note card",
                           "tee (adult)", "tee (youth)", "sticker sheet")):
        if k in t:
            return i
    return 99


def products_for(slug):
    out = []
    for i in _items():
        name = i["title"].split(":")[0]
        if EXTRA.get(i["title"]) == slug or (i["title"] not in EXTRA and slugify(name) == slug):
            out.append(i)
    if slug in CUBEMELON_BOOKS:
        out += [i for i in _items() if i["group"] == "cubemelon"
                and any(i["title"].endswith(k) for k in CUBEMELON_ON_BOOKS)]
    return sorted(out, key=lambda i: _rank(i["title"]))


def _price(i):
    single_sticker = "Sticker" in i["title"] and "Sheet" not in i["title"]
    return ("from $" if single_sticker else "$") + i["price"]


def _label(i, book):
    """The tile caption without the book's own name in front of every tile."""
    name, _, rest = i["title"].partition(":")
    if book and rest and slugify(name) == book:
        return rest.strip()
    if book == "the-king-in-yellow" and "King in Yellow Plate" in rest:
        return name + ": " + rest.replace("King in Yellow ", "").strip()
    if rest and name == "Captain Cubemelon & Friends":
        return rest.strip()
    return i["title"]


def _strip(items, heading, lede, more, book=None):
    show = items[:MAX]
    left = len(items) - len(show)
    b = ['<aside class="mx" aria-label="%s">' % e(heading),
         '<h2>%s</h2>' % e(heading), '<p class="mx-l">%s</p>' % e(lede), '<ul class="mx-row">']
    for i in show:
        b.append('<li><a href="%s"><img src="%s" alt="" loading="lazy" decoding="async" '
                 'width="300" height="300"><span>%s</span><b>%s</b></a></li>'
                 % (e(i["url"]), e(i["img"]), e(_label(i, book)), e(_price(i))))
    b.append('</ul>')
    b.append('<p class="mx-more"><a href="%s">%s</a></p>'
             % (e(more), "See %d more in the shop" % left if left else "Visit the Carrier Press shop"))
    b.append('<p class="mx-n">Printed when you order it and shipped to US addresses.</p>')
    b.append('</aside>')
    s = "\n".join(b)
    for bad in ("—", "–", "&mdash;", "&ndash;"):
        assert bad not in s, "dash in merch strip"
    return s


def book_strip(slug):
    """The "From this book" strip for /books/<slug>/, or "" when it has no products."""
    items = products_for(slug)
    if not items:
        return ""
    if all(i["group"] == "cubemelon" for i in items):
        return _strip(items, "From Captain Cubemelon",
                      "Tees and stickers of the Captain and his crew.", SHOP + "#cubemelon", slug)
    return _strip(items, "From this book",
                  "The cover and lines from this book as wall art, note cards and more.", SHOP, slug)


def comics_strip():
    """Captain Cubemelon tees and stickers, under the comics band."""
    items = [i for i in _items() if i["group"] == "cubemelon"]
    order = ("Tee (Adult)", "Tee (Youth)", "Crew Sticker Sheet", "Captain Cubemelon Sticker", "Poster")
    items.sort(key=lambda i: next((n for n, k in enumerate(order) if k in i["title"]), 99))
    if not items:
        return ""
    return _strip(items, "Wear the crew",
                  "Captain Cubemelon tees for kids and grown ups, stickers of every crew member, "
                  "and the comic covers as posters.", SHOP + "#cubemelon")


if __name__ == "__main__":
    import sys
    for s in sys.argv[1:] or sorted(CUBEMELON_BOOKS):
        print(s, [i["title"] for i in products_for(s)])
