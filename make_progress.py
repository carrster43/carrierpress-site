#!/usr/bin/env python3
"""
/progress/ and /support/, generated.

    python3 make_progress.py

/progress/  every book, app and project with its state, what the work earns,
            how it is funded and how it is growing. Data: progress_data.json
            (public: this repo is served, so it carries no IDs or sources).
            The money figures are in FIGURES below, each with its date.
/support/   membership, one time support, Ethereum, early access.
            Rails: support_data.py. An empty url is no button.
/reviews/   the grassroots review campaign: why, how, and a Write a review
            link for every book in catalog.json. Support sits on its own,
            never tied to a review (Amazon forbids any reward for one).

House rules that bind this page: no em or en dashes, never "best seller",
never "donate", never present an illustration as a forecast, never ask for a
particular star rating and never connect support or any reward to a review.
"""
import html, json, pathlib

import nav
import support_data as SD

e = html.escape
ROOT = pathlib.Path(__file__).parent
D = json.loads((ROOT / "progress_data.json").read_text(encoding="utf-8"))
AS_OF = "October 5, 2026"

# Documented figures, each with its date. Update by hand from the dashboards.
FIGURES = dict(
    kdp_sep_units=26, kdp_sep_print=22, kdp_sep_royalty=124.33, kdp_sep_date="September 1 to 28, 2026",
    ingram_30d_units=33, ingram_date="30 days to September 22, 2026",
    kdp_payout=21.42, kdp_payout_note="paid September 29 for July sales",
    titles_aug=78, print_units_jul=13,
    streams=3846, streams_date="12 months to July 27, 2026",
)

STATUS_ORDER = [
    ("in App Review", "With Apple for review", "Submitted and waiting for Apple's decision."),
    ("TestFlight", "In beta", "Running on test phones, final checks before submission."),
    ("built", "Built", "The app works; store listing and launch work remain."),
    ("in development", "In development", "Core features are being built."),
    ("planned", "Planned", "Specified on paper, not yet started."),
]
STAGE = {"planned": "Planned", "drafting": "Drafting", "revising": "Revising",
         "production": "In production", "awaiting proof": "Awaiting proof",
         "submitted": "Submitted to stores"}
LINES = [("fiction", "Fiction and literary suspense"), ("young readers", "Young readers"),
         ("classics", "Restored classics"), ("true crime", "True crime"), ("comics", "Comics")]


def money(x):
    return "${:,.2f}".format(x) if x < 100 else "${:,.0f}".format(x)


# ---------------------------------------------------------------- chrome ----
CSS = """
.pg{padding:48px 0 72px}
.pg h1{font-family:var(--serif);font-size:clamp(2rem,4vw,2.8rem);margin:0 0 12px;color:var(--ink)}
.pg h2{font-family:var(--serif);font-size:1.6rem;margin:56px 0 8px;color:var(--ink)}
.pg h3{font-family:var(--sans);font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:30px 0 10px}
.pg p{line-height:1.65;max-width:70ch;color:var(--ink-soft);margin:0 0 14px}
.pg .lede{font-size:1.12rem;color:var(--ink)}
.asof{font-family:var(--sans);font-size:13px;color:var(--muted)}
.jump{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0;font-family:var(--sans);font-size:14px}
.jump a{border:1px solid var(--line);border-radius:999px;padding:6px 14px;color:var(--ink);text-decoration:none;background:var(--card)}
.jump a:hover{border-color:var(--gold)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:30px 0 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:16px 18px}
.stat b{display:block;font-family:var(--serif);font-size:2rem;color:var(--ink);line-height:1.1}
.stat span{font-family:var(--sans);font-size:13px;color:var(--muted)}
.rows{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}
.rows li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;padding:14px 2px;border-bottom:1px solid var(--line)}
.rows .t{font-weight:600;color:var(--ink)}
.rows .d{grid-column:1/-1;font-size:.95rem;color:var(--ink-soft);line-height:1.5}
.rows .m{grid-column:1/-1;font-family:var(--sans);font-size:12.5px;color:var(--muted)}
.chip{font-family:var(--sans);font-size:12px;white-space:nowrap;border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--ink-soft);align-self:start}
.chip.go{border-color:var(--gold);color:var(--ink)}
table.n{border-collapse:collapse;width:100%;margin:8px 0 6px;font-size:.96rem}
table.n th,table.n td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink-soft)}
table.n th{font-family:var(--sans);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600}
table.n td.r,table.n th.r{text-align:right;white-space:nowrap}
.tw{overflow-x:auto}
.note{background:var(--paper-2);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:4px;padding:16px 20px;margin:18px 0}
.note p{margin:0 0 8px}.note p:last-child{margin:0}
details{border-bottom:1px solid var(--line);padding:10px 0}
summary{cursor:pointer;font-weight:600;color:var(--ink)}
details ul{columns:2 260px;padding-left:18px;margin:12px 0 4px;color:var(--ink-soft);line-height:1.6}
.tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:20px 0 0}
.tier{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:22px;display:flex;flex-direction:column}
.tier h3{margin:0 0 6px;color:var(--ink);font-size:.85rem}
.tier .pr{font-family:var(--serif);font-size:2rem;color:var(--ink)}
.tier .pr small{font-size:1rem;color:var(--muted)}
.tier ul{padding-left:18px;margin:14px 0 18px;line-height:1.55;color:var(--ink-soft);flex:1}
.btns{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;font-family:var(--sans);font-size:14px;font-weight:600;padding:10px 16px;border-radius:6px;text-decoration:none;border:1px solid var(--gold);color:var(--ink);background:transparent;cursor:pointer}
.btn.p{background:var(--gold);color:#151a33}
.btn:hover{background:var(--gold-bright);color:#151a33}
.soon{font-family:var(--sans);font-size:13px;color:var(--muted)}
.eth code{display:block;word-break:break-all;background:var(--paper-2);border:1px solid var(--line);border-radius:4px;padding:10px 12px;margin:10px 0;font-size:.92rem;color:var(--ink)}
@media (max-width:560px){.rows li{grid-template-columns:minmax(0,1fr)}.chip{justify-self:start;white-space:normal}}
.rows li>*{min-width:0}.chip{max-width:22em}
.books{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}
.books li{display:grid;grid-template-columns:48px minmax(0,1fr);gap:4px 14px;padding:12px 2px;border-bottom:1px solid var(--line);align-items:center}
.books img{width:48px;height:auto;border-radius:2px;grid-row:span 2;box-shadow:0 1px 3px rgba(0,0,0,.25)}
.books .t{font-weight:600;color:var(--ink);line-height:1.3}
.books .t small{display:block;font-weight:400;font-family:var(--sans);font-size:12.5px;color:var(--muted)}
.books .btns{gap:8px}.books .btn{font-size:13px;padding:7px 12px}
.steps{counter-reset:s;list-style:none;padding:0;margin:18px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.steps li{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:16px 18px 16px 52px;position:relative;color:var(--ink-soft);line-height:1.5}
.steps li:before{counter-increment:s;content:counter(s);position:absolute;left:16px;top:14px;font-family:var(--serif);font-size:1.6rem;color:var(--gold)}
.steps b{color:var(--ink)}
#q{width:100%;max-width:420px;font:inherit;font-family:var(--sans);font-size:15px;padding:10px 12px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink);margin:6px 0 14px}
.shelf-h{font-family:var(--sans);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:26px 0 6px}
"""


def page(path, title, desc, body):
    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Carrier Press</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="https://carrierpress.com/{path}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="https://carrierpress.com/{path}/">
<meta property="og:image" content="https://carrierpress.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>{CSS}</style>
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
      <a href="/labs/">Labs</a>
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
  </div>
</header>

<main id="main" class="pg">
<div class="wrap">
{body}
</div>
</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; 2026 Jeffrey L. Carrier. All rights reserved.</span>
      <span><a href="/">Carrier Press</a> is an imprint of Jeffrey L. Carrier.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""
    out = ROOT / path / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(head, encoding="utf-8")
    nav.patch(out)
    return out


def rows(items):
    return '<ul class="rows">\n' + "\n".join(items) + "\n</ul>"


def row(t, chip, d="", m="", go=False):
    return (f'<li><span class="t">{t}</span><span class="chip{" go" if go else ""}">{e(chip)}</span>'
            + (f'<span class="d">{e(d)}</span>' if d else "")
            + (f'<span class="m">{e(m)}</span>' if m else "") + "</li>")


# -------------------------------------------------------------- progress ----
def progress():
    F = FIGURES
    pub, wip, apps, proj = D["published"], D["in_progress"], D["apps"], D["projects"]
    books_live = sum(1 for p in pub if p["line"] != "comics")
    by = {}
    for a in apps:
        by.setdefault(a["status"], []).append(a)
    in_review = len(by.get("in App Review", []))
    music = [p for p in proj if p["kind"] == "music" and p["name"] != "Velouryx"]

    b = [f"""<h1>Progress</h1>
<p class="asof">Updated {AS_OF}</p>
<p class="lede">Carrier Press is one person making books, apps and music. This page is the whole
ledger in public: what is finished, what is still being built, what the work earns, and how it is paid for.</p>
<nav class="jump" aria-label="On this page">
<a href="#books">Books</a><a href="#apps">Apps</a><a href="#projects">Other projects</a>
<a href="#income">Income</a><a href="#growth">Growth</a><a href="#funding">Funding</a><a href="/support/">Support the press</a>
</nav>
<div class="stats">
<div class="stat"><b>{books_live}</b><span>books in print and ebook</span></div>
<div class="stat"><b>{len(wip)}</b><span>book projects in progress</span></div>
<div class="stat"><b>{len(apps)}</b><span>apps, built or in the works</span></div>
<div class="stat"><b>{in_review}</b><span>apps with Apple for review</span></div>
<div class="stat"><b>{len(music)}</b><span>music artists, 4 albums out</span></div>
</div>"""]

    # Books
    b.append('<h2 id="books">Books</h2>')
    b.append(f"<p>{books_live} titles are on sale now, in Kindle, paperback and, for most, hardcover. "
             "These are the ones still being made.</p>")
    b.append("<h3>In progress</h3>")
    b.append(rows(row(e(w["title"]), STAGE.get(w["stage"], w["stage"].title()), w["next"],
                      " · ".join(x for x in (w.get("series", ""), ("Target: " + w["target"]) if w.get("target") else "") if x),
                      go=w["stage"] == "submitted") for w in wip))
    b.append("<h3>Finished and on sale</h3>")
    for key, label in LINES:
        ts = sorted(p["title"] for p in pub if p["line"] == key)
        if ts:
            b.append(f"<details><summary>{e(label)} ({len(ts)})</summary><ul>"
                     + "".join(f"<li>{e(t)}</li>" for t in ts) + "</ul></details>")
    b.append('<p style="margin-top:14px"><a href="/">Browse every book with covers and store links</a></p>')

    # Apps
    b.append('<h2 id="apps">Apps</h2>')
    b.append("<p>Small single purpose apps under the Carrier Ventures name. None has launched yet, "
             "so none has earned anything yet. Prices are the ones each app will charge. "
             'Boat Ready already runs on the web at <a href="/boatready/app/">carrierpress.com/boatready/app/</a>.</p>')
    for st, label, blurb in STATUS_ORDER:
        group = by.get(st, [])
        if not group:
            continue
        b.append(f"<h3>{e(label)} ({len(group)})</h3><p>{e(blurb)}</p>")
        b.append(rows(row(e(a["name"]), a["price"] or "Price not set", a["what"], "Next: " + a["next"],
                          go=st in ("in App Review", "TestFlight")) for a in group))

    # Projects
    b.append('<h2 id="projects">Other projects</h2>')
    b.append(rows(row(e(p["name"]), p["status"].capitalize(), p["note"], p["kind"].capitalize(),
                      go=p["status"] == "live") for p in proj))

    # Income
    avg = F["kdp_sep_royalty"] / F["kdp_sep_units"]
    one_time = sorted({a["price"].split()[0] for a in apps if a["status"] in ("in App Review",) and "once" in a["price"]})
    b.append('<h2 id="income">Income</h2>')
    b.append("<h3>What has actually come in</h3>")
    b.append(f"""<div class="tw"><table class="n"><thead><tr><th>Source</th><th>Period</th><th class="r">Figure</th></tr></thead><tbody>
<tr><td>Amazon KDP book sales</td><td>{F['kdp_sep_date']}</td><td class="r">{F['kdp_sep_units']} copies, about ${F['kdp_sep_royalty']:,.2f} in royalties</td></tr>
<tr><td>Bookstore distribution (IngramSpark) print sales</td><td>{F['ingram_date']}</td><td class="r">{F['ingram_30d_units']} copies</td></tr>
<tr><td>Most recent KDP royalty payment</td><td>{F['kdp_payout_note']}</td><td class="r">{money(F['kdp_payout'])}</td></tr>
<tr><td>Apps</td><td>to date</td><td class="r">$0, none launched yet</td></tr>
<tr><td>Music streams on Spotify</td><td>{F['streams_date']}</td><td class="r">{F['streams']:,} streams</td></tr>
</tbody></table></div>
<p>Royalties are paid about two months after the sale, and bookstore distribution about three, so money arrives well behind the sales above.</p>""")
    b.append("<h3>What the work could earn</h3>")
    b.append(f"""<div class="note"><p><strong>These are illustrations, not forecasts.</strong> Each row is the
real price of one sale, after the store's cut, multiplied by a round number of sales so the scale is easy to see.
Nothing here predicts that those numbers will happen.</p></div>
<div class="tw"><table class="n"><thead><tr><th>Product</th><th class="r">Earned per sale</th><th class="r">At 100 a month</th><th class="r">At 1,000 a month</th></tr></thead><tbody>
<tr><td>A book, at September's actual average royalty</td><td class="r">{money(avg)}</td><td class="r">{money(avg*100)}</td><td class="r">{money(avg*1000)}</td></tr>
<tr><td>A $6.99 one time app (after Apple's 15% small developer rate)</td><td class="r">{money(6.99*.85)}</td><td class="r">{money(6.99*.85*100)}</td><td class="r">{money(6.99*.85*1000)}</td></tr>
<tr><td>A $5.99 a month app subscriber (same rate)</td><td class="r">{money(5.99*.85)}</td><td class="r">{money(5.99*.85*100)}</td><td class="r">{money(5.99*.85*1000)}</td></tr>
<tr><td>A First Reader member at $8 a month (after a ~10% + 50&cent; fee)</td><td class="r">{money(8*.9-.5)}</td><td class="r">{money((8*.9-.5)*100)}</td><td class="r">{money((8*.9-.5)*1000)}</td></tr>
</tbody></table></div>
<p>The apps waiting on Apple sell for {", ".join(one_time)} once, or by subscription for Home Rule.
Most apps keep a useful part free, and you pay only to unlock the rest.</p>""")

    # Growth
    b.append('<h2 id="growth">Growth</h2>')
    b.append(rows([
        row("Catalogue", f"{F['titles_aug']} to {books_live} titles",
            "Books on sale when this site opened on August 29, against today."),
        row("Print sales pace", f"~{F['print_units_jul']} to ~{F['kdp_sep_print'] + F['ingram_30d_units']} a month",
            f"About {F['print_units_jul']} print copies a month in July. In September, {F['kdp_sep_print']} print copies on Amazon (plus {F['kdp_sep_units'] - F['kdp_sep_print']} ebooks) and {F['ingram_30d_units']} through bookstore distribution.",
            go=True),
        row("Hardcovers", "First sales in September",
            "The first five hardcover sales came in September, all The King in Yellow."),
        row("Apps", f"{in_review} with Apple",
            f"{in_review} apps are in Apple's review queue and two more are in beta. None had launched as of {AS_OF}.", go=True),
        row("Music", "4 albums",
            "Two artists on the Velouryx label, each with two albums out, the latest in September."),
    ]))

    # Funding
    b.append('<h2 id="funding">Funding</h2>')
    b.append("""<p>Carrier Press is funded by its readers and listeners, and by nobody else. There are no investors,
no grants, no publisher advances and no ads in any app. Every cost is paid from book sales and from people who
choose to support the work directly.</p>
<h3>What support pays for</h3>
<ul class="rows">
<li><span class="t">Getting apps into the App Store</span><span class="d">Apple's developer membership and the build service that turns code into an app.</span></li>
<li><span class="t">Getting books onto shelves</span><span class="d">ISBNs, printed proofs, and bookstore distribution fees for every format.</span></li>
<li><span class="t">Getting books read</span><span class="d">Advance reader copies, reviews outreach and audiobook editions.</span></li>
<li><span class="t">Time</span><span class="d">Every month of support is time spent finishing the in progress list above instead of working around it.</span></li>
</ul>
<p style="margin-top:22px"><a class="btn p" href="/support/">Become a member or support the press</a></p>""")

    return page("progress", "Progress",
                "Every Carrier Press book, app and project with its current state, what the work earns, and how it is funded.",
                "\n".join(b))


# --------------------------------------------------------------- support ----
def btn(label, url, primary=False):
    return f'<a class="btn{" p" if primary else ""}" href="{e(url)}" target="_blank" rel="noopener">{e(label)}</a>' if url else ""


def support():
    b = ["""<h1>Support the press</h1>
<p class="lede">Carrier Press is one person. Buying a book is the best support there is, and a review is the
next best. If you want to back the work directly, here is every way to do it, and what you get.</p>
<p class="asof">Support is a payment to a small for profit press, not a charitable gift, and is not tax deductible.</p>
<nav class="jump" aria-label="On this page"><a href="#membership">Membership</a><a href="#early">Early access</a>
<a href="#once">One time</a><a href="#crypto">Ethereum</a><a href="/progress/">See the progress</a></nav>"""]

    b.append('<h2 id="membership">Membership</h2>')
    b.append("<p>A monthly membership, cancel any time. Join through whichever service you already use.</p>")
    b.append('<div class="tiers">')
    for t in SD.TIERS:
        bt = btn("Join on Gumroad", t["gumroad"], True) + btn("Join on Patreon", t["patreon"])
        b.append(f'<div class="tier"><h3>{e(t["name"])}</h3><div class="pr">{e(t["price"])} <small>a {e(t["per"])}</small></div>'
                 f'<ul>{"".join("<li>%s</li>" % e(p) for p in t["perks"])}</ul>'
                 f'<div class="btns">{bt or chr(60) + "span class=soon>Opening soon</span>"}</div></div>')
    b.append("</div>")

    b.append('<h2 id="early">Early access</h2>')
    b.append("""<ul class="rows">
<li><span class="t">Books before release</span><span class="chip go">First Reader and up</span><span class="d">Opening chapters while a book is still being written, and the finished ebook the week it comes out.</span></li>
<li><span class="t">Apps before the App Store</span><span class="chip go">First Reader and up</span><span class="d">Beta invitations to new apps while they are still being tested, starting with the ones listed as in beta on the progress page.</span></li>
<li><span class="t">Boat Ready on the web, now</span><span class="chip">$9.99 once</span><span class="d">The full Boat Ready app already runs in your browser while the phone version waits on Apple.</span></li>
<li><span class="t">The free reader list</span><span class="chip">Free</span><span class="d">The first five chapters of The Sponge Cache, and a note when each new book is out.</span></li>
</ul>
<div class="btns" style="margin-top:16px"><a class="btn" href="/apps/boatready/">Boat Ready on the web</a><a class="btn" href="/#free">Get the free chapters</a></div>""")

    b.append('<h2 id="once">One time support</h2>')
    b.append(rows(f'<li><span class="t">{e(l)}</span><span class="chip">{e(n)}</span>'
                  f'<span class="d">{btn("Support with " + l if l in ("PayPal", "Venmo") else l, u, True)}</span></li>'
                  for l, u, n in SD.ONE_TIME if u))

    b.append('<h2 id="crypto">Ethereum</h2>')
    b.append(f"""<div class="eth"><p>Send ETH or an ERC-20 token on <strong>Ethereum mainnet only</strong>. Tokens sent on
any other network, including layer 2 networks, cannot be recovered.</p>
<code id="eth">{SD.ETH_ADDRESS}</code>
<div class="btns"><a class="btn p" href="{e(SD.METAMASK_URL)}" target="_blank" rel="noopener">Send with MetaMask</a>
<button class="btn" type="button" onclick="navigator.clipboard&amp;&amp;navigator.clipboard.writeText(document.getElementById('eth').textContent).then(()=>{{this.textContent='Copied'}})">Copy address</button>
{btn("Pay with Spritz Finance", SD.SPRITZ_URL)}</div>
<p class="asof" style="margin-top:12px">Always check the address in your wallet matches the one above before you send.</p></div>""")

    return page("support", "Support the press",
                "Membership, early access to books and apps, and every way to support Carrier Press directly.",
                "\n".join(b))


# --------------------------------------------------------------- reviews ----
# Amazon's own review composer, the same link every book card on the homepage uses.
REVIEW = "https://www.amazon.com/review/create-review?asin={}"
AMZ = "https://www.amazon.com/dp/{}"
SHARE = ("I just left an honest review for a Carrier Press book. Small presses live on reviews, "
         "and one or two sentences is enough. Every title, with a one tap review link: "
         "https://carrierpress.com/reviews/")


def reviews():
    from urllib.parse import quote
    cat = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    seen, shelves, n = set(), [], 0
    for sec in cat["sections"]:
        items = []
        for bk in sec.get("books", []):
            a = bk["a"]
            if a in seen:
                continue
            seen.add(a)
            sub = f'Book {bk["n"]}, {sec["name"]}' if bk.get("n") else (bk.get("by") or "")
            items.append(
                f'<li data-q="{e((bk["t"] + " " + sec["name"] + " " + bk.get("by", "")).lower())}">'
                f'<img src="/assets/covers/{a}.jpg" alt="" loading="lazy" decoding="async" width="48" height="77">'
                f'<span class="t">{e(bk["t"])}' + (f'<small>{e(sub)}</small>' if sub else "") + '</span>'
                f'<span class="btns"><a class="btn p" href="{REVIEW.format(a)}" target="_blank" rel="noopener">Write a review</a>'
                f'<a class="btn" href="{AMZ.format(a)}" target="_blank" rel="noopener">See it on Amazon</a></span></li>')
        if items:
            n += len(items)
            shelves.append(f'<section data-shelf><h3 class="shelf-h">{e(sec["name"])}</h3>'
                           f'<ul class="books">\n' + "\n".join(items) + '\n</ul></section>')

    mail = "mailto:?subject=" + quote("A small press that runs on reviews") + "&body=" + quote(SHARE)
    b = [f"""<h1>One honest review</h1>
<p class="lede">Carrier Press is one person and {n} books. No publicity department, no ad budget worth the
name. What moves a small press on Amazon is readers saying, in their own words, what they thought.
This is a grassroots campaign: if you have read one of these books, leave one honest review. Two
sentences is plenty.</p>
<nav class="jump" aria-label="On this page"><a href="#why">Why it matters</a><a href="#how">How</a>
<a href="#books">Every book</a><a href="#share">Pass it on</a><a href="#support">Support the press</a></nav>

<h2 id="why">Why one review matters</h2>
<p>Amazon decides which books to show, in search and under "customers also bought", partly on how
many readers have reviewed them. Most of these titles have none yet. A first review does more for a
book than its hundredth ever will, and a reader deciding whether to try an unknown author reads
reviews before anything else.</p>

<h2 id="how">How to take part</h2>
<ol class="steps">
<li><b>Pick a book you have read.</b> Find it below, or search by title.</li>
<li><b>Tap Write a review.</b> Amazon opens its own review form for that book, already signed in.</li>
<li><b>Say what you honestly thought.</b> Any rating, any length. What worked, what did not, who it is for.</li>
<li><b>Pass it on.</b> Send this page to one reader who might do the same.</li>
</ol>
<div class="note">
<p><strong>The ground rules.</strong> Every honest review is welcome, whatever the rating. We never
pay for, reward, or trade anything for a review, and nothing on this site is unlocked by leaving one.</p>
<p>Amazon only accepts reviews from accounts with a recent purchase, and its rules ask the author's
family and close friends not to review. If that is you, sharing this page helps just as much.</p>
</div>

<h2 id="books">Every book</h2>
<label class="asof" for="q">Find a title</label>
<input id="q" type="search" placeholder="Type a title, series or author" autocomplete="off">
<div id="shelves">
{chr(10).join(shelves)}
</div>
<p id="none" class="asof" hidden>No title matches that search.</p>

<h2 id="share">Pass it on</h2>
<p>Grassroots means reader to reader. Copy the message below into a text, an email or a book club
chat, or use the buttons.</p>
<div class="note"><p id="msg">{e(SHARE)}</p></div>
<div class="btns">
<button class="btn p" type="button" id="cp">Copy the message</button>
<button class="btn" type="button" id="sh" hidden>Share</button>
<a class="btn" href="{e(mail)}">Send by email</a>
</div>

<h2 id="support">Support the press</h2>
<p>Separately from reviews, and never in exchange for one: readers who want to back the work
directly can do so. It pays for covers, ISBNs and print proofs. Support is a payment to a small
for profit press, not a charitable gift, and is not tax deductible.</p>
<div class="btns">
<a class="btn p" href="/support/">Every way to support</a>
{"".join(btn(l if l not in ("PayPal", "Venmo") else "Support with " + l, u) for l, u, _ in SD.ONE_TIME if u)}
</div>

<script>(function(){{
var q=document.getElementById('q'),none=document.getElementById('none');
q.addEventListener('input',function(){{var v=q.value.trim().toLowerCase(),any=false;
document.querySelectorAll('[data-shelf]').forEach(function(s){{var hit=false;
s.querySelectorAll('li').forEach(function(li){{var ok=!v||li.dataset.q.indexOf(v)>-1;li.hidden=!ok;if(ok)hit=true}});
s.hidden=!hit;if(hit)any=true}});none.hidden=any}});
var m=document.getElementById('msg').textContent,cp=document.getElementById('cp'),sh=document.getElementById('sh');
cp.addEventListener('click',function(){{navigator.clipboard&&navigator.clipboard.writeText(m).then(function(){{cp.textContent='Copied'}})}});
if(navigator.share){{sh.hidden=false;sh.addEventListener('click',function(){{navigator.share({{text:m}}).catch(function(){{}})}})}}
}})();</script>"""]
    return page("reviews", "One honest review",
                f"A grassroots campaign for Carrier Press: leave one honest Amazon review for a book you have read. A one tap review link for all {n} books.",
                "\n".join(b))


if __name__ == "__main__":
    for p in (progress(), support(), reviews()):
        print("wrote", p.relative_to(ROOT))
