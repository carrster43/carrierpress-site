#!/usr/bin/env python3
"""
/shop/: Carrier Press merch (author 2026-11-27: "Printful Quick Store").

    python3 make_shop.py      # build.py runs it too, before the sitemap

WHY THE PAGE LINKS OUT. carrierpress.com is a static site with no cart, so
checkout lives on Printful's hosted Quick Store, carrierpress.printful.me:
Printful takes the payment, prints, ships, and pays the press its share. This
page is the shop window; every tile opens that product's page on the store.

DATA. shop_data.json, one record per product (95 on 2026-11-27):
    {"group": "calendar"|"wall"|"cards"|"wear"|"cubemelon", "title": str, "price": "24.99",
     "url": "https://carrierpress.printful.me/product/...", "img": "https://cdn.printful.me/..."}
Read from the live storefront. The images are the store's own 360 px product
photos on Printful's CDN (the largest size it serves for listings); they are
linked, not copied, so a photo Printful regenerates updates here too. If a
product is removed from the store, remove its record here.

Rules kept here: no em or en dashes; the AI-art note is the LAST line of its
section (author 2026-11-14); US shipping only, said plainly, because Quick
Stores only ship to US addresses.
"""
import datetime, html, json, pathlib

import nav

DOMAIN = "carrierpress.com"
STORE = "https://carrierpress.printful.me/"

GROUPS = [
    ("calendar", "The 2027 calendar",
     "A Year of Weird Fiction: twelve covers and twelve lines from the books, 11 x 17 in, weeks starting on Sunday."),
    ("wall", "Wall art",
     "Book covers and plates as posters and canvas, printed on heavy matte paper or stretched canvas."),
    ("cards", "Note cards",
     "Folded 4 x 6 cards, blank inside, each with an envelope. Pick any mix: covers, plates and lines from the books."),
    ("wear", "Wear and carry",
     "Tees, a tote, a mug and stickers with the Carrier Press pigeon and lines from The King in Yellow."),
    ("cubemelon", "Captain Cubemelon",
     "Posters and stickers from the comic."),
]


def e(x):
    return html.escape(str(x), quote=True)


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shop posters, note cards and tees | Carrier Press</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{domain}/shop/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="The Carrier Press shop">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://{domain}/shop/">
<meta property="og:image" content="https://{domain}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
.sh h1{{font-size:clamp(1.8rem,6vw,2.6rem);font-weight:400;letter-spacing:-.02em;margin:0 0 12px}}
.sh .lede{{font-size:1.08rem;line-height:1.6;color:var(--ink-soft);max-width:62ch;margin:0 0 20px}}
.sh-jump{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 8px;padding:0;list-style:none}}
.sh-jump a{{display:inline-block;font-family:var(--sans);font-size:14px;font-weight:600;text-decoration:none;
  color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:9px 14px}}
.sh-jump a:hover,.sh-jump a:focus-visible{{border-color:var(--gold)}}
.sh-g{{padding:34px 0 6px;border-top:1px solid var(--line);margin-top:30px}}
.sh-g>h2{{font-size:clamp(1.35rem,4vw,1.7rem);font-weight:400;margin:0 0 4px}}
.sh-g>p{{font-family:var(--sans);font-size:14px;color:var(--muted);margin:0 0 18px;max-width:70ch}}
.sh-row{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:20px 16px;margin:0;padding:0;list-style:none}}
.sh-row a{{display:block;text-decoration:none;color:var(--ink)}}
.sh-row img{{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;border-radius:6px;box-shadow:var(--shadow);background:var(--paper-2)}}
.sh-row span{{display:block;font-size:14px;line-height:1.35;margin-top:8px}}
.sh-row b{{display:block;font-family:var(--sans);font-size:13px;font-weight:600;color:var(--ink-soft);margin-top:3px}}
.sh-row a:hover span,.sh-row a:focus-visible span{{text-decoration:underline;text-decoration-color:var(--gold)}}
.sh-go{{display:inline-block;background:var(--gold);color:#151a33;font-family:var(--sans);font-weight:600;
  text-decoration:none;padding:11px 18px;border-radius:6px}}
.sh-note{{font-family:var(--sans);font-size:13px;color:var(--muted);margin:26px 0 0}}
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
      <a href="/fiction/">Fiction</a>
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
      <span><a href="/">Carrier Press LLC</a>, Diamondhead, Mississippi.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

DESC = ("Posters, canvas, note cards and tees made from Carrier Press book covers and lines: "
        "The King in Yellow, The Willows, The Golem and more. Printed to order and shipped to you.")


def build():
    items = json.loads(pathlib.Path("shop_data.json").read_text())
    by = {g: [i for i in items if i["group"] == g] for g, _, _ in GROUPS}
    b = [HEAD.format(domain=DOMAIN, desc=e(DESC)),
         '<section class="wrap sh" style="padding-top:44px;padding-bottom:64px">',
         '<p class="sec-head" style="margin:0 0 10px"><span class="kicker">The shop</span></p>',
         '<h1>Put the books on your wall</h1>',
         '<p class="lede">The covers and lines you know from our books, as posters, canvas, note cards '
         'and tees. Every piece is printed when you order it. Tap one to see it up close and buy it.</p>',
         '<p><a class="sh-go" href="%s">Open the full shop</a></p>' % STORE,
         '<ul class="sh-jump">']
    b += ['<li><a href="#%s">%s</a></li>' % (g, e(name)) for g, name, _ in GROUPS if by[g]]
    b.append('</ul>')
    for g, name, line in GROUPS:
        if not by[g]:
            continue
        b += ['<section class="sh-g" id="%s" aria-labelledby="h-%s">' % (g, g),
              '<h2 id="h-%s">%s</h2>' % (g, e(name)), '<p>%s</p>' % e(line), '<ul class="sh-row">']
        for i in by[g]:
            price = ("from $" if "Sticker" in i["title"] and "Sheet" not in i["title"] else "$") + i["price"]
            b.append('<li><a href="%s"><img src="%s" alt="" loading="lazy" decoding="async" '
                     'width="300" height="300"><span>%s</span><b>%s</b></a></li>'
                     % (e(i["url"]), e(i["img"]), e(i["title"]), e(price)))
        b += ['</ul>', '</section>']
    b += ['<p class="sh-note">Checkout, printing and delivery are handled by our print partner, Printful, '
          'on carrierpress.printful.me. Shipping is to US addresses, and the cost shows at checkout.</p>',
          '<p class="sh-note">Cover art created with AI-assisted illustration tools and finished by Carrier Press.</p>',
          '</section>', FOOT.format(year=datetime.date.today().year)]
    s = "\n".join(b)
    for bad in ("—", "–", "&mdash;", "&ndash;"):
        assert bad not in s, "dash in shop page"
    out = pathlib.Path("shop")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(s, encoding="utf-8")
    nav.patch(out / "index.html")
    print("wrote shop/index.html  --  %d products in %d groups" % (len(items), sum(1 for v in by.values() if v)))


if __name__ == "__main__":
    build()
