#!/usr/bin/env python3
"""
Build /immersive/, the Carrier Press reading room in 3D, VR and hologram.

    python3 make_immersive.py

WHAT IT IS. One room, generated from the same two files every other page reads:
catalog.json for the books and apps_data.py for the apps. Nine bays of covers and
three bays of apps stand in a ring around the visitor, with the press mark turning
on a light column in the middle.

THREE WAYS IN, ONE SCENE (immersive/room.js):

    browser   drag to look around, tap a cover to open its page
    VR        "Enter VR" on a headset browser (Quest, Vision Pro, PC VR):
              WebXR immersive-vr, controllers or hands point and select
    hologram  "Place as hologram" where the browser offers immersive-ar
              (Quest 3 passthrough, Android Chrome): the same room shrunk to a
              table-top model floating in the real room

The buttons appear only where the browser says the session is supported, so
nobody is shown a door that does not open.

NO THIRD-PARTY REQUEST. three.js is vendored at /vendor/three/ (MIT, r180) and
loads only on this page, only after the page itself has rendered. Covers are the
site's own /assets/covers/ files.

A PLAIN LIST IS ALWAYS THERE. Under the canvas the page carries every bay as
ordinary links, so a reader with no WebGL, a screen reader or a slow phone gets
the same content and loses only the room.

Like make_apps.py, this writes its page and nothing else, and the test workflow
regenerates it and requires the committed copy to match.
"""
import datetime, html, json, pathlib

import apps_data
import books as _books

OUT = pathlib.Path("immersive")
D = json.load(open("catalog.json"))
BOOK_URL = _books.url_for(D)

# Short status words for an app card in the room. The long group headings on
# /apps/ do not fit on a card the size of a paperback.
STATUS = {
    "live": "On the App Store",
    "browser": "Open now in a browser",
    "soon": "Coming soon",
    "build": "Coming soon",
    "design": "In design",
}


def e(x):
    return html.escape(str(x), quote=True)


def bays():
    """The nine book bays, in catalogue order, with every cover that exists."""
    out = []
    for s in D["sections"]:
        items = []
        for b in s.get("books", []):
            asin = b["a"]
            cover = pathlib.Path("assets/covers/%s.jpg" % asin)
            if not cover.exists():
                continue
            items.append({
                "t": _books.display_title(b, s),
                "img": "/" + cover.as_posix(),
                "url": BOOK_URL[asin],
            })
        if items:
            out.append({"name": s["name"], "shelf": s.get("shelf", ""), "items": items})
    return out


def apps():
    """Every app with a page of its own, as a card: name, one line, status."""
    out = []
    for a in apps_data.APPS:
        slug = a.get("slug")
        page = pathlib.Path("apps", slug or "", "index.html")
        url = "/apps/%s/" % slug if slug and page.exists() else "/apps/"
        out.append({
            "t": a["name"],
            "line": a.get("headline", ""),
            "status": STATUS.get(a.get("status"), ""),
            "url": url,
        })
    return out


def plain_list(book_bays, app_rows):
    """The same room as links, for anyone the canvas does not reach."""
    parts = []
    for bay in book_bays:
        links = "".join('<li><a href="%s">%s</a></li>' % (e(i["url"]), e(i["t"])) for i in bay["items"])
        parts.append('<section><h3>%s</h3><ul>%s</ul></section>' % (e(bay["name"]), links))
    links = "".join('<li><a href="%s">%s</a></li>' % (e(a["url"]), e(a["t"])) for a in app_rows)
    parts.append('<section><h3>Apps</h3><ul>%s</ul></section>' % links)
    return "\n".join(parts)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Reading Room in 3D | Carrier Press</title>
<meta name="description" content="Every Carrier Press book and app in one room. Look around in a browser, step inside on a VR headset, or place it on a table as a hologram.">
<link rel="canonical" href="https://carrierpress.com/immersive/">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
<style>
.ir-stage{{position:relative;height:min(78vh,760px);min-height:420px;background:#07080f;overflow:hidden}}
.ir-stage canvas{{display:block;width:100%;height:100%;touch-action:none;cursor:grab}}
.ir-stage canvas:active{{cursor:grabbing}}
.ir-bar{{
  position:absolute;left:16px;right:16px;bottom:16px;display:flex;flex-wrap:wrap;gap:10px;
  align-items:center;justify-content:space-between;pointer-events:none;
}}
.ir-bar > *{{pointer-events:auto}}
.ir-hint{{color:#c9c4b5;font:14px/1.4 var(--sans);text-shadow:0 1px 2px #000;margin:0}}
.ir-doors{{display:flex;gap:10px;flex-wrap:wrap}}
.ir-door{{
  font:600 15px/1 var(--sans);padding:12px 18px;border-radius:999px;border:1px solid #e8c84a;
  background:rgba(7,8,15,.72);color:#f2d76b;cursor:pointer;backdrop-filter:blur(6px);
}}
.ir-door:hover,.ir-door:focus-visible{{background:#e8c84a;color:#07080f}}
.ir-door[hidden]{{display:none}}
.ir-pick{{
  position:absolute;top:16px;left:16px;max-width:min(360px,calc(100% - 32px));
  background:rgba(7,8,15,.86);border:1px solid #2b2e42;border-radius:10px;padding:14px 16px;
  color:#ece8dd;font:15px/1.45 var(--sans);backdrop-filter:blur(6px);
}}
.ir-pick[hidden]{{display:none}}
.ir-pick strong{{display:block;font:400 1.15rem/1.25 var(--serif);margin-bottom:4px}}
.ir-pick span{{display:block;color:#b9b4a6;font-size:.92rem}}
.ir-pick a{{display:inline-block;margin-top:10px;color:#f2d76b;font-weight:600}}
.ir-fallback{{position:absolute;inset:0;display:grid;place-items:center;color:#c9c4b5;padding:24px;text-align:center}}
.ir-intro{{max-width:70ch}}
.ir-list{{display:grid;gap:8px 32px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));margin-top:20px}}
.ir-list h3{{font:400 1.05rem/1.3 var(--serif);margin:18px 0 6px}}
.ir-list ul{{margin:0;padding-left:18px;font-size:.95rem;line-height:1.6}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="/">
      <img class="mark-dark" src="/assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="/assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>Carrier Press</span>
    </a>
    <nav class="nav" aria-label="Main">
      <a href="/#fiction">Fiction</a>
      <a href="/#classics">Classics</a>
      <a href="/apps/">Apps</a>
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
  </div>
</header>
<main id="main">
<div class="ir-stage" id="stage">
  <div class="ir-fallback" id="ir-fallback"><p>The room needs WebGL, which this browser does not offer. Every book and app is listed below.</p></div>
  <div class="ir-pick" id="ir-pick" hidden aria-live="polite"></div>
  <div class="ir-bar">
    <p class="ir-hint" id="ir-hint">Loading the room&hellip;</p>
    <div class="ir-doors">
      <button class="ir-door" id="enter-vr" type="button" hidden>Enter VR</button>
      <button class="ir-door" id="enter-ar" type="button" hidden>Place as hologram</button>
    </div>
  </div>
</div>
<div class="wrap" style="padding:40px 0 64px">
  <h1 style="font:400 2rem/1.2 var(--serif);margin:0 0 12px">The Reading Room</h1>
  <p class="ir-intro">{n_books} books and {n_apps} apps, standing in one ring. In a browser, drag to look around and tap anything to open it. On a VR headset, Enter VR puts you in the middle of the room. Where a headset or phone can mix the room with the one you are in, Place as hologram sets it on the table in front of you.</p>
  <p class="ir-intro" style="color:var(--muted);font-size:.95rem">Nothing here leaves this site: the 3D engine and every cover are served from carrierpress.com, and nothing loads until you open this page.</p>
  <div class="ir-list">
{plain}
  </div>
</div>
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; {year} Jeffrey L. Carrier. All rights reserved.</span>
      <span><a href="/">Carrier Press</a> is an imprint of Jeffrey L. Carrier.</span>
    </div>
  </div>
</footer>
<script type="application/json" id="room-data">{data}</script>
<script type="module" src="/immersive/room.js"></script>
</body>
</html>
"""


def main():
    book_bays = bays()
    app_rows = apps()
    data = json.dumps({"bays": book_bays, "apps": app_rows}, ensure_ascii=False, separators=(",", ":"))
    # A title containing "</script" would end the data block early.
    data = data.replace("</", "<\\/")
    out = PAGE.format(
        n_books=sum(len(b["items"]) for b in book_bays),
        n_apps=len(app_rows),
        plain=plain_list(book_bays, app_rows),
        data=data,
        year=datetime.date.today().year,
    )
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(out, encoding="utf-8")
    print("immersive: %d bays, %d covers, %d apps" % (
        len(book_bays), sum(len(b["items"]) for b in book_bays), len(app_rows)))


if __name__ == "__main__":
    main()
