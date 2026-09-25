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
import datetime, html, pathlib, sys

import apps_data
import commerce
import nav

DOMAIN = "carrierpress.com"
SUPPORT = "support@carrierpress.com"
OUT = pathlib.Path("apps")
SHOTS = OUT / "shots"


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
.lp{{padding-top:52px}}  /* top only: .wrap owns the side gutter */
.lp-kick{{font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.16em;
  text-transform:uppercase;color:var(--gold);display:inline-flex;gap:7px;align-items:center}}
.lp-kick .dot{{width:8px;height:8px;border-radius:50%;background:var(--gold-bright)}}
.lp h1{{font-size:clamp(1.9rem,5vw,2.8rem);font-weight:400;letter-spacing:-.02em;margin:12px 0 14px}}
.lp-blurb{{font-size:1.12rem;line-height:1.6;color:var(--ink-soft);max-width:62ch;margin:0}}
.lp-price{{font-family:var(--sans);font-size:15px;font-weight:600;margin:22px 0 0}}
.lp-price span{{display:block;font-weight:400;font-size:13px;color:var(--muted);margin-top:3px}}
.lp-actions{{display:flex;flex-wrap:wrap;gap:12px;margin:26px 0 0}}
.lp-btn{{font-family:var(--sans);font-size:15px;font-weight:600;text-decoration:none;
  border-radius:6px;padding:13px 20px;border:1.5px solid var(--gold);color:var(--ink);
  display:inline-flex;flex-direction:column;line-height:1.25}}
.lp-btn small{{font-weight:400;font-size:12px;color:var(--muted);margin-top:3px}}
.lp-btn.primary{{background:var(--gold);color:#111}}
.lp-btn.primary small{{color:#111;opacity:.75}}
.lp-btn:hover{{border-color:var(--ink)}}
.lp-shots{{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;
  margin:40px 0 0;padding:0 0 10px;scrollbar-width:thin}}
.lp-shots a{{flex:0 0 auto;scroll-snap-align:start;line-height:0;border-radius:12px;
  border:1px solid var(--line);overflow:hidden}}
.lp-shots img{{width:220px;height:auto;aspect-ratio:1290/2796;display:block}}
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
@media(max-width:520px){{.lp-shots img{{width:180px}}.lp-btn{{width:100%}}}}
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
<section class="wrap lp">
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
    label, _ = apps_data.BADGE[app["status"]]
    web_open = bool(c.get("web"))
    if web_open:
        label = "Open in your browser"
    names = shot_names(slug)
    og = ("https://%s/apps/shots/%s/%s.webp" % (DOMAIN, slug, names[0]) if names
          else "https://%s/assets/og-image.png" % DOMAIN)

    b = [HEAD.format(name=e(app["name"]), blurb=e(app["blurb"]), slug=e(slug),
                     domain=DOMAIN, og=e(og))]
    b.append('<span class="lp-kick"><span class="dot"></span>%s</span>' % e(label))
    b.append("<h1>%s</h1>" % e(app["name"]))
    b.append('<p class="lp-blurb">%s</p>' % e(app["blurb"]))
    price, tag = price_line(app)
    if c.get("buy") and c.get("buy_price"):
        # Two prices on one page must never read as a contradiction.
        price = "%s in the app" % price
        tag = "%s The web version is %s once." % (tag, c["buy_price"])
    b.append('<p class="lp-price">%s<span>%s</span></p>' % (e(price), e(tag)))

    acts = []
    acts.append(button(c.get("web"), "Open it in your browser",
                       "No download, no account", primary=True))
    acts.append(button(c.get("buy"), "Buy the web version",
                       "%s once, license key by email" % c.get("buy_price", "")))
    acts.append(button(c.get("pre"), "Pre-order",
                       "%s, charged only when it launches" % c.get("pre_price", ""),
                       primary=not web_open))
    if app["status"] != "live":
        acts.append(button("mailto:%s?subject=%s" % (SUPPORT, app["name"].replace(" ", "%20")),
                           "Tell me when it is out", "One email, nothing else"))
    acts = [a for a in acts if a]
    b.append('<div class="lp-actions">%s</div>' % "".join(acts))

    if names:
        b.append('<div class="lp-shots">')
        for i, n in enumerate(names, 1):
            base = "/apps/shots/%s/%s" % (e(slug), e(n))
            b.append('<a href="%s.webp"><img src="%s.webp" alt="%s, screen %d of %d" '
                     'width="220" height="477" loading="lazy" decoding="async"></a>'
                     % (base, base, e(app["name"]), i, len(names)))
        b.append("</div>")
    else:
        b.append('<p class="lp-soon">Screens are coming. This app is %s, and its '
                 'screenshots go up here the day they are captured from the real build, '
                 'not mocked up before it.</p>'
                 % ("still in design" if app["status"] == "design" else "being finished"))

    boxes = []
    free = apps_data.free_tier_rule(app)
    if free:
        boxes.append('<div class="lp-box"><h2>%s</h2><p>%s</p></div>'
                     % (e(app.get("free_label", "Without paying")), e(free)))
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
