#!/usr/bin/env python3
"""Build index.html for carrierpress.com from catalog.json.

Usage:  python3 build.py
No dependencies. Edit catalog.json to add or change titles, then re-run.
"""
import json, html, pathlib, datetime

D = json.load(open("catalog.json"))
S = D["site"]
AMZ = "https://www.amazon.com/dp/{}"

def e(x): return html.escape(str(x), quote=True)

# ---------------------------------------------------------------- copy blocks
BIO = [
 "Jeffrey L. Carrier writes fiction about the things families leave unsaid: inheritance, "
 "memory, and the quiet cost of a choice that looked simple from the outside.",

 "His novels run from literary suspense (<em>The Sponge Cache</em> and the Greek diaspora "
 "<em>Things Left Open</em> series) to small town cozy mystery (<em>The Marjorie Corey Files</em>) "
 "to the literary <em>Keystone Cycle</em>. Whatever the shelf, the pull is the same: a documented "
 "record, a family secret, and someone who decides to keep reading when it would be easier to stop.",

 "Before he wrote fiction he served in the U.S. Navy and the U.S. Air Force.",

 "He lives on the Mississippi Gulf Coast with his two sons.",
]

def book_card(b, kind):
    asin = b["a"]
    url  = AMZ.format(asin)
    bits = []
    bits.append('<article class="book">')
    bits.append(f'<a class="cover" href="{url}" target="_blank" rel="noopener">'
                f'<img src="assets/covers/{asin}.jpg" loading="lazy" decoding="async" '
                f'width="313" height="500" alt="Cover of {e(b["t"])}"></a>')
    bits.append('<div class="meta">')
    if b.get("omnibus"):
        bits.append('<span class="num">Complete series</span>')
    elif b.get("n"):
        bits.append(f'<span class="num">Book {b["n"]}</span>')
    bits.append(f'<h3><a href="{url}" target="_blank" rel="noopener">{e(b["t"])}</a></h3>')
    if b.get("by"):
        bits.append(f'<p class="by">{e(b["by"])}</p>')
    if b.get("hook"):
        bits.append(f'<p class="hook">{e(b["hook"])}</p>')
    if b.get("note"):
        bits.append(f'<p class="fmt">{e(b["note"])}</p>')
    bits.append('</div></article>')
    return "".join(bits)

ANCHORS = {"things-left-open": "fiction", "gadget-sandbox": "young", "classics": "classics"}

def section(sec):
    anchor = ANCHORS.get(sec["id"])
    idattr = f' id="{anchor}"' if anchor else ""
    out = [f'<section{idattr} aria-labelledby="h-{sec["id"]}">', '<div class="wrap">',
           '<div class="sec-head">',
           f'<p class="eyebrow">{e(sec["shelf"])}</p>',
           f'<h2 id="h-{sec["id"]}">{e(sec["name"])}</h2>',
           f'<p>{e(sec["blurb"])}</p>']
    if sec.get("series_asin"):
        out.append(f'<p class="series-link"><a href="{AMZ.format(sec["series_asin"])}" '
                   f'target="_blank" rel="noopener">The complete series on Amazon</a></p>')
    out += ['</div>',
           '<div class="shelf">']
    out += [book_card(b, sec["kind"]) for b in sec["books"]]
    out += ['</div>', '</div>', '</section>']
    return "\n".join(out)

sections_html = "\n".join(section(s) for s in D["sections"])
total = sum(len(s["books"]) for s in D["sections"])

ld = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Carrier Press",
  "url": f"https://{S['domain']}/",
  "logo": f"https://{S['domain']}/assets/logo-mark.png",
  "description": S["tagline"],
  "founder": {"@type": "Person", "name": S["author"], "sameAs": [S["amazon_author"], S["bookbub_profile"]]},
}

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carrier Press | Books by Jeffrey L. Carrier</title>
<meta name="description" content="Carrier Press publishes the fiction of Jeffrey L. Carrier, books for young readers, and a line of restored classics. {total} titles, available now.">
<link rel="canonical" href="https://{S['domain']}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="Carrier Press | Books by Jeffrey L. Carrier">
<meta property="og:description" content="Literary suspense, cozy mystery, books for young readers, and restored classics.">
<meta property="og:url" content="https://{S['domain']}/">
<meta property="og:image" content="https://{S['domain']}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="/">
      <img class="mark-dark" src="assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>Carrier Press</span>
    </a>
    <nav class="nav" aria-label="Main">
      <a href="#fiction">Fiction</a>
      <a href="#young">Young Readers</a>
      <a href="#classics">Classics</a>
      <a href="#about">About</a>
      <a class="nav-cta" href="#free">Free Sample</a>
    </nav>
  </div>
</header>

<main id="main">

<div class="hero">
  <div class="wrap hero-in">
    <div class="hero-mark"><img src="assets/logo-mark.png" alt="Carrier Press: a carrier pigeon holding an open book" width="96" height="68"></div>
    <div>
      <h1>The secrets families keep, and the people who decide to <em>read them</em>.</h1>
      <p>Carrier Press publishes the fiction of {e(S['author'])}, books for young readers,
         and a line of restored classics. {total} titles, all available now.</p>
      <div class="hero-actions">
        <a class="btn btn-gold" href="#free">Read five chapters free</a>
        <a class="btn btn-ghost" href="#fiction">Browse the catalogue</a>
      </div>
    </div>
  </div>
</div>

<!-- ============================ READER MAGNET ============================
     The button below points at the live MailerLite landing page, which is
     inbox verified and assigns signups to the group "TLO Readers".

     TO PUT THE FORM DIRECTLY ON THIS PAGE INSTEAD:
       1. MailerLite -> Forms -> Embedded forms -> create one, assign it to
          the group TLO Readers, double opt-in ON.
       2. Copy its HTML snippet.
       3. Replace the <a class="btn btn-gold"> below with that snippet.
     Nothing else changes. The welcome automation fires on group join, so it
     works identically from either capture point.
     ====================================================================== -->
<section id="free" class="magnet" aria-labelledby="h-free">
  <div class="wrap magnet-in">
    <div>
      <p class="eyebrow">Free sample</p>
      <h2 id="h-free">Read the first five chapters of <em>The Sponge Cache</em></h2>
      <p>A grandmother dies and leaves Marina a ledger that does not balance, and a stranger is
         already willing to pay far too much for it. Get the opening five chapters free, sent
         straight to your inbox as EPUB and PDF.</p>
      <p>A short welcome note from me, and only when there is news after that.</p>
      <p style="margin-top:22px">
        <a class="btn btn-ink" href="{e(S['magnet_url'])}" target="_blank" rel="noopener">Send me the free chapters</a>
      </p>
      <p class="fine">No spam. One click unsubscribe any time. The sample is yours to keep.</p>
    </div>
    <div class="magnet-cover"><img src="assets/covers/B0H6CWP5GN.jpg" width="313" height="500" alt="Cover of The Sponge Cache"></div>
  </div>
</section>

{sections_html}

<section id="about" aria-labelledby="h-about">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">The author</p><h2 id="h-about">{e(S['author'])}</h2></div>
    <div class="about-in">
      <img src="assets/portrait.jpg" width="210" height="207" alt="{e(S['author'])}" loading="lazy">
      <div>{"".join(f"<p>{p}</p>" for p in BIO)}
        <p style="margin-top:22px">
          <a class="btn btn-ink" href="{e(S['bookbub_profile'])}" target="_blank" rel="noopener">Follow on BookBub</a>
        </p>
      </div>
    </div>
  </div>
</section>

</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="brandline">
          <img src="assets/logo-mark-light.png" alt="" width="40" height="28">
          <strong>Carrier Press</strong>
        </div>
        <p class="note">Carrier Press is the independent publishing imprint of {e(S['author'])}.
           Literary suspense, cozy mystery, books for young readers, and restored classics.</p>
      </div>
      <div>
        <h4>Read</h4>
        <ul>
          <li><a href="#free">Free sample</a></li>
          <li><a href="{e(S['amazon_author'])}" target="_blank" rel="noopener">All books on Amazon</a></li>
          <li><a href="{e(S['bookbub_profile'])}" target="_blank" rel="noopener">Follow on BookBub</a></li>
        </ul>
      </div>
      <div>
        <h4>Elsewhere</h4>
        <ul>
          <li><a href="{e(S['bookbub_site'])}" target="_blank" rel="noopener">Author page on BookBub</a></li>
          <li><a href="https://www.tiktok.com/@carrierpress" target="_blank" rel="noopener">TikTok</a></li>
        </ul>
      </div>
    </div>
    <div class="colophon">
      <span>&copy; {datetime.date.today().year} {e(S['author'])}. All rights reserved.</span>
      <span>Carrier Press is an imprint of {e(S['author'])}.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

pathlib.Path("index.html").write_text(HTML, encoding="utf-8")
print(f"index.html written: {total} titles across {len(D['sections'])} sections, "
      f"{len(HTML):,} bytes")
