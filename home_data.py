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

>>> THE SEASONS <<<
The site dresses for the season (author 2026-11-17: "we could have all the
seasons"). SEASONS below is a calendar: each season has its dates, its hero
copy, its ribbon bar, an optional menu link, a feature card that leads the
threads, and optionally its own gift guide shelves. Between seasons the site is
its regular self. Which season is on is DERIVED FROM THE DATE, so nothing needs
switching by hand:

  - nav.py marks every page it owns with <body data-season="<key>"> and puts the
    season's ribbon bar above the header; styles.css keys each season's look
    (colours, hero, falling or drifting decoration, wrapping paper) off that
    attribute. Privacy and support pages are never touched.
  - .github/workflows/season.yml reruns every generator each morning and
    commits only when a page changed, so the site turns over on a season's
    first day without anyone at a keyboard.
  - CP_SEASON=<key> (or CP_SEASON=none) in the environment forces a season for
    a local preview. Never set it in CI.

The holiday season ends January 7, 2027 (author 2026-11-17).
"""
import datetime, os

_D = datetime.date


def _sunday(year, month, n):
    """The nth Sunday of a month (Mother's Day: May, 2; Father's Day: June, 3)."""
    first = _D(year, month, 1)
    return first + datetime.timedelta(days=(6 - first.weekday()) % 7, weeks=n - 1)


_DAY = datetime.timedelta(days=1)

# fan: the five covers fanned in the hero (else the best sellers).
# when(year) -> (first day, first day AFTER the season). A season may run into
# the next year (the holiday season does). Seasons must not overlap; build.py
# refuses to build if two claim the same day.
SEASONS = {
    "valentines": dict(
        name="Valentine's Day",
        when=lambda y: (_D(y, 1, 25), _D(y, 2, 15)),
        fan=["B0H7QFWVXG", "B0H7PZ3FDM", "B0H4CCMSQS", "B0GZCKYKZ9", "B0H6CWP5GN"],
        hero=dict(kicker="Valentine's Day",
                  h1="Give a book they will <em>fall for</em>.",
                  sub="Love stories from the classics shelf and a mystery series to read "
                      "together, all available on Amazon.",
                  primary=("Shop Valentine's gifts", "/gifts/"),
                  secondary=("Browse every book", "/catalog/")),
        bar=("Valentine's Day", ": books for someone you love", "Shop gifts", "/gifts/"),
        nav=("/gifts/", "Gifts"),
        feature=dict(eyebrow="Valentine's Day", title="Books for someone you love",
                     line="A woman told she has a year to live who decides to live it, four women "
                          "who rent a castle in Italy, and a small town mystery to share. Every "
                          "pick is available on Amazon.",
                     covers=["B0H7QFWVXG", "B0H7PZ3FDM", "B0H4CCMSQS", "B0GZCKYKZ9"],
                     next=("Open the Valentine's guide", "/gifts/")),
        gifts=dict(title="Valentine's Day Book Gifts | Carrier Press",
                   h1="Books for someone you love",
                   intro="Love stories from the classics shelf, newly set and annotated, and a "
                         "mystery series for the reader who stays up past midnight. Every book "
                         "here is available on Amazon.",
                   shelves=[
                       ("For the romantic",
                        "Two classics about women who finally choose their own lives.",
                        ["B0H7QFWVXG", "B0H7PZ3FDM"]),
                       ("For the one who reads in bed",
                        "A small island, an old coffee shop, and sixty years of what the town "
                        "agreed not to say. The complete series is one volume.",
                        [("B0H4CCMSQS", "The Marjorie Corey Files: The Complete Series"),
                         "B0GZCKYKZ9", "B0H6CWP5GN"]),
                   ])),
    "mothers": dict(
        name="Mother's Day",
        when=lambda y: (_D(y, 4, 25), _sunday(y, 5, 2) + _DAY),
        fan=["B0H4CCMSQS", "B0H7PZ3FDM", "B0H483NLCV", "B0H7QFWVXG", "B0GZCKYKZ9"],
        hero=dict(kicker="Mother's Day",
                  h1="For the mother who taught you to <em>read</em>.",
                  sub="Cozy mystery, classics in new editions, and books she can read to the "
                      "grandchildren, all available on Amazon.",
                  primary=("Shop Mother's Day gifts", "/gifts/"),
                  secondary=("Browse every book", "/catalog/")),
        bar=("Mother's Day", ": a book for Mom", "Shop gifts", "/gifts/"),
        nav=("/gifts/", "Gifts"),
        feature=dict(eyebrow="Mother's Day", title="A book for Mom",
                     line="A coffee shop mystery in five books, two classics she may have missed, "
                          "and a series to read aloud to the grandchildren.",
                     covers=["B0H4CCMSQS", "B0H7PZ3FDM", "B0H483NLCV", "B0H7QFWVXG"],
                     next=("Open the Mother's Day guide", "/gifts/")),
        gifts=dict(title="Mother's Day Book Gifts | Carrier Press",
                   h1="A book for Mom",
                   intro="Cozy mystery, classics in new editions, and adventures she can share "
                         "with the grandchildren. Every book here is available on Amazon.",
                   shelves=[
                       ("For the mystery lover",
                        "A small island, an old coffee shop, and sixty years of what the town "
                        "agreed not to say. The complete series is one volume.",
                        [("B0H4CCMSQS", "The Marjorie Corey Files: The Complete Series"),
                         "B0GZCKYKZ9", "B0HMZKCTTS"]),
                       ("For the classics reader",
                        "Newly set editions with new introductions and notes.",
                        ["B0H7PZ3FDM", "B0H7QFWVXG"]),
                       ("To read with the grandchildren",
                        "Book ones, so a gift can become a series. The Atherton Manor Mysteries "
                        "are for ages 9 to 13.",
                        ["B0H483NLCV", "B0GXP2C498"]),
                   ])),
    "fathers": dict(
        name="Father's Day",
        when=lambda y: (_D(y, 6, 1), _sunday(y, 6, 3) + _DAY),
        fan=["B0GZCKYKZ9", "B0H7WM2CHN", "B0H7PDS3QM", "B0H7LYK2QQ", "B0H7QSD429"],
        hero=dict(kicker="Father's Day",
                  h1="Give Dad a book he will not put <em>down</em>.",
                  sub="Assassination threads, master thieves, gentleman burglars and cosmic "
                      "horror, all available on Amazon.",
                  primary=("Shop Father's Day gifts", "/gifts/"),
                  secondary=("Browse every book", "/catalog/")),
        bar=("Father's Day", ": a book for Dad", "Shop gifts", "/gifts/"),
        nav=("/gifts/", "Gifts"),
        feature=dict(eyebrow="Father's Day", title="A book for Dad",
                     line="A JFK assassination thread, the American who robbed the Bank of "
                          "England, a gentleman burglar and a master criminal.",
                     covers=["B0GZCKYKZ9", "B0H7WM2CHN", "B0H7PDS3QM", "B0H7LYK2QQ"],
                     next=("Open the Father's Day guide", "/gifts/")),
        gifts=dict(title="Father's Day Book Gifts | Carrier Press",
                   h1="A book for Dad",
                   intro="True history, master criminals and cosmic horror, for the father "
                         "who reads the whole thing. Every book here is available on Amazon.",
                   shelves=[
                       ("For the history reader",
                        "A sixty year old secret behind the JFK assassination, and the true "
                        "story of the Americans who robbed the Bank of England.",
                        ["B0GZCKYKZ9", "B0H7WM2CHN"]),
                       ("For the thriller reader",
                        "Master criminals and a gentleman burglar, from the books that made "
                        "the genre.",
                        ["B0H7LYK2QQ", "B0H7PDS3QM", "B0H7QSD429"]),
                       ("For the horror fan",
                        "Where cosmic horror starts, restored and annotated.",
                        ["B0H7W7VY7S", "B0HQ55DVX2"]),
                   ])),
    "summer": dict(
        name="Summer reading",
        when=lambda y: (_sunday(y, 6, 3) + _DAY, _D(y, 8, 1)),
        fan=["B0H483NLCV", "B0GXP2C498", "B0H6FH7TB7", "B0GYBT12DP", "B0HN3HJJBR"],
        hero=dict(kicker="Summer reading",
                  h1="Long days. Long <em>series</em>.",
                  sub="Adventure series for young readers, mysteries for the beach and "
                      "classics for the porch, all available on Amazon.",
                  primary=("Shop young readers", "/young-readers/"),
                  secondary=("Browse every book", "/catalog/")),
        bar=("Summer reading", ": series to fill the long days", "Shop young readers",
             "/young-readers/"),
        feature=dict(eyebrow="Summer reading", title="A series for every summer reader",
                     line="Three series that start at book one, for readers 7 to 14, and a first "
                          "business book for the kid with a plan.",
                     covers=["B0H483NLCV", "B0GXP2C498", "B0H6FH7TB7", "B0GYBT12DP"],
                     next=("Shop young readers", "/young-readers/"))),
    "school": dict(
        name="Back to school",
        when=lambda y: (_D(y, 8, 1), _D(y, 9, 8)),
        fan=["B0GXP2C498", "B0GYBT12DP", "B0H483NLCV", "B0H4DQ6488", "B0H6FH7TB7"],
        hero=dict(kicker="Back to school",
                  h1="Something good to read on the <em>bus</em>.",
                  sub="Adventure series, money skills and making things, for readers 7 to 14. "
                      "All available on Amazon.",
                  primary=("Shop young readers", "/young-readers/"),
                  secondary=("Browse every book", "/catalog/")),
        bar=("Back to school", ": books for readers 7 to 14", "Shop young readers",
             "/young-readers/"),
        feature=dict(eyebrow="Back to school", title="Books for the new school year",
                     line="Adventure series to read on the bus, and money skills for the kid "
                          "who already has a business plan.",
                     covers=["B0GXP2C498", "B0GYBT12DP", "B0H483NLCV", "B0H4DQ6488"],
                     next=("Shop young readers", "/young-readers/"))),
    "october": dict(
        name="October",
        when=lambda y: (_D(y, 10, 1), _D(y, 11, 1)),
        fan=["B0H7W7VY7S", "B0HGG934BB", "B0HQ55DVX2", "B0HGTD7VBZ", "B0HGMSMFQK"],
        hero=dict(kicker="October reading",
                  h1="Books to read with the <em>lights on</em>.",
                  sub="Cosmic horror, ghost stories and gothic classics, restored and "
                      "annotated, all available on Amazon.",
                  primary=("Shop weird fiction", "/weird-fiction/"),
                  secondary=("Browse every book", "/catalog/")),
        bar=("October reading", ": cosmic horror and ghost stories", "Shop weird fiction",
             "/weird-fiction/"),
        nav=("/weird-fiction/", "Weird Fiction"),
        feature=dict(eyebrow="October reading", title="Where cosmic horror starts",
                     line="The King in Yellow, the Bierce tales it borrowed from, Lovecraft's "
                          "own mythos stories and the willows on the Danube.",
                     covers=["B0H7W7VY7S", "B0HGG934BB", "B0HQ55DVX2", "B0HGTD7VBZ"],
                     next=("Open the weird fiction line", "/weird-fiction/"))),
    "holiday": dict(
        name="Holiday",
        when=lambda y: (_D(y, 11, 15), _D(y + 1, 1, 7)),
        hero=dict(kicker="Holiday gift guide",
                  h1="Give a book they will stay up <em>reading</em>.",
                  sub="Mystery, cosmic horror, adventures for young readers and restored "
                      "classics, all available on Amazon. Pick a thread below, or start with "
                      "the gift guide.",
                  primary=("Shop the gift guide", "/gifts/"),
                  secondary=("Browse every book", "/catalog/")),
        bar=("Holiday gift guide", ": a book for everyone on your list", "Shop gifts", "/gifts/"),
        nav=("/gifts/", "Gifts"),
        feature=dict(eyebrow="Holiday gift guide", title="A book for everyone on your list",
                     line="The mystery reader, the horror fan, the classics lover and the nine "
                          "year old who reads under the covers. Every pick is available on Amazon.",
                     covers=["B0H4CCMSQS", "B0H7W7VY7S", "B0H483NLCV", "B0H7QFWVXG"],
                     next=("Open the gift guide", "/gifts/")),
        gifts=dict(title="Book Gift Ideas for Every Reader | Carrier Press",
                   h1="A book for everyone on your list",
                   intro="Mysteries to read by the fire, cosmic horror for the friend who likes "
                         "to be unsettled, adventures for young readers, and classics in new "
                         "editions. Every book here is available on Amazon.")),
}
# Seasons that are about giving: their feature card and their /gifts/ covers are
# wrapped and tied with a bow (styles.css lists the same keys).
GIFT_SEASONS = ("valentines", "mothers", "fathers", "holiday")


def season_on(day):
    """The key of the season `day` falls in, or None between seasons."""
    hits = [k for k, v in SEASONS.items()
            for y in (day.year - 1, day.year)
            if v["when"](y)[0] <= day < v["when"](y)[1]]
    if len(hits) > 1:
        raise SystemExit(f"home_data: seasons overlap on {day}: {hits}")
    return hits[0] if hits else None


_force = os.environ.get("CP_SEASON")
SEASON_KEY = (None if _force == "none" else _force) if _force else season_on(_D.today())
if SEASON_KEY is not None and SEASON_KEY not in SEASONS:
    raise SystemExit(f"home_data: unknown season {SEASON_KEY!r}")
SEASON = SEASONS.get(SEASON_KEY)

# The regular first screen, between seasons.
HERO = dict(
    kicker="Carrier Press",
    h1="The secrets families keep, and the people who decide to <em>read them</em>.",
    sub="Mystery, cosmic horror, adventures for young readers and restored classics. "
        "Read them in print, or hear them performed in Cast, a voice for every character.",
    primary=("Pull a thread", "#threads"),
    secondary=("Browse every book", "/catalog/"),
)

# The threads, in order, after the season's feature card when a season is on.
#   kind   "book" | "app"
#   a      book threads: the catalogue ASIN the card is about
#   slug   app threads: the apps_data slug
#   eyebrow    the small label above the title
#   seasonal   {season key: eyebrow} while that season is on
#   title  optional; defaults to the book title or app name
#   line   the hook, one or two sentences
#   next   (label, href) the onward link: where this thread leads after the buy
THREADS = [
    dict(kind="book", a="B0H7W7VY7S",
         eyebrow="Our best selling title",
         seasonal=dict(holiday="For the horror fan", fathers="For the horror fan",
                       october="Start the season here"),
         line="A forbidden play, the Yellow Sign and the lost city of Carcosa. Lovecraft built "
              "on this book, and a century later True Detective sent a new generation looking for it.",
         next=("Follow the sign: the weird fiction line", "/weird-fiction/")),
    dict(kind="book", a="B0GZCKYKZ9", title="The Marjorie Corey Files",
         eyebrow="Start a series",
         seasonal=dict(holiday="For the mystery reader", mothers="For the mystery lover",
                       valentines="To read together", summer="For the beach"),
         line="Three women inherit a coffee shop and sixty years of what the town agreed not to "
              "say. Book one is The Second Shooter.",
         next=("Or give all five in one volume", "book:B0H4CCMSQS")),
    dict(kind="app", slug="cancelled",
         eyebrow="Before the next statement",
         seasonal=dict(holiday="Before the January statements",
                       school="Before the school year bills"),
         title="Find every subscription you forgot",
         line="Canceled reads a bank statement on your own device, ranks every recurring charge "
              "by what it costs a year, and shows you where to cancel. One payment, never a subscription.",
         next=("See how it works", "/cancelled/")),
    # Cast replaced Downpour here (author 2026-11-21). Canceled stays through the
    # January statements; from 7 January 2027 the proposal puts The Starlight
    # Secret Society (B0H483NLCV, then Book 2 B0HN3HJJBR) in Canceled's place.
    dict(kind="app", slug="cast",
         eyebrow="Hear the books",
         seasonal=dict(holiday="For the listener on your list",
                       summer="For the long drive"),
         title="Every character, in their own voice",
         line="Cast performs a book the way a full cast would: a narrator, and a separate voice "
              "for each character, the same every time you come back. It plays in your browser today.",
         next=("Meet Cast", "https://carrierlabs.org/")),
]

# /gifts/. One shelf per kind of reader, cards from catalog.json via book_card(),
# so every gift has its print price and its Buy on Amazon button. An entry is an
# ASIN, or (ASIN, title) where the shelf title is ambiguous out of its series.
# A gift season may replace the title, heading, intro and shelves (its `gifts`).
GIFTS_TITLE = "Book Gift Ideas for Every Reader | Carrier Press"
GIFTS_H1 = "A book for everyone on your list"
GIFTS_INTRO = ("Mysteries to read in one sitting, cosmic horror for the friend who likes to be "
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
