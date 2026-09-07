#!/usr/bin/env python3
"""
Generate the per-app privacy policy pages.

    python3 make_privacy.py            # write any page that does not exist
    python3 make_privacy.py --force    # rewrite the generated ones too

Every App Store submission needs a privacy policy URL, so each app needs a
page here before it can be submitted. This script exists so those pages are
consistent and regenerable rather than thirty hand-edited copies that drift.

## What it will not touch

`flare/privacy/` and `planfinder/privacy/` are HAND-WRITTEN and predate this
script. They are the standard the copy below is trying to meet, not output to
be regenerated, so they are refused outright even under --force.

## Where the facts come from

Each app's `supabase/migrations/*.sql`, read directly rather than described
from memory. A privacy policy is a legal representation: "we store X" has to
be answerable to a column, and "we send it to Y" has to be answerable to an
edge function. Both were checked per app on 2026-09-06.

The two that call a model say so plainly and near the top. That is the fact a
reader is least likely to assume and most entitled to know, and burying it
under a "third parties" heading at the bottom would be a choice about
emphasis, not a summary.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORCE = "--force" in sys.argv

# Hand-written. Never regenerate these.
PROTECTED = {"flare", "planfinder"}

UPDATED = "6 September 2026"
# Per-app override, for a page written after the batch above. An entry sets
# `updated=` only when its copy was actually written on a different day; a
# "last updated" date that moves because a script ran is a false statement
# about a legal document, so this is not derived from today's date.

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} privacy policy | Carrier Press</title>
<meta name="description" content="{summary}">
<link rel="canonical" href="https://carrierpress.com/{slug}/privacy/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{name} privacy policy">
<meta property="og:description" content="{summary}">
<meta property="og:url" content="https://carrierpress.com/{slug}/privacy/">
<meta property="og:image" content="https://carrierpress.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
/* Scoped to this page, matching flare/privacy and planfinder/privacy.
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
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
  </div>
</header>
<main id="main">
<section><div class="wrap wrap-narrow">

<div class="sec-head">
  <p class="eyebrow">{name}</p>
  <h1>{name} privacy policy</h1>
</div>

<div class="policy">

<p class="updated">Last updated {updated}.</p>
{body}
<h2>Contact</h2>

<p><a href="mailto:support@carrierpress.com">support@carrierpress.com</a></p>

<p>{name} is published by Jeffrey L Carrier.</p>

</div>

</div></section>
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; 2026 Jeffrey L. Carrier. All rights reserved.</span>
      <span><a href="/">Carrier Press</a> is an imprint of Jeffrey L. Carrier.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

APPS = {}

# The bulk of the copy lives in privacy_content.py so this file stays small
# enough to review as a generator rather than as a document. Entries defined
# below (the first three written) win on a name clash, which never happens.
try:
    from privacy_content import APPS as _EXTRA
    APPS.update(_EXTRA)
except ImportError:
    pass

# ── Through the Gate ────────────────────────────────────────────────────────
# Schema: profiles(email, stripe_customer_id, subscription_status,
# current_period_end, parses_used), resumes(label, source_text),
# parses(record, dropped, flags), applications(company, role, applied_on,
# status, posting_url, notes). Edge function parse-resume calls Anthropic.
APPS["throughthegate"] = dict(
    name="Through the Gate",
    summary="What happens to the resume you paste in, including the fact that it is sent to a model to be read.",
    body="""
<p>Through the Gate shows you the structured record a resume parser builds from
your resume, and what it discarded on the way. This policy explains what is
kept, where it sits, who can reach it, and what leaves our servers.</p>

<h2>Your resume is sent to Anthropic to be read</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. The parsing is done by a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, not by code on
our own machines. When you ask for a parse, the full text you pasted is sent to
Anthropic's API and the result comes back to us.</p>

<p>A resume is not anonymous. Yours almost certainly contains your name, your
email address, your phone number, where you live, everywhere you have worked and
when. All of it goes, because a parser that only saw part of it could not tell
you what a real one would discard.</p>

<p>If you would rather that did not happen, the sample on our website runs on an
invented resume and needs no account, and you can read it without giving us
anything.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and a count of how many parses you have run.</li>
  <li><strong>Every resume you save</strong>: the label you gave it and the
  complete text you pasted, exactly as you pasted it.</li>
  <li><strong>Every parse</strong>: the record the model extracted, the list of
  things it dropped, and the flags it raised, with the date it was generated.</li>
  <li><strong>Any applications you track</strong>: company, role, the date you
  applied, a status, an optional link to the posting, and your own notes.</li>
  <li><strong>Whether your subscription is active</strong>, and when the current
  period ends.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No name, no date of birth, no address and no phone number are
asked for as fields, though anything in a resume you paste is kept as part of
that text. No payment card details ever reach us.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything, so another user cannot
reach your resumes or your applications even if they go looking. There is no
sharing feature, no recruiter view and no employer access. We do not sell any of
it, and we do not send it to advertisers.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives your resume text to parse it, as
  described above.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>Apple</strong> handles subscriptions bought in the app, and tells us
  only whether yours is active.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every resume, every parse and every
tracked application. It is immediate and it is not recoverable, so export
anything you want to keep first.</p>

<p>Cancelling a subscription is separate and is handled in your Apple subscription
settings, because Apple owns that relationship rather than us.</p>
""",
)

# ── Perimeter ───────────────────────────────────────────────────────────────
# Schema: profiles(email, cycle_pattern, subscription...), entries(entry_date,
# symptoms jsonb 0-10, sleep_hours, stress_level, notes), insights(findings,
# summary, window), scripts(opener, points, questions). Edge functions
# analyze + conversation-script call Anthropic.
APPS["perimeter"] = dict(
    name="Perimeter",
    summary="How Perimeter handles the perimenopause symptoms you record, including that they are sent to a model to be analysed.",
    body="""
<p>Perimeter tracks perimenopause symptoms, including the ones nobody connects,
and turns a stretch of them into something you can say at an appointment. This
policy explains what is kept, where it sits, and who can reach it.</p>

<h2>This is health information, and it is treated that way</h2>

<p>What you record in Perimeter is information about your body, at a point in
your life you may not have told anyone about. There is no useful way to soften
that, so the rest of this page is specific rather than reassuring.</p>

<h2>Your entries are sent to Anthropic to be analysed</h2>

<p>Perimeter does not find patterns with code on our own machines. When you ask
for an analysis or an appointment script, the symptom entries in that window are
sent to a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, and the result
comes back to us. That includes the severities you recorded, your sleep and
stress figures, and anything you wrote in a notes field.</p>

<p>Nothing is sent until you ask for one of those two things. Logging a day on
its own stays on our database and goes nowhere else.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and the cycle pattern you chose when you
  signed up.</li>
  <li><strong>One record per day you fill in</strong>: the severity you gave each
  symptom on a nought to ten scale, hours slept, a stress rating, and anything you
  wrote in the notes field.</li>
  <li><strong>The analyses Perimeter generates</strong>, with the stretch of dates
  each was drawn from.</li>
  <li><strong>The appointment scripts</strong>: the opener, the points and the
  questions written for you to take in.</li>
  <li><strong>Whether your subscription is active</strong>, and when the current
  period ends.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No name, no date of birth, no address, no phone number, and no
insurance or payment details. The app has nowhere to put them.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before it returns anything, so another user cannot
reach your days even if they go looking. There is no sharing feature, no
clinician view and no household account. We do not sell any of it, we do not
send it to advertisers, and no employer or insurer has any route to it.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives the entries in a window when you ask for
  an analysis or a script, as described above.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>Apple</strong> handles subscriptions bought in the app, and tells us
  only whether yours is active.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every day you logged, every
analysis and every script. It is immediate and it is not recoverable, so save
anything you want to take to an appointment before you delete.</p>

<p>Cancelling a subscription is separate and is handled in your Apple subscription
settings, because Apple owns that relationship rather than us.</p>
""",
)

# ── Quiet ───────────────────────────────────────────────────────────────────
# No supabase/ directory at all. lib/db.ts is expo-sqlite. BUILD_SPECS: no
# account, no sync, no network permission in the default build.
APPS["quiet"] = dict(
    name="Quiet",
    summary="Quiet keeps everything on your device. There is no account, no sync and no server to hold anything.",
    body="""
<p>Quiet is a personal record that never leaves the device it was written on.
This policy is short because there is very little to describe.</p>

<h2>Nothing is collected, because nothing is sent</h2>

<p>Quiet has no account, no sign in, no sync and no server. What you write is
stored in a database inside the app's own storage on your device, and it stays
there. We never receive it, so we cannot read it, hand it over, lose it or sell
it.</p>

<p>This is a property of how the app is built rather than a promise about how we
behave. The default build ships without network permission at all, so there is no
connection for your writing to travel over even in principle.</p>

<h2>What that means for you</h2>

<ul>
  <li><strong>There is no backup on our side.</strong> If you lose the device or
  delete the app, what was in it is gone, and we have no copy to restore.</li>
  <li><strong>Your device's own backup may include it.</strong> If you back up to
  iCloud or to a computer, the app's storage may be part of that backup, governed
  by Apple's terms rather than ours.</li>
  <li><strong>Deleting the app deletes the record.</strong> There is no account to
  close and nothing to request from us afterwards.</li>
</ul>

<h2>Who else is involved</h2>

<p>For the app itself, nobody. We use no analytics, no crash reporting, no
advertising identifier and no third party service inside Quiet.</p>

<p><strong>Apple</strong> handles the purchase, and tells us only that one was
made. That happens in the App Store rather than in the app, and it is not
connected to anything you write.</p>
""",
)


def main():
    written, skipped = [], []
    for slug, app in sorted(APPS.items()):
        if slug in PROTECTED:
            sys.exit(f"refusing to generate {slug}: that page is hand written")
        out_dir = os.path.join(HERE, slug, "privacy")
        out = os.path.join(out_dir, "index.html")
        if os.path.exists(out) and not FORCE:
            skipped.append(slug)
            continue
        os.makedirs(out_dir, exist_ok=True)
        html = SHELL.format(
            name=app["name"],
            slug=slug,
            summary=app["summary"],
            updated=app.get("updated", UPDATED),
            body=app["body"],
        )
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(f"{slug}/privacy/  ->  https://carrierpress.com/{slug}/privacy/")

    for w in written:
        print(f"wrote  {w}")
    for s in skipped:
        print(f"kept   {s}/privacy/ (exists; --force to rewrite)")
    print(f"\n{len(written)} written, {len(skipped)} kept")


if __name__ == "__main__":
    main()
