#!/usr/bin/env python3
"""
Search metadata for the app support (/<slug>/) and privacy (/<slug>/privacy/)
pages, in the <head> ONLY (author: "fix the support and privacy pages metadata
too", 2026-11-20).

    python3 page_ld.py           # patch every support and privacy page on disk

WHY A POST-PROCESSOR, LIKE nav.py. The support pages are rewritten by
make_support.py, but the privacy pages are written once and a bare
`make_privacy.py --force` is NOT safe (seven live pages are newer than their
source). So this patches the pages already on disk, and make_support.py and
make_privacy.py call patch() on each page they write, so a regenerated page
comes out the same.

WHAT IT CHANGES, AND NOTHING ELSE:
  1. One WebPage JSON-LD block, marked data-gen="page_ld", replaced on every run.
     `about` names the app and points at its /apps/<slug>/ landing page when that
     page is public. No Offer, no rating, nothing the page does not already say.
  2. og:image: the app's own first screenshot instead of the site-wide card,
     when one exists (the landing pages already use the same file).
  3. A meta/og description over 160 characters is cut at its last list comma
     before 157 and closed with a full stop. These descriptions are lists
     ("Help for X: a, b, c, and d"), so the cut drops trailing items and never
     rewords one.

The support URL is the one App Review opens: the visible page never changes.
noindex pages (folded-app stubs) are skipped.
"""
import html, json, pathlib, re, sys

import apps_data

DOMAIN = "carrierpress.com"
ROOT = pathlib.Path(__file__).resolve().parent
LD_RE = re.compile(r'\n?<script type="application/ld\+json" data-gen="page_ld">.*?</script>', re.S)
NAMES = {a["slug"]: a["name"] for a in apps_data.APPS if a.get("slug")}


def trim(desc, limit=160, cut=157):
    """Shorten a list-shaped description at its last comma. Returns it as is
    when it already fits or has no comma to cut at."""
    if len(desc) <= limit:
        return desc
    head = desc[:cut]
    i = head.rfind(", ")
    if i < 70:
        return desc
    out = re.sub(r"\s+and$", "", head[:i].rstrip())
    return out + "."


def _public_landing(slug):
    p = ROOT / "apps" / slug / "index.html"
    return p.exists() and "noindex" not in p.read_text(encoding="utf-8")


def _shot(slug):
    d = ROOT / "apps" / "shots" / slug
    for n in ("store-1.webp",):
        if (d / n).exists():
            return "https://%s/apps/shots/%s/%s" % (DOMAIN, slug, n)
    return None


def patch(path):
    """Patch one support or privacy page. Returns True if the file changed."""
    p = pathlib.Path(path)
    if not p.exists():
        return False
    rel = p.resolve().relative_to(ROOT).parts
    if rel[-1] != "index.html" or len(rel) not in (2, 3) or (len(rel) == 3 and rel[1] != "privacy"):
        return False
    slug = rel[0]
    if slug not in NAMES:
        return False
    s = p.read_text(encoding="utf-8")
    head_end = s.find("</head>")
    if head_end < 0 or "noindex" in s[:head_end]:
        return False
    head, rest = s[:head_end], s[head_end:]

    # 3. descriptions
    def _d(m):
        return m.group(1) + html.escape(trim(html.unescape(m.group(2))), quote=True) + '"'
    head = re.sub(r'(<meta name="description" content=")([^"]*)"', _d, head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")([^"]*)"', _d, head, count=1)

    # 2. og:image
    shot = _shot(slug)
    if shot:
        head = re.sub(r'(<meta property="og:image" content=")[^"]*"', lambda m: m.group(1) + shot + '"', head, count=1)

    # 1. JSON-LD
    title = html.unescape(re.search(r"<title>(.*?)</title>", head, re.S).group(1).strip())
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', head)
    privacy = len(rel) == 3
    url = "https://%s/%s/%s" % (DOMAIN, slug, "privacy/" if privacy else "")
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url,
          "inLanguage": "en",
          "isPartOf": {"@type": "WebSite", "name": "Carrier Press", "url": "https://%s/" % DOMAIN},
          "publisher": {"@type": "Organization", "name": "Carrier Press", "url": "https://%s/" % DOMAIN}}
    if desc_m:
        ld["description"] = html.unescape(desc_m.group(1))
    if _public_landing(slug):
        ld["about"] = {"@type": "SoftwareApplication", "name": NAMES[slug],
                       "url": "https://%s/apps/%s/" % (DOMAIN, slug)}
    head = LD_RE.sub("", head).rstrip("\n")
    head += '\n<script type="application/ld+json" data-gen="page_ld">%s</script>\n' % json.dumps(ld, ensure_ascii=False)

    out = head + rest
    if out != s:
        p.write_text(out, encoding="utf-8")
        return True
    return False


if __name__ == "__main__":
    changed = 0
    for slug in sorted(NAMES):
        for f in (ROOT / slug / "index.html", ROOT / slug / "privacy" / "index.html"):
            if patch(f):
                changed += 1
                print("  patched", f.relative_to(ROOT))
    print("%d page(s) changed" % changed)
    sys.exit(0)
