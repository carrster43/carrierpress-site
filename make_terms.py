#!/usr/bin/env python3
"""
Generate the per-app terms of use pages.

    python3 make_terms.py            # write any page that does not exist
    python3 make_terms.py --force    # rewrite the generated ones too

## WHY THESE PAGES EXIST

Apple guideline 3.1.2 wants a functional Terms of Use link in the listing of
any app that sells an auto-renewing subscription, and `carrierpress.com/<app>/terms`
404ed, so `carrier-ventures/scripts/appstore/listing.py` had been linking
Apple's standard EULA instead. That is the documented substitute and it is a
legitimate answer, but it is a generic one: it says nothing about what a given
app does, and an app whose whole pitch is "it stops at the confirm button" or
"it cannot output the answer" has limits worth writing down before somebody
relies on their absence. Twenty-five of the forty sell a subscription, so this
is most of the portfolio rather than an edge case.

Swap the EULA link in listing.py for `https://carrierpress.com/<slug>/terms/`
once these are live.

## WHERE THE FACTS COME FROM

The commercial facts are read from `apps_data.py` at generation time rather
than typed in here: the plan shape decides which paying clause a page gets,
and the price string is printed from the same field `/apps/` prints. That is
the whole reason apps_data.py exists, and a price typed twice is a price that
will disagree with itself. Each page also says the App Store's price at the
moment of purchase is the one that applies, because a static page cannot know
about a regional price or a change made this morning.

The per-app section lives in `terms_content.py`, for the same reason the bulk
of the privacy copy lives in `privacy_content.py`: so this file stays short
enough to review as a generator rather than as a document.

## WHAT IS IN THE SHARED CLAUSES

Apple requires that a custom EULA include at least the minimum terms it sets
out for licensed applications, and the clauses below carry them deliberately
rather than incidentally: the agreement is with the developer and not Apple
(WHO), scope of licence and the App Store Usage Rules (LICENCE), maintenance
and support as the developer's responsibility (SUPPORT), warranty and Apple's
sole obligation being a refund of the purchase price (WARRANTY), product and
intellectual property claims as the developer's responsibility (CLAIMS), the
user's legal and export representation (ELSEWHERE), and Apple and its
subsidiaries as third-party beneficiaries able to enforce the terms (APPLE).
Removing one of those is removing an Apple requirement, so do not edit them
without knowing which one you are holding.

## ⚠️ THIS IS DRAFTED COPY, NOT REVIEWED COPY

No lawyer has read a word of it. It describes each app honestly and it carries
Apple's required terms, which is enough to stop the listing leaning on a
generic EULA, and it is not the same thing as advice about whether these terms
are enforceable where you live. Two clauses that normally appear in a document
like this are deliberately absent, and their absence is a decision for the
publisher rather than a gap to fill in quietly:

  - No arbitration clause, class action waiver or jury trial waiver.
  - No choice of law beyond naming Mississippi, where the publisher is.

Both are about how a dispute is resolved rather than about what the software
does, both are the clauses most likely to be unenforceable if drafted badly,
and neither is required by Apple.

## THE DATE IS A LITERAL AND MUST STAY ONE

`UPDATED` is written out, never derived from `today()`. Two reasons, and the
second is the one that bites: a "last updated" date that moves because a
script ran is a false statement about a legal document, and the test workflow
regenerates everything and requires the tree to be unchanged, so a date from
today() would turn CI red at midnight. make_privacy.py holds the same rule for
the same two reasons. When the copy genuinely changes, change this by hand,
and set `updated=` on a single entry if only that page changed.
"""

import os
import sys

import apps_data

HERE = os.path.dirname(os.path.abspath(__file__))
FORCE = "--force" in sys.argv

from terms_content import APPS

UPDATED = "20 October 2026"

PUBLISHER = "Jeffrey L Carrier"
CONTACT = "support@carrierpress.com"

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} terms of use | Carrier Press</title>
<meta name="description" content="{summary}">
<link rel="canonical" href="https://carrierpress.com/{slug}/terms/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{name} terms of use">
<meta property="og:description" content="{summary}">
<meta property="og:url" content="https://carrierpress.com/{slug}/terms/">
<meta property="og:image" content="https://carrierpress.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
/* Scoped to this page, and identical to the block make_privacy.py writes.
   styles.css is hand edited and shared by the whole site, and it has no
   general prose rules because nothing else needed them. A utility page is not
   a reason to add global ones. */
.policy h2{{font-size:1.22rem;font-weight:600;letter-spacing:-.01em;margin:38px 0 12px}}
.policy p{{margin:0 0 14px;line-height:1.62}}
.policy ul{{margin:0 0 14px;padding-left:1.1rem}}
.policy li{{margin:0 0 10px;line-height:1.62}}
.policy .updated{{color:var(--ink-soft);font-size:.95rem;margin-bottom:26px}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="{home}">
      <img class="mark-dark" src="/assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="/assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>{name}</span>
    </a>
    <nav class="nav" aria-label="Main">{support_nav}
      <a href="/{slug}/privacy/">Privacy</a>
      <a class="nav-cta" href="/{slug}/terms/">Terms</a>
    </nav>
  </div>
</header>
<main id="main">
<section><div class="wrap wrap-narrow">

<div class="sec-head">
  <p class="eyebrow">{name}</p>
  <h1>{name} terms of use</h1>
</div>

<div class="policy">

<p class="updated">Last updated {updated}.</p>

<p>These terms are the agreement between you and {publisher}, who publishes
{name}, covering your use of the app. Using the app means you accept them. If
you do not, do not use it.</p>

<h2>What {name} is, and what it is not</h2>
{is_not}
<h2>What you may do with it</h2>

<p>You get a personal, non-exclusive, non-transferable licence to use one copy
of {name} on Apple-branded devices that you own or control, as the App Store
Terms of Service allow, including the Usage Rules in them. Family Sharing and
volume purchasing work the way Apple describes. The licence is not a sale: the
app, its design and its content stay ours, and you get permission to use it
rather than ownership of it.</p>

<h2>What you may not do with it</h2>

<ul>
<li>Copy it, sell it, rent it, lend it or redistribute it.</li>
<li>Take it apart: no reverse engineering, decompiling or disassembling, except
where the law gives you that right regardless of what this says.</li>
<li>Strip out or hide any notice of ownership in it.</li>
<li>Use it to break the law, to infringe anybody's rights, or to harass, harm
or impersonate another person.</li>
<li>Attack it: no attempt to breach it, overload it, scrape it wholesale, or
reach data belonging to anybody else.</li>
</ul>

<h2>Your account and your content</h2>

<p>What you put into {name} stays yours. We claim no ownership of it and we do
not sell it. We need the limited permission to store and process it that
operating the app requires, and nothing beyond that. The
<a href="/{slug}/privacy/">privacy policy</a> is the document that says what
is kept, where it sits and what leaves our servers, and it is part of this
agreement.</p>

<p>Keeping your sign-in details to yourself is your responsibility, and so is
what happens under your account. You are responsible for having the right to
enter anything you enter about another person.</p>

<h2>Age</h2>

<p>You need to be 18 or over to accept these terms. Where a child or a young
person uses the app, an adult accepts these terms on their behalf, is
responsible for that use, and is the person we are contracting with.</p>

{paying}
<h2>Support</h2>

<p>Support is ours to provide, not Apple's, and Apple has no obligation to
provide any maintenance or support for the app whatsoever. Write to
<a href="mailto:{contact}">{contact}</a>. There is no guaranteed response time
and no service level promised here.</p>

<h2>No warranty</h2>

<p>{name} is provided as it is, without warranty of any kind, express or
implied, including any implied warranty of merchantability, fitness for a
particular purpose, or non-infringement. We do not promise that it will be
uninterrupted, available, error free, or that any defect will be fixed, and we
do not promise that what it shows you is accurate or complete.</p>

<p>If the app fails to conform to any warranty that cannot be disclaimed, you
may tell Apple, and Apple will refund the purchase price. To the maximum
extent permitted by law, that refund is Apple's entire obligation, and Apple
has no other warranty obligation of any kind in relation to the app. Some
jurisdictions do not allow the exclusion of certain warranties, so parts of
this may not apply to you.</p>

<h2>Limits on what we owe you</h2>

<p>To the extent the law allows, we are not liable for indirect, incidental,
special or consequential loss, or for lost profits, lost data, or any cost of
substitute software, however it arises. Where liability cannot be excluded, it
is limited to the greater of the amount you paid for the app in the twelve
months before the claim, or twenty-five US dollars.</p>

<p>Nothing here limits liability for anything that cannot lawfully be limited,
including death or personal injury caused by negligence, or fraud. Some
jurisdictions do not allow these limits, so parts of this may not apply to
you.</p>

<h2>Claims about the app</h2>

<p>We, and not Apple, are responsible for addressing any claim from you or
anybody else about the app or your use of it. That includes product liability
claims, any claim that the app fails to meet a legal or regulatory
requirement, and claims arising under consumer protection or similar law. It
also includes any claim that the app infringes somebody else's intellectual
property: that one is ours to investigate, defend, settle and discharge.</p>

<h2>Ending it</h2>

<p>You can end this agreement at any time by deleting the app. We can end it
if you breach these terms. When it ends, your licence ends and you stop using
the app, and the clauses that are meant to outlive it, the warranty
disclaimer, the limits above and anything about content you had already
submitted, carry on.</p>

<h2>Changes</h2>

<p>The app changes, and a feature can be altered or withdrawn. These terms can
change too, and when they do the date at the top of this page changes with
them. Continuing to use the app after that means you accept the new version.
If a change matters to you and you do not accept it, stop using the app and
cancel any subscription.</p>

<h2>If you are outside the United States</h2>

<p>You are responsible for complying with the law where you are, which may
differ from ours. You confirm that you are not in a country subject to a US
Government embargo or designated by the US Government as supporting
terrorism, and that you are not on any US Government list of prohibited or
restricted parties. You also confirm you will comply with any third party
terms that apply when you use the app, such as your wireless carrier's.</p>

<h2>Apple</h2>

<p>Apple is not a party to this agreement and has no responsibility for
{name}. Apple and its subsidiaries are third party beneficiaries of these
terms, and Apple has the right to enforce them against you as a beneficiary
of them. Where you obtained the app somewhere other than Apple's App Store,
that distributor's equivalent terms apply in place of the Apple-specific parts
of this page.</p>

<h2>Everything else</h2>

<p>These terms, with the <a href="/{slug}/privacy/">privacy policy</a>, are
the whole agreement about {name}. If a court finds part of it unenforceable,
the rest still stands. Not enforcing something straight away does not waive
it. These terms are governed by the laws of the State of Mississippi, without
regard to its conflict of laws rules, and nothing here takes away a right you
have under the law where you live that cannot be waived by agreement.</p>

<h2>Contact</h2>

<p><a href="mailto:{contact}">{contact}</a></p>

<p>{name} is published by {publisher}.</p>

</div>

</div></section>
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; 2026 Jeffrey L. Carrier. All rights reserved.</span>
      <span>{support_foot}<a href="/{slug}/privacy/">Privacy</a> &middot; <a href="/">Carrier Press</a></span>
    </div>
  </div>
</footer>
</body>
</html>
"""

# ── The paying clause, one per plan shape ──────────────────────────────────
# `shape` in apps_data.py already divides the portfolio exactly the way this
# clause has to divide: an auto-renewing subscription needs the renewal and
# cancellation terms Apple asks for, a one-time unlock needs to say plainly
# that it will not come back for more, and a b2b app is not sold to the person
# using it at all. `{price}` is that row's own price string.

PAYING_SUB = """<h2>Paying for it</h2>

<p>{name} is sold as an auto-renewing subscription through the App Store, at
{price}. The free tier is described on the <a href="/{slug}/">app's own
page</a>, and the price shown in the App Store when you buy is the one that
applies: prices differ by region and can change, and the App Store is the
authority rather than this page.</p>

<p>Where a free trial is offered it is three days, and the App Store shows you
whether one applies before you confirm. After any trial, the subscription
renews automatically at the end of each period, and Apple charges your Apple
Account within 24 hours of the end of the current period unless you cancel at
least 24 hours before it ends. A trial you do not cancel in time becomes a
paid subscription and is charged.</p>

<p>Cancel in Settings on your device, under your Apple Account, then
Subscriptions. We cannot cancel it for you and we cannot see or change your
billing. Cancelling stops the next renewal; the period you have already paid
for runs to its end. Any unused part of a free trial is forfeited if you buy a
subscription during it.</p>

<p>Apple takes the payment and Apple handles refunds, under its own policy, at
<a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>. We
cannot issue a refund for an App Store purchase. If we raise the price, Apple
asks you to agree before it takes effect, and the subscription does not renew
at the higher price until you do.</p>
"""

PAYING_ONCE = """<h2>Paying for it</h2>

<p>{name} is sold as a one-time purchase through the App Store, at {price}. It
is one payment and not a subscription: it does not renew, and nothing here
bills you again. The free tier is described on the <a href="/{slug}/">app's own
page</a>, and the price shown in the App Store when you buy is the one that
applies, since prices differ by region and can change.</p>

<p>What the purchase unlocks is what is described on that page at the time you
buy. Features can change as the app develops, and we may add things later that
are sold separately, but we will not put something you already paid for back
behind a new charge.</p>

<p>Apple takes the payment and Apple handles refunds, under its own policy, at
<a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>. We
cannot issue a refund for an App Store purchase. An unlock is tied to your
Apple Account, so Apple's Restore Purchases will return it on a new device at
no further cost.</p>
"""

PAYING_B2B = """<h2>Paying for it</h2>

<p>{name} is licensed to an organisation rather than sold to the person using
it, at {price}. If you are using it because a clinic, an agency, a board, a
facility, an employer or an association gave you access, you are not being
charged and there is nothing for you to cancel. Access lasts as long as that
organisation's licence does, and it can end when their licence does.</p>

<p>Where a written agreement exists between us and that organisation, it
governs the commercial terms, and this page governs your own use of the
software. If the two conflict on a commercial question, that agreement
wins.</p>

<p>The organisation decides who gets access and what it does with the records
its people create, within the limits of our agreement with it and of the
<a href="/{slug}/privacy/">privacy policy</a>. Questions about your access,
your data or your account should go to them first, since we often cannot
answer them on their behalf.</p>
"""

PAYING = {"sub": PAYING_SUB, "once": PAYING_ONCE, "b2b": PAYING_B2B}

# ⚠️ FIVE APPS OVERRIDE THE CLAUSE ABOVE, AND THEY ARE NOT STYLE PREFERENCES.
# `shape` sorts the portfolio into three buckets for the purpose of printing a
# price on /apps/, and for that it is right. Used to pick a payment clause it
# puts a false statement on five pages, which is a different kind of mistake on
# a terms page than it would be on a shelf listing:
#
#   thebinder   "once", priced "$99 once, then $29/yr". The one-time clause
#               says it does not renew and nothing bills you again. It does.
#   crosscheck  "once", priced "$24.99 per case". Not a single unlock: you pay
#               per appeal, so "nothing here bills you again" is wrong too.
#   threshold   "once", priced "$28.99 per child". Same, per child.
#   porchlight  "once", priced "Free to trick-or-treat". It is free, so a
#               purchase clause describes a transaction that never happens.
#   cast        "sub", priced "Books from $6.99 · Your own books $22.99/mo".
#               Two different purchases, one of which is not a subscription.
#
# An entry in terms_content.py sets `paying=` to replace the clause outright.
# Anything with a plain monthly, yearly or single price keeps the shared one,
# including the per-seat subscriptions (per unit, each, per household, per
# host), which are ordinary auto-renewing subscriptions sold by the seat.


def rows():
    """Every app that is sellable and has pages: a slug, and a privacy page
    beside it. `bench` drops out here rather than by name, because it has a
    slug and no pages at all, and `shape` of "none" has no paying clause."""
    out = []
    for app in apps_data.APPS:
        slug = app.get("slug")
        if not slug:
            continue
        if not os.path.exists(os.path.join(HERE, slug, "privacy", "index.html")):
            continue
        out.append(app)
    return sorted(out, key=lambda a: a["slug"])


def main():
    data = rows()

    # Neither list is allowed to drift silently. terms_content.py checks that
    # each of its slugs has a privacy page; this checks the other direction,
    # that every sellable app has copy written for it, and refuses rather than
    # quietly writing 39 of 40 pages.
    missing = [a["slug"] for a in data if a["slug"] not in APPS]
    if missing:
        sys.exit("no terms_content.py entry for: " + ", ".join(missing))

    unknown = [a["slug"] for a in data if a["shape"] not in PAYING]
    if unknown:
        sys.exit("no paying clause for plan shape of: " + ", ".join(unknown))

    written, skipped = [], []
    for app in data:
        slug = app["slug"]
        copy = APPS[slug]
        out_dir = os.path.join(HERE, slug, "terms")
        out = os.path.join(out_dir, "index.html")
        if os.path.exists(out) and not FORCE:
            skipped.append(slug)
            continue
        os.makedirs(out_dir, exist_ok=True)
        # The app's own chrome, not the book chrome, and the support link only
        # where the page exists. Same rule as make_privacy.py: a dead link on a
        # page App Review opens is the defect these pages exist to close.
        has_support = os.path.exists(os.path.join(HERE, slug, "index.html"))
        paying = (copy.get("paying") or PAYING[app["shape"]]).format(
            name=copy["name"], slug=slug, price=app.get("price") or "the price shown in the App Store"
        )
        html = SHELL.format(
            name=copy["name"],
            slug=slug,
            summary=copy["summary"],
            updated=copy.get("updated", UPDATED),
            is_not=copy["is_not"],
            paying=paying,
            publisher=PUBLISHER,
            contact=CONTACT,
            home=f"/{slug}/" if has_support else "/",
            support_nav=f'\n      <a href="/{slug}/">Support</a>' if has_support else "",
            support_foot=f'<a href="/{slug}/">Support</a> &middot; ' if has_support else "",
        )
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(f"{slug}/terms/  ->  https://carrierpress.com/{slug}/terms/")

    for w in written:
        print(f"wrote  {w}")
    for s in skipped:
        print(f"kept   {s}/terms/ (exists; --force to rewrite)")
    shapes = {}
    for a in data:
        shapes[a["shape"]] = shapes.get(a["shape"], 0) + 1
    print(f"\n{len(written)} written, {len(skipped)} kept, {len(data)} apps "
          f"({', '.join(f'{n} {s}' for s, n in sorted(shapes.items()))})")


if __name__ == "__main__":
    main()
