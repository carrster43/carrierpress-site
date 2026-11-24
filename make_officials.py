#!/usr/bin/env python3
"""
/officials/<state>/ -- one page per state naming everyone who governs it.

    python3 make_officials.py        # writes /officials/ and 56 state pages

WHY THIS EXISTS. Who Serves is the most useful free thing on this site and it
draws no search traffic at all: in the nineteen days to 2026-11-21 the whole
domain took 345 impressions across 77 queries, and not one query was about a
representative, a district or an office. The app is not hard to find because it
is hidden; it is hard to find because a single page cannot rank for "who
represents me in Mississippi". A question asked per-place needs a page
per-place. That is the whole idea here.

WHY STATES AND NOT DISTRICTS. The same data would make 441 district pages and
6,860 state-legislature seat pages. It will not make them yet. A state page is
substantial on its own -- a governor, up to five other statewide offices, two
senators and every House member, each with a source -- while a seat page would
be one name and a phone number. Thousands of near-empty generated pages on a
domain with no authority is the shape Google files under mass-produced content,
and it would put the useful pages at risk along with the thin ones. If the 56
earn their place, districts are the next step, not the first one.

WHAT IS DELIBERATELY NOT HERE.

  Photos.  Every holder record carries a photo URL on a .gov or state host.
           Hotlinking a few hundred government images from a static site is
           somebody else's bandwidth and breaks the day they reorganise. Names
           link to the official page instead.

  Person markup.  The JSON-LD is WebPage and BreadcrumbList only. Person
           entities for several hundred officeholders would be accurate today
           and wrong the morning after an election, and make_app_pages.py
           already settled the house position on structured data that Google
           would read as a claim.

  State legislators.  Counted, not listed. New Hampshire alone would add 400
           names to one page and bury the federal delegation. The count is the
           honest summary and the app does the address-level answer.

FRESHNESS IS THE PRODUCT. Civic data that is quietly stale is worse than no
civic data, so every page prints the date its federal and statewide rows were
checked, and names the publisher behind each statewide office. Both dates come
from the data files, never from today's clock: if the next refresh does not run,
the pages say so themselves instead of implying they are current.

URLS ARE BUILT AS URLS. Never from os.path.join or pathlib.Path -- that put
backslashes into 124 URLs on the Windows machine (books.py:392, build.py:291,
both fixed 2026-11-23). Paths here are assembled with "/" and nothing else.
"""
import html
import json
import pathlib
import re

import nav

DOMAIN = "carrierpress.com"
OUT = pathlib.Path("officials")
DATA = pathlib.Path("whoserves") / "data"

# Code -> name. The same 56 as vendor/whoserves/crosscheck-congress.py, which is
# where this list is maintained; it is repeated rather than imported because that
# file is a hyphenated script, not an importable module.
STATES = {
    "al": "Alabama", "ak": "Alaska", "az": "Arizona", "ar": "Arkansas", "ca": "California",
    "co": "Colorado", "ct": "Connecticut", "de": "Delaware", "fl": "Florida", "ga": "Georgia",
    "hi": "Hawaii", "id": "Idaho", "il": "Illinois", "in": "Indiana", "ia": "Iowa",
    "ks": "Kansas", "ky": "Kentucky", "la": "Louisiana", "me": "Maine", "md": "Maryland",
    "ma": "Massachusetts", "mi": "Michigan", "mn": "Minnesota", "ms": "Mississippi",
    "mo": "Missouri", "mt": "Montana", "ne": "Nebraska", "nv": "Nevada", "nh": "New Hampshire",
    "nj": "New Jersey", "nm": "New Mexico", "ny": "New York", "nc": "North Carolina",
    "nd": "North Dakota", "oh": "Ohio", "ok": "Oklahoma", "or": "Oregon", "pa": "Pennsylvania",
    "ri": "Rhode Island", "sc": "South Carolina", "sd": "South Dakota", "tn": "Tennessee",
    "tx": "Texas", "ut": "Utah", "vt": "Vermont", "va": "Virginia", "wa": "Washington",
    "wv": "West Virginia", "wi": "Wisconsin", "wy": "Wyoming",
    "dc": "District of Columbia", "pr": "Puerto Rico", "gu": "Guam", "as": "American Samoa",
    "mp": "Northern Mariana Islands", "vi": "U.S. Virgin Islands",
}

# The six that send a delegate or resident commissioner rather than a voting
# member. Saying "Representative" for them would be wrong, and these pages are
# read by people checking exactly that.
NON_VOTING = {"dc", "pr", "gu", "as", "mp", "vi"}

PARTY = {"R": "Republican", "D": "Democrat", "I": "Independent", "L": "Libertarian"}

SMALL = {"of", "and", "the", "for"}


def office_label(key):
    """secretary_of_state -> Secretary of State."""
    words = key.split("_")
    return " ".join(w if w in SMALL and i else w.capitalize() for i, w in enumerate(words))


def e(x):
    return html.escape(str(x), quote=True)


_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December")


def pretty_date(iso):
    """2025-01-03 -> 3 January 2025. Anything unexpected comes back untouched."""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(iso).strip())
    if not m:
        return iso
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not 1 <= mo <= 12:
        return iso
    return "%d %s %d" % (d, _MONTHS[mo - 1], y)


def slug_for(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# The mobile menu. Verbatim from the other generators' templates: it must sit
# inside .site-head, because it finds its own header with currentScript.closest.
# Kept out of HEAD's format string so its braces need no doubling.
NAV_JS = ('<script>(function(){var d=document.documentElement,'
          'h=document.currentScript.closest(".site-head"),b=h.querySelector(".nav-toggle"),'
          'n=h.querySelector(".nav");d.classList.add("navjs");'
          'function set(o){h.classList.toggle("nav-open",o);b.setAttribute("aria-expanded",o)}'
          'b.addEventListener("click",function(){set(!h.classList.contains("nav-open"))});'
          'n.addEventListener("click",function(e){if(e.target.closest("a"))set(false)});'
          'd.addEventListener("keydown",function(e){if(e.key==="Escape")set(false)})})();</script>')

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{domain}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://{domain}{path}">
<meta property="og:image" content="https://{domain}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
.ws h1{{font-size:clamp(1.8rem,6vw,2.5rem);font-weight:400;letter-spacing:-.02em;margin:0 0 12px}}
.ws .lede{{font-size:1.06rem;line-height:1.6;color:var(--ink-soft);max-width:62ch;margin:0 0 8px}}
.ws .asof{{font-family:var(--sans);font-size:13px;color:var(--muted);margin:0 0 26px}}
.ws h2{{font-size:clamp(1.25rem,4vw,1.55rem);font-weight:400;margin:34px 0 4px;
  padding-top:26px;border-top:1px solid var(--line)}}
.ws h2:first-of-type{{border-top:0;padding-top:0}}
.ws .sub{{font-family:var(--sans);font-size:14px;color:var(--muted);margin:0 0 16px}}
.ws ul.seats{{list-style:none;margin:0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}}
.ws .seat{{border:1px solid var(--line);border-radius:6px;padding:14px 16px;background:var(--paper-2);min-width:0}}
.ws .seat .role{{font-family:var(--sans);font-size:12px;letter-spacing:.07em;text-transform:uppercase;
  color:var(--muted);margin:0 0 4px}}
.ws .seat .who{{font-size:1.06rem;line-height:1.3;margin:0 0 4px}}
.ws .seat .who a{{color:var(--ink);text-decoration-color:var(--gold)}}
.ws .seat .meta{{font-family:var(--sans);font-size:13px;color:var(--ink-soft);margin:0;line-height:1.5}}
.ws .seat .src{{font-family:var(--sans);font-size:12px;color:var(--muted);margin:6px 0 0;overflow-wrap:anywhere}}
.ws .vacant{{border-left:3px solid var(--gold)}}
.ws .cta{{margin:38px 0 0;padding:22px;border:1px solid var(--line);border-left:3px solid var(--gold);
  border-radius:6px;background:var(--paper-2)}}
.ws .cta h2{{font-size:1.2rem;font-weight:400;margin:0 0 8px;border-top:0;padding-top:0}}
.ws .cta p{{margin:0 0 10px;line-height:1.6}}
.ws .cta p:last-child{{margin:0}}
.ws .states{{list-style:none;margin:0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px 14px}}
.ws .states a{{color:var(--ink);text-decoration-color:var(--gold)}}
</style>
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
    <nav class="nav" id="site-nav" aria-label="Main">
      <a href="/fiction/">Fiction</a>
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    {navjs}
  </div>
</header>
<main id="main">
<section class="wrap ws" style="padding-top:44px;padding-bottom:64px">
"""

FOOT = """</section>
</main>
<footer class="site-foot">
  <div class="wrap">
    <nav class="foot-more" aria-label="More from Carrier Press"><span>More from Carrier Press</span>\
<a href="/apps/">Apps</a><a href="/labs/">Labs</a><a href="/progress/">Progress</a>\
<a href="/reviews/">Reviews</a><a href="/support/">Support</a><a href="https://carrierlabs.org/">Cast</a></nav>
    <div class="colophon">
      <span>&copy; 2026 Jeffrey L. Carrier. All rights reserved.</span>
      <span><a href="/">Carrier Press LLC</a>, Diamondhead, Mississippi.</span>
    </div>
  </div>
</footer>
{ld}
</body>
</html>
"""


def ld_block(path, name, crumbs):
    page = {"@context": "https://schema.org", "@type": "WebPage", "name": name,
            "url": "https://%s%s" % (DOMAIN, path), "inLanguage": "en",
            "isPartOf": {"@type": "WebSite", "name": "Carrier Press",
                         "url": "https://%s/" % DOMAIN},
            "publisher": {"@type": "Organization", "name": "Carrier Press",
                          "url": "https://%s/" % DOMAIN}}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
             "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "name": n,
                  "item": "https://%s%s" % (DOMAIN, u)}
                 for i, (n, u) in enumerate(crumbs)]}
    return "".join('<script type="application/ld+json">%s</script>\n'
                   % json.dumps(d, ensure_ascii=False) for d in (page, crumb))


def seat_card(role, holder, source=None, note=None):
    """One officeholder. `holder` may be None for a vacancy."""
    out = ['<li class="seat%s">' % (" vacant" if holder is None else "")]
    out.append('<p class="role">%s</p>' % e(role))
    if holder is None:
        out.append('<p class="who">Vacant</p>')
        if note:
            out.append('<p class="meta">%s</p>' % e(note))
    elif holder.get("vacant"):
        out.append('<p class="who">Vacant</p>')
    else:
        name = holder.get("name", "")
        url = holder.get("url")
        out.append('<p class="who">%s</p>'
                   % ('<a href="%s" rel="noopener">%s</a>' % (e(url), e(name)) if url else e(name)))
        bits = []
        party = PARTY.get(holder.get("party"))
        if party:
            bits.append(party)
        # An appointee filling someone else's unexpired term. Printing them as
        # the plain officeholder would be the one thing a reader of this page
        # most needs to know and least expects to be wrong about.
        if holder.get("interim"):
            bits.append("interim")
        if holder.get("since"):
            bits.append("since %s" % e(pretty_date(holder["since"])))
        contact = holder.get("contact") or {}
        if contact.get("phone"):
            bits.append(e(contact["phone"]))
        if bits:
            out.append('<p class="meta">%s</p>' % " &middot; ".join(bits))
        if contact.get("address"):
            out.append('<p class="meta">%s</p>' % e(contact["address"]))
    if source:
        pub, when = source
        out.append('<p class="src">Source: %s, checked %s</p>' % (e(pub), e(when)))
    out.append("</li>")
    return "".join(out)


def build():
    oh = json.loads((DATA / "officeholders.json").read_text(encoding="utf-8"))
    sw = json.loads((DATA / "statewide.json").read_text(encoding="utf-8"))
    seats, states_sw = oh["seats"], sw["states"]
    fed_when = oh.get("retrievedAt", "")
    # Oldest verifiedAt anywhere in the statewide file, for the index page. Same
    # reason as the per-state date below: updatedAt flatters it by a month.
    _all_ver = sorted({r.get("verifiedAt") for rows in sw["states"].values()
                       for r in rows if r.get("verifiedAt")})
    sw_oldest = (("between %s and %s" % (_all_ver[0], _all_ver[-1])) if len(_all_ver) > 1
                 else (_all_ver[0] if _all_ver else sw.get("updatedAt", "")))
    vacancies = sw.get("vacant") or {}

    written = []
    for code, name in sorted(STATES.items(), key=lambda kv: kv[1]):
        path = "/officials/%s/" % slug_for(name)
        body = []

        senators = seats.get("sen:%s" % code) or []
        reps = sorted(((int(k.split(":")[2]), v) for k, v in seats.items()
                       if k.startswith("rep:%s:" % code)), key=lambda t: t[0])
        statewide = states_sw.get(code) or []
        upper = sum(1 for k in seats if k.startswith("sldu:%s:" % code))
        lower = sum(1 for k in seats if k.startswith("sldl:%s:" % code))

        chief = next((r for r in statewide if r.get("key") in ("governor", "mayor")), None)
        chief_name = ((chief or {}).get("holder") or {}).get("name")
        sen_names = [s.get("name") for s in senators if s.get("name")]

        lead = []
        if chief_name:
            lead.append(chief_name)
        lead += sen_names
        # No election dates here, and the description must not imply any: the data
        # files carry name, party, contact and `since`, and nothing about terms
        # (checked 2026-11-23). "Next up for election" is the app's answer, not
        # this page's, and a description promising it would be false on 56 pages.
        desc = ("Who represents %s: %s%s. Statewide offices, both US senators and all %d "
                "in the US House, with the source behind every name."
                % (name, ", ".join(lead[:3]) if lead else "the current officeholders",
                   "" if len(lead) < 4 else " and more", len(reps)))
        body.append('<h1>Who represents you in %s</h1>' % e(name))
        body.append('<p class="lede">The offices that govern %s and the people holding them '
                    'right now, with the source behind every line. For the districts that cover '
                    'one exact address, open Who Serves.</p>' % e(name))
        # The statewide date is the OLDEST verifiedAt among this state's own
        # rows, never the file's updatedAt. updatedAt is when the file was last
        # touched -- 2026-10-23 while every row in it was checked 2026-09-25 --
        # and printing it would claim a month more freshness than any office on
        # the page actually has. The oldest row is the one a reader is entitled
        # to judge the page by.
        # Since check_statewide.py began re-verifying row by row (2026-11-24),
        # a state's offices no longer share one date: the ones whose sites take
        # an automated read are current, and the ones behind a captcha, a PDF or
        # a 403 still carry the date a person last looked. Printing only the
        # oldest would bury five fresh rows behind one stale one; printing only
        # the newest would be a lie about the other five. The range says both,
        # and each row still carries its own date beside its source.
        checked = sorted({r.get("verifiedAt") for r in statewide if r.get("verifiedAt")})
        if not checked:
            when = ""
        elif len(checked) == 1:
            when = " Statewide rows checked %s." % e(checked[0])
        else:
            when = (" Statewide rows checked between %s and %s."
                    % (e(checked[0]), e(checked[-1])))
        body.append('<p class="asof">Federal rows checked %s.%s</p>' % (e(fed_when), when))

        if statewide:
            body.append("<h2>Statewide offices</h2>")
            body.append('<p class="sub">%d office%s, each verified against the office’s own site.</p>'
                        % (len(statewide), "" if len(statewide) == 1 else "s"))
            body.append('<ul class="seats">')
            for row in statewide:
                src = (row.get("sourcePublisher") or "", row.get("verifiedAt") or "")
                body.append(seat_card(office_label(row.get("key", "")), row.get("holder"),
                                      src if src[0] else None))
            for row in vacancies.get(code, []):
                body.append(seat_card(office_label(row.get("key", "")), None,
                                      (row.get("sourcePublisher") or "", row.get("verifiedAt") or ""),
                                      row.get("note")))
            body.append("</ul>")

        if senators:
            body.append("<h2>United States Senate</h2>")
            body.append('<p class="sub">Both seats, with the Washington office and line.</p>')
            body.append('<ul class="seats">')
            for s in senators:
                body.append(seat_card("US Senator", s, ("the Senate", fed_when)))
            body.append("</ul>")

        if reps:
            delegate = code in NON_VOTING
            body.append("<h2>United States House</h2>")
            body.append('<p class="sub">%s</p>' % (
                "A non-voting delegate to the House." if delegate else
                "%d seat%s in the %dth Congress." % (len(reps), "" if len(reps) == 1 else "s",
                                                     oh.get("congress", 119))))
            body.append('<ul class="seats">')
            for district, holders in reps:
                if delegate:
                    role = "Delegate"
                elif district == 0:
                    role = "At-large district"
                else:
                    role = "District %d" % district
                for h in holders:
                    body.append(seat_card(role, h, ("the Clerk of the House", fed_when)))
            body.append("</ul>")

        if upper or lower:
            body.append("<h2>The state legislature</h2>")
            body.append('<p class="sub">%s seats in all: %d in the upper chamber and %d in the lower. '
                        'They are not listed here because the ones that matter to you are the two or '
                        'three whose districts cover your address, and that is the question Who Serves '
                        'answers.</p>' % (f"{upper + lower:,}", upper, lower))

        body.append('<div class="cta">')
        body.append("<h2>Your exact address</h2>")
        body.append("<p>This page is the whole state. Who Serves takes one address and returns only "
                    "the districts and offices that cover it, including the state legislative seats "
                    "left off above, and when each one is next up for election.</p>")
        body.append('<p><a href="/whoserves/app/">Open Who Serves</a> &middot; '
                    '<a href="/apps/whoserves/">What it does</a> &middot; '
                    '<a href="/officials/">Another state</a></p>')
        body.append("</div>")

        page = (HEAD.format(title=e("Who Represents You in %s | Carrier Press" % name),
                            ogtitle=e("Who represents you in %s" % name),
                            desc=e(desc), domain=DOMAIN, path=path, navjs=NAV_JS)
                + "\n".join(body) + "\n"
                + FOOT.format(ld=ld_block(path, "Who represents you in %s" % name,
                                          [("Carrier Press", "/"), ("Officials", "/officials/"),
                                           (name, path)])))
        out = OUT / slug_for(name) / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        nav.patch(out)
        written.append((name, path))

    # The index. Without it the 56 are orphans, reachable only from the sitemap,
    # which is the slowest way to be found and the weakest internal signal.
    path = "/officials/"
    idx = ['<h1>Who represents you</h1>',
           '<p class="lede">Every office that governs each state and territory, and the people '
           'holding them now, with a source on every line. Pick a state, or open Who Serves to '
           'answer it for one exact address.</p>',
           '<p class="asof">Federal rows checked %s. Statewide rows checked %s.</p>'
           % (e(fed_when), e(sw_oldest)),
           '<ul class="states">']
    idx += ['<li><a href="%s">%s</a></li>' % (e(u), e(n)) for n, u in written]
    idx.append("</ul>")
    idx.append('<div class="cta"><h2>One address, not one state</h2>'
               '<p>Who Serves narrows all of this to the districts that cover a single address, '
               'including the state legislative seats these pages leave out.</p>'
               '<p><a href="/whoserves/app/">Open Who Serves</a> &middot; '
               '<a href="/apps/whoserves/">What it does</a></p></div>')
    desc = ("Who represents you, state by state: governors and statewide offices, both US senators "
            "and every member of the US House, with the source behind each one.")
    page = (HEAD.format(title=e("Who Represents You, State by State | Carrier Press"),
                        ogtitle=e("Who represents you, state by state"),
                        desc=e(desc), domain=DOMAIN, path=path, navjs=NAV_JS)
            + "\n".join(idx) + "\n"
            + FOOT.format(ld=ld_block(path, "Who represents you, state by state",
                                      [("Carrier Press", "/"), ("Officials", path)])))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    nav.patch(OUT / "index.html")
    return written


if __name__ == "__main__":
    rows = build()
    print("officials: %d state page(s) -> officials/<state>/index.html, plus /officials/"
          % len(rows))
