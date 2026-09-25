#!/usr/bin/env python3
"""
Every site-relative link on every page must resolve to a file on disk.

    python3 check_links.py

WHY THIS EXISTS. This is a static site with no server and no router, so a wrong
path is not a redirect or a helpful error, it is a 404 for a reader and for a
crawler. The pages most exposed to it are the ones nobody browses: thirty-eight
app support pages and thirty-eight privacy pages, reached from App Store records
rather than from the site, and opened by App Review.

▶ IT WALKS EVERY .html FILE, INCLUDING support_bodies/. Those are fragments
rather than pages, so the file count is larger than the page count, and that is
deliberate: make_support.py checks a body's links when it assembles a page, and
this checks them again where they sit. A body is the one place a link can rot
without any page having been edited.

make_support.py already refuses to build a body whose links do not resolve, and
that guard exists because the narrower version of it shipped a 404: it asked only
whether THIS app's privacy page existed, and Sole Ledger's body pointed at
/ledgerforone/ after the rename deleted that directory. This file is the same
question asked of the whole site rather than one body at a time.

WHAT IT DOES NOT CHECK. External links, because a build should not depend on the
network or fail because somebody else's site is down. Fragments (#anchors), which
would need the target parsed rather than located. Both are deliberate: a check
that is flaky gets ignored, and a check that gets ignored is worse than none.
"""
import os, re, sys, glob
from collections import Counter

REF = re.compile(r'(?:href|src)="([^"]+)"')


def check(root="."):
    broken, checked = Counter(), 0
    for page in sorted(glob.glob(os.path.join(root, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(page, root)
        for raw in REF.findall(open(page, encoding="utf-8").read()):
            if raw.startswith(("http://", "https://", "mailto:", "data:", "#", "//")):
                continue
            target = raw.split("#")[0].split("?")[0]
            if not target:
                continue
            base = root if target.startswith("/") else os.path.dirname(page)
            path = os.path.normpath(os.path.join(base, target.lstrip("/")))
            checked += 1
            # A directory link is served by its index.html, which is the form
            # every internal link on this site actually takes.
            if os.path.isdir(path):
                path = os.path.join(path, "index.html")
            # GitHub Pages serves /x from x.html. The exported web apps
            # (/boatready/app/) route that way: /boatready/app/saved is saved.html.
            if not os.path.exists(path) and os.path.exists(path + ".html"):
                path += ".html"
            if not os.path.exists(path):
                broken[(rel, raw)] += 1
    return checked, broken


if __name__ == "__main__":
    checked, broken = check()
    for (page, ref), n in sorted(broken.items()):
        print(f"BROKEN  {page}  ->  {ref}" + (f"  (x{n})" if n > 1 else ""))
    print(f"{checked} internal reference(s) checked, {len(broken)} broken")
    sys.exit(1 if broken else 0)
