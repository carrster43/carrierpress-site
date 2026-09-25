#!/usr/bin/env python3
"""
Regenerate data/us/officeholders.ts from official and open sources.

⚠️ A VERBATIM COPY RUNS WEEKLY ON THE WEBSITE. carrierpress-site carries this
file at vendor/homerule/build-officeholders.py, and its scheduled workflow
(.github/workflows/homerule-officeholders.yml) runs it with --json to publish
the list the app fetches at launch (lib/live.ts). It is a copy because this
repo is private and the site's workflow cannot read it. After changing this
file, copy it there; `npm run check:vendor` says whether the two still match.

Run:  npm run build:officeholders

Three sources, and the difference between them is recorded in the data so the
app can say where a name came from:

  senate.gov ............... the Senate's own contact list. Primary.
  clerk.house.gov .......... the Clerk of the House's member data, plus the
                             Clerk's own member photographs. Primary.
  data.openstates.org ...... Open States' current legislator files, one CSV per
                             state, carrying every state senator and
                             representative with the photograph and links from
                             the legislature's own site. Secondary: Open States
                             compiles it from the states, and the app says so.

Nothing below the state legislature has a national source of any kind. Those
names are read off a county or city's own site and typed one at a time, and
until that happens the app says nobody has recorded who holds the seat.
"""
import csv
import sys
import datetime as dt
import io
import json
import os
import re
import urllib.error
import urllib.request

SENATE = "https://www.senate.gov/general/contact_information/senators_cfm.xml"
HOUSE = "https://clerk.house.gov/xml/lists/MemberData.xml"
STATE_CSV = "https://data.openstates.org/people/current/{}.csv"
HOUSE_PHOTO = "https://clerk.house.gov/content/assets/img/members/{}.jpg"
HOUSE_PAGE = "https://clerk.house.gov/members/{}"
AGENT = {"User-Agent": "HomeRule/0.1 (civic reference app; contact via repository)"}

STATES = """al ak az ar ca co ct de fl ga hi id il in ia ks ky la me md ma mi mn ms mo mt
ne nv nh nj nm ny nc nd oh ok or pa ri sc sd tn tx ut vt va wa wv wi wy dc pr""".split()


def fetch(url):
    request = urllib.request.Request(url, headers=AGENT)
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", "replace")


def tag(block, name):
    match = re.search(rf"<{name}[^>]*>(.*?)</{name}>", block, re.S)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def secure(url):
    """Upgrade http to https.

    659 of the Open States photograph URLs are plain http, and a browser
    silently blocks a mixed-content image on an https page: the portrait simply
    never appears and nothing in the console says why on a production build.
    Every host spot-checked serves the same file over https.
    """
    return re.sub(r"^http://", "https://", url) if url else url


def clean(holder):
    return {k: (secure(v) if k in ("photo", "url") and isinstance(v, str) else v)
            for k, v in holder.items() if v}


def contact(**fields):
    """A contact block with the empty fields dropped, or None if nothing is left.

    Every value comes from the same file as the name beside it, so a phone
    number is exactly as current as the membership list, and no more.
    """
    out = {k: re.sub(r"\s+", " ", v).strip() for k, v in fields.items() if v and v.strip()}
    return out or None


# The Clerk abbreviates the House office buildings. All sit in ZIP 20515.
HOUSE_BUILDINGS = {
    "CHOB": "Cannon House Office Building",
    "LHOB": "Longworth House Office Building",
    "RHOB": "Rayburn House Office Building",
}


def senators():
    """No photograph: every senate.gov image path tried returns an HTML page
    rather than a JPEG, and a broken image is worse than an absent one."""
    out = {}
    for block in re.findall(r"<member>(.*?)</member>", fetch(SENATE), re.S):
        state = tag(block, "state").lower()
        first, last = tag(block, "first_name"), tag(block, "last_name")
        if not state or not last:
            continue
        out.setdefault(f"sen:{state}", []).append(
            clean({
                "name": f"{first} {last}".strip(),
                "party": tag(block, "party"),
                "url": tag(block, "website"),
                "bio": tag(block, "bioguide_id"),
                "src": "senate",
                # <email> is the senator's web contact form, not an address.
                "contact": contact(
                    phone=tag(block, "phone"),
                    address=tag(block, "address"),
                    form=secure(tag(block, "email")) if tag(block, "email").startswith("http") else "",
                ),
            })
        )
    for holders in out.values():
        holders.sort(key=lambda h: h["name"].split()[-1])
    return out


def representatives():
    out = {}
    for block in re.findall(r"<member>(.*?)</member>", fetch(HOUSE), re.S):
        sd = tag(block, "statedistrict")
        if len(sd) < 4:
            continue
        state, number = sd[:2].lower(), sd[2:]
        # At-large seats are 00 here and reach the app as a phrase from the
        # geocoder; both resolve to "0". See districtId() in lib/ocd.ts.
        district = str(int(number)) if number.isdigit() else number.lower()
        bioguide = tag(block, "bioguideID")
        sworn = re.search(r'<sworn-date date="(\d{8})"', block)
        name = tag(block, "official-name") or tag(block, "namelist")
        if not name:
            # The Clerk publishes a VACANT seat as an empty member record.
            # FL-20 and TX-23 were both empty on 2026-09-10. That is a fact
            # worth carrying rather than a row to drop: "this seat is vacant"
            # is a real answer, and dropping it would render as "nobody has
            # recorded who holds this seat", which says the opposite about us.
            out.setdefault(f"rep:{state}:{district}", []).append({"vacant": True, "src": "house"})
            continue
        holder = {
            "name": name,
            "party": tag(block, "party"),
            "bio": bioguide,
            "src": "house",
        }
        if bioguide:
            holder["photo"] = HOUSE_PHOTO.format(bioguide)
            holder["url"] = HOUSE_PAGE.format(bioguide)
        building = HOUSE_BUILDINGS.get(tag(block, "office-building"))
        room = tag(block, "office-room")
        holder["contact"] = contact(
            phone=tag(block, "phone"),
            address=f"{room} {building}, Washington, DC 20515" if building and room else "",
        )
        if sworn:
            d = sworn.group(1)
            holder["since"] = f"{d[:4]}-{d[4:6]}-{d[6:]}"
        out.setdefault(f"rep:{state}:{district}", []).append(clean(holder))
    return out


def district_key(raw):
    """Mirror of districtId() in lib/ocd.ts.

    Open States writes districts the way the legislature does — "Washington-4"
    in Vermont, "B" in Alaska, "30A" in Maryland — and the app slugs them from
    a geocoded name. Both have to land on the same string or a state's whole
    legislature attaches to nothing.
    """
    value = raw.strip()
    if value.isdigit():
        return str(int(value))
    match = re.fullmatch(r"(\d+)([A-Za-z]*)", value)
    if match:
        return str(int(match.group(1))) + match.group(2).lower()
    return re.sub(r"^_+|_+$", "", re.sub(r"[^a-z0-9]+", "_", value.lower()))


def legislators():
    """State senators and representatives, one CSV per state."""
    out = {}
    missing = []
    for state in STATES:
        try:
            body = fetch(STATE_CSV.format(state))
        except (urllib.error.HTTPError, urllib.error.URLError):
            missing.append(state)
            continue
        for row in csv.DictReader(io.StringIO(body)):
            chamber = (row.get("current_chamber") or "").strip()
            district = (row.get("current_district") or "").strip()
            name = (row.get("name") or "").strip()
            if not name or not district or chamber not in ("upper", "lower"):
                continue
            key = district_key(district)
            links = [l for l in (row.get("links") or "").split(";") if l.startswith("http")]
            out.setdefault(f"{'sldu' if chamber == 'upper' else 'sldl'}:{state}:{key}", []).append(
                clean({
                    "name": name,
                    "party": (row.get("current_party") or "").strip(),
                    "photo": (row.get("image") or "").strip(),
                    "url": links[0] if links else "",
                    "src": "openstates",
                    "contact": contact(
                        email=(row.get("email") or "").strip(),
                        phone=(row.get("capitol_voice") or "").strip(),
                        address=(row.get("capitol_address") or "").strip(),
                        districtPhone=(row.get("district_voice") or "").strip(),
                        districtAddress=(row.get("district_address") or "").strip(),
                    ),
                })
            )
    return out, missing


def publish_json(seats, today, path):
    """Write the payload the app fetches at launch (lib/live.ts), or refuse.

    The app accepts a newer file silently, so the refusal has to happen here:
    a partial upstream outage must never look like a wave of resignations.
    Compared against the file being replaced, it refuses when the seat count
    falls by more than 5% or more than 10% of seats change hands at once.
    Refusing exits non-zero, which fails the scheduled workflow and emails
    the repository owner instead of publishing.
    """
    previous = {}
    if os.path.exists(path):
        with open(path) as f:
            previous = json.load(f).get("seats", {})
    if previous:
        names = lambda hs: sorted(h.get("name", "") for h in hs)
        changed = sum(1 for k in set(previous) | set(seats)
                      if names(previous.get(k, [])) != names(seats.get(k, [])))
        if len(seats) < len(previous) * 0.95:
            sys.exit(f"REFUSED: {len(seats)} seats against {len(previous)} last time")
        if changed > len(previous) * 0.10:
            sys.exit(f"REFUSED: {changed} of {len(previous)} seats changed at once")
        print(f"{changed} seats changed since the last published copy")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump({"version": 1, "retrievedAt": today, "seats": dict(sorted(seats.items()))},
                  f, separators=(",", ":"))
    print(f"published {path}")


def main():
    seats = {}
    seats.update(senators())
    seats.update(representatives())
    state_seats, missing = legislators()
    seats.update(state_seats)
    today = dt.date.today().isoformat()

    body = ",\n".join(
        f"  {json.dumps(key)}: {json.dumps(holders)}" for key, holders in sorted(seats.items())
    )
    if "--json" in sys.argv:
        # Publishing mode, run weekly by carrierpress-site. Writes only the JSON.
        publish_json(seats, today, sys.argv[sys.argv.index("--json") + 1])
        return
    path = os.path.join(os.path.dirname(__file__), "..", "data", "us", "officeholders.ts")
    with open(path, "w") as f:
        f.write(HEADER.replace("__DATE__", today) + body + "\n};\n")

    counts = {p: sum(len(v) for k, v in seats.items() if k.startswith(p)) for p in ("sen:", "rep:", "sldu:", "sldl:")}
    people = [h for v in seats.values() for h in v if h.get("name")]
    reach = sum(1 for h in people if h.get("contact"))
    print(f"contact details on {reach} of {len(people)} officeholders")
    print(
        f"{counts['sen:']} senators, {counts['rep:']} representatives, "
        f"{counts['sldu:'] + counts['sldl:']} state legislators, verified {today}"
        + (f" (no file for: {', '.join(missing)})" if missing else "")
    )


HEADER = '''/**
 * Sitting officeholders.
 *
 * ⚠️ GENERATED, and PERISHABLE. Run `npm run build:officeholders` to refresh.
 *
 *   senate.gov ........... the Senate's own contact list
 *   clerk.house.gov ...... the Clerk of the House's member data and photographs
 *   data.openstates.org .. Open States' current legislator files, per state
 *
 * The first two are an institution publishing its own membership, which is as
 * primary as sourcing gets. The third is a compilation from the states rather
 * than a state's own file, so it is marked `openstates` and the app cites it
 * as a secondary source. That distinction is in the data because the app makes
 * it visible: a reader is entitled to know whether a name came from the body
 * that seats the person or from somebody who collected it.
 *
 * Senators carry no photograph. Every senate.gov image path tried returns an
 * HTML page rather than a JPEG, and a broken image is worse than an absent one.
 *
 * Nothing below the state legislature is here, because nothing below it has a
 * national source. Those names are read off a county or city's own site and
 * typed one at a time.
 *
 * RETRIEVED_AT is the date these files were READ, not the date anything was
 * published, and it is the honest answer to "how do you know this is still
 * true": we do not, we know when we last looked. lib/gate.ts turns that into
 * what the screen is allowed to say.
 */

export type HolderSource = "senate" | "house" | "openstates";

export interface FederalHolder {
  /** Absent only when the seat is vacant. */
  readonly name?: string;
  /** The body publishes this seat as vacant. */
  readonly vacant?: boolean;
  /** As the body records it. Never used to sort, filter or colour anything. */
  readonly party?: string;
  /** ISO date sworn in, where the source carries one. */
  readonly since?: string;
  /** Official portrait, from the body's own site. */
  readonly photo?: string;
  /** The officeholder's official page. Never a campaign site. */
  readonly url?: string;
  /** Bioguide id, which joins this person to data/us/record.ts. */
  readonly bio?: string;
  readonly src?: HolderSource;
  /** How to reach them, from the same file as the name. See Contact. */
  readonly contact?: Contact;
}

/**
 * Published contact details. Each field is present only where the source
 * publishes it: the Senate gives a DC office, phone and web form; the Clerk a
 * DC office and phone; Open States whatever each legislature publishes, which
 * ranges from everything to an email address alone.
 */
export interface Contact {
  readonly phone?: string;
  readonly email?: string;
  readonly address?: string;
  /** A web contact form, where the office uses one instead of email. */
  readonly form?: string;
  readonly districtPhone?: string;
  readonly districtAddress?: string;
}

/** The date these records were read from the sources above. */
export const RETRIEVED_AT = "__DATE__";

export const HOLDER_SOURCES: Readonly<Record<HolderSource, { url: string; publisher: string; kind: "primary" | "secondary" }>> = {
  senate: {
    url: "https://www.senate.gov/general/contact_information/senators_cfm.xml",
    publisher: "United States Senate",
    kind: "primary",
  },
  house: {
    url: "https://clerk.house.gov/xml/lists/MemberData.xml",
    publisher: "Clerk of the House of Representatives",
    kind: "primary",
  },
  openstates: {
    url: "https://data.openstates.org/people/current/",
    publisher: "Open States",
    kind: "secondary",
  },
};

export const FEDERAL_OFFICEHOLDERS: Readonly<Record<string, readonly FederalHolder[]>> = {
'''

main()
