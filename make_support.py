#!/usr/bin/env python3
"""
Support pages for the apps, one per app, at /<slug>/.

WHY THIS EXISTS. App Store Connect requires a Support URL and the reviewer
opens it. On 2026-09-14 thirty-six of thirty-eight app repos had a privacy page
on this domain and no support page, so the URL a submission points at was a 404.
The pair looked half-present rather than absent, which is why it survived.

WHY THE CHROME IS NOT THE BOOK CHROME. These pages started life as copies of a
book page, so a landlord looking for help with Schedule E arrived at navigation
reading "Fiction, Classics, Journal, Free Sample". That is the whole of the
problem the author raised, and it is fixed here rather than by moving domains:
the URLs are already inside submitted App Store records, and the obvious move
target is unavailable (carrierventures.com and carrierapps.com both resolve to
Carrier Corporation's nameservers).

So an app page wears the APP as its brand and carries exactly two links, Support
and Privacy. The footer names Jeffrey L. Carrier, which is the App Store SELLER
NAME on every one of these apps, and links to the imprint rather than leading
with it. The stylesheet is shared and unmodified: styles.css is hand-edited and
belongs to the book side, and a utility page is not a reason to add rules to it.

BODIES ARE NOT GENERATED. Each app's prose lives in support_bodies/<slug>.html
and is written from that app's own repo. A support page assembled from a
template would be an empty website under guideline 2.1, which is worse than no
page at all because it looks like an answer.

THE DATE IS PINNED, NOT DERIVED FROM TODAY. This script used to pass
`datetime.date.today()` into the template, so every run re-dated all thirty-eight
pages whether or not a word of their copy had changed. Running the generator is
not a review, and App Review opens these pages. make_privacy.py had already
written the rule down and obeyed it; this file had not, and nothing noticed
because a changed date looks like noise in a diff.

The consequence worth keeping: `python3 make_support.py` is now reproducible.
A clean checkout regenerates byte for byte, so `git diff --exit-code` after a
build is a check that can be run in CI and mean something.

    python3 make_support.py            # all bodies present
    python3 make_support.py doorstop   # one
"""
import html, pathlib, sys, datetime, re

DOMAIN = "carrierpress.com"
BODIES = pathlib.Path("support_bodies")

UPDATED = "15 September 2026"
# The day the batch of thirty-eight bodies was written. NOT today's date: a
# "last updated" line that moves because a script ran is a false statement about
# when a page was last reviewed, and these are the URLs App Review opens. Same
# rule, and the same reasoning, as make_privacy.py.
#
# ⚠️ WHEN A BODY CHANGES, BUMP ITS DATE HERE IN THE SAME COMMIT. That is the
# cost of pinning: the date is now a claim somebody has to make on purpose
# rather than one the clock makes for them. An unbumped date after a real
# rewrite is the opposite error to the one this replaced, and just as wrong.
UPDATED_OVERRIDE = {
    # Renamed from Ledger for One on 2026-09-18, which rewrote the body.
    "soleledger": "18 September 2026",
}

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} support</title>
<meta name="description" content="{blurb}">
<link rel="canonical" href="https://{domain}/{slug}/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{name} support">
<meta property="og:description" content="{blurb}">
<meta property="og:url" content="https://{domain}/{slug}/">
<meta property="og:image" content="https://{domain}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
/* Scoped here. styles.css is hand edited, shared with the book side of the
   domain, and has no general prose rules; a utility page is not a reason to
   add global ones. */
.policy h2{{font-size:1.22rem;font-weight:600;letter-spacing:-.01em;margin:38px 0 12px}}
.policy h3{{font-size:1.02rem;font-weight:600;margin:24px 0 8px}}
.policy p{{margin:0 0 14px;line-height:1.62}}
.policy ul{{margin:0 0 14px;padding-left:1.1rem}}
.policy li{{margin:0 0 10px;line-height:1.62}}
.policy .updated{{color:var(--ink-soft);font-size:.95rem;margin-bottom:26px}}
.policy .lede{{font-size:1.06rem}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="/{slug}/">
      <img class="mark-dark" src="/assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="/assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>{name}</span>
    </a>
    <nav class="nav" aria-label="Main">
      <a class="nav-cta" href="/{slug}/">Support</a>{privacy_nav}
    </nav>
  </div>
</header>
<main id="main">
<section><div class="wrap wrap-narrow">

<div class="sec-head">
  <p class="eyebrow">{name}</p>
  <h1>{name} support</h1>
</div>

<div class="policy">

<p class="updated">Last updated {updated}.</p>

"""

TAIL = """
<h2>Contact</h2>

<p><a href="mailto:support@{domain}">support@{domain}</a></p>

<p>One person reads that, so a reply may take a few days.</p>

<p>{name} is published by Jeffrey L Carrier.</p>

</div>

</div></section>
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; {year} Jeffrey L. Carrier. All rights reserved.</span>
      <span>{privacy_foot}<a href="/">Carrier Press</a></span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def build(slug):
    src = BODIES / f"{slug}.html"
    if not src.exists():
        return None, f"no body at {src}"
    raw = src.read_text(encoding="utf-8")
    m = re.match(r"<!--\s*name:\s*(.+?)\s*\|\s*blurb:\s*(.+?)\s*-->\s*", raw, re.S)
    if not m:
        return None, f"{slug}: body must begin <!-- name: X | blurb: Y -->"
    name, blurb = m.group(1).strip(), m.group(2).strip()
    body = raw[m.end():].strip()
    if len(blurb) > 200:
        return None, f"{slug}: blurb is {len(blurb)} chars, keep it under 200"
    # Four apps have no privacy page on this domain yet. Linking one anyway
    # would put a 404 on a support page, which is the guideline 2.1 defect these
    # pages exist to close. The link appears only when the file does.
    has_privacy = (pathlib.Path(slug) / "privacy" / "index.html").exists()
    privacy_nav = f'\n      <a href="/{slug}/privacy/">Privacy</a>' if has_privacy else ""
    privacy_foot = f'<a href="/{slug}/privacy/">Privacy</a> &middot; ' if has_privacy else ""
    # ⚠️ Check EVERY site-relative link the body contains, not just this app's
    # own privacy page. The first version of this guard asked only "does
    # /<slug>/privacy/ exist", and a body that hardcoded ANOTHER app's path
    # sailed through it: Sole Ledger's body still pointed at /ledgerforone/
    # after the rename deleted that directory, which is a 404 on a live support
    # page, the exact defect these pages exist to close. A guard that only
    # covers the case you were thinking of is how the second one ships.
    for href in re.findall(r'href="(/[^"#?]*)"', body):
        target = href.strip("/")
        if not target:
            continue
        if not (pathlib.Path(target).exists() or pathlib.Path(target, "index.html").exists()):
            return None, f"{slug}: body links to {href}, which does not exist"
    page = (HEAD.format(name=html.escape(name), blurb=html.escape(blurb),
                        slug=slug, domain=DOMAIN, privacy_nav=privacy_nav,
                        updated=UPDATED_OVERRIDE.get(slug, UPDATED))
            + body + "\n"
            + TAIL.format(name=html.escape(name), slug=slug, domain=DOMAIN,
                          privacy_foot=privacy_foot,
                          year=datetime.date.today().year))
    out = pathlib.Path(slug) / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out, None


if __name__ == "__main__":
    slugs = sys.argv[1:] or sorted(p.stem for p in BODIES.glob("*.html"))
    ok, bad = 0, []
    for s in slugs:
        out, err = build(s)
        if err:
            bad.append(err)
        else:
            ok += 1
            print(f"  {out}")
    print(f"{ok} page(s) written")
    for b in bad:
        print(f"  SKIPPED  {b}")
    sys.exit(1 if bad and not ok else 0)
