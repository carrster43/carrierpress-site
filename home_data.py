#!/usr/bin/env python3
"""
The home page's hooks, in ONE place. build.py reads this file.

WHY (author brief, 2026-11-17). The home page had grown into the whole
catalogue: hero, category strip, Start Here, the Top 12, the best seller band,
every shelf, the kids' zone, music and the support band, about 82,000 pixels
tall. It now opens with a short hero and a handful of THREADS: one book, one
series, one app or one gift idea each, every one with a buy button on the card
and a link onward. Everything that left the home page lives on /catalog/, and
old deep links into it (/#top10, /#b-<asin>, ...) are forwarded there.

THE RULES EVERY THREAD OBEYS.
  - A buy path within two clicks. A book or app thread carries its own buy
    button (one click); the gift thread goes to /gifts/, where every card has
    one (two clicks).
  - Titles, covers, authors and buy links resolve from catalog.json, and app
    names, prices and Gumroad links from apps_data.py and commerce.py, so a
    thread cannot drift from the shelves. An ASIN or slug that resolves to
    nothing fails the build.
  - Book copy promotes print: "available on Amazon", no formats, no Kindle
    prices. The Amazon button opens the paperback (books.print_edition).
  - No em or en dashes. No old or merged app names (folds.py).

>>> THE HOLIDAY SWITCH <<<
HOLIDAY = True turns on the gift framing: the hero copy, each thread's
`holiday` eyebrow, and the gift guide thread. Set it False after the season and
rebuild; nothing else needs touching. /gifts/ stays up either way (gifts are a
year round reason to buy), it simply stops being the home page's first thread.
"""

HOLIDAY = True

# The first screen. `holiday` replaces `regular` while HOLIDAY is on.
HERO = dict(
    regular=dict(
        kicker="Carrier Press",
        h1="The secrets families keep, and the people who decide to <em>read them</em>.",
        sub="Mystery, cosmic horror, adventures for young readers and restored classics, "
            "plus a few small apps that each do one job well.",
        primary=("Pull a thread", "#threads"),
        secondary=("Browse every book", "/catalog/"),
    ),
    holiday=dict(
        kicker="Holiday gift guide",
        h1="Give a book they will stay up <em>reading</em>.",
        sub="Mystery, cosmic horror, adventures for young readers and restored classics, "
            "all available on Amazon. Pick a thread below, or start with the gift guide.",
        primary=("Shop the gift guide", "/gifts/"),
        secondary=("Browse every book", "/catalog/"),
    ),
)

# The threads, in order. Three to five reads well; the grid takes any number.
#   kind   "gifts" | "book" | "app"
#   a      book threads: the catalogue ASIN the card is about
#   slug   app threads: the apps_data slug
#   eyebrow / holiday   the small label above the title (holiday wins in season)
#   title  optional; defaults to the book title or app name
#   line   the hook, one or two sentences
#   next   (label, href) the onward link: where this thread leads after the buy
#   holiday_only  shown only while HOLIDAY is on
THREADS = [
    dict(kind="gifts", holiday_only=True,
         eyebrow="Gift guide", holiday="Holiday gift guide",
         title="A book for everyone on your list",
         line="The mystery reader, the horror fan, the classics lover and the nine year old "
              "who reads under the covers. Every pick is available on Amazon.",
         covers=["B0H4CCMSQS", "B0H7W7VY7S", "B0H483NLCV", "B0H7QFWVXG"],
         next=("Open the gift guide", "/gifts/")),
    dict(kind="book", a="B0H7W7VY7S",
         eyebrow="Our best selling title", holiday="For the horror fan",
         line="A forbidden play, the Yellow Sign and the lost city of Carcosa. Lovecraft built "
              "on this book, and a century later True Detective sent a new generation looking for it.",
         next=("Follow the sign: the weird fiction line", "/weird-fiction/")),
    dict(kind="book", a="B0GZCKYKZ9", title="The Marjorie Corey Files",
         eyebrow="Start a series", holiday="For the mystery reader",
         line="Three women inherit a coffee shop and sixty years of what the town agreed not to "
              "say. Book one is The Second Shooter.",
         next=("Or give all five in one volume", "book:B0H4CCMSQS")),
    dict(kind="app", slug="cancelled",
         eyebrow="Before the January statements", holiday="Before the January statements",
         title="Find every subscription you forgot",
         line="Canceled reads a bank statement on your own device, ranks every recurring charge "
              "by what it costs a year, and shows you where to cancel. One payment, never a subscription.",
         next=("See how it works", "/cancelled/")),
    dict(kind="app", slug="downpour",
         eyebrow="For the game master", holiday="For game night",
         title="Rain for the table",
         line="Downpour makes rain live in your browser, on the tavern roof or over a camp in the "
              "forest, with no loop for the table to notice.",
         next=("Hear it first", "/downpour/")),
]

# /gifts/. One shelf per kind of reader, cards from catalog.json via book_card(),
# so every gift has its print price and its Buy on Amazon button. An entry is an
# ASIN, or (ASIN, title) where the shelf title is ambiguous out of its series.
GIFTS_TITLE = "Book Gift Ideas for Every Reader | Carrier Press"
GIFTS_H1 = "A book for everyone on your list"
GIFTS_INTRO = ("Mysteries to read by the fire, cosmic horror for the friend who likes to be "
               "unsettled, adventures for young readers, and classics in new editions. "
               "Every book here is available on Amazon.")
GIFTS = [
    ("For the mystery reader",
     "A small island, an old coffee shop, and sixty years of what the town agreed not to say. "
     "The complete series is one volume, so it wraps as one gift.",
     [("B0H4CCMSQS", "The Marjorie Corey Files: The Complete Series"),
      "B0GZCKYKZ9", "B0H6CWP5GN", "B0HMZKCTTS"]),
    ("For the horror fan",
     "Where cosmic horror starts: The King in Yellow, the Bierce tales it borrowed from, "
     "and Lovecraft's own mythos stories, each restored and annotated.",
     ["B0H7W7VY7S", "B0HGG934BB", "B0HQ55DVX2", "B0HGTD7VBZ"]),
    ("For young readers",
     "Book ones, so a gift can become a series. The Atherton Manor Mysteries are for ages "
     "9 to 13.",
     ["B0H483NLCV", "B0GXP2C498", "B0H6FH7TB7"]),
    ("For the classics lover",
     "Newly set editions with new introductions and notes, from a quiet romance to a "
     "Gothic doorstop.",
     ["B0H7QFWVXG", "B0H7PZ3FDM", "B0H7QPDD4S", "B0H7QSD429"]),
]
