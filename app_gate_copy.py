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
        "note": "19 packs and 828 practice questions, from the CDL general test, air brakes and combination vehicles through HazMat, drone, pilot, captain, rail and FEMA. Every answer names its source: the federal rule, the FEMA course text, or your state's law or manual where the state sets it. Every pack was checked item by item by a reviewer who did not write it. Nothing is copied from a state manual.",
        "seo_desc": "CDL practice test questions in your browser for $4.99 a month. 828 questions across 19 packs, from general knowledge to HazMat, with the source named under every answer.",
        "faq": {
            "Is there a free CDL practice test?": ("Can I see it before I pay?", "Yes, on this page: three real questions from the General Knowledge pack, with their sources, and screens from the app. The app itself opens only with a key. You see the price, the renewal and how to cancel before you subscribe, and the checkout is on Gumroad, so your card details never reach Cleared."),
            "What does Cleared cost?": (None, "$4.99 a month or $49.99 a year, sold through Gumroad, renewing until you cancel. One subscription opens every pack, including packs added later. " + KEY_LINE),
            "Can I practise the pre-trip inspection?": (None, "Yes. The CDL packs have a pre-trip examiner: you say each item out loud, as you would to an examiner, and tick it off."),
            "Do I need an account or an app download?": (None, "No account and no download. Cleared opens in a browser once you paste your key. Your progress is kept in the browser you study in, not on a server, so it does not follow you to another browser or device. The iPhone app is not out yet."),
            "How do I cancel?": (None, "Cancel from your Gumroad library. Cancelling does not close the packs straight away: you keep them for the days you have already paid for. After that the packs close, and your progress stays in that browser."),
            "Can I try it before I pay anything?": None,
        },
    },
    "boatready": {
        "note": "The subscription opens all of it: the carriage list for your exact boat, reading lights and marks, safety advisories, the boats you look after, ticking items off as you go, Practice for lights and marks, and forecasts, tides and currents. Night Watch and Channel Marks are part of it now.",
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
        "note": "The subscription opens all of it: any US address, every government, office and officeholder, every source and check date, your election dates, up to eight saved addresses, recent votes and filings for your members of Congress, a letter addressed to any officeholder you pick, and the sourced record to share as plain text.",
        "seo_desc": "Type a US address and see every government with authority there and who holds each office, with the source and check date on each name. $14.99 a month in your browser.",
        "faq": {
            "What is free?": ("Can I see it before I pay?", "Yes, on this page: part of the record for one example address, with where each line was read, and screens from the app. The app itself opens only with a key, and there is no free trial."),
            "Exactly what is charged, and does it renew?": (None, "On the web, $14.99 a month or $143.99 a year, whichever you pick at Gumroad's checkout. Gumroad takes the payment. It renews automatically until you cancel. " + KEY_LINE + " A web subscription opens the app in browsers, not in the iPhone app."),
            "How do I cancel, and what happens after?": (None, "Cancel any time from your Gumroad receipt or library. The subscriber tools stay open for the time you already paid for, then close once Gumroad reports the subscription ended, which the page checks about once a day. A failed renewal payment closes them the same way. The browser you used can still read the addresses you saved. A new browser needs an active subscription."),
            "What happens to my address?": (None, "It goes to the US Census Bureau's geocoder to find your districts, and nowhere else. Nothing you look up is kept. If you subscribe and save an address, it stays in your own browser until you delete it. There is no account. " + DATA_KEY + " The privacy policy has the details."),
        },
    },
    "cast": {
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
        if copy.get("note"):
            app["note"] = copy["note"]
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
