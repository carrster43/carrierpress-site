"""
The sale copy of the 7 paywalled web apps (author 2026-11-05: no free access).
Laid over apps_data rather than edited into it, so the App Store wording stays
on record and one import brings the old pages back. Facts only; no refund or
guarantee is promised, because none is published.
"""

KEY_LINE = ("Your license key is on the Gumroad receipt email. Paste it on this page once in each browser you use.")
DATA_KEY = ("Your license key goes to a small key-checking server of ours on Cloudflare, which asks Gumroad about it "
            "and stores nothing. The key is then kept in an encrypted cookie in your browser and in the app's own "
            "storage there, so the page can check it again about once a day.")

COPY = {
    "endorsed": {
        "tag": "Runs in a browser: a subscription that renews until you cancel, or one payment of $29.99 with nothing to renew. The iPhone app is not out yet.",
        "note": "19 packs and 828 practice questions, from the CDL general test, air brakes and combination vehicles through HazMat, drone, pilot, captain, rail and FEMA. Every answer names its source: the federal rule, the FEMA course text, or your state's law or manual where the state sets it. Every pack was checked item by item by a reviewer who did not write it. Nothing is copied from a state manual.",
        "seo_desc": "Free CDL practice test questions in your browser: 828 across 19 packs, from general knowledge to HazMat, with the source named under every answer.",
        "faq": {
            "Is there a free CDL practice test?": ("Can I see it before I pay?", "Yes, on this page: three real questions from the General Knowledge pack, with their sources, and screens from the app. The app itself opens only with a key. You see the price, the renewal and how to cancel before you subscribe, and the checkout is on Gumroad, so your card details never reach Endorsed."),
            "What does Endorsed cost?": (None, "$4.99 a month or $49.99 a year, sold through Gumroad, renewing until you cancel, or $29.99 once with nothing to renew. Either one opens every pack, including packs added later. " + KEY_LINE),
            "Can I practise the pre-trip inspection?": (None, "Yes. The CDL packs have a pre-trip examiner: you say each item out loud, as you would to an examiner, and tick it off."),
            "Do I need an account or an app download?": (None, "No account and no download. Endorsed opens in a browser once you paste your key. Your progress is kept in the browser you study in, not on a server, so it does not follow you to another browser or device."),
            "How do I cancel?": (None, "Cancel from your Gumroad library. Cancelling does not close the packs straight away: you keep them for the days you have already paid for. After that the packs close, and your progress stays in that browser. A one-time key has nothing to cancel."),
            "Can I try it before I pay anything?": None,
        },
    },
    "boatready": {
        "tag": "Renews each month or year until you cancel.",
        "note": "The subscription opens all of it: the carriage list for your exact boat, reading lights and marks, safety advisories, the boats you look after, ticking items off as you go, Practice for lights and marks, and forecasts, tides and currents.",
        "seo_desc": "A boat safety checklist for your exact boat: the federal carriage requirements, with the CFR citation behind every line. Free to check, no account.",
        "faq": {
            "What is free and what does the subscription cost?": ("What does it cost?", "On the web, $4.99 a month or $49.99 a year. That opens the whole app: the list for your boat, reading lights and marks, safety advisories, saved boats, ticking items off, Practice, and forecasts, tides and currents."),
            "Do I need an account or a download?": (None, "No. It opens in your browser once you paste your key, with no account, and the list for your boat is worked out in the browser, so nothing about your boat is uploaded."),
            "Can I try it before paying?": ("Can I see it before paying?", "Yes, on this page: the full list for one example boat, with its rules, and screens from the app. The app itself opens only with a key, and there is no timed trial on the web."),
            "What exactly am I charged, and does it renew?": (None, "On the web, $4.99 a month or $49.99 a year, whichever you pick on Gumroad's page. Gumroad takes the payment, so your card never reaches Boat Ready, and it renews each month or year until you cancel. " + KEY_LINE),
            "How do I cancel, and what happens then?": (None, "Cancel in your Gumroad library, gumroad.com/library. What you paid for stays open until that month or year runs out. Then My boats, Practice and the paid part of Conditions lock in that browser, and the boats you saved stay there, where you can still see them. A new browser needs an active subscription."),
            "What if a renewal payment fails, or I am offshore?": (None, "The page checks your key with Gumroad about once a day. If a renewal has failed, the paid parts lock until you sort it out at Gumroad; your boats are not touched. If Gumroad cannot be reached, the app stays open for up to 7 days after it last said yes."),
            "Where does my data go?": (None, "Your boats stay in your browser, and there is no account. " + DATA_KEY + " Conditions asks NOAA for the stations you chose and never sends your position. The privacy page, linked at the foot of this page, has the full list."),
        },
    },
    # Who Serves (2026-11-22, author: "Who Serves and Zodiac ... all free, but
    # they got to watch the ad videos"): FREE on the web with a small ad below
    # the results; the subscription, an earlier subscriber's key or the Apps
    # tier of Access only turns the ads off. Checked against HomeRule
    # lib/entitlement.ts (every feature open on the web), lib/ads.ts and
    # components/AdSlot.web.tsx (not personalised, /__gate/status first, a live
    # key never loads Google's script) and AppGate 706bc1c (freeApp, the data
    # feeds open). Not claimed: that ads are live or not.
    "whoserves": {
        "tag": "Free to use, and a promo for Carrier Press books and apps may show below the results. The subscription turns the promos off for $2.99 a month or $39.99 a year and renews until you cancel.",
        "note": "The subscription turns the promos off, and that is all it changes: every tool is free in your browser. Enter your key once on this page in each browser you use. A Carrier Press Access key on the Apps or All Access tier turns the promos off too.",
        "seo_desc": "Type a US address and see every government with authority there and who holds each office, with a source and check date on each name. Free, no account.",
        "faq": {
            "Who makes Who Serves, and does it take a political side?": (None, "Carrier Labs LLC, with no investors. The web version is free, and a promo for Carrier Press books and apps may show below the results. It is not a government service and not affiliated with any agency, party or campaign. There is no rating, score, grade or endorsement of anyone, and none will be added, and no promo is placed inside the record itself. It shows the record and leaves the judging to you."),
            "What is free?": (None, "In your browser, everything: any US address, every government, office and officeholder, every source and check date, your election dates, up to eight saved addresses, what changed since you last looked, recent votes and filings for your members of Congress, a letter addressed to any officeholder, and the sourced record to share. In Volusia County, Florida, it also shows who issues building permits at the address and a checklist for a re-roof, fence, shed or pool permit, every line linked to the county, city or state page it came from, with the date it was read. No account. A promo for Carrier Press books and apps may show below the results."),
            "Exactly what is charged, and does it renew?": ("Is anything charged?", "Nothing, to use it. To turn the promos off: $2.99 a month or $39.99 a year, whichever you pick at Gumroad's checkout. Gumroad takes the payment, and it renews automatically until you cancel. " + KEY_LINE + " It turns the promos off in browsers, not in the iPhone app."),
            "How do I cancel, and what happens after?": (None, "Cancel any time from your Gumroad receipt or library. The ads stay off for the time you already paid for, then come back once Gumroad reports the subscription ended. A failed renewal payment brings them back the same way. Everything else keeps working, and the addresses you saved stay in that browser."),
            "What happens to my address?": (None, "It goes to the US Census Bureau's geocoder to find your districts, and nowhere else: not to us, and not to Google with the ad request. Nothing you look up is kept. If you save an address, it stays in your own browser until you delete it. There is no account. Without a key, the page loads Google's ad script, which sees the page address and your browser's details; the ads are not personalised. " + DATA_KEY + " The privacy policy has the details."),
        },
    },
    # Flare, Books for One and Quiet (2026-11-15): on sale on the web first,
    # with nothing free there. The App Store wording stays in apps_data.
    "flare": {
        "tag": "A subscription that runs in a browser, renewing until you cancel. The iPhone app is not out yet.",
        # 2026-11-22: the Record section (Flare, gate 526f6c0): documents read into
        # dated lines with their quotes, checked by the person, kept in the browser.
        # 2026-11-17: the sections from the merge (Flare b13c911). Perimeter's
        # founding key opens Flare too (AppGate 838f35a), so its buyers are told.
        "note": "Log symptoms, flares, sleep, food and period in a minute a day. Pattern analysis, up to 5 a day, looks across your entries and shows what tends to happen together, and the summary prints for your doctor. When you start, you choose what you are tracking. Perimenopause has 36 symptoms in five groups, your cycle pattern, and a script of what to say at the appointment beside the report. Doses, for a GLP-1 medicine, logs each dose and the day it stepped up, your weight and seven common side effects, and counts how often each came up in the weeks after each step up. Today sets the week before a change beside the week after it, for a dose step or any change you mark. Record puts your own paperwork in one place: add a photo, PDF or pasted text of a visit summary, lab report, discharge paper or medication list, and it lists what the document says, line by line, with the words each line came from. You check each line against your original and keep what is right. What you keep becomes one dated timeline and a one-page summary of medicines, allergies, conditions and recent results to hand a new doctor. Up to 30 documents a day. Flare does not diagnose, explain or treat anything, Record does not say what any result means, and it is not a medical device.",
        "limits": "Your log stays in the browser you use and is not stored on our server, so download a copy now and then from Account. Your entries are sent only when you ask for patterns or for an appointment script, which also sends the cycle pattern you chose, and nothing is kept afterwards. A document you add to Record is sent to be read, the reading comes back to your browser, and nothing is kept on our side; your original and your record stay in the browser. Bought Founding access? Your key already opens Flare for its first year.",
    },
    "soleledger": {
        "tag": "A subscription that runs in a browser, renewing until you cancel. The iPhone app is not out yet.",
        # 2026-11-17: Rentals, from Doorstop (SoleLedger 03c1479), included in
        # every key (author 2026-11-17). The web reader does not yet read a
        # rental document onto a Schedule E line (AppGate change pending), so
        # nothing here says a lease or a rental receipt is read.
        "note": "Income, deductions, quarterly payments and 1099s for one self-employed person. Add a receipt or a 1099 as a photo or PDF and it fills in the entry. Enter the estimated tax you plan to pay this year and it splits it across the four federal due dates and tracks what you have paid. Rentals comes with every key: your units, the lease on each, each unit's year on its numbered Schedule E lines, a question rather than a guess where a cost might be an improvement instead of a repair, and Schedule E working papers for each unit. Rental entries stay out of your Schedule C totals. It never applies a tax rule to you, and it is not tax advice.",
        "limits": "Your books stay in the browser you use, with a backup file you can download and restore. A document is read and then discarded, so keep your original. Reminders on the web are a calendar file, not emails. Bought Founding access? Your key already opens it for its first year.",
    },
    "quiet": {
        "tag": "One payment. It does not renew. The iPhone app is not out yet.",
        "note": "Notes, photos and voice memos, found again the way you remember them: by a word, a day, or the kind of entry. No account, no sync and no server: what you write is not sent anywhere. Export everything as a zip whenever you like, and restore it into any browser.",
        "limits": "Your journal lives in the browser you use, so keep an export. Quiet opens in one tab at a time. Private or incognito windows forget everything when they close.",
    },
    # Titrate (2026-11-15): on sale on the web first, nothing free there.
    "titrate": {
        "tag": "A subscription that runs in a browser, renewing until you cancel. The iPhone app is not out yet.",
        "note": "Record each dose your prescriber sets, log side effects in a few taps, and weigh in. Titrate counts how often you noted each side effect in the first and second week after each dose increase, and sizes general protein and fibre targets to your weight. It never suggests a dose, never says whether a symptom is serious, and never interprets your weight: after every symptom it says the same thing, that your prescriber wants to know. Flare also has a Doses section, for anyone who wants doses beside a wider symptom log.",
        "limits": "Your record stays in the browser you use and is not stored on our server, so download a copy now and then from the You tab; Restore from a copy puts one back. Nothing you log is sent anywhere. Not a medical device, and not medical advice. Bought Founding access? Your key already opens Titrate for its first year.",
    },
    # Doorstop (2026-11-16): on sale on the web first, nothing free there. Every
    # claim checked against Doorstop's code (lib/entries.ts, lib/ledger.ts,
    # lib/scheduleE.ts, lib/localStore.ts; AppGate src/ai/doorstop.js).
    "doorstop": {
        "tag": "A subscription that runs in a browser, renewing until you cancel. The iPhone app is not out yet.",
        "note": "For a landlord with one to six units. Add a receipt, an invoice, a lease or a mortgage statement as a photo or PDF and it reads the date, the amount and the Schedule E line a cost of that kind usually goes on; rent and anything else you type by hand. Where a cost might be an improvement rather than a repair, it asks you instead of guessing, and keeps it out of the totals until you answer. At the end of the year it exports plain working papers, unit by unit, for whoever files your return. It does not calculate depreciation, it does not file, and it is not tax advice. Books for One also has a Rentals section, for a freelancer who also lets property.",
        "limits": "Your ledger stays in the browser you use and is not stored on our server, so download a copy now and then from Account; Restore from a copy puts one back. A document is read and then discarded, so keep your original, and up to 40 can be read a day. Bought Founding access? Your key already opens Doorstop for its first year.",
    },
    # Threshold (2026-11-15): on sale on the web first, nothing free there.
    "threshold": {
        "tag": "One payment per child. It does not renew. The iPhone app is not out yet.",
        "note": "Add a child and their age, pick what they have, and Threshold lists every control that applies, most important first: the birthday on the account before anything else, because most other settings are worked out from it. Each control has its steps, why it matters, the platform's own instructions and the date the steps were last checked against them. When a platform changes a control you already set up, it shows under Changes. For a child of 13 to 17, the Agreement follows once the setup is done, at no extra charge: rules you and your teenager suggest, check-ins either of you writes, and freedoms that loosen on a date you both can see. Nothing is in force until both of you say yes, either of you can drop a rule or end the agreement, and your teenager sees everything you see.",
        "limits": "Threshold records what you tell it you have done. It cannot see your child's devices or confirm any setting is on, and nothing here is a guarantee that a child is safe online. Your record stays in the browser you use, so download a copy now and then from Account. Bought Founding access? Your key already opens Threshold for every child, for good.",
    },
    # Paper Trail (2026-11-16): on sale on the web first, nothing free there. Every
    # claim checked against Paper Trail's code (lib/alerts.ts, lib/calendar.ts,
    # lib/localStore.ts, lib/scans.web.ts, lib/data.web.ts; AppGate
    # src/ai/papertrail.js).
    "papertrail": {
        "tag": "A subscription that runs in a browser, renewing until you cancel. The iPhone app is not out yet.",
        "note": "Add a receipt, a warranty or an insurance policy as a photo or PDF, or paste a confirmation email, and it reads the vendor, the amount and the date that matters: when cover ends, when a policy renews and charges you, or the last day to return something. Coming up lists them soonest first, saying what happens on each day. Where it could not read a date clearly it asks you to confirm it rather than remind you about a guess. Anything it read but could not place, such as an exclusion, is shown to you, not dropped. The Home section keeps the house's equipment and its recurring jobs beside the documents they came from, puts them in the same list under What runs out next, and makes a service record to hand over when you sell.",
        "limits": "A browser cannot remind you by itself and there is no email on the web, so Paper Trail puts each date in your own calendar, as an all-day event on the day to act. Your drawer and the scans stay in the browser you use and are not stored on our server, so download a copy now and then from Account; Restore from a copy puts one back. Up to 40 documents can be read a day. It can misread a date: check the document before you act. Bought Founding access? Your key already opens Paper Trail for its first year.",
    },
    # Through the Gate (2026-11-17): on sale on the web first, nothing free there.
    # Every claim checked against Through the Gate's code (lib/links.ts
    # PARSER_NOTE, components/ParseView.tsx, app/(tabs)/applications.tsx
    # GHOST_AFTER_DAYS, lib/localStore.ts) and AppGate src/ai/throughthegate.js
    # (DAILY_CAP 20, 200 characters minimum).
    "throughthegate": {
        "tag": "Runs in a browser: a monthly subscription that renews until you cancel, or a 90-day pass paid once. The iPhone app is not out yet.",
        "note": "Paste the text of your resume and see the record a competent general resume parser builds from it: the fields it kept, the job titles it renamed with your own wording beside them, and every piece that did not survive, each with the plain reason it was lost. It flags what is worth knowing, such as a date with no month or a gap, and says what to change where there is something to change. Parse as many versions as you like and compare them. The Applications tab tracks where you applied, and marks one with no reply in a month.",
        "limits": "It shows how a competent general parser reads your resume. It is not any one employer's system and it does not predict whether you will be screened in or out. Your resumes and applications stay in the browser you use and are not stored on our server, so download a copy now and then from Account; Restore from a copy puts one back. Up to 20 resumes can be parsed a day. A 90-day pass stops parsing new versions after 90 days, and what you saved stays readable in that browser. Bought Founding access? Your key already opens Through the Gate for its first year.",
    },
    # Vet Pocket (2026-11-17): on sale on the web first, nothing free there. Every
    # claim checked against Vet Pocket's code (supabase/functions/triage/
    # prompt.mjs SYSTEM and HARD_ESCALATE, lib/triage.ts URGENCY and weightNote,
    # app/(tabs)/due.tsx KINDS, lib/calendar.ts, lib/localStore.ts) and AppGate
    # src/ai/vetpocket.js (DAILY_CAP 10, escalation applied in the gate).
    "vetpocket": {
        "tag": "A subscription that runs in a browser, renewing until you cancel. The iPhone app is not out yet.",
        "note": "Keep each pet's records in one place: species and breed, anything ongoing, weights, and every vaccination, worming and flea treatment with when the next one is due. When something is wrong, describe it in your own words and Vet Pocket answers the 2am question: go now, be seen today, book an appointment, or watch closely, with the questions your vet will ask, the signs that would change the answer, and rough cost ranges for each path. Some things, such as a cat that cannot pass urine, a swollen belly with retching, seizures or a suspected poison, are always treated as go now, whatever else is said.",
        "limits": "Vet Pocket is not a vet and does not diagnose: it points you to your vet instead and never says your pet is fine. If you are worried enough to ask, ringing your vet or an emergency clinic is always right; they triage over the phone for free. Cost ranges are estimates, not quotes. A browser cannot remind you when it is closed, so due dates go into your own calendar with a reminder a week before. Your pets' records stay in the browser you use and are not stored on our server, so download a copy now and then from Account. Up to 10 questions a day. Bought Founding access? Your key already opens Vet Pocket for its first year.",
    },
    # The Binder (2026-11-18): vault + checklist (author 2026-11-18: no staged
    # release). Every claim checked against TheBinder 20c622c: lib/checklist.ts
    # SECTIONS and TOTAL_MINUTES (84), lib/vault.ts (scrypt + XChaCha20-Poly1305,
    # no recovery), lib/localStore.ts and test/web-store.test.ts (nothing readable
    # stored, copy and restore), lib/boundaries.ts NOTHING_RELEASED and NOT_A_WILL,
    # app/_layout.web.tsx (reload or two minutes hidden locks it). No AI.
    "thebinder": {
        "tag": "$99 once, yours for good, with nothing to renew. It runs in a browser. The iPhone app is not out yet.",
        "note": "The file your family will need and almost nobody has: where the will is, which accounts exist, who to ring, and what you want to happen. Nine short sections with concrete questions and examples, under an hour and a half in all, and a clear end. Everything is encrypted in your browser with a passphrase only you know, and is never sent to us or anyone else. Download a printable plain-text copy to keep with the will, and an encrypted copy to move to another browser.",
        "limits": "Nothing in The Binder is ever released to anyone automatically. It does not watch for a death, it holds no list of people to send it to, and nobody learns it exists unless you tell them, so tell one person you trust where the Binder is and where the passphrase is written down. If you forget the passphrase, the binder cannot be opened, by you or by us. It is a list of where things are, not a will, a trust or an advance directive. It lives in the browser you use, and browsers delete what websites save: Safari does it after about a week away from the page. So the encrypted copy you download is the real backup, and the app offers it each time you finish a section.",
    },
    # FirstDay (2026-11-18): on sale on the web first, nothing free there. Every
    # claim checked against FirstDay f42e35a (lib/deadlines.ts CONFIDENCE_FLOOR
    # and explodeRecord, app/(tabs)/coming.tsx, add.tsx "Read but not filed",
    # supplies.tsx, lib/calendar.ts calendarDeadlines and alarmLead,
    # lib/localStore.ts) and AppGate src/ai/firstday.js (DAILY_CAP 25) and
    # src/license.js passEnd (the school-year pass).
    # Homeroom (2026-11-19): on sale on the web first, nothing free there. Every
    # claim checked against Homeroom 10589c1 (lib/states.ts STATES rechecked
    # 2026-11-19, lib/links.ts RULES_NOTE and ATTENDANCE_NOTE, lib/localStore.ts,
    # lib/data.web.ts and lib/gate.ts paused writes, lib/calendar.ts, the
    # transcript download) and AppGate 64e582e (pass until 2027-06-30, status
    # lapsed).
    "homeroom": {
        "tag": "A subscription or a school-year pass, in a browser. The iPhone app is not out yet.",
        "note": "Pick your state and Homeroom lays out the year's requirements at once, each with the statute it comes from and the date it was last checked: Texas, Florida, North Carolina, California, Ohio, Georgia, Pennsylvania, New York, Michigan and Illinois. Log attendance by the day, with hours where your state counts them, one record per child per day, so a correction never counts twice. Keep a portfolio of work samples by subject and date, each with a photo or a PDF, and a reading log. Tick each requirement as you meet it, put the ones with a month into your own calendar, and download a transcript you issue from the courses you enter.",
        "limits": "Homeroom sums up state homeschool law for a parent. It is not legal advice, the law changes, and the statute, read with your state's department of education guidance, is the authority; every rule shows its citation and the date Homeroom last checked it. Homeroom counts what you record and cannot tell you whether your district will accept it. Your records and photos stay in the browser you use and are not stored on our server, so download a copy now and then from Account. When a subscription ends, or the school-year pass after June 30, 2027, everything stays readable and downloadable in that browser and new entries pause.",
    },
    # Stuck (2026-11-20): on sale on the web first, nothing free there. Every
    # claim checked against Stuck b59e3c1 (lib/localStore.ts gateBody and
    # takeTurn, lib/outcome.ts, the session, transcript and Account screens,
    # several children on the web) and AppGate 611ec62 (src/ai/stuck.js: the
    # tutor's prompt, the four-field schema, DAILY_CAP 30, no name accepted).
    "stuck": {
        "tag": "A subscription, in a browser. The iPhone app is not out yet.",
        "note": "Your child types the homework problem they are stuck on, in their own words, and Stuck asks the next question, one at a time, until they get there themselves. It will not give the answer or any step of it to their own problem, including when told the work is already handed in, and it can explain the idea behind a method. Each reply is meant to be a single question. It can slip, which is why every session is there for you to read. It never scolds and never mentions cheating; it just keeps tutoring. You can read every session: the problem as typed, what they were stuck on, what got them unstuck, and how many times they asked outright for the answer. Kindergarten to grade 12, and as many children as you add, each a first name and a grade.",
        "limits": "Stuck is homework help, not a substitute for a teacher. Your child needs no account and no email, and their name never leaves your browser: the grade, the subject, the problem and the conversation go through our server to Anthropic, which writes the next question, and nothing is stored on our server. Sessions and the answer-request counts stay in the browser you use, so download a copy now and then from Account. Up to 30 turns a day. When a subscription ends, past sessions stay readable in that browser and new problems pause.",
    },
    # PillProof (2026-11-20): on sale on the web first, nothing free there. A
    # log with no health claims (author 2026-11-20). Every claim checked
    # against PillProof ae178d7 (lib/localStore.ts, lib/familySummary.ts,
    # lib/lapse.ts, lib/data.web.ts and the five .web screens) and AppGate
    # 30f0473 (no AI; never closes on lapse).
    "pillproof": {
        "tag": "A subscription, in a browser. The iPhone app is not out yet.",
        "note": "Add the person you look after, then their medicines exactly as the box says, with the times and days each is taken and, if you like, a photo of each tablet so whoever gives it can see what it looks like. Today lists each dose as it falls due. Mark it taken or skipped, with the reason, and PillProof keeps the time and the name of whoever recorded it, such as 8:04am, Cal; a slip can be undone. Updates are typed as health, how they are, or day to day, and one that needs doing can be marked done with the name of who did it. Appointments say what, when, where and who is taking them. Look after more than one person from the same browser. For the rest of the family there is a summary to download or print: the medicines as typed, the last seven days as recorded, what still needs doing and what is coming up.",
        "limits": "PillProof records what was marked as taken, by whom and when. It does not check interactions, does not advise on doses, and is not a medical device: if something in it looks wrong, the box and the pharmacist are right. It sends no reminders. Everything stays in the browser you use and is not stored on our server, so the Updates feed is not shared live: the family see what you send them. Download a copy now and then from Account. When a subscription ends, today's list stays and doses can still be marked taken or skipped; anything else that pauses says so in one line.",
    },
    # Handoff (2026-11-20, HELD): the shared record is held by the gate, one
    # per arrangement (author "A, creator covers, ship at my risk"). Every
    # claim checked against Handoff 3bbd297 (lib/handoff.ts, lib/webRecord.ts,
    # the four .web screens) and AppGate f23bb86 (src/handoff/): no owner, no
    # edit or delete, only the other parent answers an expense, answers freeze,
    # only agreed expenses count, export takes a date range and nothing else,
    # 300 writes a UTC day per arrangement, receipts not kept on the web.
    # Never "safe", never "case", never "you owe".
    "handoff": {
        "tag": "A subscription per parent, in a browser. The parent you invite joins free. The iPhone app is not out yet.",
        "note": "Start an arrangement with your key, then send the other parent an invite link. They join free, with no key, no account and no email address, and they read and add to the record at no cost. Messages go into a permanent record that neither of you can edit or delete, and each carries a cryptographic hash of the one before it, so a removed or altered message shows. Expenses carry the share asked of the other parent; only the other parent can agree, the amount is fixed once they answer, and only agreed expenses count toward one netted figure of what is outstanding. A calendar says which parent has each child on each day, with a reason when the usual pattern changes. Export the whole record for any period as a text file to keep, print or hand over: every message in the period, never a selection, what it does and does not prove, and the data anyone can check at carrierpress.com/handoff/verify/. Export needs a key of your own.",
        "limits": "Handoff does not judge who is right, sends no read receipts and gives no legal advice. It is not a substitute for a lawyer or for anything a court has ordered you to use. The record is held on our server, one per arrangement, so both of you see the same one, and nobody can remove the other parent or delete anything in it. Receipt photos are not kept on the web. An arrangement takes up to 300 additions a day. If a subscription ends, both of you can still read and add to the record; export pauses until a key is current again.",
    },
    # Crosscheck (2026-11-21): FREE to open (author, "One key = one case"): the
    # comparison and every finding cost nothing, a key drafts the letters for one
    # case. Every claim checked against Crosscheck lib/detect.ts (the five
    # finding kinds, "arithmetic" or "worth_asking"), lib/letter.ts (three
    # letters, facts, questions and requests only, assertNoLegalClaims, the
    # user's reason quoted untouched), lib/caseKey.ts (one gate call per case,
    # key and random case id only), lib/localStore.ts and lib/data.web.ts
    # (browser storage, copy, print, download, erase), and AppGate 2a027e8
    # (src/crosscheck.js: quantity = cases, Apps-tier Access opens any case).
    # Not a subscription: no trial line, no renewal line. No "appeal", no
    # photographs, no out-of-network or coding claims, no outcome promised.
    "crosscheck": {
        "tag": "One payment per case, never a subscription. Every finding is free; a key drafts the letters.",
        "note": "One key drafts the letters for one case, up to three of them: a query to the billing office naming the exact figures, a request for a fully itemised statement, and a letter asking your insurer to look at the claim again. Every sentence Crosscheck writes is a figure from your documents, a question or a request, never a legal claim or a threat. Your own reason goes in exactly as you wrote it. Copy, print or download each letter and send it yourself: Crosscheck sends nothing. Another bill needs another key, and you can choose how many cases at checkout. A Carrier Press Access key on the Apps or All Access tier drafts the letters for any case.",
        "limits": "Crosscheck compares the figures you type. It does not review coding, so it makes no upcoding, unbundling or medical-necessity judgement, and it does not predict how a billing office or insurer will answer. It is not legal or medical advice. It runs in your browser with no account, and nothing you type is uploaded: your cases stay in that browser, so download a copy now and then from Account. A key is used on a case the first time it opens that case's letters, so open them on the bill you want letters for.",
    },
    # Spellbright (2026-11-22): FREE to play with ads, or $2.99 a month with no
    # ads (author). The membership changes one thing, the ads; every mode is
    # free. Every claim checked against Spellbright 356216d: lib/ads.ts (the
    # eight breaks, none in the first 2 minutes, never two within 3, the child
    # tags), lib/adBreak.ts (requestNonPersonalizedAds, /__gate/status first, a
    # live key never loads Google's script, a lapse brings ads back),
    # lib/speech.ts and lib/voice.ts (recorded clips from the clue book, then
    # the browser's best voice), lib/profile.ts, lib/spellingStore.ts and
    # lib/adventureStore.ts (browser storage only), app/silly.tsx ("Never with
    # strangers"), and AppGate 2bf544a. Not claimed: that ads are live or not.
    "spellbright": {
        "tag": "Free to play, with a short promo for Carrier Press books and apps now and then between games. The membership turns the promos off and renews each month until you cancel.",
        "note": "The membership turns the promos off, and that is all it changes: every mode, every age and every kind of help is the same as in the free game. Enter your key once on Spellbright's page in each browser your family uses. A Carrier Press Access key on the Apps or All Access tier turns the promos off too.",
        # Spelling groups (author 2026-11-23, "Yes, $39.99", then "Yes, go live").
        # Checked against Spellbright cfb87a4 (lib/group.ts, lib/groupApi.ts,
        # app/join.tsx, app/groups.tsx: refreshGroup every 10 minutes at most) and
        # AppGate b818f00/f4a5d63 (src/spellbright/: 6 groups, 30 words, 8-character
        # codes, joinedThisWeek the only number a grown-up sees, lapse keeps words).
        # Gumroad /l/spellbrightgroups (zVMbTHq2nuqMbSHMScDM0A==, edit turdpl),
        # published by Jeffrey 2026-11-23.
        "groups": {
            "title": "Spelling groups for classrooms and homeschool families",
            "lede": "Type this week's spelling words once, and every child has them.",
            "paras": [
                "With a group plan, a teacher, homeschool parent or tutor makes a group, shares its short code and types the week's words. Each child types the code in Spellbright, and the words are waiting in Practise, Mystery Word, Word Search, Crossword and What's the Word?, with no promos for as long as the plan is active.",
            ],
            "points": [
                "Up to 6 groups: a whole class, its reading groups, or each child at home at their own level, with up to 30 words each.",
                "Change the words any time, or let Spellbright pick a set for an age. Each child's Spellbright picks them up on its own.",
                "Leave the group a note, like \"Test on Friday, you've got this!\", and see the cheers children send back after they practise.",
                "Send the code from your own phone or email in one tap, or print a page of cut-out code slips. A family tablet can keep several groups.",
                "No student accounts, no names, no emails. A child types only the code, and their practice stays on their own device. You see how many devices joined this week, never who or how they did.",
                "$39.99 a year for the whole plan, renewing until you cancel in your Gumroad library. If it ends, the groups and the words already on each device stay; changing words and promo-free play wait until you renew.",
            ],
            "buy": "https://jeffreycarrier.gumroad.com/l/spellbrightgroups",
            "buy_label": "Get the group plan",
            "buy_note": "$39.99 a year, renews until you cancel, license key by email",
            "open": "/spellbright/app/groups",
            "open_label": "Open Spelling groups",
            "open_note": "Already have a group plan key? It goes in Spellbright itself, not in the box above.",
        },
        "limits": "An ad shows only at a natural break, after a finished puzzle, round or game: never during a turn, never in front of Help, never in spelling practice and never on a grown-ups screen. None shows in the first two minutes, and never two within three minutes. Every ad request is marked for a child and asks for ads that are not personalised. With a live key, the game never loads Google's ad script. There is no account and no chat, and nobody is matched with strangers: children play the robots or people on the same device. The age picked, the spelling list and the adventure map stay in that browser. Words and their meanings are read aloud in a natural recorded voice, and anything without a recording is read by the best voice your browser has.",
    },
    # Bench (2026-11-22). Every claim checked against Bench e82f4f4
    # (gate/bench-desks.mjs author desk, lib/flags.ts, lib/history.ts,
    # test/shell.test.ts no-send) and AppGate 06abd4b (src/ai/bench.js,
    # dailyCap 10 per desk). No credits, votes or other desks claimed.
    # 2026-11-23: the Errands desk added (Bench 1eda159, AppGate ca21234).
    "bench": {
        "tag": "A subscription, in a browser. One key opens the Author desk and the Errands desk.",
        "note": "The Author desk, run by Jeffrey Carrier of Carrier Press from the craft notes behind his own editions: a listing package (a book description, a subtitle check, seven KDP keywords, three Amazon store categories for KDP and BISAC subjects for IngramSpark, which take different lists), front and back matter (copyright page, title page, About the Author short and long, Also By, the call to your next book), back-cover copy sized to your trim with a tagline and A+ module copy, and pitch emails for a library or an independent bookstore. Every draft is checked by rules you can see: a best-seller or award claim your material does not make, an ISBN or a price you did not type, a placeholder left in, praise that is not word for word, keywords that do not fit KDP. The Errands desk: write down the errand you have been putting off and it plans it in steps (what to find out and where to check it, options side by side, the message ready to send, the form answers to paste) and ends with the one thing you do yourself. A drafted message can only go to an address you typed, and opens unsent in your own mail app. A plan with any step that would act for you is thrown away whole, and you are shown why.",
        "limits": "Bench drafts and plans. It never sends, posts, files, books or pays for anything, and it does not browse the web, so a plan says where to check things rather than claiming it looked them up, and any web address it writes that you did not give is flagged. What you type goes through our server to Anthropic, which writes the draft, and nothing is stored on our server. Your past work stays in the browser you use, so download a copy now and then. Up to 10 runs a day on each desk. When a subscription ends, past work stays readable in that browser and new runs pause. Drafts are written by an AI model: read every word before you use it.",
    },
    # Potluck (2026-11-22, author: "Add a paid unlock"). Every claim checked
    # against Potluck 4fc24f6 (lib/webStreet.ts cardsHtml, flyerHtml,
    # streetCopy; the .web.tsx screens; docs/WEB_API.md) and AppGate 43e0371
    # (src/potluck/: CARD_DAYS 120, WRITES_PER_DAY 1000, auto-hide on harassment
    # and unsafe, no reporter id out, no address column). No October map on the
    # web; never the merged apps' names; nothing called "safe".
    "potluck": {
        "tag": "A membership for the whole street, paid by whoever opens it. Every neighbour joins free. The iPhone app is not out yet.",
        "note": "Your key opens one street. Print a door card for every house: each has its own code, works once and lasts 120 days, and whoever types it is on the street, free, with no account, no email address and no password. Print this week's flyer for the neighbours who will never open an app: what is on, what is on the lending shelf and how to join, with no names on it. Neighbours post happenings, one-off or repeating, say they are coming to the next one, list things to lend and record loans, and you look after the reports. Enter your key once on this page in the browser you use. A Carrier Press Access key on the Apps or All Access tier opens a street too.",
        "limits": "Potluck is for organising things and lending things. It is not a place to report people, and if something is happening now, ring 911. No address is asked for or kept, by us or on a card: which house got which card number is your own note, kept in your browser. The street is held on our server so every neighbour sees the same one. A report of harassment or something unsafe hides a post straight away, and nobody, you included, is told who reported it. There are no notifications: neighbours see what is on when they open it, which is what the flyer is for. If the membership ends, nothing is taken away: the street stays readable, and saying you are coming, returning things, reporting and blocking all still work, while new posts, door cards and the flyer pause until it is renewed. A street takes up to 1,000 changes a day.",
    },
    "firstday": {
        "tag": "A subscription or a school-year pass, in a browser. The iPhone app is not out yet.",
        "note": "Paste the school emails and add the letters and PDFs. FirstDay pulls out every date a parent has to act on, every form and every supply request, and puts them in one list: slips to sign and send back, money owed, things to be at, each with the letter it came from. A slip is tracked as signed and then as sent back. Every date carries its own confidence, and one FirstDay was not sure it read correctly is not scheduled: it waits at the top of the list for you to confirm or dismiss. Anything it read but could not file is shown to you. One supply list covers every letter and every child, and the names you add tell it which child a letter is about.",
        "limits": "FirstDay reads dates out of school mail and can misread one, so a reminder is a prompt to check the letter, not a replacement for reading it. A browser cannot remind you when it is closed, so confirmed dates go into your own calendar with an alarm days ahead. Your children's names and your dates stay in the browser you use and are not stored on our server, so download a copy now and then from Account. Up to 25 letters can be read a day. The school-year pass stops reading new letters after June 30, 2027, and what you saved stays readable in that browser. Bought Founding access? Your key already opens FirstDay for its first year.",
    },
    # Pantry (2026-11-19): on sale on the web first, nothing free there. Every
    # claim checked against Pantry be05e52 (lib/pantry.ts receiptItems,
    # parseQuickAdd, byUrgency, freshnessPhrase; lib/localStore.ts findReceipt,
    # saveSettings, exportAll, restoreAll; app/(tabs)/tonight.tsx) and AppGate
    # src/ai/pantry.js (DAILY_CAP 15, two ideas at most, safety claims removed).
    "pantry": {
        "tag": "A subscription, in a browser. The iPhone app is not out yet.",
        "note": "What is for dinner tonight, from what is already in the house. Type one line, \"chicken thighs fridge 3\" or just \"rice\", or photograph a grocery receipt, choose a PDF, or paste a receipt or an online order email, and Pantry turns the till's abbreviations back into food and guesses how long each thing keeps. Everything sorts soonest first, with the undated things at the bottom rather than hidden. Ask what you can make and you get up to two dinners that use up what goes off first, with the time it takes and what else it assumes you have. Write what you cannot eat once in Account and every idea is told to keep it out, including as a hidden ingredient, and to say so when nothing can be made without it. The same receipt read twice adds nothing twice.",
        "limits": "Dates from a receipt are typical shelf life for that kind of food, not a date read off the packet, so change any of them. Pantry cannot see your kitchen or how anything was stored: check the food, not the app, and read the label of anything bought against what you cannot eat. A browser cannot remind you when it is closed, so the web version sends no reminders. Your pantry stays in the browser you use and is not stored on our server, so download a copy now and then from Account. Up to 15 receipts and dinner ideas a day.",
    },
    # Fluent Hour (2026-11-19): on sale on the web first, nothing free there.
    # Every claim checked against FluentHour 6c732b7 (lib/scenarios.ts,
    # lib/types.ts LANGUAGES, lib/localStore.ts takeTurn and ONE_A_DAY,
    # lib/speech.web.ts rate 0.88 and the type-instead fallback, progress tab)
    # and AppGate src/ai/fluenthour.js (converse's SYSTEM, DAILY_CAP 30, at
    # most one correction, kept only when whole).
    "fluenthour": {
        "tag": "A subscription, in a browser. The iPhone app is not out yet.",
        "note": "One spoken conversation a day with someone patient. Choose Spanish, French, German, Italian, Portuguese or Japanese at your level, pick a situation (a bakery that has run out of what you wanted, a landlord and a heater that has stopped working, a pharmacist when you do not know the word, and three more), and the other person speaks first. You answer out loud. Replies are a sentence or two, read aloud a little slower than normal. At most one correction a turn, and only when a listener would not have understood; the conversation carries on either way, with no praise, no streaks and no points. Every correction is kept on the Corrections tab, with the minutes you spoke.",
        "limits": "Listening uses your browser's own speech recognition. It works in Chrome, Edge and Safari; in Firefox, and wherever the microphone is not allowed, you type what you would say instead. Some browsers send the audio to their maker to turn it into words (Chrome to Google, Safari to Apple); Fluent Hour never receives your voice, only the words. Replies are read aloud by your browser's own voice, so how it sounds depends on your device. The partner reads a transcript and cannot hear you, so it never corrects pronunciation. One new conversation a day, and up to 30 turns a day. Your conversations stay in the browser you use and are not stored on our server, so download a copy now and then from Account.",
    },
    # Trade Desk (2026-11-19): on sale on the web first, nothing free there. Every
    # claim checked against TradeDesk 48e4010 (lib/jobs.ts createJob and
    # raiseInvoice, lib/money.ts total, lib/localInvoices.ts issueInvoice and
    # voidInvoice, components/InvoiceCard.web.tsx, app/(tabs)/account.web.tsx,
    # app/(tabs)/code.web.tsx, app/_layout.web.tsx) and AppGate src/ai/tradedesk.js
    # (DAILY_CAP 25, the citation guarantee and the fixed check sentence).
    # 2026-11-23: the Decisions card and weekly update (TradeDesk be7d0a4,
    # lib/decisions.ts, lib/decisionStore.ts, components/Decisions.web.tsx).
    "tradedesk": {
        "tag": "A subscription, in a browser. The iPhone app is not out yet.",
        "note": "Customers, jobs, quotes and invoices for one person with a van. A job is a title and, if you like, a customer; lines and tax are worked in whole cents, with tax taken once on the taxable lines. Raise the invoice from the job and its amounts are copied, so the invoice you sent stays as sent. Numbers continue your own sequence, and a voided invoice keeps its number. Your payment instructions print on every invoice. Write rough notes and it drafts the scope of work for the customer to sign; when they ask for more, it drafts the change order with the price and the days it adds, or says the request is already in the scope. Ask an electrical code question and the answer cites the NEC article; when it cannot name one, it says so and tells you what to look up. Log each decision on a job as it is made: what was decided, who decided it, how they said it and on what day, against the scope as it stood. A logged decision is never edited, only struck with the reason, so the record holds up if a change is ever argued about. From it, Trade Desk writes the weekly update to your customer: what was decided, what was signed, and what you are still waiting on.",
        "limits": "The web version has no card payment link: your customer pays you the way your invoice says, and you mark the money received. Code answers state requirements in our own words and are not the code text; check them against the edition your jurisdiction adopted, state and local amendments, and your inspector. Every draft is checked by you before it goes to a customer. Up to 25 drafts and code answers a day. Your jobs stay in the browser you use and are not stored on our server, and one tab at a time can have Trade Desk open, so download a copy now and then from Account.",
    },
    "cast": {
        "price": "Books from $14.99 · Your own books $22.99/mo",
        "tag": "A book is one payment and never renews. Your Own Books is a membership with a one-week trial for new members, renewing until you cancel.",
        "note": "84 books on the shelf: 52 Carrier Press originals, the three American Firsts and 29 classics. Series sit together in reading order, and every card says how fully the book is cast. Each purchase is a license to hear that book in full in Cast, not an audio file and not a copy of the book.",
        "limits": "Cast makes its natural voices right in your browser, a different one for the narrator and each character, after one download of about 90 MB. They are computer voices, not recordings of narrators. Until the download finishes, your browser's own voices read, and those vary by browser. Cast needs a connection to open a book. Keep the tab open while you listen, since a browser can pause speech when a phone locks or a tab sleeps. Your place is saved in the browser you use, ready when you come back.",
        "seo_desc": "Hear any book's opening before you buy: a narrator and a voice for each character, in natural voices made in your browser. 84 books, from $14.99 each.",
        "faq": {
            "Can I hear a book before I pay?": ("Can I hear it before I pay?", "Yes. Open Cast and press Play on any book: its opening plays before you pay, usually the first chapter or two, and each card says how long. No account and no email. The lines on this page play in your browser's own voices; inside Cast, its natural voices take over once they are downloaded."),
            "What exactly am I charged?": (None, "A book from the shelf is one payment, from $14.99, with the price on its Gumroad listing. It never renews. Your Own Books, which plays EPUB files you add, is a membership: a one-week trial for new members, then $22.99 a month or $109.99 a year, renewing until you cancel. It does not open the shelf books, and neither is part of Carrier Press Access. Gumroad takes the payment."),
            "How do I cancel the membership?": (None, "In your Gumroad library, before the trial or the period ends. A cancelled membership runs to the end of the period you paid for. When it ends, the books you added stay in that browser and the first chapter of each still plays there."),
            "What happens to files I add?": (None, "An EPUB you add is read inside your browser and never uploaded. Cast keeps the script it makes, in that browser, and not the file. Remove deletes it, and so does clearing the site's data."),
            "Where is my key, and what if I come back later?": ("Coming back to a book?", "Open Cast in the same browser and Continue listening has your latest books, each at your place. Your license key is on the Gumroad receipt email: paste it on this page to open the book it was bought for, and a key for another book goes in under I have a key, inside Cast. There is no account, so your place and your books live in the browser you use. In another browser, or after clearing site data, paste the same key again; your place stays behind in the first browser."),
        },
    },
}


def apply(apps):
    for app in apps:
        copy = COPY.get(app.get("slug"))
        if not copy:
            continue
        for field in ("note", "tag", "price", "limits", "groups"):
            if copy.get(field):
                app[field] = copy[field]
        seo = app.get("seo")
        if seo and copy.get("seo_desc"):
            seo["desc"] = copy["seo_desc"]
        if seo and copy.get("faq"):
            known = {q for q, _ in seo["faq"]}
            missing = set(copy["faq"]) - known
            assert not missing, "FAQ question not found: %s" % missing
            faq = []
            for q, a in seo["faq"]:
                if q in copy["faq"]:
                    change = copy["faq"][q]
                    if change is None:
                        continue
                    faq.append((change[0] or q, change[1]))
                else:
                    faq.append((q, a))
            seo["faq"] = faq
