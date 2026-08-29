"""Monthly journal generator.

Posts are markdown files in posts/. One post a month is meant to serve two
destinations: a page here, and the body of that month's MailerLite send, so the
blog feeds the reader list rather than competing with it. Every post page
therefore carries the signup block.

Drafts never render. Missing or malformed front matter stops the build rather
than shipping a broken page.
"""
import os, re, glob, datetime, html
from _md import render as md_render, front_matter

def e(x): return html.escape(str(x), quote=True)

def _head(S, title, desc, canon):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Carrier Press</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canon)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(canon)}">
<meta property="og:image" content="https://{S['domain']}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<link rel="alternate" type="application/rss+xml" title="Carrier Press journal" href="/feed.xml">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="/">
      <img class="mark-dark" src="/assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="/assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>Carrier Press</span>
    </a>
    <nav class="nav" aria-label="Main">
      <a href="/#fiction">Fiction</a>
      <a href="/#classics">Classics</a>
      <a href="/blog/">Journal</a>
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
  </div>
</header>
<main id="main">
"""

def _foot(S):
    return f"""</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; {datetime.date.today().year} {e(S['author'])}. All rights reserved.</span>
      <span><a href="/">Carrier Press</a> is an imprint of {e(S['author'])}.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

def _signup(S):
    return ('<aside class="post-signup">'
            '<p><strong>One post a month, nothing else.</strong> The same piece goes to the '
            'reader list, along with the free opening chapters of <em>The Sponge Cache</em>.</p>'
            f'<p><a class="btn btn-ink" href="{e(S["magnet_url"])}" target="_blank" '
            'rel="noopener">Send me the free chapters</a></p></aside>')

def _load():
    posts = []
    for f in sorted(glob.glob("posts/*.md"), reverse=True):
        meta, body = front_matter(open(f, encoding="utf-8").read())
        if str(meta.get("draft", "")).lower() == "true":
            continue
        for req in ("title", "date", "summary"):
            if not meta.get(req):
                raise SystemExit(f"BUILD STOPPED: {f} is missing front matter '{req}'")
        try:
            d = datetime.date.fromisoformat(meta["date"])
        except ValueError:
            raise SystemExit(f"BUILD STOPPED: {f} date {meta['date']!r} is not YYYY-MM-DD")
        slug = meta.get("slug") or re.sub(r"[^a-z0-9]+", "-",
                    os.path.basename(f)[:-3].lower()).strip("-")
        posts.append(dict(title=meta["title"], summary=meta["summary"], date=d,
                          slug=slug, html=md_render(body)))
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

def build(S):
    posts = _load()
    os.makedirs("blog", exist_ok=True)
    # Regenerate from scratch. Without this, flipping a post back to draft would
    # leave its page on disk and it would stay live, which makes "draft" a lie.
    keep = {f"{p['slug']}.html" for p in posts} | {"index.html"}
    for stale in os.listdir("blog"):
        if stale.endswith(".html") and stale not in keep:
            os.remove(os.path.join("blog", stale))

    for p in posts:
        canon = f"https://{S['domain']}/blog/{p['slug']}.html"
        open(f"blog/{p['slug']}.html", "w", encoding="utf-8").write(
            _head(S, p["title"], p["summary"], canon)
            + '<article class="post"><div class="wrap wrap-narrow">'
            + f'<p class="eyebrow">{p["date"].strftime("%d %B %Y")}</p>'
            + f'<h1>{e(p["title"])}</h1>'
            + f'<div class="post-body">{p["html"]}</div>'
            + _signup(S)
            + '<p class="post-back"><a href="/blog/">All posts</a></p>'
            + '</div></article>' + _foot(S))

    items = "".join(
        f'<article class="post-item">'
        f'<p class="eyebrow">{p["date"].strftime("%d %B %Y")}</p>'
        f'<h2><a href="/blog/{p["slug"]}.html">{e(p["title"])}</a></h2>'
        f'<p>{e(p["summary"])}</p></article>' for p in posts)
    if not items:
        items = '<p>The first post is being written.</p>'
    open("blog/index.html", "w", encoding="utf-8").write(
        _head(S, "Journal", "Notes from Carrier Press, once a month.",
              f"https://{S['domain']}/blog/")
        + '<section><div class="wrap wrap-narrow"><div class="sec-head">'
          '<p class="eyebrow">Once a month</p><h1>Journal</h1>'
          '<p>What is being written, what has just shipped, and what the research turned up.</p>'
          '</div>' + items + _signup(S) + '</div></section>' + _foot(S))

    rss = "".join(
        f"<item><title>{e(p['title'])}</title>"
        f"<link>https://{S['domain']}/blog/{p['slug']}.html</link>"
        f'<guid isPermaLink="true">https://{S["domain"]}/blog/{p["slug"]}.html</guid>'
        f"<pubDate>{datetime.datetime.combine(p['date'], datetime.time(12)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>"
        f"<description>{e(p['summary'])}</description></item>" for p in posts)
    open("feed.xml", "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        f'<title>Carrier Press journal</title><link>https://{S["domain"]}/blog/</link>'
        # rel="self" is what a validator and most readers use to confirm the feed's
        # own canonical address. Its absence is the commonest RSS validation warning.
        f'<atom:link href="https://{S["domain"]}/feed.xml" rel="self" type="application/rss+xml"/>'
        '<description>Notes from Carrier Press, once a month.</description>'
        f'<language>en-us</language>{rss}</channel></rss>\n')
    return len(posts)
