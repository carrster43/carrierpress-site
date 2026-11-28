#!/usr/bin/env python3
"""
Free help pages for the apps (2026-11-27, "app help pages first"):

  /apps/endorsed/practice/             free practice tests, one per credential
  /apps/endorsed/practice/<pack>/      the pack's exam note, first study section
                                       and its 10 free questions, with answers
  /apps/boatready/requirements/        boat safety equipment by boat length
  /apps/boatready/requirements/<band>/ the federal carriage list for that size,
                                       and what each common difference adds
  /apps/cancelled/help/                how to find every subscription you pay for
  /apps/cancelled/help/<topic>/        annual plans, statement names, and what to
                                       do when a charge keeps coming

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

CANCELED IS THE EXCEPTION: its pages are written guidance (CANCEL_PAGES below),
because what it gives free is the person's own statement read back. Its
per-company cancel routes (ROUTES in ~/Projects/Cancelled/lib/merchants.ts)
are the paid unlock, one free, so no page here names a company's cancel
steps. The method on these pages is the app's own (lib/recurring.ts,
statements.ts, merchants.ts, cancel.ts); a page must never promise what the
app does not do.

Rules kept here: no em or en dashes.
"""
import datetime, html, json, pathlib, re

import nav

DOMAIN = "carrierpress.com"
DATA = pathlib.Path("help_data")
HUBS = {"endorsed": ("/apps/endorsed/practice/", "Free practice tests, with answers"),
        "boatready": ("/apps/boatready/requirements/", "Required safety equipment by boat length"),
        "cancelled": ("/apps/cancelled/help/", "How to find every subscription you pay for"),
        "cast": ("/apps/cast/help/", "Books read with a voice for each character")}

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


# ── Canceled ────────────────────────────────────────────────────────────────
# Written guidance, not exported data (see the docstring). Each section is
# (heading, [blocks]); a block is a paragraph string, or ("ul"|"ol", [items]).

CANCEL_CTA = ("Canceled does the reading for you. Open a year of statements and it lists every recurring "
              "charge, ranked by what it costs a year, on your own device, with nothing uploaded and no bank "
              "login. Seeing the list costs nothing. One payment, never a subscription, shows where to "
              "cancel each one.")

CANCEL_PAGES = [
    {"slug": "", "kicker": "Canceled: free guide",
     "h1": "How to find every subscription you pay for",
     "title": "How to Find Every Subscription You Pay For | Canceled",
     "desc": "A step by step way to find every recurring charge in your bank and card statements, including "
             "the yearly ones, and what each really costs you a year.",
     "lede": "The charges that slip by are rarely the big streaming plans. They are the yearly renewal, the "
             "free trial that turned paid, and the plan billed through an app store under a name you do not "
             "recognize. This is the method that finds them, five steps you can do by hand.",
     "sections": [
        ("1. List every way you pay", [
            "A subscription can bill any account it was given, so start with the list of accounts, not the "
            "list of subscriptions you remember.",
            ("ul", ["Every credit card, including the store card and the one in the drawer",
                    "Every checking account, for plans paid by automatic debit",
                    "PayPal, if you have ever paid with it: a plan billed through PayPal shows on your card as "
                    "PayPal, not as the company",
                    "Your Apple Account and Google Play account, which keep their own subscription lists",
                    "Your phone bill, which can carry plans bought through your carrier"])]),
        ("2. Download a full year", [
            "A year matters because yearly plans charge once and then hide for eleven months. Three months "
            "of statements shows you every monthly plan and none of the yearly ones.",
            "On your bank's or card's website, open the account's transactions and look for Download or "
            "Export. Many banks cap how far back one download reaches, so you may need two or three "
            "downloads to cover twelve months. Some banks offer only PDF statements; the card your plans are "
            "billed to usually offers a download even when the bank does not."]),
        ("3. Look for a schedule and a price that holds", [
            "A charge that repeats is not yet a subscription. Groceries repeat. Coffee repeats. What marks a "
            "subscription is that it lands on a schedule, at the same price, from a business that bills that "
            "way.",
            ("ul", ["Monthly plans land within a few days of the same date each month",
                    "Weekly, quarterly and twice yearly plans keep their own spacing",
                    "The amount matches to the cent, or steps up once and then holds at the new price",
                    "An amount that wanders ($88, then $97, then $91) is shopping, not a plan"]),
            "One missed month does not rule a plan out: a statement can have a gap."]),
        ("4. Price each one by the year", [
            "Multiply a monthly charge by twelve and a weekly one by fifty two. A $10.99 plan is $131.88 a "
            "year, and a price rise you did not notice, $3 a month, is $36 a year. Sort the list by the "
            "yearly figure; the order is usually a surprise."]),
        ("5. Cancel each one where it is billed", [
            "This is where many attempts go wrong. A plan bought inside an iPhone or Android app is billed by "
            "Apple or Google, and it is canceled in that store's subscription list. Deleting the app, or "
            "canceling inside it, does not stop the charge. A plan billed through PayPal or your phone "
            "company is canceled with the company or through that account.",
            "Whatever the route, ask for a confirmation number or email and keep it. Then check the next "
            "statement: a plan that charges again after you canceled is a billing error, and you have ways "
            "to stop it."]),
     ]},
    {"slug": "annual-subscriptions", "kicker": "Canceled: free guide",
     "h1": "How to find yearly subscriptions before they renew",
     "title": "How to Find Annual Subscriptions Before They Renew | Canceled",
     "desc": "Yearly plans charge once and hide for eleven months. How to find every annual subscription in "
             "your statements and work out when each one renews.",
     "lede": "A yearly plan is the easiest subscription to forget and the most expensive to miss. It charges "
             "once, at a price large enough to notice, and then says nothing for a year, so by the time it "
             "renews nobody remembers agreeing to it.",
     "sections": [
        ("Why three months of statements cannot find them", [
            "A monthly plan shows three times in three months. A yearly plan shows once in twelve, or not at "
            "all if it renewed four months ago. The only way to see every yearly plan is a full year of "
            "statements, and thirteen months is safer, because a plan that renews on the 3rd can fall just "
            "outside a twelve month window."]),
        ("Where the yearly ones hide", [
            ("ul", ["Software and apps bought by the year: antivirus, password managers, photo editing, "
                    "cloud storage",
                    "Memberships: warehouse clubs, shopping memberships, roadside assistance, professional "
                    "associations",
                    "Web domains and website hosting, often set to renew automatically",
                    "A plan you moved from monthly to yearly for the discount and then forgot about",
                    "A free trial that turned into a yearly plan rather than a monthly one"])]),
        ("How to tell a yearly plan from a one-time purchase", [
            "One charge on its own proves nothing; you bought something. Two charges from the same company, "
            "about a year apart and at the same price, or one step higher, are a yearly plan. With only one "
            "year of statements you will often see a single charge from a company that sells subscriptions; "
            "treat it as a possible yearly plan and check the account it belongs to.",
            "Watch for a yearly plan paid monthly. Some software sells a yearly commitment billed in twelve "
            "monthly payments, and canceling partway can cost a fee. The plan's own account page says which "
            "kind you have."]),
        ("Work out the renewal date", [
            "A yearly plan normally renews on the same date as its last charge, one year on. Put that date in "
            "your calendar a week early, which gives you time to decide and cancel before it charges. A "
            "company can move a billing date, so treat it as an estimate, and check the account page if the "
            "date matters."]),
     ]},
    {"slug": "statement-charge-names", "kicker": "Canceled: free guide",
     "h1": "What is that charge? Reading the names on your statement",
     "title": "What Is This Charge on My Statement? Reading Merchant Names",
     "desc": "Why one subscription can look like four different charges on a statement, and how to read the "
             "prefixes, numbers and codes banks wrap around a company's name.",
     "lede": "A statement does not print a company's name. It prints what the payment network passed along, "
             "plus whatever your bank adds, and the same plan can look different on every account. Once you "
             "know what is wrapped around the name, most mystery charges explain themselves.",
     "sections": [
        ("One plan, four different lines", [
            "The same streaming plan can appear as NETFLIX.COM followed by a code on one card, as PAYPAL "
            "*NETFLIX when it is paid through PayPal, as PURCHASE AUTHORIZED ON 09/03 NETFLIX.COM with a card "
            "number in a checking account, and with the company's street address added on another card. All "
            "four are one plan."]),
        ("What banks wrap around the name", [
            ("ul", ["Purchase wording and dates: PURCHASE AUTHORIZED ON, POS, DEBIT CARD PURCHASE, and the "
                    "date the card was used",
                    "Card numbers: the last four digits of the card that paid",
                    "Reference numbers and codes after the name, often after a star",
                    "Store numbers, phone numbers, street addresses, a city and a state code",
                    "A payment processor's prefix in front of the business: PAYPAL * for PayPal, SQ * for "
                    "Square, TST* for Toast"]),
            "Strip those away and what is left is usually the business. SQ * and TST* are mostly shops and "
            "restaurants, so a charge with either prefix is rarely a subscription."]),
        ("Charges billed by Apple or Google", [
            "Every plan bought inside an iPhone app, plus iCloud+ and Apple Music, can show under the same "
            "Apple billing name, so three different plans can look like one company charging three amounts. "
            "Google Play purchases work the same way. The way to see what each charge is, is the subscription "
            "list in your Apple Account or Google Play account, which names each plan and its price."]),
        ("Names that are ordinary words", [
            "Some brands share their name with everyday businesses, so a word on its own is not proof. A "
            "line that reads like a streaming service may be a bar or a local health clinic. Check the amount "
            "and the schedule: a subscription charges the same price on the same day each period."]),
        ("If you still cannot place it", [
            "Search the cleaned name with the word billing, and look for a match on the company's own "
            "website. If nothing fits, call the number on the back of your card: the card issuer can see more "
            "about the merchant than the statement shows, and can dispute a charge you did not agree to."]),
     ]},
    {"slug": "still-charged-after-canceling", "kicker": "Canceled: free guide",
     "h1": "Still being charged after you canceled? What to do",
     "title": "Still Charged After Canceling a Subscription? What to Do",
     "desc": "What to do when a subscription keeps charging after you canceled: check where it is billed, "
             "put it in writing, then have your card issuer or bank stop it.",
     "lede": "A charge after you canceled is not the end of the road. It usually has one of three causes, and "
             "each has a fix. Work down the list in order.",
     "sections": [
        ("First, check that you canceled the right thing", [
            "A frequent cause is canceling in the wrong place. A plan bought inside an iPhone or Android "
            "app is billed by Apple or Google; deleting the app or canceling inside it does nothing. The same "
            "goes for a plan billed through PayPal, through your phone company, or as an add-on to another "
            "membership: it is canceled where it is billed.",
            "Another is timing. Many plans run to the end of the period you have paid "
            "for, and a charge dated before you canceled is not a new one. Compare the charge date with your "
            "confirmation."]),
        ("Second, put it in writing", [
            "When a company has no cancel button, insists on a call, or keeps billing after it said it had "
            "stopped, write to it. Say what you are canceling, the date you first asked, and that any charge "
            "after that date is not authorized. Email it if the company lists an address for it; otherwise "
            "send it by certified mail with a return receipt. Some gyms ask for a letter as their own route. "
            "Keep a copy: it is what a dispute rests on."]),
        ("Third, have your card issuer or bank stop it", [
            ("ul", ["On a credit or debit card: call the number on the back and dispute the charge as "
                    "canceled. Have your confirmation or your letter ready. Card issuers set time limits on "
                    "disputes, often counted from the statement date, so do not wait.",
                    "From a checking account: ask your bank to stop payments to the company, a stop payment "
                    "on the automatic debit, and dispute any taken after the date you canceled."])]),
        ("Keep the paper trail", [
            "A screenshot of the confirmation page, the confirmation email, the letter and its receipt, and a "
            "note of every call with its date. With those, a dispute is usually short."]),
     ]},
]


def _blocks(blocks):
    out = []
    for bl in blocks:
        if isinstance(bl, str):
            out.append("<p>%s</p>" % e(bl))
        else:
            tag, items = bl
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % e(i) for i in items), tag))
    return out


def _guide(app, pages, cta, cta_label, hub_name, fine):
    """A written guide: a hub page (slug "") plus topic pages, each with the app's
    box after its second section. A page may carry `extra`, a function giving
    more HTML after its sections (the Cast shelf list)."""
    hub = HUBS[app][0]
    og = _og(app)
    for pg in pages:
        if len(pg["title"]) > 65 or len(pg["desc"]) > 160:
            raise SystemExit("make_app_help: %s page %r: title %d / desc %d characters"
                             % (app, pg["slug"], len(pg["title"]), len(pg["desc"])))
    for pg in pages:
        path = hub + (pg["slug"] + "/" if pg["slug"] else "")
        b = ['<p class="sec-head" style="margin:0 0 10px"><span class="kicker">%s</span></p>' % e(pg["kicker"]),
             "<h1>%s</h1>" % e(pg["h1"]), '<p class="lede">%s</p>' % e(pg["lede"])]
        for i, (h, blocks) in enumerate(pg["sections"]):
            b.append("<h2>%s</h2>" % e(h))
            b += _blocks(blocks)
            if i == min(1, len(pg["sections"]) - 1):
                b.append('<div class="ah-cta"><p>%s</p><a class="ah-go" href="/apps/%s/">%s</a></div>'
                         % (e(cta), app, e(cta_label)))
        if pg.get("extra"):
            b += pg["extra"]()
        others = [o for o in pages if o is not pg]
        b.append('<h2>More from this guide</h2><ul class="ah-links">')
        b += ['<li><a href="%s">%s</a></li>' % (hub + (o["slug"] + "/" if o["slug"] else ""),
                                                 e(o["h1"][0].upper() + o["h1"][1:])) for o in others]
        b.append("</ul>")
        b.append('<p class="ah-fine">%s</p>' % e(fine))
        crumbs = [("Home", "/"), ("Apps", "/apps/"), (APP_NAME[app], "/apps/%s/" % app), (hub_name, hub)]
        if pg["slug"]:
            crumbs.append((pg["h1"][0].upper() + pg["h1"][1:], path))
        _page(path, pg["title"], pg["desc"], pg["h1"], og,
              [{"@type": "Article", "headline": pg["h1"], "url": "https://%s%s" % (DOMAIN, path),
                "description": pg["desc"], "author": {"@type": "Organization", "name": "Carrier Labs LLC"},
                "publisher": {"@type": "Organization", "name": "Carrier Press"}}],
              crumbs, b)
    return len(pages)


APP_NAME = {"cancelled": "Canceled", "cast": "Cast"}


def cancelled():
    return _guide("cancelled", CANCEL_PAGES, CANCEL_CTA, "See Canceled", "Find every subscription",
                  "Company names are their owners' trademarks, used here only to describe what appears on a "
                  "statement. Canceled is made by Carrier Labs LLC and is not affiliated with any of them, or "
                  "with any bank.")


# ── Cast ────────────────────────────────────────────────────────────────────
# Written guidance plus one list built from data (cast_shelf.json via listen.py,
# and the catalogue). What Cast gives free is the opening of every shelf book,
# so the list links each one's free opening and nothing more.
#
# 🚨 NEVER CALL A CAST TITLE AN AUDIOBOOK. KDP Virtual Voice needs a title with
# no audiobook edition, and the site hosts none on purpose (listen.py,
# make_audio.py). Cast sells a license to hear a book performed in the app.
# The pages say "performed" and "read aloud"; a build check below stops on
# "audiobook" anywhere in this copy.

CAST_CTA = ("Cast performs a book with a narrator and a voice of its own for every character, right in your "
            "browser. The opening of every book on its shelf plays free, with no key and no account.")


def _cast_list():
    import listen
    D = json.loads(pathlib.Path("catalog.json").read_text(encoding="utf-8"))
    groups = [("Restored classics", lambda s: s["id"] == "classics"),
              ("Mysteries, suspense and history", lambda s: not s.get("kids") and not s.get("nonfic")
               and s["id"] != "classics"),
              ("For young readers", lambda s: bool(s.get("kids")))]
    import books as _books
    url = _books.url_for(D)
    out, total = [], 0
    for label, test in groups:
        rows = []
        for sec in D["sections"]:
            if not test(sec):
                continue
            for bk in sec["books"]:
                c = listen.CAST.get(bk["a"])
                if not c or c.get("mode") != "cast" or bk.get("soon"):
                    continue
                rows.append('<li><a href="%s">%s</a> <span class="ah-src">%s</span><br>'
                            '<a href="%s">Hear the opening free</a></li>'
                            % (url[bk["a"]], e(bk["t"]), e(bk.get("by") or D["site"]["author"]),
                               listen.cast_listen_url(c)))
        if rows:
            total += len(rows)
            out += ["<h2>%s</h2>" % e(label), '<ul class="ah-links">'] + rows + ["</ul>"]
    if total < 20:
        raise SystemExit("make_app_help: only %d Cast books with a voice per character" % total)
    return ['<p>%d books on Cast\'s shelf have a voice for each character. Each title opens its own page; '
            'the second link plays its opening in Cast, free.</p>' % total] + out


CAST_PAGES = [
    {"slug": "", "kicker": "Cast: free guide",
     "h1": "Hear a book read with a voice for each character",
     "title": "Books Read Aloud with a Voice for Each Character | Cast",
     "desc": "Most text to speech reads a whole book in one voice. Here is how a book can be performed with a "
             "narrator and a separate voice for every character instead.",
     "lede": "Ordinary text to speech reads every line in the same voice, so a conversation between three "
             "people sounds like one person talking to themselves. A performed reading gives the narrator one "
             "voice and each character their own, and the scene suddenly plays like a scene.",
     "sections": [
        ("One voice or a cast", [
            "Your phone and computer can already read a book aloud. They read it the way a person reads a "
            "letter: every word in one voice, quotation marks and all. That is fine for an article. In a "
            "novel, where half the page is people talking, it loses the thing that makes dialogue work, which "
            "is hearing who is speaking.",
            "A performed reading works out who says each line and gives that line to that character's voice. "
            "The narrator keeps the descriptions. The result sounds closer to a radio play than to a screen "
            "reader."]),
        ("What you can hear free", [
            ("ul", ["The opening of every book on Cast's shelf, in your browser, with no key and no account",
                    "The voices are computer voices, made in your browser after one download of about 90 MB, "
                    "not recordings of actors",
                    "Every book's card says how fully it is cast, so you know before you press Play"])]),
     ]},
    {"slug": "books-with-a-voice-for-each-character", "kicker": "Cast: free guide",
     "h1": "Books performed with a different voice for each character",
     "title": "Books Performed with a Different Voice for Each Character",
     "desc": "Classics, mysteries and books for young readers performed with a narrator and a voice for every "
             "character. The opening of each one plays free in your browser.",
     "lede": "Every book below is performed in Cast with a narrator and a separate voice for each character. "
             "Press the free link under any title to hear how it opens before you decide anything.",
     "sections": [
        ("How to listen", [
            "The free opening plays in your browser on a phone or a computer, with no key and no account. "
            "Cast makes its natural voices after one download of about 90 MB; until that finishes, your "
            "browser's own voices read. To hear a whole book, buy that book once in Cast; nothing renews."]),
     ],
     "extra": _cast_list},
    {"slug": "read-an-epub-aloud", "kicker": "Cast: free guide",
     "h1": "How to have an EPUB read aloud on a phone or computer",
     "title": "How to Have an EPUB Read Aloud on iPhone, Mac, Android or PC",
     "desc": "The free read aloud tools already on your iPhone, Mac, Android phone or Windows PC, and how to "
             "hear an EPUB with a separate voice for each character instead.",
     "lede": "Every phone and computer can read text aloud without anything extra to install. Here is where "
             "each one keeps it, and what to do when one flat voice for a whole novel is not enough.",
     "sections": [
        ("iPhone and iPad", [
            "Turn on Speak Screen in Settings, then Accessibility, then Spoken Content. Open the book in your "
            "reading app and swipe down from the top of the screen with two fingers. The page is read aloud, "
            "and a small panel lets you pause, skip and change the speed."]),
        ("Mac", [
            "Turn on Speak selection in System Settings, then Accessibility, then Spoken Content. Select the "
            "text you want and press Option and Escape together. Press them again to stop."]),
        ("Android", [
            "Turn on Select to Speak in Settings, then Accessibility. Tap its button, then tap or drag over "
            "the text on screen to have it read."]),
        ("Windows", [
            "Narrator is built in. Press the Windows key, Control and Enter together to turn it on or off. It "
            "is made for reading everything on screen, so it suits a page of text better than a long book."]),
        ("One voice for every character, or a cast", [
            "All four read in one voice. For a novel full of dialogue, Cast reads an EPUB the way a performer "
            "would: a narrator, and a separate voice for each character. It reads EPUB files without copy "
            "protection, up to 80 MB. Books sold DRM free and books you wrote yourself work; most books bought "
            "from the big ebook stores are copy protected, and Kindle files and PDFs are not EPUBs, so Cast "
            "cannot open those. Your own books are a membership, with a one-week trial for new members."]),
     ]},
    {"slug": "how-character-voices-work", "kicker": "Cast: free guide",
     "h1": "How text to speech can give each character a voice",
     "title": "How Text to Speech Gives Each Character Its Own Voice",
     "desc": "How a program reads a novel, works out who says each line, and gives every character a voice of "
             "their own, and why some books come out better than others.",
     "lede": "Giving each character a voice is not really a voice problem. Natural computer voices are easy to "
             "find now. The hard part is working out, line by line, who is speaking, from nothing but the "
             "printed page.",
     "sections": [
        ("Step one: split the page into speech and narration", [
            "The program walks the book chapter by chapter, in reading order, and leaves out the front and "
            "back matter. Quotation marks, straight or curly, split each paragraph into spoken lines and "
            "narration."]),
        ("Step two: find the cast", [
            "Names that sit close to speech verbs, such as said, asked and whispered, are the characters. "
            "Different forms of one name, a first name and a title, say, are folded into one person. Each "
            "character then gets a voice slot, with hints for whether the character is a man or a woman, "
            "young or old."]),
        ("Step three: decide who says each line", [
            "A line tagged with a name is easy. A line with only she said, or no tag at all, has to be worked "
            "out from who spoke before and who is in the scene. The program records how sure it is, and when "
            "it is not sure enough, the narrator reads the line instead. A line in the wrong voice is worse "
            "than a line in the narrator's."]),
        ("Why some books cast better than others", [
            "How well this works depends far more on the author than on the program. A book that tags its "
            "dialogue the conventional way, with names and said, casts very well. Literary prose that leaves "
            "its dialogue untagged is much harder, and a book with little quoted dialogue is simply read by "
            "the narrator. That is why every book in Cast says how fully it is cast.",
            "Cast's shelf books are cast once, ahead of time, into a script that can be checked and "
            "corrected. Your own EPUBs are cast right in your browser when you add them."]),
     ]},
]


def cast():
    for pg in CAST_PAGES:
        text = json.dumps({k: v for k, v in pg.items() if k != "extra"}) + CAST_CTA
        if "audiobook" in text.lower():
            raise SystemExit("make_app_help: Cast page %r says audiobook (see the note above CAST_CTA)" % pg["slug"])
    return _guide("cast", CAST_PAGES, CAST_CTA, "Open Cast", "Voices for every character",
                  "The voices in Cast are computer voices, not recordings of narrators. Cast is made by Carrier "
                  "Labs LLC.")


def build():
    n = endorsed() + boatready() + cancelled() + cast()
    print("app help: %d page(s) -> apps/endorsed/practice/, apps/boatready/requirements/, apps/cancelled/help/, "
          "apps/cast/help/" % n)


if __name__ == "__main__":
    build()
