#!/usr/bin/env python3
"""
/play/ -- the game, and where to buy it.

    python3 make_play.py

*** IT REFUSES TO RUN WHILE play_data.ITCH_URL IS None, AND THAT IS THE FEATURE. ***

The game is sold on itch.io because a browser game cannot be paywalled on
GitHub Pages at all: this site is static files, and a gate written in its own
JavaScript is a lock with the key taped to it. itch serves the HTML5 embed only
to an account that bought the project, which is a real gate.

The itch project is created by hand and does not exist yet. A page written now
and published now would advertise a game with nowhere to go, and a "coming soon"
button is the single most forgettable thing on a website -- it gets left up for
a year because nothing breaks while it is wrong. So this script writes nothing
at all until there is a URL, nav.py emits no Play link, and build.py leaves
/play/ out of the sitemap. One constant turns all three on together.

WHY THE CAST AND NOT SCREENSHOTS. The character art is finished; the world art
is not. The page says so in its first paragraph, above the price, in the same
words the itch description uses. Leading it with screenshots of the scenery that
paragraph apologises for would undercut it. Screenshots go on when the art does.
"""
import datetime, html, pathlib, sys

import nav
import play_data as P

DOMAIN = "carrierpress.com"
OUT = pathlib.Path("play")
SUPPORT = "support@carrierpress.com"


def e(x):
    return html.escape(str(x), quote=True)


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Play | Carrier Press</title>
<meta name="description" content="{tagline}">
<link rel="canonical" href="https://{domain}/play/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{tagline}">
<meta property="og:url" content="https://{domain}/play/">
<meta property="og:image" content="https://{domain}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
/* Scoped here, same reasoning as /labs/, /apps/ and /audio/. Every colour is an
   existing token, so dark mode follows without a second block. */

.pl-top{{display:grid;grid-template-columns:336px 1fr;gap:38px;align-items:start;margin:8px 0 0}}
.pl-hero img{{display:block;width:100%;height:auto;max-width:336px}}
.pl-top h1{{font-size:clamp(1.6rem,3.6vw,2.3rem);font-weight:400;letter-spacing:-.02em;margin:0 0 12px}}
.pl-tag{{font-size:1.12rem;line-height:1.55;color:var(--ink-soft);margin:0 0 22px;max-width:52ch}}

/* The disclosure sits ABOVE the price, not under it. That order is the whole
   argument for the price being honest rather than cheap. */
.pl-disc{{
  background:var(--paper-2);border:1px solid var(--line);border-left:3px solid var(--gold);
  border-radius:4px;padding:20px 22px;margin:0 0 22px;
}}
.pl-disc p{{margin:0;line-height:1.62;font-size:.97rem}}
.pl-disc b{{
  font-family:var(--sans);font-size:10.5px;font-weight:700;letter-spacing:.16em;
  text-transform:uppercase;color:var(--gold);display:block;margin-bottom:7px;
}}

.pl-buy{{display:flex;flex-wrap:wrap;gap:14px 18px;align-items:center;margin:0 0 10px}}
.pl-price{{font-family:var(--sans);font-size:1.5rem;font-weight:600;letter-spacing:-.01em}}
.pl-note{{font-family:var(--sans);font-size:13px;color:var(--muted);margin:0}}

.pl-hook{{margin:46px 0 0;padding-top:30px;border-top:1px solid var(--line)}}
.pl-hook p{{margin:0;font-size:1.08rem;line-height:1.62;max-width:64ch}}

.pl-facts{{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(262px,1fr));
  gap:18px;margin:34px 0 0;
}}
.pl-fact{{border:1px solid var(--line);border-radius:5px;padding:19px 20px}}
.pl-fact h3{{font-size:1.02rem;font-weight:600;margin:0 0 7px;letter-spacing:-.005em}}
.pl-fact p{{margin:0;font-size:.93rem;line-height:1.56;color:var(--ink-soft)}}

.pl-sec{{margin:52px 0 18px;padding-top:26px;border-top:1px solid var(--line)}}
.pl-sec h2{{font-size:clamp(1.15rem,2.4vw,1.42rem);margin:0 0 6px;font-weight:400;letter-spacing:-.01em}}
.pl-sec p{{margin:0;color:var(--ink-soft);font-size:.96rem;max-width:66ch}}

.pl-cast{{display:flex;flex-wrap:wrap;gap:22px 26px;align-items:flex-end;margin:0}}
.pl-cast figure{{margin:0;text-align:center;width:104px}}
.pl-cast img{{display:block;width:auto;height:118px;margin:0 auto 8px}}
.pl-cast figcaption{{
  font-family:var(--sans);font-size:11.5px;font-weight:600;letter-spacing:.04em;color:var(--muted);
}}

table.pl-keys{{border-collapse:collapse;font-size:.95rem}}
table.pl-keys td{{padding:9px 26px 9px 0;border-bottom:1px solid var(--line);vertical-align:baseline}}
table.pl-keys tr:last-child td{{border-bottom:0}}
table.pl-keys td.k{{font-family:var(--sans);font-size:13px;color:var(--muted);white-space:nowrap}}

.pl-foot{{
  margin:56px 0 0;padding-top:26px;border-top:1px solid var(--line);
  font-size:.95rem;line-height:1.62;color:var(--muted);max-width:70ch;
}}
.pl-foot a{{color:var(--ink-soft)}}

@media(max-width:720px){{
  .pl-top{{grid-template-columns:1fr;gap:24px}}
  .pl-hero img{{max-width:220px;margin:0 auto}}
  .pl-disc{{padding:17px 18px}}
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
      <a href="/audio/">Audio</a>
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


def build():
    if not P.ITCH_URL:
        sys.exit(
            "make_play.py: nothing written.\n"
            "  play_data.ITCH_URL is None, so there is nowhere to send a buyer.\n"
            "  The itch project has to be created by hand first: account,\n"
            "  payouts, terms, then upload release/*.zip and Publish. The\n"
            "  settings and the page copy are in the game repo under\n"
            "  docs/ITCH_RELEASE.md and docs/ITCH_PAGE_COPY.md.\n"
            "  Then set ITCH_URL in play_data.py and run:\n"
            "      python3 make_play.py && python3 build.py && python3 nav.py")

    b = [HEAD.format(domain=DOMAIN, title=e(P.TITLE), tagline=e(P.TAGLINE))]
    b.append('<section class="wrap" style="padding:52px 0 0">')

    b.append('<div class="pl-top">')
    b.append('<div class="pl-hero"><img src="%s" alt="Captain Cubemelon holding the Gravity Wrench" '
             'width="336" height="420"></div>' % e(P.HERO))
    b.append("<div>")
    b.append('<p class="sec-head" style="margin:0 0 10px"><span class="kicker">%s &middot; v%s</span></p>'
             % (e(P.STATUS), e(P.VERSION)))
    b.append("<h1>%s</h1>" % e(P.TITLE))
    b.append('<p class="pl-tag">%s</p>' % e(P.TAGLINE))

    b.append('<div class="pl-disc"><b>Read this first</b><p>%s</p></div>' % e(P.DISCLOSURE))

    b.append('<div class="pl-buy">')
    b.append('<span class="pl-price">%s</span>' % e(P.PRICE))
    b.append('<a class="btn btn-gold" href="%s">Play it on itch.io</a>' % e(P.ITCH_URL))
    b.append("</div>")
    b.append('<p class="pl-note">It runs in the browser. Click the game, then press Enter, '
             'because a browser only sends keys to a game once you have clicked it.</p>')
    b.append("</div></div>")

    b.append('<div class="pl-hook"><p>%s</p></div>' % e(P.HOOK))

    b.append('<div class="pl-facts">')
    for h, t in P.FACTS:
        b.append('<div class="pl-fact"><h3>%s</h3><p>%s</p></div>' % (e(h), e(t)))
    b.append("</div>")

    b.append('<div class="pl-sec"><h2>The cast</h2><p>These are finished. The worlds '
             'they walk through are not, which is what the note at the top is about.</p></div>')
    b.append('<div class="pl-cast">')
    b.append('<figure><img src="/assets/game/captain_cubemelon.png" alt="Captain Cubemelon">'
             '<figcaption>Captain Cubemelon</figcaption></figure>')
    for f, name in P.CAST:
        b.append('<figure><img src="/assets/game/%s" alt="%s"><figcaption>%s</figcaption></figure>'
                 % (e(f), e(name), e(name)))
    b.append("</div>")

    b.append('<div class="pl-sec"><h2>Controls</h2><p>Keyboard and a computer. There is no '
             'gamepad or touch support yet, so this is not one for a phone.</p></div>')
    b.append('<table class="pl-keys"><tbody>')
    for what, keys in P.CONTROLS:
        b.append('<tr><td class="k">%s</td><td>%s</td></tr>' % (e(what), e(keys)))
    b.append("</tbody></table>")

    b.append('<p class="pl-foot">Captain Cubemelon started as comics and twelve novels, and '
             'the game shares their continuity rather than retelling it. You do not need to '
             'have read any of them. The books are on the <a href="/">shelf</a>, and the '
             'twelve novels are among the titles compiled for <a href="/audio/">audio</a>. '
             'Questions to <a href="mailto:%s">%s</a>.</p>' % (SUPPORT, SUPPORT))
    b.append("</section>")
    b.append(FOOT.format(year=datetime.date.today().year))

    OUT.mkdir(exist_ok=True)
    path = OUT / "index.html"
    path.write_text("\n".join(b), encoding="utf-8")
    nav.patch(path)          # the Play link exists now, so every page needs it
    print("wrote play/index.html  --  %s, %s, %s" % (P.STATUS, P.PRICE, P.ITCH_URL))


if __name__ == "__main__":
    build()
