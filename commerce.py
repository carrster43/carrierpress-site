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

# One product for the whole portfolio. Pay what you want, $3 minimum.
TIP_URL = "https://jeffreycarrier.gumroad.com/coffee"

# slug -> web sale settings.
#   web      path of the working web app on this domain, if one is deployed
#   buy      Gumroad URL of the web unlock (license key product)
#   buy_price
#   pre      Gumroad URL of the pre-order
#   pre_price
WEB = {
    "boatready": dict(web="/boatready/app/", buy=GUMROAD + "boatready", buy_price="$9.99"),
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
