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
    "cleared": {
        "tag": "Runs in a browser: a subscription that renews until you cancel, or one payment of $29.99 with nothing to renew. The iPhone app is not out yet.",
        "note": "19 packs and 828 practice questions, from the CDL general test, air brakes and combination vehicles through HazMat, drone, pilot, captain, rail and FEMA. Every answer names its source: the federal rule, the FEMA course text, or your state's law or manual where the state sets it. Every pack was checked item by item by a reviewer who did not write it. Nothing is copied from a state manual.",
        "seo_desc": "CDL practice test questions in your browser for $4.99 a month or $29.99 once. 828 questions across 19 packs, from general knowledge to HazMat, with the source named under every answer.",
        "faq": {
            "Is there a free CDL practice test?": ("Can I see it before I pay?", "Yes, on this page: three real questions from the General Knowledge pack, with their sources, and screens from the app. The app itself opens only with a key. You see the price, the renewal and how to cancel before you subscribe, and the checkout is on Gumroad, so your card details never reach Cleared."),
            "What does Cleared cost?": (None, "$4.99 a month or $49.99 a year, sold through Gumroad, renewing until you cancel, or $29.99 once with nothing to renew. Either one opens every pack, including packs added later. " + KEY_LINE),
            "Can I practise the pre-trip inspection?": (None, "Yes. The CDL packs have a pre-trip examiner: you say each item out loud, as you would to an examiner, and tick it off."),
            "Do I need an account or an app download?": (None, "No account and no download. Cleared opens in a browser once you paste your key. Your progress is kept in the browser you study in, not on a server, so it does not follow you to another browser or device. The iPhone app is not out yet."),
            "How do I cancel?": (None, "Cancel from your Gumroad library. Cancelling does not close the packs straight away: you keep them for the days you have already paid for. After that the packs close, and your progress stays in that browser. A one-time key has nothing to cancel."),
            "Can I try it before I pay anything?": None,
        },
    },
    "boatready": {
        "tag": "Renews each month or year until you cancel.",
        "note": "The subscription opens all of it: the carriage list for your exact boat, reading lights and marks, safety advisories, the boats you look after, ticking items off as you go, Practice for lights and marks, and forecasts, tides and currents.",
        "seo_desc": "A boat safety checklist for your exact boat: the federal carriage requirements, with the CFR citation behind every line. $4.99 a month or $49.99 a year in your browser.",
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
    "whoserves": {
        "tag": "Renews each month or year until you cancel.",
        "note": "The subscription opens all of it: any US address, every government, office and officeholder, every source and check date, your election dates, up to eight saved addresses, recent votes and filings for your members of Congress, a letter addressed to any officeholder you pick, and the sourced record to share as plain text.",
        "seo_desc": "Type a US address and see every government with authority there and who holds each office, with the source and check date on each name. $4.99 a month in your browser.",
        "faq": {
            "What is free?": ("Can I see it before I pay?", "Yes, on this page: part of the record for one example address, with where each line was read, and screens from the app. The app itself opens only with a key, and there is no free trial."),
            "Exactly what is charged, and does it renew?": (None, "On the web, $4.99 a month or $39.99 a year, whichever you pick at Gumroad's checkout. Gumroad takes the payment. It renews automatically until you cancel. " + KEY_LINE + " A web subscription opens the app in browsers, not in the iPhone app."),
            "How do I cancel, and what happens after?": (None, "Cancel any time from your Gumroad receipt or library. The subscriber tools stay open for the time you already paid for, then close once Gumroad reports the subscription ended, which the page checks about once a day. A failed renewal payment closes them the same way. The browser you used can still read the addresses you saved. A new browser needs an active subscription."),
            "What happens to my address?": (None, "It goes to the US Census Bureau's geocoder to find your districts, and nowhere else. Nothing you look up is kept. If you subscribe and save an address, it stays in your own browser until you delete it. There is no account. " + DATA_KEY + " The privacy policy has the details."),
        },
    },
    # Flare, Books for One and Quiet (2026-11-15): on sale on the web first,
    # with nothing free there. The App Store wording stays in apps_data.
    "flare": {
        "tag": "A subscription that runs in a browser, renewing until you cancel. The iPhone app is not out yet.",
        # 2026-11-17: the sections from the merge (Flare b13c911). Perimeter's
        # founding key opens Flare too (AppGate 838f35a), so its buyers are told.
        "note": "Log symptoms, flares, sleep, food and period in a minute a day. Pattern analysis, up to 5 a day, looks across your entries and shows what tends to happen together, and the summary prints for your doctor. When you start, you choose what you are tracking. Perimenopause has 36 symptoms in five groups, your cycle pattern, and a script of what to say at the appointment beside the report. Doses, for a GLP-1 medicine, logs each dose and the day it stepped up, your weight and seven common side effects, and counts how often each came up in the weeks after each step up. Today sets the week before a change beside the week after it, for a dose step or any change you mark. Flare does not diagnose, explain or treat anything, and it is not a medical device.",
        "limits": "Your log stays in the browser you use and is not stored on our server, so download a copy now and then from Account. Your entries are sent only when you ask for patterns or for an appointment script, which also sends the cycle pattern you chose, and nothing is kept afterwards. Bought Founding access? Your key already opens Flare for its first year.",
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
        "limits": "Vet Pocket is not a vet and does not diagnose: it never names a condition and never says your pet is fine. If you are worried enough to ask, ringing your vet or an emergency clinic is always right; they triage over the phone for free. Cost ranges are estimates, not quotes. A browser cannot remind you when it is closed, so due dates go into your own calendar with a reminder a week before. Your pets' records stay in the browser you use and are not stored on our server, so download a copy now and then from Account. Up to 10 questions a day. Bought Founding access? Your key already opens Vet Pocket for its first year.",
    },
    "cast": {
        "price": "Books from $14.99 · Your own books $22.99/mo",
        "tag": "A book is one payment and never renews. Your Own Books is a membership with a one-week trial for new members, renewing until you cancel.",
        "note": "A license to listen to one book in full, not an audio file and not a copy of the book. 84 books on the shelf: 52 Carrier Press originals, the three American Firsts and 29 classics, and every card says how fully it is cast.",
        "limits": "In a browser the voices are computer voices your browser and device already have, not recordings of narrators, and how they sound depends on the browser. The sample on this page plays them before you pay. Cast needs a connection to open a book, and a browser can stop speaking when a phone locks or the tab goes to sleep, so keep the page open while you listen. Your place stays in the browser you use. Natural voices are in the iPhone app, not the web version.",
        "seo_desc": "Hear a book performed with a narrator and a voice for each character, in your browser. Computer voices, and every card says how fully it is cast. Books from $14.99, one payment.",
        "faq": {
            "Can I hear a book before I pay?": ("Can I hear it before I pay?", "Yes, on this page: a few lines from The Runaway Crate, read by your browser's own voices the way Cast reads them. Cast itself opens only with a key."),
            "What exactly am I charged?": (None, "A book from the shelf is one payment, from $14.99, with the price on its Gumroad listing. It never renews. Your Own Books, which plays EPUB files you add, is a membership: a one-week trial for new members, then $22.99 a month or $109.99 a year, renewing until you cancel. It does not open the shelf books, and neither is part of Carrier Press Access. Gumroad takes the payment."),
            "How do I cancel the membership?": (None, "In your Gumroad library, before the trial or the period ends. A cancelled membership runs to the end of the period you paid for. When it ends, the books you added stay in that browser and the first chapter of each still plays there."),
            "What happens to files I add?": (None, "An EPUB you add is read inside your browser and never uploaded. Cast keeps the script it makes, in that browser, and not the file. Remove deletes it, and so does clearing the site's data."),
            "Where is my key, and what if I come back later?": (None, "Your license key is on the Gumroad receipt email. Paste it on this page to open Cast and the book it was bought for. A key for another book goes in under I have a key, inside Cast. There is no account: your place and your opened books are kept in the browser you use, so in another browser, or after clearing site data, paste the same key again. Your place does not follow you there."),
        },
    },
}


def apply(apps):
    for app in apps:
        copy = COPY.get(app.get("slug"))
        if not copy:
            continue
        for field in ("note", "tag", "price", "limits"):
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
