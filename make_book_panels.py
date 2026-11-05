#!/usr/bin/env python3
"""
The real spine and back of a book, for the 3D book (assets/xr/book3d.js).

    python3 make_book_panels.py     # needs Pillow, pdftoppm and the wrap PDFs
    python3 make_book_panels.py B0H7R61S7C B0H7R7Y1N4   # only these; the rest kept

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
committed; panels_check_2.jpg and on past ten titles): site cover, wrap
front, spine, back, one row per title. A wrap that
belongs to another edition, or carries placeholder art, shows up there and
nowhere else. Added 2026-11-01 for the Top 10, then the rest the same day.
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
    # ChatGPT full wrap at an estimated 300 pages (.75in spine). Re-cut if the interior differs.
    "THE-NOISE-FLOOR": "../THE_NOISE_FLOOR/covers/Noise_Floor_wrap_13.0x9.25.pdf",
    "B0H7W7VY7S": f"{CL}/PRODUCTION/02_King_in_Yellow/3_COVER/KIY_PAPERBACK_WRAP_6x9_232pp_IS.pdf",
    "B0HGG934BB": f"{CL}/PRODUCTION/05_Carcosa_Omnibus/3_COVER/Carcosa_PAPERBACK_wrap_12.575x9.25_130pp.pdf",
    "B0HQCG586W": f"{CL}/PRODUCTION/18_Bierce_Can_Such_Things_Be/3_COVER/Bierce_PAPERBACK_wrap_12.78x9.25_212pp.pdf",
    "B0HQ55DVX2": f"{CL}/PRODUCTION/17_Lovecraft_Call_of_Cthulhu/3_COVER/Lovecraft_PAPERBACK_wrap_12.69x9.25_176pp.pdf",
    "B0H7QFWVXG": f"{CL}/PREPRODUCTION/05_Blue_Castle/3_COVER/The_Blue_Castle_WRAP_5.5x8.5_266pp_KDP_RGB_300dpi.pdf",
    "B0H7LYK2QQ": f"{CL}/PRODUCTION/01_Dr_Mabuse_Translation/3_COVER/MABUSE_WRAP_6x9_cream_245pp_FINAL_RGB_300dpi.pdf",
    "B0H7PZ3FDM": f"{CL}/PREPRODUCTION/06_Enchanted_April/3_COVER/The_Enchanted_April_WRAP_5.5x8.5_274pp_TITLESAFE_KDP_RGB_300dpi.pdf",
    "B0H7QPDD4S": f"{CL}/PREPRODUCTION/07_Mysteries_of_Udolpho/3_COVER/The_Mysteries_of_Udolpho_WRAP_6x9_819pp_KDP_RGB_300dpi.pdf",
    "B0HHJK9GMT": "Carrier Press/Books/The American Firsts/02 - Twelve Minutes on River Road (Camden 1949)/covers/kdp_wrap/Twelve_Minutes_WRAP_12.095x8.75_KDP.pdf",
    "B0H2Y3TMMC": f"{CL}/PRODUCTION/15_Meyrink_Golem_Translation/3_COVER/Golem_PAPERBACK_wrap_12.92x9.25_268pp.pdf",
    "B0H4CCMSQS": "Carrier Press/Box Sets/The Marjorie Corey Files - Complete Series (5 Books)/covers/marjorie_wrap_KDP_RGB_v3.pdf",
    "B0H7PDG821": f"{CL}/_KDP_CLASSICS_UPLOAD/Monk/The_Monk_Full_Wrap_13.27x9.25_300DPI.pdf",
    # 2026-11-01, the rest of the catalogue: the wrap whose spine fits the live
    # paperback's page count, KDP/RGB before IngramSpark/CMYK. Not listed, so
    # drawn: no paperback (Letters for Cash), no wrap on disk (All About
    # Feelings, both Ghost Stories, The Recipe Notebooks), or only wraps for
    # another page count (6000 Tons of Gold, Artful Anticks, The Laughing
    # Willow, The Mech Workshop Machine, The Runaway Crate), or the wrap's front
    # is not the live cover on panels_check (Stealing First Base, Digital Gold
    # Rush, The Morning Table, Portal Park, The Pencil Under the Bench).
    "B07VPL3FS3": "Carrier Press/Books/Standalone Novels/Who Wants To Be Greek - English Narrative/covers/Who_Wants_to_Be_Greek_KDP_Wrap_SPINEFIX.pdf",
    "B07X4CGTKR": "Carrier Press/Classics/The Surprise Book/covers/The_Surprise_Book_WRAP_6x9_180pp_KDP_300dpi.pdf",
    "B07X7H37LC": "Carrier Press/Classics/Dancers in the Dark/covers/Dancers_WRAP_RGB_KDP_v3_EDGECLEAR.pdf",
    "B07XKDY286": "Carrier Press/Classics/A New History of Blue Beard/covers/A_New_History_of_Blue_Beard_WRAP_6x9_84pp_EXTENDED_KDP_300dpi.pdf",
    "B0GX2YNHT9": "Carrier Press/Books/Nonfiction/Passive Income Blueprint/covers/passive_blueprint_wrap_KDP_RGB_v2.pdf",
    "B0GX34KKKQ": f"{CL}/PRODUCTION/16_Sidis_Animate_Inanimate/3_COVER/Sidis_PAPERBACK_wrap_12.605x9.25_142pp.pdf",
    "B0GX38GVW3": "Carrier Press/Books/Nonfiction/Automation Income Systems/covers/automation_wrap_KDP_RGB_v2.pdf",
    "B0GXP2C498": "Carrier Press/Books/The Gadget Sandbox Chronicles/Book 01 - The First Build/covers/first_build_wrap_KDP_RGB_v2.pdf",
    "B0GXW2XL1N": "Carrier Press/Books/The Marjorie Corey Files/Book 03 - The Sea Captain's Portrait/covers/The_Sea_Captains_Portrait_wrap_300dpi.pdf",
    "B0GYBT12DP": "Carrier Press/Books/Nonfiction/Side Hustle Jr/covers/Side_Hustle_Junior_6x9_0.417in_spine_300dpi_CMYK_BioFix.pdf",
    "B0GYWWCLG8": "Carrier Press/Books/Standalone Novels/Concrete Mirrors/covers/concrete_mirrors_wrap_KDP_RGB_v2.pdf",
    "B0GZCKYKZ9": "Carrier Press/Books/The Marjorie Corey Files/Book 01 - The Second Shooter/covers/The_Second_Shooter_Full_Wrap_300dpi.pdf",
    "B0GZJ9DPJC": f"{CL}/PREPRODUCTION/11_Green_Mummy/3_COVER/GREEN_MUMMY_WRAP_276pp_RGB_KDP.pdf",
    "B0H1LG32RB": "Carrier Press/Books/Standalone Novels/The Last Adviser/covers/TLA_paperback_wrap_RGB_KDP.pdf",
    "B0H278QHQH": "Carrier Press/Books/YA and Genre Fiction/The Digital Founders/covers/digital_founders_wrap_6x9_492pp_KDP_RGB_v3.pdf",
    "B0H2WM1V3D": "Carrier Press/Books/The Glitch Blocks (Captain Cubemelon Novels)/Book 05 - The Moving Line/covers/Bk5_The_Moving_Line_WRAP_FINAL_164pp_KDP_RGB_300dpi.pdf",
    "B0H3G5L8JW": "Carrier Press/Books/Nonfiction/Safe Online Projects for Kids/covers/safe_online_wrap_5x8_122pp_KDP_RGB_300dpi.pdf",
    "B0H3KKRTMP": "Carrier Press/Classics/The Secret of Chimneys/covers/CHIMNEYS_WRAP_262pp_RGB_KDP.pdf",
    "B0H3ZQZ3Z8": "Carrier Press/Books/The Glitch Blocks (Captain Cubemelon Novels)/Book 04 - The Broken Save/covers/Bk4_The_Broken_Save_WRAP_FINAL_156pp_KDP_RGB_300dpi.pdf",
    "B0H46VTCYP": "Carrier Press/Books/Nonfiction/AI Income Streams/covers/ai-income-streams-WRAP-FINAL-168pg.pdf",
    "B0H47ZCBH1": "Carrier Press/Books/Standalone Novels/The Fortune Weaver/covers/the_fortune_weaver_NO_AUTHOR_PHOTO_IS_CMYK_SWOP.pdf",
    "B0H483NLCV": "Carrier Press/Books/Standalone Novels/The Starlight Secret Society/covers/the_starlight_secret_society_cover_wrap.pdf",
    "B0H48WBFTD": "Carrier Press/Books/Standalone Novels/The Sterling Conspiracy/covers/the_sterling_wrap_6x9_346pp_13.03x9.25_0.78spine_KDP_RGB_300dpi.pdf",
    "B0H4BQSGB6": "Carrier Press/Books/Standalone Novels/Who Wants To Be Greek - Bilingual/covers/WWTBG_Bilingual_6x9_wrap_KDP_RGB.pdf",
    "B0H4BSJQYV": "Carrier Press/Books/The Marjorie Corey Files/Book 04 - The Prattler Files/covers/The_Prattler_Files_Full_Wrap_300dpi.pdf",
    "B0H4DFKCGC": "Carrier Press/Books/Nonfiction/Seeded for Success/covers/seeded_wrap_IS_CMYK_v2.pdf",
    "B0H4DQ6488": "Carrier Press/Books/YA and Genre Fiction/The Startup Club/covers/startup_club_wrap_6x9_258pp_12.831x9.250_300dpi_RGB.pdf",
    "B0H4DR314J": "Carrier Press/Books/Nonfiction/The Passive Income Dividend System/covers/passive_dividend_wrap_KDP_RGB_v2.pdf",
    "B0H4DTYL5S": "Carrier Press/Books/YA and Genre Fiction/The Growing Fortune/covers/growing_fortune_wrap_6x9_KDP_RGB_SAFEFIX.pdf",
    "B0H4DX9RRF": "Carrier Press/Books/YA and Genre Fiction/The Billionaire's Legacy Game/covers/billionaire_wrap_KDP_RGB_6x9_SAFEFIX.pdf",
    "B0H597VNJ5": "Carrier Press/Books/The Gadget Sandbox Chronicles/Book 04 - Sky Islands Save File/covers/Book_04_Sky_Islands_Save_File_WRAP_2E_CREAM_164pp_KDP_RGB_300dpi.pdf",
    "B0H59JV13T": "Carrier Press/Books/The Keystone Cycle/Book 05 - The Roebuck Bay Record/covers/The_Roebuck_Bay_Record_KDP_White_660pp_Complementary_Wrap.pdf",
    "B0H59MBV8R": "Carrier Press/Books/The Keystone Cycle/Book 01 - The Drosos Ledger/covers/The_Drosos_Ledger_PHOTO_RAISED_IS_CMYK.pdf",
    "B0H59N5CVT": "Carrier Press/Books/The Keystone Cycle/Book 02 - The Hudson Creek Record/covers/The_Hudson_Creek_Record_KDP_White_502pp_Complementary_Wrap.pdf",
    "B0H59PY6VD": "Carrier Press/Books/The Keystone Cycle/Book 03 - The Sfax Letters/covers/The_Sfax_Letters_IS_CMYK_PDFX1a.pdf",
    "B0H59QNK51": "Carrier Press/Books/The Gadget Sandbox Chronicles/Book 03 - The Frost Cave Reset/covers/Book_03_The_Frost_Cave_Reset_WRAP_2E_CREAM_190pp_KDP_RGB_300dpi.pdf",
    "B0H6CK8NB6": "_KDP_UPLOAD/TLO_READABILITY_2026-10-02/TLO_2_The_Pearl_Ledger/3_KDP_PAPERBACK_COVER_The_Pearl_Ledger_12.913x9.250_Cream_264pp_KDP_300dpi_wrap_READABILITY.pdf",
    "B0H6CWP5GN": "_KDP_UPLOAD/TLO_READABILITY_2026-10-02/TLO_1_The_Sponge_Cache/3_KDP_PAPERBACK_COVER_The_Sponge_Cache_12.887x9.250_Cream_254pp_KDP_300dpi_wrap_READABILITY.pdf",
    "B0H6D8M2T1": "_KDP_UPLOAD/TLO_READABILITY_2026-10-02/TLO_4_The_Mastic_Codex/3_KDP_PAPERBACK_COVER_The_Mastic_Codex_12.893x9.250_Cream_256pp_KDP_300dpi_wrap_READABILITY.pdf",
    "B0H6DCTJ2F": "_KDP_UPLOAD/TLO_READABILITY_2026-10-02/TLO_3_The_Sixth_Cache/3_KDP_PAPERBACK_COVER_The_Sixth_Cache_12.933x9.250_Cream_272pp_KDP_300dpi_wrap_READABILITY.pdf",
    "B0H6DKF4ZK": "_KDP_UPLOAD/TLO_READABILITY_2026-10-02/TLO_5_The_Seven_Plates/3_KDP_PAPERBACK_COVER_The_Seven_Plates_12.927x9.250_Cream_270pp_KDP_300dpi_wrap_READABILITY.pdf",
    "B0H6F76741": "Carrier Press/Books/The Glitch Blocks (Captain Cubemelon Novels)/Book 03 - The Loop That Spoke/covers/Bk3_The_Loop_That_Spoke_WRAP_FINAL_164pp_KDP_RGB_300dpi.pdf",
    "B0H6F7KGGK": "Carrier Press/Books/The Glitch Blocks (Captain Cubemelon Novels)/Book 02 - Static Orchard/covers/Bk2_Static_Orchard_WRAP_FINAL_168pp_KDP_RGB_300dpi.pdf",
    "B0H6FH7TB7": "Carrier Press/Books/The Glitch Blocks (Captain Cubemelon Novels)/Book 01 - The First Flicker/covers/Book_07_The_First_Flicker_2E_wrap_KDP_RGB.pdf",
    "B0H6V88BL1": "Carrier Press/Books/The Glitch Blocks (Captain Cubemelon Novels)/Book 06 - The Between Badge/covers/Bk6_The_Between_Badge_WRAP_FINAL_158pp_KDP_RGB_300dpi.pdf",
    "B0H6VGK2MZ": "Carrier Press/Books/Standalone Novels/Beneath the Surface/covers/BTS_paperback_wrap_RGB_KDP.pdf",
    "B0H7NMYT5J": "Carrier Press/Classics/The Murder of Roger Ackroyd/covers/ACKROYD_WRAP_246pp_RGB_KDP.pdf",
    "B0H7P6LRQJ": "Archive/Completed/Publishing/KDP-filed-staging/PB_REVISION_The_Defects_That_Pass_Review/The_Defects_That_Pass_Review_WRAP_6x9_188pp_KDP_v4.pdf",
    "B0H7PDS3QM": f"{CL}/PREPRODUCTION/08_Arsene_Lupin/3_COVER/Arsene_Lupin_WRAP_6x9_186pp_KDP_RGB_300dpi.pdf",
    "B0H7QSD429": "Carrier Press/Classics/The Man Who Was Thursday/covers/The_Man_Who_Was_Thursday_WRAP_5.5x8.5_209pp_KDP_RGB_300dpi.pdf",
    "B0H7VNFRN4": f"{CL}/PREPRODUCTION/12_Honeymoon_in_Space/3_COVER/out/HONEYMOON_IN_SPACE_WRAP_RGB.pdf",
    "B0H7WM2CHN": "Carrier Press/Classics/The Man Who Robbed the Bank of England/covers/BIDWELL_370pp_ISSPINE_WRAP_CMYK_SWOP_IS.pdf",
    "B0HGMSMFQK": f"{CL}/PRODUCTION/07_Machen_Great_God_Pan/3_COVER/Machen_PAPERBACK_wrap_12.64x9.25_156pp.pdf",
    "B0HGS6TH57": f"{CL}/PRODUCTION/06_Chambers_Mystery_of_Choice/3_COVER/Chambers_PAPERBACK_wrap_12.735x9.25_194pp.pdf",
    "B0HGTD7VBZ": f"{CL}/PRODUCTION/08_Blackwood_Willows_Wendigo/3_COVER/Blackwood_PAPERBACK_wrap_12.685x9.25_174pp.pdf",
    "B0HGVD689V": f"{CL}/PRODUCTION/11_Wattles_Science_Getting_Rich/3_COVER/Wattles_PAPERBACK_wrap_12.55x9.25_120pp.pdf",
    "B0HHJSF9SP": "Carrier Press/Books/The American Firsts/01 - One Minute Past Noon (Wall Street 1920)/covers/kdp_wrap/FINAL_One_Minute_Past_Noon_wrap_12.175x8.75_300dpi.pdf",
    "B0HL27ZXPJ": f"{CL}/PRODUCTION/13_Machen_Three_Impostors/3_COVER/Impostors_PAPERBACK_wrap_12.705x9.25_182pp.pdf",
    "B0HMK4LL3B": "Carrier Press/Books/The American Firsts/03 - Mrs. Kehoe (Bath 1927)/covers/kdp_wrap/Mrs_Kehoe_WRAP_12.08x8.75_300dpi.pdf",
    "B0HMZKCTTS": f"{CL}/PRODUCTION/12_Chesterton_Father_Brown/3_COVER/FatherBrown_PAPERBACK_wrap_13.3300x9.2500_432pp.pdf",
    "B0HN3HJJBR": "Carrier Press/Books/The Atherton Manor Mysteries/_SERIES/covers/book2_the-music-of-the-spheres/3_COVER/CHATGPT_2026-10-14/Music_of_the_Spheres_KDP_wrap_3603x2625_338pp.pdf",
    "B0HNGNHF35": "Carrier Press/Books/The Atherton Manor Mysteries/_SERIES/covers/book3_the-tower-on-the-highest-hill/3_COVER/CHATGPT_2026-10-14/Tower_on_the_Highest_Hill_KDP_wrap_3599x2625_331pp.pdf",
    # Sweeney Todd: catalog ASINs fixed in b4dda51; B0H7R61S7C is Volume One.
    "B0H7R61S7C": f"{CL}/PRODUCTION/03_Sweeney_Todd_String_of_Pearls/_IS_SWEENEY_UPLOAD/SWEENEY_VOL1_WRAP_RGB.pdf",
    "B0H7R7Y1N4": f"{CL}/PRODUCTION/03_Sweeney_Todd_String_of_Pearls/_IS_SWEENEY_UPLOAD/SWEENEY_VOL2_WRAP_RGB.pdf",
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
    only = sys.argv[1:]
    old = json.loads((OUT / "panels.json").read_text()) if only else {}
    panels, rows = {a: p for a, p in old.items() if a not in only}, []
    for asin, rel in WRAPS.items():
        if only and asin not in only:
            continue
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
    for n in range(0, len(rows), 10):
        page = rows[n:n + 10]
        sheet = Image.new("RGB", (max(r.width for r in page), sum(r.height + 12 for r in page)), "white")
        y = 0
        for r in page:
            sheet.paste(r, (0, y))
            y += r.height + 12
        sheet.save("panels_check.jpg" if n == 0 else f"panels_check_{n // 10 + 1}.jpg", quality=80)
    print(f"{len(panels)} titles. Now LOOK at panels_check*.jpg.")


if __name__ == "__main__":
    main()
