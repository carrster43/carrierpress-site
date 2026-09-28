#!/usr/bin/env python3
"""
One landing page per app, at /apps/<slug>/.

    python3 make_app_pages.py

WHY NOT /<slug>/. That URL is the SUPPORT URL inside every App Store Connect
record, and App Review opens it. A sales page with Gumroad buttons there would
put a purchase route outside the App Store on the page Apple reads, which is a
3.1.1 conversation nobody needs. So support stays at /<slug>/, and the page a
stranger lands on to see, try, pre-order or tip lives here.

WHAT A PAGE SHOWS, ALL OF IT FROM DATA:
    apps_data.py  name, blurb, status, price, what the trial gives, what pays
    commerce.py   the web app path and every Gumroad URL
    apps/shots/   whatever make_app_shots.py captured

A button appears only when its URL exists. An app with nothing to sell yet gets
"Tell me when it is out", which is a mailto and needs no form service, no
tracking script and no privacy claim this site cannot back.
"""
import datetime, html, json, pathlib, sys

import apps_data
import commerce
import nav

DOMAIN = "carrierpress.com"
SUPPORT = "support@carrierpress.com"
OUT = pathlib.Path("apps")
SHOTS = OUT / "shots"
ICONS = OUT / "icons"
# slug -> hero colour, written by make_app_shots.py from each app's own icon.
LOOKS = (json.loads((ICONS / "accents.json").read_text())
         if (ICONS / "accents.json").exists() else {})


def e(x):
    return html.escape(str(x), quote=True)


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} | Carrier Press</title>
<meta name="description" content="{blurb}">
<link rel="canonical" href="https://{domain}/apps/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{blurb}">
<meta property="og:url" content="https://{domain}/apps/{slug}/">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
/* Scoped here for the same reason as /apps/ and /labs/: styles.css belongs to
   the book side. Every colour is an existing token, so dark mode follows. */
.lp{{padding-top:44px}}  /* top only: .wrap owns the side gutter */
/* THE HERO. One colour per app, taken from its own icon by make_app_shots.py
   and darkened there until white text clears 7:1, so it is fixed in both
   themes on purpose: it is the app's colour, not the site's. */
.lp-hero{{--accent:var(--navy);background-color:var(--accent);
  background-image:radial-gradient(120% 110% at 15% 0%,rgba(255,255,255,.16),rgba(255,255,255,0) 60%),
  linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.28));color:#fff;padding:56px 0 64px}}
.lp-hero-in{{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:56px;align-items:center}}
.lp-id{{display:flex;gap:16px;align-items:center}}
.lp-icon{{width:72px;height:72px;border-radius:17px;box-shadow:0 10px 26px rgba(0,0,0,.35);flex:0 0 auto}}
.lp-name{{display:block;font-family:var(--sans);font-size:13px;font-weight:700;letter-spacing:.16em;
  text-transform:uppercase;color:rgba(255,255,255,.86)}}
.lp-status{{display:inline-block;margin-top:6px;font-family:var(--sans);font-size:12px;font-weight:600;
  border:1px solid rgba(255,255,255,.45);border-radius:99px;padding:3px 10px;color:#fff}}
.lp-hero h1{{font-family:var(--sans);font-size:clamp(2.2rem,6vw,3.5rem);font-weight:800;line-height:1.04;
  letter-spacing:-.03em;margin:26px 0 16px;color:#fff;text-wrap:balance}}
.lp-blurb{{font-size:1.08rem;line-height:1.6;color:rgba(255,255,255,.9);max-width:56ch;margin:0}}
.lp-cta{{margin:30px 0 0}}
.lp-btn{{font-family:var(--sans);font-size:15px;font-weight:600;text-decoration:none;
  border-radius:6px;padding:13px 20px;border:1.5px solid var(--gold);color:var(--ink);
  display:inline-flex;flex-direction:column;line-height:1.25}}
.lp-btn small{{font-weight:400;font-size:12px;color:var(--muted);margin-top:3px}}
.lp-btn:hover{{border-color:var(--ink)}}
.lp-btn.hero{{background:#fff;color:var(--accent);border:0;font-size:17px;font-weight:700;
  padding:16px 28px;border-radius:10px;box-shadow:0 10px 24px rgba(0,0,0,.25)}}
.lp-btn.hero small{{color:var(--accent);opacity:.75;font-weight:500}}
.lp-btn.hero:hover{{transform:translateY(-1px)}}
.lp-price{{font-family:var(--sans);font-size:15px;font-weight:600;margin:20px 0 0;color:#fff}}
.lp-price span{{display:block;font-weight:400;font-size:13px;color:rgba(255,255,255,.8);margin-top:3px}}
.lp-more{{margin:16px 0 0;font-family:var(--sans);font-size:14px;display:flex;flex-wrap:wrap;gap:6px 22px}}
.lp-more a{{color:#fff;text-underline-offset:3px}}
.lp-more small{{color:rgba(255,255,255,.75)}}
.lp-hero-shot{{line-height:0}}
.lp-hero-shot img{{width:100%;height:auto;aspect-ratio:1290/2796;border-radius:22px;
  box-shadow:0 30px 60px rgba(0,0,0,.4)}}
.lp-h2{{font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.16em;
  text-transform:uppercase;color:var(--gold);margin:0 0 14px}}
@media(max-width:820px){{.lp-hero-in{{grid-template-columns:1fr;gap:40px}}
  .lp-hero-shot{{max-width:250px;margin:0 auto}}.lp-hero{{padding:40px 0 48px}}}}
.lp-shots{{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;
  margin:0;padding:0 0 10px;scrollbar-width:thin}}
.lp-shots a{{flex:0 0 auto;scroll-snap-align:start;line-height:0;border-radius:12px;
  border:1px solid var(--line);overflow:hidden}}
.lp-shots img{{width:240px;height:auto;aspect-ratio:1290/2796;display:block}}
.lp-soon{{margin:40px 0 0;border:1px dashed var(--line);border-radius:8px;padding:26px;
  color:var(--muted);font-size:.95rem;max-width:62ch}}
.lp-split{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin:40px 0 0}}
.lp-box{{background:var(--paper-2);border:1px solid var(--line);border-radius:5px;padding:20px 22px}}
.lp-box h2{{font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.16em;
  text-transform:uppercase;color:var(--gold);margin:0 0 9px}}
.lp-box p{{margin:0;line-height:1.6;font-size:.97rem;color:var(--ink-soft)}}
.lp-tip{{margin:44px 0 0;padding:22px 24px;border-left:3px solid var(--gold);
  background:var(--paper-2);border-radius:4px;max-width:70ch}}
.lp-tip p{{margin:0 0 12px;line-height:1.6}}
.lp-tip p:last-child{{margin:0}}
.lp-tip .fine{{font-size:.86rem;color:var(--muted)}}
.lp-foot{{margin:48px 0 0;padding-top:22px;border-top:1px solid var(--line);
  font-family:var(--sans);font-size:13px;display:flex;flex-wrap:wrap;gap:8px 18px}}
.lp-foot a{{color:var(--ink-soft)}}
@media(max-width:520px){{.lp-shots img{{width:190px}}.lp-btn.hero{{width:100%}}}}
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

FOOT = """</section>
</main>
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


def shot_names(slug):
    folder = SHOTS / slug
    if not folder.is_dir():
        return []
    return sorted(p.name[:-len("-sm.webp")] for p in folder.glob("*-sm.webp"))


def button(url, label, sub="", primary=False):
    """A button only ever exists with a real URL behind it."""
    if not url:
        return ""
    external = url.startswith("http")
    return ('<a class="lp-btn%s" href="%s"%s>%s%s</a>'
            % (" primary" if primary else "", e(url),
               ' target="_blank" rel="noopener"' if external else "",
               e(label), "<small>%s</small>" % e(sub) if sub else ""))


def hero_button(url, label, sub=""):
    """The single white button in the hero."""
    external = url.startswith("http")
    return ('<a class="lp-btn hero" href="%s"%s>%s%s</a>'
            % (e(url), ' target="_blank" rel="noopener"' if external else "",
               e(label), "<small>%s</small>" % e(sub) if sub else ""))


def text_link(url, label, sub=""):
    """Everything that did not win the hero button: present, but quiet."""
    external = url.startswith("http")
    return ('<span><a href="%s"%s>%s</a>%s</span>'
            % (e(url), ' target="_blank" rel="noopener"' if external else "",
               e(label), " <small>%s</small>" % e(sub) if sub else ""))


def price_line(app):
    if not app.get("price"):
        if app["status"] == "design":
            return ("Not priced yet", "It is not built, so naming a number would be guessing.")
        return ("Not priced yet", "The price is set when it reaches the App Store.")
    tag = {"sub": "In the App Store app: a free trial, then the subscription.",
           "once": "One payment. Never a subscription.",
           "b2b": "Free to the person using it. The organisation pays."}.get(app["shape"], "")
    return (app["price"], tag)


def page(app):
    slug = app["slug"]
    c = commerce.for_app(slug)
    # The chip says where the app IS. The hero button already says what to do,
    # so a chip reading "Open in your browser" beside it would be the same words twice.
    label, _ = apps_data.BADGE[app["status"]]
    names = shot_names(slug)
    og = ("https://%s/apps/shots/%s/%s.webp" % (DOMAIN, slug, names[0]) if names
          else "https://%s/assets/og-image.png" % DOMAIN)

    b = [HEAD.format(name=e(app["name"]), blurb=e(app["blurb"]), slug=e(slug),
                     domain=DOMAIN, og=e(og))]
    look = LOOKS.get(slug)
    style = ' style="--accent:%s"' % look if look else ""
    icon = ICONS / ("%s.webp" % slug)

    # ---- The hero: who it is, what it does, ONE thing to do next. ----
    b.append('<section class="lp-hero"%s><div class="wrap lp-hero-in"><div>' % style)
    ident = ['<div class="lp-id">']
    if icon.exists():
        ident.append('<img class="lp-icon" src="/%s" alt="" width="72" height="72">' % e(icon.as_posix()))
    ident.append('<div><span class="lp-name">%s</span><span class="lp-status">%s</span></div></div>'
                 % (e(app["name"]), e(label)))
    b.append("".join(ident))
    b.append("<h1>%s</h1>" % e(app.get("headline") or app["name"]))
    b.append('<p class="lp-blurb">%s</p>' % e(app["blurb"]))

    # The one button. Whatever is most useful RIGHT NOW wins the slot, and
    # everything else drops to a quiet text link underneath. Three equal
    # buttons read as three equal asks, and a stranger acts on none of them.
    notify = None
    if app["status"] != "live":
        notify = ("mailto:%s?subject=%s" % (SUPPORT, app["name"].replace(" ", "%20")),
                  "Tell me when it is out", "One email, nothing else")
    offers = [(c.get("web"), "Open it in your browser", "No download, no account"),
              (c.get("pre"), "Pre-order", "%s, charged only when it launches" % c.get("pre_price", "")),
              notify and notify]
    offers = [o for o in offers if o and o[0]]
    if offers:
        b.append('<div class="lp-cta">%s</div>' % hero_button(*offers[0]))

    price, tag = price_line(app)
    if c.get("buy") and c.get("buy_price"):
        # Two prices on one page must never read as a contradiction.
        price = "%s in the app" % price
        tag = "%s The web version is %s once." % (tag, c["buy_price"])
    b.append('<p class="lp-price">%s<span>%s</span></p>' % (e(price), e(tag)))

    more = []
    if c.get("buy"):
        more.append((c["buy"], "Buy the web version",
                     "%s once, license key by email" % c.get("buy_price", "")))
    more += offers[1:]
    if more:
        b.append('<div class="lp-more">%s</div>' % "".join(text_link(*m) for m in more))
    b.append("</div>")

    if names:
        first = "/apps/shots/%s/%s.webp" % (e(slug), e(names[0]))
        b.append('<div class="lp-hero-shot"><img src="%s" alt="%s, screen 1 of %d" '
                 'width="290" height="629" decoding="async"></div>' % (first, e(app["name"]), len(names)))
    b.append("</div></section>")

    # ---- Below the fold: the rest of the screens, then the terms. ----
    b.append('<section class="wrap lp">')
    if len(names) > 1:
        b.append('<h2 class="lp-h2">More screens</h2><div class="lp-shots">')
        for i, n in enumerate(names[1:], 2):
            base = "/apps/shots/%s/%s" % (e(slug), e(n))
            b.append('<a href="%s.webp"><img src="%s.webp" alt="%s, screen %d of %d" '
                     'width="240" height="520" loading="lazy" decoding="async"></a>'
                     % (base, base, e(app["name"]), i, len(names)))
        b.append("</div>")
    elif not names:
        b.append('<p class="lp-soon" style="margin-top:0">Screens are coming. This app is %s, and its '
                 'screenshots go up here the day they are captured from the real build, '
                 'not mocked up before it.</p>'
                 % ("still in design" if app["status"] == "design" else "being finished"))

    boxes = []
    free = apps_data.free_tier_rule(app)
    if free:
        boxes.append('<div class="lp-box"><h2>%s</h2><p>%s</p></div>'
                     % (e(apps_data.free_label(app)), e(free)))
    if app.get("note"):
        boxes.append('<div class="lp-box"><h2>What the purchase buys</h2><p>%s</p></div>'
                     % e(app["note"]))
    if boxes:
        b.append('<div class="lp-split">%s</div>' % "".join(boxes))

    if commerce.TIP_URL:
        b.append('<div class="lp-tip"><p><strong>Support the build.</strong> These apps '
                 'are made by one independent developer, with no advertising and no '
                 'investors. If you want to see this one finished, a tip helps pay for '
                 'the time.</p><p>%s</p><p class="fine">A tip buys nothing and unlocks '
                 'nothing. It is a payment to Jeffrey L. Carrier, not a donation to a '
                 'charity, and it is not tax-deductible.</p></div>'
                 % button(commerce.TIP_URL, "Leave a tip", "Pay what you want, from $3"))

    foot = ['<a href="/apps/">All apps and prices</a>']
    if pathlib.Path(slug, "index.html").exists():
        foot.append('<a href="/%s/">Support</a>' % e(slug))
    if pathlib.Path(slug, "privacy", "index.html").exists():
        foot.append('<a href="/%s/privacy/">Privacy</a>' % e(slug))
    b.append('<div class="lp-foot">%s</div>' % "".join(foot))
    b.append(FOOT.format(year=datetime.date.today().year))

    out = OUT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(b), encoding="utf-8")
    nav.patch(out)
    return out


def check():
    """Refuse to build a page that links to a web app that is not on disk."""
    bad = []
    for slug, c in commerce.WEB.items():
        web = c.get("web")
        if web and not pathlib.Path(web.strip("/"), "index.html").exists():
            bad.append("%s: commerce.WEB says %s but nothing is there" % (slug, web))
    return bad


if __name__ == "__main__":
    problems = check()
    if problems:
        sys.exit("\n".join(problems))
    n = 0
    for a in apps_data.APPS:
        if a.get("slug"):
            page(a)
            n += 1
    print("wrote %d landing pages under apps/<slug>/" % n)
