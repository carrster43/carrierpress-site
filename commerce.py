#!/usr/bin/env python3
"""
Where each app takes money on the web. The single source for every Buy,
Pre-order and Support button on /apps/<slug>/.

THE AUTHOR'S DECISIONS, 2026-09-25. Do not re-litigate them here:

    PRE-ORDER   one-time, never a subscription for something nobody can use
                yet. Built on Gumroad's pre-order setting, which does NOT charge
                the card until the release date, so the site's rule "nothing is
                sold before the part you would rely on is finished" still holds.
    TIP         labelled "Support the build", never "donate". Carrier Press is
                an imprint, not a charity, and "donation" reads tax-deductible.
    WEB UNLOCK  a Gumroad product with license keys. Boat Ready's is $9.99.

>>> EVERY URL BELOW IS EMPTY UNTIL THE GUMROAD PRODUCT EXISTS. <<<
An empty URL means NO BUTTON, not a button that 404s. make_app_pages.py
refuses to render a button whose URL is empty, so filling one field here is the
whole of "turning it on".
"""

GUMROAD = "https://jeffreycarrier.gumroad.com/l/"

# Every "Support the build" button points at /support/ (author 2026-10-19), where
# all three rails show: Gumroad (pay what you want, $3 minimum), PayPal and
# Ethereum. The Gumroad tip product itself is support_data.ONE_TIME[0].
TIP_URL = "/support/"

# slug -> web sale settings.
#   web      path of the working web app on this domain, if one is deployed
#   buy      Gumroad URL of the web unlock (license key product)
#   buy_price
#   pre      Gumroad URL of the pre-order
#   pre_price
WEB = {
    # Gumroad prices matched to the approved price list 2026-10-27 (Canceled,
    # Conception Zodiac, Downpour, Who Serves). Boat Ready is still the old
    # one-time web unlock until its web build sells the subscription.
    "boatready": dict(web="/boatready/app/", buy=GUMROAD + "boatready", buy_price="$9.99"),
    # Published by Jeffrey 2026-10-06. Canceled is one-time like Boat Ready.
    "cancelled": dict(web="/cancelled/app/", buy=GUMROAD + "canceled", buy_price="$38.99"),
    # Web builds live 2026-10-06 with the sale CLOSED (Gumroad hit a product
    # creation limit before their products could be made). The free part runs;
    # add buy= and buy_price= once each Gumroad product is published.
    "nightwatch": dict(web="/nightwatch/app/"),
    "channelmarks": dict(web="/channelmarks/app/"),
    # Published by Jeffrey 2026-10-18.
    "conceptionzodiac": dict(web="/conceptionzodiac/app/", buy=GUMROAD + "conceptionzodiac", buy_price="$14.99"),
    # Web only since 2026-10-16: no App Store price to set beside the web one.
    "downpour": dict(web="/downpour/app/", buy=GUMROAD + "downpour", buy_price="$14.99", web_only=True),
    # Who Serves (store name until 1.0.1: Home Rule) is a SUBSCRIPTION on the
    # web too, so `sub` makes the page drop the word "once".
    "whoserves": dict(web="/whoserves/app/", buy=GUMROAD + "whoserves",
                     buy_price="$14.99 a month or $143.99 a year", sub=True),
    # Cleared, published by Jeffrey 2026-10-21 as a Gumroad membership.
    "cleared": dict(web="/cleared/app/", buy=GUMROAD + "cleared",
                    buy_price="$4.99 a month or $49.99 a year", sub=True),
}


def for_app(slug):
    return WEB.get(slug, {})


# ---- Ebooks sold direct ------------------------------------------------------
# Catalog ASIN -> the Gumroad product for its DRM-free EPUB.
#
# THE AUTHOR'S RULES, 2026-09-25:
#   PRICE   the same as the live Kindle price, never lower. Amazon price-matches
#           downward, so undercutting it here drags the Kindle royalty down too.
#   PRINT   paperback and hardcover stay on Amazon. The card's existing Amazon
#           button already covers them; nothing here sells print.
#   SELECT  Who Wants To Be Greek, Letters for Cash and Top End are in KDP
#           Select, which forbids selling the ebook anywhere else. They must
#           NEVER get an entry here. build.py refuses to build if one does.
EBOOKS = {
    # "B0XXXXXXXX": dict(url=GUMROAD + "permalink", price="$6.99"),
}

# By ASIN, not by title: the Greek BILINGUAL Edition (B0H4BQSGB6) is a separate,
# wide product, and a title match would wrongly block it. Top End is not in the
# catalog; add its ASIN here if it ever is.
KDP_SELECT = {
    "B07VPL3FS3",   # Who Wants To Be Greek?, English Narrative Edition
    "B0GWYMSCLL",   # Letters for Cash
}


# ---- Founding access and the waiting list (AUTHOR, 2026-10-18) -------------
# Every unreleased app gets the SAME founding access: $2.99 once, PAID NOW, which
# unlocks the web version at launch (its first year, for a subscription app).
# Gumroad no longer has a pre-order setting, so the card is charged at purchase;
# the author chose that, with a plain promise: if the app never launches, the
# $2.99 comes back in full. Never a recurring charge for something nobody can
# use yet (the 09-25 rule still holds). Fill PRESALE[slug] only
# after Jeffrey has PUBLISHED that Gumroad product; an empty entry = no button.
PRESALE_PRICE = "$2.99"
PRESALE = {
    # Published by Jeffrey 2026-10-18.
    "flare": GUMROAD + "flare-founding",
    "throughthegate": GUMROAD + "throughthegate-founding",
    "soleledger": GUMROAD + "soleledger-founding",
    "titrate": GUMROAD + "titrate-founding",
    "doorstop": GUMROAD + "doorstop-founding",
    "papertrail": GUMROAD + "papertrail-founding",
    "vetpocket": GUMROAD + "vetpocket-founding",
    "perimeter": GUMROAD + "perimeter-founding",
    "threshold": GUMROAD + "threshold-founding",
}

# Unreleased apps that get NO founding access, and why. Anything not here and not
# already on sale is eligible.
NO_PRESALE = {
    "nightwatch": "merged into Boat Ready, which is already on sale",
    "channelmarks": "merged into Boat Ready, which is already on sale",
    "waitlist": "free to the person using it; the clinic pays",
    "gedcompletion": "free to the student; the board pays",
    "porchlight": "free to the people using it",
    "potluck": "free to the people using it",
    "planfinder": "licensed to agencies, not sold to the person using it",
    "crosscheck": "held on regulatory grounds; no money until that is answered",
    "bench": "waiting list only until the first desk is proven (author 2026-10-19)",
}

# The MailerLite embedded form every landing page posts to. Empty = the page
# falls back to the old "Tell me when it is out" email link. Each signup carries
# the app's slug in the `app` field, so a launch email goes only to that list.
# Form "App waiting list (carrierpress.com/apps)", group App Waiting List, double opt-in ON,
# hidden field App (default "apps"; each page sends its slug). Made 2026-10-18.
WAITLIST_ACTION = "https://assets.mailerlite.com/jsonp/2504319/forms/201729201809654833/subscribe"


def presale_url(slug):
    return "" if slug in NO_PRESALE else PRESALE.get(slug, "")
