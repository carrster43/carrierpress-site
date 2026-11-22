"""Share cards for the book pages: assets/og/books/<slug>.jpg, 1200x630.

LOCAL ONLY, like make_app_og.py: it drives headless Chrome, which CI does not
have, so the JPEGs are committed and books.py only checks whether a card
exists (books.og_card). With a card, a book page offers it as a large link
preview; without one, the page keeps the old small cover thumbnail.

Run after adding a book, retitling one, or changing a hook or cover:
    PYTHONDONTWRITEBYTECODE=1 python3 make_book_og.py            # every book
    PYTHONDONTWRITEBYTECODE=1 python3 make_book_og.py <slug> ...  # just these
then python3 build.py, so the pages pick up any new card.

Every word on a card comes from catalog.json: shelf, title, author, and the
hook (else the first sentence of the description), so a card cannot say
something the book page does not. No price: the foot says only what is true of
that title (foot_for), read from catalog.json and formats.json. "In print on
Amazon", not "and at bookstores": not every title is with IngramSpark yet.

Speed: this Chrome takes ~15s to shut down after each screenshot, so cards are
drawn by WORKERS Chromes at once, each with its own profile. (Drawing many to
one tall page and cutting it with sips was tried: sips misplaced some crops.)
"""
import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import books

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "assets" / "og" / "books"
COVERS = HERE / "assets" / "covers"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H, WORKERS = 1200, 630, 8
CUTS = [": ", ", with ", ", and ", ", but "]


def sentences(text):
    # Some descriptions join paragraphs with no space ("rejected.One"), so a
    # full stop followed straight by a capital also ends a sentence.
    return [s for s in re.split(r"(?<=[.!?])\s+|(?<=[a-z][.!?])(?=[A-Z])", text.strip()) if s]


def line_for(D, b):
    """The hook, else the description's opening, kept to about two lines."""
    hook = b.get("hook") or books._own_line(D, b["a"])
    about = [p for p in (b.get("desc") or []) if str(p).strip()]
    src = hook or (about[0] if about else "")
    src = re.sub(r"(?<=[a-z][.!?])(?=[A-Z])", " ", src.strip())
    if not src:
        return ""
    if len(src) <= 140:
        return src
    first = sentences(src)[0]
    # Short opening sentences ("A globe. A sundial.") read as one beat: keep
    # adding them while the line stays under 140.
    out = first
    for s in sentences(src)[1:]:
        if len(out) + 1 + len(s) > 140:
            break
        out += " " + s
    if len(out) <= 150:
        return out
    hits = [first.index(c) for c in CUTS if c in first and first.index(c) >= 40]
    return first[:min(hits)].rstrip(" ,") + "." if hits else ""


def foot_for(F, b):
    if b.get("narrator"):
        return "Audiobook"
    if b.get("soon"):
        return "Coming soon"
    fmts = " ".join(f.get("f", "") for f in (F.get(b["a"]) or {}).get("formats", [])).lower()
    if any(w in fmts for w in ("paperback", "hardcover", "spiral", "board")):
        return "In print on Amazon"
    return "On Amazon"


CARD = """<div class="card"><div class="cv{sq}"><img src="{cover}" alt=""></div>
<div class="tx"><div class="eb">{shelf}</div><h1 style="font-size:{size}px">{title}</h1>
<div class="by">{by}</div>{line}</div>
<div class="ft"><img src="{mark}" alt="">Carrier Press &middot; {foot}</div></div>"""

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0}
html,body{width:1200px;background:#1a1a2e}
.card{position:relative;width:1200px;height:630px;overflow:hidden;background:#1a1a2e;color:#f3eee2;
  font-family:Georgia,'Iowan Old Style',serif;border-bottom:10px solid #e8c84a}
.cv{position:absolute;left:70px;top:62px;height:470px;width:294px}
.cv.sq{width:470px}
.cv img{width:100%;height:100%;object-fit:cover;display:block;border-radius:4px;
  box-shadow:0 18px 50px rgba(0,0,0,.55),0 2px 6px rgba(0,0,0,.4)}
.tx{position:absolute;left:430px;right:64px;top:0;bottom:110px;display:flex;flex-direction:column;justify-content:center}
.sq~.tx{left:606px}
.eb{font:700 19px/1.2 'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#e8c84a}
h1{font-weight:700;line-height:1.05;margin:18px 0 14px;letter-spacing:-.3px}
.by{font:400 30px/1.2 Georgia,serif;color:#c9c4b6}
p{font:italic 400 28px/1.34 Georgia,serif;color:#e4dfd2;margin-top:24px}
.ft{position:absolute;left:430px;bottom:42px;font:400 22px/1 Georgia,serif;color:#e8c84a;display:flex;align-items:center;gap:12px}
.sq~.ft{left:606px}
.ft img{width:44px;height:auto}
</style></head><body>{cards}</body></html>"""


def card(D, S, F, b, sec):
    title = books.display_title(b, sec)
    n = len(title)
    size = 72 if n <= 18 else 62 if n <= 26 else 54 if n <= 36 else 46
    line = line_for(D, b)
    if not line and b.get("narrator"):
        line = "Narrated by %s." % b["narrator"]
    return CARD.format(
        sq=" sq" if b.get("square") else "",
        cover=(COVERS / ("%s.jpg" % b["a"])).as_uri(),
        shelf=html.escape(sec["name"]),
        title=html.escape(title), size=size,
        by="by " + html.escape(b.get("by") or S["author"]),
        line="<p>%s</p>" % html.escape(line) if line else "",
        foot=html.escape(foot_for(F, b)),
        mark=(HERE / "assets" / "logo-mark-light-small.png").as_uri())


def shoot(card_html, out, tmp):
    work = pathlib.Path(tmp) / out.stem
    work.mkdir()
    src, png = work / "card.html", work / "card.png"
    src.write_text(PAGE.replace("{cards}", card_html), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=%d,%d" % (W, H),
                    "--allow-file-access-from-files", "--no-first-run",
                    "--user-data-dir=%s" % (work / "profile"),
                    "--screenshot=%s" % png, src.as_uri()],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Not the exit code: this Chrome writes the file, then crashes on teardown.
    if not png.exists():
        raise SystemExit("no card written for %s" % out.name)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86",
                    str(png), "--out", str(out)], check=True, stdout=subprocess.DEVNULL)
    return out.stem


def main(only):
    D = json.load(open(HERE / "catalog.json"))
    S = D["site"]
    F = json.load(open(HERE / "formats.json"))["books"]
    OUT.mkdir(parents=True, exist_ok=True)
    recs = [r for r in books.records(D)
            if (not only or r[2] in only) and (COVERS / ("%s.jpg" % r[0]["a"])).exists()]
    with tempfile.TemporaryDirectory() as tmp, ThreadPoolExecutor(WORKERS) as pool:
        jobs = [pool.submit(shoot, card(D, S, F, b, sec), OUT / ("%s.jpg" % slug), tmp)
                for b, sec, slug in recs]
        for k, j in enumerate(jobs, 1):
            j.result()
            if k % 20 == 0 or k == len(jobs):
                print("  %d/%d" % (k, len(jobs)), flush=True)
    print("book share cards: %d -> %s" % (len(recs), OUT.relative_to(HERE)))


if __name__ == "__main__":
    main(set(sys.argv[1:]))
