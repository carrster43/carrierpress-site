#!/usr/bin/env python3
"""
Checks every support body before it is allowed near the live site.

These bodies are written per app from that app's own repo, which is the only way
a support page is worth having, but it also means nobody has read all of them.
This enforces the rules that are checkable, so review time goes on the claims
that are not.

    python3 check_support.py
"""
import pathlib, re, sys, html.parser

ALLOWED = {"p", "h2", "h3", "ul", "li", "strong", "a", "em"}
HEADER = re.compile(r"^<!--\s*name:\s*(.+?)\s*\|\s*blurb:\s*(.+?)\s*-->\s*", re.S)

# A price on a web page is wrong in every storefront that prices differently and
# wrong everywhere the day it changes. The app reads its price from the store.
# A trial LENGTH is the part that changes silently, so it is banned the same way
# a price is. An unquantified "opens on a free trial" is allowed, because several
# apps implement a real time-based trial in lib/access.ts and saying so is true.
PRICE = re.compile(r"\$\s?\d|\bUSD\b|\d+\s?(?:dollars|cents)\b"
                   r"|\bper (?:month|year)\b|\b/\s?(?:mo|yr)\b"
                   r"|\b(?:\d+|one|two|three|seven|ten|fourteen|thirty)[- ](?:day|week|month)"
                   r"\s+(?:free\s+)?trial\b"
                   r"|\btrial (?:lasts|runs|is)\s+(?:\d+|one|two|three|seven|ten|fourteen|thirty)\b",
                   re.I)

# House rule: no em dashes, no en dashes, and no "--" standing in for one.
DASH = re.compile(r"[—–]|(?<!\w)--(?!\w)")

BANNED_SECTIONS = re.compile(r"<h[123][^>]*>\s*(contact|last updated)", re.I)


class Tags(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.seen, self.stack, self.unbalanced = set(), [], []

    def handle_starttag(self, tag, attrs):
        self.seen.add(tag)
        if tag != "br":
            self.stack.append(tag)
        for k, v in attrs:
            if k == "class" and v != "lede":
                self.unbalanced.append(f'class="{v}" is not allowed')
            if k not in ("class", "href"):
                self.unbalanced.append(f"attribute {k} is not allowed")

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.unbalanced.append(f"</{tag}> does not close the open tag")


def check(path):
    raw = path.read_text(encoding="utf-8")
    slug, problems, warnings = path.stem, [], []

    m = HEADER.match(raw)
    if not m:
        return slug, ["missing the <!-- name: X | blurb: Y --> header line"], [], 0
    name, blurb = m.group(1), m.group(2)
    body = raw[m.end():].strip()

    if len(blurb) > 200:
        problems.append(f"blurb is {len(blurb)} chars (max 200)")
    if not body.startswith('<p class="lede">'):
        problems.append('body must open with <p class="lede">')

    for label, rx, why in (("price", PRICE, "prices belong to the store, not a web page"),
                           ("dash", DASH, "house rule: no em or en dashes")):
        for hit in rx.finditer(body):
            ctx = body[max(0, hit.start() - 45):hit.end() + 45].replace("\n", " ")
            problems.append(f"{label}: ...{ctx}...")

    if BANNED_SECTIONS.search(body):
        problems.append("body contains a Contact or Last updated heading; the generator adds those")
    if re.search(r"<h1", body, re.I):
        problems.append("body contains an <h1>; the generator adds the title")

    t = Tags()
    t.feed(body)
    for tag in sorted(t.seen - ALLOWED):
        problems.append(f"<{tag}> is not in the allowed set")
    problems += t.unbalanced
    if t.stack:
        problems.append(f"unclosed tags: {', '.join(t.stack)}")

    words = len(re.sub(r"<[^>]+>", " ", body).split())
    if words < 250:
        warnings.append(f"{words} words, thin")
    elif words > 900:
        warnings.append(f"{words} words, long")
    if body.count("<h2") < 2:
        warnings.append("fewer than two sections")

    return slug, problems, warnings, words


if __name__ == "__main__":
    files = sorted(pathlib.Path("support_bodies").glob("*.html"))
    if not files:
        sys.exit("no bodies found")
    bad = 0
    for f in files:
        slug, problems, warnings, words = check(f)
        if problems:
            bad += 1
            print(f"FAIL  {slug}  ({words}w)")
            for p in problems:
                print(f"        {p}")
        elif warnings:
            print(f"warn  {slug}  ({words}w)  " + "; ".join(warnings))
        else:
            print(f"ok    {slug}  ({words}w)")
    print(f"\n{len(files)} bodies, {bad} failing")
    sys.exit(1 if bad else 0)
