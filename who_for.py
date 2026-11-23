"""
"Who it's for" cards on each app's page (author 2026-11-21, "Yes, add cards").

These are NOT reviews and must never read like one: no names, no quotation
marks, no stars, no first person, no "customers say". Each card is a kind of
buyer in the third person and what the app does for them, and every claim in
it must be true of the app as it ships on the web (checked against its row in
apps_data.py and its key page). The author asked for simulated reviews; they
were declined because invented reviews break the FTC's fake-review rule even
with a disclaimer, and these cards were offered instead.

Rules: no em or en dashes, never "safe", no promised outcomes (no "save",
"never miss", "win"), no prices, no old or merged app names.
"""

CARDS = {
    "endorsed": [
        ("A driver going for a CDL", "Works through the practice tests between shifts, with the source named under every answer."),
        ("Someone adding an endorsement", "Studies just the HazMat, passenger or school bus section they need, not the whole manual again."),
        ("A career changer", "Compares what the drone, vessel captain and rail credentials ask of them before choosing one."),
    ],
    "boatready": [
        ("A new boat owner", "Finds out which gear federal rules require for their exact boat."),
        ("Someone heading out for the first trip of the season", "Checks the list at the dock, offline, with the CFR citation behind every line."),
        ("A buyer looking at a used boat", "Sees what the boat must carry before deciding what to budget for."),
    ],
    "whoserves": [
        ("A voter at a new address", "Sees every district and office that covers the new home on one screen."),
        ("Someone with a problem to raise", "Finds which official actually holds the office that handles it, from school board to Congress."),
        ("A person planning to vote", "Sees when each of those seats is next up for election."),
    ],
    "conceptionzodiac": [
        ("Someone curious about astrology", "Works out the sign overhead at their conception rather than their birth."),
        ("A friend choosing a gift", "Looks up the conception sign for a birthday, with nothing stored and no account."),
        ("A parent-to-be", "Plays with the dates for fun, knowing the birthday never leaves the device."),
    ],
    "cancelled": [
        ("Someone whose bank statement keeps growing", "Sees every recurring charge in one list, ranked by what it costs a year."),
        ("A person tidying up their money in January", "Finds the subscriptions they forgot and where to cancel each one."),
        ("Someone who wants it private", "Reads the statement on their own device, with nothing uploaded."),
    ],
    "downpour": [
        ("A game master running a campaign", "Brings rain onto the tavern roof or over the camp as the scene changes."),
        ("A table that notices loops", "Hears rain made live in the browser, so the same patch never repeats."),
        ("Someone building tension for a boss fight", "Lets the storm roll in right as the fight starts."),
    ],
    "quiet": [
        ("A private journaler", "Writes a personal record that never leaves the device, with no account and no sync."),
        ("Someone who distrusts the cloud", "Keeps notes where no code sends what they write anywhere."),
        ("A person working through something hard", "Has a place to write it down that stays on their own device."),
    ],
    "threshold": [
        ("A parent handing over a first phone", "Gets every control that applies to the child's age, in the order that matters."),
        ("A family with consoles, tablets and a laptop", "Sets them all up from one list, home internet included."),
        ("A parent of a teenager", "Finishes the setup with an agreement both of them say yes to."),
    ],
    "flare": [
        ("Someone living with a chronic condition", "Logs symptoms, sleep, stress and food, and sees what tends to happen together."),
        ("A person with a doctor's appointment coming up", "Prints a summary of the last month, and one page of medicines, allergies and results gathered from their own papers."),
        ("Someone on a GLP-1 medicine", "Keeps doses in the same log as everything else, in one place."),
    ],
    "soleledger": [
        ("A freelancer facing quarterly taxes", "Sees income, deductions and the quarterly estimate in one set of books."),
        ("Someone reconciling 1099s in January", "Checks each form against what was actually paid."),
        ("A small landlord", "Keeps each unit's income and costs in the Rentals section for Schedule E."),
    ],
    "papertrail": [
        ("A household with a drawer of receipts", "Turns receipts, warranties and policies into dates and facts they can find."),
        ("Someone who forgets renewals", "Puts each date to act on into their own calendar."),
        ("A homeowner getting ready to sell", "Has the house's equipment and service record ready to hand over."),
    ],
    "throughthegate": [
        ("A job seeker getting no replies", "Sees what a resume parser kept from their resume and what it threw away."),
        ("Someone rewriting a resume", "Tries each version to see which one a parser reads cleanly."),
        ("A person changing careers", "Checks that the skills they are leading with survive the parse."),
    ],
    "vetpocket": [
        ("A pet owner at 9pm on a Friday", "Gets help deciding between an emergency visit and calling the vet on Monday, with a cost range for each."),
        ("A household with more than one pet", "Keeps vaccinations, worming and flea dates for each one in one place."),
        ("Someone new to a dog or cat", "Puts each due date into their own calendar with a reminder a week before."),
    ],
    "thebinder": [
        ("Someone putting their affairs in order", "Writes down where the will is, which accounts exist and who to ring."),
        ("A parent thinking ahead", "Leaves the family one file instead of a search through drawers."),
        ("A person who wants it private", "Encrypts it with a passphrase only they know."),
    ],
    "firstday": [
        ("A parent buried in school emails", "Forwards them and gets back one calendar, one supply list and one form tracker."),
        ("A family with more than one school", "Sees the dates from every school email in one calendar."),
        ("Someone starting the new term", "Knows which forms are still to sign before the first day."),
    ],
    "cast": [
        ("A listener who loves audiobooks", "Presses Play and hears a narrator and a voice for every character."),
        ("Someone browsing for the next book", "Hears the opening of any book on the shelf before buying."),
        ("A reader with their own EPUB files", "Adds them and has those performed too."),
    ],
    "tradedesk": [
        ("A one-person trade business", "Runs each job, scope and change order from the van, with gloves on."),
        ("An electrician on site", "Gets code answers that carry the article number."),
        ("Someone who hates paperwork", "Keeps the admin on each job under a minute."),
    ],
    "pantry": [
        ("A household watching the food budget", "Plans meals from what is already in the house, starting with what expires first."),
        ("Someone tired of buying for one recipe", "Gets ideas that use what is on the shelf, not a new shopping list."),
        ("A family after the holidays", "Plans the week around the leftovers first."),
    ],
    "fluenthour": [
        ("Someone learning a language for travel", "Speaks through one everyday scenario a day, in about ten minutes."),
        ("A learner who quit apps with streaks", "Practises with no lessons, no streaks and no gems."),
        ("A person with a New Year's resolution", "Keeps it to one short spoken session a day."),
    ],
    "homeroom": [
        ("A homeschooling parent", "Sees what their own state asks for and records the year against it."),
        ("A family new to homeschooling", "Reads each state rule with its citation and the date it was last checked."),
        ("A parent at the end of the year", "Has the portfolio assembled as the year went, ready to download."),
    ],
    "stuck": [
        ("A parent helping with homework", "Hands over a tutor that asks questions instead of giving the answer."),
        ("A student stuck on one problem", "Gets nudged toward the next step, one question at a time."),
        ("A parent who wants to see the help", "Reads the whole conversation afterwards."),
    ],
    "pillproof": [
        ("An adult child looking after a parent", "Marks each dose taken or skipped, with the time and who marked it."),
        ("A carer sharing the load with siblings", "Gives the family a printable summary of the doses that were taken."),
        ("A household juggling appointments", "Keeps appointments and updates in the same log, saying who is doing what."),
    ],
    "handoff": [
        ("Two parents living apart", "Share one record of the arrangement, kept by neither of them, with messages neither can edit or delete."),
        ("A parent tracking shared costs", "Logs each expense with the share asked of the other parent and the answer."),
        ("Someone who needs the record for a period", "Exports it, with a plain statement of what the export does and does not prove."),
    ],
    "crosscheck": [
        ("A patient with an ER bill bigger than expected", "Types in the bill and the insurer's statement and sees every place they disagree."),
        ("Someone who suspects a double charge", "Sees the same line charged twice, with the figures from each document."),
        ("A person ready to ask questions", "Drafts letters to the billing office and the insurer, and sends them themselves."),
    ],
    # Spellbright (2026-11-22): checked against app/index.tsx, app/silly.tsx,
    # lib/ages.ts (the youngest player's band sets the shared board),
    # app/practice.tsx (look, cover, spell, check) and lib/crossword.ts
    # showsPoints (stars at 4 to 5). No outcomes promised.
    "spellbright": [
        ("A parent of a new reader", "Hands over picture clues that are read aloud, with stars instead of points at ages 4 and 5."),
        ("A family around one screen", "Plays the tile board or Silly Sentences together on one device, with the youngest player's age setting the words."),
        ("A grown-up with this week's spelling list", "Types in the words from school, then the child practises them by look, cover, spell, check and meets them again in the games."),
    ],
}


def cards(slug):
    return CARDS.get(slug, [])
