#!/usr/bin/env python3
"""
One row per app. The single source of truth for /apps/.

WHY A DATA FILE AND NOT A HAND-WRITTEN PAGE. /labs/ is hand-written and that was
right for it: it is a build log, forty lines of prose, edited when the prose
changes. /apps/ is forty-four rows of the same six fields, and every one of those
fields goes stale on its own schedule -- a price, a store link, a status. Hand
written, the page drifts silently and nothing in the build says so. The support
and privacy pages already settled this argument the same way.

STATUS IS THE FIELD THAT MATTERS AND IT IS MEASURED, NOT ASPIRED TO.

    live     on the App Store, buyable today            -> store link
    browser  runs in a browser right now, no download   -> direct link
    soon     finished software, not yet on a store      -> "coming soon"
    build    real repo, a named thing still missing     -> "coming soon"
    design   specified in full, not started             -> "in design"

*** AS OF 2026-09-20 NOTHING IS `live`. ***  That is deliberate and it is the
honest state: the closest app, Home Rule, still needs an age rating, one paywall
screenshot per subscription, and Submit. A page that showed Buy buttons today
would be selling something nobody can buy. The moment an app ships, flip its
status to "live" and fill `store`, and the page changes with it.

PLAN SHAPES

    sub     free tier, 14-day trial, then monthly or yearly
    once    free forever for the core job, one payment unlocks the rest
    b2b     sold to an institution; no self-serve price
    none    in design, no price yet

>>> THE FREE TIER CAPS BELOW ARE DEFAULTS, NOT DECISIONS. <<<
`free` is the single field that decides whether the free tier is a fair trial of
the product or a demo that annoys people into leaving. It is a judgment about
each app's own shape -- a symptom log needs weeks before it can show you
anything, a resume parser is useful on the first document -- and it is yours to
set. See free_tier_rule() at the foot of this file.
"""

# number, slug, name, blurb, status, shape, price, free, note
APPS = [

    # ---- No backend, no account, no running cost. The fastest to a store. ----
    dict(n=43, slug="boatready", name="Boat Ready",
         blurb="Federal carriage requirements for your exact boat, answered offline, with the CFR citation and the manual page behind every line.",
         status="soon", shape="once", price="$6.99 once",
         free="Checking a boat is free, now and always. Unlimited boats, unlimited checks, no account.",
         note="The purchase saves the boats you look after and lets you tick items off as you go. That is all it buys. It is one payment, not a subscription."),

    dict(n=44, slug="nightwatch", name="Night Watch",
         blurb="Identify a vessel by the lights or day shape you can actually see, with the Rule number behind every answer.",
         status="soon", shape="once", price="$6.99 once",
         free="Identifying lights is free, now and always. Every light, every day shape, no account.",
         note="The purchase opens Practice mode, which drills every signature until you know them without a phone in your hand."),

    dict(n=45, slug="channelmarks", name="Channel Marks",
         blurb="What a US buoy or beacon is telling you, and which side to pass it, with the handbook paragraph attached.",
         status="soon", shape="once", price="$6.99 once",
         free="Reading the marks is free, now and always. No account, no signal needed.",
         note="The purchase opens Practice mode, which drills every mark in both directions until you know it cold. One payment, not a subscription."),

    dict(n=41, slug="conceptionzodiac", name="Conception Zodiac",
         blurb="The sign overhead at conception rather than at birth. A pure calculation, with no account, no database and no network call.",
         status="build", shape="once", price="$2.99 once", free_label="Try it",
         free="Enter any birthday and see how many conception signs it could be.",
         note="The purchase shows which sign, the others it could be, and the weeks that settle it, and keeps people by name so a family is one tap each. The list never leaves the phone. One payment, not a subscription."),

    # Downpour, added 2026-09-25. Price deliberately empty: his call when the
    # in-app purchase is created. Trial/unlock split from Downpour mobile/lib/access.ts (09-25).
    dict(n=36, slug="downpour", name="Downpour",
         blurb="Rain for sleep, built live on your phone drop by drop instead of played from a recording, so there is no loop to notice at 3am. Five surfaces, a sleep timer that fades out, no signal needed.",
         status="soon", shape="once", price="", free_label="Try it",
         free="Listen to the Tent for ten minutes at a time, as often as you like, and hear for yourself that it never loops.",
         note="The purchase opens everything: all five surfaces, Slower and Lower, the sleep timer, and rain that plays until you stop it. One payment, not a subscription, and nothing about you leaves the phone."),

    # ---- Runs in a browser today ----
    dict(n=31, slug="planfinder", name="Plan Finder",
         blurb="Guided Medicare Advantage comparison that compares on the whole picture, including whether a plan covers the drugs somebody already takes. No enrollment, no commission, no TPMO status.",
         status="browser", shape="b2b", price="Licensed to agencies",
         free="The sample comparison is open to anyone, with no account and no email address.",
         note="Sample data is invented on purpose. Carriers, plans and coverage are fictional, so a demo can never misdescribe a real product.",
         link="https://carrster43.github.io/planfinder-web/sample", link_label="Open the sample comparison"),

    dict(n=14, slug="throughthegate", name="Through the Gate",
         blurb="Shows the structured record a resume parser actually keeps, and, more to the point, everything it threw away.",
         status="build", shape="sub", price="$19/mo",
         free="One resume, parsed in full, free. You see the whole record before you decide anything.",
         note="Priced by the month because a job search ends. Most people need it for about three."),

    # ---- Finished software, listing staged, not yet submitted ----
    dict(n=42, slug="homerule", name="Home Rule",
         blurb="Everyone who governs your address, on one screen: the districts, the offices, the names, and when each of them is next up for election.",
         status="soon", shape="sub", price="$5.99/mo or $39.99/yr",
         free="Look up any address, free, as often as you like. The offices and the names are the free tier.",
         note="The subscription saves addresses, watches them for redistricting, and adds the election calendar."),

    dict(n=1, slug="flare", name="Flare",
         blurb="Symptom log for PCOS, endometriosis, fibromyalgia and autoimmune conditions. Finds co-occurrence across entries and prints a summary for the doctor.",
         status="soon", shape="sub", price="$7.99/mo or $59.99/yr",
         free="Log freely for 30 days and keep logging after. One doctor summary, free.",
         note="Flare finds patterns across what you record. It does not diagnose, explain or treat anything, and it is not a medical device."),

    dict(n=10, slug="soleledger", name="Books for One",
         blurb="A freelancer tax engine. Income, deductions, quarterly estimates, 1099 reconciliation. Nothing else.",
         status="soon", shape="sub", price="$14.99/mo or $119.99/yr",
         free="Track income and expenses for one quarter, free. The ledger is yours either way.",
         note="It never applies a tax rule to you. You enter your own annual target and it does the arithmetic."),

    dict(n=39, slug="porchlight", name="Porchlight",
         blurb="The opt-in map of which houses are giving out candy on the night. Forked from Potluck, and the only thing here with a date it cannot negotiate.",
         status="build", shape="once", price="Free to trick-or-treat",
         free="The map is free for everyone walking the street. It always will be.",
         note="Targeted at Halloween 2027. The revenue is the organizer side, not the map."),

    # ---- Built, ranked by the demand model ----
    dict(n=2, slug="titrate", name="Titrate",
         blurb="A GLP-1 companion. Side effects plotted against dose, protein targets, plateau interpretation, and when to stop reading a phone and call somebody.",
         status="build", shape="sub", price="$14.99/mo or $119.99/yr",
         free="Log doses and side effects free, indefinitely. The chart that puts them together is the paid part.",
         note="It organises what you record against your own dose history. It does not advise on dosing."),

    dict(n=12, slug="doorstop", name="Doorstop",
         blurb="The one to six unit landlord's ledger, ending in a clean Schedule E.",
         status="build", shape="sub", price="$7.99/mo per unit",
         free="One unit, one full year, free. Enough to see whether the Schedule E comes out right.",
         note="It never applies a tax rule. It checks rather than assumes."),

    dict(n=29, slug="papertrail", name="Paper Trail",
         blurb="Receipts, warranties and policies photographed into structured facts, with an alert before something lapses.",
         status="build", shape="sub", price="$6.99/mo or $54.99/yr",
         free="Twenty documents, free, kept forever. Alerts on all of them.",
         note="The paid tier is unlimited documents and the search across them."),

    dict(n=4, slug="vetpocket", name="Vet Pocket",
         blurb="Pet records, plus an answer to whether this is an emergency visit or it can wait until Monday, with a cost range attached to each path.",
         status="build", shape="sub", price="$4.99/mo or $39.99/yr",
         free="One animal, complete records, free forever.",
         note="The triage answer is a range of what the visit tends to cost, not a diagnosis."),

    dict(n=3, slug="perimeter", name="Perimeter",
         blurb="Thirty-seven perimenopause symptoms, including the ones nobody connects to it. Produces a script for the GP appointment.",
         status="build", shape="sub", price="$9.99/mo or $79.99/yr",
         free="The full symptom list and one appointment script, free.",
         note="It organises what you tell it into something you can say out loud in ten minutes."),

    dict(n=23, slug="threshold", name="Threshold",
         blurb="Every parental control across phone, console, tablet and ten apps, for one child's age, configured in one sitting.",
         status="build", shape="once", price="$28.99 per child",
         free="See the whole checklist for your child's age before you pay for anything.",
         note="One payment per child, never a subscription. The job is done in an afternoon and should not bill monthly for the rest of the year."),

    dict(n=9, slug="firstday", name="FirstDay",
         blurb="Forward the school emails and PDFs. Get back one calendar, one supply list and one form tracker.",
         status="build", shape="sub", price="$6.99/mo",
         free="One child, one term, free.",
         note="Seasonal by nature. Most families need it in August and again in January."),

    dict(n=5, slug="pillproof", name="PillProof",
         blurb="Senior-first medication adherence. Confirm a dose by photographing the pill. Billed to the adult child, not the patient.",
         status="build", shape="sub", price="$8.99/mo",
         free="Three medications, free, with reminders.",
         note="Photo confirmation is not wired yet, and that is the part most people would be relying on. It is not being sold until it is."),

    dict(n=7, slug="thebinder", name="The Binder",
         blurb="The if-something-happens file, with staged release to named people on verified death.",
         status="build", shape="once", price="$99 once, then $29/yr",
         free="Build the whole vault and the whole checklist, free. You only pay to name the people it releases to.",
         note="v1 is the vault and the checklist. Staged release is deferred to v1.1 by design, and that is the reason it is not for sale yet."),

    dict(n=17, slug="stuck", name="Stuck",
         blurb="Homework help that is Socratic by architecture and structurally cannot output the answer. Parents can read the whole transcript.",
         status="build", shape="sub", price="$11.99/mo",
         free="Five sessions a month, free, with the full transcript.",
         note="It cannot give an answer. That is not a policy, it is how it is built."),

    dict(n=15, slug="scope", name="Scope",
         blurb="Quote to signed statement of work to change order, for solo service providers. Makes raising a change order unemotional.",
         status="build", shape="sub", price="$24.99/mo",
         free="Three documents a month, free, fully signable.",
         note=""),

    dict(n=28, slug="errand", name="Errand",
         blurb="Researches, drafts, fills the form, and stops at the confirm button. Assistive, not autonomous.",
         status="build", shape="sub", price="$24.99/mo",
         free="Five errands a month, free.",
         note="It stops at the confirm button. Every time, on purpose."),

    dict(n=30, slug="quiet", name="Quiet",
         blurb="The personal record that never leaves the device. No account, no sync, and no network permission in the default build.",
         status="soon", shape="once", price="$78.99 once", free_label="Try it",
         free="Your first 10 entries. Search, export and delete keep working after that, so nothing you wrote is ever held back.",
         note="The purchase removes the limit for good. There is no server to pay for, so there is nothing to bill you monthly for: your journal lives in a database on your phone and nowhere else."),

    dict(n=26, slug="houseledger", name="House Ledger",
         blurb="The home's service record: systems, ages, warranties, contractors. Built so it hands over cleanly at sale.",
         status="build", shape="sub", price="$48.99/yr",
         free="Ten records, free, kept forever.",
         note=""),

    dict(n=27, slug="pantry", name="Pantry",
         blurb="Inverts the meal planner. Starts from what is already in the house and what expires first, rather than from a recipe you have to shop for.",
         status="build", shape="sub", price="$5.99/mo",
         free="The whole pantry and the expiry order, free. Always.",
         note=""),

    dict(n=20, slug="thirdplace", name="Third Place",
         blurb="Recurring low-commitment gatherings. One tap to say you are coming, and an honest count of who actually turns up regularly. Explicitly not dating.",
         status="build", shape="sub", price="$11.99/mo per host",
         free="Free for everyone attending, forever. Only the host pays.",
         note=""),

    dict(n=21, slug="potluck", name="Potluck",
         blurb="Neighbourhood organising and lending, geofenced to a few blocks, address verified without storing an address. Two verbs: organise a thing, lend a thing.",
         status="build", shape="b2b", price="Free to neighbours",
         free="Free for every neighbour, permanently. Moderation shipped in the first migration, not bolted on later.",
         note="Sold to the association or the city, never to the street."),

    dict(n=19, slug="fluenthour", name="Fluent Hour",
         blurb="One spoken scenario a day, ten minutes. No lessons, no streaks, no gems, no owl.",
         status="build", shape="sub", price="$17.99/mo",
         free="Seven scenarios, free. One a day, same as the paid tier.",
         note=""),

    dict(n=6, slug="relay", name="Relay",
         blurb="A shared care record that replaces the seven-sibling group chat with a typed update feed, so nobody has to scroll to find out what happened.",
         status="build", shape="sub", price="$19.99/mo per household",
         free="Three people, free. Enough to find out whether the family will actually use it.",
         note=""),

    dict(n=8, slug="handoff", name="Handoff",
         blurb="Co-parenting calendar, expense splits, and a message log that exports in a form a court will accept.",
         status="build", shape="sub", price="$11.99/mo each",
         free="The message log is free and stays free. Export is the paid part.",
         note="The calendar interface is missing. The log underneath it is built and verified against a live database."),

    dict(n=16, slug="tradedesk", name="Trade Desk",
         blurb="Field service for one person with a van. Under sixty seconds of admin per job, usable with gloves on. Offline first.",
         status="build", shape="sub", price="$38.99/mo",
         free="Ten jobs, free, with invoicing.",
         note=""),

    dict(n=13, slug="cancelled", name="Canceled",
         blurb="Finds every recurring charge in your bank statement, on your phone, ranks them by what they cost you a year, and shows you where to cancel. One payment, never a subscription, which would rather defeat the point.",
         status="build", shape="once", price="$38.99 once", free_label="Try it",
         free="Open a statement and see every recurring charge and what each costs you a year, plus where to cancel the most expensive one. The unlock shows where to cancel the rest.",
         note="It does not connect to your bank, and that is a deliberate limit rather than a missing feature."),

    dict(n=18, slug="homeroom", name="Homeroom",
         blurb="Homeschool compliance measured against the family's own state rules, assembling the portfolio as the year goes.",
         status="build", shape="sub", price="$98.99/yr",
         free="Build the portfolio free. The compliance assertion is the paid part.",
         note="Waiting on legal review of the per-state rule set. The assertion is the product, so there is no version of this that ships without it."),

    dict(n=24, slug="signalcheck", name="Signal Check",
         blurb="Teen wellbeing the teen agreed to. Consent-first, with autonomy earned back on a visible schedule.",
         status="build", shape="sub", price="$9.99/mo",
         free="The consent agreement and the schedule are free to set up and read.",
         note="Waiting on a COPPA review it is not going to skip."),

    dict(n=22, slug="waitlist", name="Waitlist",
         blurb="Structured self-guided CBT and a fortnightly symptom check, for the months between a referral and a first appointment.",
         status="build", shape="b2b", price="Licensed to clinics",
         free="Free to every person using it. The clinic or the university pays.",
         note="Waiting on the licensed instrument text."),

    dict(n=25, slug="permitpath", name="Permit Path",
         blurb="Per-jurisdiction permit checklists, department by department tracking, and a timeline built from what actually happened rather than what was promised.",
         status="build", shape="b2b", price="$48.99 per application",
         free="The checklist for your jurisdiction is free to read before you file anything.",
         note="The engine is generic. Each jurisdiction has to be researched and loaded one at a time."),

    dict(n=33, slug="gedcompletion", name="GED Completion",
         blurb="A completion engine, not a question bank. Diagnostic-first, no streaks, with a caseworker dashboard. Aimed at the roughly forty percent who start testing and never finish.",
         status="build", shape="b2b", price="Contract-priced",
         free="Free to every student. The board, the facility or the employer pays.",
         note="Waiting on the question bank."),

    dict(n=11, slug="crosscheck", name="Crosscheck",
         blurb="Photograph the hospital bill and the explanation of benefits. Get itemised error detection and an appeal letter that cites its own reasoning.",
         status="build", shape="once", price="$24.99 per case",
         free="The error detection is free. You pay only when there is something to appeal.",
         note="Held on regulatory grounds, and it will stay held until that is answered properly."),

    # ---- Specified in full, not started ----
    dict(n=32, slug=None, name="Carrier Press",
         blurb="The business of being an author: query to agent match to submission to rights to direct-to-reader, in one place that knows what was sent where and when.",
         status="design", shape="sub", price="$29-79/mo", free="", note=""),

    dict(n=40, slug=None, name="Carry",
         blurb="One dated timeline of conditions, medications, labs and who said what when, extracted from portals and paper.",
         status="design", shape="sub", price="", free="",
         note="It will organise. It will never interpret."),

    dict(n=35, slug=None, name="Throughline",
         blurb="The decision and commitment log for projects that are not software, assembling the weekly stakeholder update as it goes.",
         status="design", shape="sub", price="", free="", note=""),

    dict(n=38, slug=None, name="AI Integrator",
         blurb="The connection layer between an assistant and the tools that already hold the work: auth, scopes, a capability catalog, and an audit log of every action taken and on whose authority.",
         status="design", shape="b2b", price="$99-499/mo", free="", note=""),

    dict(n=37, slug="cast", name="Cast",
         blurb="A book performed with a voice per character and a score under the action. The reading is analysed once per title, offline; the performance happens on your device.",
         status="soon", shape="once", price="$19.99 once",
         free="The opening of every title, free, in full cast: in most books the first chapter or two. Not a clip and not a countdown.",
         note="All 48 books are in the app, 34 of them performed by a full cast and 14 by a single voice, and the shelf shows which is which. One payment opens every book. It creates no audiobook edition, which is what keeps the free Audible route open on every title.",
         link="/audio/", link_label="See the catalogue and what it costs"),

    dict(n=34, slug=None, name="Rough-In",
         blurb="The code answer for electricians with the article number attached, refusing to answer when it cannot cite one.",
         status="design", shape="sub", price="", free="", note=""),
]


def free_tier_rule(app):
    """
    >>> YOURS TO SET. This function is the free tier, and the free tier is the
    >>> whole funnel: it is the only thing anybody experiences before deciding.

    Right now every cap lives in the `free` string on each row above, written
    per app, because the apps are not alike -- Flare needs weeks of entries
    before it can show anybody anything, while Through the Gate is useful on the
    first document. A single global rule would be wrong for one of them.

    There are three defensible positions and they produce different businesses:

      TIME     free for N days, then everything locks.
               Simple, and it converts on urgency. It also means somebody who
               tries the app in a quiet month never sees it work.

      VOLUME   N items forever, unlimited everything else.
               What is written above. Generous, slower to convert, and it means
               the free tier is a permanently useful product rather than a
               countdown -- which is the position the rest of this portfolio
               already takes.

      FEATURE  the core job free forever, the compounding part paid.
               What the three boating apps and Porchlight already do, and the
               only one of the three that survives having no server to pay for.

    Return the line you want under an app's price, or leave this returning the
    hand-written string to keep the per-app judgment.
    """
    return app.get("free", "")


BADGE = {
    "live":    ("On the App Store",  "live"),
    "browser": ("Open in a browser",  "browser"),
    "soon":    ("Coming soon",        "soon"),
    "build":   ("Coming soon",        "soon"),
    "design":  ("In design",          "design"),
}

GROUPS = [
    ("browser", "Open right now",
     "No download, no account, no email address. It runs the real engine in a browser."),
    ("soon", "Coming soon: waiting on a store",
     "Finished software, held up by a submission rather than by a feature. Each of "
     "these is close, and what it is waiting on is named on its own page."),
    ("build", "Coming soon: waiting on one piece",
     "Built and running, with one named thing still missing. In most cases that "
     "missing thing is the part somebody would actually be relying on, which is "
     "why it is not for sale yet."),
    ("design", "In design",
     "Specified in full, scoped, and not started. Listed because the specification "
     "is the part that took the thinking."),
]
