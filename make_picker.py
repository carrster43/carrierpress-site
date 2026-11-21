#!/usr/bin/env python3
"""
/pick/: "Find your next book", two tap-to-answer questions and three picks
(author 2026-11-18: "yes, build it", goal "to purchase for a satisfied customer").

    python3 make_picker.py    # build.py runs it too, before the sitemap

THE GOAL IS A SATISFIED BUYER, NOT A CLICK. So the page:
  * asks who the book is for first, because a parent, a gift giver and a reader
    buying for themselves need different signals;
  * leads every lane with ONE "start here" book (a series' Book 1, or the lane's
    steadiest seller), then offers two alternatives, never a wall of covers;
  * says on each pick the thing that prevents a disappointed buyer: the age
    range on young readers' books, the real event behind each American Firsts
    novel, the author of each classic;
  * opens print first (promote-print rule) and, for a gift, the hardcover when
    one exists, via formats.json.

EVERY WORD ABOUT A BOOK COMES FROM ITS OWN RECORD (catalog.json): the editorial
"why" line the Start Here and King in Yellow bands already use, else the
shelf hook, else the first paragraph of the Amazon description. Nothing about a
book is written here. A lane that points at a missing or coming-soon title fails
the build rather than shipping a dead end.

TO CHANGE THE PICKS, edit LANES below. Each lane needs exactly three ASINs; the
first is the "start here" book.
"""
import datetime, html, json, pathlib, re

import books
import nav

DOMAIN = "carrierpress.com"

# Question 1. "gift" swaps the buy button to the hardcover where one exists.
WHO = [
    ("me", "Me", "adult", False),
    ("young", "A young reader", "young", False),
    ("gift-adult", "A gift for a grown-up", "adult", True),
    ("gift-young", "A gift for a young reader", "young", True),
]

# Question 2, by audience. (key, button label, one-line promise, [start, alt, alt], lane note)
LANES = {
    "adult": [
        ("mystery", "A mystery to solve",
         "Clues, suspects and a fair solution.",
         ["B0GZCKYKZ9", "B0H7NMYT5J", "B0HMZKCTTS"], None),
        ("suspense", "Literary suspense",
         "Family secrets, old records and a slow reveal.",
         ["B0H6CWP5GN", "B0H59MBV8R", "B0H6VGK2MZ"], None),
        ("truecrime", "Real crime, told as a novel",
         "Novels built on real American crimes.",
         ["B0HHJK9GMT", "B0HHJSF9SP", "B0HMK4LL3B"],
         "Each one is built on a real crime with real victims. Written for adult readers."),
        ("horror", "Weird, ghostly and cosmic",
         "Where cosmic horror and the English ghost story began.",
         ["B0H7W7VY7S", "B0HH3CJRRW", "B0HGG934BB"], None),
        ("classic", "A great old novel",
         "Restored, annotated classics: romance, crime and adventure.",
         ["B0H7QFWVXG", "B0H7LYK2QQ", "B0H7PDS3QM"], None),
        ("ideas", "Big ideas and true history",
         "Strange science, a real bank fraud and a gold panic.",
         ["B0GX34KKKQ", "B0H7WM2CHN", "B07XF4J8SR"], None),
        ("money", "Money and income",
         "Personal finance guides for adult readers.",
         ["B0GX2YNHT9", "B0H4DR314J", "B0GX38GVW3"], None),
    ],
    "young": [
        ("y-mystery", "A mystery with puzzles",
         "The Atherton Manor Mysteries: seven children and a house full of puzzles.",
         ["B0H483NLCV", "B0HN3HJJBR", "B0HNGNHF35"],
         "A series: start with Book 1."),
        ("y-build", "Game worlds and building",
         "Two adventure series set in worlds you build.",
         ["B0GXP2C498", "B0H6FH7TB7", "B0H59B9QFV"], None),
        ("y-money", "Money skills and making things",
         "Stories that teach earning, saving and starting something.",
         ["B0GYBT12DP", "B0H46C5QFS", "B0H4DQ6488"], None),
    ],
}

# MailerLite: one group and one embedded form per lane (author 2026-11-18, "Yes,
# set them up"). Groups are named "Picker: <lane label>"; forms "Picker: <lane
# label> (carrierpress.com/pick)". Double opt-in ON on every form. Each signup
# also carries the custom field `picker` = "<who>/<lane>" (e.g. gift-adult/horror),
# so a list can be cut by gift vs self as well as by lane.
ML_ACCOUNT = "2504319"
# ON 2026-11-18 once a test signup's confirmation email was SEEN arriving (sent
# 04:08:19Z, 1 sent / 0 bounced in the form's report). The forms have no builder
# design ("Form design is missing") and do not need one: this page posts to them
# directly, and each form carries MailerLite's default confirmation email.
# 🔑 That email comes FROM jeffrey@carrierpress.com, so Gmail files a test copy
# under SENT as well as INBOX; search it by subject "Confirmation email".
# Set False to hide the signup box without touching anything else.
SIGNUP_LIVE = True
FORMS = {
    "mystery": "204536266544383324",
    "suspense": "204536624892085806",
    "truecrime": "204536626880186165",
    "horror": "204536628398523497",
    "classic": "204536630314272090",
    "ideas": "204536632239458124",
    "money": "204536634261112042",
    "y-mystery": "204536637479192523",
    "y-build": "204536639464146065",
    "y-money": "204536644863263957",
}

SHELF = {"adult": "/catalog/", "young": "/young-readers/"}
MAGNET_LANES = {"horror"}   # the free King in Yellow sample fits these lanes only


def e(x):
    return html.escape(str(x), quote=True)


def _first_para(desc, limit=230):
    if isinstance(desc, str):
        desc = [desc]
    text = next((p for p in (desc or []) if str(p).strip()), "")
    text = re.sub(r"\s+", " ", str(text)).strip()
    # Some descriptions arrive with paragraphs glued ("a system.Most advice").
    text = re.sub(r"([a-z][.!?])([A-Z])", r"\1 \2", text)
    if len(text) <= limit:
        return text
    cut = text[:limit]
    end = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    return cut[:end + 1] if end > 60 else cut.rsplit(" ", 1)[0] + "..."


def _whys(D):
    """Editorial lines already approved for the home and catalogue bands."""
    out = {}
    for x in (D.get("featured") or {}).get("books", []):
        out.setdefault(x["a"], x["why"])
    for x in (D.get("bestseller") or {}).get("connected", []):
        out.setdefault(x["a"], x["why"])
    return out


def _ages(b, sec):
    m = re.search(r"ages? (\d+ to \d+)", b.get("note") or "")
    return m.group(1) if m else sec.get("ages")


def _edition(asin, gift):
    fmts = {f["f"]: f for f in (books.FORMATS["books"].get(asin) or {}).get("formats", [])}
    if gift and fmts.get("Hardcover", {}).get("asin"):
        f = fmts["Hardcover"]
        return "Hardcover", f["asin"], None
    return books.print_edition(asin)


def data(D):
    recs = {b["a"]: (b, sec, slug) for b, sec, slug in books.records(D)}
    whys = _whys(D)

    def pick(asin):
        if asin not in recs or recs[asin][0].get("soon"):
            raise SystemExit(f"make_picker: {asin} is not a buyable catalogue title")
        b, sec, slug = recs[asin]
        facts = []
        ages = _ages(b, sec)
        if ages:
            facts.append(f"Ages {ages}")
        if b.get("n") and sec.get("kind") != "standalone" and not b.get("omnibus"):
            facts.append(f'{sec["name"]}, Book {b["n"]}')
        elif "Book " in (b.get("note") or ""):
            facts.append(b["note"].split(". For young")[0])
        elif b.get("note") and not ages:
            facts.append(b["note"])
        if b.get("by"):
            facts.insert(0, f'By {b["by"]}')
        out = {"a": asin, "t": books.display_title(b, sec), "url": f"/books/{slug}/",
               "why": whys.get(asin) or b.get("hook") or _first_para(b.get("desc")),
               "facts": facts}
        for key, gift in (("buy", False), ("gift", True)):
            fmt, a, price = _edition(asin, gift)
            if not fmt:   # promote-print rule: a pick must open a print edition
                raise SystemExit(f"make_picker: {asin} has no paperback or hardcover in formats.json")
            out[key] = {"f": fmt or "Amazon", "a": a, "p": price}
        return out

    lanes = {}
    for aud, rows in LANES.items():
        lanes[aud] = []
        for key, label, line, asins, note in rows:
            if len(asins) != 3:
                raise SystemExit(f"make_picker: lane {key} needs exactly 3 books, has {len(asins)}")
            if key not in FORMS:
                raise SystemExit(f"make_picker: lane {key} has no MailerLite form in FORMS")
            lanes[aud].append({"k": key, "label": label, "line": line, "note": note,
                               "magnet": key in MAGNET_LANES,
                               "form": (f"https://assets.mailerlite.com/jsonp/{ML_ACCOUNT}/forms/{FORMS[key]}/subscribe"
                                        if SIGNUP_LIVE else None),
                               "picks": [pick(a) for a in asins]})
    return {"who": [{"k": k, "label": l, "aud": a, "gift": g} for k, l, a, g in WHO],
            "lanes": lanes, "shelf": SHELF, "amz": books.AMZ}


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Find your next book | Carrier Press</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{domain}/pick/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="Find your next book">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://{domain}/pick/">
<meta property="og:image" content="https://{domain}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>
.pk{{padding-top:44px;padding-bottom:64px}}
.pk h1{{font-size:clamp(1.8rem,6vw,2.6rem);font-weight:400;letter-spacing:-.02em;margin:0 0 12px}}
.pk .lede{{font-size:1.08rem;line-height:1.6;color:var(--ink-soft);max-width:60ch;margin:0 0 26px}}
.pk-step{{border-top:1px solid var(--line);padding:26px 0 8px}}
.pk-step h2{{font-size:clamp(1.3rem,4vw,1.6rem);font-weight:400;margin:0 0 16px;outline:none}}
.pk-step .n{{font-family:var(--sans);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--gold);display:block;margin-bottom:6px}}
.pk-opts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin:0;padding:0;list-style:none}}
.pk-opts button{{width:100%;text-align:left;cursor:pointer;font:inherit;color:var(--ink);background:var(--paper-2);
  border:1px solid var(--line);border-radius:8px;padding:14px 16px;line-height:1.35}}
.pk-opts button strong{{display:block;font-family:var(--sans);font-size:15px;font-weight:600}}
.pk-opts button span{{display:block;font-size:14px;color:var(--muted);margin-top:4px}}
.pk-opts button:hover,.pk-opts button:focus-visible{{border-color:var(--gold)}}
.pk-opts button[aria-pressed="true"]{{border-color:var(--gold);box-shadow:inset 3px 0 0 var(--gold)}}
.pk-note{{font-family:var(--sans);font-size:14px;color:var(--ink-soft);border-left:3px solid var(--gold);padding:4px 0 4px 12px;margin:0 0 18px}}
.pk-lead{{display:grid;grid-template-columns:150px 1fr;gap:22px;align-items:start;margin:0 0 28px}}
.pk-lead img{{width:100%;height:auto;aspect-ratio:2/3;object-fit:cover;border-radius:4px;box-shadow:var(--shadow)}}
.pk-tag{{font-family:var(--sans);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--gold);margin:0 0 6px}}
.pk-lead h3{{font-size:1.45rem;font-weight:400;margin:0 0 6px}}
.pk-lead h3 a,.pk-alt h4 a{{color:var(--ink);text-decoration:none}}
.pk-lead h3 a:hover,.pk-alt h4 a:hover{{text-decoration:underline;text-decoration-color:var(--gold)}}
.pk-facts{{font-family:var(--sans);font-size:13px;color:var(--muted);margin:0 0 10px}}
.pk-why{{line-height:1.6;margin:0 0 14px;max-width:60ch}}
.pk-fit{{font-family:var(--sans);font-size:13px;color:var(--ink-soft);margin:0 0 14px}}
.pk-act{{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;margin:0}}
.pk-act .go{{display:inline-block;background:var(--gold);color:#151a33;font-family:var(--sans);font-weight:600;
  text-decoration:none;padding:11px 18px;border-radius:6px}}
.pk-act .more{{font-family:var(--sans);font-size:14px;color:var(--ink)}}
.pk-alts-h{{font-family:var(--sans);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin:0 0 12px}}
.pk-alts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px;margin:0 0 26px;padding:0;list-style:none}}
.pk-alt{{display:grid;grid-template-columns:76px 1fr;gap:14px;align-items:start}}
.pk-alt img{{width:100%;height:auto;aspect-ratio:2/3;object-fit:cover;border-radius:3px;box-shadow:var(--shadow)}}
.pk-alt h4{{font-size:1.05rem;font-weight:400;margin:0 0 4px}}
.pk-alt .pk-why{{font-size:14px;margin:0 0 8px}}
.pk-alt .go{{padding:8px 13px;font-size:14px}}
.pk-end{{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;font-family:var(--sans);font-size:14px;margin:22px 0 0}}
.pk-end button{{font:inherit;background:none;border:1px solid var(--line);border-radius:999px;padding:9px 14px;color:var(--ink);cursor:pointer}}
.pk-end button:hover,.pk-end button:focus-visible{{border-color:var(--gold)}}
.pk-box{{margin:30px 0 0;padding:20px;border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:6px;background:var(--paper-2)}}
.pk-box p{{margin:0 0 10px;line-height:1.6}}
.pk-box p:last-child{{margin:0}}
.pk-sub .pk-lbl{{display:block;font-family:var(--sans);font-size:13px;color:var(--ink-soft);margin:4px 0 6px}}
.pk-row{{display:flex;flex-wrap:wrap;gap:10px}}
.pk-row input[type=email]{{flex:1 1 220px;min-width:0;font:inherit;font-size:16px;padding:10px 12px;border:1px solid var(--line);
  border-radius:6px;background:var(--paper);color:var(--ink)}}
.pk-row button{{flex:0 0 auto;font-family:var(--sans);font-weight:600;font-size:15px;background:var(--gold);color:#151a33;
  border:0;border-radius:6px;padding:11px 18px;cursor:pointer}}
.pk-row button:disabled{{opacity:.6;cursor:default}}
.pk-msg{{display:block;font-family:var(--sans);font-size:14px;margin:8px 0 0;min-height:1em}}
.pk-fine{{display:block;font-family:var(--sans);font-size:12px;color:var(--muted);margin:8px 0 0;line-height:1.5}}
@media (max-width:520px){{.pk-lead{{grid-template-columns:104px 1fr;gap:16px}}.pk-lead h3{{font-size:1.25rem}}}}
</style>
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
      <a href="/fiction/">Fiction</a>
      <a class="nav-cta" href="/#free">Free Sample</a>
    </nav>
  </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>&copy; {year} Jeffrey L. Carrier. All rights reserved.</span>
      <span><a href="/">Carrier Press LLC</a>, Diamondhead, Mississippi.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

DESC = ("Two quick questions, then three books picked for you: where to start, "
        "and two more if that one is not it. Young readers, mystery, true crime, "
        "classics and more.")

# The page logic. State lives in the hash (#me/horror) so Back works and a
# result can be shared. Without JavaScript the <noscript> shelf links still work.
JS = r"""
(function(){
var D=JSON.parse(document.getElementById('pk-data').textContent);
var root=document.getElementById('pk-app');
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function who(k){for(var i=0;i<D.who.length;i++)if(D.who[i].k===k)return D.who[i];return null;}
function lane(aud,k){var L=D.lanes[aud]||[];for(var i=0;i<L.length;i++)if(L[i].k===k)return L[i];return null;}
function buy(p,gift,small){
  var b=gift?p.gift:p.buy, label=b.f==='Amazon'?'Buy on Amazon':('Buy the '+b.f.toLowerCase());
  return '<a class="go" href="'+D.amz.replace('{}',encodeURIComponent(b.a))+'" target="_blank" rel="noopener" '+
    'aria-label="'+esc(label+', '+p.t+', on Amazon')+'">'+esc(label)+'</a>';
}
function facts(p){return p.facts.length?'<p class="pk-facts">'+esc(p.facts.join(' · '))+'</p>':'';}
function opts(items,cur,attr){
  return '<ul class="pk-opts">'+items.map(function(o){
    return '<li><button type="button" '+attr+'="'+esc(o.k)+'" aria-pressed="'+(o.k===cur)+'"><strong>'+
      esc(o.label)+'</strong>'+(o.line?'<span>'+esc(o.line)+'</span>':'')+'</button></li>';}).join('')+'</ul>';
}
function render(focus){
  var h=location.hash.replace(/^#/,'').split('/'), w=who(h[0]), l=w&&lane(w.aud,h[1]), out=[];
  out.push('<section class="pk-step" aria-labelledby="pk-q1"><h2 id="pk-q1" tabindex="-1"><span class="n">Question 1 of 2</span>Who is the book for?</h2>'+
    opts(D.who,w&&w.k,'data-who')+'</section>');
  if(w){
    out.push('<section class="pk-step" aria-labelledby="pk-q2"><h2 id="pk-q2" tabindex="-1"><span class="n">Question 2 of 2</span>'+
      (w.aud==='young'?'What do they enjoy?':(w.gift?'What do they like to read?':'What are you in the mood for?'))+'</h2>'+
      opts(D.lanes[w.aud],l&&l.k,'data-lane')+'</section>');
  }
  if(w&&l){
    var p=l.picks[0], fit=(w.gift?'A gift':'For you')+' · '+l.label;
    out.push('<section class="pk-step" aria-labelledby="pk-r"><h2 id="pk-r" tabindex="-1">Start here</h2>'+
      (l.note?'<p class="pk-note">'+esc(l.note)+'</p>':'')+
      '<div class="pk-lead"><a href="'+esc(p.url)+'" tabindex="-1" aria-hidden="true"><img src="/assets/covers/'+esc(p.a)+'.jpg" alt="" width="313" height="500" decoding="async"></a>'+
      '<div><p class="pk-tag">Our pick</p><h3><a href="'+esc(p.url)+'">'+esc(p.t)+'</a></h3>'+facts(p)+
      '<p class="pk-why">'+esc(p.why)+'</p><p class="pk-fit">Picked because you chose: '+esc(fit)+'</p>'+
      '<p class="pk-act">'+buy(p,w.gift)+'<a class="more" href="'+esc(p.url)+'">Read about it first</a></p></div></div>'+
      '<p class="pk-alts-h">If that one is not quite it</p><ul class="pk-alts">'+
      l.picks.slice(1).map(function(q){
        return '<li class="pk-alt"><a href="'+esc(q.url)+'" tabindex="-1" aria-hidden="true"><img src="/assets/covers/'+esc(q.a)+'.jpg" alt="" width="313" height="500" loading="lazy" decoding="async"></a>'+
          '<div><h4><a href="'+esc(q.url)+'">'+esc(q.t)+'</a></h4>'+facts(q)+'<p class="pk-why">'+esc(q.why)+'</p>'+
          '<p class="pk-act">'+buy(q,w.gift)+'</p></div></li>';}).join('')+'</ul>'+
      (!l.form?'':'<form class="pk-box pk-sub" action="'+esc(l.form)+'" method="post">'+
        '<p><strong>Hear when the next one comes out.</strong> Leave an email and you only hear about new books like these. One click unsubscribes you.</p>'+
        '<label for="pk-email" class="pk-lbl">Email address</label>'+
        '<span class="pk-row"><input id="pk-email" type="email" name="fields[email]" required autocomplete="email" placeholder="you@example.com">'+
        '<input type="hidden" name="fields[picker]" value="'+esc(w.k+'/'+l.k)+'">'+
        '<input type="hidden" name="ml-submit" value="1"><input type="hidden" name="anticsrf" value="true">'+
        '<button type="submit">Keep me posted</button></span>'+
        '<span class="pk-msg" role="status" aria-live="polite"></span>'+
        '<span class="pk-fine">The list is kept by MailerLite, the mailing service Carrier Press uses. It holds your email and the answers you picked here, nothing else.</span></form>')+
      (l.magnet?'<div class="pk-box"><p>Not ready to buy? Read the opening of The King in Yellow first, free by email.</p>'+
        '<p><a class="more" href="/#free">Get the free sample</a></p></div>':'')+
      '<p class="pk-end"><button type="button" data-reset>Start over</button><a href="'+esc(D.shelf[w.aud])+'">See the whole shelf</a></p></section>');
  }
  root.innerHTML=out.join('');
  if(focus){var t=document.getElementById(focus);if(t){t.focus({preventScroll:true});t.scrollIntoView({behavior:'smooth',block:'start'});}}
}
root.addEventListener('click',function(ev){
  var b=ev.target.closest('button'); if(!b)return;
  var h=location.hash.replace(/^#/,'').split('/'), f=null;
  if(b.hasAttribute('data-who')){h=[b.getAttribute('data-who')];f='pk-q2';}
  else if(b.hasAttribute('data-lane')){h=[h[0],b.getAttribute('data-lane')];f='pk-r';}
  else if(b.hasAttribute('data-reset')){h=[];f='pk-q1';}
  else return;
  history.pushState(null,'',h.length?'#'+h.join('/'):location.pathname);
  render(f);
});
root.addEventListener('submit',function(ev){
  var f=ev.target; if(!f.classList.contains('pk-sub')||!window.fetch)return;
  ev.preventDefault();
  var m=f.querySelector('.pk-msg'), b=f.querySelector('button');
  b.disabled=true; m.textContent='Adding you...';
  fetch(f.action,{method:'POST',body:new FormData(f)}).then(function(r){return r.json();}).then(function(j){
    if(j&&j.success){m.textContent='Done. Your picks are on their way to your inbox, from Jeffrey L. Carrier. Not there in a minute? Check Promotions or Spam.';f.querySelector('input[type=email]').value='';}
    else{m.textContent='That did not go through. Check the address and try again.';b.disabled=false;}
  }).catch(function(){m.textContent='That did not go through. Please try again in a moment.';b.disabled=false;});
});
window.addEventListener('popstate',function(){render(null);});
render(location.hash.length>1?'pk-r':null);
})();
"""


def build():
    D = json.loads(pathlib.Path("catalog.json").read_text())
    P = data(D)
    blob = json.dumps(P, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    shelves = [("Fiction", "/fiction/"), ("Classics", "/classics/"), ("Young readers", "/young-readers/"),
               ("Weird fiction", "/weird-fiction/"), ("Money and income", "/money/")]
    b = [HEAD.format(domain=DOMAIN, desc=e(DESC)),
         '<section class="wrap pk">',
         '<p class="sec-head" style="margin:0 0 10px"><span class="kicker">Not sure where to start?</span></p>',
         '<h1>Find your next book</h1>',
         '<p class="lede">Two quick questions, then one book to start with and two more if that one '
         'is not quite it. Every pick opens in print on Amazon.</p>',
         '<div id="pk-app" aria-live="polite"></div>',
         '<noscript><p class="lede">Browse by shelf instead: '
         + " &middot; ".join(f'<a href="{h}">{e(n)}</a>' for n, h in shelves) + '</p></noscript>',
         '</section>',
         '<script type="application/json" id="pk-data">' + blob + '</script>',
         '<script>' + JS + '</script>',
         FOOT.format(year=datetime.date.today().year)]
    s = "\n".join(b)
    for bad in ("—", "–", "&mdash;", "&ndash;"):
        assert bad not in s, "dash in picker page"
    out = pathlib.Path("pick")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(s, encoding="utf-8")
    nav.patch(out / "index.html")
    n = sum(len(v) for v in P["lanes"].values())
    print("wrote pick/index.html  --  %d lanes, %d picks" % (n, n * 3))


if __name__ == "__main__":
    build()
