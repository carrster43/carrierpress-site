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


PROOFS = {"cleared": _cleared, "boatready": _boat, "whoserves": _whoserves, "conceptionzodiac": _zodiac,
          "cancelled": _cancelled, "downpour": _downpour, "cast": _cast}


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
.pf-lines b{font-weight:600;margin-right:6px}
</style>"""
