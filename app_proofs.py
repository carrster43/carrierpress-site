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
    return ("A few lines from The Runaway Crate. The button reads them in your browser's own computer voices, "
            "as Cast does, with the narrator and each character in a different voice where your browser has enough."), (
        '<button type="button" id="pf-hear" class="pf-hear">Hear these lines</button><div id="pf-lines" class="pf-lines">%s</div>' % lines)


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


PROOFS = {"cleared": _cleared, "boatready": _boat, "whoserves": _whoserves, "conceptionzodiac": _zodiac,
          "cancelled": _cancelled, "downpour": _downpour, "cast": _cast,
          "flare": _flare, "soleledger": _soleledger, "quiet": _quiet, "titrate": _titrate}


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
