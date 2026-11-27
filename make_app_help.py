#!/usr/bin/env python3
"""
Free help pages for the apps (2026-11-27, "app help pages first"):

  /apps/endorsed/practice/             free practice tests, one per credential
  /apps/endorsed/practice/<pack>/      the pack's exam note, first study section
                                       and its 10 free questions, with answers
  /apps/boatready/requirements/        boat safety equipment by boat length
  /apps/boatready/requirements/<band>/ the federal carriage list for that size,
                                       and what each common difference adds

    python3 make_app_help.py      # build.py runs it too, before the sitemap

WHY. People search "CDL air brakes practice test" and "boat safety equipment
requirements 16 ft". A page that answers exactly that ranks, and each one
leads to the app that answers the rest.

THE WORDS ARE THE APPS' OWN. help_data/*.json is exported from each app's code
by export_app_help.ts (LOCAL ONLY), so these pages can never say what the app
does not: Endorsed's reviewed packs with their citations, and Boat Ready's
requirementsFor(), which is checked against the CFR. Nothing here gives away
more than the app already gives free (Endorsed: first section + first 10
questions; Boat Ready: checking a boat is free).

Rules kept here: no em or en dashes.
"""
import datetime, html, json, pathlib, re

import nav

DOMAIN = "carrierpress.com"
DATA = pathlib.Path("help_data")
HUBS = {"endorsed": ("/apps/endorsed/practice/", "Free practice tests, with answers"),
        "boatready": ("/apps/boatready/requirements/", "Required safety equipment by boat length")}

# The name people search for, where the pack's own title is not it.
SEARCH_NAME = {
    "cdl-general": "CDL General Knowledge Practice Test",
    "air-brakes": "CDL Air Brakes Practice Test",
    "combination": "CDL Combination Vehicles Practice Test",
    "hazmat": "CDL HazMat Endorsement Practice Test",
    "passenger": "CDL Passenger Endorsement Practice Test",
    "school-bus": "CDL School Bus Endorsement Practice Test",
    "tank": "CDL Tanker Endorsement Practice Test",
    "doubles-triples": "CDL Doubles and Triples Practice Test",
    "twic": "TWIC Card Practice Questions",
    "federal-fleet": "Federal Fleet Driving Practice Questions",
    "limo": "Limo and Chauffeur Practice Questions",
    "drone-107": "FAA Part 107 Practice Test",
    "private-pilot": "Private Pilot Knowledge Test Practice Questions",
    "captain-oupv": "USCG Captain (OUPV) Practice Questions",
    "rail-engineer-conductor": "Locomotive Engineer and Conductor Practice Questions",
    "medical-courier": "Medical Courier Practice Questions",
    "animal-transport": "Animal Transport Practice Questions",
    "armored-transport": "Armored Car Guard Practice Questions",
    "fema-nims-ics": "FEMA IS-100, 200, 700 and 800 Practice Questions",
}
MODES = [("road", "On the road"), ("air", "In the air"), ("water", "On the water"),
         ("rail", "On the rails"), ("response", "Emergency response")]
SEVERITY = {"required": "Required", "conditional": "Required in some cases", "state": "Set by your state"}


def e(x):
    return html.escape(str(x), quote=True)


def _fit(*options, limit):
    for o in options:
        if len(o) <= limit:
            return o
    raise SystemExit("make_app_help: nothing fits %d characters: %r" % (limit, options[-1]))


def _ft(x):
    return ("%g" % x)


CSS = """
.ah h1{font-size:clamp(1.8rem,6vw,2.5rem);font-weight:400;letter-spacing:-.02em;margin:0 0 12px}
.ah .lede{font-size:1.08rem;line-height:1.6;color:var(--ink-soft);max-width:66ch;margin:0 0 18px}
.ah h2{font-size:clamp(1.3rem,4vw,1.6rem);font-weight:400;margin:34px 0 10px;padding-top:26px;border-top:1px solid var(--line)}
.ah h3{font-size:1.12rem;margin:22px 0 6px}
.ah p,.ah li{line-height:1.65;max-width:68ch}
.ah-cta{margin:20px 0 8px;padding:16px 18px;border:1px solid var(--line);border-radius:8px;max-width:660px}
.ah-cta p{margin:0 0 12px}
.ah-go{display:inline-block;background:var(--gold);color:#151a33;font-family:var(--sans);font-weight:600;
  font-size:15px;text-decoration:none;padding:11px 18px;border-radius:6px}
.ah-go:hover{background:var(--gold-bright)}
.ah-q{padding-left:1.4em}.ah-q>li{margin:0 0 22px}
.ah-q ol{list-style:upper-alpha;margin:8px 0;padding-left:1.6em}.ah-q ol li{margin:2px 0}
.ah details{margin-top:6px}.ah summary{cursor:pointer;font-family:var(--sans);font-size:14px;font-weight:600;color:var(--ink-soft)}
.ah details p{margin:6px 0}
.ah-src{font-family:var(--sans);font-size:13px;color:var(--muted)}
.ah-item{padding:14px 0;border-bottom:1px solid var(--line);max-width:70ch}
.ah-item h3{margin:0 0 4px}.ah-item p{margin:4px 0}
.ah-tag{display:inline-block;font-family:var(--sans);font-size:12px;font-weight:600;letter-spacing:.02em;
  border:1px solid var(--line);border-radius:999px;padding:2px 9px;margin-left:8px;vertical-align:middle;color:var(--ink-soft)}
.ah-carry{font-weight:600}
.ah-links{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px 18px}
.ah-links a{text-decoration-color:var(--gold)}
.ah-fine{font-family:var(--sans);font-size:13px;color:var(--muted);margin-top:26px;max-width:72ch}
"""

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{domain}{path}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://{domain}{path}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{ld}</script>
<style>{css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="/">
      <img class="mark-dark" src="/assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="/assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>Carrier Press</span>
    </a>
    <nav class="nav" aria-label="Main">
      <a href="/fiction/">Fiction</a>
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
  </div>
</header>
<main id="main">
<section class="wrap ah" style="padding-top:44px;padding-bottom:64px">
"""

FOOT = """</section>
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; {year} Jeffrey L. Carrier. All rights reserved.</span>
      <span><a href="/">Carrier Press LLC</a>, Diamondhead, Mississippi.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def _page(path, title, desc, og_title, og_img, ld_extra, crumbs, body):
    ld = {"@context": "https://schema.org", "@graph": ld_extra + [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": "https://%s%s" % (DOMAIN, u)}
            for i, (n, u) in enumerate(crumbs)]}]}
    s = (HEAD.format(title=e(title), desc=e(desc), domain=DOMAIN, path=path, og_title=e(og_title),
                     og_img=og_img, css=CSS, ld=json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))
         + "\n".join(body) + FOOT.format(year=datetime.date.today().year))
    for bad in ("—", "–", "&mdash;", "&ndash;"):
        if bad in s:
            raise SystemExit("make_app_help: a dash reached %s" % path)
    out = pathlib.Path(path.strip("/")) / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s, encoding="utf-8")
    nav.patch(out)


def _og(slug):
    card = pathlib.Path("apps/og/%s.png" % slug)
    return "https://%s/%s" % (DOMAIN, card.as_posix()) if card.exists() else "https://%s/assets/og-image.png" % DOMAIN


# ── Endorsed ────────────────────────────────────────────────────────────────

def endorsed():
    d = json.loads((DATA / "endorsed.json").read_text(encoding="utf-8"))
    packs, free = d["packs"], d["free"]
    hub = HUBS["endorsed"][0]
    og = _og("endorsed")
    for p in packs:
        if p["id"] not in SEARCH_NAME:
            raise SystemExit("make_app_help: add a SEARCH_NAME for Endorsed pack %r" % p["id"])
    for p in packs:
        name = SEARCH_NAME[p["id"]]
        path = "%s%s/" % (hub, p["id"])
        qs = p["questions"]
        state = any(q.get("basis") == "state-test" for q in qs) or p["first"].get("basis") == "state-test"
        title = (_fit("%s, Free with Answers" % name, name, limit=65) if name.endswith("Questions") else
                 _fit("%s: %d Free Questions with Answers" % (name, len(qs)),
                      "%s: %d Free Questions" % (name, len(qs)), name, limit=65))
        desc = _fit("%d free %s questions with answers and the rule each rests on, plus a study section. "
                    "From Endorsed, which covers %d credentials." % (len(qs), p["title"], len(packs)),
                    "%d free %s questions with answers and the rule each rests on, plus a study section."
                    % (len(qs), p["title"]),
                    "%d free %s questions with answers." % (len(qs), p["title"]), limit=160)
        b = ['<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Endorsed: free practice</span></p>',
             "<h1>%s</h1>" % e(name), '<p class="lede">%s</p>' % e(p["examBy"]),
             '<div class="ah-cta"><p>These are the first %d of the %d questions in Endorsed\'s %s pack, with the '
             'first of its %d study sections. Every answer names the rule it comes from. The full pack, and %d '
             'other credentials, are in Endorsed.</p><a class="ah-go" href="/apps/endorsed/">See Endorsed</a></div>'
             % (len(qs), p["totalQuestions"], e(p["title"]), p["totalSections"], len(packs) - 1),
             '<h2 id="questions">%d practice questions</h2>' % len(qs), '<ol class="ah-q">']
        for q in qs:
            opts = "".join("<li>%s</li>" % e(o) for o in q["options"])
            letter = "ABCD"[q["answer"]]
            b.append('<li><p>%s</p><ol>%s</ol><details><summary>Show the answer</summary>'
                     '<p><strong>%s. %s</strong></p><p>%s</p><p class="ah-src">Source: %s%s</p></details></li>'
                     % (e(q["prompt"]), opts, letter, e(q["options"][q["answer"]]), e(q["why"]), e(q["cite"]),
                        " (state test figure)" if q.get("basis") == "state-test" else ""))
        b.append("</ol>")
        f = p["first"]
        b.append("<h2>Study: %s</h2>" % e(f["title"]))
        b += ["<p>%s</p>" % e(x) for x in f["body"]]
        b.append('<p class="ah-src">Source: %s%s</p>' % (e("; ".join(f["cite"])),
                 " (state test figures)" if f.get("basis") == "state-test" else ""))
        if len(p["sectionTitles"]) > 1:
            b.append("<h2>What else the pack covers</h2><ul>")
            b += ["<li>%s</li>" % e(t) for t in p["sectionTitles"][1:]]
            b.append('</ul><p><a class="ah-go" href="/apps/endorsed/">Study the whole pack in Endorsed</a></p>')
        if state:
            b.append('<p class="ah-fine">Figures marked as state test figures come from the state CDL manuals, '
                     'which can differ from state to state. Check your own state\'s manual.</p>')
        b.append('<h2>More free practice tests</h2><ul class="ah-links">')
        b += ['<li><a href="%s%s/">%s</a></li>' % (hub, o["id"], e(SEARCH_NAME[o["id"]]))
              for o in packs if o["id"] != p["id"]]
        b.append('</ul><p><a href="%s">All free practice tests</a></p>' % hub)
        b.append('<p class="ah-fine">Endorsed is a study aid from Carrier Labs LLC. It is not affiliated with '
                 'any government agency, and it does not give the real test.</p>')
        _page(path, title, desc, name, og,
              [{"@type": "WebPage", "name": name, "url": "https://%s%s" % (DOMAIN, path), "description": desc}],
              [("Home", "/"), ("Apps", "/apps/"), ("Endorsed", "/apps/endorsed/"),
               ("Free practice tests", hub), (p["title"], path)], b)

    desc = ("Free practice questions with answers for the CDL, air brakes, hazmat, tanker, TWIC, FAA Part 107, "
            "USCG captain and more, each cited to its rule.")
    desc = _fit(desc, "Free practice questions with answers for %d transport credentials." % len(packs), limit=160)
    b = ['<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Endorsed: free practice</span></p>',
         "<h1>Free practice tests for transport credentials</h1>",
         '<p class="lede">Ten free questions for each credential in Endorsed, with the answer, the reason and '
         'the rule it rests on. Pick yours.</p>']
    for mode, label in MODES:
        mp = [p for p in packs if p["mode"] == mode]
        if not mp:
            continue
        b.append('<h2>%s</h2><ul class="ah-links">' % e(label))
        b += ['<li><a href="%s%s/">%s</a></li>' % (hub, p["id"], e(SEARCH_NAME[p["id"]])) for p in mp]
        b.append("</ul>")
    b.append('<div class="ah-cta" style="margin-top:30px"><p>The full packs, with every study section and '
             'question, are in Endorsed.</p><a class="ah-go" href="/apps/endorsed/">See Endorsed</a></div>')
    _page(hub, "Free CDL, Hazmat, TWIC and Part 107 Practice Tests", desc,
          "Free practice tests for transport credentials", og,
          [{"@type": "CollectionPage", "name": "Free practice tests", "url": "https://%s%s" % (DOMAIN, hub),
            "description": desc}],
          [("Home", "/"), ("Apps", "/apps/"), ("Endorsed", "/apps/endorsed/"), ("Free practice tests", hub)], b)
    return len(packs) + 1


# ── Boat Ready ──────────────────────────────────────────────────────────────

def _item(r, label=None):
    return ('<div class="ah-item"><h3>%s<span class="ah-tag">%s</span></h3><p class="ah-carry">%s</p>'
            '<p>%s</p><p class="ah-src">%s</p></div>'
            % (e(r["title"]), e(label or SEVERITY.get(r["severity"], r["severity"])), e(r["carry"]),
               e(r["detail"]), e(r["cite"])))


def _changes(added, gone):
    titles = {r["title"] for r in added}
    out = [_item(r) for r in added]
    out += ['<p>No longer needed: %s.</p>' % e(t) for t in gone if t not in titles]
    return out


def boatready():
    d = json.loads((DATA / "boatready.json").read_text(encoding="utf-8"))
    hub = HUBS["boatready"][0]
    og = _og("boatready")
    bands = d["bands"]
    for bd in bands:
        path = "%s%s/" % (hub, bd["slug"])
        kayak = bd["slug"] == "kayak-and-canoe"
        h1 = "Required safety equipment for %s" % bd["name"]
        title = _fit("%s | Boat Ready" % h1.replace("Required safety equipment", "Boat Safety Equipment Required"),
                     "Boat Safety Equipment Required for %s" % bd["name"].replace("a boat ", "Boats ").replace("feet", "Feet").replace("under", "Under"),
                     h1, limit=65)
        if kayak:
            title = "Kayak and Canoe Safety Equipment Requirements | Boat Ready"
        span = ("paddled, under %s feet" % _ft(bd["hi"])) if kayak else \
            ("under %s feet" % _ft(bd["hi"]) if bd["lo"] <= 10 else
             "from %s feet up to, but not including, %s feet" % (_ft(bd["lo"]), _ft(bd["hi"])))
        desc = _fit("What US federal rules require aboard %s: life jackets, signals, extinguishers and more, "
                    "each item cited to the CFR." % bd["name"],
                    "What US federal rules require aboard %s, each item cited to the CFR." % bd["name"], limit=160)
        if kayak:
            desc = ("What US federal rules require aboard a kayak or canoe: life jackets, a sound signal, and "
                    "lights and distress signals when they apply, each cited to the CFR.")
        base_txt = ("a kayak or canoe you paddle, on inland waters, in daylight" if kayak else
                    "a motorboat with an outboard motor, on inland waters, in daylight, 4 people aboard, "
                    "no closed space where fuel vapour can collect, and no installed toilet")
        b = ['<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Boat Ready: free reference</span></p>',
             "<h1>%s</h1>" % e(h1),
             '<p class="lede">The US federal carriage requirements for a recreational boat %s, from Boat Ready\'s '
             'rule list, which is checked against the Code of Federal Regulations (rules as of %s). Each item '
             'names its regulation.</p>' % (e(span), e(d["rulesAsOf"])),
             '<div class="ah-cta"><p>Every boat is different. Boat Ready checks your own boat, any length and any '
             'engine, free.</p><a class="ah-go" href="/apps/boatready/">Check your boat in Boat Ready</a></div>',
             "<h2>The list for the basic boat</h2>",
             "<p>Worked out for %s. The sections after it say what changes.</p>" % e(base_txt)]
        b += [_item(r) for r in bd["base"]]
        for w in bd["within"]:
            b.append("<h2>At %s feet and over</h2>" % _ft(w["from"]))
            b += _changes(w["added"], w["gone"])
        for v in bd["variants"]:
            b.append("<h2>If the boat %s</h2>" % e(v["label"][0].lower() + v["label"][1:]))
            b += _changes(v["added"], v["gone"])
        b.append('<h2>Other boat sizes</h2><ul class="ah-links">')
        b += ['<li><a href="%s%s/">%s</a></li>' % (hub, o["slug"], e(o["name"][0].upper() + o["name"][1:]))
              for o in bands if o["slug"] != bd["slug"]]
        b.append("</ul>")
        b.append('<p class="ah-fine">%s</p>' % e(d["disclaimer"]))
        _page(path, title, desc, h1, og,
              [{"@type": "WebPage", "name": h1, "url": "https://%s%s" % (DOMAIN, path), "description": desc}],
              [("Home", "/"), ("Apps", "/apps/"), ("Boat Ready", "/apps/boatready/"),
               ("Safety equipment by boat length", hub), (bd["name"][0].upper() + bd["name"][1:], path)], b)

    desc = ("US federal boat safety equipment requirements by boat length, for kayaks and canoes up to 65 foot "
            "boats: what to carry, each item cited to the CFR.")
    b = ['<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Boat Ready: free reference</span></p>',
         "<h1>Required boat safety equipment, by boat length</h1>",
         '<p class="lede">What US federal rules require aboard a recreational boat changes with its length, its '
         'engine and where and when you use it. Pick the size closest to yours.</p><ul class="ah-links">']
    b += ['<li><a href="%s%s/">%s</a></li>' % (hub, o["slug"], e(o["name"][0].upper() + o["name"][1:])) for o in bands]
    b += ["</ul>",
          '<div class="ah-cta" style="margin-top:30px"><p>For your own boat, exactly: Boat Ready asks its length, '
          'engine and waters and gives the list, free.</p><a class="ah-go" href="/apps/boatready/">Check your boat '
          'in Boat Ready</a></div>', '<p class="ah-fine">%s</p>' % e(d["disclaimer"])]
    _page(hub, "Boat Safety Equipment Requirements by Boat Length | Boat Ready", desc,
          "Required boat safety equipment, by boat length", og,
          [{"@type": "CollectionPage", "name": "Boat safety equipment by boat length",
            "url": "https://%s%s" % (DOMAIN, hub), "description": desc}],
          [("Home", "/"), ("Apps", "/apps/"), ("Boat Ready", "/apps/boatready/"),
           ("Safety equipment by boat length", hub)], b)
    return len(bands) + 1


def build():
    n = endorsed() + boatready()
    print("app help: %d page(s) -> apps/endorsed/practice/, apps/boatready/requirements/" % n)


if __name__ == "__main__":
    build()
