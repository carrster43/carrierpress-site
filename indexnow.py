#!/usr/bin/env python3
"""
Tell Bing (and every engine that shares IndexNow: Yandex, Seznam, Naver) which
carrierpress.com pages are new or changed, the same day, instead of waiting
for a crawl. Bing's index also feeds DuckDuckGo, Yahoo and Copilot.

    python3 indexnow.py --diff <old-sha> <new-sha>   # what .github/workflows/indexnow.yml runs
    python3 indexnow.py https://carrierpress.com/guides/ ...   # named URLs, by hand
    python3 indexnow.py --dry-run --diff HEAD~1 HEAD           # print, send nothing

--diff compares sitemap_state.json between two commits (build.py keeps a
content hash per page there) and sends every sitemap page whose hash is new or
different. Not the sitemap's <lastmod>: that is a date, so a page changed
twice in one day keeps the same lastmod and its second change would be missed
(found on the first run, 2026-11-27: the 11 book pages that gained a guide
link had already been rebuilt that morning).

THE KEY. 26beacee0781c8f753ebaa28770da918.txt at the site root (added
2026-11-20) proves the site owns the key. It is public by design, which is why
it can sit in a public repo. Never delete or rename that file without changing
KEY here in the same commit.

No dependencies; the standard library only, so the workflow needs no install.
"""
import json, re, subprocess, sys, urllib.request

HOST = "carrierpress.com"
KEY = "26beacee0781c8f753ebaa28770da918"
ENDPOINT = "https://api.indexnow.org/indexnow"
URL_RE = re.compile(r"<url><loc>([^<]+)</loc><lastmod>([^<]+)</lastmod></url>")


def _sitemap_at(rev):
    try:
        out = subprocess.run(["git", "show", "%s:sitemap.xml" % rev], capture_output=True,
                             text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return {}            # the old commit may predate the file, or be all zeros on a new branch
    return dict(URL_RE.findall(out))


def _state_at(rev):
    try:
        out = subprocess.run(["git", "show", "%s:sitemap_state.json" % rev], capture_output=True,
                             text=True, check=True).stdout
        return {k: v.get("sha256") for k, v in json.loads(out).items()}
    except (subprocess.CalledProcessError, ValueError):
        return {}


def changed(old, new):
    live = _sitemap_at(new)                         # only pages the new sitemap lists
    a, b = _state_at(old), _state_at(new)
    urls = {"https://%s%s" % (HOST, path) for path, h in b.items() if a.get(path) != h}
    # The journal's dates come from the posts, not the hash file: keep the lastmod test for them.
    old_map = _sitemap_at(old)
    urls |= {u for u, d in live.items() if "/blog/" in u and old_map.get(u) != d}
    return sorted(u for u in urls if u in live)


def send(urls, dry=False):
    urls = [u for u in urls if u.startswith("https://%s/" % HOST)]
    if not urls:
        print("indexnow: nothing to send")
        return
    for i in range(0, len(urls), 10000):            # the protocol's per-request cap
        batch = urls[i:i + 10000]
        body = {"host": HOST, "key": KEY, "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
                "urlList": batch}
        if dry:
            print("indexnow (dry run): would send %d url(s)" % len(batch))
            print("\n".join(batch))
            continue
        req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print("indexnow: sent %d url(s), HTTP %d" % (len(batch), r.status))
        except urllib.error.HTTPError as e:
            # 200 and 202 are success. 422 means a URL is not on this host or the
            # key file does not match; 429 means slow down. Fail loudly either way.
            raise SystemExit("indexnow: HTTP %d %s" % (e.code, e.read().decode(errors="replace")[:300]))


if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    if args[:1] == ["--diff"] and len(args) == 3:
        send(changed(args[1], args[2]), dry)
    elif args:
        send(args, dry)
    else:
        raise SystemExit(__doc__)
