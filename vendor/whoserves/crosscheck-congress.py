#!/usr/bin/env python3
"""Cross-check the published Congress seats against Congress.gov's member list.

Run:  CONGRESS_API_KEY=... python3 scripts/crosscheck-congress.py <officeholders.json>

The seats come from the chambers themselves (the House Clerk's member data and
the Senate's contact list, scripts/build-officeholders.py). Congress.gov, the
Library of Congress, is a second, independent list of the same people. This is
the accuracy audit's second-source rule applied to Congress: two lists that
agree are a stronger answer than one, and a disagreement is a lead to check
by hand, never a correction applied automatically.

It changes nothing. It prints every disagreement and exits 1 when there is
one, so the weekly job's failure email is the alert. It runs AFTER the feed is
published, so a disagreement can never hold back a week's data.

Compared per seat: who holds it (bioguide id) and their party's first letter.
A seat the chamber lists as vacant is expected to have no current member.
docs/congress-gov-api.md.
"""
import json
import os
import sys
import urllib.request

API = "https://api.congress.gov/v3/member"
AGENT = {"User-Agent": "HomeRule/0.1 (civic reference app; contact via repository)"}

STATES = {
    "Alabama": "al", "Alaska": "ak", "Arizona": "az", "Arkansas": "ar", "California": "ca",
    "Colorado": "co", "Connecticut": "ct", "Delaware": "de", "Florida": "fl", "Georgia": "ga",
    "Hawaii": "hi", "Idaho": "id", "Illinois": "il", "Indiana": "in", "Iowa": "ia",
    "Kansas": "ks", "Kentucky": "ky", "Louisiana": "la", "Maine": "me", "Maryland": "md",
    "Massachusetts": "ma", "Michigan": "mi", "Minnesota": "mn", "Mississippi": "ms",
    "Missouri": "mo", "Montana": "mt", "Nebraska": "ne", "Nevada": "nv", "New Hampshire": "nh",
    "New Jersey": "nj", "New Mexico": "nm", "New York": "ny", "North Carolina": "nc",
    "North Dakota": "nd", "Ohio": "oh", "Oklahoma": "ok", "Oregon": "or", "Pennsylvania": "pa",
    "Rhode Island": "ri", "South Carolina": "sc", "South Dakota": "sd", "Tennessee": "tn",
    "Texas": "tx", "Utah": "ut", "Vermont": "vt", "Virginia": "va", "Washington": "wa",
    "West Virginia": "wv", "Wisconsin": "wi", "Wyoming": "wy",
    "District of Columbia": "dc", "Puerto Rico": "pr", "Guam": "gu", "American Samoa": "as",
    "Northern Mariana Islands": "mp", "Virgin Islands": "vi",
}


def fetch(url):
    request = urllib.request.Request(url, headers=AGENT)
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def current_members(key):
    """Every current member, from Congress.gov, in pages of 250."""
    out, offset = [], 0
    while True:
        page = fetch(f"{API}?currentMember=true&limit=250&offset={offset}&format=json&api_key={key}")
        items = page.get("members", [])
        out += items
        if len(items) < 250:
            return out
        offset += 250


def seat_of(member):
    """'sen:al' or 'rep:ca:14', the same ids the officeholder feed uses; '' if unplaceable."""
    state = STATES.get(member.get("state", ""))
    terms = (member.get("terms") or {}).get("item") or []
    if not state or not terms:
        return ""
    if terms[-1].get("chamber") == "Senate":
        return f"sen:{state}"
    return f"rep:{state}:{int(member.get('district') or 0)}"


def compare(seats, members):
    """Disagreements, as sentences a person can check. Empty when the two lists agree."""
    theirs, problems = {}, []
    for member in members:
        seat = seat_of(member)
        if seat:
            theirs.setdefault(seat, {})[member.get("bioguideId", "")] = (member.get("partyName") or "?")[:1]
        else:
            problems.append(f"Congress.gov lists {member.get('name')} ({member.get('bioguideId')}) with no seat we can place")

    ours_ids = set()
    for seat, holders in sorted(seats.items()):
        if not seat.startswith(("sen:", "rep:")):
            continue
        listed = theirs.get(seat, {})
        for holder in holders:
            if holder.get("vacant"):
                if listed:
                    problems.append(f"{seat}: the chamber lists it vacant, Congress.gov lists {sorted(listed)}")
                continue
            bio = holder.get("bio", "")
            ours_ids.add(bio)
            if bio not in listed:
                problems.append(f"{seat}: {holder.get('name')} ({bio}) is not a current member here on Congress.gov (it lists {sorted(listed) or 'nobody'})")
            elif listed[bio] != (holder.get("party") or "?")[:1]:
                problems.append(f"{seat}: {holder.get('name')} party {holder.get('party')} here, {listed[bio]} on Congress.gov")
    for seat, listed in sorted(theirs.items()):
        for bio in sorted(listed):
            if bio not in ours_ids:
                problems.append(f"{seat}: Congress.gov lists {bio} as a current member, the chamber's list does not")
    return problems


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: crosscheck-congress.py <officeholders.json>")
    key = os.environ.get("CONGRESS_API_KEY", "")
    if not key:
        print("CONGRESS_API_KEY not set: cross-check skipped.")
        return
    with open(sys.argv[1]) as f:
        seats = json.load(f)["seats"]
    members = current_members(key)
    problems = compare(seats, members)
    congress = sum(len(v) for k, v in seats.items() if k.startswith(("sen:", "rep:")))
    print(f"{congress} Congress seats checked against {len(members)} Congress.gov members: {len(problems)} disagreements")
    for line in problems:
        print("  " + line)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
