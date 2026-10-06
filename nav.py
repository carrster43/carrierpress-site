#!/usr/bin/env python3
"""
The product sections in the site nav, in ONE place.

    python3 nav.py            # re-sync the nav into every page on disk

WHY THIS EXISTS. The nav has been edited three times in two days and each time
it lived in more files than the last: build.py regenerates the homepage,
labs/index.html is hand written and never regenerated, and make_apps.py and
make_audio.py each carry their own <head> template. Adding "Apps" meant three
edits, "Audio" meant four, and the site memory already records the count being
wrong once. A list of four links does not deserve four copies.

HOW. Each generator writes its file as before, then calls patch() on it. patch()
finds the contiguous run of product-section links inside <nav class="nav"> and
replaces it. It never touches the links either side, which genuinely differ:
the homepage nav uses same-page anchors (#fiction) and carries Young Readers and
About, while the subpages use /#fiction and carry Journal instead.

It asserts it found exactly one run. A nav it cannot recognise is a nav that has
been restructured, and silently leaving it alone is how this drifted in the
first place.

>>> THE PLAY LINK IS CONDITIONAL, AND THAT IS THE POINT. <<<

/play/ is the game, which is sold on itch.io, and the itch project does not
exist yet. While play_data.ITCH_URL is None there is no Play link anywhere and
make_play.py refuses to emit the page at all, so the site cannot ship a nav item
pointing at a page advertising a game nobody can reach. Set that one constant
and everything turns on together.
"""
import pathlib, re, sys

import play_data

# The product sections, in nav order. Books live at the front of the nav and are
# owned by each page's own template; these are the things that are not books.
SECTIONS = [
    ("/labs/", "Labs"),
    ("/apps/", "Apps"),
    ("/audio/", "Audio"),
    ("/progress/", "Progress"),
    ("/reviews/", "Reviews"),
    ("/support/", "Support"),
]
if play_data.ITCH_URL:
    SECTIONS.append(("/play/", "Play"))

# Every page whose nav this module owns. A generated page is patched by its own
# generator as well; listing it here is what makes `python3 nav.py` a complete
# re-sync rather than a partial one.
PAGES = ["index.html", "labs/index.html", "apps/index.html",
         "audio/index.html", "play/index.html",
         "progress/index.html", "support/index.html",
         "reviews/index.html"]

# One or more consecutive product-section links, each on its own line. The
# alternation is closed on purpose: a run is only a run if every link in it is a
# section this module owns.
RUN = re.compile(
    r'(?:\n[ \t]*<a href="/(?:labs|apps|audio|play|progress|reviews|support)/">[^<]*</a>)+'
)


def block(indent="      "):
    return "".join('\n%s<a href="%s">%s</a>' % (indent, h, t) for h, t in SECTIONS)


# THE PHONE MENU. Every page this module owns carries the long nav, eight or
# nine links, and on a phone that was a sideways strip the links slid under the
# pinned Free Sample and got cut mid-word. Below 760px these pages now show the
# brand, Free Sample, and a Menu button that drops the full list down.
#
# The script is inline and self-contained so there is no shared JS file to go
# missing, and it adds `navjs` to <html> before anything is hidden: with
# scripting off, styles.css never collapses the nav and the old strip remains.
# Support, privacy and journal pages carry two to four links, fit a phone as
# they are, and never come through here.
TOGGLE = (
    '\n%s<button class="nav-toggle" type="button" aria-expanded="false" '
    'aria-controls="site-nav">Menu</button>'
    '\n%s<script>(function(){var d=document.documentElement,'
    'h=document.currentScript.closest(".site-head"),b=h.querySelector(".nav-toggle"),'
    'n=h.querySelector(".nav");d.classList.add("navjs");'
    'function set(o){h.classList.toggle("nav-open",o);b.setAttribute("aria-expanded",o)}'
    'b.addEventListener("click",function(){set(!h.classList.contains("nav-open"))});'
    'n.addEventListener("click",function(e){if(e.target.closest("a"))set(false)});'
    'd.addEventListener("keydown",function(e){if(e.key==="Escape")set(false)})})();</script>'
)
NAV_OPEN = '<nav class="nav" aria-label="Main">'


def add_toggle(s):
    """Insert the Menu button after the main nav, once. Idempotent."""
    if "nav-toggle" in s:
        return s
    if s.count(NAV_OPEN) != 1:
        raise SystemExit("nav.py: expected exactly one main nav, found %d" % s.count(NAV_OPEN))
    s = s.replace(NAV_OPEN, '<nav class="nav" id="site-nav" aria-label="Main">')
    start = s.index('<nav class="nav" id="site-nav"')
    close = s.index("</nav>", start) + len("</nav>")
    indent = re.search(r"\n([ \t]*)<nav class=\"nav\" id", s).group(1)
    return s[:close] + TOGGLE % (indent, indent) + s[close:]


def patch(path):
    """Rewrite the section links in one rendered page. Returns True if changed."""
    p = pathlib.Path(path)
    if not p.exists():
        return False
    s = p.read_text(encoding="utf-8")
    hits = RUN.findall(s)
    if len(hits) != 1:
        raise SystemExit(
            "nav.py: expected exactly one run of section links in %s, found %d. "
            "The nav has been restructured; fix RUN rather than letting this "
            "page drift." % (path, len(hits)))
    indent = re.search(r'\n([ \t]*)<a href="/(?:labs|apps|audio|play|progress|reviews|support)/">', s).group(1)
    out = RUN.sub(lambda m: block(indent), s, count=1)
    out = add_toggle(out)
    if out != s:
        p.write_text(out, encoding="utf-8")
        return True
    return False


if __name__ == "__main__":
    names = [t for _, t in SECTIONS]
    changed = [p for p in PAGES if patch(p)]
    print("nav: %s" % " | ".join(names))
    print("changed: %s" % (", ".join(changed) if changed else "nothing, already in sync"))
    if not play_data.ITCH_URL:
        print("play: OFF (play_data.ITCH_URL is None)")
