"""
Per-app privacy policy copy, consumed by make_privacy.py.

Kept apart from the generator so the generator stays small and this stays
reviewable as prose. Nothing here is boilerplate with a name swapped in.

## How every entry was written

Read out of the app's own `supabase/migrations/*.sql` and
`supabase/functions/` on 2026-09-06, not described from memory. A privacy
policy is a legal representation: "we store X" must be answerable to a
column, "we send it to Y" must be answerable to a function.

Two detection mistakes were made and corrected while writing these, and
both are worth remembering. Searching for `api.anthropic.com` MISSED every
app that calls the model through `@anthropic-ai/sdk`, which is most of
them. Searching for the SDK alone then missed Errand, which calls the API
directly. Only the union of both is right, and a policy built on either
half would have told users their data stayed on our servers when it did
not.

## The two rules that shaped the copy

1. **A model call is disclosed in its own section near the top.** It is the
   fact a reader is least likely to assume and most entitled to know.
   Burying it in a list of third parties at the bottom is a decision about
   emphasis, not a summary.

2. **Where an app holds data about someone who never installed it — a
   tenant, a co-parent, an elderly parent, a client, a neighbour, a child —
   that gets its own section too.** Those people cannot read a policy they
   were never shown, so the section is addressed to the user about their
   responsibility, not to the absent person about their rights.

## Deliberately absent

Homeroom and Signal Check are shelved, Signal Check on COPPA grounds.
Publishing a polished privacy policy for an app shelved over children's
privacy would read as clearing a gate that is not cleared. They get pages
when they get an attorney, not before.
"""

APPS = {}

# ── Cancelled ───────────────────────────────────────────────────────────────
# tables: profiles, tracked. No model call. No third-party personal data.
# ── The three boating apps ───────────────────────────────────────────────────
# Written 2026-09-14 from each repo. All three share one stack and it is the
# shortest in the fleet: async-storage and expo-iap, no supabase directory, no
# analytics, no crash reporter, no network code. The purchase is `type:
# "in-app"`, a ONE-TIME unlock and NOT a subscription, and `isUnlocked()` reads
# local storage and never touches the network.
#
# Stored keys, read from lib/storage.ts and lib/purchases.ts rather than assumed:
#   boatready     "vessels", "checked:<id>", "unlocked"
#   channelmarks  "unlocked"
#   nightwatch    "unlocked"
APPS["boatready"] = dict(
    name="Boat Ready",
    updated="14 September 2026",
    summary="What Boat Ready keeps about your boats and your equipment checks, which stays on your phone.",
    body="""
<p>Boat Ready answers what safety equipment federal rules require a
recreational boat to carry, and lets you keep that answer per boat. It works
with no signal, which is the point, since the question tends to arrive at a
ramp.</p>

<h2>There is no account and no server</h2>

<p><strong>You do not sign in, because there is nothing to sign in to.</strong>
This app has no database of ours, no cloud sync and no backend. Everything it
knows is written to your phone's own storage and stays there.</p>

<h2>What is stored, on your device</h2>

<ul>
  <li><strong>The boats you save</strong>: the name you gave each one, its
  length, its hull and engine details, and the other answers the requirements
  depend on.</li>
  <li><strong>Which items you have ticked off</strong> for each boat.</li>
  <li><strong>Whether the app is unlocked</strong>, so it does not have to ask
  the App Store every time it opens.</li>
</ul>

<p>That is the whole list. No name, no email address, no phone number, no
location, no registration or hull number is asked for or kept, and a boat's name
is whatever you decide to type.</p>

<p><strong>Nothing above is ever uploaded</strong>, because there is nowhere to
upload it to.</p>
<h2>Who else is involved</h2>

<p><strong>Apple, and nobody else.</strong> The unlock is a one-time purchase
made through the App Store, so Apple handles the payment and tells the app only
that the purchase exists. Apple never receives anything you entered.</p>

<p>There is no analytics, no crash reporting, no advertising and no tracking
software of any kind. There is no language model. There is no server of ours for
anything to be sent to.</p>

<h2>The one moment anything leaves</h2>

<p>The app has a link to the US Coast Guard's own site, because the official
source should always be one tap away. <strong>Tapping it opens your browser</strong>,
and what happens then is between you and the Coast Guard under their policy. The
app sends nothing with you and is not told that you went.</p>

<h2>Deleting it</h2>

<p>There is no account to close. <strong>Deleting the app removes your boats and
your checklists with it</strong>, and there is no copy anywhere else, so if a
boat's details took a while to enter, write them down before you delete. Your
purchase is held by Apple rather than by us, so reinstalling and tapping Restore
brings the unlock back without paying again.</p>
""",
)

APPS["channelmarks"] = dict(
    name="Channel Marks",
    updated="14 September 2026",
    summary="What Channel Marks keeps about you, which is one flag saying you bought it.",
    body="""
<p>Channel Marks tells you what a US buoy or beacon means and which side to
pass it on. It is built to work with no signal at all, because the moment you
need it is not the moment to discover you have none.</p>

<h2>There is no account, and almost nothing to keep</h2>

<p><strong>You do not sign in and nothing about you is collected.</strong> There
is no database of ours, no cloud sync and no backend.</p>

<h2>What is stored, on your device</h2>

<p><strong>One thing: whether the app is unlocked</strong>, so it does not have
to ask the App Store every time it opens.</p>

<p>That is genuinely the entire list. The app does not record which marks you
looked up, how long you spent, where you were, or anything else. There is no
name, no email address, no location and no history, and the app requests no
device permissions.</p>
<h2>Who else is involved</h2>

<p><strong>Apple, and nobody else.</strong> The unlock is a one-time purchase
made through the App Store, so Apple handles the payment and tells the app only
that the purchase exists. Apple never receives anything you entered.</p>

<p>There is no analytics, no crash reporting, no advertising and no tracking
software of any kind. There is no language model. There is no server of ours for
anything to be sent to.</p>

<h2>The one moment anything leaves</h2>

<p>The app has a link to the US Coast Guard's own site, because the official
source should always be one tap away. <strong>Tapping it opens your browser</strong>,
and what happens then is between you and the Coast Guard under their policy. The
app sends nothing with you and is not told that you went.</p>

<h2>Deleting it</h2>

<p>There is no account to close and nothing of yours to erase. Deleting the app
removes it and the one stored flag. Your purchase is held by Apple rather than
by us, so reinstalling and tapping Restore brings the unlock back without paying
again.</p>
""",
)

APPS["nightwatch"] = dict(
    name="Night Watch",
    updated="14 September 2026",
    summary="What Night Watch keeps about you, which is one flag saying you bought it.",
    body="""
<p>Night Watch helps you work out what a vessel is from the lights or day
shapes you can see, with the Navigation Rules behind each answer. It works with
no signal, which matters on the water at night.</p>

<h2>There is no account, and almost nothing to keep</h2>

<p><strong>You do not sign in and nothing about you is collected.</strong> There
is no database of ours, no cloud sync and no backend.</p>

<h2>What is stored, on your device</h2>

<p><strong>One thing: whether the app is unlocked</strong>, so it does not have
to ask the App Store every time it opens.</p>

<p>That is genuinely the entire list. Nothing records what you identified, when,
or where. <strong>The app asks for no location permission</strong>, which is
worth saying plainly for an app used on a boat: it does not know where you are
and is not built to.</p>
<h2>Who else is involved</h2>

<p><strong>Apple, and nobody else.</strong> The unlock is a one-time purchase
made through the App Store, so Apple handles the payment and tells the app only
that the purchase exists. Apple never receives anything you entered.</p>

<p>There is no analytics, no crash reporting, no advertising and no tracking
software of any kind. There is no language model. There is no server of ours for
anything to be sent to.</p>

<h2>The one moment anything leaves</h2>

<p>The app has a link to the US Coast Guard's own site, because the official
source should always be one tap away. <strong>Tapping it opens your browser</strong>,
and what happens then is between you and the Coast Guard under their policy. The
app sends nothing with you and is not told that you went.</p>

<h2>Deleting it</h2>

<p>There is no account to close and nothing of yours to erase. Deleting the app
removes it and the one stored flag. Your purchase is held by Apple rather than
by us, so reinstalling and tapping Restore brings the unlock back without paying
again.</p>
""",
)

APPS["cancelled"] = dict(
    updated="24 September 2026",
    name="Canceled",
    summary="What Canceled keeps about the recurring charges you track, which stays on your phone.",
    body="""
<p>Canceled finds the subscriptions you are still paying for and helps you end
the ones you do not want. This policy explains what is kept and what is not.</p>

<h2>Your bank is not connected, and that is the design</h2>

<p>Canceled does not link to your bank and never asks for banking credentials.
It reads a CSV statement that you download from your bank yourself and choose to
open in the app, and that file is parsed <strong>on your device</strong>. The
recurring charges it finds are found by that parsing, not typed in by you.
Nothing from the file is uploaded. That makes it less automatic than the
alternatives and it is the reason the app can promise what the rest of this page
promises.</p>

<h2>There is no account and no server</h2>

<p><strong>You do not sign in, because there is nothing to sign in to.</strong>
This app has no database of ours, no cloud sync and no backend. Everything it
knows is written to your phone's own storage and stays there.</p>

<p>Earlier versions of this app did have an account, reached by a code sent to
your email address, and a hosted database behind it. Both were removed on 21
September 2026 along with the email address they needed. There is no longer
anywhere for us to keep anything about you.</p>

<h2>What is stored, on your device</h2>

<ul>
  <li><strong>Each charge you choose to track</strong>: the merchant as your
  statement names it, the name shown for it, how much it is, how often it bills,
  when it was last seen, whatever status you have given it, and any note you
  added.</li>
  <li><strong>Whether the app is unlocked</strong>, so it does not have to ask
  the App Store every time it opens.</li>
</ul>

<p>That is the whole list. It is two entries in your phone's own storage.
Charges found in a statement are not saved at all unless you tap to keep one.</p>

<h2>What is not stored</h2>

<p>No email address, no name, no password and no account, because there is no
account. No bank login, no account number and no card number, because the app
never asks for any of them. <strong>No statement data</strong>: the file you
open is read and the charges are worked out from it, and neither the file nor
the transactions in it are written anywhere or sent anywhere.</p>

<p><strong>Nothing above is ever uploaded</strong>, because there is nowhere to
upload it to.</p>

<h2>Who else is involved</h2>

<p><strong>Apple, and nobody else.</strong> The unlock is a one-time purchase
made through the App Store, so Apple handles the payment and tells the app only
that the purchase exists. Apple never receives anything you entered, including
the charges you track.</p>

<p>Canceled is a one-time purchase and not a subscription, which is deliberate:
an app about ending recurring charges should not add one.</p>

<p>There is no analytics, no crash reporting, no advertising and no tracking
software of any kind. There is no language model. There is no server of ours for
anything to be sent to.</p>

<h2>The one moment anything leaves</h2>

<p>When the app shows you where to cancel a subscription, that is a link to the
merchant's own page. <strong>Tapping it opens your browser</strong>, and what
happens then is between you and that company under their policy. The app sends
nothing with you and is not told that you went. The same is true of the link to
this page and of the support email address.</p>

<h2>Deleting it</h2>

<p>Everything is on your phone, so you control all of it. The account screen has
a button that erases every charge you were tracking, immediately and
unrecoverably. Deleting the app removes the same data along with it. Neither
needs to ask us, because we do not have a copy.</p>

<p>Your unlock is held by Apple against your Apple ID rather than by us, so it
survives both and can be restored from the account screen.</p>
""",
)

# ── Crosscheck ──────────────────────────────────────────────────────────────
# tables: profiles, cases, letters. No model call. Health + financial.
# ── Conception Zodiac ────────────────────────────────────────────────────────
# ⚠️ WRITTEN 2026-09-14 AGAINST A REPO WITH NO APP LAYER. ConceptionZodiac is
# `lib/` and `test/` only: no app/ directory, no app.config.js, no screens, and
# ZERO dependencies in package.json. Its README says it outright, "Pure
# calculation. No backend, no accounts, no database, no network, no
# dependencies."
#
# That makes every statement below structurally true today, because there is
# nothing in the repo that could collect anything. It also means this page
# describes a library rather than a shipped app.
#
# ✅ THE SCREENS WERE BUILT THE SAME DAY (`ae1d65d`) AND THIS PAGE WAS RE-DERIVED.
# The app now has a one-time unlock and saves people locally, so two sentences
# that were true at first publish became false within the hour: "no in-app
# purchase" and "keeps no record of it". Both corrected. That is exactly the
# drift the warning below predicted, and it took about sixty minutes.
#
# 🔴 RE-DERIVE THIS PAGE AGAIN IF THE APP GAINS ANYTHING THAT LEAVES THE DEVICE. The moment somebody adds
# storage, analytics or a network call, the sentences below become the exact
# kind of false claim the 14 September audit spent a day removing from nine
# other pages.
APPS["conceptionzodiac"] = dict(
    name="Conception Zodiac",
    updated="14 September 2026",
    summary="What Conception Zodiac does with the birth date and pregnancy length you type, and where the people you save are kept.",
    body="""
<p>Conception Zodiac works out the zodiac sign at conception rather than at
birth, from a birth date and, if you know it, how many weeks the pregnancy
lasted.</p>

<h2>Nothing you type leaves your device</h2>

<p><strong>There is no account, no sign in, no database and no server of
ours.</strong> The app does the arithmetic on your device, and anything it keeps
is kept there. Nothing is uploaded, because there is nowhere for it to go.</p>

<h2>What is stored, on your device</h2>

<ul>
  <li><strong>The people you choose to save</strong>, if you unlock that: the
  name you typed for each one, their birth date, and the pregnancy length if you
  entered it. Saving is entirely optional and the app is fully usable without
  it.</li>
  <li><strong>Whether the app is unlocked</strong>, so it does not have to ask
  the App Store every time it opens.</li>
</ul>

<p>The date the app works out is <strong>never stored</strong>, only recomputed
from what you typed. That is deliberate, and the reason is in the section below
about what this app will not tell you.</p>

<p>This is not a policy choice that could quietly change in a later release
without you noticing the difference: the app is built as a calculation with no
network code and no third-party libraries in it at all. <strong>If that ever
changes, this page changes with it, and the date at the top will tell you
so.</strong></p>

<h2>Why the gestational age matters, and why it stays with you</h2>

<p>A birth date on its own is ordinary. <strong>How many weeks a pregnancy
lasted is health information</strong>, about the birth and about the person who
gave birth, and a birth at thirty-four weeks says something a stranger has no
business holding. It is asked for because it is the only thing that makes the
answer specific rather than a fixed shift from the birth sign.</p>

<p>So it is worth being exact about what happens to it: <strong>it is used for
one calculation and it is not stored, not sent anywhere, and not attached to
you.</strong> Close the app and it is gone.</p>

<h2>What this app will not tell you</h2>

<p>It names a sign. <strong>It does not state a conception date as a
fact.</strong> Naming the zodiac sign of a conception season is a toy. Asserting
the date on which two named people conceived a child is a claim about their
private lives and, if anyone relied on it, a medical claim as well. The app is
built so that it cannot make one.</p>

<p>For the same reason, where the pregnancy length is unknown the answer is
genuinely uncertain, and the app shows that uncertainty rather than hiding it
behind a single confident word. It is entertainment, not obstetrics, and not a
way to establish when anything happened.</p>

<h2>Children</h2>

<p>The birth being described is often a child's. Nothing about that child, or
anyone else, is collected, stored or transmitted by this app, because nothing at
all is.</p>

<h2>Who else is involved</h2>

<p><strong>Apple, and nobody else.</strong> Saving people is a one-time
purchase made through the App Store, so Apple handles the payment and tells the
app only that the purchase exists. <strong>Apple never receives a birth date, a
pregnancy length, a name you typed, or anything else from this app.</strong></p>

<p>There is no analytics, no advertising, no tracking software and no language
model. There is no server of ours for anything to be sent to.</p>

<h2>Deleting it</h2>

<p>There is no account to close. <strong>Removing the app from your device
removes any people you saved with it</strong>, and there is no copy anywhere
else, because everything was only ever on your phone. Your purchase is held by
Apple rather than by us, so reinstalling and tapping Restore brings the unlock
back without paying again.</p>
""",
)

APPS["crosscheck"] = dict(
    updated="14 September 2026",
    name="Crosscheck",
    summary="How Crosscheck handles the medical bills and insurance statements you photograph, which are health information.",
    body="""
<p>Crosscheck compares a medical bill against the statement your insurer sent for
the same care, and writes out the questions the difference raises. This policy
explains what is kept, where it sits, and who can reach it.</p>

<h2>This is health information, and it is treated that way</h2>

<p>A bill and an explanation of benefits describe what was done to your body, by
whom, and when. There is no useful way to soften that, so the rest of this page
is specific rather than reassuring.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and a subscription status field that is unused in this version.</li>
  <li><strong>Each case</strong>: the figures you entered from the bill and from
  the insurer's statement, and the differences between them that Crosscheck
  worked out.</li>
  <li><strong>Each letter</strong> it composed for you, kept so you can find it
  again.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No insurance member number, no policy number, no card details and
no clinical notes are asked for as fields.</p>

<h2>Nothing is sent to a model, and nothing is sent to your insurer</h2>

<p>Crosscheck does the comparison with ordinary arithmetic on our own servers. No
part of your case is sent to a language model or to any other company for
processing.</p>

<p>It also never contacts anybody on your behalf. It writes a letter and hands it
to you. Whether it is sent, to whom, and what happens next is entirely yours, and
we have no visibility into any of it.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before it returns anything. There is no sharing
feature, no advocate view and no employer or insurer access. We do not sell any
of it and we do not send it to advertisers.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
This app has no in-app purchase in this version, so nothing about a payment
or a subscription reaches Apple or anyone else.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every case and every letter,
immediately and unrecoverably. Save any letter you still need before you delete.</p>
""",
)

# ── Doorstop ────────────────────────────────────────────────────────────────
# tables: profiles units leases transactions documents records. _shared model
# call (extract-document). Holds TENANT data.
APPS["doorstop"] = dict(
    updated="8 September 2026",
    name="Doorstop",
    summary="What Doorstop keeps about your rental units, and about the tenants whose details you enter.",
    body="""
<p>Doorstop is a ledger for a landlord with a handful of units, ending in a clean
Schedule E. This policy explains what is kept, where it sits, and who can reach
it.</p>

<h2>Documents you photograph are sent to Anthropic to be read</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. When you photograph a lease, an invoice or a receipt, the image is
sent to a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, which reads it
and returns the figures. The whole document goes, including anything on it you
were not thinking about, such as a tenant's name or a signature.</p>

<p>Nothing is sent unless you photograph something. Figures you type in yourself
stay on our database.</p>

<h2>You are entering other people's information</h2>

<p>A lease is about a tenant. When you record one you are storing another
person's name, their tenancy dates and what they pay, and they did not install
this app or read this page.</p>

<p>That information is yours to hold as their landlord, and we treat it as your
record rather than theirs: we will not contact them, we do not build any profile
of them, and they have no account here. Whatever obligations you have to your
tenants about their data are yours, and this app does not discharge them.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>Your units</strong>, and the leases against them, including tenant
  details you choose to enter and the rent and dates.</li>
  <li><strong>Every transaction</strong> you record: amount, date, category and
  your own notes.</li>
  <li><strong>Documents you photograph</strong>, and the structured figures
  extracted from them.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No bank connection, no card details, and no credit or background
check data on anybody.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no tenant view,
no co-owner account and no sharing feature. We do not sell any of it and we do not
send it to advertisers.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives documents you photograph, as above.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every unit, lease, transaction and
document, immediately and unrecoverably. Export anything you need for a tax year
before you delete, because we cannot recover it afterwards.</p>
""",
)

# ── Errand ──────────────────────────────────────────────────────────────────
# tables: profiles errands allowed_recipients. plan-errand calls the API
# directly (not the SDK). Assistive, stops at confirm.
APPS["errand"] = dict(
    updated="14 September 2026",
    name="Errand",
    summary="What Errand keeps about the tasks you hand it, and the hard limit on what it is allowed to do with them.",
    body="""
<p>Errand researches a task, drafts what is needed and fills the form in, then
stops at the confirm button. This policy explains what is kept and what the app
is not permitted to do.</p>

<h2>Your task is sent to Anthropic to be planned</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. When you give Errand a task, what you wrote is sent to a large
language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, which works out
the steps and drafts the text. Whatever you put in the task description goes with
it, so treat that field as something that leaves our servers.</p>

<h2>It stops before anything irreversible</h2>

<p>Errand is assistive, not autonomous, and that is enforced rather than
promised. It will prepare a message, a form or a request and put it in front of
you, and you press the button. It does not send, submit, pay or agree on your
behalf.</p>

<p>It also cannot reach arbitrary people. Recipients have to be on a list you
control, which is why <em>allowed recipients</em> is a table in the database
rather than a setting in the interface.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and a subscription status field that is unused in this version.</li>
  <li><strong>Each errand</strong>: what you asked for, the plan produced, the
  drafts prepared, and how far it got.</li>
  <li><strong>The recipients you have allowed</strong>, so the app knows who it
  may prepare something for.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No card details, no bank connection, and no credentials for any
other service. Errand does not hold logins for the places it drafts things for.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. We do not sell any of it
and we do not send it to advertisers.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives your task text, as above.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li>This app has no in-app purchase in this version, so nothing about a
  payment or a subscription reaches Apple or anyone else.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every errand and your recipient
list, immediately and unrecoverably.</p>
""",
)

# ── FirstDay ────────────────────────────────────────────────────────────────
# tables: profiles children documents records deadlines supplies reminder_sends
# _shared model call. CHILD data. Forwarded school email.
APPS["firstday"] = dict(
    updated="11 September 2026",
    name="FirstDay",
    summary="What FirstDay keeps from the school emails you forward, including that they are about your child and are read by a model.",
    body="""
<p>FirstDay turns the school's emails and PDFs into one calendar, one supply list
and one form tracker. This policy explains what is kept, where it sits, and who
can reach it.</p>

<h2>What you forward is sent to Anthropic to be read</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. When you forward an email or upload a PDF, its full contents are sent
to a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, which reads it
and returns the dates, the supplies and the forms. The whole document goes,
including anything the school put in it that you were not thinking about.</p>

<h2>This is information about a child</h2>

<p>School correspondence names your child, their class, their teacher and often
their school. You are entering it, and it is held as your record as their
parent.</p>

<p>We ask for as little about them as the app can work with: a name to tell one
child's list from another's, and a year or class where a document mentions it.
There is no date of birth field, no photograph, no address and no school login.
Your child has no account here, we will never contact them, and nothing about
them is used for anything but building your own lists.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>Each child you set up</strong>, by the name you gave.</li>
  <li><strong>Documents you forward or upload</strong>, and the structured records
  read out of them.</li>
  <li><strong>Deadlines, supply items and form statuses</strong>, with the dates
  they are due.</li>
  <li><strong>A record of reminders sent</strong>, so the same one is not sent twice.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No school portal credentials, no child's date of birth, no
photographs, no grades and no payment details.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no school view,
no teacher access and no sharing between parents. We do not sell any of it, we do
not send it to advertisers, and nothing about a child is used for advertising in
any form.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives the documents you forward, as above.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>Resend</strong> delivers reminder emails, and receives your email
  address and the contents of that reminder.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every child you set up, every
document and everything read out of them, immediately and unrecoverably.</p>
""",
)

# ── Fluent Hour ─────────────────────────────────────────────────────────────
# tables: profiles sessions turns. converse calls the model. Spoken practice.
APPS["fluenthour"] = dict(
    updated="11 September 2026",
    name="Fluent Hour",
    summary="What Fluent Hour keeps from your spoken practice sessions, and what happens to what you say.",
    body="""
<p>Fluent Hour gives you one spoken scenario a day, about ten minutes, with no
lessons and no streaks. This policy explains what is kept, where it sits, and who
can reach it.</p>

<h2>Your side of the conversation is sent to Anthropic</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. The other side of the conversation is a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>. What you say is
transcribed to text and that text is sent so a reply can come back. There is no
way to have the conversation without this, because it is the conversation.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, the language you are learning, and
  whether your subscription is active.</li>
  <li><strong>Each session</strong>: the scenario, when it happened and how long
  it ran.</li>
  <li><strong>Each turn in it</strong>, as text: what you said and what came back.</li>
</ul>

<h2>Audio is not kept</h2>

<p>Speech is turned into text so the conversation can happen, and the recording is
not retained afterwards. What remains is the transcript. There is no voiceprint,
no speaker model and no audio file of you on our servers, and nothing about your
voice is used to train anything.</p>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No name, no age, no location and no payment details.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no teacher view,
no class and no leaderboard. We do not sell any of it and we do not send it to
advertisers.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives your transcribed turns, as above.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile and every session and turn,
immediately and unrecoverably.</p>
""",
)

# ── GED Completion ──────────────────────────────────────────────────────────
# tables: profiles orgs org_members org_invites diagnostic_items
# diagnostic_answers subject_status availability study_sessions. No model call.
# A CASEWORKER can see the learner's progress. That is the whole point and the
# whole risk, so it is stated plainly.
APPS["gedcompletion"] = dict(
    updated="14 September 2026",
    name="GED Completion",
    summary="What GED Completion keeps about your studying, and exactly what your caseworker can see.",
    body="""
<p>GED Completion is a completion engine rather than a question bank: it works out
where you are, what is left, and when you can realistically sit each test. This
policy explains what is kept and, most importantly, who else can see it.</p>

<h2>If you joined through a programme, your caseworker can see your progress</h2>

<p>This is the part that matters most, so it is here rather than at the bottom.
GED Completion is often paid for by a workforce programme, a corrections
department or an employer. If you joined using an invite from one of those, staff
at that organisation can see your diagnostic results, which subjects you have
finished, and whether you have been studying.</p>

<p>They can see your progress. They cannot see your individual answers as you work
through a session, and there is no message from us to them about anything you do.
If you would rather nobody saw any of it, do not join through an organisation
invite; an individual account is not visible to anyone but you.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and which organisation you belong to if
  you joined through one.</li>
  <li><strong>Your diagnostic answers</strong>, and what they indicate about each
  subject.</li>
  <li><strong>Your status per subject</strong>, and what the plan says is left.</li>
  <li><strong>The availability you entered</strong>, and the study sessions built
  from it.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No date of birth, no address, no case number, no offence history
and no benefits or immigration information. None of that is asked for, and the
app has nowhere to put it.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
This app has no in-app purchase in this version, so nothing about a payment or a subscription reaches Apple or anyone else. Nothing you write is
sent to a language model or to any other company.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, your answers, your status and your
sessions, immediately and unrecoverably. If you belong to an organisation, deleting
your account also ends their visibility of your progress.</p>
""",
)

# ── Handoff ─────────────────────────────────────────────────────────────────
# tables: profiles arrangements parties invites children custody_days messages
# expenses. No model call. Court-admissible export; the OTHER PARENT sees it.
APPS["handoff"] = dict(
    updated="11 September 2026",
    name="Handoff",
    summary="What Handoff keeps for a shared custody arrangement, what the other parent can see, and what a court export contains.",
    body="""
<p>Handoff holds a co-parenting calendar, the expenses between two households, and
a message log that can be exported for a court. This policy explains what is kept
and, above all, who else can see it.</p>

<h2>The other parent sees the shared record. Assume everything is on the record.</h2>

<p>This is the part that matters most, so it is here rather than at the bottom.
When you join an arrangement, the other party sees the custody days, the expenses
and every message in the log. That is the point of the app.</p>

<p>Messages cannot be edited or deleted once sent, by you or by them. That is
deliberate, because a log that either side could quietly revise would be worthless
in the situation it exists for. <strong>Write every message as though it will be
read aloud in a courtroom, because it may be.</strong></p>

<h2>What a court export contains</h2>

<p>An export is the complete message log and expense record for the arrangement,
with timestamps, in the order things happened. It is not filtered, and it is not
your side only. Either party can produce one. We are not a party to your matter,
we do not send anything to any court, and we take no position on how an export is
used.</p>

<h2>This is information about children</h2>

<p>An arrangement names the children it concerns and records where they are on
which days. We ask for as little as the app can work with: a name and, where a
schedule needs it, a date of birth. There is no photograph, no school record and
no location tracking of any kind. Children have no account here, we never contact
them, and nothing about them is used for advertising in any form.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>The arrangement</strong>, the parties in it and the invites sent.</li>
  <li><strong>The children</strong> it concerns, and the custody days recorded.</li>
  <li><strong>Every message</strong> in the log, with the time it was sent.</li>
  <li><strong>Every expense</strong>: what it was for, the amount, and how it splits.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No location, no phone number, no court file, no order document and
no payment card details.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
<strong>RevenueCat</strong> sits between the app and the app store and tracks
whether your subscription is active, receiving the purchase events and an
identifier for your account. <strong>Apple</strong> handles the payment itself;
card details go to Apple and never to us. Nothing in your arrangement is sent to a
language model, and none of it reaches any of the three. We do not sell any of it and we do not send it to advertisers.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your own profile. <strong>It does not erase the
shared arrangement</strong>, because the other party's copy of a joint record is
not yours to delete, and a message log that vanished when one side left would
defeat its purpose. Your messages remain in the log they were sent to.</p>
""",
)

# ── House Ledger ────────────────────────────────────────────────────────────
# tables: profiles homes systems service_events tasks documents records
# reminder_sends. _shared model call.
APPS["houseledger"] = dict(
    updated="8 September 2026",
    name="House Ledger",
    summary="What House Ledger keeps about your home and its service history, and what happens to documents you photograph.",
    body="""
<p>House Ledger is the service record for a house: what is in it, how old, under
what warranty, and who last touched it. This policy explains what is kept.</p>

<h2>Documents you photograph are sent to Anthropic to be read</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. When you photograph a warranty, an invoice or a manual, the image is
sent to a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, which reads it and
returns the dates and figures. The whole document goes, including a contractor's
details or your own address if they appear on it.</p>

<p>Nothing is sent unless you photograph something.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>Your home</strong>, and the systems in it with their ages and
  warranty dates.</li>
  <li><strong>Every service event</strong>: what was done, when, by whom, and what
  it cost.</li>
  <li><strong>Documents you photograph</strong> and the structured records read
  from them.</li>
  <li><strong>Tasks and a record of reminders sent</strong>, so the same one is not
  sent twice.</li>
</ul>

<h2>A note on contractors</h2>

<p>If you record who serviced something, you are storing a business contact in
your own record. We do not contact them, do not build any profile of them, and do
not sell or share contractor details with anyone.</p>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No property valuation, no mortgage or insurance policy details, and
no payment card details.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no agent view and
no sharing feature. We do not sell any of it and we do not send it to advertisers.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives documents you photograph, as above.</li>
  <li><strong>Supabase</strong> hosts the database and sends sign in codes.</li>
  <li><strong>Resend</strong> delivers reminder emails, and receives your email
  address and the contents of that reminder.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, the home, every system, service
event and document, immediately and unrecoverably. The record is meant to hand
over cleanly when you sell, so export it before you delete rather than after.</p>
""",
)

# ── Books for One (slug: soleledger) ────────────────────────────────────────
# tables: profiles sources transactions estimated_payments forms_1099 documents
# records reminder_sends. _shared model call. Financial. CPA gate lifted by
# REMOVING the derivation, so the app states no tax conclusion.
APPS["soleledger"] = dict(
    name="Books for One",
    # Copy genuinely changed on this date: Resend and RevenueCat added as
    # processors, and the "no EIN" claim corrected against the schema.
    updated="15 September 2026",
    summary="What Books for One keeps about your freelance income and deductions, and what it deliberately does not work out for you.",
    body="""
<p>Books for One is a freelancer's books: income, deductions, quarterly payments
and 1099 reconciliation, and nothing else. This policy explains what is kept.</p>

<h2>Documents you photograph are sent to Anthropic to be read</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. When you photograph a receipt, an invoice or a 1099, the image is sent
to a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, which reads it and
returns the figures. The whole document goes, including a client's name or a payer
identification number if it is printed on the form.</p>

<p>Nothing is sent unless you photograph something. Figures you type stay on our
database.</p>

<h2>It does not tell you what to pay</h2>

<p>Worth stating because the app used to be built the other way. Books for One
records what you earned and spent and tracks what you have paid. It does not work
out a safe harbour figure or tell you what a quarterly payment should be. You
enter your own target, and it counts against it.</p>

<p>That is a deliberate limit rather than a missing feature. A rule applied without
knowing your filing status can be confidently and expensively wrong, and nothing
here is tax advice. For that, ask somebody licensed to give it.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>Your income sources</strong>, and every transaction with its amount,
  date, category and your notes.</li>
  <li><strong>The estimated payments you record</strong> as having been made.</li>
  <li><strong>1099 forms</strong> you enter or photograph, and how they reconcile.</li>
  <li><strong>Documents you photograph</strong> and what was read out of them.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No bank connection and no card details. The app never asks for
either and has nowhere to put them.</p>

<p><strong>Your own Social Security number is never asked for.</strong> A 1099
does carry the payer's identification number, which is your client's rather than
yours, and that number is stored when it is printed on a form you photograph or
when you type it in. For a company that is an EIN. For a client who is a sole
trader it may be their Social Security number, so it is treated as sensitive and
is visible only to you.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. Nothing is filed with any
tax authority, and nothing is sent to anyone on your behalf. We do not sell any of
it and we do not send it to advertisers.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives documents you photograph, as above.</li>
  <li><strong>Supabase</strong> hosts the database and sends sign in codes.</li>
  <li><strong>Resend</strong> delivers reminder emails, and receives your email
  address and the contents of that reminder.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile and every source, transaction,
payment, form and document, immediately and unrecoverably. You may be required to
keep records for several years, so export a year before you delete it.</p>
""",
)

# ── Pantry ──────────────────────────────────────────────────────────────────
# tables: profiles items suggestions documents records. _shared + suggest-dinner.
APPS["pantry"] = dict(
    updated="11 September 2026",
    name="Pantry",
    summary="What Pantry keeps about the food in your kitchen, and what is sent away to suggest a meal.",
    body="""
<p>Pantry starts from what you already have and what expires first, rather than
from a menu. This policy explains what is kept.</p>

<h2>Your item list is sent to Anthropic to suggest a meal</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. When you ask for a suggestion, the items you have on hand are sent to
a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, which proposes
what to cook. If you photograph a receipt, that image is sent to be read as well.</p>

<p>Nothing is sent unless you ask for a suggestion or photograph something.
Adding an item by hand stays on our database.</p>

<h2>What a food list can reveal</h2>

<p>Worth saying plainly: what somebody eats can imply a religion, a health
condition or a household size. We do not analyse your list for any of that, do not
segment or profile you on it, and never sell or share it. It exists to answer one
question, which is what to cook tonight.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>Every item you have</strong>, with quantity and any expiry date.</li>
  <li><strong>The suggestions made</strong>, so you are not offered the same thing
  repeatedly.</li>
  <li><strong>Receipts you photograph</strong> and the items read out of them.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No grocery store account, no loyalty card, no purchase history from
any retailer, and no payment details.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives your item list when you ask for a
  suggestion, and any receipt you photograph.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every item, suggestion and receipt,
immediately and unrecoverably.</p>
""",
)

# ── Paper Trail ─────────────────────────────────────────────────────────────
# tables: profiles documents records alerts reminder_sends. _shared model call.
APPS["papertrail"] = dict(
    updated="8 September 2026",
    name="Paper Trail",
    summary="What Paper Trail keeps from the receipts, warranties and policies you photograph, and where those images go.",
    body="""
<p>Paper Trail turns the pile of paperwork into facts with dates, and warns you
before something lapses. This policy explains what is kept.</p>

<h2>Everything you photograph is sent to Anthropic to be read</h2>

<p>This is the part you are least likely to assume, so it is here rather than at
the bottom. The whole point of the app is reading documents, and that reading is
done by a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>. Every image you
add is sent in full.</p>

<p>Because the app takes whatever paperwork you have, that can be a wider range of
information than you intended in the moment: an insurance policy carries a policy
number, a receipt can carry the last four digits of a card, a warranty carries your
address. <strong>Photograph the document you want tracked, and cover anything on it
you would rather not send.</strong></p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>Every document image</strong> you add, kept so you can find the
  original again.</li>
  <li><strong>The structured record</strong> read out of each one: what it is, what
  it covers, and the dates that matter.</li>
  <li><strong>Alerts</strong> for expiry, and a record of reminders sent so the same
  one is not sent twice.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. Nothing is asked for as a field beyond what you choose to
photograph, and no payment card details ever reach us.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no household or
shared view. We do not sell any of it, we do not send it to advertisers, and we do
not analyse your documents for anything except the dates you asked us to track.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives every document you photograph.</li>
  <li><strong>Supabase</strong> hosts the database and sends sign in codes.</li>
  <li><strong>Resend</strong> delivers reminder emails, and receives your email
  address and the contents of that reminder.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every document image, every record
and every alert, immediately and unrecoverably. If a document is the only copy you
have, save it elsewhere before you delete.</p>
""",
)

# ── Permit Path ─────────────────────────────────────────────────────────────
# tables: profiles jurisdictions permit_types requirements applications
# application_steps. No model call.
APPS["permitpath"] = dict(
    updated="14 September 2026",
    name="Permit Path",
    summary="What Permit Path keeps about your permit applications, and why it never contacts a department for you.",
    body="""
<p>Permit Path tracks a building permit across the departments that have to touch
it, and builds a timeline from what actually happened. This policy explains what is
kept.</p>

<h2>It never files anything and never contacts a department</h2>

<p>Permit Path is a record of your own application, kept by you. It does not submit
forms, does not email a plans examiner and has no connection to any municipal
system. Nothing you enter is sent to a jurisdiction, and no jurisdiction can see
your account.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address.</strong></li>
  <li><strong>Each application</strong>: the property it concerns, the permit type,
  the jurisdiction, and the reference number if you have one.</li>
  <li><strong>Each step</strong>: which department, what was required, what you
  submitted and what came back, with dates.</li>
</ul>

<h2>A note on the property address</h2>

<p>A permit is about a place. If you enter the address of a job, you are storing a
location, and where it is somebody else's property you are storing a fact about
them. We do not look it up, do not enrich it against any other source, and do not
sell or share it.</p>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No licence number, no contractor bond details, no drawings unless
you choose to note them, and no payment details.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
Nothing is sent to a language model or to any other company. <strong>This app has
no in-app purchase</strong>, so there is no payment or subscription information
about you for anyone to hold.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile and every application and step,
immediately and unrecoverably. A permit timeline can matter long after the work is
done, so export one you may need before you delete it.</p>
""",
)

# ── PillProof ───────────────────────────────────────────────────────────────
# tables: profiles households memberships recipients device_links pairing_codes
# medications schedules doses pairing_attempts. No model call.
# The person tracked is USUALLY NOT the payer. Health data about a third party.
APPS["pillproof"] = dict(
    updated="14 September 2026",
    name="PillProof",
    summary="What PillProof keeps about the person taking the medication, who is usually not the person paying for the app.",
    body="""
<p>PillProof records that a dose was taken, and is usually paid for by an adult
child on behalf of a parent. This policy explains what is kept and who can see it.</p>

<p><strong>In this version a dose is confirmed in the app, not by photographing the
pill.</strong> Each confirmation records the time and which account confirmed it, so
a carer confirming on someone's behalf is recorded as the carer rather than as the
person taking the medication. One reference photograph per medication is stored, so
the person taking it can see what the pill should look like.</p>

<h2>The person tracked is usually not the person who signed up</h2>

<p>This is the part that matters most, so it is here rather than at the bottom. If
you set PillProof up for a parent, you are creating a record of another adult's
medication and daily behaviour, and they are the subject of it.</p>

<p>They are an adult and it is their health information. <strong>Set this up with
them, not for them.</strong> A person old enough to take their own medication is old
enough to be told that the times they took it are being sent to somebody else, and
the app is designed to be visible on their device rather than hidden on it.</p>

<p>If the person cannot meaningfully agree to that, the decision you are making is a
legal one about capacity and authority, and it is not one this app can make or
verify for you.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether the subscription is active.</li>
  <li><strong>The household</strong>, its members, and who is the recipient.</li>
  <li><strong>The medications and schedules</strong>: names, doses and times.</li>
  <li><strong>Each dose</strong>: whether it was confirmed, and when.</li>
  <li><strong>The device pairing</strong> between the two phones, and attempts to
  pair.</li>
</ul>

<h2>Photographs of pills</h2>

<p>Confirmation works by photographing the pill. Those images are of medication
rather than of a person, and they are checked and kept against the dose record.
They are not sent to a language model, are not used to identify anybody, and no
face recognition of any kind exists in this app.</p>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to an email
address. <strong>No location and no movement tracking of any kind</strong>, which is
deliberate: this app tells you a dose was taken, not where somebody is. No
diagnosis, no clinical notes, no insurance details and no payment card details.</p>

<h2>Who can see it</h2>

<p>Members of the household you set up, and nobody else using the app. Every table
checks the signed in account against the household before returning anything. There
is no clinician view, no pharmacy access and no sharing outside the household. We do
not sell any of it and we do not send it to advertisers.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
<strong>RevenueCat</strong> sits between the app and the app store and tracks
whether your subscription is active, receiving the purchase events and an
identifier for your account. <strong>Apple</strong> handles the payment itself;
card details go to Apple and never to us.</p>

<h2>Deleting it</h2>

<p>Deleting the account removes the household, its members, the medications,
schedules and every dose record, immediately and unrecoverably. The recipient can
unpair their device at any time, which stops any further record being made.</p>
""",
)

# ── Porchlight ─────────────────────────────────────────────
# tables: profiles porches listings reports. Functions: delete-account only.
# No model call. PUBLISHES COORDINATES OF A HOME, which no other app here does,
# so that leads. Read from 0001_init.sql 2026-09-07: porches holds lat/lng plus
# created_lat/created_lng, a landmark, five booleans and a required ends_at.
# There is NO address column anywhere in the schema. purge_expired_porches()
# DELETES rather than hides, so retention is a fact and not a promise.
APPS["porchlight"] = dict(
    name="Porchlight",
    updated="11 September 2026",
    summary="Porchlight puts the location of your front door on a public map, on purpose, for one night. Here is exactly what that means and what it does not.",
    body="""
<p>Porchlight is the opt-in map of which doors are giving out candy on Halloween,
and what they are offering. This policy explains what is published, what is kept,
and what is deliberately impossible here.</p>

<h2>Adding your porch publishes where you live</h2>

<p>This is the most important sentence on the page, so it is the first one.
When you add your porch, the location of your door appears on a map that every
other person using the app in your area can see, along with whatever you said you
are offering and the hours you gave. That is the entire product and it is not a
side effect.</p>

<p>It is the same signal a lit porch has sent to every stranger on the street for
a century, with more detail and a stop time attached. But a lightbulb is not
searchable and this is, so you should decide to publish deliberately rather than
discover it afterwards.</p>

<p><strong>Doing nothing publishes nothing.</strong> If you do not add your porch,
there is no row for your house and no way for anyone else to create one. A
household that wants to be left alone is not shown as declining or unavailable
&mdash; it simply is not on the map, indistinguishable from a house nobody asked.</p>

<h2>There is no way to mark a house as one to avoid</h2>

<p>No part of this app lets anyone say anything about a house other than their
own. There is no column that could hold it, no reporting reason that creates it
and no screen that would show it. This is refused rather than postponed: an
unverifiable public accusation attached to a private address is defamation with a
map reference, and it would be unmoderatable on the single night it was used.</p>

<h2>Your address is never stored, because it is never asked for</h2>

<p>There is no address field in this app and no address column in its database.
What is stored is a coordinate you placed yourself, plus a free-text landmark if
you chose to write one &mdash; the sort of thing neighbours already say to each
other, like &ldquo;the blue one with the big oak.&rdquo; You decide how specific
that is, and you can leave it empty.</p>

<h2>Your device location, and the one thing it is for</h2>

<p>When you add or move your porch, the app records where your device was standing
at that moment and refuses the pin if it is not within about sixty metres. That
check is the only reason location permission is requested, and it exists to stop
somebody pinning a neighbour's door &mdash; which is this product's worst possible
failure, because it points children at a house whose household never agreed to
open it.</p>

<p>Location is requested <strong>while you are using the app only</strong>. There
is no background location, no tracking, and no history of anywhere you went. The
coordinate is used at the moment you create the pin and to draw the map around
you, and nothing keeps a trail.</p>

<h2>The map does not exist in November</h2>

<p>Every porch requires a stop time; there is no way to publish one without an
end. Pins are <strong>deleted</strong> two days after their window closes, and
community listings thirty days after theirs. Deleted, not hidden: a hidden row is
still a record that a particular household expected children at a particular place
on a particular night, kept indefinitely for a purpose nobody agreed to.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong> and a display name, if you set one.</li>
  <li><strong>Your porch</strong> &mdash; its coordinate, your landmark text, which
  of the five offerings you ticked, an optional short note, and your hours. One
  household has one porch; adding it again edits the one you have.</li>
  <li><strong>Where your device stood</strong> when you created or moved that pin.</li>
  <li><strong>Community listings</strong>, for organisers who bought one.</li>
  <li><strong>Reports</strong>, so moderation works.</li>
</ul>

<h2>What is not stored</h2>

<p>No street address. No password, because there is not one &mdash; signing in is a
code sent to your email. No phone number. No payment details of any kind: the app
is free for households, permanently, and the only thing sold is a community listing
bought by an organiser through a web page rather than inside the app.</p>

<p>Nothing here is sent to a language model, and there is no advertising SDK, no
targeting, no auction and no impression tracking anywhere in this app. A paid
listing is content the organiser wrote, shown to everyone in range, ordered by
start time like everything else.</p>

<h2>Reporting</h2>

<p>Anyone can report a porch or a listing, and the first report hides it
immediately, before anybody has judged whether the report was right. That trade is
deliberate: a wrongly hidden porch means a household hands out less candy, and a
wrongly visible one means strangers at somebody's door.</p>

<p>Reports are private to the person who filed them. Nobody can read anybody
else's, so a report is never itself a public accusation.</p>

<h2>Blocking</h2>

<p>You can block whoever added a porch or a listing, which stops their pins
appearing for you. It is a different thing from reporting and it is worth being
exact about the difference. A report takes a pin off the map for everybody. A
block takes it off <em>your</em> map and nobody else's.</p>

<p>We store one row when you block somebody: your account, their account, and
the time. Only you can read it. The person you blocked is never told, the number
of times anyone has been blocked is never counted or shown, and nothing at all
about their pin changes for other families. You can undo a block at any time
from the account screen, and closing either account deletes the row.</p>

<p>This is not a way to mark a house as one to avoid. There is no such feature
here and there will not be one. Blocking publishes nothing about anybody; it
only subtracts somebody from your own view.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes. That
is the whole list. We do not sell anything to anyone.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile and your porch immediately, and the
pin disappears from everyone's map. If you only want off the map, delete your porch
and keep the account &mdash; you do not have to close it to stop being listed.</p>
""",
)

# ── Potluck ─────────────────────────────────────────────────────────────────
# tables: profiles neighbourhoods invites memberships happenings rsvps items
# loans reports blocks. No model call. ADDRESS VERIFIED + neighbours see you.
APPS["potluck"] = dict(
    updated="14 September 2026",
    name="Potluck",
    summary="What Potluck keeps about you and your address, and exactly what your neighbours can see.",
    body="""
<p>Potluck is neighbourhood-scale organising and lending, geofenced to a few
blocks. This policy explains what is kept and who sees it.</p>

<h2>Your neighbours see your name and what you offer</h2>

<p>This is the part that matters most, so it is here rather than at the bottom.
Everyone in your neighbourhood sees the display name you chose, anything you offer
to lend, and anything you organise or say you are coming to. That is the app
working as intended.</p>

<p>They do <strong>not</strong> see your email address, and they do not see your
street address. Where you live is used to decide which neighbourhood you belong to
and is not shown to other members.</p>

<h2>Why an address is needed at all</h2>

<p>Membership is address verified, because a neighbourhood tool that anyone could
join from anywhere is not a neighbourhood tool. <strong>We never receive your
address and never store it.</strong> The address lives on the invite, issued by the
neighbourhood association or municipal office that already holds it: they posted
the code to that address, and claiming the code is what proves you receive post
there. Your membership records the date it was verified and nothing else. There is
no address column in this app's database, which is deliberate, because a list of
names, faces and street addresses for a few blocks is exactly the database this
app's users should be most afraid of.</p>

<p>You can choose the display name your neighbours see. If you would rather they
did not see your full legal name, use something else.</p>

<h2>Reporting and blocking</h2>

<p>Moderation shipped with the first version rather than being added later. If you
report someone, what you wrote is visible to whoever reviews it, not to the person
reported. If you block someone, they are not told.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address, display name and address</strong>, and the
  neighbourhood you belong to.</li>
  <li><strong>Things you organise</strong>, who has said they are coming, and what
  people are bringing.</li>
  <li><strong>Items you offer to lend</strong>, and the loans made.</li>
  <li><strong>Reports and blocks</strong>, so moderation works.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No phone number, no location tracking of any kind, and no payment
details. Potluck is free to neighbours.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
Nothing is sent to a language model or to any other company, and we do not sell
anything to anyone.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, your address and your membership,
immediately. Things you organised that other people came to remain in the
neighbourhood's record, without your name attached, because they were shared
events rather than only yours.</p>
""",
)

# ── Relay ───────────────────────────────────────────────────────────────────
# tables: profiles circles members invites updates medications appointments
# providers. No model call. Health data about a CARE RECIPIENT, shared to a circle.
APPS["relay"] = dict(
    updated="14 September 2026",
    name="Relay",
    summary="What Relay keeps about the person being cared for, and which members of the circle can see it.",
    body="""
<p>Relay replaces the seven sibling group chat with one typed feed about the person
everybody is caring for. This policy explains what is kept and who sees it.</p>

<h2>Most of what is stored is about someone else</h2>

<p>This is the part that matters most, so it is here rather than at the bottom. The
medications, appointments and updates in Relay describe the health of the person
being cared for, and that person is usually not the one who set the circle up.</p>

<p>If they can be asked, ask them. A care circle formed around somebody without
their knowledge is a decision about their autonomy, and it is not one this app can
make or verify for you. If they cannot be asked, the authority you are relying on is
a legal one that exists outside this app.</p>

<h2>Who in the circle sees what</h2>

<p>There are no private notes and no way to hide an update from one particular
sibling. Family members all see the same feed, which is deliberate: the app exists
so that the same facts reach everybody, and a feed with entries hidden from chosen
people would recreate the problem it was built to solve.</p>

<p><strong>There is one exception, and it is the only one.</strong> A helper, meaning
a paid carer or a neighbour rather than family, sees the medical, mood and
day-to-day updates and <strong>never sees financial updates at all</strong>. That is
enforced by the database rather than by hiding a tab, so it holds regardless of
which screen anyone opens. The role travels on the invite code, so it is set by
whoever invites, not chosen by whoever joins.</p>

<p><strong>Write updates on the assumption that every family member will read
them.</strong></p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether the subscription is active.</li>
  <li><strong>The circle</strong>, its members and the invites sent.</li>
  <li><strong>Every update</strong> posted, with who wrote it and when.</li>
  <li><strong>Medications, appointments and providers</strong> recorded for the
  person being cared for.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your
email address. No location tracking, no clinical records from any provider, no
insurance details and no payment card details. Relay holds what the family types,
not anything drawn from a medical system.</p>

<h2>Who can see it</h2>

<p>Members of the circle, and nobody else using the app. Every table checks the
signed in account against circle membership before returning anything. There is no
clinician view and no access for any provider named in it. We do not sell any of it
and we do not send it to advertisers. Nothing is sent to a language model.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
<strong>RevenueCat</strong> sits between the app and the app store and tracks
whether your subscription is active, receiving the purchase events and an
identifier for your account. <strong>Apple</strong> handles the payment itself;
card details go to Apple and never to us.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your own membership and profile. Updates you posted
remain in the circle's feed, because a shared care record that developed gaps when
one sibling left would be unreliable for the people still using it. Deleting the
circle itself removes everything in it for everybody.</p>
""",
)

# ── Scope ───────────────────────────────────────────────────────────────────
# tables: profiles projects change_orders. draft-scope + draft-change-order call
# the model. Stores CLIENT name/email + acceptance records.
APPS["scope"] = dict(
    updated="11 September 2026",
    name="Scope",
    summary="What Scope keeps about your projects and your clients, and what a signed acceptance record contains.",
    body="""
<p>Scope takes a quote to a signed statement of work to a change order, for someone
working on their own. This policy explains what is kept.</p>

<h2>Your scope text is sent to Anthropic to be drafted</h2>

<p>This is the part you are least likely to assume, so it is here rather than at the
bottom. When you ask Scope to draft a statement of work or a change order, what you
wrote about the job is sent to a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, and the draft comes
back. If your description names the client or describes their business, that goes
with it.</p>

<p>Nothing is sent unless you ask for a draft.</p>

<h2>You are storing your clients' details</h2>

<p>A project holds a client's name and email address, and they did not install this
app or read this page. We treat that as your business record: we never contact your
clients, never market to them, never build any profile of them, and never sell or
share their details.</p>

<p>The one time we do reach a client is when <em>you</em> send them a document to
accept, because you asked us to.</p>

<h2>What an acceptance record contains</h2>

<p>When a client accepts a statement of work or a change order, Scope records that
acceptance so there is evidence the work was agreed. That record is kept with the
project and is the thing you would rely on in a dispute. It is yours, we do not
share it with anybody, and we take no position in any disagreement between you and a
client.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, your business name, default rate and
  currency, and whether your subscription is active.</li>
  <li><strong>Each project</strong>: client name and email, title, the scope itself,
  amounts and deposit, when it was sent and when accepted.</li>
  <li><strong>Each change order</strong>: what was requested, the line items, the
  change in price and days, and its acceptance.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your email
address. No bank connection and no card numbers. Scope records what a deposit was agreed
to be; it does not move the money and has nowhere to put a card.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives your scope text when you ask for a draft.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every project and every change order,
immediately and unrecoverably. Acceptance records are often the only evidence of what
was agreed, so export anything you may need before you delete.</p>
""",
)

# ── Stuck ───────────────────────────────────────────────────────────────────
# tables: profiles learners sessions turns. tutor calls the model.
# A CHILD's work, and the PARENT sees the transcript by design.
APPS["stuck"] = dict(
    updated="11 September 2026",
    name="Stuck",
    summary="What Stuck keeps from a child's homework session, and the fact that a parent can read all of it.",
    body="""
<p>Stuck helps with homework by asking questions rather than giving answers. It
cannot output a finished answer, which is a property of how it is built. This policy
explains what is kept and who reads it.</p>

<h2>A parent can read the whole transcript, and the child should know that</h2>

<p>This is the part that matters most, so it is here rather than at the bottom. Every
session is kept in full and the parent who owns the account can read it. That is
intentional, because a homework helper a parent cannot inspect is not one they can
trust.</p>

<p><strong>Tell the child.</strong> A young person who does not know their work is
being read is being watched rather than helped, and the app is meant to be the second
thing.</p>

<h2>The question is sent to Anthropic</h2>

<p>The tutoring is done by a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>. What the child types
is sent so a reply can come back. Whatever they write goes, including anything about
themselves they put in a message.</p>

<h2>This is information about a child</h2>

<p>We ask for as little as the app can work with: a name to tell one learner from
another, and a year or level so questions are pitched right. There is no date of
birth, no photograph, no school, no address and no contact detail for the child.</p>

<p>The child has no account of their own; the account belongs to the parent. We never
contact a child, and nothing about one is used for advertising in any form or sold to
anybody.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>The parent's email address</strong>, and whether the subscription is
  active.</li>
  <li><strong>Each learner</strong>, by the name and level given.</li>
  <li><strong>Each session</strong>, and every turn in it, as text.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to the
parent's email address. No grades, no school records and no payment card details.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives the text of each turn.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting the account removes the profile, every learner and every session and
turn, immediately and unrecoverably.</p>
""",
)

# ── The Binder ──────────────────────────────────────────────────────────────
# tables: profiles vaults vault_sections. No model call. v1 is vault +
# checklist; staged release deferred to v1.1, so the policy must NOT promise it.
APPS["thebinder"] = dict(
    updated="14 September 2026",
    name="The Binder",
    summary="What The Binder holds, and an honest account of what it does and does not yet do when you die.",
    body="""
<p>The Binder is the if-something-happens file: the things the people you leave
behind will need to find. This policy explains what is kept.</p>

<h2>What this version does, and what it does not</h2>

<p>Stated plainly because the alternative would be misleading about the most
important thing in the product. <strong>This version is a vault and a checklist that
you keep.</strong> It does not yet release anything to anybody automatically, and
nothing is sent to a named person on your death in this version.</p>

<p>Automatic staged release to named people, on verified death, is planned for a
later version. Until it ships, <strong>somebody has to know this exists and how to
get into it</strong>, or the file will not be found. Tell at least one person.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether you have paid.</li>
  <li><strong>Your vault</strong>, and the sections in it, with whatever you have
  written into each.</li>
</ul>

<p>What goes in the sections is entirely your choice, and people put serious things
in a file like this. Treat it as one of the most sensitive records you keep, because
it probably is.</p>

<h2>Please do not put passwords in it</h2>

<p>Worth saying directly. The Binder is designed for the things a person needs to
know: where documents are, who to call, what you wanted. It is not a password
manager, is not built to the standard one is built to, and passwords stored here
would sit in ordinary database rows. Use a password manager for those, and use The
Binder to say which one you use.</p>

<h2>What is not stored</h2>

<p>No password for the app itself, because there is not one. Signing in is by a code
sent to your email address. We do not ask for a Social Security number, a will, an
account number or a payment card, and none of those are fields.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no executor view and
no sharing feature in this version. We do not sell any of it, we do not send it to
advertisers, and nothing in it is sent to a language model.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
This app has no in-app purchase in this version, so nothing about a payment or a subscription reaches Apple or anyone else.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, the vault and everything written in
it, immediately and unrecoverably. There is no copy anywhere else, which is the point
of it and also the risk.</p>
""",
)

# ── Third Place ─────────────────────────────────────────────────────────────
# tables: profiles gatherings attendances. No model call. Explicitly NOT dating.
APPS["thirdplace"] = dict(
    updated="14 September 2026",
    name="Third Place",
    summary="What Third Place keeps about the gatherings you host or attend, and what other people there can see.",
    body="""
<p>Third Place is for recurring, low-commitment, in-person gatherings: one tap to say
you are coming, and an honest count of who actually turns up. This policy explains
what is kept.</p>

<h2>This is not a dating app, and it is not built like one</h2>

<p>Said plainly because the distinction changes what exists here. There is no
matching, no swiping, no algorithm pairing you with anybody, no private messaging and
no profile for anyone to browse. You see gatherings, and you say whether you are
coming.</p>

<h2>What other people see</h2>

<p>The host of a gathering sees who has said they are coming, by display name. Other
attendees see the same count and names. Nobody sees your email address, and there is
no way for another user to contact you inside the app.</p>

<p>You choose the display name, so if you would rather not show your full name,
use something else.</p>

<h2>The attendance count is honest, including about you</h2>

<p>The app records whether people who said they were coming actually came, because a
regular count that ignores no-shows is not useful to a host. That means your own
attendance history is visible to the host of a gathering you keep saying yes to.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address and display name</strong>, and whether a host
  subscription is active if you host.</li>
  <li><strong>Gatherings</strong>: what, where and when, as the host entered them.</li>
  <li><strong>Attendances</strong>: who said they were coming, and who came.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your email
address. <strong>No location tracking of any kind</strong>: a gathering has a place
because the host typed one, and your phone is never asked where you are. No phone
number, no photographs and no payment card details.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
This app has no in-app purchase in this version, so nothing about a payment or a subscription reaches Apple or anyone else.
Nothing is sent to a language model, we do not sell anything, and we do not send
anything to advertisers.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile and your attendances, immediately.</p>

<p><strong>Gatherings you hosted remain, and your host name remains on them.</strong>
The name was recorded on the gathering when you created it, so that a run club does
not lose its organiser's name the day that person leaves, and deleting your account
does not remove it. They were other people's evenings too. <strong>If you would
rather a gathering stopped, turn it off before you delete your account</strong>, so
that nobody arrives to an empty room.</p>
""",
)

# ── Threshold ───────────────────────────────────────────────────────────────
# tables: profiles children child_platforms guides progress change_alerts.
# No model call. Sets up parental controls; CHILD data; NO monitoring.
APPS["threshold"] = dict(
    name="Threshold",
    summary="What Threshold keeps to set up parental controls for one child, and why it never sees what that child does.",
    body="""
<p>Threshold walks you through every parental control across a phone, a console, a
tablet and the apps on them, for one child's age, in one sitting. This policy
explains what is kept.</p>

<h2>It does not monitor your child, and it cannot</h2>

<p>This is the most important thing on the page. Threshold tells you which settings
to change and where they are. It has no connection to your child's device, no
connection to any account of theirs, and no access to anything they do.</p>

<p>It does not see their messages, their browsing, their screen time, their location
or their friends. It cannot, because it is never connected to any of it. What you get
is a guide and a record of what you have set up.</p>

<h2>What we hold about the child</h2>

<p>As little as the app can work with: a name to tell one child's setup from
another's if you have more than one, and an age, because the age is what determines
which settings are recommended.</p>

<p>No date of birth, no photograph, no school, no contact detail, no device
identifier and no account name for any platform. The child has no account here, we
never contact them, and nothing about them is sold or used for advertising in any
form.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether you have paid for this child.</li>
  <li><strong>Each child</strong>: the name and age you entered.</li>
  <li><strong>Which platforms</strong> you said they use, and your progress through
  each guide.</li>
  <li><strong>Alerts</strong> for when a platform changes its settings, so a guide you
  completed can be revisited.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your email
address. <strong>No credentials for any platform.</strong> Threshold never asks for
your child's logins or your own, because it changes nothing on your behalf; you make
each change yourself, on the device.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
<strong>RevenueCat</strong> sits between the app and the App Store and tracks whether
your purchase is active; it receives the purchase events and an identifier for your
account. <strong>Apple</strong> handles the payment itself, and card details go to
Apple and never to us. Nothing is sent to a language model or to any platform named
in a guide.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every child and all progress,
immediately and unrecoverably. The settings you changed on real devices stay changed;
they were never ours to undo.</p>
""",
)

# ── Titrate ─────────────────────────────────────────────────────────────────
# tables: profiles doses symptom_logs weights. No model call. GLP-1. The registry
# risk note: never a dose recommendation.
APPS["titrate"] = dict(
    updated="14 September 2026",
    name="Titrate",
    summary="How Titrate handles GLP-1 dose, symptom and weight records, and the line it will not cross.",
    body="""
<p>Titrate handles what a GLP-1 prescription does not: side effects logged against
dose changes, protein targets sized to your weight, and a written record to take to
the next appointment. <strong>It will not tell you whether a symptom is normal.</strong>
That is a judgement for the person who prescribed the medication, and the app is
built to refuse it rather than approximate it. This policy explains what is kept.</p>

<h2>This is health information, and it is treated that way</h2>

<p>Your doses, your symptoms and your weight are information about your body and
about a medication you are taking. There is no useful way to soften that, so the rest
of this page is specific rather than reassuring.</p>

<h2>It never recommends a dose</h2>

<p>Worth stating on the privacy page because it limits what the app is for. Titrate
records the dose your prescriber set and what happened at it. It does not suggest
increasing, decreasing or skipping anything, and nothing in it is medical advice.
Dose decisions belong to you and your prescriber.</p>

<h2>Weight is stored, and that is worth a sentence</h2>

<p>Weight is one of the more sensitive things a person tracks, and people using a
GLP-1 have often had a long relationship with being weighed. It is kept because
change over time is the point of the record. It is never shown to anyone else, never
compared to anybody, and never used to advertise anything to you.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and a subscription status field that is unused in this version.</li>
  <li><strong>Each dose</strong>: what was taken and when.</li>
  <li><strong>Each symptom log</strong>: what you felt, how strongly, and on what day.</li>
  <li><strong>Weights</strong> you record, with their dates.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your email
address. No prescriber's details, no pharmacy, no prescription number, no insurance
information and no payment card details.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no clinician view, no
telehealth integration and no sharing feature. Nothing is sent to a language model, we
do not sell any of it, and no employer or insurer has any route to it.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
This app has no in-app purchase in this version, so nothing about a payment
or a subscription reaches Apple or anyone else.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile and every dose, symptom log and weight,
immediately and unrecoverably.</p>
""",
)

# ── Trade Desk ──────────────────────────────────────────────────────────────
# tables: profiles customers jobs line_items invoices stripe_events.
# No model call. Stores CUSTOMER data + Stripe.
APPS["tradedesk"] = dict(
    updated="14 September 2026",
    name="Trade Desk",
    summary="What Trade Desk keeps about your jobs and your customers, and who handles the money.",
    body="""
<p>Trade Desk is field service for one person with a van: under a minute of admin per
job, usable with gloves on. This policy explains what is kept.</p>

<h2>You are storing your customers' details</h2>

<p>A job is at somebody's property. Trade Desk holds your customers' names, their
contact details and their addresses, and they did not install this app or read this
page.</p>

<p>We treat that as your business record. We never contact your customers, never
market to them, never build any profile of them, and never sell or share their
details with anybody. The only time we reach a customer is when you send them an
invoice, because you asked us to.</p>

<h2>Money is handled by Stripe, not by us</h2>

<p>When a customer pays an invoice, that payment goes through
<a href="https://stripe.com/privacy">Stripe</a>. Card numbers never reach our
servers and we never store them. We keep a record that an invoice was paid and when,
which is what a ledger needs.</p>

<h2>It works offline, and syncs when it can</h2>

<p>Trade Desk is built to work in a basement with no signal, so jobs are recorded on
your device first and sent to our servers when a connection returns. Between those
two moments the record exists only on your phone.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>Your customers</strong>: names, contact details and addresses you enter.</li>
  <li><strong>Each job</strong>, its line items, and what was done.</li>
  <li><strong>Invoices</strong>, and whether they were paid.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your email
address. No card numbers, no bank credentials, and no location tracking: a job has an
address because you typed one, and your phone is never asked where you are.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Stripe</strong> processes payments and holds the card details.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<p>Nothing is sent to a language model.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every customer, job and invoice,
immediately and unrecoverably. You may need invoices for your own tax records, and
this app has no export, so keep whatever you need before you delete: an individual
invoice can be shared from the job it belongs to. Stripe keeps its own record of
payments, under its terms rather than ours.</p>
""",
)

# ── Vet Pocket ──────────────────────────────────────────────────────────────
# tables: profiles pets weights treatments triages. triage calls the model.
# Animal health. The ER-or-wait call is the risk surface.
APPS["vetpocket"] = dict(
    updated="11 September 2026",
    name="Vet Pocket",
    summary="What Vet Pocket keeps about your pet, what happens when you ask whether to go to the emergency vet, and the limits of that answer.",
    body="""
<p>Vet Pocket keeps your pet's records and helps you judge whether something is an
emergency visit or can wait until morning, with a cost range on each path. This
policy explains what is kept.</p>

<h2>What you describe is sent to Anthropic</h2>

<p>This is the part you are least likely to assume, so it is here rather than at the
bottom. When you ask whether to go now or wait, what you typed about your pet's
symptoms is sent to a large language model run by
<a href="https://www.anthropic.com/legal/privacy">Anthropic</a>, and the assessment
comes back.</p>

<p>Nothing is sent unless you ask for one. Recording a weight or a treatment stays on
our database.</p>

<h2>It is not a veterinarian, and it never is</h2>

<p>On the privacy page because it bounds what the app is. Vet Pocket helps you decide
whether to make a call. It does not diagnose, does not prescribe, and is not a
substitute for a vet. If you think your animal is in danger, go, and do not wait for
an app to agree with you.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and whether your subscription is active.</li>
  <li><strong>Each pet</strong>: the details you entered about them.</li>
  <li><strong>Weights and treatments</strong>, with their dates.</li>
  <li><strong>Each triage</strong>: what you described and what came back.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your email
address. No veterinary practice records, no pet insurance details, no microchip
number and no payment card details.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no vet view, and no
practice or insurer has any route to it. We do not sell any of it and we do not send
it to advertisers.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Anthropic</strong> receives what you describe when you ask for a triage.</li>
  <li><strong>Supabase</strong> hosts the database and sends the sign in codes.</li>
  <li><strong>RevenueCat</strong> sits between the app and the app store and
  tracks whether your subscription is active. It receives the purchase events and
  an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile and every pet, weight, treatment and
triage, immediately and unrecoverably.</p>
""",
)

# ── Waitlist ────────────────────────────────────────────────────────────────
# tables: profiles checkins module_progress instrument_items. No model call.
# MENTAL HEALTH, for people waiting for a first appointment. Highest duty of care
# on the page: it must say what happens in a crisis, because nothing does.
APPS["waitlist"] = dict(
    updated="14 September 2026",
    name="Waitlist",
    summary="How Waitlist handles what you record about your mental health while you wait for a first appointment, and what it does not do in a crisis.",
    body="""
<p>Waitlist is structured self-guided CBT and a fortnightly check, for the months
between a referral and a first appointment. This policy explains what is kept.</p>

<h2>Nobody is watching this, including in a crisis</h2>

<p>This is the most important thing on the page and it comes first. Waitlist is not
monitored by a clinician or by anybody else. <strong>No one reads your check-ins. No
alert is raised if your scores get worse, and nothing you write here reaches a crisis
service.</strong></p>

<p>That is a deliberate design: the app exists for a period when nobody is looking
after you, and pretending otherwise would be worse than saying so. But it means that
if you are in crisis, this app is not the thing to use. Contact your local emergency
number or a crisis line. It is not able to help, and it will not know.</p>

<h2>This is mental health information, and it is treated that way</h2>

<p>What you record here is about your mental health at a difficult time. There is no
useful way to soften that, so the rest of this page is specific rather than
reassuring.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, and a subscription status field that is unused in this version.</li>
  <li><strong>Each check-in</strong>: your answers to the questions asked, and the
  date.</li>
  <li><strong>Your progress</strong> through the CBT modules, and anything you wrote
  inside an exercise.</li>
</ul>

<h2>What is not stored</h2>

<p>No password, because there is not one. Signing in is by a code sent to your email
address. No name, no date of birth, no address, no phone number, no GP or clinic, no
referral details, no diagnosis and no payment card details. The app has nowhere to put
any of them, and that is on purpose.</p>

<h2>Who can see it</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before returning anything. There is no clinician view, no
service can request access, and there is no sharing feature of any kind.</p>

<p>Nothing you write is sent to a language model. <strong>We do not sell any of it, we
do not send it to advertisers, and no employer or insurer has any route to it.</strong>
If you take a summary to your first appointment, you take it; we send nothing to
anybody.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database and sends the sign in codes.
This app has no in-app purchase in this version, so nothing about a payment
or a subscription reaches Apple or anyone else.</p>

<h2>Deleting it</h2>

<p>Deleting your account removes your profile, every check-in and all module progress,
immediately and unrecoverably. If you want to show a clinician how the months went,
save it before you delete rather than after.</p>
""",
)


# ── Added 2026-09-12 ────────────────────────────────────────────────────────
# Both read out of the app's own migrations and functions on 2026-09-12, to the
# same standard as the 2026-09-06 batch. Two things are deliberately NOT
# claimed, because they are not true:
#   * Homeroom stores a reminder preference but NO function sends mail. The copy
#     says the setting is kept, not that email is sent.
#   * Signal Check has subscription COLUMNS but no billing code at all, so its
#     copy does not mention payment.
# Both pages exist because the apps link a privacy URL that was returning 404.

APPS["homeroom"] = dict(
    name="Homeroom",
    updated="12 September 2026",
    summary="What Homeroom keeps about your children, where their schoolwork is stored, and who can reach it.",
    body="""
<p>Homeroom is a homeschool record for one family. Almost everything in it is
about a child, so this policy leads with that rather than working up to it.</p>

<h2>This is a record about named children</h2>

<p>You enter your children yourself. For each one Homeroom keeps the name you
typed, a date of birth, a grade label, and whether they are currently active.
Against each child it keeps attendance dates and hours, any note you added,
the work you logged with its subject, title and description, and a reading log.</p>

<p>None of it is shared with anyone. There is no other parent, no teacher, no
classroom and no directory in this app. It is a filing cabinet, not a network.</p>

<h2>Uploaded documents are private, on purpose</h2>

<p>Work samples, filed affidavits and evaluator letters go into a private
storage area, not a public one. That distinction is the point: in several states
those documents carry a home address and a parent's signature, and a public
bucket would make them readable by anyone who ever saw the link. Only your
signed in account can read yours.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>Your email address</strong>, your timezone, your state, and the
  school year you are recording.</li>
  <li><strong>Each child</strong>, with the name, date of birth and grade you
  entered.</li>
  <li><strong>Attendance, work and reading</strong> logged against a child.</li>
  <li><strong>Files you upload</strong>, in private storage.</li>
  <li><strong>A reminder preference</strong>, meaning whether you want one and at
  what hour. Homeroom stores that setting today and does not currently send
  reminder email. If that changes, this page changes with it.</li>
  <li><strong>Whether your subscription is active</strong>, and when the period
  ends.</li>
</ul>

<h2>What is not stored, and where nothing goes</h2>

<p>No address, no phone number, no payment details. Purchases happen through the
App Store and card details never reach this app. Nothing you write is sent to an
AI model: Homeroom does not use one.</p>

<h2>Who can see your records</h2>

<p>You, and nobody else using the app. Every table checks the signed in account
against the owner of the row before it returns anything, so another family
cannot reach your children's records even if they go looking.</p>

<h2>Who else is involved</h2>

<ul>
  <li><strong>Supabase</strong> hosts the database that holds your children's
  records and the documents you upload, and sends the sign in codes.</li>
  <li><strong>RevenueCat</strong> sits between the app and the App Store and
  tracks whether your subscription is active. It receives the purchase events
  and an identifier for your account.</li>
  <li><strong>Apple</strong> handles the payment itself. Card details go to Apple
  and never to us.</li>
</ul>

<h2>Deleting it</h2>

<p>Account, then delete. It removes the account itself, and your children,
attendance, work, reading log and uploaded files go with it. It cannot be
undone and we cannot recover it for you. Deleting the account does not cancel
an App Store subscription, which is billed by Apple: cancel that in your device
Settings.</p>
""",
)

APPS["signalcheck"] = dict(
    name="Signal Check",
    updated="12 September 2026",
    summary="What Signal Check keeps for a parent and a teenager, why the teenager has their own account, and what each of them can see.",
    body="""
<p>Signal Check is an agreement between one parent and one teenager. Both of
them are users of it, and this policy is written to be read by either.</p>

<h2>The teenager has their own account</h2>

<p>Not a profile underneath the parent's. That is deliberate and it is the
reason the rest of this page reads the way it does: a separate account is what
makes "you can see exactly what they see" true rather than a promise, and it is
also what lets a teenager leave.</p>

<h2>You can each see everything in your own pair</h2>

<p>This is the part that matters most, so it is here rather than at the bottom.
Within a pair, both people see the same things: every term that has been
proposed, its current state, and every check in either of you has written. There
is no private side. Neither of you has a view the other cannot open.</p>

<p>Outside the pair, nothing is visible to anyone. There is no feed, no other
families, no search.</p>

<h2>Nobody can agree on your behalf</h2>

<p>A term becomes binding only when each person accepts it as themselves. That
rule is enforced by the database rather than by the app, which matters: a rule
that lives only in the phone is a suggestion, and an earlier version let a
parent record the teenager's agreement without the teenager ever seeing it. It
is now refused at the point of writing. You may agree on your own behalf and on
nobody else's.</p>

<h2>Age, and why no birthday is kept</h2>

<p>Signal Check is for 13 and over. We ask rather than verify, and we do not
store a date of birth, because keeping one would mean collecting the thing the
question is there to avoid.</p>

<h2>What is stored</h2>

<ul>
  <li><strong>An email address and a display name</strong> for each of you.</li>
  <li><strong>The pair</strong>, who is in it, which of you is the parent and
  which the teenager, and when it was ended if it has been.</li>
  <li><strong>Invite codes</strong>, and when they were used.</li>
  <li><strong>Terms</strong>: the text, who proposed it, who has accepted it, and
  any date it is set to loosen on.</li>
  <li><strong>Check ins</strong>: what was written and who wrote it.</li>
</ul>

<h2>What is not stored, and where nothing goes</h2>

<p>No date of birth, no address, no phone number, no location, no payment
details. Signal Check does not take payment. Nothing either of you writes is
sent to an AI model: Signal Check does not use one. There is no advertising and
no tracking.</p>

<h2>Who else is involved</h2>

<p><strong>Supabase</strong> hosts the database described above, the one that
enforces the pairing rule rather than leaving it to the app, and it sends the sign
in codes. Signal Check takes no payment, so no payment processor is involved at
all.</p>

<h2>Deleting it</h2>

<p>Either of you can delete your own account from inside the app, and doing so
ends your side of the pair. It cannot be undone and we cannot recover it for
you.</p>
""",
)


# ── Added 2026-09-12, second pass ───────────────────────────────────────────
# These two are unlike every other entry here: neither has a Supabase project,
# an account, or a server. Read out of the code on 2026-09-12.
#   * HomeRule makes exactly ONE outbound call, to the US Census geocoder, and
#     it is named. The first audit grep missed it, because the call reads
#     `(fetchImpl ?? fetch)(url)` and the literal string "fetch(" never appears.
# Quiet was ALMOST added here by mistake and is deliberately absent. It already
# has a page, generated from the APPS["quiet"] entry in make_privacy.py, and that
# copy is accurate: verified 2026-09-12 that the app has no network code, no
# host, no analytics. A duplicate entry here would have silently overridden it on
# the next --force, because privacy_content is merged OVER make_privacy's dict.
# The earlier sweep that reported Quiet as having "no privacy URL" was measuring
# the APP, which does not reference one. That is not the same as the page being
# missing.

APPS["homerule"] = dict(
    name="Home Rule",
    updated="25 September 2026",
    summary="Home Rule has no account and no server. Your address goes to one named place, and nothing about you goes anywhere else.",
    body="""
<p>Home Rule tells you which governments have authority over an address and who
currently holds office in them. There is no account, no sign in, and no server
belonging to us. Almost everything here is about the one exception.</p>

<h2>Your address goes to one place, and it is named</h2>

<p>To work out which districts contain an address, the address you type is sent
to the United States Census Bureau geocoder at
<code>geocoding.geo.census.gov</code>. That is a public federal service and it is
the only place your address is ever sent. It is how the lookup works and there is
no version of the feature without it.</p>

<p>We do not control that service and we do not receive a copy of what you sent
it. What the Census Bureau logs is governed by the Census Bureau, not by us.</p>

<h2>The lookup itself keeps nothing</h2>

<p>Searching for an address does not save it. Nothing is written as a side
effect of looking something up, and there is nowhere for it to be written to,
because there is no account and no database of ours anywhere.</p>

<h2>Saving an address is your decision, and it stays with you</h2>

<p>Home Rule lets you keep a small number of addresses so you do not have to
retype them. That is a separate, deliberate act, and what it writes stays on your
own device. There is no account to attach it to and no server to send it to.</p>

<p>So the promise is precise rather than sweeping: we never keep your address.
You can, and only you. On the web those saved addresses live in your browser's
own storage for this site and disappear when you clear site data.</p>

<h2>Who holds office, and how the list stays current</h2>

<p>The officeholder records, the districts and the sources they came from ship
inside the app itself. Because officeholders change between app updates, the app
also downloads newer copies of its officeholder lists when they exist, from
<code>carrierpress.com/homerule/data/officeholders.json</code> and
<code>carrierpress.com/homerule/data/statewide.json</code>. Those are plain
downloads of public files. They send no address, no identifier and nothing you
have looked up, and they are the same files for everyone.</p>

<p>Official portraits are shown as published by the government sites they come
from, so your device fetches each picture from that site, the way any web page
loads an image. We have no way of knowing which officials you looked at, because
nothing reports back to us.</p>

<h2>What there is none of</h2>

<p>No account. No password. No analytics, no crash reporting, no advertising, no
tracking and no third party SDK of any kind. No payment details: subscriptions
are bought through Apple, and we never see your card, your Apple ID or anything
about you beyond whether the subscription is active on this device. Your device's location is never requested,
and an address is only ever one you typed.</p>

<h2>Deleting it</h2>

<p>Delete the app, or clear its data. That removes anything you chose to save.
There is nothing held on our side to ask us to delete, and nothing for us to
recover if you change your mind.</p>
""",
)


# ── Cast ─────────────────────────────────────────────────────────────────────
# Written 2026-09-24 from ~/Projects/Cast/player. Same stack as the boating
# apps: async-storage and expo-iap, no server, no network code, no analytics,
# no crash reporter. Speech is Apple's on-device AVSpeechSynthesizer via
# expo-speech, so the book text is never sent anywhere to be voiced.
# Stored keys, read from lib/storage.ts, lib/purchases.ts and app/play.tsx:
#   cast          "unlocked", "progress:<stem>" (the line reached, per book)
APPS["cast"] = dict(
    name="Cast",
    updated="24 September 2026",
    summary="What Cast keeps about you, which is where you are in each book and whether you bought it.",
    body="""
<p>Cast performs Carrier Press books with a separate voice for each character
and music under the scenes. Every book is on your phone when you install it, so
it plays with no signal and nothing has to be fetched while you listen.</p>

<h2>There is no account and no server</h2>

<p><strong>You do not sign in, because there is nothing to sign in to.</strong>
This app has no database of ours, no cloud sync and no backend.</p>

<h2>The voices are made on your phone</h2>

<p>Every voice you hear is one of Apple's own speech voices, running on your
device. <strong>The text of the book is never sent anywhere to be read
aloud.</strong> No speech service, no language model and no server of ours is
involved, so nobody learns which book you are listening to or how far you got.</p>

<h2>What is stored, on your device</h2>

<ul>
  <li><strong>Where you are in each book</strong>, as a line number, so a book
  opens where you left it.</li>
  <li><strong>Whether the app is unlocked</strong>, so it does not have to ask
  the App Store every time it opens.</li>
</ul>

<p>That is the whole list. No name, no email address, no location and no
listening history beyond that one line number per book is asked for or kept.</p>

<p><strong>Nothing above is ever uploaded</strong>, because there is nowhere to
upload it to.</p>

<h2>Who else is involved</h2>

<p><strong>Apple, and nobody else.</strong> The unlock is a one-time purchase
made through the App Store, so Apple handles the payment and tells the app only
that the purchase exists.</p>

<p>There is no analytics, no crash reporting, no advertising and no tracking
software of any kind. There is no server of ours for anything to be sent to.</p>

<h2>Deleting it</h2>

<p>There is no account to close. <strong>Deleting the app removes your place in
every book with it</strong>, and there is no copy anywhere else. Your purchase
is held by Apple rather than by us, so reinstalling and tapping Restore brings
the unlock back without paying again.</p>
""",
)


# ── Downpour ─────────────────────────────────────────────────────────────────
# Written 2026-09-24 from ~/Projects/Downpour/mobile (the Expo app is nested).
# No network code on the iOS path (react-native-audio-api's fetch calls are all
# under src/web-core/), no storage dependency of any kind, no purchase, no
# analytics. State lives in React state and is gone when the app closes.
# Resolved Info.plist asks for no permissions; only UIBackgroundModes audio.
APPS["downpour"] = dict(
    name="Downpour",
    updated="24 September 2026",
    summary="What Downpour keeps about you, which is only whether you bought the unlock.",
    body="""
<p>Downpour plays rain for sleep. The rain is built live on your phone rather
than played from a recording, so nothing is streamed or downloaded while you
listen and it works with no signal at all.</p>

<h2>There is no account and no server</h2>

<p><strong>You do not sign in, because there is nothing to sign in to.</strong>
This app has no database of ours, no cloud sync and no backend.</p>

<h2>One thing is stored, on your device</h2>

<ul>
  <li><strong>Whether the app is unlocked</strong>, so the three extra surfaces
  play without asking the App Store every time, including with no signal.</li>
</ul>

<p>That is the whole list. The surface, treatments, volume and sleep timer you
choose are held only while the app is open and are forgotten when it closes.
<strong>Nothing is ever uploaded</strong>, because there is nowhere to upload
it to.</p>

<p>It asks for no permissions: not your microphone, not your location, not your
contacts and not your photos.</p>

<h2>Who else is involved</h2>

<p><strong>Apple, and nobody else.</strong> The unlock is a one-time purchase
made through the App Store, so Apple handles the payment and tells the app only
that the purchase exists. We never see payment details. There is no analytics, no crash reporting,
no advertising and no tracking software of any kind, and no server of ours for
anything to be sent to.</p>

<h2>Deleting it</h2>

<p>Delete the app. There is no account to close and no data held anywhere else
by us, so there is nothing to ask us to remove. Your purchase is held by Apple,
so reinstalling and tapping Restore brings the unlock back without paying
again.</p>
""",
)
