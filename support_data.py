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

# The Carrier Press BUSINESS PayPal (opened 2026-10-27), a customer set price link,
# not the personal paypal.me. PAYPAL_QR is the same link as a scannable code,
# regenerate it if the link ever changes.
PAYPAL_URL = "https://www.paypal.com/ncp/payment/MZFRVK76XEPG2"
PAYPAL_QR = "/assets/paypal-support-qr.svg"

# Spritz Finance referral. Empty until Jeffrey supplies his code or link.
SPRITZ_URL = ""

# Monthly support. A GIFT, nothing promised in return: no perks, no tiers, nothing
# Jeffrey has to deliver (his word 2026-10-28). Paid access lives in the apps and
# the access ladder, never here. PayPal product PROD-7HN187780H641835W. (amount, url)
PAYPAL_SUB = "https://www.paypal.com/webapps/billing/plans/subscribe?plan_id=%s"
MONTHLY = [
    ("$3", PAYPAL_SUB % "P-9P8147312P7461713NLRDMCI"),
    ("$8", PAYPAL_SUB % "P-5AA50429TV363310YNLRDMTQ"),
    ("$25", PAYPAL_SUB % "P-03F23745DX767632ENLRDNEI"),
]

# One time and open ended support. (label, url, note)
ONE_TIME = [
    ("Support the build", "https://jeffreycarrier.gumroad.com/coffee", "Pay what you want, $3 and up, by card"),
    ("PayPal", PAYPAL_URL, "Any amount"),
    ("Venmo", "https://account.venmo.com/u/Jeffrey-Carrier-6", "Any amount"),
    ("Support once by card", "", "Stripe"),
    ("Support monthly by card", "", "Stripe, cancel any time"),
]
