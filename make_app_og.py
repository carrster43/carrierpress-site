"""Share cards for the app pages: apps/og/<slug>.png and apps/og/index.png, 1200x630.

LOCAL ONLY. It drives headless Chrome, which CI does not have, so the PNGs are
committed and the page generators only check whether a card exists:
make_app_pages.py (apps/<slug>/), make_support.py (/<slug>/) and
make_privacy.py (/<slug>/privacy/) use apps/og/<slug>.png when it is there,
and apps/og/index.png otherwise. /apps/ uses apps/og/index.png.

Before this, an app page offered either the Carrier Press books card or a tall
phone screenshot that a 1.91:1 preview crops to a strip.

Run after adding an app, renaming one, or changing its headline or blurb:
    PYTHONDONTWRITEBYTECODE=1 python3 make_app_og.py
then the usual regenerate sequence, so the pages pick up any new card.

Every word on a card comes from apps_data.py (name, headline, else the first
sentence of the blurb), so a card cannot say something the page does not.
"""
import html
import json
import pathlib
import re
import subprocess
import tempfile

import apps_data
import folds

HERE = pathlib.Path(__file__).resolve().parent
ICONS = HERE / "apps" / "icons"
OUT = HERE / "apps" / "og"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ACCENTS = json.loads((ICONS / "accents.json").read_text())
NAVY = "#1a1a2e"
# The /apps/ card shows these icons, in this order, when they exist.
SHOWCASE = ["cast", "flare", "papertrail", "boatready", "handoff", "pillproof"]

# Where a long first sentence can end cleanly. Earliest cut that leaves at least
# 30 characters wins; a sentence of 120 characters or fewer is kept whole.
CUTS = [": ", ", with ", ", including ", ", across ", ", and ", ", plus "]


def line_for(app):
    if app.get("headline"):
        return app["headline"]
    first = re.split(r"(?<=[.!?])\s", app["blurb"])[0]
    if len(first) <= 120:
        return first
    hits = [first.index(c) for c in CUTS if c in first and first.index(c) >= 30]
    return first[:min(hits)].rstrip(" ,") + "." if hits else first


CSS = """
*{box-sizing:border-box;margin:0}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:var(--bg);color:#fff;font-family:Georgia,'Iowan Old Style',serif;position:relative}
.eyebrow{font:700 22px/1 'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.78)}
.foot{position:absolute;left:80px;bottom:56px;font:700 22px/1 'Helvetica Neue',Helvetica,Arial,sans-serif;color:rgba(255,255,255,.78)}
.bar{position:absolute;left:0;right:0;bottom:0;height:10px;background:#e8c84a}
"""

APP = """<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{css}
.icon{{position:absolute;left:80px;top:150px;width:260px;height:260px;border-radius:58px;
  box-shadow:0 10px 40px rgba(0,0,0,.35);background:rgba(255,255,255,.14);overflow:hidden;
  display:flex;align-items:center;justify-content:center;font:700 130px/1 Georgia,serif}}
.icon img{{width:100%;height:100%;display:block}}
.text{{position:absolute;left:400px;right:70px;top:0;bottom:120px;display:flex;flex-direction:column;justify-content:center}}
h1{{font:700 {size}px/1.02 Georgia,serif;margin:20px 0 22px;letter-spacing:-.5px}}
p{{font:400 34px/1.3 Georgia,serif;color:rgba(255,255,255,.92)}}
</style></head><body style="--bg:{bg}">
<div class="icon">{icon}</div>
<div class="text"><div class="eyebrow">An app from Carrier Labs</div><h1>{name}</h1><p>{line}</p></div>
<div class="foot">carrierpress.com/apps</div><div class="bar"></div>
</body></html>"""

INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{css}
.text{{position:absolute;left:80px;right:80px;top:84px}}
h1{{font:700 76px/1.04 Georgia,serif;margin:20px 0 18px;letter-spacing:-.5px}}
p{{font:400 34px/1.3 Georgia,serif;color:rgba(255,255,255,.88)}}
.row{{position:absolute;left:80px;bottom:120px;display:flex;gap:26px}}
.row img{{width:132px;height:132px;border-radius:30px;box-shadow:0 8px 28px rgba(0,0,0,.4)}}
</style></head><body style="--bg:{bg}">
<div class="text"><div class="eyebrow">Carrier Labs LLC</div><h1>Apps from Carrier Labs</h1>
<p>Each built to do one job well. Open them in your browser today.</p></div>
<div class="row">{icons}</div>
<div class="foot">carrierpress.com/apps</div><div class="bar"></div>
</body></html>"""


def shoot(page_html, out, tmp):
    src = pathlib.Path(tmp) / (out.stem + ".html")
    src.write_text(page_html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,630",
                    "--allow-file-access-from-files", "--no-first-run",
                    # Its own profile: other headless Chromes on this Mac hold
                    # the default one, and a second user of it exits 2 or hangs.
                    "--user-data-dir=%s" % (pathlib.Path(tmp) / "profile"),
                    "--screenshot=%s" % out, src.as_uri()],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Not the exit code: this Chrome writes the file, then crashes on teardown
    # (status 2). The file being there, and new, is the real test.
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        raise SystemExit("no card written for %s" % out.name)


def card_url(slug, domain="carrierpress.com"):
    """The share image for an app's pages: its own card, else the /apps/ card."""
    name = "%s.png" % slug if (OUT / ("%s.png" % slug)).exists() else "index.png"
    return "https://%s/apps/og/%s" % (domain, name)


def main():
    OUT.mkdir(exist_ok=True)
    made = []
    with tempfile.TemporaryDirectory() as tmp:
        for app in apps_data.APPS:
            slug = app.get("slug")
            if not slug or slug in folds.FOLDED:
                continue
            ico = ICONS / ("%s.webp" % slug)
            icon = ('<img src="%s" alt="">' % ico.as_uri() if ico.exists()
                    else html.escape(app["name"][0]))
            name = app["name"]
            page = APP.format(css=CSS, bg=ACCENTS.get(slug, NAVY), icon=icon,
                              name=html.escape(name), line=html.escape(line_for(app)),
                              size=92 if len(name) <= 12 else 76)
            shoot(page, OUT / ("%s.png" % slug), tmp)
            made.append(slug)
        icons = "".join('<img src="%s" alt="">' % (ICONS / ("%s.webp" % s)).as_uri()
                        for s in SHOWCASE if (ICONS / ("%s.webp" % s)).exists())
        shoot(INDEX.format(css=CSS, bg=NAVY, icons=icons), OUT / "index.png", tmp)
    print("app share cards: %d apps + index -> %s" % (len(made), OUT.relative_to(HERE)))


if __name__ == "__main__":
    main()
