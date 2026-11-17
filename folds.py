#!/usr/bin/env python3
"""
Apps folded into a host app. One place, read by every generator that writes an
app's pages.

THE DECISION (author, 2026-11-16, "approval all"; settled 2026-11-17, "Yes, all
five"; Documents/APP_MERGE_MAP_2026-11-16.md). Each folded app is now a section
of its host, built in the host's own repo:

    Perimeter     -> Flare        the Perimenopause section
    Relay         -> PillProof    the family Updates feed and Appointments
    Third Place   -> Potluck      recurring gatherings
    Porchlight    -> Potluck      the October door map
    Scope         -> Trade Desk   scope and change orders on each job
    Signal Check  -> Threshold    the Agreement, after setup, for teenagers

WHAT THAT DOES TO THE SITE.

    /apps/          the folded rows drop out of the list and out of every count
                    (apps_data.LISTED). The rows stay in apps_data.APPS as the
                    record of what each app was.
    /apps/<slug>/   a noindex redirect stub to the host's landing page
                    (make_app_pages.py). Pages has no server redirects.
    /<slug>/        the support page: a stub to the host's (make_support.py).
    /<slug>/privacy/  a stub to the host's privacy page (make_privacy.py).

A stub declares the host as canonical and says noindex, so build.py's sitemap
drops it by the rule it already applies to /homerule/.

⚠️ PERIMETER KEEPS A REAL /apps/perimeter/ PAGE. Its founding access product
is still on sale (commerce.PRESALE["perimeter"], author 2026-11-17), now worded
as opening Flare, including its Perimenopause section. A buyer needs a page that
says what the $2.99 buys, so that one page is not redirected. Its support and
privacy pages are, because those belong to the app, and the app is Flare now.

Titrate and Doorstop are NOT here. Each also lives on inside a host (Flare's
Doses section, Books for One's Rentals section), but both stay their own live
web products with their own keys, so their pages stay.
"""
import html

DOMAIN = "carrierpress.com"

# slug -> (host slug, host name, the one sentence a stub and a page say).
FOLDED = {
    "perimeter": ("flare", "Flare",
                  "Perimeter is now part of Flare, as its Perimenopause section."),
    "relay": ("pillproof", "PillProof",
              "Relay is now part of PillProof, as its family Updates feed and Appointments."),
    "thirdplace": ("potluck", "Potluck",
                   "Third Place is now part of Potluck, as its recurring gatherings."),
    "porchlight": ("potluck", "Potluck",
                   "Porchlight is now part of Potluck, as its October map of the doors giving out treats."),
    "scope": ("tradedesk", "Trade Desk",
              "Scope is now part of Trade Desk, as the scope and change orders on each job."),
    "signalcheck": ("threshold", "Threshold",
                    "Signal Check is now part of Threshold, as its Agreement section for teenagers."),
}

# Folded, but its landing page stays a page (see the docstring).
KEEP_LANDING = {"perimeter"}


def host(slug):
    return FOLDED[slug][0]


def host_name(slug):
    return FOLDED[slug][1]


def moved(slug):
    return FOLDED[slug][2]


STUB = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<link rel="canonical" href="https://{domain}{to}">
<meta http-equiv="refresh" content="0; url={to}">
<script>location.replace("{to}" + location.search + location.hash);</script>
</head><body style="font-family:system-ui,sans-serif;padding:24px">
<p>{moved} This page has moved to <a href="{to}">{domain}{to}</a>.</p>
</body></html>
"""


def stub(slug, to, what=""):
    """The redirect page for a folded app. `to` is a site path ending in /."""
    title = "%s is now part of %s" % (_name(slug), host_name(slug))
    if what:
        title = "%s %s" % (_name(slug), what)
        title = "%s: now part of %s" % (title, host_name(slug))
    return STUB.format(title=html.escape(title), domain=DOMAIN, to=to,
                       moved=html.escape(moved(slug)))


def _name(slug):
    # The folded app's own name is the first words of its sentence.
    return moved(slug).split(" is now part of ")[0]
