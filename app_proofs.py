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
        ["Born", "Birth sign", "Conception, full term", "Sign at conception", "Could also be"],
        [("March 15, 1990", "Pisces", "About June 21, 1989", "Cancer", "Gemini")])


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
            "things it reported, in its own words. It names no employer's system and gives no score."), \
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
            "what the Due tab says about each treatment. The 2am answer is not shown here: it comes only from a "
            "real question about a real animal, and is never written by hand."), \
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
            "browser, not on our server. We do not show a made-up reply here: what Stuck says to a child is only "
            "ever written live, by the tutor."), \
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


def _tradedesk():
    return ("One invented job, no real tradesperson's or customer's: a water heater swap, quoted and invoiced "
            "through Trade Desk's own code. Tax is worked once on the taxable lines, not line by line, and the "
            "invoice prints the payment instructions written in Account in place of a card link."), \
        _table(["Line", "Taxed", "Amount"], TRADEDESK)


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
          "pillproof": _pillproof}


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
