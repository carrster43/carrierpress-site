"""Sprout, the weekly magazine of Carrier Press and Carrier Labs. Settings in ONE place.

    python3 make_sprout.py        # lint every issue, then build /sprout/

THE NAME IS DECIDED: "Sprout" (author 2026-11-20, kept despite BookSprout).
THE LIST IS FREE: no paid tier (author 2026-11-20). Do not re-raise either.
The name is still one constant. Every page, the feed title and the subscribe copy read NAME, so a
rename is this one line plus a rebuild. The URL path is PATH, kept separate on
purpose: renaming the magazine should not break links people already saved.

THE EMAIL SIGNUP IS CONDITIONAL, LIKE THE PLAY LINK. While ML_FORM is None there
is no email form anywhere, only the RSS link, so the site cannot ship a form
that posts to a MailerLite list nobody has created. Creating the group and form
in MailerLite is the author's call (an outward-facing account change); once it
exists, set ML_FORM to its form id and rebuild. Sends are CAMPAIGNS, not
automations, so they do not spend the free plan's 3-automation allowance.
"""

NAME = "Sprout"
PATH = "sprout"                      # carrierpress.com/sprout/
TAGLINE = "What grew this week at Carrier Press and Carrier Labs."
CADENCE = "Every Friday"

# MailerLite account (same as the picker). ML_FORM: None until the author
# approves creating a "Sprout" group and its embedded form.
ML_ACCOUNT = "2504319"
ML_FORM = "204676981464237712"   # "Sprout: weekly magazine", group "Sprout" 204676955919877751, created 2026-11-20 (author "Yes, do both"); double opt-in ON

# House rules a published issue must pass (make_sprout.lint). Each entry is
# (regex, why). Matching is case-insensitive. These come from the standing
# rules in memory, not taste: break one and the build stops.
BANNED = [
    (r"[–—]", "no em or en dashes in any copy"),
    (r"\s--\s", "no double-hyphen dash substitutes"),
    (r"best[- ]?sell", "no 'best seller' without data"),
    (r"\bkindle\b.{0,40}\$\d", "promote print: no Kindle prices"),
    # Case-sensitive on purpose: "the hold cleared" is English, "Cleared" is the old app.
    (r"(?-i:\b(Cleared|Titrate|Doorstop|House Ledger|Perimeter)\b)",
     "customers never see old app names"),
    (r"kids future fund|\bKFF\b", "never connect KFF to Carrier Press"),
    (r"medicare|annuit", "Medicare and annuity work never appear here"),
    (r"\bfree (copy|copies|book)s? for (a |an )?review", "no free anything for reviews"),
]

# The AI note. House rule (author 2026-11-14): it stays, on the LAST line of the
# page, never the first. The builder appends it, so an issue never carries it.
AI_NOTE = ("Sprout is drafted with AI tools and read by Jeffrey L. Carrier "
           "before it goes out.")
