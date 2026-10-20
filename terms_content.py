#!/usr/bin/env python3
"""
The per-app half of the terms of use pages. make_terms.py holds the clauses
that are the same for every app; this file holds the one section that is not.

## WHY THIS SECTION EXISTS AND WHY IT IS FIRST

Every other clause in a terms page is machinery: who the agreement is with,
what Apple is responsible for, how a subscription renews. A reader skims it
because it reads the same on every app in the store, and mostly they are
right to.

The section below is the one that is actually about the app they are holding,
and it is the one that decides whether a disappointed user has been misled.
`What it is not` is a limit on the product, written down before somebody
relies on the product not having that limit. So it goes above the machinery,
not under a heading at the bottom, on the same argument make_privacy.py uses
for putting "your resume is sent to Anthropic" near the top.

## THE RULE FOR WRITING ONE

Each entry says what the app does, then names the thing a reasonable person
might otherwise assume it does. The limit has to be real and checkable in the
app, not a defensive hedge: "no warranty of any kind" is in the shared
clauses already and adds nothing here.

Where the portfolio has already written the limit down in its own voice, this
reuses that wording rather than inventing a second version of it. Four came
in from support_bodies/: boatready ("not an inspection and it is not legal
advice"), doorstop ("not a preparer and not tax advice, and it files
nothing"), homeroom ("summaries written for a parent, not legal advice") and
scope ("not legal advice and not a lawyer"). Two came from apps_data.py:
flare ("not a medical device") and pantry ("not a food-safety device"). A
page that contradicts the support page beside it is worse than either page
alone.

## WHAT IS DELIBERATELY NOT HERE

No arbitration clause, no class action waiver, and no jury trial waiver.
Those are a decision about how a dispute gets resolved rather than a
description of the product, they are the clauses most likely to be
unenforceable if written badly, and they are not Apple's to require. They
need a lawyer, and their absence is a choice rather than an oversight.

`bench` has no entry. It is the one app in apps_data.py with a slug and no
pages at all, because it is not built and the waiting list decides whether it
will be. An app with no binary needs no end user licence.
"""

# slug -> dict(name, summary, is_not)
#
# `summary` is the meta description and the og:description, so it reads as a
# sentence about this app rather than as a category label.
# `is_not` is HTML, and it is the whole of the section described above.

APPS = {}

# ── The marine three ───────────────────────────────────────────────────────
# All three answer from the federal text offline, and all three are read on a
# boat where being wrong has a cost that is not money. The limit is the same
# in each case and it is not softened: the app is a reference, the skipper is
# responsible, and the official publication wins.

APPS["boatready"] = dict(
    name="Boat Ready",
    summary="The terms for Boat Ready, including the limit that matters: it is a reference, not an inspection, and the skipper stays responsible.",
    is_not="""
<p>Boat Ready reads the federal carriage requirements for the boat you
describe to it and shows you the list, with the CFR citation behind every
line. It works offline because the text does not change while you are on the
water.</p>

<p><strong>It is not an inspection and it is not legal advice.</strong> It
answers from the boat you described. If you described the boat wrongly, or
the boat changed, or your state or your water adds a requirement the federal
text does not, the list will be wrong and the app has no way to know it. The
Code of Federal Regulations is the authority, not this app, and where the two
differ the CFR is right.</p>

<p>You remain the person responsible for the vessel, for what it carries and
for what the law requires of you. Nothing here transfers any part of that to
us, and a list that came out of this app is not a defence to anything.</p>
""",
)

APPS["nightwatch"] = dict(
    name="Night Watch",
    summary="The terms for Night Watch, including the limit that matters: it helps you learn the lights, it does not navigate for you.",
    is_not="""
<p>Night Watch identifies a vessel from the lights or the day shape you can
see, and gives you the Rule number behind the answer. The purchase opens
Practice mode, which drills the signatures.</p>

<p><strong>Do not navigate by this app.</strong> It is a reference and a
teaching tool. It cannot see what you are looking at, it does not know your
position, your visibility, your traffic or your sea room, and it has no way
of telling whether you have identified the right vessel. The Navigation
Rules are the authority, and the obligation to keep a proper lookout and to
avoid collision is yours and cannot be delegated to software.</p>

<p>An answer from Night Watch is a prompt to look harder, never a reason to
hold your course.</p>
""",
)

APPS["channelmarks"] = dict(
    name="Channel Marks",
    summary="The terms for Channel Marks, including the limit that matters: it explains the marks, it is not a chart and not a substitute for one.",
    is_not="""
<p>Channel Marks tells you what a US buoy or beacon is saying and which side
to pass it, with the handbook paragraph attached. The purchase opens Practice
mode.</p>

<p><strong>It is not a chart, and it is not a substitute for one.</strong> It
explains a mark in the abstract. It does not know where you are, which
channel you are in, which direction the convention runs in that particular
water, whether the mark has been moved, or whether it is still there at all.
Aids to navigation are changed and discrepancies are reported through the
Coast Guard's Local Notice to Mariners, and this app does not read those.</p>

<p>Navigate from a current chart and the official Light List. Use this to
understand what you are seeing, not to decide where to steer.</p>
""",
)

# ── Health and the body ────────────────────────────────────────────────────
# The hardest group to write, because the apps are genuinely useful and the
# temptation is to let the usefulness imply a clinical claim nobody made.
# Each entry names the clinical thing the app does not do, in the app's own
# terms rather than in a blanket "not medical advice" that covers everything
# and therefore warns about nothing.

APPS["flare"] = dict(
    name="Flare",
    summary="The terms for Flare, including the limit that matters: it finds patterns in what you logged, and it is not a medical device.",
    is_not="""
<p>Flare is a symptom log. You record what you felt and when, and it looks
for things that tend to occur together across your own entries, then prints
a summary you can hand to a doctor.</p>

<p><strong>It does not diagnose, explain or treat anything, and it is not a
medical device.</strong> A co-occurrence it shows you is a pattern in your
own typing. It is not a finding, it is not a cause, and it is not evidence of
a condition. Two things rising together in a log is one of the most
unreliable signals in medicine, which is exactly why the output is built to
be read by a clinician rather than acted on by you.</p>

<p>Nothing in Flare is a reason to start, stop or change a treatment. Take
the summary to the person qualified to read it, and if something is getting
worse, do not wait for the pattern to firm up first.</p>
""",
)

APPS["perimeter"] = dict(
    name="Perimeter",
    summary="The terms for Perimeter, including the limit that matters: it organises what you tell it into something you can say out loud. It does not diagnose.",
    is_not="""
<p>Perimeter holds a list of thirty-six perimenopause symptoms, including
several that are rarely connected to it, and turns what you mark into a
script for a ten minute appointment.</p>

<p><strong>It does not diagnose anything, and recognising your symptoms on a
list is not a diagnosis.</strong> The list exists because these symptoms are
under-recognised, and that cuts both ways: every one of them has other
causes, several of them serious. The script is there so the appointment
starts from a record instead of a feeling, not so it can be skipped.</p>

<p>Perimeter is not a substitute for a clinician and it does not know your
history, your medications or anything else about you that a doctor would ask
about first.</p>
""",
)

APPS["titrate"] = dict(
    name="Titrate",
    summary="The terms for Titrate, including the limit that matters: it charts what you recorded against your own dose history, and it does not advise on dosing.",
    is_not="""
<p>Titrate records the dose you took and the side effects you had, plots one
against the other, tracks a protein target you set, and tells you when a
plateau has lasted long enough to be worth a phone call.</p>

<p><strong>It does not advise on dosing.</strong> It never tells you to go
up, to hold, to come down or to stop. Your prescriber sets your dose, and the
only thing this app does with a dose is record the one you tell it you took.
Changing a GLP-1 dose on the strength of a chart on your phone is the
specific thing this app is built not to encourage.</p>

<p>Titrate is not a clinician and not a monitoring service. Nobody is
watching your entries. If something frightening is happening, it needs a
person, and the app's own copy says so at the point where that matters.</p>
""",
)

APPS["pillproof"] = dict(
    name="PillProof",
    summary="The terms for PillProof, including the limits that matter: it is not a medical device, and nobody is watching whether a dose was missed.",
    is_not="""
<p>PillProof is a medication reminder built for an older person to use and
for an adult child to pay for. It holds the schedule and prompts at the
right time.</p>

<p><strong>It is not a medical device, and it is not a monitoring
service.</strong> A reminder can fail for every ordinary reason a phone
fails: it is off, it is silent, it is flat, it is in another room, a
notification was swiped away, or an operating system update changed what
notifications an app is allowed to send. If somebody's safety depends on a
dose being taken, it cannot depend on this app alone, and nobody at Carrier
Press is alerted when a dose is missed.</p>

<p>Photo confirmation is not wired yet. That is the feature most people
would assume they were buying, which is why the app is not for sale until it
works. Nothing here is a reason to change a prescription.</p>
""",
)

APPS["signalcheck"] = dict(
    name="Signal Check",
    summary="The terms for Signal Check, including the limits that matter: it is consented to by the teenager, and it is not a crisis service.",
    is_not="""
<p>Signal Check is a wellbeing check-in that a teenager has agreed to in
writing and can see the whole of, with autonomy returning on a schedule both
people signed.</p>

<p><strong>It is not a crisis service and it is not monitoring.</strong> No
clinician, moderator or human of any kind at Carrier Press reads the
check-ins or is alerted by one. The app cannot detect risk, will not escalate
anything, and is not an alternative to an emergency number, a crisis line or
a professional. If a young person is in danger, this app is not in that
loop and was never meant to be.</p>

<p>It is also not surveillance, and a parent who wants covert monitoring has
bought the wrong product: the consent and the visibility are the design, not
a setting. Where a child is too young to agree for themselves, the adult
accepting these terms is agreeing on their behalf and is responsible for that
choice. A COPPA review is outstanding and the app is not for sale until it is
answered.</p>
""",
)

APPS["waitlist"] = dict(
    name="Waitlist",
    summary="The terms for Waitlist, including the limits that matter: it is structured self-guided work for the months before an appointment, not treatment and not a crisis service.",
    is_not="""
<p>Waitlist holds structured self-guided CBT material and a fortnightly
symptom check, for the months between a referral and a first appointment. It
is licensed to a clinic or a university, and it is free to the person using
it.</p>

<p><strong>It is not treatment, not therapy and not a crisis
service.</strong> Nobody reads your answers in real time, nothing you enter
raises an alarm anywhere, and the symptom check is a record for your own
appointment rather than an assessment. It does not shorten your wait, it does
not change your place in a queue, and it is not a reason to decline the
appointment when it comes.</p>

<p>If you are in crisis, use an emergency number or a crisis line. This app
is designed for the waiting, not for the emergency, and the licensed
instrument text it needs is still outstanding.</p>
""",
)

APPS["vetpocket"] = dict(
    name="Vet Pocket",
    summary="The terms for Vet Pocket, including the limit that matters: the triage answer is a cost range and a sense of urgency, not a diagnosis.",
    is_not="""
<p>Vet Pocket keeps your animal's records and answers the eleven at night
question: is this an emergency visit, or can it wait until Monday, and
roughly what does each path cost.</p>

<p><strong>It is not a veterinarian and the answer is not a
diagnosis.</strong> It has not seen your animal. It is working from what you
typed, and the cost figure is a range of what that kind of visit tends to
run, not a quote, not a price we can hold anyone to, and not an opinion about
what your animal needs.</p>

<p>A wait until Monday answer is never a reason to override your own eyes. If
your animal is deteriorating, call a vet or an emergency clinic, and treat
anything this app says as the less informed of the two opinions.</p>
""",
)

APPS["crosscheck"] = dict(
    name="Crosscheck",
    summary="The terms for Crosscheck, including the limit that matters: it is not a lawyer, not a billing advocate, and nothing it writes is legal advice.",
    is_not="""
<p>Crosscheck reads a hospital bill against the explanation of benefits,
finds the lines that do not agree, and writes an appeal letter that cites the
reasoning it used.</p>

<p><strong>Crosscheck is not a lawyer and not a billing advocate, and
nothing it produces is legal advice.</strong> It does not represent you, it
does not file anything, it does not talk to your insurer or your provider,
and it is not running a case on your behalf. The letter is a draft for you to
read, change and send as your own.</p>

<p>It can be wrong about a line, and an appeal it supports can still fail.
Appeals run on deadlines set by your plan and your state, and missing one is
final: the app does not track them for you and cannot extend one. The app is
held on regulatory grounds and is not for sale while that is unresolved.</p>
""",
    paying="""<h2>Paying for it</h2>

<p>Crosscheck is {price}, through the App Store. <strong>It is charged per
case rather than once:</strong> the error detection is free, and you pay when
there is something to appeal, so a second appeal is a second payment. It is
not a subscription and nothing renews on its own, but neither is it a single
unlock that covers everything afterwards.</p>

<p>The price shown in the App Store when you buy is the one that applies, and
paying for a case buys the appeal letter for that case. It does not buy an
outcome: the letter can be sent and the appeal can still be refused, and
there is no refund for an appeal that fails.</p>

<p>Apple takes the payment and Apple handles refunds, under its own policy, at
<a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>. We
cannot issue a refund for an App Store purchase.</p>
""",
)

APPS["quiet"] = dict(
    name="Quiet",
    summary="The terms for Quiet, including the two that matter: it never leaves your phone, which also means nobody can recover it for you.",
    is_not="""
<p>Quiet is a personal record that stays on the device. There is no account,
no sync, and no code in it that sends what you write anywhere. The one-time
purchase removes the ten entry limit for good.</p>

<p><strong>Because there is no server, there is no backup and no
recovery.</strong> This is the trade the product is built on and it is worth
being plain about: if you delete the app, lose the phone, or wipe it, what
you wrote is gone, and we cannot get it back because we never had it. Export
regularly if it matters to you. Delete everything means it, immediately, and
we cannot undo it.</p>

<p>Quiet is a journal and not therapy. Nobody reads it, which is the point,
and which also means nothing in it reaches anyone who could help.</p>
""",
)

APPS["relay"] = dict(
    name="Relay",
    summary="The terms for Relay, including the limit that matters: it is a shared family record, not a medical record and not a care service.",
    is_not="""
<p>Relay replaces the seven sibling group chat with a typed update feed, so
the family can find out what happened without scrolling.</p>

<p><strong>It is not a medical record and not a care service.</strong> What
is in it is what a family member typed. It is not verified, it is not
clinical documentation, no professional is reading it, and a clinician has no
obligation to accept anything out of it. Do not rely on it as the record of a
medication, a dose or an instruction from a doctor.</p>

<p>Everyone invited into a household can read what is posted there, which is
the purpose, and you should treat anything you write in it as something the
whole household will see. Whoever posts about another person's health is
responsible for having the standing to do that.</p>
""",
)

# ── Money, tax and documents ───────────────────────────────────────────────
# Three of these end in a federal tax form and one ends in a file somebody
# opens after a death. In every case the app does arithmetic on what the user
# entered and files nothing, and that is the limit that has to be unmissable.

APPS["soleledger"] = dict(
    name="Books for One",
    summary="The terms for Books for One, including the limit that matters: it is not a preparer, not tax advice, and it files nothing.",
    is_not="""
<p>Books for One is a freelancer's ledger: income, deductions, the four
federal quarterly dates, and 1099 reconciliation. You enter your own annual
target and it does the arithmetic.</p>

<p><strong>It is not a tax preparer, it is not tax advice, and it files
nothing.</strong> It never applies a tax rule to you and never decides
whether something is deductible. It adds up what you told it and sorts it the
way you sorted it. Nothing is transmitted to the IRS or to any state, no
return is prepared, and no extension or payment is made on your behalf.</p>

<p>The numbers it shows are only as right as your entries, and a quarterly
estimate out of this app is an estimate you produced. Your return, your
payments and the deadlines are yours, and a CPA or an enrolled agent is the
person who should see this before you rely on it.</p>
""",
)

APPS["doorstop"] = dict(
    name="Doorstop",
    summary="The terms for Doorstop, including the limit that matters: it is not a preparer and not tax advice, and it files nothing.",
    is_not="""
<p>Doorstop is a ledger for a landlord with one to six units. It keeps each
unit's books apart and ends in a clean Schedule E. When it cannot tell a
repair from an improvement it asks you, because the answer changes whether
the cost comes off this year or is depreciated over 27.5 years.</p>

<p><strong>It is not a preparer and not tax advice, and it files
nothing.</strong> It never applies a tax rule. It checks rather than assumes,
and the answer it writes down is the answer you gave it. A Schedule E out of
this app is a worksheet you produced, not a return, and nothing goes to the
IRS or to any state.</p>

<p>Repair against improvement is a judgment with real money on it, and
getting it wrong is your exposure rather than ours. Have a CPA review the
treatment before you file.</p>
""",
)

APPS["houseledger"] = dict(
    name="House Ledger",
    summary="The terms for House Ledger, including the limit that matters: it is the record you keep, not a warranty, an inspection or a disclosure.",
    is_not="""
<p>House Ledger is a home's service record: the systems, their ages, their
warranties and who worked on them, kept so that it hands over cleanly when
the house sells.</p>

<p><strong>It is not an inspection, not a warranty and not a
disclosure.</strong> Every record in it is one you entered. The app does not
verify that a warranty is in force, does not know whether a term has lapsed,
does not chase a contractor, and has no view on whether work was done
properly. A warranty is a contract between you and whoever issued it, and
what this app shows about it has no bearing on that.</p>

<p>If you hand the record to a buyer, you are making the representations in
it, not us. Seller disclosure is set by your state and this app does not
satisfy it.</p>
""",
)

APPS["tradedesk"] = dict(
    name="Trade Desk",
    summary="The terms for Trade Desk, including the limits that matter: the invoices and the records are yours, and offline work syncs when the van has signal again.",
    is_not="""
<p>Trade Desk is field service admin for one person with a van: under a
minute of paperwork per job, usable with gloves on, and built to work with no
signal.</p>

<p><strong>It is not an accountant, a payment processor or a compliance
tool.</strong> An invoice it produces is a document you issued. It does not
collect money, does not calculate or remit sales tax, and does not know what
your trade or your state requires on an invoice, a licence number or a
contract. Whether a job was quoted, done or billed correctly is between you
and your customer.</p>

<p>Offline first means work is held on the phone until there is signal. A
phone that is lost or wiped before it syncs takes whatever had not synced
with it, and that is a limit of working offline rather than a fault.</p>
""",
)

APPS["cancelled"] = dict(
    name="Canceled",
    summary="The terms for Canceled, including the limit that matters: it finds the charges and shows you where to cancel. It cancels nothing for you.",
    is_not="""
<p>Canceled reads a bank statement on your phone, finds the recurring
charges, ranks them by what they cost you in a year, and shows you where to
cancel each one. Your statement is never uploaded.</p>

<p><strong>It does not connect to your bank and it cancels
nothing.</strong> The first is a deliberate limit rather than a missing
feature, and the second follows from it: the app has no account anywhere, no
authority to act for you, and no way to end a subscription on your behalf.
You cancel it, with the merchant, yourself.</p>

<p>It reads what the statement says. A charge can be missed, misread or
misnamed, cancellation instructions change without telling anyone, and a
charge it flagged may be one you meant to keep. Nothing here stops a renewal,
and a subscription you did not cancel is still running.</p>
""",
)

APPS["scope"] = dict(
    name="Scope",
    summary="The terms for Scope, including the limit that matters: it is not legal advice and not a lawyer, and the documents are yours.",
    is_not="""
<p>Scope takes a solo service provider from a quote to a signed statement of
work to a change order, so raising a change order stops being a conversation
you dread.</p>

<p><strong>It is not legal advice and not a lawyer.</strong> The documents
are starting points. Whether one is enforceable where you work, whether it
says what your trade needs it to say, and whether a signature collected this
way is valid for your purpose are all questions this app cannot answer. A
contract you sent from Scope is a contract you wrote.</p>

<p>It does not review what you agreed to, does not advise on a dispute, and
takes no position on whether a change order is justified. Where the money or
the risk is material, the document should be read by a lawyer before it is
sent rather than after it is argued about.</p>
""",
)

APPS["thebinder"] = dict(
    name="The Binder",
    summary="The terms for The Binder, including the limit that matters: it is not a will and it is not an estate plan.",
    is_not="""
<p>The Binder is the if-something-happens file: the vault and the checklist,
built free, with release to named people the paid part.</p>

<p><strong>It is not a will, not a trust and not an estate plan.</strong>
Nothing assembled here has testamentary effect. A will has formal
requirements set by your state, usually including witnesses, and no app
satisfies them. If this file is all that exists when it is needed, your
estate will be handled as though you left no instructions, because legally
you did not.</p>

<p>It is also not a typeset PDF, and staged release is deferred to v1.1 by
design, which is the reason it is not for sale yet. Treat the vault as the
thing that makes a real estate plan easier to carry out, not as a substitute
for having one. Get a will drawn up by an attorney in your state.</p>
""",
    paying="""<h2>Paying for it</h2>

<p>The Binder is {price}, through the App Store. The vault and the checklist
are free to build in full, and the payment is for naming the people it
releases to. Both parts are described on the <a href="/{slug}/">app's own
page</a>, and the price shown in the App Store when you buy is the one that
applies.</p>

<p><strong>This is a one-time payment and then a renewing annual one, so read
the second half carefully.</strong> The first charge is the one-time purchase.
The annual part renews automatically at the end of each year and Apple charges
your Apple Account within 24 hours of the end of the current period, unless
you cancel at least 24 hours before it ends. The one-time payment is not
refunded if you later cancel the annual part.</p>

<p>Cancel in Settings on your device, under your Apple Account, then
Subscriptions. We cannot cancel it for you and we cannot see or change your
billing. If the annual part lapses, treat the release mechanism as not
running: what you have stored stays yours to read and export, and nothing is
released to anybody.</p>

<p>Apple takes the payment and Apple handles refunds, under its own policy, at
<a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>. We
cannot issue a refund for an App Store purchase.</p>
""",
)

# ── Law, rules and jurisdictions ───────────────────────────────────────────
# These answer a question whose real answer is a statute, a permit office or
# an election authority. Each entry has to say the same thing in its own
# terms: the app is a summary with a date on it, and the authority is
# elsewhere.

APPS["homeroom"] = dict(
    name="Homeroom",
    summary="The terms for Homeroom, including the limit that matters: the state rules are summaries written for a parent, not legal advice.",
    is_not="""
<p>Homeroom measures a homeschool year against your own state's rules and
assembles the portfolio as the year goes, so a gap shows in week two rather
than in June.</p>

<p><strong>These are summaries written for a parent, not legal
advice.</strong> Each one is a reading of a statute as it stood when it was
checked, and every page shows that date. Legislatures amend these rules,
districts interpret them differently, and your own circumstances may change
which of them apply to you. Where the statute and this app disagree, the
statute governs.</p>

<p>The compliance assertion is the product and it is still waiting on legal
review of the per-state rule set, which is why it is not for sale. When it
ships, an assertion from Homeroom is a record you are keeping, not a
determination by any authority, and it binds no district, board or court.
Filing what your state requires, on time, remains yours.</p>
""",
)

APPS["permitpath"] = dict(
    name="Permit Path",
    summary="The terms for Permit Path, including the limit that matters: it tracks the application, it is not an expediter and it is not legal advice.",
    is_not="""
<p>Permit Path holds a per-jurisdiction permit checklist, tracks the
application department by department, and builds the timeline from what
actually happened rather than from what you were promised.</p>

<p><strong>It is not a permit expediter, not a licensed design professional
and not legal advice.</strong> It files nothing, submits nothing, and speaks
to no department on your behalf. A checklist is a reading of one
jurisdiction's requirements at the time it was researched and loaded, and
those requirements change, as do fees, forms and which counter owns which
review.</p>

<p>Nothing here approves anything, and a complete checklist is not a permit.
Building or operating without the permit your jurisdiction actually requires
is your exposure, whatever this app showed you.</p>
""",
)

APPS["threshold"] = dict(
    name="Threshold",
    summary="The terms for Threshold, including the limit that matters: it is a checklist you work through. The controls belong to Apple, Google and the platforms.",
    is_not="""
<p>Threshold walks you through every parental control across phone, console,
tablet and the ten apps a child actually uses, for one child's age, in a
single sitting. One payment per child.</p>

<p><strong>It does not set any control and it is not monitoring
software.</strong> You make each change yourself, in the platform's own
settings, on your own devices. Threshold cannot see whether a setting took,
cannot tell you it was switched off later, and is not watching anything
afterwards. Every control described belongs to Apple, Google, Microsoft,
Nintendo or the app vendor, and any of them can move, rename or remove it
without notice, which can leave an instruction here out of date.</p>

<p>No configuration makes a child safe online. A finished checklist reduces
exposure and does not eliminate it, and it is not a substitute for knowing
what your child is doing.</p>
""",
    paying="""<h2>Paying for it</h2>

<p>Threshold is {price}, through the App Store. You can see the whole
checklist for a child's age before paying for anything.</p>

<p><strong>It is one payment per child, never a subscription.</strong> The job
is done in an afternoon and should not bill you monthly for the rest of the
year, so nothing renews and nothing recurs. It is charged per child rather
than once for the app, so a second child is a second payment, and the price
shown in the App Store when you buy is the one that applies.</p>

<p>Apple takes the payment and Apple handles refunds, under its own policy, at
<a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>. We
cannot issue a refund for an App Store purchase. A purchase is tied to your
Apple Account, so Apple's Restore Purchases will return it on a new device at
no further cost.</p>
""",
)

# NO `homerule` ENTRY, AND IT IS NOT AN OVERSIGHT. Home Rule became Who
# Serves, and `homerule/index.html` is now a "Who Serves has moved" notice.
# Its privacy page is still there because a shipped binary and a live listing
# link to it, and those cannot be edited after the fact. No binary links a
# terms page, because none has ever existed, so generating one would put a
# document at a URL nothing references and give the renamed app two sets of
# terms. Who Serves has the entry; its page is /whoserves/terms/.

APPS["whoserves"] = dict(
    name="Who Serves",
    summary="The terms for Who Serves, including the limit that matters: every line carries its source and check date, and it is not an official source.",
    is_not="""
<p>Who Serves puts everyone who governs your address on one screen: the
districts, the offices, the names, the source and check date behind each, and
when each of them is next up for election. The subscription adds recent votes
and filings for your members of Congress and addresses a letter to any
officeholder you pick.</p>

<p><strong>It is not an official source and it is not an election
authority.</strong> Each entry is right as of its check date. Vote and filing
records come from Congress.gov and are summarised; a summary can be wrong
about a bill in ways that matter, and the official record governs. Election
dates move.</p>

<p>Do not rely on it to register, to find a polling place, or to meet any
deadline for voting, filing or candidacy. A letter it addresses is a letter
you are sending, and we do not deliver it, read it or take any position on
it.</p>
""",
)

APPS["planfinder"] = dict(
    name="Plan Finder",
    summary="The terms for Plan Finder, including the limits that matter: the sample data is invented, and it enrolls nobody in anything.",
    is_not="""
<p>Plan Finder is a guided Medicare Advantage comparison that compares on the
whole picture, including whether a plan covers the drugs somebody already
takes. It is licensed to agencies.</p>

<p><strong>It is not an insurance agent, broker or plan, it is not connected
to Medicare or to CMS, and it enrolls nobody in anything.</strong> It
produces a comparison for a person to read. It does not recommend a plan,
does not submit an application, and does not create any relationship between
you and a carrier.</p>

<p>The sample comparison runs on invented data on purpose. The carriers,
plans and coverage in it are fictional, so a demo can never misdescribe a
real product, and nothing in the sample should be read as a statement about
any actual plan. For real coverage, the authority is the plan's own Evidence
of Coverage and the official Medicare Plan Finder. Where an agency licenses
this, that agency is responsible for its own advice and its own compliance,
not us.</p>
""",
)

APPS["gedcompletion"] = dict(
    name="GED Completion",
    summary="The terms for GED Completion, including the limit that matters: it is a completion engine, not the test and not a credential.",
    is_not="""
<p>GED Completion is a completion engine rather than a question bank:
diagnostic first, no streaks, with a caseworker dashboard. It is contracted
by a board, a facility or an employer, and it is free to every student.</p>

<p><strong>It is not the GED test, it is not affiliated with GED Testing
Service or any awarding body, and it issues no credential.</strong> Finishing
everything here earns you nothing by itself. You still sit the real test,
through the official channel, under that body's own rules and fees.</p>

<p>It does not predict whether you will pass and does not guarantee an
outcome. The question bank it needs is still outstanding. Where an
institution contracts this, what that institution does with a student's
progress is governed by its own policies and its agreement with us.</p>
""",
)

# ── People, places and gatherings ──────────────────────────────────────────
# The group with the least paperwork and the most real-world risk. Three of
# these put a user in contact with a stranger or send a child to a door, and
# none of them vets anybody. That has to be said outright.

APPS["porchlight"] = dict(
    name="Porchlight",
    summary="The terms for Porchlight, including the limit that matters: a pin means a household opted in. It is not a vetted or inspected house.",
    is_not="""
<p>Porchlight is the opt-in map of which houses are giving out candy on
Halloween night, with what each is handing out and how far away it is. The
map is free to everyone walking the street and always will be.</p>

<p><strong>A pin means somebody put themselves on a map. It means nothing
else.</strong> We do not visit, verify, vet, inspect or background check any
household, and we could not. We do not know who lives there, whether the
listing is honest, whether the route to the door is safe, or whether the
allergy-safe and step-free notes are accurate. Those notes are the
household's own claim.</p>

<p>Supervise your children. Check the candy yourself. Treat an allergy note
as a conversation to have at the door rather than an assurance, because for a
child with a serious allergy the consequence of a wrong label is not
something an app can carry. An adult using this app accepts that the
decision to approach any house is theirs.</p>
""",
    paying="""<h2>Paying for it</h2>

<p><strong>Porchlight is free to everyone walking the street, and it always
will be.</strong> There is nothing to buy to see the map, no trial that ends,
and no account needed. Nothing in this agreement charges you anything.</p>

<p>The paid side is the organiser side, for whoever is running a
neighbourhood's night rather than walking it. If that is ever sold to you, it
will be priced in the App Store at the point of purchase and the terms of that
purchase will be on this page before it is.</p>

<p>Free does not mean unsupported, and it does not change anything above about
what the map is: a household's own opt-in, which nobody has verified.</p>
""",
)

APPS["potluck"] = dict(
    name="Potluck",
    summary="The terms for Potluck, including the limit that matters: neighbours are not vetted, and a lend is between the two of you.",
    is_not="""
<p>Potluck is neighbourhood organising and lending, geofenced to a few
blocks, with the address verified without an address being stored. Two verbs:
organise a thing, lend a thing. It is free to every neighbour, permanently,
and sold to the association or the city.</p>

<p><strong>We do not vet, verify or background check your
neighbours.</strong> Address verification confirms that somebody could
receive something at a location. It is not an identity check, a character
reference or a statement that a person is safe to meet or to lend to.</p>

<p>Whatever you lend, you lend at your own risk, and whatever you break, you
answer for. We are not a party to it, we do not insure it, we do not hold a
deposit and we will not arbitrate it. Meeting anyone from this app is your
decision. Moderation shipped in the first migration rather than being bolted
on later, and it is still moderation, which is not the same as safety.</p>
""",
)

APPS["thirdplace"] = dict(
    name="Third Place",
    summary="The terms for Third Place, including the limits that matter: hosts and guests are not vetted, and it is explicitly not dating.",
    is_not="""
<p>Third Place is recurring low-commitment gatherings: one tap to say you are
coming, and an honest count of who actually turns up regularly. Free for
everyone attending, and only the host pays.</p>

<p><strong>This is explicitly not a dating app, and we vet
nobody.</strong> No host and no guest is verified, identity checked or
background checked. A gathering is organised by a person, in a place we have
never seen, and we are not the organiser, the venue or the insurer of
anything that happens there.</p>

<p>A host is responsible for their own gathering, including whatever their
venue, their local rules or their insurance require of them, and for anything
they serve. Deciding to attend, and deciding to leave, is yours. Using this
to pursue somebody who has made clear they are not interested is grounds for
removal.</p>
""",
)

APPS["handoff"] = dict(
    name="Handoff",
    summary="The terms for Handoff, including the limit that matters: it exports in a form a court will accept, which is not the same as legal advice.",
    is_not="""
<p>Handoff is a co-parenting calendar, expense splits, and a message log that
exports in a form a court will accept. The log is free and stays free; export
is the paid part.</p>

<p><strong>It is not a lawyer, a mediator or a court, and nothing in it is
legal advice.</strong> An export is a record of what was typed in this app. It
is not certified, not authenticated, and we do not appear to attest to it. No
court is obliged to admit it, what a court requires is set by its own rules
and your jurisdiction, and whether anything here helps your case is a
question for your attorney.</p>

<p>A record only one person can revise is not a record, so the other parent
can see what you write and edits are visible. Write accordingly. The app
takes no side, does not enforce a custody order, does not calculate support,
and cannot make anyone pay their half of an expense.</p>
""",
)

APPS["firstday"] = dict(
    name="FirstDay",
    summary="The terms for FirstDay, including the limit that matters: it reads the school email so you have one list, and it does not replace reading the letter.",
    is_not="""
<p>FirstDay takes the school emails and PDFs you forward it and hands back
one calendar, one supply list and one form tracker. It is seasonal by nature:
most families need it in August and again in January.</p>

<p><strong>It does not replace reading the letter.</strong> Extraction gets
dates, items and deadlines wrong, especially from a scan, a photograph or a
newsletter laid out in columns. A date that is not on the calendar may still
be real, and one that is may be wrong. The school's own communication is the
authority.</p>

<p>It sends nothing to the school, submits no form, and returns no permission
slip on your behalf. A missed deadline is a missed deadline whatever this app
showed, and the forms are yours to file.</p>
""",
)

# ── The ones where a model does the work ───────────────────────────────────
# Three apps where the useful output is produced by a language model. The
# privacy pages already say the text is sent to Anthropic, near the top, for
# the same reason. What these clauses add is the other half: a model is
# confidently wrong sometimes, and the output is a draft.

APPS["throughthegate"] = dict(
    name="Through the Gate",
    summary="The terms for Through the Gate, including the limits that matter: your resume goes to a model to be read, and the result is one parser's reading.",
    is_not="""
<p>Through the Gate shows you the structured record a resume parser builds
from your resume, and everything it threw away. One resume is parsed in full,
free, so you see the whole record before you decide anything.</p>

<p><strong>Your resume is sent to Anthropic to be read.</strong> The parsing
is done by a large language model rather than by code on our machines, and a
resume is not anonymous: yours almost certainly carries your name, address,
employers and dates, and all of it goes. The privacy policy covers this in
full, and the sample on our website runs on an invented resume if you would
rather it did not happen.</p>

<p><strong>It is one parser's reading, not the one an employer will
use.</strong> Every applicant tracking system parses differently, and what
this app discards is not necessarily what theirs will. A clean record here is
not a prediction about any employer's software, is no indication of whether
you will be contacted, and is not career advice. Priced by the month because
a job search ends.</p>
""",
)

APPS["errand"] = dict(
    name="Errand",
    summary="The terms for Errand, including the limit the product is built on: it stops at the confirm button, every time, on purpose.",
    is_not="""
<p>Errand researches the thing, drafts the message, fills the form, and then
stops at the confirm button and hands it back to you. Assistive, not
autonomous. Five errands a month are free.</p>

<p><strong>It stops at the confirm button. Every time, on purpose, and this
is not a setting that could be turned off.</strong> It submits nothing,
sends nothing, pays nothing and agrees to nothing on your behalf. When you
press confirm, you are the one applying, writing, booking or filing, and you
are responsible for what it says.</p>

<p>Read it before you send it. The research and the draft are produced by a
language model, which means they can be fluent and wrong at the same time: a
fee, a deadline, an eligibility rule or an office's requirements may be out
of date or simply invented. Anything that matters should be checked against
the authority's own page before you confirm.</p>
""",
)

APPS["stuck"] = dict(
    name="Stuck",
    summary="The terms for Stuck, including the limits that matter: it cannot output the answer, and it is not a substitute for a teacher.",
    is_not="""
<p>Stuck is homework help that is Socratic by architecture: your child types
the problem they are stuck on and gets the next question back, never the
answer. A parent can read the whole transcript. Five sessions a month are
free, with the full transcript.</p>

<p><strong>It cannot give an answer. That is not a policy, it is how it is
built</strong>, and it is why it is not a tool for finishing homework
quickly.</p>

<p><strong>It is not a substitute for a teacher</strong>, and a question it
asks can still be a poor one: the questions come from a language model, which
can misread a problem, follow a dead end, or be wrong about the mathematics
or the history underneath it. Read the transcript. A parent or guardian
accepts these terms on behalf of a child who uses the app and is responsible
for supervising that use, and whether using it is allowed on a given
assignment is between you and the school.</p>
""",
)

# ── Everything else ────────────────────────────────────────────────────────

APPS["papertrail"] = dict(
    name="Paper Trail",
    summary="The terms for Paper Trail, including the limit that matters: an alert is best effort, and a lapse is still a lapse.",
    is_not="""
<p>Paper Trail photographs receipts, warranties and policies into structured
facts and warns you before something lapses. Twenty documents are free and
kept forever, with alerts on all of them.</p>

<p><strong>An alert is best effort, not a guarantee.</strong> It depends on a
date being read correctly off your document, and on a notification or an
email actually arriving: extraction misreads dates, especially on a crumpled
receipt or a scan, and notifications fail because a phone is off, silent,
flat or has had its permissions changed. If a deadline would be expensive to
miss, keep your own reminder as well.</p>

<p>It does not renew, cancel, claim or extend anything for you, and it is not
a party to any warranty or policy in it. A return window that closed, a
policy that auto-renewed and charged you, or a warranty that lapsed are
between you and that company, whatever the app did or did not warn you
about.</p>
""",
)

APPS["pantry"] = dict(
    name="Pantry",
    summary="The terms for Pantry, including the limit that matters: it orders what you entered by expiry. It is not a food-safety device.",
    is_not="""
<p>Pantry inverts the meal planner: it starts from what is already in the
house and what expires first, rather than from a recipe you have to shop for.
The whole pantry and the expiry order are free, always.</p>

<p><strong>It is not a food-safety device.</strong> It sorts the dates you
typed in. It has not seen your food, does not know how it was stored, and
cannot tell you whether anything is safe to eat. A date on a package is a
manufacturer's quality estimate rather than a safety line, and food kept
badly can be unsafe well before the date it carries.</p>

<p>Use your own judgement, and the guidance from your own food safety
authority, on whether to eat something. The app also takes no position on
allergens or dietary requirements: ingredients are what you entered, and a
recipe it suggests has not been checked against anybody's allergy.</p>
""",
)

APPS["cast"] = dict(
    name="Cast",
    summary="The terms for Cast, including the limits that matter: the shelf is licensed to play in the app, and a book you add has to be yours to use.",
    is_not="""
<p>Cast performs a book with a narrator and a voice for each character, made
on your phone with synthetic voices. You can play the Carrier Press shelf or
add EPUB files of your own.</p>

<p><strong>The shelf is licensed for playback in the app, and that is
all.</strong> Buying a book here does not transfer any right in it. You may
not record, capture, redistribute, publish or make any further copy of a
performance, and it creates no audiobook edition: there is no file to keep,
and nothing produced here may be sold or uploaded anywhere.</p>

<p><strong>A book you add has to be one you have the right to use this
way.</strong> You are responsible for that, and adding a file you do not hold
the rights to is a breach of these terms. The voices are synthetic and are
not the voice of any real person, living or dead. Every card says how fully a
title is cast, and a less fully cast book is a disclosure rather than a
defect.</p>
""",
    paying="""<h2>Paying for it</h2>

<p>Cast is {price}, through the App Store. <strong>Those are two different
purchases and only one of them renews.</strong> A shelf book is bought once,
for that book, and does not recur. Playing your own added EPUB files is an
auto-renewing monthly subscription. The opening of every shelf book, and the
first chapter of every book you add, plays free either way.</p>

<p>The subscription renews automatically at the end of each month, and Apple
charges your Apple Account within 24 hours of the end of the current period
unless you cancel at least 24 hours before it ends. Cancel in Settings on your
device, under your Apple Account, then Subscriptions. We cannot cancel it for
you and we cannot see or change your billing. Cancelling stops the next
renewal and does not take away a shelf book you have already bought.</p>

<p>The price shown in the App Store when you buy is the one that applies.
Apple takes the payment and Apple handles refunds, under its own policy, at
<a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>. We
cannot issue a refund for an App Store purchase. What a purchase buys is a
licence to play, as set out above, and never a file or an audiobook
edition.</p>
""",
)

APPS["conceptionzodiac"] = dict(
    name="Conception Zodiac",
    summary="The terms for Conception Zodiac, including the limit that matters: it is entertainment and arithmetic, and it is not a fertility or medical tool.",
    is_not="""
<p>Conception Zodiac works back from a birthday to the sign that was overhead
at conception rather than at birth, and shows the weeks that would settle it.
It is a pure calculation with no account, no database and no network call,
and the list never leaves the phone.</p>

<p><strong>It is entertainment.</strong> Astrology is not science, and
nothing here describes, predicts or explains any person, their health or
their character. The calculation is arithmetic on a date you typed.</p>

<p><strong>It is not a fertility tool, a conception date, a due date
calculator or anything medical.</strong> It works from a typical gestation to
a range of dates, which is why it shows you the weeks that could change the
answer. Do not use it to establish when a conception happened, to plan or
avoid a pregnancy, or for any legal or medical purpose. A real conception
date is a clinical question.</p>
""",
)

APPS["downpour"] = dict(
    name="Downpour",
    summary="The terms for Downpour, including what the one-time purchase buys: rain made live in the browser for a tabletop game.",
    is_not="""
<p>Downpour makes rain for tabletop game masters: on a tavern roof, over a
camp, rolling in as the boss fight starts. Every drop is generated live in
your browser. Nine surfaces, three layerable at once, six ready scenes, and
Night Arcs that change the rain over time. The Tent plays free for ten
minutes at a stretch, as often as you like.</p>

<p><strong>It is an audio toy for a game table, and it is not a sleep,
relaxation, therapeutic or medical product.</strong> It makes no claim about
focus, sleep or wellbeing.</p>

<p>It plays in a browser, so it needs the browser tab open and awake, and
how it sounds depends on your device, your speakers and your browser. Protect
your hearing: it can be played loud, and sustained volume through headphones
can damage it. There is no file to download, nothing produced here may be
redistributed as an audio release, and the purchase is a licence to play it
rather than a transfer of anything.</p>
""",
)

APPS["fluenthour"] = dict(
    name="Fluent Hour",
    summary="The terms for Fluent Hour, including the limit that matters: it is ten minutes of practice a day, not a course and not a certification.",
    is_not="""
<p>Fluent Hour is one spoken scenario a day, about ten minutes. No lessons,
no streaks, no gems and no owl. Seven scenarios are free, one a day, the same
as the paid tier.</p>

<p><strong>It is not a course, a school, a qualification or a
certification.</strong> Nothing here is accredited, nothing it produces is
recognised by any institution or employer, and it does not assess your level
in a way anybody else is obliged to accept.</p>

<p>The scenarios and the corrections are generated, which means a correction
can be wrong, idiomatic for one region and odd in another, or confident about
a rule that does not exist. An empty Corrections list is not a lack of
feedback. Where accuracy matters, for an exam, a visa or a job, use a human
teacher or an official test.</p>
""",
)

# ── Sanity check ───────────────────────────────────────────────────────────
# A slug here with no privacy page beside it is a slug that is wrong, and a
# typo would otherwise show up as a terms page sitting at a URL nothing links
# to. make_terms.py checks the other direction, that every app with a privacy
# page has an entry here, so between the two neither list can drift silently.

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for slug in sorted(APPS):
        assert os.path.exists(os.path.join(here, slug, "privacy", "index.html")), slug
    print(f"{len(APPS)} entries, every slug has a privacy page beside it")
