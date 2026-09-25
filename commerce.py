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
TIP_URL = ""

# slug -> web sale settings.
#   web      path of the working web app on this domain, if one is deployed
#   buy      Gumroad URL of the web unlock (license key product)
#   buy_price
#   pre      Gumroad URL of the pre-order
#   pre_price
WEB = {
    "boatready": dict(web="/boatready/app/", buy="", buy_price="$9.99"),
}


def for_app(slug):
    return WEB.get(slug, {})
