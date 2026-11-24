#!/usr/bin/env python3
"""
Re-check every statewide officeholder against the page the data already cites.

    python3 check_statewide.py              # report only, changes nothing
    python3 check_statewide.py --write      # also bump verifiedAt on confirmed rows
    python3 check_statewide.py --limit 10   # a sample, for trying it out

WHY THIS AND NOT A SCRAPER. officeholders.json refreshes itself every Monday
from three national sources (.github/workflows/whoserves-officeholders.yml).
statewide.json has no builder and no workflow: its 295 offices across 56 states
are kept by hand, and on 2026-11-23 every row in it still read verifiedAt
2026-09-25. Pages whose whole value is being current cannot sit on data nobody
checks.

There is no national feed for state executives. The alternatives are scraping 56
bespoke .gov sites for names, or asking Ballotpedia, whose data is not ours to
take. Both put a wrong name on a civic page, which is the one failure this app
cannot absorb. So this does neither.

WHAT IT ACTUALLY DOES. Every row already carries the URL it was verified
against. This fetches that page and asks one question: is the name we published
still on it? That is the same question a person would ask, against the same
source they would open, and it is cheap enough to ask weekly.

  confirmed   the holder's name is still on the cited page. --write moves
              verifiedAt to today. Nothing else is touched, ever.
  changed     the page loaded and the name is NOT on it. Reported, never acted
              on: a name that vanished may be an election, a resignation, a
              redesign or a renamed heading, and only a person can tell which.
  unreachable the fetch failed after retries. Reported, never acted on.

IT NEVER WRITES A NAME. Not a new holder, not a corrected spelling, not a
vacancy. The only field it can change is verifiedAt, and only upward, and only
on a row whose name it has just seen with its own eyes. That is the whole safety
story: the worst bug here can make the data look staler than it is, which is the
harmless direction. crosscheck-congress.py takes the same position on Congress.

EXIT CODE. Non-zero when any row is `changed`, so a scheduled run's failure
email is the alert, exactly as the officeholders workflow treats a refusal.
`unreachable` alone does not fail the run: a state website being down on a
Monday is not news about who holds the office.
"""
import argparse
import datetime as dt
import html
import json
import pathlib
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request

DATA = pathlib.Path("whoserves") / "data" / "statewide.json"
# Generic, as the vendored builders are: it names the software, not a person.
AGENT = {"User-Agent": "CarrierPress-WhoServes/0.1 (civic reference; contact via repository)"}
PAUSE = 1.5          # between requests, so 56 state sites are not hammered
TIMEOUT = 45


def fetch(url, tries=3):
    """GET with a short backoff. Returns (body, None) or (None, why).

    `why` distinguishes the refusals, because they are different facts about
    the world and the report is read by a person deciding where to spend an
    afternoon. A 403 is not a flaky network: on 2026-11-24, 34 rows came back
    "fetch failed", and curl got 403 from the same hosts with the same agent,
    so those state sites refuse every non-browser client and no retry will ever
    help. A name resolution failure means the cited host has gone, which is a
    fact about the DATA rather than the fetch -- ohioauditor.gov did not
    resolve at all, and a sourceUrl that no longer exists wants replacing.
    """
    last = "fetch failed after retries"
    for attempt in range(tries):
        try:
            request = urllib.request.Request(url, headers=AGENT)
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                raw = response.read()
            break
        except urllib.error.HTTPError as ex:
            if ex.code in (401, 403, 429):
                return None, "blocked by the site (HTTP %d); no retry will help" % ex.code
            last = "HTTP %d" % ex.code
        except urllib.error.URLError as ex:
            reason = str(getattr(ex, "reason", ex))
            if "getaddrinfo" in reason or "Name or service not known" in reason:
                return None, "host does not resolve; the cited URL may be dead"
            last = "network: %s" % reason[:50]
        except OSError as ex:
            last = "network: %s" % str(ex)[:50]
        if attempt == tries - 1:
            return None, last
        time.sleep(4 * (attempt + 1))
    else:
        return None, last
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding), None
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace"), None


def page_text(body):
    """Visible-ish text: script and style gone, tags gone, entities decoded."""
    body = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    return normalise(html.unescape(body))


def normalise(s):
    """Fold case, accents and punctuation so Peña matches Pena and O'Malley
    matches OMalley. Hyphens become spaces, so Hyde-Smith matches Hyde Smith."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("-", " ").replace("’", "'")
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# Suffixes and courtesy titles that a page may carry and the data may not, or
# the other way round. They are never the evidence that a person is still there.
NOISE = {"jr", "sr", "ii", "iii", "iv", "dr", "mr", "mrs", "ms", "the", "honorable", "hon"}


def name_parts(name):
    """The parts of a name worth matching on: first and last, noise dropped."""
    parts = [p for p in normalise(name).split() if p not in NOISE and len(p) > 1]
    if len(parts) < 2:
        return parts
    return [parts[0], parts[-1]]


# Given names whose short form is not a prefix of the long one, so no amount of
# stem matching will join them. Listed rather than guessed, because the rule
# this replaces would have to be loose enough to also join Mike to Miriam.
# One line per pair, both directions built below.
_NICKNAMES = """
mike michael | bill william | bob robert | dick richard | jim james | joe joseph
tom thomas | dave david | steve stephen | steve steven | chris christopher
dan daniel | ed edward | jack john | ken kenneth | larry lawrence | rick richard
ron ronald | sam samuel | tony anthony | pat patrick | pat patricia | beth elizabeth
liz elizabeth | betty elizabeth | peggy margaret | meg margaret | sue susan
kate katherine | kathy katherine | cathy catherine | nancy ann | ted edward
ted theodore | tim timothy | greg gregory | jeff jeffrey | andy andrew
matt matthew | nick nicholas | phil philip | phil phillip | ray raymond
rob robert | gene eugene | hank henry | hal harold | art arthur | fred frederick
"""
NICK = {}
for _pair in _NICKNAMES.replace("\n", " | ").split("|"):
    _bits = _pair.split()
    if len(_bits) == 2:
        NICK.setdefault(_bits[0], set()).add(_bits[1])
        NICK.setdefault(_bits[1], set()).add(_bits[0])


def _first_name_ok(first, text):
    """A given name, allowing the short form the office's own site tends to use.

    The data carries the name on the certificate and the page carries the name
    on the door: North Carolina records Bradford B. Briner and the Treasurer's
    own site says Brad Briner; Pennsylvania records Dave W. Sunday and the page
    says David Sunday. Both were reported as changed on 2026-11-24, and both
    were the same man. A shared prefix of three or more letters, in either
    direction, is the shape every one of those pairs takes."""
    if re.search(r"\b%s\b" % re.escape(first), text):
        return True
    for alt in NICK.get(first, ()):
        if re.search(r"\b%s\b" % re.escape(alt), text):
            return True
    if len(first) < 3:
        return False
    # A shared three-letter stem, not a shared prefix: Brad/Bradford and
    # Zach/Zachary are prefixes, but Dave/David diverge at the fourth letter
    # and are still the same man. Three letters is enough because the surname
    # has already matched exactly -- it is the surname that identifies, and
    # this only has to corroborate. Peggy and Peter part at the third letter,
    # which is the case that has to keep failing.
    return bool(re.search(r"\b%s[a-z]*\b" % re.escape(first[:3]), text))


def present(name, text):
    """How well is this person still named on the page: "both", "surname", "no".

    The three answers are different claims and must not be collapsed into two.

      both      first and last found. Evidence the row is still right.
      surname   the surname is there and the given name is not, anywhere, in
                any form. On 2026-11-24 that was Wisconsin's page headed "Meet
                Sarah", North Carolina's naming only "Briner", and
                Pennsylvania's naming only "Sunday" -- three pages that render
                the bio client-side and leave one name in the shell. Somebody
                of that surname still holds the office, so reporting this as
                "the name is gone" was simply false. It is not proof either:
                a successor can share a surname. Reported, never written.
      no        neither name is on the page. The only shape a real change takes
                -- and also the shape of a shell that names nobody at all.
    """
    parts = name_parts(name)
    if not parts:
        return "no"
    if len(parts) == 1:
        return "both" if re.search(r"\b%s\b" % re.escape(parts[0]), text) else "no"
    first, last = parts
    if not re.search(r"\b%s\b" % re.escape(last), text):
        return "no"
    return "both" if _first_name_ok(first, text) else "surname"


# A page can load and still carry no evidence either way. Calling that "the
# name is gone" is the one thing this script must not do: on 2026-11-24 it did,
# nine times, and every one was a wall or a file type rather than a new
# officeholder. These are the shapes that came back.
WALL = re.compile(
    r"(?i)\b(captcha|incapsula|request unsuccessful|access denied|bot manager|"
    r"are you a human|enable javascript|checking your browser|cf-browser-verification|"
    r"ddos protection|unusual traffic|403 forbidden)\b")


def unreadable(body, url, text):
    """Why this page proves nothing, or None if it is readable evidence."""
    if url.lower().split("?")[0].endswith(".pdf") or body.lstrip()[:5].startswith("%PDF"):
        return "PDF, which this script cannot read"
    hit = WALL.search(text[:4000])
    if hit:
        return "blocked: %s" % hit.group(1).lower()
    if len(text) < 200:
        return "almost no text (%d chars); rendered by script, or a shell" % len(text)
    return None


def rows(data):
    """Every checkable row, as (state, office key, holder name, url, row)."""
    for code, offices in sorted(data["states"].items()):
        for row in offices:
            holder = row.get("holder") or {}
            name, url = holder.get("name"), row.get("sourceUrl")
            if name and url:
                yield code, row.get("key", ""), name, url, row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true",
                    help="bump verifiedAt on confirmed rows; names are never written")
    ap.add_argument("--limit", type=int, default=0, help="check only the first N rows")
    ap.add_argument("--stale", action="store_true",
                    help="only rows not already verified today, to re-check what a "
                         "previous run could not confirm without re-reading all 295")
    args = ap.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    todo = list(rows(data))
    if args.stale:
        todo = [t for t in todo if (t[4].get("verifiedAt") or "") != dt.date.today().isoformat()]
    if args.limit:
        todo = todo[:args.limit]
    today = dt.date.today().isoformat()

    confirmed, surname_only, changed, unreachable = [], [], [], []
    seen_host = {}
    for i, (code, key, name, url, row) in enumerate(todo, 1):
        body, why_fetch = fetch(url)
        label = "%s %s" % (code.upper(), key)
        if body is None:
            unreachable.append((label, name, url, why_fetch))
        else:
            text = page_text(body)
            why = unreadable(body, url, text)
            if why:
                unreachable.append((label, name, url, why))
            else:
                verdict = present(name, text)
                if verdict == "both":
                    confirmed.append((label, name, row))
                elif verdict == "surname":
                    surname_only.append((label, name, url))
                else:
                    changed.append((label, name, url))
        if i < len(todo):
            time.sleep(PAUSE)
        if i % 25 == 0:
            print("  ... %d/%d" % (i, len(todo)), flush=True)

    print()
    print("statewide rows checked: %d" % len(todo))
    print("  confirmed    %3d" % len(confirmed))
    print("  surname only %3d" % len(surname_only))
    print("  changed      %3d" % len(changed))
    print("  unreachable  %3d" % len(unreachable))

    if changed:
        print("\nNAME NO LONGER ON THE CITED PAGE -- check each by hand:")
        for label, name, url in changed:
            print("  %-28s %-28s %s" % (label, name, url))
    if unreachable:
        print("\nCOULD NOT BE READ (nothing concluded):")
        for label, name, url, why in unreachable:
            print("  %-28s %-24s %-46s %s" % (label, name, why, url))

    if args.write and confirmed:
        for _, _, row in confirmed:
            row["verifiedAt"] = today
        data["updatedAt"] = today
        DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("\nverifiedAt moved to %s on %d confirmed row(s). No name was written."
              % (today, len(confirmed)))
    elif args.write:
        print("\nnothing confirmed; file untouched.")

    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
