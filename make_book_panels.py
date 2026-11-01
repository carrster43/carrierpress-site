#!/usr/bin/env python3
"""
The real spine and back of a book, for the 3D book (assets/xr/book3d.js).

    python3 make_book_panels.py     # needs Pillow, pdftoppm and the wrap PDFs

WHAT IT DOES. For each title in WRAPS it renders that title's print wrap (the
paperback cover file uploaded to KDP or IngramSpark) and cuts out the two panels
the 3D book needs:

    assets/covers/spine/<ASIN>.jpg   the spine, 1000px tall
    assets/covers/back/<ASIN>.jpg    the back cover, 500px tall, like the fronts

and records each book's trim and spine width in assets/covers/panels.json.
books.b3_attrs reads that file, so the 3D book is the real trim, the real spine
thickness and the real spine and back. A title not listed here keeps the drawn
spine in the cover's own colour.

THE GEOMETRY COMES FROM THE PAGE, NOT THE FILENAME. A wrap is bleed, back,
spine, front, bleed, with .125in bleed all round. Trim height is the page height
less .25in; trim width is the standard trim for that height; the spine is what
is left. Filenames carry page counts that are sometimes stale (the KIY folder
has 135, 230 and 232 page wraps), so they are never parsed.

WHY THE OUTPUT IS COMMITTED. The wraps live in ~/Documents/A_Publishing_House,
outside this repo, and Pillow is not in the standard library. Every build reads
the committed panels.json and JPGs, so the site builds anywhere and CI does not
run this.

⭐ CHECK THE PAIRING BY EYE AFTER EVERY RUN. It writes panels_check.jpg (not
committed): site cover, wrap front, spine, back, one row per title. A wrap that
belongs to another edition, or carries placeholder art, shows up there and
nowhere else. Added 2026-11-01 for the Top 10; all ten rows matched.
"""
import json, pathlib, subprocess, sys, tempfile

try:
    from PIL import Image
except ImportError:
    sys.exit("make_book_panels.py needs Pillow (pip install pillow), run it in a venv.")

HOME = pathlib.Path.home() / "Documents/A_Publishing_House"
CL = "Classics/Classics_Republish"
# ASIN: the paperback wrap that matches the live listing (front checked by eye).
WRAPS = {
    "B0H7W7VY7S": f"{CL}/PRODUCTION/02_King_in_Yellow/3_COVER/KIY_PAPERBACK_WRAP_6x9_232pp_IS.pdf",
    "B0HGG934BB": f"{CL}/PRODUCTION/05_Carcosa_Omnibus/3_COVER/Carcosa_PAPERBACK_wrap_12.575x9.25_130pp.pdf",
    "B0H7QFWVXG": f"{CL}/PREPRODUCTION/05_Blue_Castle/3_COVER/The_Blue_Castle_WRAP_5.5x8.5_266pp_KDP_RGB_300dpi.pdf",
    "B0H7LYK2QQ": f"{CL}/PRODUCTION/01_Dr_Mabuse_Translation/3_COVER/MABUSE_WRAP_6x9_cream_245pp_FINAL_RGB_300dpi.pdf",
    "B0H7PZ3FDM": f"{CL}/PREPRODUCTION/06_Enchanted_April/3_COVER/The_Enchanted_April_WRAP_5.5x8.5_274pp_TITLESAFE_KDP_RGB_300dpi.pdf",
    "B0H7QPDD4S": f"{CL}/PREPRODUCTION/07_Mysteries_of_Udolpho/3_COVER/The_Mysteries_of_Udolpho_WRAP_6x9_819pp_KDP_RGB_300dpi.pdf",
    "B0HHJK9GMT": "Carrier Press/Books/The American Firsts/02 - Twelve Minutes on River Road (Camden 1949)/covers/kdp_wrap/Twelve_Minutes_WRAP_12.095x8.75_KDP.pdf",
    "B0H2Y3TMMC": f"{CL}/PRODUCTION/15_Meyrink_Golem_Translation/3_COVER/Golem_PAPERBACK_wrap_12.92x9.25_268pp.pdf",
    "B0H4CCMSQS": "Carrier Press/Box Sets/The Marjorie Corey Files - Complete Series (5 Books)/covers/marjorie_wrap_KDP_RGB_v3.pdf",
    "B0H7PDG821": f"{CL}/_KDP_CLASSICS_UPLOAD/Monk/The_Monk_Full_Wrap_13.27x9.25_300DPI.pdf",
}
DPI, BLEED = 150, 0.125
TRIM_W = {9.0: 6.0, 8.5: 5.5, 8.0: 5.0}
OUT = pathlib.Path("assets/covers")


def render(pdf, tmp):
    stem = pathlib.Path(tmp) / "wrap"
    subprocess.run(["pdftoppm", "-r", str(DPI), "-f", "1", "-l", "1", "-png", "-singlefile",
                    str(pdf), str(stem)], check=True)
    return Image.open(f"{stem}.png").convert("RGB")


def main():
    (OUT / "spine").mkdir(exist_ok=True)
    (OUT / "back").mkdir(exist_ok=True)
    panels, rows = {}, []
    for asin, rel in WRAPS.items():
        with tempfile.TemporaryDirectory() as tmp:
            im = render(HOME / rel, tmp)
        W, H = im.size[0] / DPI, im.size[1] / DPI
        th = round((H - 2 * BLEED) * 4) / 4
        tw = TRIM_W[th]
        sp = W - 2 * tw - 2 * BLEED
        if not 0.05 < sp < 3:
            sys.exit(f"{asin}: spine {sp:.3f}in is not a spine; is {rel} a paperback wrap?")
        px = lambda v: round(v * DPI)
        y0, y1 = px(BLEED), px(BLEED + th)
        back = im.crop((px(BLEED), y0, px(BLEED + tw), y1))
        spine = im.crop((px(BLEED + tw), y0, px(BLEED + tw + sp), y1))
        front = im.crop((px(BLEED + tw + sp), y0, px(BLEED + 2 * tw + sp), y1))
        back.resize((round(500 * tw / th), 500), Image.LANCZOS).save(
            OUT / f"back/{asin}.jpg", quality=82, optimize=True, progressive=True)
        spine.resize((max(8, round(1000 * sp / th)), 1000), Image.LANCZOS).save(
            OUT / f"spine/{asin}.jpg", quality=85, optimize=True)
        panels[asin] = {"trim": [tw, th], "spine": round(sp, 3)}

        h = 300
        cover = Image.open(OUT / f"{asin}.jpg").convert("RGB")
        parts = [cover.resize((round(h * cover.width / cover.height), h)), front.resize((round(h * tw / th), h)),
                 spine.resize((max(4, round(h * sp / th)), h)), back.resize((round(h * tw / th), h))]
        row = Image.new("RGB", (sum(p.width + 10 for p in parts), h), "white")
        x = 0
        for p in parts:
            row.paste(p, (x, 0))
            x += p.width + 10
        rows.append(row)
        print(f"{asin}  {tw}x{th}  spine {sp:.3f}in")

    (OUT / "panels.json").write_text(json.dumps(panels, indent=1, sort_keys=True) + "\n")
    sheet = Image.new("RGB", (max(r.width for r in rows), sum(r.height + 12 for r in rows)), "white")
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height + 12
    sheet.save("panels_check.jpg", quality=80)
    print(f"{len(panels)} titles. Now LOOK at panels_check.jpg.")


if __name__ == "__main__":
    main()
