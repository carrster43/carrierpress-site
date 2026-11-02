#!/usr/bin/env python3
"""Build formats.json: every catalog title's formats, Amazon prices, ISBN-13s and
page counts, read from its live Amazon product page. books.py shows them on each
/books/<slug>/ page with the date they were read.

Amazon will not serve its product pages to curl, so the read happens in a browser
tab already open on amazon.com:

  1. python3 make_formats.py --asins      prints the catalog ASINs as a JS array
  2. In the amazon.com tab's console, set `ASINS = <that array>` and paste JS below.
     It reads each title's page and its paperback and hardcover pages, one request
     at a time, and leaves the raw result in `window.__res` (a JSON object).
  3. Save `JSON.stringify(window.__res)` to formats_raw.json, then run
     python3 make_formats.py "November 1, 2026"     (the date the pages were read)

Read only. Nothing here clicks, buys or signs in.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent

# Print editions Amazon shows on one of our pages that belong to another publisher
# (a merged record). Never list them as ours. The Enchanted April Kindle B0H7PZ3FDM
# is merged with B08RXL6LH1; these are that publisher's paperback and hardcover.
NOT_OURS = {"B0HFRZSNX3", "1761835599"}

JS = r"""
const ex = doc => {
  const fm = {};
  doc.querySelectorAll('[id^=tmm-grid-swatch-]').forEach(el => {
    const t = el.innerText.replace(/\s+/g,' ').trim();
    const name = (t.match(/^(Kindle|Paperback|Hardcover|Audiobook|Audible)/i)||[])[1];
    const a = el.querySelector('a[href*="/dp/"],a[href*="/gp/product/"]');
    const asin = a ? ((a.getAttribute('href').match(/\/(?:dp|product)\/([A-Z0-9]{10})/)||[])[1]) : null;
    if (name) fm[name] = {price:(t.match(/\$[\d,.]+/)||[])[0]||null, asin};
  });
  const det = {};
  doc.querySelectorAll('#detailBullets_feature_div li').forEach(li => {
    const m = li.innerText.replace(/[‎‏]/g,'').replace(/\s+/g,' ').trim()
               .match(/^(ISBN-13|Print length|Publication date)\s*:\s*(.+)$/);
    if (m) det[m[1]] = m[2];
  });
  doc.querySelectorAll('[id^=rpi-attribute-book_details-]').forEach(el => {
    const k = el.querySelector('.rpi-attribute-label')?.innerText.replace(/\s+/g,' ').trim();
    const v = el.querySelector('.rpi-attribute-value')?.innerText.replace(/\s+/g,' ').trim();
    if (k && v) det[k] = v;
  });
  return {title:(doc.querySelector('#productTitle')||{}).textContent?.trim(), fm, det};
};
const get = async a => new DOMParser().parseFromString(
  await (await fetch('/dp/'+a, {credentials:'include'})).text(), 'text/html');
window.__res = {};
(async () => { for (const a of ASINS) { try {
  const x = ex(await get(a));
  for (const f of ['Paperback','Hardcover']) if (x.fm[f]?.asin) x[f+'_det'] = ex(await get(x.fm[f].asin)).det;
  window.__res[a] = x; } catch (e) { window.__res[a] = {err:String(e)}; } } window.__done = true; })();
"""


def asins():
    cat = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    out = []
    for s in cat["sections"]:
        for b in s["books"]:
            if b["a"] not in out:
                out.append(b["a"])
    return out


def pages(s):
    m = re.search(r"(\d[\d,]*)\s*pages", s or "")
    return int(m.group(1).replace(",", "")) if m else None


def normalize(raw, asof):
    books = {}
    for a, x in raw.items():
        if x.get("err") or not x.get("fm"):
            continue
        fmts = []
        for name, f in x["fm"].items():
            if not f.get("price") or f.get("asin") in NOT_OURS:
                continue
            det = x.get(name + "_det") or {}
            fmts.append({k: v for k, v in dict(
                f=name, price=f["price"], asin=f.get("asin") or a,
                isbn=det.get("ISBN-13"), pages=pages(det.get("Print length"))).items() if v})
        pd = (x.get("Paperback_det") or {}).get("Publication date") or (x.get("det") or {}).get("Publication date")
        books[a] = {k: v for k, v in dict(formats=fmts, pub=pd).items() if v}
    return {"asof": asof, "books": books}


if __name__ == "__main__":
    if sys.argv[1:] == ["--asins"]:
        print(json.dumps(asins()))
    elif sys.argv[1:] == ["--js"]:
        print(JS)
    elif len(sys.argv) == 2:
        raw = json.loads((ROOT / "formats_raw.json").read_text(encoding="utf-8"))
        data = normalize(raw, sys.argv[1])
        (ROOT / "formats.json").write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        missing = [a for a in asins() if a not in data["books"]]
        print("formats.json: %d titles, %d missing %s" % (len(data["books"]), len(missing), missing))
    else:
        sys.exit(__doc__)
