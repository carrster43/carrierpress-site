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

    sub     3-day trial, then monthly or yearly
    once    3-day trial, then one payment (safety apps keep the answer free)
    b2b     sold to an institution; no self-serve price
    none    in design, no price yet

>>> THE FREE TIER CAPS BELOW ARE DEFAULTS, NOT DECISIONS. <<<
`free` is the single field that decides whether the free tier is a fair trial of
the product or a demo that annoys people into leaving. It is a judgment about
each app's own shape -- a symptom log needs weeks before it can show you
anything, a resume parser is useful on the first document -- and it is yours to
set. See free_tier_rule() at the foot of this file.
"""
import re

# number, slug, name, blurb, status, shape, price, free, note
# headline (optional): the landing page h1, and the store screenshot 1 caption.
#   Without one the page's h1 is the app name.
APPS = [

    # ---- No backend, no account, no running cost. The fastest to a store. ----
    dict(n=43, slug="boatready", headline="Everything your boat must carry.", name="Boat Ready",
         blurb="Federal carriage requirements for your exact boat, answered offline, with the CFR citation and the manual page behind every line.",
         status="soon", shape="sub", price="$4.99/mo or $49.99/yr",
         # No trial exists on either rail, so the sub-shape default line about
         # one must not print here (2026-11-04).
         tag="Renews each month or year until you cancel. Gear, Lights, Buoys, Sound signals and advisories are free, with no card.",
         limits="On the web, Gumroad takes the payment and you cancel in your Gumroad library. What you enter stays in the browser you enter it in, so it does not follow you to another one. Boat Ready covers federal rules only.",
         free="Checking a boat is free, now and always. Unlimited boats, unlimited checks, no account.",
         note="The subscription saves the boats you look after, lets you tick items off as you go, opens Practice for lights and marks, and adds forecasts, tides and currents. Checking a boat, reading lights and marks, and every safety advisory stay free. Night Watch and Channel Marks are part of it now.",
         # Search copy (2026-11-02). Every FAQ answer below is lifted from this
         # app's own landing and support page; nothing here is new fact.
         seo=dict(
             title="Boat Safety Checklist and Required Equipment | Boat Ready",
             desc="A boat safety checklist for your exact boat: the federal carriage requirements, with the CFR citation behind every line. Free to check, $4.99/mo to save boats.",
             h1="Boat safety checklist: everything your boat must carry",
             faq=[
                 ("Is Boat Ready a boat safety checklist?",
                  "It answers one question about one boat: does it carry what federal law requires? You describe the boat, including its length overall, how many people are aboard, what drives it, whether you run inland or coastal, and a few toggles such as an enclosed engine or fuel space, a fixed fire system, an installed toilet and use after dark. You get the carriage list for that exact boat. The subscription adds a checklist you tick off as you go."),
                 ("What is free and what does the subscription cost?",
                  "Checking a boat is free, now and always: unlimited boats, unlimited checks, no account. Reading lights and marks and every safety advisory stay free too. On the web the subscription is $4.99 a month or $49.99 a year. It saves the boats you look after, lets you tick items off as you go, opens Practice for lights and marks, and adds forecasts, tides and currents."),
                 ("Where do the requirements come from?",
                  "Every line carries the section of the Code of Federal Regulations it comes from, in Titles 33 and 46. Where the federal boating safety manual, COMDTINST M16796.8A, still matches the current rule, its page is cited too, so you can check the source instead of taking the app's word."),
                 ("Does my boat need a fire extinguisher?",
                  "It depends on the boat. A boat with no engine at all, such as a kayak, a canoe or a sailboat with no motor, carries no federal extinguisher requirement. With an engine, the exemption needs all three of these at once: under 26 feet, outboard power, and no enclosed space where fuel or vapour can collect. Miss one and the requirement comes back, in the length bands of 33 CFR 175.320."),
                 ("Does it cover my state's boating rules?",
                  "No. Boat Ready covers federal carriage requirements only, and states often require more. Every result ends with a line telling you to check your state boating agency, so a short clean list is never read as a promise that you are compliant."),
                 ("Is it an inspection or legal advice?",
                  "No. It is a reference tool for recreational vessels. It cannot look at your gear, and it is not affiliated with, endorsed by, or connected to the United States Coast Guard or the Coast Guard Auxiliary."),
                 ("Do I need an account or a download?",
                  "No. It opens in your browser, and checking a boat needs no account and uploads nothing. It is built to answer offline, because the question gets asked at a dock or on the water."),
                 ("Who makes Boat Ready?",
                  "One person, Jeffrey L. Carrier, under the Carrier Press imprint. Questions go to support@carrierpress.com, and one person reads them, so a reply may take a few days. It is not the Coast Guard's app and not NOAA's."),
                 ("Can I try it before paying?",
                  "Yes, the free parts, with no card and no account: Gear with every item and its rule, Lights, Buoys, Sound signals and NOAA advisories. There is no timed trial of the paid parts on the web. The paid screens list what they open before you can subscribe."),
                 ("What exactly am I charged, and does it renew?",
                  "On the web, $4.99 a month or $49.99 a year, whichever you pick on Gumroad's page. Gumroad takes the payment, so your card never reaches Boat Ready, and it renews each month or year until you cancel. Your license key comes on the receipt; you paste it once in each browser you use."),
                 ("How do I cancel, and what happens then?",
                  "Cancel in your Gumroad library, gumroad.com/library. What you paid for stays open until that month or year runs out. Then My boats, Practice and the paid part of Conditions lock in your browser. The free parts stay, and the boats you saved stay in that browser, where you can still see them."),
                 ("What if a renewal payment fails, or I am offshore?",
                  "The page asks Gumroad about your key about once a day. If a renewal has failed, the paid parts lock until you sort it out at Gumroad and paste your key again; your boats are not touched. With no signal, the paid parts stay open for up to 7 days after Gumroad last said yes."),
                 ("Where does my data go?",
                  "It stays in your browser. There is no account and no server of ours. Your license key is kept there too and goes only to Gumroad, to be checked. Conditions asks NOAA for the stations you chose and never sends your position. The privacy page, linked at the foot of this page, has the full list."),
             ]),
    ),

            dict(n=41, slug="conceptionzodiac", headline="The other sign.", name="Conception Zodiac",
         blurb="The sign overhead at conception rather than at birth. A pure calculation, with no account and no database, and the birthday you enter never leaves your device.",
         status="build", shape="once", price="$14.99 once", free_label="Try it",
         free="Any birthday, as many as you like, with no sign up and no time limit: its birth sign, and how many conception signs it could be.",
         note="The purchase shows which sign, the others it could be, and the weeks that settle it, and keeps people by name so a family is one tap each. The list never leaves your device. One payment, not a subscription.",
         limits="It names a sign, never a date, and it is for curiosity, not medical advice. On the web, what you type stays in that browser; only a license key goes out, to Gumroad, to check it. The same key works in any browser you paste it into, without paying again, though saved people stay in the browser that saved them. Jeffrey L. Carrier makes it, and support@carrierpress.com reaches him."),

    # Downpour, added 2026-09-25. WEB ONLY since 2026-10-16 (his call, after
    # the 10-14 App Store 4.3 rejection): sold on Gumroad at $14.99 once for
    # tabletop game masters. Facts from Downpour mobile/lib/access.ts,
    # lib/scenes.ts and RainWindow.web.tsx (2026-11-04). `limits` is printed on
    # the landing page.
    dict(n=36, slug="downpour", headline="Rain for the table.", name="Downpour",
         blurb="Rain for tabletop game masters: on the tavern roof, over a camp in the forest, rolling in as the boss fight starts. Every drop is made live in your browser, so there is no recording and no loop for the table to notice.",
         status="browser", shape="once", price="$14.99 once", free_label="Try it",
         tag="One payment, never a subscription. The license key comes by email from Gumroad, and you paste it into any browser you use.",
         free="Play the Tent for ten minutes at a time, as often as you like, with all four controls working on it. Rain Window shows one live camera for three minutes a visit. No account and no email address.",
         note="Nine surfaces, up to three layered at once, and six ready scenes. Night Arcs change the rain over time: Storm passing builds to a peak and eases off over 90 minutes, Wind down fades over an hour, Rolling showers comes and goes. Save your own rains, switch between them mid-session with a crossfade, and paste a rain's code into Discord for another table. A timer from 15 minutes to 2 hours fades it out. Rain Window puts a live public camera from somewhere it is raining now on your screen while your rain plays, with any camera on the list and no time limit.",
         limits="It plays while the browser tab stays open. Phones pause browser sound when the screen locks, so a laptop or tablet by the table works best. It is rain only: no music, no thunder, no tavern voices. Rain Window needs a connection, and a camera can go dark when its owner stops the stream. Your settings and saved rains stay in that browser and do not follow your key to another one, so copy a rain's code to move it. Downpour is made by Jeffrey L. Carrier, and support@carrierpress.com reaches him."),

    # ---- Runs in a browser today ----
    dict(n=31, slug="planfinder", name="Plan Finder",
         blurb="Guided Medicare Advantage comparison that compares on the whole picture, including whether a plan covers the drugs somebody already takes. No enrollment, no commission, no TPMO status.",
         status="browser", shape="b2b", price="Licensed to agencies",
         free="The sample comparison is open to anyone, with no account and no email address.",
         note="Sample data is invented on purpose. Carriers, plans and coverage are fictional, so a demo can never misdescribe a real product.",
         link="https://carrster43.github.io/planfinder-web/sample", link_label="Open the sample comparison"),

    dict(n=14, slug="throughthegate", name="Through the Gate",
         blurb="Shows the structured record a resume parser actually keeps, and, more to the point, everything it threw away.",
         status="build", shape="sub", price="$19.99/mo",
         free="One resume, parsed in full, free. You see the whole record before you decide anything.",
         note="Priced by the month because a job search ends. Most people need it for about three."),

    # ---- Finished software, listing staged, not yet submitted ----
    dict(n=42, slug="whoserves", name="Who Serves",
         blurb="Everyone who governs your address, on one screen: the districts, the offices, the names, and when each of them is next up for election.",
         status="soon", shape="sub", price="$14.99/mo or $143.99/yr",
         # Matched to HomeRule HEAD 2026-10-03 (Paywall.tsx ALWAYS_FREE, docs/description.txt):
         # the lookup is free forever, there is NO trial, and the subscription
         # sends no change notices. `tag` replaces the generic subscription-trial
         # line on the card and the landing page, which would be false here.
         free_label="Free, forever",
         free="Any US address, every government, every office and officeholder, every source and check date, and your election dates. No account.",
         tag="Looking up any address is free. The subscription adds the tools below.",
         note="The subscription saves up to eight addresses on your device, adds recent votes and filings for your members of Congress, addresses a letter to any officeholder you pick, and shares the sourced record as plain text.",
         # The cautious visitor's questions, answered before they pay. Each answer
         # is read from HomeRule (lib/webLicense.web.ts, lib/entitlement.ts,
         # components/Colophon.tsx) or the privacy page. No refund line: none is
         # published. 2026-11-04.
         seo=dict(
             title="Who Serves: Everyone Who Governs Your Address, With Sources | Carrier Press",
             desc="Type a US address and see every government with authority there and who holds each office, with the source and check date on each name. Free to look up, no account.",
             faq=[
                 ("Who makes Who Serves, and does it take a political side?",
                  "Jeffrey L. Carrier, one independent developer, under the Carrier Press imprint, with no advertising and no investors. It is not a government service and not affiliated with any agency, party or campaign. There is no rating, score, grade or endorsement of anyone, and none will be added. It shows the record and leaves the judging to you."),
                 ("Where does each fact come from, and how fresh is it?",
                  "Every name shows where it was read and when it was last checked. Districts come from the US Census Bureau, Congress from the Senate and the Clerk of the House, state legislators from Open States, which compiles them from the states, and county offices from the county or a statewide directory. Congress and the state legislatures are read again every week. When a check is too old, or an election has passed since, the app says so rather than vouching for the name."),
                 ("What is free?",
                  "Looking up any US address, every government, office and officeholder, every source and check date, and your election dates, with no account. That stays free with or without a subscription. There is no free trial of the subscription, because the record itself is what is free; open the app and try any address first."),
                 ("Exactly what is charged, and does it renew?",
                  "On the web, $14.99 a month or $143.99 a year, whichever you pick at Gumroad's checkout. Gumroad takes the payment. It renews automatically until you cancel. Your license key is on the Gumroad receipt, and you paste it into the app in any browser you use. A web subscription opens the subscriber tools in browsers, not in the iPhone app."),
                 ("How do I cancel, and what happens after?",
                  "Cancel any time from your Gumroad receipt or library. The subscriber tools stay open for the time you already paid for, then close once Gumroad reports the subscription ended, which the page checks about once a day. A failed renewal payment closes them the same way. Looking up addresses stays free, and addresses you saved stay readable."),
                 ("What happens to my address?",
                  "It goes to the US Census Bureau's geocoder to find your districts, and nowhere else. Nothing you look up is kept. If you subscribe and save an address, it stays in your own browser until you delete it. There is no account and no server of ours. The privacy policy has the details."),
                 ("How do I reach a person?",
                  "Write to support@carrierpress.com, for a correction or a question, before or after paying."),
             ])),

    dict(n=1, slug="flare", name="Flare",
         blurb="Symptom log for PCOS, endometriosis, fibromyalgia and autoimmune conditions. Finds co-occurrence across entries and prints a summary for the doctor.",
         status="soon", shape="sub", price="$4.99/mo or $47.99/yr",
         free="Log freely for 30 days and keep logging after. One doctor summary, free.",
         note="Flare finds patterns across what you record. It does not diagnose, explain or treat anything, and it is not a medical device."),

    dict(n=10, slug="soleledger", name="Books for One",
         blurb="A freelancer tax engine. Income, deductions, quarterly estimates, 1099 reconciliation. Nothing else.",
         status="soon", shape="sub", price="$14.99/mo or $143.99/yr",
         free="Track income and expenses for one quarter, free. The ledger is yours either way.",
         note="It never applies a tax rule to you. You enter your own annual target and it does the arithmetic."),

    dict(n=39, slug="porchlight", name="Porchlight",
         blurb="The opt-in map of which houses are giving out candy on the night. Forked from Potluck, and the only thing here with a date it cannot negotiate.",
         status="build", shape="once", price="Free to trick-or-treat",
         free="The map is free for everyone walking the street. It always will be.",
         note="Targeted at Halloween 2027. The revenue is the organizer side, not the map: $14.99 per event, once."),

    # ---- Built, ranked by the demand model ----
    dict(n=2, slug="titrate", name="Titrate",
         blurb="A GLP-1 companion. Side effects plotted against dose, protein targets, plateau interpretation, and when to stop reading a phone and call somebody.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="Log doses and side effects free, indefinitely. The chart that puts them together is the paid part.",
         note="It organises what you record against your own dose history. It does not advise on dosing."),

    dict(n=12, slug="doorstop", name="Doorstop",
         blurb="The one to six unit landlord's ledger, ending in a clean Schedule E.",
         status="build", shape="sub", price="$14.99/mo for 1-3 units, $24.99/mo for 4-6",
         free="One unit, one full year, free. Enough to see whether the Schedule E comes out right.",
         note="It never applies a tax rule. It checks rather than assumes."),

    dict(n=29, slug="papertrail", name="Paper Trail",
         blurb="Receipts, warranties and policies photographed into structured facts, with an alert before something lapses.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="Twenty documents, free, kept forever. Alerts on all of them.",
         note="The paid tier is unlimited documents and the search across them."),

    dict(n=4, slug="vetpocket", name="Vet Pocket",
         blurb="Pet records, plus an answer to whether this is an emergency visit or it can wait until Monday, with a cost range attached to each path.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="One animal, complete records, free forever.",
         note="The triage answer is a range of what the visit tends to cost, not a diagnosis."),

    dict(n=3, slug="perimeter", name="Perimeter",
         blurb="Thirty-six perimenopause symptoms, including the ones nobody connects to it. Produces a script for the GP appointment.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="The full symptom list and one appointment script, free.",
         note="It organises what you tell it into something you can say out loud in ten minutes."),

    dict(n=23, slug="threshold", name="Threshold",
         blurb="Every parental control across phone, console, tablet and ten apps, for one child's age, configured in one sitting.",
         status="build", shape="once", price="$28.99 per child",
         free="See the whole checklist for your child's age before you pay for anything.",
         note="One payment per child, never a subscription. The job is done in an afternoon and should not bill monthly for the rest of the year."),

    dict(n=9, slug="firstday", name="FirstDay",
         blurb="Forward the school emails and PDFs. Get back one calendar, one supply list and one form tracker.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="One child, one term, free.",
         note="Seasonal by nature. Most families need it in August and again in January."),

    dict(n=5, slug="pillproof", name="PillProof",
         blurb="Senior-first medication adherence. Confirm a dose by photographing the pill. Billed to the adult child, not the patient.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="Three medications, free, with reminders.",
         note="Photo confirmation is not wired yet, and that is the part most people would be relying on. It is not being sold until it is."),

    dict(n=7, slug="thebinder", name="The Binder",
         blurb="The if-something-happens file, with staged release to named people on verified death.",
         status="build", shape="once", price="$99 once, then $29/yr",
         free="Build the whole vault and the whole checklist, free. You only pay to name the people it releases to.",
         note="v1 is the vault and the checklist. Staged release is deferred to v1.1 by design, and that is the reason it is not for sale yet."),

    dict(n=17, slug="stuck", name="Stuck",
         blurb="Homework help that is Socratic by architecture and structurally cannot output the answer. Parents can read the whole transcript.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="Five sessions a month, free, with the full transcript.",
         note="It cannot give an answer. That is not a policy, it is how it is built."),

    dict(n=15, slug="scope", name="Scope",
         blurb="Quote to signed statement of work to change order, for solo service providers. Makes raising a change order unemotional.",
         status="build", shape="sub", price="$24.99/mo or $239.99/yr",
         free="Three documents a month, free, fully signable.",
         note=""),

    dict(n=28, slug="errand", name="Errand",
         blurb="Researches, drafts, fills the form, and stops at the confirm button. Assistive, not autonomous.",
         status="build", shape="sub", price="$24.99/mo or $239.99/yr",
         free="Five errands a month, free.",
         note="It stops at the confirm button. Every time, on purpose."),

    dict(n=30, slug="quiet", headline="Search the way you remember it.", name="Quiet",
         blurb="The personal record that never leaves the device. No account, no sync, and no code that sends what you write anywhere.",
         status="soon", shape="once", price="$78.99 once", free_label="Try it",
         free="Your first 10 entries. Search, export and delete keep working after that, so nothing you wrote is ever held back.",
         note="The purchase removes the limit for good. There is no server to pay for, so there is nothing to bill you monthly for: your journal lives in a database on your phone and nowhere else."),

    dict(n=26, slug="houseledger", name="House Ledger",
         blurb="The home's service record: systems, ages, warranties, contractors. Built so it hands over cleanly at sale.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="Ten records, free, kept forever.",
         note=""),

    dict(n=27, slug="pantry", name="Pantry",
         blurb="Inverts the meal planner. Starts from what is already in the house and what expires first, rather than from a recipe you have to shop for.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="The whole pantry and the expiry order, free. Always.",
         note=""),

    dict(n=20, slug="thirdplace", name="Third Place",
         blurb="Recurring low-commitment gatherings. One tap to say you are coming, and an honest count of who actually turns up regularly. Explicitly not dating.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr per host",
         free="Free for everyone attending, forever. Only the host pays.",
         note=""),

    dict(n=21, slug="potluck", name="Potluck",
         blurb="Neighbourhood organising and lending, geofenced to a few blocks, address verified without storing an address. Two verbs: organise a thing, lend a thing.",
         status="build", shape="b2b", price="Free to neighbours",
         free="Free for every neighbour, permanently. Moderation shipped in the first migration, not bolted on later.",
         note="Sold to the association or the city, never to the street."),

    dict(n=19, slug="fluenthour", name="Fluent Hour",
         blurb="One spoken scenario a day, ten minutes. No lessons, no streaks, no gems, no owl.",
         status="build", shape="sub", price="$17.99/mo or $172.99/yr",
         free="Seven scenarios, free. One a day, same as the paid tier.",
         note=""),

    dict(n=6, slug="relay", name="Relay",
         blurb="A shared care record that replaces the seven-sibling group chat with a typed update feed, so nobody has to scroll to find out what happened.",
         status="build", shape="sub", price="$19.99/mo or $191.99/yr per household",
         free="Three people, free. Enough to find out whether the family will actually use it.",
         note=""),

    dict(n=8, slug="handoff", name="Handoff",
         blurb="Co-parenting calendar, expense splits, and a message log that exports in a form a court will accept.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr each",
         free="The message log is free and stays free. Export is the paid part.",
         note="The calendar interface is missing. The log underneath it is built and verified against a live database."),

    dict(n=16, slug="tradedesk", name="Trade Desk",
         blurb="Field service for one person with a van. Under sixty seconds of admin per job, usable with gloves on. Offline first.",
         status="build", shape="sub", price="$38.99/mo or $374.99/yr",
         free="Ten jobs, free, with invoicing.",
         note=""),

    dict(n=13, slug="cancelled", headline="Every charge, priced by the year.", name="Canceled",
         blurb="Finds every recurring charge in your bank statement, on your own device, ranks them by what they cost you a year, and shows you where to cancel. One payment, never a subscription, which would rather defeat the point.",
         status="build", shape="once", price="$38.99 once", free_label="Try it",
         free="Two invented examples show it working before you open anything of your own, and nothing from them is saved. Then open a statement and see every recurring charge and what each costs you a year, plus where to cancel the most expensive one it knows. The unlock shows where to cancel the rest.",
         note="Where to cancel every charge it knows, as many on your tracking list as you like, every way to cut your spending, how long an emergency fund takes, and your progress month to month. It does not connect to your bank, and that is a deliberate limit rather than a missing feature.",
         limits="Your statement is read in your browser and never uploaded. You can test that: load the app, turn off your Wi-Fi and mobile data, then open a statement, and it reads the same. There is no account and no bank login. Your lists stay in that browser, so clearing its data loses them. Canceled is made by Jeffrey L. Carrier, one independent developer. Questions go to support@carrierpress.com."),

    dict(n=18, slug="homeroom", name="Homeroom",
         blurb="Homeschool compliance measured against the family's own state rules, assembling the portfolio as the year goes.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
         free="Build the portfolio free. The compliance assertion is the paid part.",
         note="Waiting on legal review of the per-state rule set. The assertion is the product, so there is no version of this that ships without it."),

    dict(n=24, slug="signalcheck", name="Signal Check",
         blurb="Teen wellbeing the teen agreed to. Consent-first, with autonomy earned back on a visible schedule.",
         status="build", shape="sub", price="$14.99/mo or $143.99/yr",
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
         status="design", shape="sub", price="$14.99/mo or $143.99/yr", free="",
         note="It will organise. It will never interpret."),

    dict(n=35, slug=None, name="Throughline",
         blurb="The decision and commitment log for projects that are not software, assembling the weekly stakeholder update as it goes.",
         status="design", shape="sub", price="$14.99/mo or $143.99/yr", free="", note=""),

    dict(n=38, slug=None, name="AI Integrator",
         blurb="The connection layer between an assistant and the tools that already hold the work: auth, scopes, a capability catalog, and an audit log of every action taken and on whose authority.",
         status="design", shape="b2b", price="$99-499/mo", free="", note=""),

    # Cast reworked 2026-10-05 to the author's model (2026-10-04): his books
    # sold one at a time at audiobook prices ($6.99 floor), and a subscription
    # ($22.99/mo, $109.99/yr, 3-day free trial) for the listener's own EPUBs.
    # The $19.99 all-books unlock is retired.
    # Updated 2026-11-04 for the open web sale: the page must say what a browser
    # gets (computer voices it already has) before anyone pays. Every FAQ answer
    # is lifted from the web build (Cast lib/web-notes.web.tsx) or the privacy
    # page; nothing is new fact, and no refund policy is stated because none has
    # been decided.
    dict(n=37, slug="cast", headline="The characters, in their own voices.", name="Cast",
         blurb="A book performed with a narrator and a voice for each character. In your browser today, in the computer voices your browser provides; the coming iPhone app makes natural voices on the phone. Play the Carrier Press shelf, or add EPUB files of your own.",
         status="soon", shape="sub", price="Books from $6.99 · Your own books $22.99/mo",
         tag="In the iPhone app, when it is out: shelf books are bought one at a time, and your own books are $109.99 a year or $22.99 a month, with a 3-day free trial. Cancel before it ends and nothing is charged.",
         free_label="Try it",
         free="The opening of every shelf book, usually the first chapter or two, and the first chapter of every book you add. In your browser, with no account and no email.",
         note="A license to listen to one book in full, not an audio file and not a copy of the book. 84 books on the shelf: 52 Carrier Press originals, the three American Firsts and 29 classics, and every card says how fully it is cast. It creates no audiobook edition, which keeps the free Audible route open on every title.",
         limits="In a browser the voices are computer voices your browser and device already have, not recordings of narrators, and how they sound depends on the browser. Press Play on any book to hear them before paying. Cast needs a connection to open a book, and a browser can stop speaking when a phone locks or the tab goes to sleep, so keep the page open while you listen. Your place stays in the browser you use. Natural voices are in the iPhone app, not the web version.",
         link="/audio/", link_label="See the catalogue",
         seo=dict(
             title="Cast: Books Performed, a Voice for Each Character | Carrier Press",
             desc="Hear a book performed with a narrator and a voice for each character, in your browser. Every book's opening plays free, with no account. Computer voices, and every card says how fully it is cast.",
             faq=[
                 ("Who makes Cast?",
                  "Jeffrey L. Carrier, who publishes as Carrier Press: one independent developer, no investors and no advertising. To reach a person, write to support@carrierpress.com."),
                 ("Are these real narrators?",
                  "No. They are computer voices, not recordings of actors or narrators. In a browser they are the voices your browser and device already have, so how many there are and how they sound depends on your browser. Cast gives the narrator and each character a different voice where the browser has enough of them, and each book's card says how fully it is cast."),
                 ("Can I hear a book before I pay?",
                  "Yes. Every book's opening plays free in your browser, with no account and no email. Each card says how long its opening is. What you hear is what a license opens the rest of."),
                 ("What exactly am I charged?",
                  "A book from the shelf is one payment, from $14.99, with the price on its card. It never renews. Your Own Books, which plays EPUB files you add, is a membership: one week free for new members, then $22.99 a month or $109.99 a year, renewing until you cancel. It does not open the shelf books, and neither is part of Carrier Press Access. Gumroad takes the payment."),
                 ("How do I cancel the membership?",
                  "In your Gumroad library, before the trial or the period ends. A cancelled membership runs to the end of the period you paid for. When it ends, the books you added stay in your browser and the first chapter of each still plays."),
                 ("What happens to files I add?",
                  "An EPUB you add is read inside your browser and never uploaded. Cast keeps the script it makes, in that browser, and not the file. Remove deletes it, and so does clearing the site's data. Adding a book is free and its first chapter plays free."),
                 ("Where is my key, and what if I come back later?",
                  "Your license key is on the Gumroad receipt email. Open Cast, tap I have a key, and paste it; it opens the book it was bought for. There is no account: your place and your opened books are kept in the browser you use, so in another browser, or after clearing site data, paste the same key again. Your place does not follow you there."),
             ]),
    ),

    # Cleared, added 2026-10-27 (author approved the pricing proposal). Web sale
    # live since 2026-10-21 by Gumroad membership; price decided 2026-10-20.
    # Free part from Cleared docs/PLAN.md.
    dict(n=47, slug="cleared", headline="Every transport credential, one study app.", name="Cleared",
         blurb="Study guides and practice tests for the CDL and the credentials around it: HazMat, passenger and school bus, TWIC, drone, pilot, vessel captain, rail and more, with the source named under every answer.",
         status="browser", shape="sub", price="$4.99/mo or $49.99/yr",
         tag="A subscription, open in a browser today. The iPhone app is not out yet.",
         free_label="Try it",
         free="The first study section and 10 practice questions of every pack, free, in your browser.",
         note="19 packs and 828 practice questions, from the CDL general test, air brakes and combination vehicles through HazMat, drone, pilot, captain, rail and FEMA. Every answer names its source: the federal rule, the FEMA course text, or your state's law or manual where the state sets it. Every pack was checked item by item by a reviewer who did not write it. Nothing is copied from a state manual.",
         # Search copy (2026-11-02). Every FAQ answer below is lifted from the
         # Cleared landing page and its support page (/cleared/); nothing is new fact.
         seo=dict(
             title="CDL Practice Test and Permit Test Prep | Cleared",
             desc="Free CDL practice test questions in your browser. 828 questions across 19 packs, from general knowledge to HazMat, with the source named under every answer.",
             h1="CDL practice test and permit test prep, with the source behind every answer",
             faq=[
                 ("Is there a free CDL practice test?",
                  "Yes. The first study section and the first 10 practice questions of every pack are free in your browser, along with the engine compartment part of the pre-trip examiner. No account and no email are needed. A subscription opens every pack."),
                 ("What does Cleared cost?",
                  "On the web it is $4.99 a month or $49.99 a year, sold through Gumroad. One subscription opens every pack, including packs added later. Your license key is on the Gumroad receipt email; paste it into the unlock screen once in each browser you study in."),
                 ("Which CDL tests does it cover?",
                  "Cleared has 19 packs and 828 practice questions. On the CDL side that includes General Knowledge, Air Brakes, Combination Vehicles, HazMat, Passenger, School Bus, Tank Vehicle, and Doubles and Triples. The shelf also has TWIC, FAA Part 107 Remote Pilot and Private Pilot, USCG Captain (OUPV), Locomotive Engineer and Conductor, and the FEMA NIMS and ICS core courses."),
                 ("Will it help me prepare for the CDL permit test?",
                  "Cleared is study preparation for the CDL knowledge tests, with a study guide and practice questions in each pack. It is not the exam and it does not issue anything: your state licensing agency gives the tests. Where a figure comes from a state manual rather than a federal rule, the app marks it and tells you to check your own state's manual, because that is what you will be tested on."),
                 ("Where do the answers come from?",
                  "Every answer names the federal rule, FEMA course or state law it rests on, for example 49 CFR 383.91(a). Every pack was checked item by item against its cited text by a reviewer who did not write it. Nothing is copied from a state manual."),
                 ("Can I practise the pre-trip inspection?",
                  "Yes. The CDL packs have a pre-trip examiner: you say each item out loud, as you would to an examiner, and tick it off. The engine compartment part is free."),
                 ("Do I need an account or an app download?",
                  "No. Cleared opens in a browser at carrierpress.com/cleared/app. Your progress is kept in the browser you study in, not on a server, so it does not follow you to another browser or device. The iPhone app is not out yet."),
                 ("How do I cancel?",
                  "Cancel from your Gumroad library. Cancelling does not close the packs straight away: you keep them for the days you have already paid for."),
                 ("Who makes Cleared?",
                  "Carrier Press, the imprint of Jeffrey L. Carrier: one independent developer, no advertising and no investors. It is not connected to any government agency. Write to support@carrierpress.com with any question."),
                 ("Can I try it before I pay anything?",
                  "Yes, with no account and no email. Open any pack and use its first section and first 10 questions. You see the price, the renewal and how to cancel before you can subscribe, and the checkout is on Gumroad, so your card details never reach Cleared."),
             ]),
    ),

    # Bench, registry 43 (author 2026-10-19). Operators who run a desk get the
    # revenue share; subscribers get credits (never cash) and a vote on the next
    # desk. Concept only: this page exists for the waiting list.
    dict(n=46, slug="bench", headline="Generic AI gives generic answers.", name="Bench",
         blurb="Bench fixes that one trade at a time. Each desk is built by a working professional who knows the rules, the paperwork and the shortcuts, and who reviews what the AI produces. Join the waiting list and help decide which trade gets the first desk.",
         status="design", shape="sub", price="$19.99/mo per desk",
         tag="The planned price per desk, per month. Nothing is sold until it is built.", free="",
         note="Not built. The waiting list decides whether it gets built, and which desk opens first."),

    dict(n=34, slug=None, name="Rough-In",
         blurb="The code answer for electricians with the article number attached, refusing to answer when it cannot cite one.",
         status="design", shape="sub", price="$19.99/mo or $191.99/yr", free="", note=""),
]


# The default trial lines (author, 2026-09-25: "use a short trial default for
# all cards"), then three days for every trial (author, 2026-09-26). The
# subscription line matches its price tag; the one-payment line is below.
SUB_TRIAL = ("Three days of everything, then the subscription. Cancel before "
             "it ends and nothing is charged.")
# Three days (author, 2026-09-26). "Then the price above", not "unlocks it for
# good": The Binder renews yearly and Crosscheck is priced per case.
ONCE_TRIAL = "Three days of everything, then the price above."

# Safety carve-out: the answer stays free, only saving or practice is sold.
SAFETY_FREE = {"boatready", "nightwatch", "channelmarks"}


# The web apps behind the server paywall (author 2026-11-05). Their pages sell
# the key and show a sample (app_proofs.py); nothing about them is free.
# Shows a free trial, which the web version does not have.
HIDDEN_SHOTS = {"cast": {"store-2"}}
GATED_APPS = ("cleared", "boatready", "whoserves", "conceptionzodiac", "cancelled", "downpour", "cast")


def free_tier_rule(app):
    """
    The line under an app's price: what you can try before paying.

    AUTHOR RULE, 2026-09-25: apps are not free unless the purchase earns, so
    every card defaults to a SHORT TRIAL of a paid app, never a free tier.
    The per-row `free` strings above are the older, more generous caps; they
    are kept as a record but no longer printed, except where noted below.

    Three kinds of row keep their own hand-written line:

      free_label   The row was already tightened to a taste by the author
                   (Conception Zodiac, Downpour, Quiet, Canceled).
      who pays     b2b rows and "Free to ..." prices (Porchlight, Potluck,
                   Waitlist, GED): the person using it is not the buyer, so a
                   trial would misstate the business, not tighten it.
      SAFETY_FREE  Boat Ready's legally required safety list, and (author,
                   2026-09-26) identifying lights in Night Watch and reading
                   marks in Channel Marks. The purchase buys saving or
                   practice, never the answer somebody needs on the water.
    """
    if app.get("slug") in GATED_APPS:
        return ""
    if app.get("free_label") or app["shape"] == "b2b" \
            or app.get("price", "").startswith("Free to") \
            or app["slug"] in SAFETY_FREE:
        return app.get("free", "")
    if app["status"] == "design":
        return ""
    return SUB_TRIAL if app["shape"] == "sub" else ONCE_TRIAL


def free_label(app):
    """The heading for that line. Only a hand-written row may say otherwise."""
    if app.get("free_label"):
        return app["free_label"]
    if (app["shape"] == "b2b" or app.get("price", "").startswith("Free to")) \
            and re.search(r"\bpays\b|\bfree (?:for|to) (?:every|everyone)",
                          app.get("free", ""), re.I):
        return "Who pays"
    if app["slug"] in SAFETY_FREE:
        return "Always free"
    return "Try it"


BADGE = {
    "live":    ("On the App Store",  "live"),
    "browser": ("Runs in a browser",  "browser"),
    "soon":    ("Coming soon",        "soon"),
    "build":   ("Coming soon",        "soon"),
    "design":  ("In design",          "design"),
}

GROUPS = [
    ("browser", "In your browser today",
     "No download and no account. Each page shows a sample first. The paid apps open "
     "with a license key, sent by email from Gumroad."),
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


# Screenshot alt text, written by looking at each full-size shot (site review
# 2026-10-31, #12). Keyed "<slug>/<name>"; a shot with no entry falls back to
# its position, which is honest but tells a screen reader nothing.
import json as _json, pathlib as _pathlib
_ALTS = _pathlib.Path(__file__).parent / "apps" / "shots" / "alts.json"
SHOT_ALTS = _json.loads(_ALTS.read_text(encoding="utf-8")) if _ALTS.exists() else {}


def shot_alt(app, name, i, n, word="screenshot"):
    alt = SHOT_ALTS.get("%s/%s" % (app.get("slug", ""), name))
    return "%s: %s" % (app["name"], alt) if alt else "%s, %s %d of %d" % (app["name"], word, i, n)


import app_gate_copy as _gate_copy
_gate_copy.apply(APPS)
