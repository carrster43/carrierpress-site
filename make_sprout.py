#!/usr/bin/env python3
"""Sprout, the weekly magazine. Issues in sprout_issues/NNN.md -> /sprout/.

    python3 make_sprout.py          # lint, then build
    python3 make_sprout.py --lint   # lint only, writes nothing

One issue a week, one markdown file each, named by number (001.md). Front matter:

    no: 1                    the issue number, must match the file name
    date: 2026-11-20         the Friday it goes out
    cover: <headline>        the cover line, also the page title
    summary: <one sentence>  index card, meta description, feed item
    draft: true|false        drafts never render

The same file is the body of that week's MailerLite campaign, so the page and
the email cannot say different things.

Writes /sprout/index.html (latest issue up top, then the back issues),
/sprout/<no>/index.html for each issue, and /sprout/feed.xml. Regenerates from
scratch each run, so flipping an issue back to draft takes its page down.
Every page goes through nav.patch(), so the nav, holiday ribbon and footer
match the rest of the site without a second copy here.
"""
import datetime, glob, html, json, os, re, shutil, sys

import blog
import nav
import sprout_data as D
from _md import render as md_render, front_matter

e = blog.e


def _head(*a, **k):
    """blog's head plus Sprout's own stylesheet. sprout/sprout.css is hand kept and
    separate from styles.css so the magazine's look never collides with site edits."""
    return blog._head(*a, **k).replace(
        '<link rel="stylesheet" href="/styles.css">',
        '<link rel="stylesheet" href="/styles.css">\n'
        f'<link rel="stylesheet" href="/{D.PATH}/sprout.css">'
        f'\n<link rel="alternate" type="application/rss+xml" title="{e(D.NAME)}" '
        f'href="/{D.PATH}/feed.xml">', 1)


def lint(path, meta, body):
    """Every house rule a published issue must pass. Returns a list of problems."""
    probs = []
    text = "\n".join(str(v) for v in meta.values()) + "\n" + body
    for pat, why in D.BANNED:
        for m in re.finditer(pat, text, re.I):
            line = text.count("\n", 0, m.start()) + 1
            probs.append(f"{path}: {why} (matched {m.group(0)!r}, around line {line})")
    if re.search(r"\bAI\b", body):
        probs.append(f"{path}: the AI note is added by the builder as the last line; "
                     "leave it out of the issue body")
    return probs


def _load():
    issues, problems = [], []
    for f in sorted(glob.glob("sprout_issues/*.md")):
        meta, body = front_matter(open(f, encoding="utf-8").read())
        if str(meta.get("draft", "")).lower() == "true":
            continue
        for req in ("no", "date", "cover", "summary"):
            if not meta.get(req):
                raise SystemExit(f"SPROUT STOPPED: {f} is missing front matter '{req}'")
        no = int(meta["no"])
        if int(os.path.basename(f)[:-3]) != no:
            raise SystemExit(f"SPROUT STOPPED: {f} says no: {no}; file name and number must agree")
        try:
            d = datetime.date.fromisoformat(meta["date"])
        except ValueError:
            raise SystemExit(f"SPROUT STOPPED: {f} date {meta['date']!r} is not YYYY-MM-DD")
        problems += lint(f, meta, body)
        # _md reads one line per bullet. Issues wrap bullets onto indented
        # continuation lines for readability, so fold those back first.
        body = re.sub(r"\n[ \t]+(?=\S)", " ", body)
        issues.append(dict(no=no, date=d, cover=meta["cover"], summary=meta["summary"],
                           html=md_render(body)))
    nos = [i["no"] for i in issues]
    if len(nos) != len(set(nos)):
        raise SystemExit("SPROUT STOPPED: two issues share a number")
    issues.sort(key=lambda i: i["no"], reverse=True)
    return issues, problems


def form_html():
    """The MailerLite signup form, shared by /sprout/ and the homepage card
    (build.py sprout_band_html). Empty while ML_FORM is None. Posts by fetch so
    the reader stays on the page; on any failure it falls back to a plain post."""
    if not D.ML_FORM:
        return ""
    action = f"https://assets.mailerlite.com/jsonp/{D.ML_ACCOUNT}/forms/{D.ML_FORM}/subscribe"
    return (f'<form class="sp-form" action="{e(action)}" method="post">'
            '<label class="sp-label" for="sp-email">Your email</label>'
            '<div class="sp-row"><input id="sp-email" type="email" name="fields[email]" '
            'required autocomplete="email" placeholder="you@example.com">'
            '<input type="hidden" name="ml-submit" value="1">'
            f'<button class="btn btn-ink" type="submit">Subscribe</button></div>'
            '<p class="sp-fine">One email a week, on Fridays. The list is kept by MailerLite, '
            'the mailing service Carrier Press uses. It holds your email, nothing else. '
            'Every issue has an unsubscribe link.</p>'
            '<p class="sp-done" hidden>Almost done. Check your inbox for a confirmation email from Jeffrey L. Carrier and click the link inside. If it is not there, look in Promotions or Spam.</p></form>'
            '<script>document.querySelectorAll(".sp-form").forEach(function(f){'
            'f.addEventListener("submit",function(ev){ev.preventDefault();'
            'fetch(f.action,{method:"POST",body:new FormData(f)}).then(function(r){return r.json();})'
            '.then(function(j){if(j&&j.success){f.querySelector(".sp-row").hidden=true;'
            'f.querySelector(".sp-done").hidden=false;}else{f.submit();}})'
            '.catch(function(){f.submit();});});});</script>')


def pitch():
    """The one-line promise, shared by /sprout/ and the homepage card."""
    return (f'<strong>Get {e(D.NAME)} {e(D.CADENCE[:1].lower() + D.CADENCE[1:])}.</strong> '
            'New books, new apps, and what is on the bench, in a five minute read.')


def _subscribe():
    feed = f"/{D.PATH}/feed.xml"
    return ('<aside class="post-signup sp-sub" id="subscribe">'
            f'<p>{pitch()}</p>'
            + form_html() +
            f'<p class="sp-rss">Prefer a feed reader? <a href="{feed}">Follow by RSS</a>.</p>'
            '</aside>')


def _issue_block(i, h="h1"):
    return (f'<p class="eyebrow">{e(D.NAME)} No. {i["no"]} &middot; '
            f'{i["date"].strftime("%d %B %Y").lstrip("0")}</p>'
            f'<{h} class="sp-cover">{e(i["cover"])}</{h}>'
            f'<div class="post-body sp-body">{i["html"]}</div>')


def _ai():
    return f'<p class="sp-ai">{e(D.AI_NOTE)}</p>'


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)
    nav.patch(path)


def build(S, issues):
    root = D.PATH
    keep = {str(i["no"]) for i in issues}
    if os.path.isdir(root):
        for name in os.listdir(root):
            full = os.path.join(root, name)
            if os.path.isdir(full) and name.isdigit() and name not in keep:
                shutil.rmtree(full)
    base = f"https://{S['domain']}/{root}/"

    for n, i in enumerate(issues):
        canon = f"{base}{i['no']}/"
        newer = issues[n - 1] if n > 0 else None
        older = issues[n + 1] if n + 1 < len(issues) else None
        pager = '<p class="post-back sp-pager">'
        if older:
            pager += f'<a href="/{root}/{older["no"]}/">No. {older["no"]}</a> &middot; '
        pager += f'<a href="/{root}/">All issues</a>'
        if newer:
            pager += f' &middot; <a href="/{root}/{newer["no"]}/">No. {newer["no"]}</a>'
        pager += "</p>"
        ld = {"@context": "https://schema.org", "@type": "Article",
              "headline": i["cover"], "description": i["summary"],
              "datePublished": i["date"].isoformat(), "url": canon,
              "isPartOf": {"@type": "Periodical", "name": D.NAME, "url": base},
              "author": {"@type": "Person", "name": S["author"]},
              "publisher": {"@type": "Organization", "name": S["title"],
                            "url": f"https://{S['domain']}/"}}
        _write(f"{root}/{i['no']}/index.html",
               _head(S, f"{D.NAME} No. {i['no']}: {i['cover']}", i["summary"], canon,
                          "article", ld)
               + '<article class="post sprout"><div class="wrap wrap-narrow">'
               + _issue_block(i) + _subscribe() + pager + _ai()
               + "</div></article>" + blog._foot(S))

    if issues:
        latest, back = issues[0], issues[1:]
        lead = ('<div class="sp-latest">' + _issue_block(latest, "h2")
                + f'<p class="post-back"><a href="/{root}/{latest["no"]}/">'
                  f'Link to this issue</a></p></div>')
        backs = "".join(
            f'<article class="post-item"><p class="eyebrow">No. {b["no"]} &middot; '
            f'{b["date"].strftime("%d %B %Y").lstrip("0")}</p>'
            f'<h2><a href="/{root}/{b["no"]}/">{e(b["cover"])}</a></h2>'
            f'<p>{e(b["summary"])}</p></article>' for b in back)
        backs = ('<h2 class="sp-back-head">Back issues</h2>' + backs) if backs else ""
    else:
        lead, backs = "<p>The first issue is being written.</p>", ""
    _write(f"{root}/index.html",
           _head(S, D.NAME, D.TAGLINE, base, "website",
                      {"@context": "https://schema.org", "@type": "Periodical",
                       "name": D.NAME, "description": D.TAGLINE, "url": base,
                       "publisher": {"@type": "Organization", "name": S["title"]}})
           + '<section class="sprout"><div class="wrap wrap-narrow"><div class="sec-head">'
             f'<p class="eyebrow">{e(D.CADENCE)}</p><h1 class="sp-mast">{e(D.NAME)}</h1>'
             f'<p>{e(D.TAGLINE)}</p></div>'
           + _subscribe() + lead + backs + _ai() + "</div></section>" + blog._foot(S))

    rss = "".join(
        f"<item><title>{e(D.NAME)} No. {i['no']}: {e(i['cover'])}</title>"
        f"<link>{base}{i['no']}/</link>"
        f'<guid isPermaLink="true">{base}{i["no"]}/</guid>'
        f"<pubDate>{datetime.datetime.combine(i['date'], datetime.time(12)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>"
        f"<description>{e(i['summary'])}</description></item>" for i in issues)
    open(f"{root}/feed.xml", "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        f"<title>{e(D.NAME)}</title><link>{base}</link>"
        f'<atom:link href="{base}feed.xml" rel="self" type="application/rss+xml"/>'
        f"<description>{e(D.TAGLINE)}</description><language>en-us</language>"
        f"{rss}</channel></rss>\n")
    return len(issues)


if __name__ == "__main__":
    S = json.load(open("catalog.json", encoding="utf-8"))["site"]
    issues, problems = _load()
    if problems:
        print("SPROUT LINT FAILED:\n  " + "\n  ".join(problems))
        sys.exit(1)
    print(f"lint: {len(issues)} issue(s) pass the house rules")
    if "--lint" in sys.argv:
        sys.exit(0)
    n = build(S, issues)
    print(f"sprout: {n} issue(s) -> /{D.PATH}/, feed at /{D.PATH}/feed.xml; "
          f"email signup {'ON, form ' + D.ML_FORM if D.ML_FORM else 'OFF (ML_FORM is None), RSS only'}")
