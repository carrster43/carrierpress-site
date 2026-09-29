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

DESIGNED SETS WIN. When <repo>/docs/screenshots-v2/ holds <slug>_new_<n>.png,
those replace the raw capture for that app. Icons and the hero colour for each
landing page come from <repo>/assets/icon.png into apps/icons/.

    python3 make_app_shots.py boatready nightwatch   # only these apps' shots

The folder name maps to the slug by lowercasing it (BoatReady -> boatready). A
folder with no matching row in apps_data.py is reported and skipped, never
guessed at.
"""
import json, pathlib, shutil, subprocess, sys

import apps_data

SRC = pathlib.Path.home() / "Projects/carrier-ventures/scripts/shots/ready"
OUT = pathlib.Path("apps/shots")
ICONS = pathlib.Path("apps/icons")
PROJECTS = pathlib.Path.home() / "Projects"
SIZES = (("-sm", 360), ("", 780))


def webp(src, dst, width):
    subprocess.run(["cwebp", "-quiet", "-q", "80", "-resize", str(width), "0",
                    str(src), "-o", str(dst)], check=True)


def repo_for(slug):
    """~/Projects/<Repo> for a slug, matched by lowercasing (BoatReady -> boatready)."""
    for d in PROJECTS.iterdir():
        if d.is_dir() and d.name.lower() == slug:
            return d
    return None


def v2_shots(slug):
    """
    The designed store screenshots (answer first, icon-colour ground, caption),
    when an app has them: <repo>/docs/screenshots-v2/<slug>_new_<n>.png. They
    win over the raw capture, because they are what the App Store will show and
    the landing page should show the same thing.
    """
    repo = repo_for(slug)
    if not repo:
        return []
    return sorted((repo / "docs/screenshots-v2").glob("%s_new_*.png" % slug))


def icon_path(repo):
    """assets/icon.png, or one level down (Cast lives in player/, Downpour in mobile/)."""
    for p in [repo / "assets/icon.png"] + sorted(repo.glob("*/assets/icon.png")):
        if p.is_file() and "_original" not in str(p):
            return p
    return None


def contrast_on_white(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(x) for x in rgb)
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return 1.05 / (lum + 0.05)


# Apps whose icon ground is near-black, so the sampled accent is a plain dark band
# while their screenshots carry a colour. These take the screenshot colour instead,
# already checked to clear 7:1 against white text.
ACCENT_OVERRIDES = {
    "cast": "#6E5316",      # deep gold, from the Cast screenshot ground
    "downpour": "#22557F",  # deep blue, from the Downpour screenshot ground
}


def accent_from(icon):
    """
    The icon's colour: its most common opaque pixel that is not near-white. Darkened until white
    text on it clears 7:1, because the landing page hero sets white body copy on
    this colour and a pale icon would otherwise make it unreadable.
    """
    from PIL import Image
    im = Image.open(icon).convert("RGBA").resize((64, 64))
    counts = {}
    for r, g, b, a in im.getdata():
        # Skip near-white: most icons are a coloured mark on a white ground,
        # and the ground is the one colour that says nothing about the app.
        if a > 200 and min(r, g, b) < 225:
            counts[(r, g, b)] = counts.get((r, g, b), 0) + 1
    if not counts:
        return None
    rgb = max(counts, key=counts.get)
    while contrast_on_white(rgb) < 7:
        rgb = tuple(int(c * 0.9) for c in rgb)
    return "#%02X%02X%02X" % rgb


def icons(slugs):
    """apps/icons/<slug>.webp at 256px, and accents.json, for every app with a repo."""
    ICONS.mkdir(parents=True, exist_ok=True)
    accents, missing = {}, []
    for slug in sorted(slugs):
        repo = repo_for(slug)
        icon = icon_path(repo) if repo else None
        if not icon:
            missing.append(slug)
            continue
        webp(icon, ICONS / ("%s.webp" % slug), 256)
        accent = ACCENT_OVERRIDES.get(slug) or accent_from(icon)
        if accent:
            accents[slug] = accent
    (ICONS / "accents.json").write_text(json.dumps(accents, indent=1, sort_keys=True) + "\n")
    print("wrote %s  --  %d icons" % (ICONS, len(accents)))
    if missing:
        print("no icon found, page falls back to the site colours: %s" % ", ".join(missing))


def main(only=None):
    if not SRC.is_dir():
        sys.exit("no capture output at %s" % SRC)
    slugs = {a["slug"] for a in apps_data.APPS if a.get("slug")}
    icons(slugs)
    done, skipped = 0, []
    for folder in sorted(p for p in SRC.iterdir() if p.is_dir()):
        slug = folder.name.lower()
        if slug not in slugs:
            skipped.append(folder.name)
            continue
        if only and slug not in only:
            continue
        pngs = v2_shots(slug) or sorted(folder.glob("*.png"))
        if not pngs:
            continue
        dest = OUT / slug
        # Rebuilt whole, so a screenshot dropped from the rail drops off the site.
        shutil.rmtree(dest, ignore_errors=True)
        dest.mkdir(parents=True)
        for png in pngs:
            for suffix, width in SIZES:
                webp(png, dest / ("%s%s.webp" % (png.stem.replace(slug + "_new_", "store-"), suffix)), width)
        done += 1
    print("wrote %s  --  %d apps" % (OUT, done))
    if skipped:
        print("skipped, no row in apps_data.py: %s" % ", ".join(skipped))


if __name__ == "__main__":
    # Optional slugs: rebuild only those apps' screenshots. Icons always rebuild.
    main(set(sys.argv[1:]) or None)
