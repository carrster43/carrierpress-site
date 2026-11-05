"""The weird fiction and cosmic horror hub, /weird-fiction/: its copy and its titles.

ONE SOURCE, TWO READERS. build.py renders the hub from this module and books.py
renders the "Read next in weird fiction" block on each title's own page from the
same NEXT table, so the hub and the cross-sell can never name different books.
Nothing here is imported from build.py or books.py (they import this), which is
what keeps the three from becoming circular.

THE COPY IS WRITTEN FROM THE CATALOGUE. Card lines are built from what each
edition's own `adds` list in catalog.json says it contains, plus well known
dates of first publication. Where the catalogue already carries an editorial line
for a title (bestseller.connected), that line is reused verbatim. A title gets no
claim here that its catalogue record does not support.

HOUSE RULES, enforced by build.py before the page is written: no em or en dash, no
"best seller" wording, no mention of how the editions were made beyond what the
catalogue states. The hub makes NO sales claim: it says "our most-read title" at
most, never a ranking or a unit count.
"""

SLUG = "weird-fiction"
KIY = "B0H7W7VY7S"          # The King in Yellow, the hub's lead
CARCOSA = "B0HGG934BB"

TITLE = "Classic Weird Fiction and Cosmic Horror Books | Carrier Press"
H1 = "Classic weird fiction and cosmic horror, restored"
DESC = ("Start with The King in Yellow, then Carcosa. Annotated editions of Chambers, "
        "Machen, Blackwood, M. R. James, Radcliffe and more, in paperback, hardcover and Kindle.")
EYEBROW = "Weird fiction and cosmic horror"

INTRO = [
    "Weird fiction is the horror of the thing you cannot quite see. The shelf below is where "
    "that tradition was built: a play that ruins its readers, a city that should not exist, "
    "an island that has noticed two campers. Most of these books are over a century old and "
    "still do their work in a few quiet pages.",
    "Start with The King in Yellow, Robert W. Chambers's 1895 book of linked tales and the "
    "most-read title in the Carrier Press catalogue. Lovecraft built on it, and the Yellow "
    "Sign and Carcosa reached a new audience when True Detective went looking for them. "
    "Every edition here is newly set and annotated, with an introduction, headnotes and a "
    "glossary, so the old language and the old references stop being a barrier.",
]

# The lead block, King in Yellow. Written for this page; the homepage band has its own.
LEAD = ("A play that ruins everyone who reads it sits at the centre of the first four tales, "
        "and Chambers never lets you read it. You only meet its readers afterwards. That "
        "restraint is why the book is still frightening, and why a century of writers kept "
        "returning to the Yellow Sign and to Carcosa.")

# Reading order: the three steps the hub promises. Each is (asin, why).
ORDER = [
    (KIY, "The book itself. Read it first."),
    (CARCOSA, "Where the names came from: Bierce's Carcosa tales beside Chambers's Yellow Sign tales."),
    ("B0HGS6TH57", "Chambers back in weird country, two years later."),
    ("B0HGMSMFQK", "Machen: the British weird tale at full strength."),
    ("B0HGTD7VBZ", "Blackwood: a place that has noticed you."),
    ("B0HH3CJRRW", "M. R. James: the scholar's ghost story."),
    ("B0H2Y3TMMC", "Meyrink: a dream of Prague, new in English."),
]

# Shelves: (heading, intro, [asins]). The King in Yellow is the lead above and is
# not repeated. The Yellow Sign shelf opens with Carcosa because that is step two.
SHELVES = [
    ("The Yellow Sign",
     "Chambers and the stories he borrowed from, gathered so the borrowing reads as a sequence.",
     [CARCOSA, "B0HQCG586W", "B0HGS6TH57"]),
    ("Lovecraft and where he got it",
     "Six Lovecraft stories, with every borrowed name followed back to its source.",
     ["B0HQ55DVX2"]),
    ("The British weird tale",
     "Machen, Blackwood and M. R. James, with the Prague of Meyrink's Golem for company.",
     ["B0HGMSMFQK", "B0HL27ZXPJ", "B0HGTD7VBZ", "B0HH3CJRRW", "B0HL24L2L3", "B0H2Y3TMMC"]),
    ("Gothic roots and dark pulp",
     "The castles, cloisters and Fleet Street cellars the weird tradition grew out of.",
     ["B0H7QPDD4S", "B0H7PDG821", "B0H7R61S7C", "B0H7R7Y1N4", "B0H7LYK2QQ"]),
]

# The card line for each title. Carcosa, Mystery of Choice, Pan and Willows reuse the
# catalogue's own bestseller.connected lines at build time (see build.py); every other
# line is below, each traceable to that edition's `adds` list.
LINES = {
    "B0HQ55DVX2": ("Six Lovecraft stories, from The Picture in the House to The Dunwich Horror, "
                   "each from its first magazine printing. A headnote for each, and 41 notes "
                   "tracing his borrowed names back to Bierce, Chambers, Machen, Blackwood and Lamb."),
    "B0HQCG586W": ("Where Carcosa began: Bierce's own collection of 24 stories, in the order he "
                   "placed them, with An Inhabitant of Carcosa and Ha\u00efta the Shepherd. A headnote "
                   "before every story, and a comparison showing 17 readings he changed."),
    "B0HL27ZXPJ": ("Machen's linked tales of three impostors and the people who cross their path, "
                   "with the horror kept at the edge of the telling. This edition has a headnote "
                   "for each of the 14 sections, and Machen's own comments on the book."),
    "B0HH3CJRRW": ("M. R. James's complete 1904 collection: eight scholar's ghost stories where "
                   "the dread arrives through something ordinary. A headnote for each story, "
                   "and Lovecraft's essay on James."),
    "B0HL24L2L3": ("The second and third James collections, More Ghost Stories and A Thin Ghost, "
                   "in one volume of twelve stories, with a headnote for each."),
    "B0H2Y3TMMC": ("Meyrink's 1915 novel of a dreamlike Prague ghetto, in a new, complete English "
                   "translation. A glossary of about 33 entries, and the 1847 Golem legend newly "
                   "translated as an appendix."),
    "B0H7QPDD4S": ("Radcliffe's 1794 gothic novel: a young woman, a castle in the Apennines, and "
                   "terrors that turn out to have causes. Austen mocked it in Northanger Abbey, "
                   "and the notes here say why it still matters."),
    "B0H7PDG821": ("Lewis's 1796 gothic shocker: a celebrated preacher, a temptation and a bargain "
                   "that goes wrong, with the Bleeding Nun and the Inquisition along the way."),
    "B0H7R61S7C": ("The penny dreadful that gave Fleet Street its demon barber. Volume One opens "
                   "with an introduction on who wrote it, the penny dreadful trade and whether "
                   "Todd was real."),
    "B0H7R7Y1N4": ("Volume Two finishes the tale, with notes on Fleet Street, penny dreadfuls and "
                   "Newgate, a Sweeney Todd timeline from the 1830s to today, and ten questions."),
    "B0H7LYK2QQ": ("Norbert Jacques's master criminal, in a new translation from the German. The "
                   "introduction covers Jacques, his Berlin and Fritz Lang's films, with a note "
                   "on the title, the names and the card game."),
}

# What "Read next in weird fiction" shows on each title's own page: four ASINs, the
# nearest books on this shelf first. Every key is a hub title.
KIY_SEQ = [CARCOSA, "B0HGS6TH57", "B0HGMSMFQK", "B0HGTD7VBZ"]
NEXT = {
    KIY: KIY_SEQ,
    CARCOSA: [KIY, "B0HGS6TH57", "B0HGTD7VBZ", "B0HGMSMFQK"],
    "B0HQCG586W": [KIY, CARCOSA, "B0HGS6TH57", "B0HGMSMFQK"],
    "B0HQ55DVX2": [CARCOSA, KIY, "B0HGMSMFQK", "B0HGTD7VBZ"],
    "B0HGS6TH57": [KIY, CARCOSA, "B0HGMSMFQK", "B0HGTD7VBZ"],
    "B0HGMSMFQK": [KIY, "B0HL27ZXPJ", "B0HGTD7VBZ", "B0HH3CJRRW"],
    "B0HL27ZXPJ": [KIY, "B0HGMSMFQK", "B0HGTD7VBZ", "B0HH3CJRRW"],
    "B0HGTD7VBZ": [KIY, "B0HGMSMFQK", "B0HH3CJRRW", CARCOSA],
    "B0HH3CJRRW": ["B0HL24L2L3", KIY, "B0HGTD7VBZ", "B0HGMSMFQK"],
    "B0HL24L2L3": ["B0HH3CJRRW", KIY, "B0HGTD7VBZ", "B0HGMSMFQK"],
    "B0H2Y3TMMC": [KIY, "B0HGMSMFQK", "B0HGTD7VBZ", "B0H7LYK2QQ"],
    "B0H7QPDD4S": ["B0H7PDG821", KIY, "B0H7R61S7C", "B0HH3CJRRW"],
    "B0H7PDG821": ["B0H7QPDD4S", KIY, "B0H7R61S7C", "B0HH3CJRRW"],
    "B0H7R61S7C": ["B0H7R7Y1N4", "B0H7PDG821", "B0H7QPDD4S", KIY],
    "B0H7R7Y1N4": ["B0H7R61S7C", "B0H7PDG821", "B0H7QPDD4S", KIY],
    "B0H7LYK2QQ": [KIY, "B0H2Y3TMMC", "B0H7R61S7C", "B0H7PDG821"],
}

NEXT_HEADING = "Read next in weird fiction"
HUB_LINK_TEXT = "All classic weird fiction and cosmic horror from Carrier Press"

# Visible FAQ and the FAQPage markup read from this one list. Answers that quote a
# price or a format are filled from formats.json at build time ({kiy_prices}).
FAQ = [
    ("Where should I start with cosmic horror classics?",
     "Start with The King in Yellow, then read Carcosa, which gathers the Bierce tales Chambers "
     "borrowed his names from beside his own Yellow Sign tales. After those, the shelf runs "
     "through Chambers's The Mystery of Choice, Machen's The Great God Pan, Blackwood's The "
     "Willows, M. R. James's ghost stories and Meyrink's The Golem."),
    ("What is in the Carrier Press edition of The King in Yellow?",
     "It is an annotated edition of Robert W. Chambers's book. It has an Introduction with a map "
     "of how to read the collection, headnotes for the stories, a glossary of the Yellow Mythos "
     "with 17 entries, and 11 new illustrations. {kiy_prices}"),
    ("What is Carcosa, and where does it come from?",
     "Carcosa is the lost city at the heart of The King in Yellow. Chambers took the name, and "
     "Hali, from Ambrose Bierce's tales. The Carrier Press Carcosa gathers seven Bierce and Chambers "
     "pieces in publication order, with a dated headnote for each piece and Lovecraft's essay "
     "on Bierce and Chambers reprinted."),
    ("Are these editions just the free public domain texts?",
     "No. The works are in the public domain, but each edition here is newly set with its own "
     "cover and new apparatus written for it, such as an introduction, headnotes, a glossary "
     "and notes. The page for each title lists what that edition adds."),
]
