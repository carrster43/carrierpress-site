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

# Carrier Press Access (author 2026-10-28): one self-serve Gumroad membership,
# Apps $14.99 / Books $14.99 / All Access $24.99 a month. The Apps and All
# Access key unlocks every web app below; Books delivers the direct ebooks.
# Nothing in it needs Jeffrey's hands. Empty until the product is published.
ACCESS_URL = "https://jeffreycarrier.gumroad.com/l/dyewjv"  # published by Jeffrey 2026-10-28
ACCESS_PRICE = "from $14.99 a month"
# Only web builds that actually take an Access key, deployed 2026-10-28;
# Canceled joined 2026-10-29 (repo 28cb2da).
# Flare, Books for One and Quiet joined 2026-11-15 (AppGate 54f41d0).
# Titrate joined 2026-11-15 (AppGate 9c1fc03). Doorstop and Threshold went live
# 2026-11-16 (AppGate 072c2f6a): founding access or an Access key opens each.
# Paper Trail 2026-11-16 (AppGate deployed 85d2593c): founding or Access opens it.
ACCESS_APPS = ["boatready", "whoserves", "endorsed", "conceptionzodiac", "downpour", "cancelled",
               "flare", "soleledger", "quiet", "threshold", "papertrail", "throughthegate", "vetpocket",
               "thebinder", "firstday", "tradedesk", "pantry", "fluenthour", "homeroom", "stuck", "pillproof",
               "handoff", "crosscheck", "spellbright", "potluck", "bench"]

# slug -> web sale settings.
#   web      path of the working web app on this domain, if one is deployed
#   buy      Gumroad URL of the web unlock (license key product)
#   buy_price
#   pre      Gumroad URL of the pre-order
#   pre_price
WEB = {
    # Gumroad prices matched to the approved price list 2026-10-27 (Canceled,
    # Conception Zodiac, Downpour, Who Serves). Boat Ready's web sale is the
    # Gumroad membership "Boat Ready Subscription", published by Jeffrey
    # 2026-10-29; old $9.99 one-time keys still unlock (BoatReady 3be2639).
    "boatready": dict(web="/boatready/app/", buy=GUMROAD + "boatready-subscription",
                      buy_price="$4.99 a month or $49.99 a year", sub=True),
    # Published by Jeffrey 2026-10-06. Canceled is one-time like Boat Ready.
    "cancelled": dict(web="/cancelled/app/", buy=GUMROAD + "canceled", buy_price="$38.99"),
    # Web builds live 2026-10-06 with the sale CLOSED (Gumroad hit a product
    # creation limit before their products could be made). The free part runs;
    # add buy= and buy_price= once each Gumroad product is published.
    "nightwatch": dict(web="/nightwatch/app/"),
    "channelmarks": dict(web="/channelmarks/app/"),
    # Published by Jeffrey 2026-10-18.
    # Free with ads on the web since 2026-11-22 (author); the $7.99 key, an
    # earlier buyer's key and the Apps tier of Access only turn the ads off
    # (AppGate 706bc1c freeApp; ConceptionZodiac lib/ads.ts isAdFree).
    "conceptionzodiac": dict(web="/conceptionzodiac/app/", buy=GUMROAD + "conceptionzodiac", buy_price="$7.99",
                             page_price="Free to use, or $7.99 once with no ads",
                             buy_label="Turn off the ads",
                             buy_note="$7.99 once, never renews, license key by email",
                             price_note="Everything is free, with a small ad below a result. One payment of $7.99 "
                                        "turns the ads off for good, in any browser you enter the key in. If you "
                                        "bought a key before, it already turns them off.",
                             open_label="Open Conception Zodiac",
                             open_note="Free in your browser, no account",
                             key_on_page=True,
                             access_note="no ads in Conception Zodiac, plus the other web apps, with one key, %s" % ACCESS_PRICE),
    # Web only since 2026-10-16: no App Store price to set beside the web one.
    "downpour": dict(web="/downpour/app/", buy=GUMROAD + "downpour", buy_price="$14.99", web_only=True),
    # Who Serves (store name until 1.0.1: Home Rule) is a SUBSCRIPTION on the
    # web too, so `sub` makes the page drop the word "once".
    # Free with ads on the web since 2026-11-22 (author); the subscription, an
    # earlier subscriber's key and the Apps tier of Access only turn the ads
    # off (AppGate 706bc1c freeApp; HomeRule lib/ads.ts isAdFree). $2.99 a month
    # (author 2026-11-22; was $4.99) or $39.99 a year (kept, author "Keep yearly plan").
    "whoserves": dict(web="/whoserves/app/", buy=GUMROAD + "whoserves",
                     buy_price="$2.99 a month or $39.99 a year", sub=True,
                     page_price="Free to use, or $2.99 a month with no ads",
                     buy_label="Turn off the ads",
                     price_note="Everything is free, with a small ad below the results. The subscription turns the "
                                "ads off, $2.99 a month or $39.99 a year, and renews until you cancel in your Gumroad "
                                "library. If it ends, Who Serves keeps working, with the ads back.",
                     buy_note="$2.99 a month or $39.99 a year, renews until cancelled, license key by email",
                     open_label="Open Who Serves",
                     open_note="Free in your browser, no account",
                     key_on_page=True,
                     access_note="no ads in Who Serves, plus the other web apps, with one key, %s" % ACCESS_PRICE),
    # Cleared, published by Jeffrey 2026-10-21 as a Gumroad membership. The
    # $29.99 one-time key (argfux, /l/endorsed-once, was /l/cleared-once) was published 2026-11-17;
    # the gate (AppGate deployed 40326a4b) opens it as a second "own" product.
    "endorsed": dict(web="/endorsed/app/", buy=GUMROAD + "endorsed",
                    buy_price="$4.99 a month or $49.99 a year", sub=True,
                    price_note="On the web, $4.99 a month or $49.99 a year until you cancel in your Gumroad library, "
                               "or $29.99 once with nothing to renew.",
                    extra=[(GUMROAD + "endorsed-once", "One-time key on the web",
                            "$29.99 once, opens every pack for good, never renews, license key by email")]),
    # Published by Jeffrey 2026-11-15 (Gumroad drafts 2026-11-14). Flare and
    # Books for One are memberships; Quiet is one payment. All three are served
    # by the gate (~/Projects/AppGate), not from this repo.
    "flare": dict(web="/flare/app/", buy=GUMROAD + "flare",
                  buy_price="$7.99 a month or $59.99 a year", sub=True),  # raised 2026-11-18 (author), from $4.99/$47.99
    "soleledger": dict(web="/soleledger/app/", buy=GUMROAD + "booksforone",
                       buy_price="$14.99 a month or $143.99 a year", sub=True),
    "quiet": dict(web="/quiet/app/", buy=GUMROAD + "quiet", buy_price="$49.99"),
    # Titrate and Doorstop: unpublished 2026-11-17, folded into Flare and Books
    # for One (folds.py). Nothing had sold.
    # Threshold (2026-11-15): $28.99 PER CHILD, once (author: a quantity box at
    # checkout; one key covers the children bought with it). The Gumroad product
    # (vbiwqf) was published by Jeffrey 2026-11-16; the gate carries its id.
    "threshold": dict(web="/threshold/app/", buy=GUMROAD + "threshold", buy_price="$28.99 per child",
                      price_note="Once, never a subscription. Choose how many children at checkout and one key covers them.",
                      buy_note="$28.99 per child, once, choose how many at checkout, license key by email"),
    # Paper Trail (2026-11-16): a subscription at the price of record (apps_data:
    # $14.99/mo or $143.99/yr), published by Jeffrey 2026-11-16 (ygkehr), and the
    # gate (AppGate products.js, deployed 85d2593c) carries its id. Founding
    # access opens it for a first year from launch day.
    "papertrail": dict(web="/papertrail/app/", buy=GUMROAD + "papertrail",
                       buy_price="$7.99 a month or $69.99 a year", sub=True),
    # Through the Gate (2026-11-17): $19.99 a month (zvmep) or $44.99 once for a
    # 90-day pass (hhldj, /l/throughthegate-pass), both published by Jeffrey
    # 2026-11-17. The gate (AppGate deployed cb2c636e) opens the pass for 90 days
    # from the sale (kind "pass"). Founding access opens it for a first year.
    "throughthegate": dict(web="/throughthegate/app/", buy=GUMROAD + "throughthegate",
                           buy_price="$19.99 a month", sub=True,
                           price_note="On the web, $19.99 a month until you cancel in your Gumroad library, "
                                      "or $44.99 once for a 90-day pass that never renews.",
                           extra=[(GUMROAD + "throughthegate-pass", "90-day pass on the web",
                                   "$44.99 once, open for 90 days from the day you buy it, never renews, license key by email")]),
    # Vet Pocket (2026-11-17): a subscription at the price of record (apps_data:
    # $9.99/mo or $79.99/yr). Its Gumroad product is DRAFTED, not published:
    # this branch waits for his publish, then the gate deploy, then the push.
    # Founding access opens it for a first year from launch day.
    "vetpocket": dict(web="/vetpocket/app/", buy=GUMROAD + "vetpocket",
                      buy_price="$9.99 a month or $79.99 a year", sub=True),
    # The Binder (2026-11-18): $49 once (author 2026-11-18: "$49 once"), one key
    # that never expires (AppGate kind "own") and no renewal. DRAFTED by Claude
    # 2026-11-18 (owzkit /l/thebinder), PUBLISHED by Jeffrey and live 2026-11-18. The $29/yr renewal draft
    # (/l/thebinder-renewal) stays unpublished and is linked from nowhere. No
    # founding access was ever sold for it.
    "thebinder": dict(web="/thebinder/app/", buy=GUMROAD + "thebinder", buy_price="$49",
                      buy_label="Buy the web version",
                      buy_note="$49 once, yours for good, never renews, license key by email",
                      price_note="On the web, $49 once, yours for good. It never renews."),
    # FirstDay (2026-11-18): $7.99 a month or $59.99 a year (ikblap, /l/firstday),
    # or $49.99 once for the school year (ziufob, /l/firstday-pass), the prices of
    # record (author "Apply all" 2026-11-17). The subscription is PUBLISHED and
    # live 2026-11-18; the pass was PUBLISHED by Jeffrey 2026-11-19 and is offered
    # here from then. The gate ends the pass at the first June 30 after the sale (AppGate
    # license.js passEnd); keep "June 30, 2027" here and on Gumroad moving together.
    "firstday": dict(web="/firstday/app/", buy=GUMROAD + "firstday",
                     buy_price="$7.99 a month or $59.99 a year", sub=True,
                     price_note="On the web, $7.99 a month or $59.99 a year until you cancel in your Gumroad library, "
                                "or $49.99 once for the school year, through June 30, 2027, never renews.",
                     extra=[(GUMROAD + "firstday-pass", "School-year pass on the web",
                             "$49.99 once, open through June 30, 2027, never renews, license key by email")]),
    # Trade Desk (2026-11-19): $19.99 a month or $191.99 a year (bezlwj, /l/tradedesk,
    # author 2026-11-19, lowered from $38.99/$374.99 because the web version has no
    # card payment link). DRAFTED by Claude 2026-11-19, NOT published: this branch
    # waits for his publish, then the gate deploy, then the push. No founding was
    # ever sold for it.
    # Pantry (2026-11-19): $6.99 a month or $59.99 a year (author "Apply all"
    # 2026-11-17, APP_PRICE_COMPARISON_2026-11-17.md). DRAFTED by Claude, NOT
    # published: this branch waits for his publish, then the gate deploy, then
    # the push. No founding was ever sold for it.
    "pantry": dict(web="/pantry/app/", buy=GUMROAD + "pantry",
                   buy_price="$6.99 a month or $59.99 a year", sub=True),
    # Fluent Hour (2026-11-19): $17.99 a month or $119.99 a year (author "Apply
    # all" 2026-11-17, APP_PRICE_COMPARISON_2026-11-17.md: the yearly cut from
    # $172.99). DRAFTED by Claude (lnnca, /l/fluenthour), NOT published: this
    # branch waits for his publish, then the gate deploy, then the push. No
    # founding was ever sold for it.
    # Homeroom (2026-11-19): $8.99 a month or $79.99 a year, or $69.99 once for
    # the school year (author "Apply all" 2026-11-17, APP_PRICE_COMPARISON lines
    # 38 and 77). Legal hold cleared by the author 2026-11-19 after the 10 states
    # were rechecked. Drafted by Claude (rombumb /l/homeroom, nplgpp
    # /l/homeroom-pass), both PUBLISHED by Jeffrey 2026-11-19; gate 9749f94c.
    # No founding was ever sold.
    "homeroom": dict(web="/homeroom/app/", buy=GUMROAD + "homeroom",
                     buy_price="$8.99 a month or $79.99 a year", sub=True,
                     price_note="On the web, $8.99 a month or $79.99 a year until you cancel in your Gumroad library, "
                                "or $69.99 once for the school year, through June 30, 2027, never renews.",
                     extra=[(GUMROAD + "homeroom-pass", "School-year pass on the web",
                             "$69.99 once, open through June 30, 2027, never renews, license key by email")]),
    # Stuck (2026-11-20): $9.99 a month or $79.99 a year (author "Apply all"
    # 2026-11-17, APP_PRICE_COMPARISON line 41). Children's privacy hold cleared
    # by the author 2026-11-20 ("All ages, I assume the risk"). Drafted by Claude
    # (drehbp /l/stuck), PUBLISHED by Jeffrey 2026-11-20 (is_published:true read
    # back); gate 24f4af7b deployed before this push. No founding was ever sold.
    "stuck": dict(web="/stuck/app/", buy=GUMROAD + "stuck",
                  buy_price="$9.99 a month or $79.99 a year", sub=True),
    # PillProof (2026-11-20): $7.99 a month or $69.99 a year per household
    # (author "Apply all" 2026-11-17, APP_PRICE_COMPARISON line 40). Health
    # claims hold cleared by the author 2026-11-20 as "Ship as a log, no
    # claims". crtdu (/l/pillproof) drafted by Claude, PUBLISHED (read back
    # is_published:true 2026-11-20); gate deployed d7fb18ea before this push.
    # No founding was ever sold.
    "pillproof": dict(web="/pillproof/app/", buy=GUMROAD + "pillproof",
                      buy_price="$7.99 a month or $69.99 a year", sub=True),
    # Handoff (2026-11-20; LIVE 2026-11-21): $14.99 a month or
    # $143.99 a year per parent (APP_PRICE_COMPARISON line 62). Author
    # 2026-11-20, "A, creator covers, ship at my risk": the gate holds the
    # shared record; the creator's key pays for the arrangement, the invited
    # parent joins free (?join=CODE on the key page, assets/handoff-join.js)
    # and needs a key only to export. /l/handoff (7Nf1zXRkMHOmxtI6xrRQ4Q==)
    # drafted by Claude and PUBLISHED by Jeffrey 2026-11-21; gate deployed
    # ba0e38af (AppGate b6af8a7) before this push.
    "handoff": dict(web="/handoff/app/", buy=GUMROAD + "handoff",
                    buy_price="$14.99 a month or $143.99 a year",
                    price_note="Per parent, renewing until you cancel. The parent you invite joins free and needs a key only to export.",
                    sub=True),
    # Crosscheck (2026-11-21): $39.99 per case, a Gumroad digital product with the
    # quantity box on, NOT a membership (author 2026-11-21, "One key = one
    # case"). The app opens with no key (AppGate 2a027e8 `freeApp`); a key drafts
    # the letters for one case, a second bill needs a second key, and the Apps
    # tier of Access drafts letters for any case. The Gumroad product
    # (/l/crosscheck) is NOT made yet: this branch is held until Jeffrey
    # publishes it and the gate is deployed with its real product id. No
    # founding was ever sold.
    "crosscheck": dict(web="/crosscheck/app/", buy=GUMROAD + "crosscheck", buy_price="$39.99 per case",
                       buy_label="Buy a key",
                       buy_note="$39.99 per case, once, choose how many cases at checkout, license key by email",
                       price_note="One payment per case, never a subscription. One key drafts the letters for one "
                                  "case; a second bill needs a second key.",
                       open_label="Open Crosscheck",
                       open_note="Free: type the figures and see every finding",
                       key_hint="paste it under Letters, on the case it is for",
                       access_note="letters for any case, plus the other web apps, with one key, %s" % ACCESS_PRICE),
    # Spellbright (2026-11-22): free to play with ads, or $2.99 a month with no
    # ads (author 2026-11-22). Every mode is free; the Gumroad membership
    # (/l/spellbright, fiDDKpZNk1CGHwUNEcluVg==, edit vwsyma) buys only the
    # removal of ads, and so does the Apps tier of Access. No yearly price. The
    # game opens with no key (AppGate 2bf544a `freeApp`); the key is entered on
    # the key page (key_on_page), and the game asks /__gate/status before it
    # loads Google's ad script (Spellbright lib/adBreak.ts). DRAFTED by Claude,
    # NOT published: this branch is held until Jeffrey publishes it and the gate
    # is deployed. No founding was ever sold.
    #   page_price   the price line on the key page, where the free game comes first
    #   key_on_page  a free-to-open app whose key is still entered on its key page
    "spellbright": dict(web="/spellbright/app/", buy=GUMROAD + "spellbright", buy_price="$2.99 a month", sub=True,
                        page_price="Free to play, or $2.99 a month with no ads",
                        buy_label="Turn off the ads",
                        buy_note="$2.99 a month, renews until you cancel, license key by email",
                        price_note="Every mode is free, with a short ad now and then between games. The membership "
                                   "turns the ads off and renews each month until you cancel in your Gumroad "
                                   "library. If it ends, Spellbright keeps working, with the ads back.",
                        open_label="Play Spellbright",
                        open_note="Free in your browser, no account",
                        key_on_page=True,
                        access_note="no ads in Spellbright, plus the other web apps, with one key, %s" % ACCESS_PRICE),
    # Bench (2026-11-22, author "$19.99/mo, $191.99/yr"): $19.99 a month or
    # $191.99 a year per desk; the key opens the Author desk. jzpiu (/l/bench)
    # DRAFTED by Claude, NOT published: this commit is held until Jeffrey
    # publishes the membership. No founding presale was ever sold.
    "bench": dict(web="/bench/app/", buy=GUMROAD + "bench",
                  buy_price="$19.99 a month or $191.99 a year", sub=True, web_only=True),
    # Potluck (2026-11-22, author: "Add a paid unlock"): $4.99 a month or $39.99
    # a year PER STREET. A sample street opens with no key (AppGate 43e0371
    # `freeApp`); the organiser's key opens their real street, door cards and
    # the weekly flyer, and is entered on this page (key_on_page). Neighbours
    # join free with a door card in the app, never on this page. DRAFTED by
    # Claude, NOT published: this branch is held until Jeffrey publishes the
    # membership and the gate is deployed.
    "potluck": dict(web="/potluck/app/", buy=GUMROAD + "potluck", buy_price="$4.99 a month or $39.99 a year", sub=True,
                    page_price="$4.99 a month or $39.99 a year, for the whole street",
                    buy_label="Open your street",
                    buy_note="$4.99 a month or $39.99 a year, license key by email",
                    price_note="One membership covers the whole street, and every neighbour joins free. It renews until "
                               "you cancel in your Gumroad library. If it ends, the street stays readable and new posts, "
                               "door cards and the flyer pause until it is renewed.",
                    open_label="Look round a sample street",
                    open_note="Free in your browser, no account",
                    key_on_page=True,
                    extra=[("/potluck/app/account", "Got a door card?", "Join your street free, with the code on it")],
                    access_note="a street, plus the other web apps, with one key, %s" % ACCESS_PRICE),
    "fluenthour": dict(web="/fluenthour/app/", buy=GUMROAD + "fluenthour",
                       buy_price="$17.99 a month or $119.99 a year", sub=True),
    "tradedesk": dict(web="/tradedesk/app/", buy=GUMROAD + "tradedesk",
                      buy_price="$19.99 a month or $191.99 a year", sub=True),
    # Cast, published by Jeffrey 2026-11-03: TWO web products, so it names its
    # own Buy link (buy_label, buy_note), its own price sentence (price_note)
    # and the second offer (extra). Shelf books are one-time Gumroad versions,
    # $14.99 floor; Your Own Books is a membership. Not in Carrier Press Access.
    "cast": dict(web="/cast/app/", buy=GUMROAD + "cast", buy_price="from $14.99 a book",
                 buy_label="Buy a book on the web",
                 buy_note="from $14.99 a book, one payment, license key by email",
                 price_note="On the web, shelf books are one payment each, from $14.99, and nothing "
                            "renews. Your own books start with a one-week trial for new members, then $22.99 a "
                            "month or $109.99 a year until you cancel in your Gumroad library.",
                 extra=[("/cast/app/", "Hear any book's opening", "plays in this browser, no key needed"),
                        (GUMROAD + "castyourbooks", "Your own books on the web",
                         "a one-week trial, then $22.99 a month or $109.99 a year until you cancel, license key by email")]),
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

# Public domain in the US only: never sold direct on Gumroad, which sells
# worldwide (author rule, web-versions-gumroad-rail). build.py refuses an entry.
NEVER_DIRECT = {
    "B0H3KKRTMP",   # The Secret of Chimneys, Agatha Christie
    "B0H7NMYT5J",   # The Murder of Roger Ackroyd, Agatha Christie
}

# By ASIN, not by title: the Greek BILINGUAL Edition (B0H4BQSGB6) is a separate,
# wide product, and a title match would wrongly block it. Top End is not in the
# catalog; add its ASIN here if it ever is.
KDP_SELECT = {
    "B07VPL3FS3",   # Who Wants To Be Greek?, English Narrative Edition
    "B0GWYMSCLL",   # Letters for Cash
}


# Ebooks delivered by the Carrier Press Access BOOKS tier (and All Access) on
# Gumroad, as DRM-free EPUBs in the buyer's library. Author 2026-11-21: until a
# book has its own Gumroad product (EBOOKS above), its "Ebook" link goes to
# Access. List a book here ONLY once its EPUB is uploaded to BOTH the Books and
# the All Access tier; a link to a membership that does not hold the book is a
# broken promise. Never a KDP Select or NEVER_DIRECT title (build.py refuses).
# Files: SALES_PUSH/_backmatter_tools/out_direct_v2/, checked by
# check_direct_epub.py. First 48 uploaded 2026-10-28.
ACCESS_EBOOKS = {
    "B0H6CWP5GN",  # The Sponge Cache
    "B0H6CK8NB6",  # The Pearl Ledger
    "B0H6DCTJ2F",  # The Sixth Cache
    "B0H6D8M2T1",  # The Mastic Codex
    "B0H6DKF4ZK",  # The Seven Plates
    "B0GZCKYKZ9",  # The Second Shooter
    "B0H22L5LD9",  # The Recipe Notebooks
    "B0GXW2XL1N",  # The Sea Captain's Portrait
    "B0H4BSJQYV",  # The Prattler Files
    "B0H4CHK34V",  # The Morning Table
    "B0H4CCMSQS",  # The Marjorie Corey Files: The Complete Series
    "B0H59MBV8R",  # The Drosos Ledger
    "B0H59N5CVT",  # The Hudson Creek Record
    "B0H59PY6VD",  # The Sfax Letters
    "B0H5B1M3W6",  # The Pencil Under the Bench
    "B0H59JV13T",  # The Roebuck Bay Record
    "B0GXP2C498",  # The First Build
    "B0H59B9QFV",  # The Runaway Crate
    "B0H59QNK51",  # The Frost Cave Reset
    "B0H597VNJ5",  # Sky Islands Save File
    "B0H59H8PRT",  # The Mech Workshop Machine
    "B0H59QWDGT",  # Portal Park
    "B0H6FH7TB7",  # The First Flicker
    "B0H6F7KGGK",  # Static Orchard
    "B0H6F76741",  # The Loop That Spoke
    "B0H3ZQZ3Z8",  # The Broken Save
    "B0H2WM1V3D",  # The Moving Line
    "B0H6V88BL1",  # The Between Badge
    "B0H6VGK2MZ",  # Beneath the Surface
    "B0H1LG32RB",  # The Last Adviser
    "B0GYWWCLG8",  # Concrete Mirrors
    "B0GZK79LKN",  # Stealing First Base
    "B0H48WBFTD",  # The Sterling Conspiracy
    "B0H483NLCV",  # The Starlight Secret Society
    "B0H47ZCBH1",  # The Fortune Weaver
    "B0GYBT12DP",  # Side Hustle Junior
    "B0H46C5QFS",  # Digital Gold Rush
    "B0H4DQ6488",  # The Startup Club
    "B0H278QHQH",  # The Digital Founders
    "B0H4DX9RRF",  # The Billionaire's Legacy Game
    "B0H4DTYL5S",  # The Growing Fortune
    "B0H4DFKCGC",  # Seeded for Success
    "B0H3G5L8JW",  # Safe Online Projects for Kids
    "B0GX2YNHT9",  # Passive Income Blueprint
    "B0H4DR314J",  # The Passive Income Dividend System
    "B0GX38GVW3",  # Automation Income Systems
    "B0H46VTCYP",  # AI Income Streams
    "B0H4BQSGB6",  # Who Wants To Be Greek? Greek Bilingual Edition
    # 38 more uploaded 2026-11-21 (folders "Ebooks, part 10..17"); the 30 above
    # whose Contents or back matter changed were replaced the same day.
    "B0HN3HJJBR",  # The Music of the Spheres
    "B0HNGNHF35",  # The Tower on the Highest Hill
    "B0H7P6LRQJ",  # The Defects That Pass Review
    "B0HHJSF9SP",  # One Minute Past Noon
    "B0HHJK9GMT",  # Twelve Minutes on River Road
    "B0HMK4LL3B",  # Mrs. Kehoe
    "B0H7W7VY7S",  # The King in Yellow
    "B0HGG934BB",  # Carcosa
    "B0HGS6TH57",  # The Mystery of Choice
    "B0HGMSMFQK",  # The Great God Pan
    "B0HQCG586W",  # Can Such Things Be?
    "B0HQ55DVX2",  # The Call of Cthulhu and Other Mythos Tales
    "B0HGTD7VBZ",  # The Willows
    "B0HL27ZXPJ",  # The Three Impostors
    "B0HH3CJRRW",  # Ghost Stories of an Antiquary
    "B0HL24L2L3",  # More Ghost Stories of an Antiquary
    "B0H2Y3TMMC",  # The Golem
    "B0H7QSD429",  # The Man Who Was Thursday
    "B0H7QFWVXG",  # The Blue Castle
    "B0H7PZ3FDM",  # The Enchanted April
    "B0H7QPDD4S",  # The Mysteries of Udolpho
    "B0H7PDG821",  # The Monk
    "B0H7PDS3QM",  # The Extraordinary Adventures of Arsene Lupin
    "B0H7LYK2QQ",  # Dr. Mabuse the Gambler
    "B0H7R61S7C",  # Sweeney Todd, Volume One
    "B0H7R7Y1N4",  # Sweeney Todd, Volume Two
    "B0H7VNFRN4",  # A Honeymoon in Space
    "B0H7WM2CHN",  # The Man Who Robbed the Bank of England
    "B0GZJ9DPJC",  # The Green Mummy
    "B07X7H37LC",  # Dancers in the Dark
    "B07XF4J8SR",  # 6,000 Tons of Gold
    "B07XKDY286",  # A New History of Blue Beard
    "B085P2CWR1",  # The Laughing Willow
    "B07Y5MNP3M",  # Artful Anticks
    "B07X4CGTKR",  # The Surprise Book
    "B0HGVD689V",  # The Science of Getting Rich
    "B0GX34KKKQ",  # The Animate and the Inanimate
    "B0HMZKCTTS",  # Father Brown
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
    "papertrail": GUMROAD + "papertrail-founding",
    "vetpocket": GUMROAD + "vetpocket-founding",
    # perimeter: unpublished 2026-11-17 (author, "Stop selling it"); its keys still open Flare.
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
    "planfinder": "licensed to agencies, not sold to the person using it",
}

# The MailerLite embedded form every landing page posts to. Empty = the page
# falls back to the old "Tell me when it is out" email link. Each signup carries
# the app's slug in the `app` field, so a launch email goes only to that list.
# Form "App waiting list (carrierpress.com/apps)", group App Waiting List, double opt-in ON,
# hidden field App (default "apps"; each page sends its slug). Made 2026-10-18.
WAITLIST_ACTION = "https://assets.mailerlite.com/jsonp/2504319/forms/201729201809654833/subscribe"


def presale_url(slug):
    return "" if slug in NO_PRESALE else PRESALE.get(slug, "")


# ------------------------------------------------------------ Amazon links ----
# The Associates tracking tag appended to every /dp/ product link across the
# three sites. Added 2026-11-22, after an audit found 1,148 Amazon product
# links across the site and not one of them tagged: every click was earning
# the referral fee for nobody.
#
# The tag is live. Account approved and the store ID confirmed in Associates
# Central on 2026-11-22. Emptying this string is the clean off switch: it
# restores the plain product URL byte for byte, so nothing downstream has to
# change if the account ever lapses or the tag is reissued.
#
# Amazon pays no referral fee on products the Associate buys themselves, or for
# friends and relatives. That is about Jeffrey's own purchases, not about the
# books: a stranger buying a Carrier Press title through a link on
# carrierpress.com is ordinary referral traffic and is what the tag is for.
AMZ_TAG = "carrierpress-20"

# Only /dp/ PURCHASE links carry the tag. The review composer
# (/review/create-review) deliberately does not: it is not a purchase path, it
# earns nothing, and a tagged review request reads as an ad for a favour.
# refresh_ratings.py fetches /dp/ pages to scrape ratings and is also left bare;
# tagging a request no human clicks would be meaningless at best.
#
# Every builder reads AMZ_URL. Four of them (books, build, listen,
# make_progress) each kept a private copy of the bare URL and make_publish had
# it inline, which is how one string ended up in five places and out of reach of
# a single edit. Keep it here; the shape stays "...{}" so the existing
# AMZ.format(asin) call sites need no change.
AMZ_URL = "https://www.amazon.com/dp/{}" + (f"?tag={AMZ_TAG}" if AMZ_TAG else "")
