#!/usr/bin/env python3
"""
The members' podcast list (author 2026-11-06: episodes unlock with Carrier Press
Access, Books and All Access tiers). Run after new episodes are downloaded:

    python3 make_member_episodes.py

Reads the NotebookLM queue, converts each finished episode to 64 kbps AAC in the
gate's bundles (never in this public repo), and writes podcast_members.json,
which listen.py reads. The queue lives outside this repo, so CI builds from the
committed JSON and never runs this file.

An episode is a discussion, never a reading. See listen.py.
"""
import csv, json, pathlib, re, subprocess

import books
import listen

PODCASTS = pathlib.Path.home() / "Documents/SALES_PUSH/PODCASTS"
BUNDLE = pathlib.Path.home() / "Projects/AppGate/bundles/podcast/app"
OUT = pathlib.Path("podcast_members.json")
GROUPS = {"novel", "kids", "money", "classic"}
# Titles sold as entirely the author's own writing, pitched to libraries that
# screen for AI. No AI-hosted episode on their pages without his word.
NO_AI_HOLD = {"stealing-first-base", "who-wants-to-be-greek-english-narrative-edition"}


def runtime(path):
    info = subprocess.run(["afinfo", str(path)], capture_output=True, text=True, check=True).stdout
    secs = int(float(re.search(r"estimated duration: ([\d.]+)", info).group(1)))
    return "%d:%02d" % (secs // 60, secs % 60)


def main():
    rows = list(csv.DictReader(open(PODCASTS / "PODCAST_QUEUE.tsv", newline=""), delimiter="\t"))
    catalog = json.loads(pathlib.Path("catalog.json").read_text())
    by_slug = {slug: b for b, _sec, slug in books.records(catalog)}
    free = {ep["asin"] for ep in listen.EPISODES} | {s["asin"] for s in listen.SOON}
    BUNDLE.mkdir(parents=True, exist_ok=True)
    episodes, coming, left_out = [], [], []
    for r in rows:
        b = by_slug.get(r["slug"])
        if not b or b["a"] in free or b.get("soon"):
            continue
        if "PRIVATE" in r["flag"] or r["slug"] in NO_AI_HOLD:
            left_out.append(r["slug"])
        elif r["status"] == "downloaded":
            src = PODCASTS / r["file"]
            dst = BUNDLE / (r["slug"] + ".m4a")
            if not dst.exists():
                subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", str(src), str(dst)], check=True)
            episodes.append(dict(slug=r["slug"], asin=b["a"], book=b["t"], runtime=runtime(dst),
                                 title="A conversation about " + b["t"]))
        elif r["status"] in ("todo", "generating", "queued") and r["group"] in GROUPS:
            coming.append(dict(asin=b["a"], book=b["t"]))
    OUT.write_text(json.dumps(dict(episodes=episodes, coming=coming), indent=1) + "\n")
    print("members: %d episodes, %d coming; left out: %s" % (len(episodes), len(coming), ", ".join(left_out) or "none"))


if __name__ == "__main__":
    main()
