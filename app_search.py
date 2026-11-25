#!/usr/bin/env python3
"""
Search titles and snippets for the /apps/<slug>/ landing pages that have no
`seo` block in apps_data.py (author: "fix the app pages metadata too", 2026-11-20).

WHY. The default <title> is "<Name> | Carrier Press", which tells Google nothing
about what the app does, and a blurb over ~155 characters is cut mid-sentence in
the snippet. Each title here leads with what a person would search for and ends
with the app's own name, the same shape as the four apps that already carry
`seo` (Boat Ready, Cast, Endorsed, Who Serves).

WHY NOT `seo` IN apps_data.py. `seo` also turns on the subscribe button, the h1
override and the FAQ block. This changes the <head> and nothing else.

RULES. Titles 65 characters or fewer. Descriptions 155 or fewer, taken from the
app's own blurb (whole sentences, or the blurb's own words shortened), never a
new claim. A description of None keeps the blurb (already short enough).
make_app_pages.py asserts the lengths, so an over-long entry fails the build.
Plan Finder is left out on purpose: Medicare copy holds still stand.
"""

SEARCH = {
    "conceptionzodiac": ("Conception Sign Calculator | Conception Zodiac", None),
    "downpour": ("Rain Sounds for Tabletop RPG Game Masters | Downpour",
                 "Rain for tabletop game masters: on the tavern roof, over a camp in the forest, rolling in as the boss fight starts. Made live in your browser, no loop."),
    "throughthegate": ("Resume Parser Check: What ATS Software Keeps | Through the Gate", None),
    "flare": ("Symptom Tracker for PCOS, Endometriosis, Fibromyalgia | Flare",
              "A symptom log for PCOS, endometriosis, fibromyalgia, autoimmune conditions and perimenopause. Finds what tends to happen together, with a doctor summary."),
    "soleledger": ("Freelancer Bookkeeping, Quarterly Taxes and 1099s | Books for One",
                   "A freelancer's books: income, deductions, quarterly estimates and 1099 reconciliation, with a Rentals section for a landlord's units and Schedule E."),
    "papertrail": ("Receipt, Warranty and Home Maintenance Tracker | Paper Trail",
                   "Receipts, warranties and policies photographed into structured facts, with a calendar reminder before something lapses, and a Home section for upkeep and service."),
    "vetpocket": ("Pet Health Records and Emergency or Wait Answers | Vet Pocket", None),
    "threshold": ("Parental Controls Setup Guide by Child's Age | Threshold",
                  "Every parental control that applies to one child's age, across phones, tablets, computers, consoles, six apps and home internet, in the order that matters."),
    "firstday": ("School Emails to One Calendar, Supply List and Forms | FirstDay", None),
    # 2026-11-20: a log with no health claims (author). No "adherence", and no
    # photo presented as confirming anything.
    "pillproof": ("Medication Log for a Parent, With Family Updates | PillProof",
                  "A medication log for someone you look after: each dose taken or skipped, with the time and whose word it is, plus family updates and appointments."),
    "thebinder": ("If Something Happens File: Will, Accounts, Wishes | The Binder", None),
    "stuck": ("Socratic Homework Help That Never Gives the Answer | Stuck", None),
    "errand": ("AI Errand Assistant That Stops Before You Confirm | Errand", None),
    "quiet": ("Private Offline Journal, No Account and No Sync | Quiet", None),
    "pantry": ("Meal Planner From What Is Already in Your Kitchen | Pantry", None),
    "potluck": ("Neighborhood Lending and Organizing, a Few Blocks Wide | Potluck",
                "Your street's noticeboard for organising and lending. One organiser opens it; each neighbour joins free with the card through their door. No address kept."),
    "fluenthour": ("Daily 10-Minute Spoken Language Practice | Fluent Hour", None),
    "handoff": ("Co-Parenting Calendar, Expense Split and Message Log | Handoff", None),
    "tradedesk": ("Field Service App for One-Person Trade Businesses | Trade Desk",
                  "Field service for one person with a van. Under sixty seconds of admin per job, usable with gloves on, with scope and change orders on each job."),
    "cancelled": ("Find and Cancel Recurring Charges and Subscriptions | Canceled",
                  "Finds every recurring charge in your bank statement, on your own device, ranks them by what they cost you a year, and shows you where to cancel."),
    "homeroom": ("Homeschool Compliance and Portfolio by State | Homeroom", None),
    "waitlist": ("Self-Guided CBT While You Wait for a First Appointment | Waitlist", None),
    "permitpath": ("Permit Checklists and Tracking by Jurisdiction | Permit Path", None),
    "gedcompletion": ("GED Prep, Diagnostic First, Built to Finish | GED Completion",
                      "A GED completion engine, not a question bank. Diagnostic-first, no streaks. Aimed at the roughly forty percent who start testing and never finish."),
    # 2026-11-21: it compares figures the user types and drafts letters of facts,
    # questions and requests; it writes no appeal of its own reasoning.
    "crosscheck": ("Compare a Medical Bill With Your EOB | Crosscheck",
                   "Free to open: type in the figures from a medical bill and your insurer's statement. Crosscheck lists every place the bill and the EOB disagree."),
    # 2026-11-22: the blurb's own words, shortened. Never the trademarked board game's name.
    "spellbright": ("Word Games for Kids 4 to 12, Free in Your Browser | Spellbright",
                    "A word game for children aged 4 to 12, free in your browser: a tile board, crosswords, word search and more, set to a child's age, with help always free."),
    # 2026-11-22: the Author desk is open; no claim about desks not yet open.
    "bench": ("Book Listing Copy and Front Matter for Self-Publishers | Bench",
              "Book listing copy, KDP keywords and front matter for self-publishers, and a desk that plans the errand you keep putting off. It drafts; you send."),
}
