#!/usr/bin/env python3
"""
Copy the App Store screenshots onto the site, sized for a web page.

    python3 make_app_shots.py        # then python3 make_apps.py

WHERE THEY COME FROM. carrier-ventures/scripts/shots/ready/<App>/*.png is the
capture rail's output: 1290x2796 PNGs at Apple's iPhone 6.9" size, about 500KB
each. Those are the files that go to App Store Connect and they are not touched
here. A card on /apps/ shows them about 120px wide, so shipping the originals
would put 25MB on one page.

WHAT THIS WRITES. apps/shots/<slug>/<name>-sm.webp (360px wide, the card strip)
and <name>.webp (780px wide, what the thumbnail opens). The site repo carries
the output, not the source, so make_apps.py builds on any machine and never
reaches into another repo.

The folder name maps to the slug by lowercasing it (BoatReady -> boatready). A
folder with no matching row in apps_data.py is reported and skipped, never
guessed at.
"""
import pathlib, shutil, subprocess, sys

import apps_data

SRC = pathlib.Path.home() / "Projects/carrier-ventures/scripts/shots/ready"
OUT = pathlib.Path("apps/shots")
SIZES = (("-sm", 360), ("", 780))


def webp(src, dst, width):
    subprocess.run(["cwebp", "-quiet", "-q", "80", "-resize", str(width), "0",
                    str(src), "-o", str(dst)], check=True)


def main():
    if not SRC.is_dir():
        sys.exit("no capture output at %s" % SRC)
    slugs = {a["slug"] for a in apps_data.APPS if a.get("slug")}
    done, skipped = 0, []
    for folder in sorted(p for p in SRC.iterdir() if p.is_dir()):
        slug = folder.name.lower()
        if slug not in slugs:
            skipped.append(folder.name)
            continue
        pngs = sorted(folder.glob("*.png"))
        if not pngs:
            continue
        dest = OUT / slug
        # Rebuilt whole, so a screenshot dropped from the rail drops off the site.
        shutil.rmtree(dest, ignore_errors=True)
        dest.mkdir(parents=True)
        for png in pngs:
            for suffix, width in SIZES:
                webp(png, dest / ("%s%s.webp" % (png.stem, suffix)), width)
        done += 1
    print("wrote %s  --  %d apps" % (OUT, done))
    if skipped:
        print("skipped, no row in apps_data.py: %s" % ", ".join(skipped))


if __name__ == "__main__":
    main()
