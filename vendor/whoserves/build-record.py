#!/usr/bin/env python3
"""Regenerate data/us/record.ts: what members of Congress have actually done.

Run:  npm run build:record

This is the claim gate's half of the app. The original sketch for Home Rule
asked for "pros and cons" on each official; docs/claim-gate.md explains why
that became the sourced record instead, and this is the file that makes the
record real rather than a promise.

Four things, all from the institution that produced them:

  committees ....... clerk.house.gov member data. What a member actually sits
                     on, which is where most of the work of Congress happens
                     and which almost no voter could name.
  votes ............ clerk.house.gov roll call XML and senate.gov roll call
                     XML. How this person voted, with the question, the bill
                     and the official page for the whole tally.
  disclosures ...... disclosures-clerk.house.gov annual financial disclosure
                     index. LINKED, never summarised: the app points at the
                     filing and lets the reader read it.

Nothing here is characterised, scored, ranked or totalled. A vote is a vote and
the reader draws the conclusion.
"""
import collections
import datetime as dt
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile

HOUSE = "https://clerk.house.gov/xml/lists/MemberData.xml"
SENATE = "https://www.senate.gov/general/contact_information/senators_cfm.xml"
HOUSE_ROLL = "https://clerk.house.gov/evs/{year}/roll{roll:03d}.xml"
HOUSE_ROLL_PAGE = "https://clerk.house.gov/Votes/{year}{roll}"
SENATE_MENU = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_{c}_{s}.xml"
SENATE_VOTE = "https://www.senate.gov/legislative/LIS/roll_call_votes/vote{c}{s}/vote_{c}_{s}_{n:05d}.xml"
FD_ZIP = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip"
FD_PDF = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc}.pdf"
AGENT = {"User-Agent": "HomeRule/0.1 (civic reference app; contact via repository)"}

CONGRESS, SESSION = 119, 2
VOTE_YEAR = dt.date.today().year
# Both counts are per chamber. RECENT is every recorded vote (the 1.0 list,
# procedure included); DECISIONS is the On the Record list, chosen by the rule
# below and by nothing else. docs/specs/ON_THE_RECORD_1_1.md, decision C.
RECENT = 20
DECISIONS = 25
# A floor for how far back the walk goes looking for 25 decisions, so a source
# outage cannot turn into a thousand requests.
MAX_HOUSE_FETCHES = 600

# ── The decision rule ────────────────────────────────────────────────────────
#
# A vote is a DECISION when the chamber's OWN question wording, exactly as it
# prints it, is a final decision on a measure or a nomination. Nobody judges
# which votes matter; the list below is the whole of the judgement, it is
# published in the spec, and it applies whatever the result (decision A).
# Procedure (cloture, motions to proceed, to table, to recommit, the previous
# question, amendments, quorum calls) stays in the full list and out of this one.
HOUSE_DECISION = re.compile(
    r"^On (Passage"
    r"|Motion to Suspend the Rules and (Pass|Agree|Concur)\b.*"
    r"|Agreeing to the Resolution(, as Amended)?"
    r"|Agreeing to the Conference Report"
    r"|Agreeing to the Senate Amendments?"
    r"|Motion to Concur in the Senate Amendments?\b.*"
    r"|Concurring in the Senate Amendments?\b.*"
    r"|Overriding the Veto)$"
)
SENATE_DECISION = re.compile(
    r"^On (Passage of the Bill"
    r"|the Joint Resolution"
    r"|the Resolution"
    r"|the Concurrent Resolution"
    r"|the Conference Report"
    r"|the Nomination"
    r"|the Resolution of Ratification"
    r"|Overriding the Veto"
    r"|the Motion to Concur\b.*)$"
)

# ── Where the recording of a vote lives ──────────────────────────────────────
#
# Only sources that are US government work (17 USC 105), and only as LINKS:
# nothing is downloaded, clipped or re-served. C-SPAN's own footage is never a
# source (it is theirs, and this app is sold). See the spec, section 1.
#
#   House floor ...... HouseLive, the Clerk's own floor video, by legislative
#                      day. Its floor file states "Pursuant to Title 17 Section
#                      105 ... in the public domain". It takes ?date= only, so
#                      the vote's time is shown beside the link, not seeked to.
#   Senate floor ..... NONE. floor.senate.gov no longer resolves and senate.gov
#                      points past floor video at C-SPAN, so per decision E a
#                      Senate row links its tally and any committee video only.
#   Committee ........ congress.gov committee-meeting records, and only a
#                      meeting that names this bill or nomination itself and
#                      lists a congress.gov video. Never a title or keyword
#                      match. Needs CONGRESS_API_KEY; without it this is skipped
#                      and nothing else changes.
HOUSE_FLOOR_VIDEO = "https://live.house.gov/?date={date}"
CONGRESS_API = "https://api.congress.gov/v3"
MEETING_CACHE = os.path.join(os.path.dirname(__file__), "cache", "committee-meetings.json")
BILL_PAGE = {
    "HR": "house-bill", "HRES": "house-resolution", "HJRES": "house-joint-resolution",
    "HCONRES": "house-concurrent-resolution", "S": "senate-bill", "SRES": "senate-resolution",
    "SJRES": "senate-joint-resolution", "SCONRES": "senate-concurrent-resolution",
}
MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

FILING_TYPE = {
    "O": "Original filing",
    "A": "Annual report",
    "C": "Candidate report",
    "D": "Disclosure",
    "P": "Periodic transaction report",
    "T": "Termination report",
    "X": "Filing extension",
}


def fetch(url, binary=False):
    request = urllib.request.Request(url, headers=AGENT)
    with urllib.request.urlopen(request, timeout=45) as response:
        raw = response.read()
    return raw if binary else raw.decode("utf-8", "replace")


def tag(block, name):
    match = re.search(rf"<{name}[^>]*>(.*?)</{name}>", block, re.S)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def committees_and_ids():
    """bioguide -> [committee names], plus state-district and name indexes."""
    xml = fetch(HOUSE)

    names = {}
    for block in re.findall(r"<committee\b(.*?)</committee>", xml, re.S):
        code = re.search(r'comcode="([^"]+)"', block)
        full = re.search(r"<committee-fullname>(.*?)</committee-fullname>", block, re.S)
        if code and full:
            names[code.group(1)] = re.sub(r"\s+", " ", full.group(1)).strip()
    for block in re.findall(r"<subcommittee\b(.*?)</subcommittee>", xml, re.S):
        code = re.search(r'subcomcode="([^"]+)"', block)
        full = re.search(r"<subcommittee-fullname>(.*?)</subcommittee-fullname>", block, re.S)
        if code and full:
            names[code.group(1)] = re.sub(r"\s+", " ", full.group(1)).strip()

    served = {}
    by_district = {}
    for member in re.findall(r"<member>(.*?)</member>", xml, re.S):
        bioguide = tag(member, "bioguideID")
        if not bioguide:
            continue
        by_district[tag(member, "statedistrict")] = (bioguide, tag(member, "lastname"))
        assignments = re.search(r"<committee-assignments>(.*?)</committee-assignments>", member, re.S)
        if not assignments:
            continue
        seats = []
        for kind, attrs in re.findall(r"<(committee|subcommittee)\s+([^/>]*)/>", assignments.group(1)):
            code = re.search(r'(?:sub)?comcode="([^"]+)"', attrs)
            if not code or code.group(1) not in names:
                continue
            role = re.search(r'leadership="([^"]+)"', attrs)
            label = names[code.group(1)]
            seats.append(f"{label} — {role.group(1)}" if role else label)
        if seats:
            served[bioguide] = seats
    return served, by_district


def senate_ids():
    """(state, lastname) -> bioguide, for joining Senate roll calls."""
    out = {}
    for block in re.findall(r"<member>(.*?)</member>", fetch(SENATE), re.S):
        bioguide = tag(block, "bioguide_id")
        if bioguide:
            out[(tag(block, "state").upper(), tag(block, "last_name").lower())] = bioguide
    return out


def question_of(raw):
    """The chamber's question, with the Senate's inline <measure> tag removed."""
    return re.sub(r"\s+", " ", re.sub(r"<measure>.*?</measure>", "", raw, flags=re.S)).strip()


def measure_key(text):
    """'H R 8800', 'H.R. 9340', 'S.J.Res. 5', 'PN1129' -> 'HR8800', 'HR9340', 'SJRES5', 'PN1129'."""
    key = re.sub(r"[^A-Z0-9]", "", (text or "").upper())
    return key if re.fullmatch(r"(HR|HRES|HJRES|HCONRES|S|SRES|SJRES|SCONRES|PN)\d+", key) else ""


def measure_page(key):
    """The congress.gov page for a bill or nomination: text, actions, and the CRS summary."""
    match = re.fullmatch(r"([A-Z]+)(\d+)", key)
    if not match:
        return ""
    kind, number = match.groups()
    if kind == "PN":
        return f"https://www.congress.gov/nomination/{CONGRESS}th-congress/{number}"
    return f"https://www.congress.gov/bill/{CONGRESS}th-congress/{BILL_PAGE[kind]}/{number}"


def iso_day(clerk_date):
    """'22-Jul-2026' -> '2026-07-22'."""
    day, month, year = clerk_date.split("-")
    return f"{year}-{MONTHS[month[:3]]:02d}-{int(day):02d}"


def vote_years():
    """Calendar years of the current Congress so far, newest first."""
    return [VOTE_YEAR, VOTE_YEAR - 1] if SESSION == 2 else [VOTE_YEAR]


def latest_house_roll(year):
    """The Clerk publishes no machine-readable index, so probe for the top.

    A roll that does not exist yet comes back 200 with a 65-byte empty body
    (seen 2026-10-18), so a status code alone says nothing. A roll exists only
    if its body carries vote metadata.
    """
    low, high = 0, 999
    while low < high:
        mid = (low + high + 1) // 2
        try:
            exists = "<vote-metadata>" in fetch(HOUSE_ROLL.format(year=year, roll=mid))[:4000]
        except Exception:
            exists = False
        if exists:
            low = mid
        else:
            high = mid - 1
    return low


def house_votes(positions):
    """Newest first: every roll until RECENT are kept, then decisions until DECISIONS are."""
    kept_all = kept_decisions = fetched = 0
    for year in vote_years():
        for roll in range(latest_house_roll(year), 0, -1):
            if (kept_all >= RECENT and kept_decisions >= DECISIONS) or fetched >= MAX_HOUSE_FETCHES:
                return
            fetched += 1
            try:
                xml = fetch(HOUSE_ROLL.format(year=year, roll=roll))
            except Exception:
                continue
            meta = re.search(r"<vote-metadata>(.*?)</vote-metadata>", xml, re.S)
            if not meta:
                continue
            block = meta.group(1)
            question = question_of(tag(block, "vote-question"))
            decision = bool(HOUSE_DECISION.match(question))
            in_recent = kept_all < RECENT
            if not in_recent and not (decision and kept_decisions < DECISIONS):
                continue
            kept_all += 1
            kept_decisions += decision
            roll_id = f"h{year}-{roll}"
            date = tag(block, "action-date")
            time = re.search(r"<action-time[^>]*>(.*?)</action-time>", block, re.S)
            yield roll_id, {
                "chamber": "House",
                "date": date,
                "question": question,
                "desc": tag(block, "vote-desc") or tag(block, "amendment-author"),
                "bill": tag(block, "legis-num"),
                "result": tag(block, "vote-result"),
                "url": HOUSE_ROLL_PAGE.format(year=year, roll=roll),
                "decision": decision,
                "recent": in_recent,
                "time": f"{time.group(1).strip()} ET" if time else "",
                "media": [{
                    "kind": "floor",
                    "label": "House floor video",
                    "url": HOUSE_FLOOR_VIDEO.format(date=iso_day(date)),
                    "by": "Office of the Clerk, U.S. House of Representatives",
                }],
            }
            for record in re.findall(r"<recorded-vote>(.*?)</recorded-vote>", xml, re.S):
                who = re.search(r'name-id="([^"]+)"', record)
                cast = tag(record, "vote")
                if who and cast:
                    positions[who.group(1)].append([roll_id, cast])


def senate_votes(ids, positions):
    """Same rule as the House. The menu carries each question, so only kept votes are fetched."""
    chosen = []
    kept_decisions = 0
    for session in ([2, 1] if SESSION == 2 else [1]):
        try:
            menu = fetch(SENATE_MENU.format(c=CONGRESS, s=session))
        except Exception:
            continue
        for block in re.findall(r"<vote>(.*?)</vote>", menu, re.S):
            number = int(tag(block, "vote_number") or 0)
            decision = bool(SENATE_DECISION.match(question_of(tag(block, "question"))))
            in_recent = len(chosen) < RECENT
            if in_recent or (decision and kept_decisions < DECISIONS):
                chosen.append((session, number, decision, in_recent))
                kept_decisions += decision
            if len(chosen) >= RECENT and kept_decisions >= DECISIONS:
                break
        if len(chosen) >= RECENT and kept_decisions >= DECISIONS:
            break

    for session, number, decision, in_recent in chosen:
        try:
            xml = fetch(SENATE_VOTE.format(c=CONGRESS, s=session, n=number))
        except Exception:
            continue
        roll_id = f"s{CONGRESS}-{session}-{number}"
        date = tag(xml, "vote_date").split(",")[0]
        yield roll_id, {
            "chamber": "Senate",
            "date": date,
            "question": question_of(tag(xml, "question")),
            "desc": tag(xml, "vote_title") or tag(xml, "vote_document_text"),
            "bill": tag(xml, "document_name"),
            "result": tag(xml, "vote_result"),
            "url": f"https://www.senate.gov/legislative/LIS/roll_call_votes/vote{CONGRESS}{session}/vote_{CONGRESS}_{session}_{number:05d}.htm",
            "decision": decision,
            "recent": in_recent,
            "media": [],
        }
        for member in re.findall(r"<member>(.*?)</member>", xml, re.S):
            bioguide = ids.get((tag(member, "state").upper(), tag(member, "last_name").lower()))
            cast = tag(member, "vote_cast")
            if bioguide and cast:
                positions[bioguide].append([roll_id, cast])


def api(path, key, **params):
    query = "&".join(f"{k}={v}" for k, v in {"format": "json", "api_key": key, **params}.items())
    return json.loads(fetch(f"{CONGRESS_API}{path}?{query}"))


def committee_videos(wanted, key):
    """measure key -> committee meetings that name it and have a congress.gov video.

    A meeting is fetched once and then only when congress.gov says it changed
    (its updateDate), so the weekly run is a few list pages plus whatever is
    new, not 2,800 requests. The cache is public data and lives beside this
    script.
    """
    try:
        with open(MEETING_CACHE) as f:
            cache = json.load(f)
    except (OSError, ValueError):
        cache = {}

    offset = 0
    while True:
        page = api(f"/committee-meeting/{CONGRESS}", key, limit=250, offset=offset)
        items = page.get("committeeMeetings", [])
        for item in items:
            event = f"{item['chamber']}/{item['eventId']}"
            if cache.get(event, {}).get("u") == item.get("updateDate"):
                continue
            try:
                detail = api(f"/committee-meeting/{CONGRESS}/{item['chamber'].lower()}/{item['eventId']}", key)
            except Exception:
                continue
            meeting = detail.get("committeeMeeting", {})
            related = meeting.get("relatedItems") or {}
            names = [measure_key(f"{b.get('type', '')}{b.get('number', '')}") for b in related.get("bills") or []]
            names += [measure_key(f"PN{n.get('number', '')}") for n in related.get("nominations") or []]
            video = next(
                (v.get("url", "") for v in meeting.get("videos") or []
                 if v.get("url", "").startswith("https://www.congress.gov/")),
                "",
            )
            committees = meeting.get("committees") or [{}]
            cache[event] = {
                "u": item.get("updateDate"),
                "m": sorted(n for n in names if n),
                "v": video,
                "d": (meeting.get("date") or "")[:10],
                "t": meeting.get("type") or "Meeting",
                "c": committees[0].get("name", ""),
            }
        if len(items) < 250:
            break
        offset += 250

    os.makedirs(os.path.dirname(MEETING_CACHE), exist_ok=True)
    with open(MEETING_CACHE, "w") as f:
        json.dump(cache, f, sort_keys=True, separators=(",", ":"))

    out = collections.defaultdict(list)
    for entry in sorted(cache.values(), key=lambda e: e["d"], reverse=True):
        if not entry["v"]:
            continue
        for name in entry["m"]:
            if name in wanted and len(out[name]) < 2:
                out[name].append({
                    "kind": "committee",
                    "label": f"{entry['c']} {entry['t'].lower()}, {entry['d']}".strip(),
                    "url": entry["v"],
                    "by": "Congress.gov, Library of Congress",
                })
    return out


def measure_facts(wanted, key):
    """measure key -> what congress.gov says about the bill or nomination today.

    One request per measure: the display title, the latest action verbatim with
    its date, the sponsor, and whether a CRS summary exists (so the link never promises a
    summary that is not there). Copied as the source prints them, never
    rewritten. A failed request leaves that measure without these lines.
    docs/congress-gov-api.md.
    """
    out = {}
    for name in sorted(wanted):
        match = re.fullmatch(r"([A-Z]+)(\d+)", name)
        if not match:
            continue
        kind, number = match.groups()
        try:
            if kind == "PN":
                item = api(f"/nomination/{CONGRESS}/{number}", key).get("nomination", {})
                title, crs = item.get("description", ""), False
            else:
                item = api(f"/bill/{CONGRESS}/{kind.lower()}/{number}", key).get("bill", {})
                title = item.get("title", "")
                crs = int((item.get("summaries") or {}).get("count") or 0) > 0
                sponsor = ((item.get("sponsors") or [{}])[0] or {}).get("bioguideId", "")
        except Exception:
            continue
        facts = {}
        title = re.sub(r"\s+", " ", title or "").strip()
        if title:
            facts["title"] = title[:400]
        latest = item.get("latestAction") or {}
        text = re.sub(r"\s+", " ", latest.get("text") or "").strip()
        day = (latest.get("actionDate") or "")[:10]
        if text and re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
            facts["latestAction"] = {"date": day, "text": text[:400]}
        if kind != "PN":
            facts["crsSummary"] = crs
            # Who introduced it, so a member's page can list the bills they
            # sponsored that came to a recorded vote. Nothing else is inferred.
            if re.fullmatch(r"[A-Z]\d{6}", sponsor):
                facts["sponsor"] = sponsor
        if facts:
            out[name] = facts
    return out


def disclosures(by_district):
    """Filings are LINKED, never parsed into claims. The app points at the PDF."""
    out = collections.defaultdict(list)
    for year in (dt.date.today().year, dt.date.today().year - 1):
        try:
            archive = zipfile.ZipFile(io.BytesIO(fetch(FD_ZIP.format(year=year), binary=True)))
        except Exception:
            continue
        inner = [n for n in archive.namelist() if n.endswith(".xml")]
        if not inner:
            continue
        xml = archive.read(inner[0]).decode("utf-8", "replace")
        for record in re.findall(r"<Member>(.*?)</Member>", xml, re.S):
            district = tag(record, "StateDst")
            doc = tag(record, "DocID")
            known = by_district.get(district)
            if not known or not doc:
                continue
            bioguide, lastname = known
            if tag(record, "Last").lower() != lastname.lower():
                continue
            out[bioguide].append({
                "year": tag(record, "Year"),
                "type": FILING_TYPE.get(tag(record, "FilingType"), "Filing"),
                "date": tag(record, "FilingDate"),
                "url": FD_PDF.format(year=tag(record, "Year") or year, doc=doc),
            })
    return out


def main():
    args = sys.argv[1:]
    json_out = args[args.index("--json") + 1] if "--json" in args else ""
    global MEETING_CACHE
    if "--cache" in args:
        MEETING_CACHE = args[args.index("--cache") + 1]

    served, by_district = committees_and_ids()
    ids = senate_ids()

    positions = collections.defaultdict(list)
    rolls = {}
    for roll_id, meta in house_votes(positions):
        rolls[roll_id] = meta
    for roll_id, meta in senate_votes(ids, positions):
        rolls[roll_id] = meta

    # The bill or nomination page on congress.gov: its text, its actions and,
    # where one exists, the Congressional Research Service summary. Linked,
    # never paraphrased.
    for meta in rolls.values():
        page = measure_page(measure_key(meta["bill"]))
        if page:
            meta["billUrl"] = page

    key = os.environ.get("CONGRESS_API_KEY", "")
    videos = 0
    if key:
        wanted = {measure_key(m["bill"]) for m in rolls.values()} - {""}
        found = committee_videos(wanted, key)
        for meta in rolls.values():
            extra = found.get(measure_key(meta["bill"]), [])
            meta["media"] = meta["media"] + extra
            videos += len(extra)
        facts = measure_facts(wanted, key)
        for meta in rolls.values():
            meta.update(facts.get(measure_key(meta["bill"]), {}))
    else:
        facts = {}
        print("CONGRESS_API_KEY not set: committee video and bill status skipped, everything else built.")

    filings = disclosures(by_district)

    record = {}
    for bioguide in set(served) | set(positions) | set(filings):
        entry = {}
        if served.get(bioguide):
            entry["committees"] = served[bioguide]
        if positions.get(bioguide):
            entry["votes"] = positions[bioguide]
        if filings.get(bioguide):
            entry["filings"] = filings[bioguide][:6]
        if entry:
            record[bioguide] = entry

    today = dt.date.today().isoformat()
    if json_out:
        with open(json_out, "w") as f:
            json.dump(
                {"version": 1, "retrievedAt": today, "rolls": rolls, "members": record},
                f, sort_keys=True, separators=(",", ":"),
            )
    else:
        body = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in sorted(record.items()))
        meta = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in sorted(rolls.items()))
        path = os.path.join(os.path.dirname(__file__), "..", "data", "us", "record.ts")
        with open(path, "w") as f:
            f.write(
                HEADER.replace("__DATE__", today)
                + meta
                + "\n};\n\nexport const MEMBER_RECORD: Readonly<Record<string, MemberRecord>> = {\n"
                + body
                + "\n};\n"
            )

    print(
        f"{len(record)} members: {sum(1 for v in record.values() if 'committees' in v)} with committees, "
        f"{sum(len(v.get('votes', [])) for v in record.values())} vote positions across {len(rolls)} roll calls "
        f"({sum(1 for r in rolls.values() if r['decision'])} decisions), "
        f"{sum(len(v.get('filings', [])) for v in record.values())} filings, {videos} committee videos, "
        f"{len(facts)} measures with congress.gov status"
    )


HEADER = '''/**
 * The record: what members of Congress have actually done.
 *
 * ⚠️ GENERATED, and PERISHABLE. Run `npm run build:record` to refresh.
 *
 *   clerk.house.gov ................. committee assignments and roll calls
 *   senate.gov ...................... roll calls
 *   disclosures-clerk.house.gov ..... annual financial disclosure filings
 *   api.congress.gov ................ committee video, bill title and status
 *
 * This is the claim gate's half of the app. The original sketch asked for
 * "pros and cons" on each official; docs/claim-gate.md explains why that became
 * the sourced record instead, and this file is what makes the record real
 * rather than a promise.
 *
 * Nothing here is characterised, scored, ranked or totalled. A vote is a vote,
 * with its question, its bill and a link to the whole tally. A filing is
 * LINKED and never summarised: the app points at the PDF and lets the reader
 * read it, because a summary of a financial disclosure is an assertion about a
 * person's money and the filing itself is a public record.
 *
 * Roll calls are stored once and referenced by id, because 441 members voting
 * on the same twenty questions is twenty questions, not 8,820.
 */

export interface RollCall {
  readonly chamber: "House" | "Senate";
  readonly date: string;
  readonly question: string;
  readonly desc: string;
  readonly bill?: string;
  readonly result: string;
  /** The official page for the entire tally, not just this member. */
  readonly url: string;
  /**
   * A final decision on a measure or nomination, by the chamber's own question
   * wording (scripts/build-record.py, HOUSE_DECISION / SENATE_DECISION). Never
   * set by hand. Absent on records built before On the Record.
   */
  readonly decision?: boolean;
  /** Among the chamber's latest recorded votes of any kind (the 1.0 list). */
  readonly recent?: boolean;
  /** The time the chamber recorded the vote, House only, as "6:58 PM ET". */
  readonly time?: string;
  /** The bill or nomination on congress.gov: text, actions, CRS summary. */
  readonly billUrl?: string;
  /**
   * The measure as congress.gov shows it at build time, verbatim: its display
   * title (a bill) or description (a nomination). May differ from `desc`,
   * which is the chamber's wording at the vote; both are shown, labelled.
   */
  readonly title?: string;
  /** Congress.gov's latest action on the measure, verbatim, with its date. */
  readonly latestAction?: { readonly date: string; readonly text: string };
  /** Bills only: whether the Congressional Research Service has summarised it. */
  readonly crsSummary?: boolean;
  /** Bills only: the sponsor's bioguide id, as Congress.gov lists it. */
  readonly sponsor?: string;
  /** Official recordings, LINKED and never re-hosted. Empty when none is listed. */
  readonly media?: readonly Recording[];
}

export interface Recording {
  readonly kind: "floor" | "committee";
  readonly label: string;
  readonly url: string;
  /** Who published it, shown beside the link. */
  readonly by: string;
}

export interface Filing {
  readonly year: string;
  readonly type: string;
  readonly date: string;
  readonly url: string;
}

export interface MemberRecord {
  /** Committees and subcommittees, with any leadership role as the Clerk states it. */
  readonly committees?: readonly string[];
  /** [roll call id, position as cast]. */
  readonly votes?: ReadonlyArray<readonly [string, string]>;
  readonly filings?: readonly Filing[];
}

/** The date these records were read from the sources above. */
export const RECORD_RETRIEVED_AT = "__DATE__";

export const ROLL_CALLS: Readonly<Record<string, RollCall>> = {
'''

main()
