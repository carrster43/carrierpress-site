#!/usr/bin/env python3
"""Re-verify every rating in catalog.json against the live Amazon listings.

Usage:  python3 refresh_ratings.py [--write]

Without --write it only reports. With --write it updates catalog.json, then run
build.py. Ratings on a static site go stale silently, and a stale rating is a
claim you cannot stand behind, so re-run this before any push that touches them.

WHY THE PARSING IS STRICT: a naive "([0-9.]+) out of 5 stars" regex matches page
furniture on listings that have NO reviews at all. A first pass of this sweep
reported a phantom 5.0 for eleven titles that have no ratings whatsoever. A star
value is therefore only accepted when a rating COUNT is present too, and only
from the product's own review block.
"""
import json, re, html, sys, time, urllib.request, collections, datetime

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def fetch(asin):
    req = urllib.request.Request(f"https://www.amazon.com/dp/{asin}",
        headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

def read(t):
    stars = None
    m = re.search(r'id="acrPopover"[^>]*title="([\d.]+) out of 5 stars"', t)
    if m: stars = m.group(1)
    if not stars:
        m = re.search(r'data-hook="rating-out-of-text"[^>]*>\s*([\d.]+) out of 5', t)
        if m: stars = m.group(1)
    flat = " ".join(html.unescape(re.sub(r'<[^>]+>', ' ', t)).split())
    m = re.search(r'([\d,]+)\s+(?:global\s+)?ratings?\b', flat)
    count = m.group(1) if m else None
    return (stars, count) if (stars and count) else (None, None)

def main():
    write = "--write" in sys.argv
    d = json.load(open("catalog.json"), object_pairs_hook=collections.OrderedDict)
    books = [b for s in d["sections"] for b in s["books"]]
    today = datetime.date.today().isoformat()
    changed = gone = 0
    for b in books:
        if not b.get("rating"):
            continue
        try:
            st, ct = read(fetch(b["a"]))
        except Exception as ex:
            print(f"  {b['a']}  FETCH FAILED ({ex}), left untouched"); continue
        was = (b["rating"].get("stars"), b["rating"].get("count"))
        if not st:
            print(f"  {b['a']}  RATING GONE from the listing, was {was[0]} on {was[1]}. "
                  f"REMOVE IT rather than shipping a claim that is no longer true.")
            gone += 1
        elif (st, ct) != was:
            print(f"  {b['a']}  {was[0]} on {was[1]}  ->  {st} on {ct}")
            if write:
                b["rating"]["stars"], b["rating"]["count"] = st, ct
                b["rating"]["checked"] = today
            changed += 1
        else:
            print(f"  {b['a']}  unchanged, {st} on {ct}")
            if write: b["rating"]["checked"] = today
        time.sleep(1.5)
    if write:
        open("catalog.json", "w").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        print("catalog.json updated. Now run: python3 build.py")
    print(f"\n{changed} changed, {gone} disappeared. "
          f"{'WROTE' if write else 'Report only, pass --write to apply.'}")
    return 1 if gone else 0

if __name__ == "__main__":
    sys.exit(main())
