#!/usr/bin/env python3
"""
/apps/ -- what each tool costs, what the free tier gives you, and what is not
out yet.

    python3 make_apps.py

WHY THIS IS A SEPARATE PAGE FROM /labs/. /labs/ is a build log and says so in
its own second paragraph: "This is a build log, not a store." That page's job is
to be honest about what exists. This page's job is to be honest about what
something costs. They are different questions and they go stale at different
rates, so they are different pages and /labs/ keeps its sentence.

THE STYLESHEET IS SHARED AND UNMODIFIED. styles.css is hand-edited and belongs
to the book side. Everything this page needs is scoped into one block in its own
head, same reasoning as /labs/ and /planfinder/privacy/. Every colour is an
existing token, so dark mode follows automatically and there is nothing to
maintain in two places.

NOTHING HERE IS A BUY BUTTON. As of 2026-09-20 no app is on a store, so the only
action offered is "tell me when it is out", which is a mailto and needs no
third-party form service, no tracking script and no privacy claim this site
cannot back. When an app goes live, set status="live" and fill `store` in
apps_data.py and the card grows a real link.
"""
import html, pathlib, sys, datetime

import apps_data
import nav

DOMAIN = "carrierpress.com"
OUT = pathlib.Path("apps")
SUPPORT = "support@carrierpress.com"

BLURB = ("What each tool costs, what you get without paying anything, and which "
         "ones are not out yet. No advertising, no analytics, no engagement loop.")


def e(x):
    return html.escape(str(x), quote=True)


def count_words(n):
    """45 -> "Forty-five". Capitalised, because it opens a sentence."""
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    if n < 20:
        w = ones[n]
    elif n < 100:
        w = tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")
    else:
        w = str(n)
    return w[:1].upper() + w[1:]


HEAD = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Apps and pricing | Carrier Press</title>
<meta name="description" content="{e(BLURB)}">
<link rel="canonical" href="https://{DOMAIN}/apps/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="Apps and pricing">
<meta property="og:description" content="{e(BLURB)}">
<meta property="og:url" content="https://{DOMAIN}/apps/">
<meta property="og:image" content="https://{DOMAIN}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
/* Scoped to this page on purpose. styles.css is hand edited and shared by the
   whole site, and a pricing page is not a reason to add rules to it. Same
   reasoning as /labs/. Every colour below is an existing token, so dark mode
   follows without a second block. */

.ap-intro p{{margin:0 0 16px;line-height:1.66;max-width:70ch}}
.ap-intro p:last-child{{margin-bottom:0}}

/* The three plan shapes. Not a pricing table with a highlighted middle column,
   because there is no upsell here: an app is a subscription or it is one
   payment, and which one it is follows from the app rather than from us. */
.ap-plans{{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(248px,1fr));
  gap:18px;margin:34px 0 0;
}}
.ap-plan{{
  background:var(--paper-2);border:1px solid var(--line);border-radius:5px;
  padding:22px 22px 24px;
}}
.ap-plan h3{{
  font-family:var(--sans);font-size:11.5px;font-weight:700;letter-spacing:.18em;
  text-transform:uppercase;color:var(--gold);margin:0 0 10px;
}}
.ap-plan .big{{
  display:block;font-size:1.3rem;line-height:1.25;margin:0 0 10px;letter-spacing:-.01em;
}}
.ap-plan p{{margin:0;font-size:.95rem;line-height:1.6;color:var(--ink-soft)}}

/* The house rules. A lifted panel rather than a warning box: the facts are
   ordinary and stating them plainly is the whole point. */
.ap-rules{{
  background:var(--paper-2);border:1px solid var(--line);border-left:3px solid var(--gold);
  border-radius:4px;padding:22px 24px;margin:30px 0 0;
}}
.ap-rules ul{{margin:0;padding-left:20px}}
.ap-rules li{{margin:0 0 10px;line-height:1.6;font-size:1rem}}
.ap-rules li:last-child{{margin:0}}

.ap-legend{{
  display:flex;flex-wrap:wrap;gap:10px 18px;margin:44px 0 30px;
  font-family:var(--sans);font-size:12.5px;color:var(--muted);align-items:center;
}}
.ap-legend .k{{display:inline-flex;align-items:center;gap:7px}}
.ap-legend .dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}
.dot-browser{{background:var(--gold-bright);box-shadow:0 0 0 3px rgba(232,200,74,.22)}}
.dot-live{{background:var(--gold-bright);box-shadow:0 0 0 3px rgba(232,200,74,.22)}}
.dot-soon{{background:var(--ink-soft)}}
.dot-design{{background:none;box-shadow:inset 0 0 0 1.5px var(--muted)}}

.ap-group{{margin:52px 0 22px;padding-top:26px;border-top:1px solid var(--line)}}
.ap-group:first-of-type{{border-top:0;padding-top:0;margin-top:8px}}
.ap-group h2{{font-size:clamp(1.15rem,2.4vw,1.42rem);margin:0 0 7px;font-weight:400;letter-spacing:-.01em}}
.ap-group p{{margin:0;color:var(--ink-soft);font-size:.96rem;max-width:66ch}}
.ap-group .count{{
  font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;color:var(--gold);display:block;margin-bottom:6px;
}}

.ap-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:18px}}
.ap-card{{
  border:1px solid var(--line);border-radius:5px;padding:20px 21px 21px;
  display:flex;flex-direction:column;background:var(--paper);
}}
.ap-card.is-open{{border-color:var(--gold);background:var(--paper-2)}}
.ap-top{{display:flex;align-items:baseline;gap:9px;margin:0 0 8px}}
.ap-num{{font-family:var(--sans);font-size:11px;font-weight:700;color:var(--muted);letter-spacing:.08em}}
.ap-card h3{{margin:0;font-size:1.13rem;font-weight:400;letter-spacing:-.01em;flex:1}}
.ap-badge{{
  font-family:var(--sans);font-size:10px;font-weight:700;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted);white-space:nowrap;
  display:inline-flex;align-items:center;gap:6px;
}}
.ap-card.is-open .ap-badge{{color:var(--gold)}}
/* The blurb takes the slack, not the price block. Bottom-anchoring the price
   with margin-top:auto made it land at a different height in every card,
   because everything below it (free tier, note, links) varies in length. This
   way one row of cards agrees on where the price line starts. */
.ap-blurb{{margin:0 0 15px;font-size:.96rem;line-height:1.58;color:var(--ink-soft);flex:1}}

.ap-price{{
  font-family:var(--sans);font-size:14px;font-weight:600;color:var(--ink);
  padding-top:14px;border-top:1px solid var(--line);margin:0;
}}
.ap-price .tag{{font-weight:400;color:var(--muted);font-size:12.5px;display:block;margin-top:2px}}
.ap-free{{margin:11px 0 0;font-size:.9rem;line-height:1.54;color:var(--ink-soft)}}
.ap-free b{{font-family:var(--sans);font-size:10px;font-weight:700;letter-spacing:.13em;
  text-transform:uppercase;color:var(--gold);display:block;margin-bottom:3px}}
.ap-note{{margin:11px 0 0;font-size:.86rem;line-height:1.52;color:var(--muted)}}
.ap-links{{
  margin:15px 0 0;font-family:var(--sans);font-size:13px;
  display:flex;flex-wrap:wrap;gap:6px 16px;
}}
.ap-links a{{color:var(--ink-soft);text-decoration:none;border-bottom:1px solid var(--line)}}
.ap-links a:hover{{color:var(--gold);border-bottom-color:var(--gold)}}
.ap-links a.go{{color:var(--ink);font-weight:600;border-bottom-color:var(--gold)}}

/* Screenshots. A strip that scrolls sideways inside the card, so a card with
   five shots is the same height as a card with one. Each thumbnail opens the
   larger image; there is no script on this page and a lightbox is not a reason
   to add one. */
.ap-shots{{
  display:flex;gap:9px;overflow-x:auto;scroll-snap-type:x mandatory;
  margin:0 0 15px;padding:0 0 6px;scrollbar-width:thin;
}}
.ap-shots a{{flex:0 0 auto;scroll-snap-align:start;line-height:0;border-radius:7px;
  border:1px solid var(--line);overflow:hidden}}
.ap-shots a:hover{{border-color:var(--gold)}}
.ap-shots img{{width:104px;height:auto;aspect-ratio:1290/2796;display:block}}

/* Apple's badge, unmodified, at the size their guidelines give as the floor.
   Black on a light page, white on a dark one, the same swap the logo makes. */
.ap-store{{display:inline-block;margin:15px 0 0;line-height:0}}
.ap-store img{{height:40px;width:auto}}
.ap-store .b-light{{display:none}}
@media (prefers-color-scheme:dark){{
  .ap-store .b-dark{{display:none}}
  .ap-store .b-light{{display:inline}}
}}

.ap-foot{{
  margin:56px 0 0;padding-top:26px;border-top:1px solid var(--line);
  font-size:.95rem;line-height:1.62;color:var(--muted);max-width:70ch;
}}
.ap-foot a{{color:var(--ink-soft)}}

@media (max-width:640px){{
  .ap-top{{flex-wrap:wrap}}
  .ap-badge{{width:100%;margin-top:2px}}
}}
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
    <nav class="nav" aria-label="Main">
      <a href="/#fiction">Fiction</a>
      <a href="/#classics">Classics</a>
      <a href="/blog/">Journal</a>
      <a href="/labs/">Labs</a>
      <a href="/apps/">Apps</a>
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
  </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; {year} Jeffrey L. Carrier. All rights reserved.</span>
      <span><a href="/">Carrier Press</a> is an imprint of Jeffrey L. Carrier.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


SHOTS = OUT / "shots"
# Apple's official artwork, self-hosted so the page still makes no third-party
# request. From https://developer.apple.com/app-store/marketing/guidelines/
BADGES = (pathlib.Path("assets/badges/app-store-black.svg"),
          pathlib.Path("assets/badges/app-store-white.svg"))


def shots(app):
    """The screenshot strip, from whatever make_app_shots.py put on disk."""
    if not app.get("slug"):
        return ""
    folder = SHOTS / app["slug"]
    if not folder.is_dir():
        return ""
    names = sorted(p.name[:-len("-sm.webp")] for p in folder.glob("*-sm.webp"))
    out = ['<div class="ap-shots">']
    for i, name in enumerate(names, 1):
        base = "/apps/shots/%s/%s" % (e(app["slug"]), e(name))
        out.append('<a href="%s.webp"><img src="%s-sm.webp" alt="%s, screenshot %d of %d" '
                   'width="104" height="225" loading="lazy" decoding="async"></a>'
                   % (base, base, e(app["name"]), i, len(names)))
    out.append("</div>")
    return "".join(out)


def store_badge(app):
    """The real badge, and only for an app that is really on the store."""
    if not app.get("store"):
        return ""
    # A live app with no badge file would ship a broken image on the one card
    # that matters most. Refuse the build instead of rendering it.
    missing = [str(p) for p in BADGES if not p.is_file()]
    if missing:
        sys.exit("%s has a store link but the badge art is missing: %s"
                 % (app["name"], ", ".join(missing)))
    return ('<a class="ap-store" href="%s">'
            '<img class="b-dark" src="/%s" alt="Download on the App Store" height="40">'
            '<img class="b-light" src="/%s" alt="Download on the App Store" height="40">'
            '</a>' % (e(app["store"]), BADGES[0], BADGES[1]))


def card(app):
    """One app. The badge, the price and the free line all come from the row."""
    label, cls = apps_data.BADGE[app["status"]]
    open_now = app["status"] in ("live", "browser")
    free = apps_data.free_tier_rule(app)

    out = ['<article class="ap-card%s">' % (" is-open" if open_now else "")]
    out.append('<div class="ap-top">')
    out.append('<span class="ap-num">%02d</span>' % app["n"])
    out.append("<h3>%s</h3>" % e(app["name"]))
    out.append('<span class="ap-badge"><span class="dot dot-%s"></span>%s</span>'
               % (cls, e(label)))
    out.append("</div>")
    # Above the blurb, not below it: the blurb is what stretches to even out a
    # row, so anything under it lands at a different height in every card.
    out.append(shots(app))
    out.append('<p class="ap-blurb">%s</p>' % e(app["blurb"]))

    if app.get("price"):
        out.append('<div class="ap-price">%s' % e(app["price"]))
        if app["shape"] == "sub":
            out.append('<span class="tag">14-day free trial, then the subscription. '
                       'Cancel before it ends and nothing is charged.</span>')
        elif app["shape"] == "once":
            out.append('<span class="tag">One payment. Never a subscription.</span>')
        elif app["shape"] == "b2b":
            out.append('<span class="tag">Free to the person using it. The organisation pays.</span>')
        out.append("</div>")
    elif app["status"] == "design":
        out.append('<div class="ap-price">Not priced yet'
                   '<span class="tag">It is not built, so naming a number would be guessing.</span></div>')
    else:
        # A BUILT app with no price yet (Downpour, 2026-09-25): the price is set
        # when its in-app purchase is created. "It is not built" would be false.
        tag = " One payment, never a subscription." if app["shape"] == "once" else ""
        out.append('<div class="ap-price">Not priced yet'
                   '<span class="tag">The price is set when it reaches the App Store.%s</span></div>'
                   % tag)

    if free:
        # `free_label` (2026-09-25): a TRIAL is not a free tier, and his rule is
        # that apps are not free unless the purchase earns. Rows whose free part
        # is only a taste say "Try it"; the rest keep "Free tier".
        out.append('<p class="ap-free"><b>%s</b>%s</p>'
                   % (e(app.get("free_label", "Free tier")), e(free)))
    if app.get("note"):
        out.append('<p class="ap-note">%s</p>' % e(app["note"]))

    links = []
    if app.get("link"):
        links.append('<a class="go" href="%s">%s &rarr;</a>'
                     % (e(app["link"]), e(app.get("link_label", "Open it"))))
    if app["status"] in ("soon", "build") and not app.get("store"):
        links.append('<a href="mailto:%s?subject=%s">Tell me when %s is out</a>'
                     % (SUPPORT,
                        e(app["name"].replace(" ", "%20")),
                        e(app["name"])))
    if app.get("slug"):
        # The landing page (make_app_pages.py): screens, the web version, and
        # every way to buy or pre-order. Support stays at /<slug>/.
        links.insert(0, '<a class="go" href="/apps/%s/">See it &rarr;</a>' % e(app["slug"]))
        links.append('<a href="/%s/">Support</a>' % e(app["slug"]))
        links.append('<a href="/%s/privacy/">Privacy</a>' % e(app["slug"]))
    out.append(store_badge(app))
    if links:
        out.append('<div class="ap-links">%s</div>' % "".join(links))

    out.append("</article>")
    return "\n".join(out)


def build():
    apps = apps_data.APPS
    n_open = sum(1 for a in apps if a["status"] in ("live", "browser"))
    n_soon = sum(1 for a in apps if a["status"] in ("soon", "build"))

    b = [HEAD]
    b.append('<section class="wrap" style="padding:52px 0 0">')
    b.append('<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Carrier Ventures</span></p>')
    b.append('<h1 style="font-size:clamp(1.7rem,4vw,2.5rem);font-weight:400;'
             'letter-spacing:-.02em;margin:0 0 22px">What these cost</h1>')

    b.append('<div class="ap-intro">')
    # Counted, not typed: this said "Forty-four" and went wrong the day
    # Downpour's row was added (2026-09-25).
    b.append("<p>%s small tools, each built to do exactly one thing for exactly "
             % count_words(len(apps_data.APPS)) +
             "one kind of person. This page says what each one costs, what you get "
             "without paying anything, and which ones are not out yet.</p>")
    # Rewritten 2026-09-25 when the first web sale opened. The old line said
    # "Nothing here takes your money yet", which stopped being true the moment
    # Boat Ready for the Web was published on Gumroad.
    b.append("<p><strong>None of them is on the App Store yet.</strong> Every price below is "
             "the price it will carry there, and every card says where that app actually is. "
             "Some can already be used, and bought, in a browser: those cards say so and "
             "link to their page. If you want to know when one ships, the card has a link "
             "that sends an email and does nothing else.</p>")
    b.append("</div>")

    b.append('<div class="ap-plans">')
    b.append('<div class="ap-plan"><h3>Free tier</h3><span class="big">Not a countdown</span>'
             "<p>Every app has a free tier that keeps working. It is capped by how much "
             "you use it, not by how long you have had it, so an app you open twice a "
             "year is still useful the second time.</p></div>")
    b.append('<div class="ap-plan"><h3>Free trial</h3><span class="big">14 days, then you decide</span>'
             "<p>Every subscription opens with fourteen days of everything. Cancel before "
             "it ends and you are not charged. The trial is set up through the App Store, "
             "so cancelling is one screen in your own Apple account and not a conversation "
             "with us.</p></div>")
    b.append('<div class="ap-plan"><h3>One payment</h3><span class="big">Where one payment is right</span>'
             "<p>Some of these do a job that finishes. Configuring parental controls, "
             "cancelling a subscription, checking a boat. Those are sold once. Billing "
             "monthly for a job that took an afternoon would be a worse product.</p></div>")
    b.append("</div>")

    b.append('<div class="ap-rules"><ul>')
    b.append("<li><strong>No advertising, ever.</strong> Not on the free tier, not anywhere.</li>")
    b.append("<li><strong>No analytics and no engagement loop.</strong> No streaks, no "
             "gamification, no notifications designed to pull you back. A tool you use "
             "less often because it worked is a tool that worked.</li>")
    b.append("<li><strong>The free tier is not a demo.</strong> Where an app answers a "
             "question, answering it is free and stays free. What you pay for is keeping, "
             "comparing and carrying that answer forward.</li>")
    b.append("<li><strong>Nothing is sold before the part you would rely on is finished.</strong> "
             "Several of these are running software held back over one missing piece, and "
             "each card names the piece.</li>")
    b.append("</ul></div>")

    b.append('<div class="ap-legend">')
    for key, (label, cls) in (("browser", apps_data.BADGE["browser"]),
                              ("live", apps_data.BADGE["live"]),
                              ("soon", apps_data.BADGE["soon"]),
                              ("design", apps_data.BADGE["design"])):
        b.append('<span class="k"><span class="dot dot-%s"></span>%s</span>' % (cls, e(label)))
    b.append("</div>")

    for status, title, desc in apps_data.GROUPS:
        rows = [a for a in apps if a["status"] == status]
        if not rows:
            continue
        count = "%d %s" % (len(rows), "tool" if len(rows) == 1 else "tools")
        b.append('<div class="ap-group"><span class="count">%s</span><h2>%s</h2><p>%s</p></div>'
                 % (e(count), e(title), e(desc)))
        b.append('<div class="ap-grid">')
        b.extend(card(a) for a in rows)
        b.append("</div>")

    opens = ("One tool opens in a browser today" if n_open == 1
             else "%d tools open in a browser today" % n_open)
    b.append('<p class="ap-foot">%s, and %d more are waiting on a '
             'store rather than on a feature. <a href="/labs/">Labs</a> is the build log '
             'behind this page: what is finished, what is missing from each, and what is '
             'still only a specification. Questions to '
             '<a href="mailto:%s">%s</a>.</p>' % (opens, n_soon, SUPPORT, SUPPORT))
    b.append("</section>")
    b.append(FOOT.format(year=datetime.date.today().year))

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text("\n".join(b), encoding="utf-8")
    nav.patch(OUT / "index.html")
    print("wrote apps/index.html  --  %d apps, %d open, %d coming soon"
          % (len(apps), n_open, n_soon))


if __name__ == "__main__":
    sys.exit(build())
