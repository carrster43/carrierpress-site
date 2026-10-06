#!/usr/bin/env python3
"""
Every way a reader can pay the press directly, for /support/. One place.

THE RULES, all standing decisions:
    WORDING   "support", never "donate". Carrier Press is an imprint of one
              person, not a charity, so "donation" reads as tax deductible.
    EMPTY     an empty url renders NO button. Fill one field and rebuild with
              `python3 make_progress.py`; that is the whole of turning one on.
    PATREON   the account exists but has no published page and no claimed
              vanity, so patreon.com/CarrierPress is NOT his. Leave it empty
              until the creator page is live and the real URL is pasted here.
    STRIPE    use the PRESS Stripe account's payment link, never the apps
              account (Carrier Ventures). Money must land in the right business.
"""

ETH_ADDRESS = "0xD7bF6e0E28210DC7d3cDD3A5E7e34280eDbA18e7"  # same as catalog.json, EIP-55 checked

# MetaMask's universal link: opens the wallet's Send screen to this address on
# chain 1 (Ethereum mainnet). The reader picks the amount.
METAMASK_URL = "https://metamask.app.link/send/%s@1" % ETH_ADDRESS

# Spritz Finance referral. Empty until Jeffrey supplies his code or link.
SPRITZ_URL = ""

# Membership tiers. `gumroad` and `patreon` are the join URLs for each rail.
TIERS = [
    dict(name="Reader", price="$3", per="month",
         perks=["The monthly journal a week before it goes public",
                "Your name in the back of every new book, under Readers Who Made This Possible"],
         gumroad="", patreon=""),
    dict(name="First Reader", price="$8", per="month",
         perks=["Everything in Reader",
                "The ebook of every new release the week it comes out",
                "Opening chapters of books in progress, before they are finished",
                "Beta invitations to new apps before they reach the App Store"],
         gumroad="", patreon=""),
    dict(name="Patron of the Press", price="$25", per="month",
         perks=["Everything in First Reader",
                "A signed print copy of every new release, posted to you (US)",
                "The research notes behind the true crime line"],
         gumroad="", patreon=""),
]

# One time and open ended support. (label, url, note)
ONE_TIME = [
    ("Support the build", "https://jeffreycarrier.gumroad.com/coffee", "Pay what you want, $3 and up, by card"),
    ("PayPal", "https://paypal.me/carrierjeffrey", "Any amount"),
    ("Venmo", "https://account.venmo.com/u/Jeffrey-Carrier-6", "Any amount"),
    ("Support once by card", "", "Stripe"),
    ("Support monthly by card", "", "Stripe, cancel any time"),
]
