"""
What a visitor sees of each paywalled web app before paying (author 2026-11-05):
a small sample that shows the app is real and cannot be used on their own boat,
address or statement. Every value was produced by the app's own engine or data
on 2026-11-05 (~/Projects/AppGate/proofs); none of it is written by hand. To
refresh, re-run those scripts and paste the result.
"""
from html import escape as e

CLEARED = [
    ("A tractor with a gross combination weight rating of 40,000 pounds pulls a trailer rated 30,000 pounds. Which class is needed?",
     ["Class A", "Class B", "Class C"], 0,
     "A combination of 26,001 pounds or more towing a unit rated over 10,000 pounds is Class A.", "49 CFR 383.91"),
    ("How long must you hold a commercial learner's permit before taking the skills test?",
     ["7 days", "14 days", "30 days", "90 days"], 1,
     "The skills test may not be taken in the first 14 days after the CLP is first issued.", "49 CFR 383.25"),
    ("A CLP holder has the tank (N) endorsement. What may they drive?",
     ["A loaded tank vehicle with a trainer", "Only an empty tank vehicle", "Any tank vehicle once they have 14 days"], 1,
     "A CLP holder with N may operate only an empty tank vehicle, purged of residue if it held hazardous materials.", "49 CFR 383.25"),
]

BOAT = [
    ("Registration and numbering", "Certificate of number aboard", "33 CFR 173.11, 173.15, 173.21, 173.27"),
    ("Life jackets", "4 wearable life jackets", "33 CFR 175.15, 175.19, 175.21"),
    ("Throwable flotation", "1 throwable device", "33 CFR 175.15(b), 175.17(a), 175.19(b)"),
    ("Children under 13", "Worn by any child under 13", "33 CFR 175.15(c), 175.25"),
    ("Visual distress signals", "Day and night signals, e.g. 3 red flares", "33 CFR 175.110(a), 175.115(a), 175.125, 175.130"),
    ("Sound signals", "Horn or whistle", "33 CFR 83.33(b)"),
    ("Anchor ball", "One black ball, if you anchor by day", "33 CFR 83.30(a), (e), (g); 84.06"),
]

WHOSERVES = [
    ("US House, Mississippi District 2", "Bennie G. Thompson", "Clerk of the House, read 2026-11-02"),
    ("US Senate, Mississippi", "Cindy Hyde-Smith", "US Senate, read 2026-11-02"),
    ("US Senate, Mississippi", "Roger F. Wicker", "US Senate, read 2026-11-02"),
    ("Governor of Mississippi", "Tate Reeves", "Office of the Governor, read 2026-10-23"),
    ("Mississippi State Senate", "District 29", "US Census Bureau geocoder, read 2026-11-05"),
    ("Mississippi State House", "District 67", "US Census Bureau geocoder, read 2026-11-05"),
    ("County and city", "Hinds County, City of Jackson", "US Census Bureau geocoder, read 2026-11-05"),
]

CANCELLED = [
    ("Coreform Fitness", "$39.00", "$468.00"),
    ("Ledgerline News", "$17.00", "$204.00"),
    ("Lumen TV", "$15.99", "$191.88"),
    ("Northsong Music", "$10.99", "$131.88"),
    ("Atlas Cloud Storage", "$2.99", "$35.88"),
]
CANCELLED_TOTAL = "$1,031.64"

CAST = [
    ("narrator", "The orange portal closed behind the crew with a warm pop, and the first thing Patch Bolt did was read the dust."),
    ("narrator", "Then a crate shot past him so fast it stole the dust from under his boots."),
    ("narrator", "A second later, something enormous rumbled under the canyon floor."),
    ("Ember", "Proper problems usually introduce themselves first."),
    ("Patch", "Now this is a proper builder's problem."),
]


# Flare: three findings, word for word, from the frozen engine run on its
# invented 14-day endometriosis log (Flare lib/sample.ts, run 2026-09-28).
FLARE = [
    ("On days with 6 hours of sleep or less, you recorded higher fatigue and brain fog than on days with 7 hours or more.", "notable"),
    ("Your higher stress ratings were recorded on the same days as your higher fatigue and brain fog scores.", "notable"),
    ("Pelvic pain, cramping and back pain rose and fell together on the same days across the log.", "notable"),
]

# Books for One: quarterStatuses() from SoleLedger lib/quarterly.ts, run
# 2026-11-15 on an $8,000 target with $2,000 paid Apr 14, $2,000 Jun 30 and
# $1,000 Sep 12, as of Nov 15 2026.
SOLELEDGER = [
    ("Q1", "Jan 1 to Mar 31", "Apr 15, 2026", "$2,000.00", "Covered"),
    ("Q2", "Apr 1 to May 31", "Jun 15, 2026", "$2,000.00", "Covered"),
    ("Q3", "Jun 1 to Aug 31", "Sep 15, 2026", "$1,000.00", "$1,000.00, past due"),
    ("Q4", "Sep 1 to Dec 31", "Jan 15, 2027", "$0.00", "$2,000.00"),
]

# Quiet: parseQuery() from Quiet lib/query.ts, run 2026-11-15, northern
# hemisphere. The right-hand column is the app's own explanation line.
QUIET = [
    ("photos from last summer", "Looking through photos, from last summer.", "Jun 1 to Aug 31, 2026"),
    ("voice memos in march", "Looking through voice memos, from March.", "Mar 1 to Mar 31, 2026"),
    ("notes about mum from 2025", "Looking through notes, from 2025, mentioning mum.", "all of 2025"),
    ("\"the lake\" last week", "Looking through everything, from last week, mentioning \"the lake\".", "Nov 2 to Nov 8, 2026"),
]


# Titrate: describe(pattern()), describeTrend() and targetsForKg() from
# Titrate lib/pattern.ts + lib/nutrition.ts, run 2026-11-15 on its own
# invented six months (lib/sample.ts). Counts only: the app states no judgement.
TITRATE_DOSES = [("0.25 mg", "May 31"), ("0.5 mg", "Jun 28"), ("1 mg", "Jul 26"), ("1.7 mg", "Aug 23")]
TITRATE = [
    ("Nausea", "You noted Nausea on 9 of the 28 days in the first week after an increase, and 5 of 28 in the second week. Across 4 increases."),
    ("Weight", "Down 10.1lb over 154 days."),
    ("Daily targets", "110 to 147 g protein · 25 to 38 g fibre"),
]


# Doorstop: buildReturn() from Doorstop lib/ledger.ts, run 2026-11-16 on its own
# invented year (lib/sample.ts, SAMPLE_UNITS + SAMPLE_TRANSACTIONS, 2026).
DOORSTOP = [
    ("14 Alder Row", "Line 3, Rents received", "19,800.00"),
    ("14 Alder Row", "Lines 7, 9, 11, 14 and 16: cleaning, insurance, management, repairs, taxes", "9,193.00"),
    ("14 Alder Row", "Net", "10,607.00"),
    ("14 Alder Row", "Not in the totals: New roof over the back extension. Repair or improvement, unanswered", "7,400.00"),
    ("Rear cottage", "Line 3, Rents received", "11,000.00"),
    ("Rear cottage", "Lines 5, 9 and 14: advertising, insurance, repairs", "1,290.00"),
    ("Rear cottage", "Net", "9,710.00"),
    ("Rear cottage", "Not in the totals: Hardware shop. No category", "96.40"),
]

# Threshold ea5748f: guidesFor({age_band: "9-12"}, ["ios", "youtube", "roblox"],
# false, GUIDES), labels from lib/types.ts. Titles and check dates only: the
# steps are what the key opens.
THRESHOLD = [
    ("1", "iPhone or iPad", "The account's own age", "Check the birthday on the child's Apple Account", "Nov 15, 2026"),
    ("2", "iPhone or iPad", "Who can reach them", "Limit who can contact the child on iPhone or iPad", "Nov 15, 2026"),
    ("3", "Roblox", "Who can reach them", "Set the Roblox account age and lock chat", "Nov 15, 2026"),
    ("4", "iPhone or iPad", "What they can see", "Set content restrictions on iPhone or iPad", "Nov 15, 2026"),
    ("5", "YouTube", "What they can see", "Decide between YouTube Kids and a supervised YouTube account", "Nov 15, 2026"),
    ("6", "iPhone or iPad", "What they can buy", "Require approval for purchases on Apple devices", "Nov 15, 2026"),
    ("7", "iPhone or iPad", "How long, and when", "Set Screen Time Schedules and Time Allowances on Apple devices", "Nov 15, 2026"),
    ("8", "iPhone or iPad", "Where they are", "Decide what shares the child's location on Apple devices", "Nov 15, 2026"),
]


def _table(head, rows):
    return ('<div class="pf-wrap"><table class="pf-table"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % ("".join("<th scope=\"col\">%s</th>" % e(h) for h in head),
               "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % e(c) for c in r) for r in rows)))


def _cleared():
    out = []
    for prompt, options, right, why, cite in CLEARED:
        buttons = "".join('<button type="button"%s>%s</button>' % (" data-right" if i == right else "", e(o))
                          for i, o in enumerate(options))
        out.append('<div class="pf-q"><p>%s</p><div class="pf-opts">%s</div>'
                   '<p class="pf-why" hidden>%s <b>Source: %s</b></p></div>' % (e(prompt), buttons, e(why), e(cite)))
    return "Three questions from the CDL General Knowledge pack, as the app asks them.", "".join(out)


def _boat():
    return ("The list for one example boat: 20 feet, outboard, coastal water, 4 people aboard, used by day. "
            "Federal rules as read 2026-10-01. It is a reference, not an inspection, and your state may require more."), \
        _table(["What", "Carry", "Rule"], BOAT)


def _whoserves():
    return ("The record for one example address: the Mississippi State Capitol, 400 High Street, Jackson. "
            "This is a short part of it, and the app shows the same for any US address."), \
        _table(["Office or area", "Who or what", "Where it was read"], WHOSERVES)


def _zodiac():
    return "One example birthday, worked out the way the app does it.", _table(
        ["Born", "Birth sign", "Sign at conception", "Could also be"],
        [("March 15, 1990", "Pisces", "Cancer", "Gemini")])


def _cancelled():
    return ("An invented statement, with invented company names. Nobody's real data. "
            "These five recurring charges come to %s a year." % CANCELLED_TOTAL), \
        _table(["Charge", "Each month", "Each year"], CANCELLED)


def _downpour():
    return ("25 seconds of the Tent surface at its default settings, made by the same code the app "
            "runs. The app makes rain live, so it never loops."), (
        '<audio controls preload="none" src="/assets/proofs/downpour-tent.m4a" class="pf-audio">'
        'Your browser cannot play this clip.</audio>')


def _cast():
    lines = "".join('<p data-voice="%s"><b>%s</b> %s</p>' % (e(v), e(v.capitalize()), e(t)) for v, t in CAST)
    return ("Five lines from The Runaway Crate, a voice for each speaker. This button uses your browser's own voices. "
            "In Cast, the same scene plays in its natural voices, and the whole opening is yours to hear."), (
        '<button type="button" id="pf-hear" class="pf-hear">Hear these lines</button><div id="pf-lines" class="pf-lines">%s</div>'
        '<p class="pf-next"><a href="/cast/app/play?stem=02_The_Runaway_Crate">Open The Runaway Crate in Cast</a></p>' % lines)


def _flare():
    items = "".join('<li>%s <b>(%s)</b></li>' % (e(o), e(st)) for o, st in FLARE)
    return ("An invented 14-day endometriosis log, no real person's, run once through Flare's pattern analysis. "
            "Three of the findings it gave, word for word. It describes what happened together and names no cause."), (
        '<ul class="pf-list">%s</ul>' % items)


def _soleledger():
    return ("An example year: you entered $8,000 as the estimated tax you plan to pay, then paid $2,000 in April, "
            "$2,000 late in June and $1,000 in September. Payments go to the earliest quarter first, as the IRS "
            "applies them. Federal dates only; a date that falls on a weekend or holiday moves to the next business day."), \
        _table(["Quarter", "Covers income from", "Due", "Paid toward it", "Still owed"], SOLELEDGER)


def _quiet():
    return ("What Quiet understood from four searches typed on November 15, 2026. It shows this line under the "
            "search box, so a wrong reading is easy to spot."), \
        _table(["You type", "Quiet reads it as", "Days it searches"], QUIET)


def _titrate():
    doses = ", ".join("%s from %s" % (d, day) for d, day in TITRATE_DOSES)
    return ("An invented six months, no real person's: a dose set four times by a prescriber (%s), "
            "17 nausea notes and 12 weigh-ins ending at 91.6 kg, run through Titrate's own code. What it says, word for word. "
            "Every line is a count or your own numbers drawn back; none says what they mean." % doses), \
        _table(["Screen", "Titrate says"], TITRATE)


# Paper Trail (2026-11-16): lib/sample.ts's invented drawer run through
# decideAlert() and expiryPhrase() (lib/alerts.ts) for 2026-11-16, by
# scratchpad papertrail-sample.mts. Values pasted, not written.
PAPERTRAIL = [
    ("Dishwasher, 5 year parts (Warranty)", "Kelvin Appliance", "Cover ends in 24 days.",
     "Reminds you on 2026-11-16, the day it was filed: less than 30 days were left"),
    ("Home contents (Policy)", "Fairhaven Mutual", "Renews in 41 days, and will charge you unless you cancel.",
     "Reminds you on 2026-11-16, the day it was filed: less than 45 days were left"),
    ("Standing desk (Receipt)", "Ridgeline Supply", "Last day to return is in 9 days.",
     "Reminds you on 2026-11-22, 3 days ahead"),
    ("Cordless drill (Warranty)", "Bellweather Tools", "Cover ends in 120 days.",
     "Asks you to confirm the date first; no reminder until you do"),
    ("Boiler manual and service record (Manual)", "Kelvin Appliance", "Nothing on it expires.",
     "Files it; nothing to remind you about"),
]


def _papertrail():
    return ("Five invented documents, no real household's, filed on November 16, 2026 and run through Paper Trail's "
            "own alert code. The drill's date was hard to read, so it asks before it reminds. On the web the reminder "
            "goes into your own calendar on the day shown."), \
        _table(["Document", "From", "What it says", "What Paper Trail does"], PAPERTRAIL)


# Through the Gate (2026-11-17): lib/sample.ts SAMPLE_PARSE, which
# scripts/generate-sample-parse.mjs produced by running the invented resume
# through the real prompt (provenance "engine"). Values pasted, not written.
THROUGHTHEGATE = [
    ("Growth Alchemist (job title)", "Renamed to \"Growth Marketing Manager\", the title most searches match on. Your wording is kept beside it."),
    ("Rebuilt the onboarding sequence and cut first-90-day churn from 19% to 11%",
     "Dropped. It sits inside a paragraph under the job, so it is read as description text and not kept as an achievement."),
    ("CERTIFICATIONS: Google Analytics IQ",
     "Dropped. It is in a narrow right-hand column, which is read as a sidebar, and the certification was lost with it."),
    ("Summer '22 (start date)",
     "Left empty, because it gives no month, so tenure cannot be worked out. Suggests: a month and year, such as June 2022."),
    ("B.A. Communications, with no year",
     "Flagged: with no graduation year the degree cannot be placed on a timeline."),
]


def _throughthegate():
    return ("An invented resume, no real person's, run once through Through the Gate's own parser. Five of the "
            "things it reported, shortened. It names no employer's system and gives no score."), \
        _table(["In the resume", "What the parser did"], THROUGHTHEGATE)


# Vet Pocket (2026-11-17): lib/sample.ts's invented animals (Biscuit and
# Pepper) run through duePhrase() (lib/triage.ts) for 2026-11-17, by scratchpad
# vetpocket-sample.mts. Values pasted, not written. No triage answer is shown:
# the app's own rule is that one is never written by hand (lib/sample.ts).
VETPOCKET = [
    ("Biscuit (dog)", "Annual booster", "Due in 6 days"),
    ("Biscuit (dog)", "Monthly spot-on", "Due in 6 days"),
    ("Biscuit (dog)", "Quarterly wormer", "Due in 12 days"),
    ("Pepper (cat)", "Annual booster", "Due 2027-05-01"),
    ("Pepper (cat)", "Monthly spot-on", "Overdue by 3 days"),
]


def _vetpocket():
    return ("Two invented animals, no real household's, on November 17, 2026, run through Vet Pocket's own code: "
            "what the Due tab says about each treatment. The 2am answer is written live, only ever for a real "
            "question about a real animal, so it is yours to see in the app."), \
        _table(["Pet", "Treatment", "What Vet Pocket says"], VETPOCKET)


# The Binder (2026-11-18): an invented, half-finished binder (no real person's
# answers) run through lib/checklist.ts SECTIONS, progress and describeProgress
# the way app/(tabs)/binder.tsx words each section, by scratchpad
# thebinder-sample.mts against TheBinder 20c622c. Values pasted, not written.
THEBINDER_HEADLINE = "2 of 9 finished. Every one of them is something nobody has to guess at."
THEBINDER = [
    ("The documents", "About 10 minutes", "Done"),
    ("Money", "About 15 minutes", "3 of 5 answered"),
    ("Insurance", "About 8 minutes", "3 questions"),
    ("Property and keys", "About 8 minutes", "3 questions"),
    ("Digital life", "About 10 minutes", "1 of 5 answered"),
    ("Medical wishes", "About 10 minutes", "4 questions"),
    ("What you want to happen", "About 10 minutes", "4 questions"),
    ("Who to tell", "About 8 minutes", "Done"),
    ("Pets", "About 5 minutes", "2 questions"),
]


def _thebinder():
    return ("An invented binder, half finished, no real person's answers, run through The Binder's own code: "
            "the binder screen reads: %s It words each section like this. What is written in a "
            "section is never shown here, or anywhere but your own browser." % THEBINDER_HEADLINE), \
        _table(["Section", "Time", "What The Binder says"], THEBINDER)


def _doorstop():
    return ("An invented year, no real landlord's: two units at one address, 22 rent payments and 11 costs, "
            "run through Doorstop's own Schedule E code. The new roof might be an improvement and the owner has not "
            "said, and one receipt has no line, so both are held out of the totals and listed instead. "
            "Depreciation is not calculated."), \
        _table(["Unit", "On the working papers", "Amount"], DOORSTOP)
def _threshold():
    return ("An invented ten-year-old with an iPhone, YouTube and Roblox, run through Threshold's own code: "
            "the eight controls it lists, in the order it sets, with the date each one's steps were last checked "
            "against the platform's own instructions. The steps themselves are what the key opens."), \
        _table(["", "On", "Control", "What to do", "Last checked"], THRESHOLD)


# FirstDay (2026-11-18): lib/sample.ts's invented newsletter filed through the
# app's own code (localStore.fileRecord, explodeRecord), each date run through
# phraseFor() (lib/deadlines.ts) and calendarDeadlines()/alarmLead()
# (lib/calendar.ts) for 2026-11-18 at the default 5 days and 7am, by scratchpad
# firstday-sample.mts. Values pasted, not written.
FIRSTDAY = [
    ("Book fair volunteer sign-up", "Due in 9 days.",
     "Read as 2026-11-27. Asks you to confirm it first; nothing in your calendar until you do"),
    ("Aquarium trip permission slip", "Needs signing and returning in 12 days.",
     "In your calendar on 2026-11-30, with an alarm on 2026-11-25 at 7am"),
    ("Aquarium trip fee", "Payment due in 12 days.",
     "In your calendar on 2026-11-30, with an alarm on 2026-11-25 at 7am"),
    ("Picture day", "Happening in 15 days.",
     "In your calendar on 2026-12-03, with an alarm on 2026-11-30 at 7am"),
    ("Three supply requests", "Headphones for library time, needed by 2026-11-23; 4 Glue sticks; 1 Box of tissues",
     "Adds them to one supply list, across every letter and every child"),
]


def _firstday():
    return ("One invented class newsletter, no real family's or school's, filed on November 18, 2026 and run "
            "through FirstDay's own code. Mia is matched to the child set up as Mia Lane. The volunteer date was "
            "only implied (\"by the end of next week\"), so it asks before anything is scheduled; the other three "
            "were stated plainly. The winter concert, with no date yet, is shown as read but not filed."), \
        _table(["In the letter", "What FirstDay says", "What FirstDay does"], FIRSTDAY)


# Pantry (2026-11-19): an invented receipt dated November 16 and one typed
# line, run on November 19 through lib/pantry.ts receiptItems(), parseQuickAdd(),
# byUrgency() and freshnessPhrase() at Pantry be05e52, by scratchpad
# pantry-sample.mts. Values pasted, not written.
PANTRY = [
    ("chicken thighs", "Fridge", "Receipt, about 2 days", "Was yesterday"),
    ("baby spinach", "Fridge", "Receipt, about 5 days", "2 days"),
    ("leftover chili", "Fridge", "Typed: leftover chili fridge 2", "2 days"),
    ("whole milk", "Fridge", "Receipt, about 7 days", "4 days"),
    ("cheddar", "Fridge", "Receipt, about 28 days", "2026-12-14"),
    ("frozen peas", "Freezer", "Receipt, about 240 days", "2027-07-14"),
    ("long grain rice", "Cupboard", "Receipt, keeps", "No date, listed last"),
]


def _pantry():
    return ("One invented grocery receipt from November 16, no real household's, plus one line typed by hand, "
            "as Pantry's own code lists them on November 19. Each receipt date is the typical shelf life for that "
            "kind of food added to the day of the shop, a guess you can change. Soonest first, so the chicken is "
            "what tonight's idea should use up, and the rice sits at the bottom rather than vanishing."), \
        _table(["Item", "Kept", "Where the date came from", "Shown as"], PANTRY)


# Trade Desk (2026-11-19): an invented job run through the app's own code:
# lib/money.ts total() at 8.25% and lib/invoiceDocument.ts invoiceText() for
# invoice 1041, by scratchpad tradedesk-sample.mts at TradeDesk 48e4010.
# Values pasted, not written.
TRADEDESK = [
    ("Labor, 6.5 hours at $95.00", "No", "$617.50"),
    ("40 gallon gas water heater", "Yes", "$1,149.00"),
    ("Expansion tank and flex connector", "Yes", "$89.00"),
    ("Haul away the old heater", "No", "$75.00"),
    ("Subtotal", "", "$1,930.50"),
    ("Tax at 8.25%, once on the $1,238.00 that is taxable", "", "$102.14"),
    ("Total on invoice 1041", "", "$2,032.64"),
]


# Fluent Hour (2026-11-19): an invented opening and first line in French, run
# through lib/localStore.ts saveSettings(), takeTurn() and gateBody() at
# FluentHour 6c732b7 with the network replaced by a recorder, by scratchpad
# fluenthour-sample.mts. The body the browser sends, pasted, not written.
FLUENTHOUR = [
    ("Language and level", "fr, beginner"),
    ("Situation", "Ordering at a bakery where they have run out of what you wanted"),
    ("The conversation so far", "One turn: the partner's opening, \"Bonjour ! Désolée, il n'y a plus de croissants. Je vous mets un pain au chocolat ?\""),
    ("What you said, as words", "Oui, je veux un pain au chocolat"),
    ("Not sent", "Your voice, your name or email, any other conversation"),
]


def _fluenthour():
    return ("One invented exchange at a bakery, no real learner's, run through Fluent Hour's own code: everything "
            "the browser sends for the learner's first line. The reply comes back with a correction only when one "
            "is worth making, and the conversation is kept in that browser, not on our server."), \
        _table(["Sent for one turn", "In this example"], FLUENTHOUR)


# Homeroom (2026-11-19): lib/sample.ts's invented family (Iris, Year 7, in
# Pennsylvania: 57 school days logged, one filing marked done) run through
# lib/compliance.ts ruleStatuses() and attendanceTotals() over the REAL rule
# corpus in lib/states.ts (rechecked 2026-11-19) at Homeroom 10589c1, for
# 2026-11-19, by scratchpad homeroom-sample.mts. Values pasted, not written.
HOMEROOM = [
    ("Notice to file", "File a notarised affidavit with the district before you start, then by 1 August each year.",
     "24 P.S. §§ 13-1327.1(b)(1), 13-1327(d)", "Done, 14 August"),
    ("Parent qualification", "The supervising parent needs a high school diploma or its equivalent.",
     "24 P.S. § 13-1327.1(a), (m)", "Open"),
    ("Subjects", "Teach the subjects the statute lists for elementary and secondary levels.",
     "24 P.S. § 13-1327.1(c)-(d)", "Open"),
    ("Attendance", "180 days, or 900 hours at elementary and 990 hours at secondary, each year.",
     "24 P.S. § 13-1327.1(c)", "Open: 57 days and 269.5 hours so far; 8 of those days have no hours against them"),
    ("Portfolio", "Keep a portfolio of materials, work samples and standardised test results.",
     "24 P.S. § 13-1327.1(e), (h.1)", "Open"),
    ("Assessment", "Standardised tests in reading and mathematics in grades 3, 5 and 8.",
     "24 P.S. § 13-1327.1(e)(1)", "Open"),
]


def _homeroom():
    return ("One invented family, no real one: Iris, in Year 7 in Pennsylvania, on November 19, 2026, run through "
            "Homeroom's own code. Only her records are invented (the days logged and one filing marked done). Every "
            "rule and citation is the app's real Pennsylvania corpus, last checked November 19, 2026. These are "
            "summaries for a parent, not legal advice."), \
        _table(["Requirement", "What Pennsylvania asks", "The statute", "Where Iris stands"], HOMEROOM)


# Stuck (2026-11-20): lib/sample.ts's invented learner (Amara, grades 6 to 8)
# and her first invented problem, run through lib/localStore.ts gateBody() at
# Stuck b59e3c1 as the Start button runs it (no earlier turns; the opening line
# is the problem as typed), by scratchpad stuck-sample.mts. No tutor words are
# shown: lib/sample.ts forbids inventing what the tutor says to a child.
STUCK = [
    ("Grade", "6 to 8"),
    ("Subject", "Maths"),
    ("The problem, as typed", "2/3 + 1/4 and I keep getting 3/7"),
    ("The conversation so far", "None yet: this is the opening turn"),
    ("Not sent", "Amara's name, your name or email, any other session"),
]


def _stuck():
    return ("One invented problem, no real child's, run through Stuck's own code: everything the browser sends "
            "when a child starts. The tutor's reply comes back as one question, and the session is kept in that "
            "browser, not on our server. Every reply is written live by the tutor, for your child's own "
            "problem."), \
        _table(["Sent for the opening turn", "In this example"], STUCK)


# PillProof (2026-11-20): one invented household (Rose, her two medicines, Dan
# and Priya recording) run through PillProof's own web code at ae178d7,
# lib/localStore.ts then lib/familySummary.ts, by scratchpad
# pillproof-sample.mts. The rows are the summary's own lines for the two days
# recorded, word for word; the five days before say "Nothing recorded in this
# browser." No counts, rates or scores, because the app shows none.
PILLPROOF = [
    ("Fri 20 Nov, 8am", "Amlodipine (5mg tablet)", "taken, 8:04am, Rose"),
    ("Fri 20 Nov, 8am", "Metformin (500mg tablet)", "taken, 8:05am, Rose"),
    ("Fri 20 Nov, 6pm", "Metformin (500mg tablet)", "not yet"),
    ("Thu 19 Nov, 8am", "Amlodipine (5mg tablet)", "taken, 8:10am, Dan"),
    ("Thu 19 Nov, 8am", "Metformin (500mg tablet)", "taken, 8:12am, Dan"),
    ("Thu 19 Nov, 6pm", "Metformin (500mg tablet)", "skipped: they have run out, recorded by Priya"),
]


def _pillproof():
    return ("One invented family, no real person's, run through PillProof's own code: the doses section of the "
            "summary a carer downloads for the rest of the family. Each dose says what happened and whose word it "
            "is, exactly as recorded, and the medicine exactly as typed from the box. A day nobody opened PillProof "
            "says \"Nothing recorded in this browser\" rather than showing as missed."), \
        _table(["Due", "Medicine, as typed", "What was recorded"], PILLPROOF)


# Handoff (2026-11-20): one invented family (Dana, Marcus and Ivy), no real
# person's, run through Handoff's own web code at 3bbd297 by scratchpad
# handoff-sample.mts: five messages sealed with lib/chain.ts seal(), an agreed
# and a not-agreed expense, a weekend swap with its reason, then the November
# export from lib/webRecord.ts buildWebExport() (lib/handoff.ts buildExport
# with the VERIFICATION DATA appendix). Printed WHOLE, word for word, so a
# visitor can paste it into /handoff/verify/ and see it check out; change a
# word in it and the check says where. To refresh, re-run the script and
# paste its output here.
HANDOFF = r'''COMMUNICATION AND EXPENSE RECORD

Arrangement: Ivy
Period: 2026-11-01 to 2026-11-30
Generated: 2026-11-30T20:14:05.118Z
Generated by: Dana

Parties:
  Dana
  Marcus

Children:
  Ivy (born 2018-03-14)

======================================================================

ABOUT THIS RECORD

Messages in this app cannot be edited or deleted by either party. Each one
carries a cryptographic hash of the message before it, so removing,
altering or reordering any message breaks every hash that follows it.

This record contains EVERY message between the parties in the period above.
The app provides no way to export a filtered selection.

What this does not establish:
  - It shows that messages were not altered after being sent. It says
    nothing about whether their contents are true.
  - Timestamps are the server's clock. This is not an independent
    timestamping authority.
  - The chain cannot by itself prove that messages after the last one shown
    were not omitted. The totals below are stated so that the other party,
    who holds the same log, can confirm them against their own copy.

VERIFICATION

  Chain verified: 5 messages, all hashes consistent.
  Total messages in this arrangement: 5
  Messages in this period: 4
  Final chain hash: 513bb4b6824b03416807f8b12d85fb0282dfe44d12da0a54cdcfa425a14a2a42
  Final sequence number: 5

======================================================================

MESSAGES

[2] 2026-11-02T09:15:03.507Z · Marcus
    Can we swap the weekend of the 14th? My sister's wedding is that Saturday.
    hash 2d18f88cb1f1b185…

[3] 2026-11-02T12:01:44.090Z · Dana
    Yes. I will have her the weekend of the 21st instead.
    hash ee939591a14a682b…

[4] 2026-11-09T19:30:21.664Z · Marcus
    I have added the swim lessons. The term starts on the 16th.
    hash 9c38b79f0b7ac653…

[5] 2026-11-10T07:58:12.205Z · Dana
    I had not seen the swim lessons before they were booked, so I have marked them not agreed for now. Can we talk on Thursday?
    hash 513bb4b6824b0341…

======================================================================

EXPENSES

2026-11-04  School shoes  USD 64.00  [agreed]
    raised by Dana, 50% asked of the other party

2026-11-09  Swim lessons, autumn term  USD 180.00  [disputed]
    raised by Marcus, 50% asked of the other party
    response: Not discussed before booking

======================================================================

CHANGES TO THE USUAL PATTERN

2026-11-14  Swapped weekends for a family wedding
2026-11-21  Swapped weekends for a family wedding

======================================================================

VERIFICATION DATA

One line per message in the arrangement, so the chain can be checked from
its first message. Messages in the period above carry the seven fields the
chain is computed over. Messages outside it carry only their number and
their two hashes, so their text is not printed here. Anyone can check these
lines, without an account or a key, at https://carrierpress.com/handoff/verify/

{"seq":1,"content_hash":"ce7bac8cc27881e2544822b8d1ecaa749aebe104aa69924bbcc72728429ec782","chain_hash":"c1ebfcea71033609df3ab501eb4fcd7dea98610de691eb0d541c646ea884a605"}
{"seq":2,"author_ref":"a93e0d4b-7f12-4e6a-8c35-b1d2e4f60a7c","author_name":"Marcus","sent_at":"2026-11-02T09:15:03.507Z","body":"Can we swap the weekend of the 14th? My sister's wedding is that Saturday.","content_hash":"ef7df2016e12f5876e668155052cee20855b598b1950b6845772b770c4abc301","chain_hash":"2d18f88cb1f1b185910a77dc9d47403d97bbd69329c62b793f00828756bdc913"}
{"seq":3,"author_ref":"5c1f8e2a-3b7d-4c9e-a061-2f4d8b7c9e10","author_name":"Dana","sent_at":"2026-11-02T12:01:44.090Z","body":"Yes. I will have her the weekend of the 21st instead.","content_hash":"70fde102d748128e32c1e74903fd38a23638863163bf328905a496a07f35dd52","chain_hash":"ee939591a14a682b8a934b268a30ee04047b1142b1bf830b33a9eeb37319d44a"}
{"seq":4,"author_ref":"a93e0d4b-7f12-4e6a-8c35-b1d2e4f60a7c","author_name":"Marcus","sent_at":"2026-11-09T19:30:21.664Z","body":"I have added the swim lessons. The term starts on the 16th.","content_hash":"4e94d4faca2793df876727aa4f0ad061c28c27dfbd4442e746ebc8f11c5c82df","chain_hash":"9c38b79f0b7ac653704b0a9c94ea87985e1146f57c09dbbc34141f39414965a5"}
{"seq":5,"author_ref":"5c1f8e2a-3b7d-4c9e-a061-2f4d8b7c9e10","author_name":"Dana","sent_at":"2026-11-10T07:58:12.205Z","body":"I had not seen the swim lessons before they were booked, so I have marked them not agreed for now. Can we talk on Thursday?","content_hash":"4995a59462c77ed20d12e8a9ad1db08fdd6bed57cd369ae3b7a54882535b6d8e","chain_hash":"513bb4b6824b03416807f8b12d85fb0282dfe44d12da0a54cdcfa425a14a2a42"}

======================================================================

End of record.'''

HANDOFF_CSS = ("<style>.pf-pre{max-height:30em;overflow:auto;margin:0;padding:14px 16px;border:1px solid var(--line,#ddd);"
               "border-radius:8px;background:var(--paper-2,#f6f4ef);color:var(--ink,#111);font:12.5px/1.5 ui-monospace,Menlo,Consolas,monospace;"
               "white-space:pre;tab-size:4}.pf-after{max-width:62ch;margin:14px 0 0}</style>")


def _handoff():
    return ("One invented family, no real person's, run through Handoff's own code: five messages, a pair of expenses "
            "and a weekend swap, exported for November. This is the whole export, exactly as the app writes it, "
            "including what it does not prove and the verification data at the end. Message 1 falls before November, "
            "so the appendix carries it as hashes only, without its text."), \
        (HANDOFF_CSS + '<pre class="pf-pre" tabindex="0" aria-label="A Handoff export for an invented family">%s</pre>'
         '<p class="pf-after">Copy all of it into <a href="/handoff/verify/">the record checker</a> and it checks out. '
         'Change one word of a message in the verification data and the checker says which message stopped matching. '
         'Expenses show the app\'s own status words: "disputed" is shown in the app as Not agreed.</p>' % e(HANDOFF))


def _tradedesk():
    return ("One invented job, no real tradesperson's or customer's: a water heater swap, quoted and invoiced "
            "through Trade Desk's own code. Tax is worked once on the taxable lines, not line by line, and the "
            "invoice prints the payment instructions written in Account in place of a card link."), \
        _table(["Line", "Taxed", "Amount"], TRADEDESK)


# Crosscheck (2026-11-21): its own sample fixtures (lib/sample.ts SAMPLE_BILL,
# SAMPLE_EOB, SAMPLE_INPUTS: an invented emergency visit) run through its own
# code at ~/Projects/Crosscheck 0c1fdaa, lib/detect.ts detect() then
# lib/letter.ts billingOfficeLetter(), by scratchpad crosscheck-sample.mts
# (node --experimental-strip-types), 2026-11-21. Findings word for word, in the
# detector's order (largest first), with the case screen's own line for
# "arithmetic". The letter is its first six paragraphs word for word; the date
# is the day the script ran, as the app writes the day a letter is drafted.
# assertNoLegalClaims() found 0 sentences in all three letters.
CROSSCHECK = [
    ("$468.00", "The bill asks for $1,310.00. The Explanation of Benefits puts your share at $842.00. "
                "That is a difference of $468.00.", "This is subtraction between your two documents."),
    ("$26.00", "The line items add up to $2,814.00, but the total on the bill is $2,840.00. "
               "That is $26.00 apart.", "This is subtraction between your two documents."),
]
CROSSCHECK_SUBJECT = "Query on account A-55127"
CROSSCHECK_LETTER = [
    "November 21, 2026",
    "To the billing office at Riverbend Regional,",
    "I am writing about account A-55127, for services on 2026-07-14.",
    "The bill I received asks me to pay $1,310.00. The Explanation of Benefits from Northgate Health lists "
    "my responsibility as $842.00. The two differ by $468.00.",
    "The line items add up to $2,814.00, but the total on the bill is $2,840.00. That is $26.00 apart.",
    "Please could you review the account and let me know how the amount was worked out. If the difference "
    "is an error I would be grateful if you could correct it. If it is not, please could you explain what it "
    "is for, so I understand what I am being asked to pay.",
]
CROSSCHECK_CSS = ("<style>.pf-letter{max-width:62ch;margin:22px 0 0;padding:18px 20px;border:1px solid var(--line,#ddd);"
                  "border-radius:8px;background:var(--paper-2,#f6f4ef)}.pf-letter p{margin:0 0 10px;line-height:1.6}"
                  ".pf-letter .pf-subj{font-weight:700}.pf-after{max-width:62ch;margin:14px 0 0}</style>")


def _crosscheck():
    letter = "".join("<p>%s</p>" % e(x) for x in CROSSCHECK_LETTER)
    return ("One invented emergency visit, no real patient's, run through Crosscheck's own code: the bill asks "
            "for $1,310.00 and the insurer's Explanation of Benefits puts the patient's share at $842.00. Here "
            "are the findings it reports, largest first, word for word, then the opening of the letter it drafts "
            "to the billing office."), \
        (CROSSCHECK_CSS + _table(["Difference", "What Crosscheck found", "What it is"], CROSSCHECK)
         + '<div class="pf-letter" aria-label="The start of a letter Crosscheck drafted"><p class="pf-subj">%s</p>%s</div>'
         '<p class="pf-after">The letter goes on to offer anything that would help, then your own reason, exactly as you '
         'typed it, and your name. '
         'Every sentence Crosscheck wrote above is a figure from the two documents, a question or a request.</p>'
         % (e(CROSSCHECK_SUBJECT), letter))


# Spellbright (2026-11-22): three What's the Word? questions made by its own
# code at ~/Projects/Spellbright 356216d, lib/whatsword.ts newRound() over the
# reviewed clue book (lib/words/clues.json) and word lists
# (lib/words/bands.json), seeded rounds run by scratchpad
# spellbright-sample/sample.mts (node --experimental-strip-types): ages 4 to 5
# (band a, seed 2026) questions 1 and 3, ages 6 to 7 (band b, seed 2026)
# question 1. Picture, meaning and choices word for word and in the order shown;
# the choices are lowercase as the game shows them. Each "<word> means: <meaning>"
# line is the game's own line under a wrong pick (app/whatsword.tsx), with the
# clue book's meaning for that word.
SPELLBRIGHT = [
    ("Ages 4 to 5", "\U0001F68C", "a big long car that carries lots of people", ["tune", "bus", "week"], 1,
     ["tune means: a song you can hum", "week means: seven days in a row"]),
    ("Ages 4 to 5", "\U0001F3DE️", "a green place with grass, trees and a swing", ["dog", "park", "girl"], 1,
     ["dog means: a furry pet that barks and wags its tail", "girl means: a child who will grow up to be a woman"]),
    ("Ages 6 to 7", "\U0001F3B5", "to sing with your lips closed", ["seen", "hum", "feed", "bid"], 1,
     ["seen means: looked at with your eyes", "feed means: to give food to a person or animal",
      "bid means: to offer a price for something you want to buy"]),
]
SPELLBRIGHT_CSS = "<style>.pf-q .pf-pic{font-size:2.2rem;line-height:1;display:block;margin:0 0 6px}</style>"


def _spellbright():
    out = []
    for age, pic, meaning, choices, right, taught in SPELLBRIGHT:
        buttons = "".join('<button type="button"%s>%s</button>' % (" data-right" if i == right else "", e(w))
                          for i, w in enumerate(choices))
        out.append('<div class="pf-q"><p><span class="pf-pic" aria-hidden="true">%s</span><b>%s.</b> %s</p>'
                   '<div class="pf-opts">%s</div><p class="pf-why" hidden>%s</p></div>'
                   % (e(pic), e(age), e(meaning), buttons, "<br>".join(e(t) for t in taught)))
    return ("Three clues from What's the Word?, made by Spellbright's own code from its reviewed clue book: two "
            "from a round for ages 4 to 5, where every clue has a picture, and one for ages 6 to 7. Which word "
            "is it? Tap one to see. In the game, a wrong pick shows what that word does mean, so every miss "
            "teaches a word."), SPELLBRIGHT_CSS + "".join(out)


# Potluck (2026-11-22): the flyer its own code prints, for its own sample street.
# Potluck 4fc24f6, lib/webStreet.ts sampleStreet() through flyerLines() (the
# function cardsHtml's sibling flyerHtml prints from), run by scratchpad
# potluck-sample/sample.mts with TZ=America/New_York and "now" Monday
# 2026-11-23 9am. Titles, times, places and the shelf word for word and in
# order. The sample street is invented and labelled as one in the app.
POTLUCK_WEEK = [
    ("Could someone help carry a sofa upstairs?", "Tuesday, Nov 24, 6pm", None),
    ("Slow run, all paces, back by 8", "\u21bb Every Wednesday, 7am", "Corner of Elm and Third"),
    ("Leaf raking on the green, bags provided", "Friday, Nov 27, 10am", "The green at the end of Elm"),
]
POTLUCK_NOTES = [("Water off Thursday morning for the main", None)]
POTLUCK_SHELF = [("Extension ladder", False), ("Pressure washer", True), ("Folding tables (4)", False)]
POTLUCK_CSS = ("<style>.pf-flyer{background:#fff;color:#1c1a17;border:1px solid #e2ded7;border-radius:10px;"
               "padding:18px 20px;max-width:560px;font-family:Georgia,serif}.pf-flyer h3{font-size:1.35rem;margin:0 0 2px}"
               ".pf-flyer h4{font-size:1rem;margin:14px 0 4px}.pf-flyer ul{margin:0;padding-left:20px}"
               ".pf-flyer li{margin:6px 0}.pf-flyer .m{color:#5e5850;font-size:.88rem}</style>")


def _potluck():
    def li(title, rest):
        return "<li><b>%s</b>%s</li>" % (e(title), '<br><span class="m">%s</span>' % e(rest) if rest else "")
    week = "".join(li(t, ", ".join(x for x in (w, p) if x)) for t, w, p in POTLUCK_WEEK)
    notes = "".join(li(t, p or "") for t, p in POTLUCK_NOTES)
    shelf = "".join("<li>%s%s</li>" % (e(n), ' <span class="m">(out at the moment)</span>' if out else "")
                    for n, out in POTLUCK_SHELF)
    return ("The weekly flyer, as Potluck's own code prints it for the sample street anyone can look round in the "
            "app: this week, the lending shelf, and how to join. It carries no names and no addresses, so it can go "
            "through every door, including the ones that will never open an app."), \
        (POTLUCK_CSS + '<div class="pf-flyer" aria-label="A sample weekly flyer"><h3>On Elm Street this week</h3>'
         '<p class="m">From your neighbours on Potluck</p><h4>This week</h4><ul>%s</ul><h4>Just so you know</h4>'
         '<ul>%s</ul><h4>On the lending shelf</h4><ul>%s</ul><p class="m">Ask on Potluck to borrow. Nobody gets '
         'chased; things just come back.</p><h4>Join your street</h4><p class="m">If a Potluck door card came '
         'through your door, go to <b>carrierpress.com/potluck/app</b> and type its code. No card yet? Ask whoever '
         'put this through your door. It is free for you, and we never ask for your address.</p></div>'
         % (week, notes, shelf))


# Bench (2026-11-22): one invented book (The Lantern Keeper) run through
# Bench's own code at e82f4f4 by scratchpad bench-sample.mts: cleanRun() and the
# fields userMessage() sends for a listing package, then lib/flags.ts flagsFor()
# on five lines WE wrote to show the checks, word for word. No desk draft is
# shown: a draft is written live by the model, for the subscriber's own book.
BENCH_SENT = [
    ("Desk and job", "Author desk, Listing package"),
    ("Title", "The Lantern Keeper"),
    ("Genre", "Middle grade mystery"),
    ("Who it is for", "Readers of seaside adventure mysteries, ages 9 to 12"),
    ("The book", "Twelve-year-old Nell inherits a lighthouse that nobody has lit in forty years. On her first night there, someone lights it anyway."),
    ("Not sent", "Your name, your email, your past drafts"),
]
BENCH_FLAGS = [
    ("The bestselling mystery of the year.", "\u201cbestselling\u201d: a best-seller claim needs sales data behind it."),
    ("Paperback ISBN: [to be assigned]", "\u201c[to be assigned]\u201d: a placeholder is still in the draft; fill it or take it out before it is printed."),
    ("ISBN 979-8-0000-0001-9, when you typed 979-8-0000-0001-2", "\u201c979-8-0000-0001-9\u201d: an ISBN you did not type; never print an ISBN that is not yours."),
    ("Six keywords", "\u201c6 keywords\u201d: KDP has seven keyword boxes; use all seven."),
    ("Subtitle: A Novel", "\u201cA Novel\u201d: Carrier Press house rule: no \"A Novel\" in the subtitle."),
]


# The Errands desk (2026-11-23): one invented errand run through Bench 1eda159
# cleanRun(), then refusalFor() on three plans WE wrote, word for word
# (scratchpad errands-sample.mts). No plan the model wrote is shown.
ERRANDS_SENT = [
    ("What needs doing", "Renew the dog's rabies shot before the kennel stay on 12 December"),
    ("What you already know", "We used Elm Street Vets last year."),
    ("Addresses a draft may go to", "front@elmstreetvets.example"),
]
ERRANDS_REFUSED = [
    ("A step that books the appointment", 'Refused: a step asked to "book". Bench does not act on your behalf, so the whole plan was thrown away rather than partly used.'),
    ("A plan with no step for you to do", "Refused: the plan had no step for you to do, so it thought it had finished the job."),
    ("A message addressed to someone you did not name", "Refused: a draft was addressed to billing@other.example, which is not one of the addresses you gave."),
]


def _bench():
    return ("Run through Bench's own code: one invented book and one invented errand, no real person's. What the "
            "browser sends for each, the checks run on lines we wrote to show them, and three plans we wrote that "
            "the Errands desk refuses. Every real draft and plan is written live, for you, and kept in your "
            "browser, not on our server."), \
        _table(["Sent for a listing package", "In this example"], BENCH_SENT) + \
        _table(["If a draft said", "Bench shows"], BENCH_FLAGS) + \
        _table(["Sent to the Errands desk", "In this example"], ERRANDS_SENT) + \
        _table(["If a plan had", "Bench refuses it whole and says"], ERRANDS_REFUSED)


PROOFS = {"endorsed": _cleared, "boatready": _boat, "whoserves": _whoserves, "conceptionzodiac": _zodiac,
          "cancelled": _cancelled, "downpour": _downpour, "cast": _cast,
          "flare": _flare, "soleledger": _soleledger, "quiet": _quiet, "titrate": _titrate,
          "doorstop": _doorstop,
          "threshold": _threshold,
          "papertrail": _papertrail,
          "throughthegate": _throughthegate,
          "vetpocket": _vetpocket,
          "thebinder": _thebinder,
          "firstday": _firstday,
          "tradedesk": _tradedesk,
          "pantry": _pantry,
          "fluenthour": _fluenthour,
          "homeroom": _homeroom,
          "stuck": _stuck,
          "pillproof": _pillproof,
          "handoff": _handoff,
          "crosscheck": _crosscheck,
          "spellbright": _spellbright,
          "potluck": _potluck,
          "bench": _bench}


def block(slug):
    lede, body = PROOFS[slug]()
    return ('<section class="wrap lp pf" aria-labelledby="h-proof"><h2 class="lp-h2" id="h-proof">See it working</h2>'
            '<p class="pf-lede">%s</p>%s</section>' % (e(lede), body))


CSS = """<style>
.gate{margin:22px 0 0;max-width:460px;font-family:var(--sans)}
.gate label{display:block;color:#fff;font-size:14px;font-weight:600;margin:0 0 6px}
.gate-row{display:flex;gap:8px;flex-wrap:wrap}
.gate input{flex:1 1 220px;min-width:0;padding:11px 12px;border:1px solid rgba(255,255,255,.7);border-radius:8px;font-size:15px;background:#fff;color:#111}
.gate button,.gate-open a{padding:11px 16px;border-radius:8px;border:1px solid #fff;background:transparent;color:#fff;font-size:15px;font-weight:600;cursor:pointer;text-decoration:none;display:inline-block}
.gate button:disabled{opacity:.6;cursor:wait}
.gate-open a{background:#fff;color:var(--accent)}
.gate .gate-forget{border:0;padding:6px 0;margin-left:14px;font-size:13px;font-weight:400;text-decoration:underline}
.gate-note{min-height:1.3em;margin:8px 0 0;color:#fff;font-size:14px}
.gate-note.bad{font-weight:600}
.gate small{display:block;color:rgba(255,255,255,.8);font-size:12px;margin-top:6px}
.pf-lede{max-width:62ch}
.pf-wrap{overflow-x:auto}
.pf-table{border-collapse:collapse;width:100%;font-size:15px}
.pf-table th,.pf-table td{text-align:left;padding:8px 12px 8px 0;border-bottom:1px solid var(--line,#ddd);vertical-align:top}
.pf-q{margin:0 0 22px;max-width:62ch}
.pf-q p{margin:0 0 8px}
.pf-opts{display:flex;flex-wrap:wrap;gap:8px}
.pf-opts button{padding:9px 12px;border:1px solid var(--muted,#777);border-radius:8px;background:transparent;color:inherit;font:inherit;cursor:pointer;text-align:left}
.pf-opts button:disabled{cursor:default}
.pf-opts button.right{border-width:2px;font-weight:700}
.pf-opts button.right::before{content:"\\2713 "}
.pf-opts button.wrong{text-decoration:line-through}
.pf-why{margin-top:10px!important}
.pf-audio{width:100%;max-width:460px}
.pf-hear{padding:10px 16px;border:1px solid var(--muted,#777);border-radius:8px;background:transparent;color:inherit;font:inherit;font-weight:600;cursor:pointer;margin:0 0 14px}
.pf-lines p{margin:0 0 8px;max-width:62ch}
.pf-list{max-width:62ch;padding-left:1.2em}
.pf-list li{margin:0 0 10px}
.pf-lines b{font-weight:600;margin-right:6px}
</style>"""
