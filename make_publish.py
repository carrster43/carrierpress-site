#!/usr/bin/env python3
"""
/publish/ : the author inquiry page. Outside authors ask Carrier Press to
publish their book (author 2026-11-20).

    python3 make_publish.py

WHAT IT SELLS. One core package (editorial review, copyedit and proofread,
typesetting, ISBN, release on Amazon KDP and IngramSpark under the Carrier
Press imprint) plus add-ons quoted one by one: author website, a Sprout
magazine feature, audiobook, podcast, video, other media. NO PRICES on the
page: every book is quoted after the sample is read, and the author has set
no rate card. Add one to PACKAGE / ADDONS below if that changes.

HOW THE FORM SENDS. There is no server behind it. Pressing Send builds a plain
text email from the answers and opens the author's own mail app, addressed to
INBOX. The carrierpress.com catch-all (ImprovMX, `*` to Gmail, verified
2026-10-27) delivers any address on the domain, so a dedicated one lets Gmail
filter inquiries without a new mailbox. If the mail app does not open, the
page shows the finished inquiry with a Copy button and the address, so nothing
the author typed is lost.

Why not a server: the only one on this domain is the AppGate worker, and
adding a route there means a gate deploy. A static mailto form ships with the
site and costs nothing. If inquiries ever need storing, the natural upgrade is
a /__gate/inquiry route that keeps the same field names.

The page is hand-built, not templated off a book page, and nav.patch() gives it
the shared menu, footer row and season bar like every other page.
"""
import html, json, pathlib

import nav

INBOX = "publish@carrierpress.com"
OUT = pathlib.Path("publish/index.html")
TITLE = "Publish with Carrier Press"
DESC = ("Editorial review, copyedit, typesetting, ISBNs for every format including large print, and release on Amazon and IngramSpark "
        "under the Carrier Press imprint, with audiobook, podcast, video, website and magazine add-ons.")

# THE FORMATS. Every edition is its own ISBN (author 2026-11-20: charge per
# ISBN, discount for taking every format including large print). The ISBNs come
# from the Carrier Press Bowker block, NOT KDP's free ones: a free KDP ISBN lists
# the book as "Independently published", which defeats publishing it under the
# imprint. Set the two prices to show them on the page; None keeps them off.
FORMATS = ["Paperback", "Hardcover", "Large print", "Ebook"]
ISBN_EACH = 49            # author 2026-11-20
ISBN_ALL = 149            # all-formats bundle, saves $47 against 4 x $49
N_WORD = {3: "three", 4: "four", 5: "five", 6: "six"}.get(len(FORMATS), str(len(FORMATS)))


def isbn_price():
    if ISBN_EACH and ISBN_ALL:
        return f" ISBNs are ${ISBN_EACH} per format, or ${ISBN_ALL} for all {N_WORD}."
    return f" Take all {N_WORD} formats and the ISBNs come at a bundle discount."


# (key, name, what it is). The key is the checkbox value and the line in the email.
PACKAGE = [
    ("Editorial review", "A full read of the manuscript and a written editorial letter on structure, "
     "pacing, character and voice: what is working, and what the book needs before it goes to print."),
    ("Copyedit and proofread", "A line by line pass for grammar, consistency, continuity and house style, "
     "then a final proof of the typeset pages before anything is released."),
    ("Typesetting", "Print ready interiors for paperback, hardcover and a large print edition, set in a "
     "proper book face, and a formatted ebook with a working table of contents."),
    ("ISBNs", "One for each format you choose (paperback, hardcover, large print, ebook), registered to the "
     "Carrier Press imprint, so the book carries the Carrier Press name in every catalog that lists it."
     + isbn_price()),
    ("Amazon KDP", "Paperback, hardcover, large print and Kindle editions on Amazon, with the listing, "
     "description, categories and keywords written for you."),
    ("IngramSpark", "Print distribution through Ingram, the catalog bookstores and libraries order from, "
     "so a shop or library can order the book like any other."),
]
ADDONS = [
    ("Audiobook", "An audiobook edition of the book, produced and published for listeners."),
    ("Podcast", "A podcast series that introduces the book and its world to new listeners."),
    ("Video", "A book trailer and short videos sized for sharing."),
    ("Author website", "A home for you and your books: a page for each title, buy links and a reader list signup."),
    ("Magazine feature", "A feature on you and your book in Sprout, the weekly Carrier Press magazine."),
    ("Other media", "Something else in mind? Tell us in the form and we will quote it."),
]
# THE TRUST SECTIONS (author 2026-11-20: "look as we are a legitimate publishing
# house"). Modelled on the ELEMENTS that real submissions pages carry (survey of
# 13 presses, the IBPA Hybrid Publisher Criteria, Writer Beware, the ALLi
# partner code), written in our own words. Every line below is a promise the
# press must keep; change the constant, not the prose, when a term changes.
REPLY_DAYS = 30          # the reply-time promise on the page
ROYALTY = "60% of net receipts on print books and 70% on ebooks"   # author 2026-11-20; IBPA needs over 50%
PACKAGE_PRICE = 3900     # the core publishing package, author 2026-11-20
# THE COMPLETE PACKAGE (author 2026-11-20: "add a $12,000 one to see what is
# possible"). The She Writes Press price point, built only from things Carrier
# Press already does for its own books. Everything in the publishing package,
# plus every item below. Same royalty and payout terms as the core package.
COMPLETE_PRICE = 12000
COMPLETE = [
    ("Full developmental edit", "A detailed edit of the whole manuscript, not just a letter, and a second full read after you revise."),
    ("ISBNs for all four formats", "Paperback, hardcover, large print and ebook, all registered to the Carrier Press imprint."),
    ("Audiobook", "An audiobook edition, produced and published alongside the print and ebook editions."),
    ("Podcast", "A podcast series that introduces the book and its world to new listeners."),
    ("Video", "A book trailer and a set of short videos sized for sharing."),
    ("Author website", "A home for you and your books: a page for each title, buy links and a reader list signup."),
    ("Sprout magazine feature", "A feature on you and your book in Sprout, the weekly Carrier Press magazine."),
    ("Launch campaign", "An announcement to the Carrier Press reader list, and pitches to independent bookstores and libraries in your region."),
]
TIERS = [f"Publishing package (${PACKAGE_PRICE:,})", f"Complete package (${COMPLETE_PRICE:,})", "Not sure yet"]
# Payout terms (author 2026-11-20): royalties paid within 150 days of the sale,
# once the author's earned balance is over $100. The 150 days covers the slowest
# rail: IngramSpark pays about 90 days after the end of the sale month, KDP
# about 60. Smaller balances carry forward; they are never forfeited.
PAY_DAYS = 150
PAY_MIN = 100
PROMISES = [
    ("No reading fee, ever", "Sending an inquiry and a sample costs nothing. You pay only if we offer a contract and you sign it."),
    (f"A reply within {REPLY_DAYS} days", "Every inquiry gets a personal answer, yes or no, by email."),
    ("Your work stays private", "Your manuscript is read by the publisher and no one else, and is never used for anything but your book."),
    ("Simultaneous submissions welcome", "Send your book to other presses or agents too. Just tell us if you sign elsewhere."),
    ("You keep your copyright", "We license the right to publish your book. The book stays yours."),
    ("Everything in writing first", "The quote and the contract spell out every fee, deliverable, date and royalty before any work begins."),
]
NEVERS = [
    "require you to buy copies of your own book",
    "promise sales numbers, bestseller lists or a profit",
    "send unsolicited offers or chase you with countdown discounts",
    "hold back your royalties to recover our fees",
    "use AI tools on your book without telling you first in the quote",
    "keep the rights if the book goes out of print or you end the contract under its terms",
]
# The standard agreement, published in full (author 2026-11-20). The PDF is
# built from Documents/Carrier_Press_LLC/13_PUBLISHING_AGREEMENT_TEMPLATE_CARRIER_PRESS.md
# (pandoc to docx, soffice to pdf) and copied here; rebuild and recopy it
# whenever a term changes, or the page and the contract disagree.
CONTRACT = "/publish/carrier-press-publishing-agreement.pdf"
CONTRACT_LINK = f'<a href="{CONTRACT}">Read the standard publishing agreement (PDF)</a>'


class Raw(str):
    """An FAQ answer that is already HTML and must not be escaped."""


FAQ = [
    ("Do I keep the rights to my book?",
     "Yes. You keep the copyright. The contract licenses Carrier Press to publish the formats you choose, "
     "and it includes a reversion clause, so the rights come back to you under the terms we both sign."),
    ("How are royalties paid?",
     (f"You receive {ROYALTY}. Net receipts are what the store pays Carrier Press for a copy, after the "
      "store's discount and the printing cost. " if ROYALTY else "")
     + f"Royalties are paid within {PAY_DAYS} days of the sale, once your earned balance is over ${PAY_MIN}. "
       f"A smaller balance carries forward to the next payment and is never lost. The contract states your "
       "royalty and defines net receipts in plain words, and royalties are never held back to recover the "
       "package fee."),
    (f"Why {PAY_DAYS} days?",
     "Amazon pays publishers about two months after the end of the month a book sells, and IngramSpark about "
     f"three. {PAY_DAYS} days lets every store's payment arrive before yours is due, so you are paid on a date "
     "we can always keep."),
    ("Will my book be in bookstores?",
     "Through IngramSpark your book is listed in the Ingram catalog, which bookstores and libraries order from, "
     "so any shop or library can order it. We do not promise shelf placement: that is each store's choice."),
    ("Do I have to buy copies?",
     "No. Author copies are available at print cost if you want them for events or gifts, and never required."),
    ("Can I bring my own editor or finished files?",
     "Yes. Untick anything you already have in the form and the quote covers only what is left."),
    ("Why does each format need its own ISBN?",
     "An ISBN names one edition of one book. The paperback, hardcover, large print and ebook are each a "
     "separate edition, so each needs its own number for stores and libraries to order the right one. "
     "That is why ISBNs are priced per format, with a discount when you take them all."),
    ("Who owns the ISBNs?",
     "Carrier Press, as the publisher of record. An ISBN identifies the publisher as well as the edition, "
     "which is what puts the Carrier Press name on your book in every catalog. If the rights come back to "
     "you, the next edition takes new ISBNs under its new publisher, as it would leaving any press."),
    ("Do you use AI?",
     "Audiobook, podcast and video editions are produced with AI narration and AI production tools, and the "
     "quote says so. If AI tools are used in any other part of the work, the quote names them before anything "
     "starts, and you can decline them."),
    ("Can I see a sample contract?",
     Raw(f"Yes. {CONTRACT_LINK}. It is the same agreement every author signs, with Schedule A filled in "
         "for your book. Take whatever time you need to read it before you sign.")),
    ("What if something goes wrong?",
     f"Write to {INBOX} and the publisher answers personally. Every concern gets a written reply."),
]
SHELF = 8                 # covers shown under "Books we have published"
GENRES = ["Literary fiction", "Mystery or thriller", "True crime", "Science fiction or fantasy",
          "Horror", "Romance", "Historical fiction", "Young adult", "Middle grade",
          "Children's picture book", "Memoir", "Nonfiction", "Poetry", "Other"]
TIMELINES = ["Flexible", "As soon as possible", "Within 3 months", "3 to 6 months", "6 months or more"]

e = html.escape


def shelf():
    """The first book of each of the press's own lines, then standalones: proof the
    press publishes ORIGINAL books. The classics are left out on purpose; an
    author weighing a press wants to see new work, not reprints."""
    cat = json.loads(pathlib.Path("catalog.json").read_text(encoding="utf-8"))
    secs = [x for x in cat["sections"] if x["id"] != "classics" and not x.get("nonfic")]
    firsts = [x["books"][0] for x in secs if x["id"] != "standalone" and x.get("books")]
    rest = next((x["books"] for x in secs if x["id"] == "standalone"), [])
    out = []
    for b in firsts + rest:
        a, t = b.get("a"), b.get("t")
        if a and t and not b.get("soon") and pathlib.Path(f"assets/covers/{a}.jpg").exists():
            out.append(f'<a href="https://www.amazon.com/dp/{a}" target="_blank" rel="noopener">'
                       f'<img src="/assets/covers/{a}.jpg" alt="{e(t)}" loading="lazy" width="120" height="180"></a>')
        if len(out) == SHELF:
            break
    return "".join(out)


def cards(rows):
    return "".join(f'<li><b>{e(n)}</b><span>{e(d)}</span></li>' for n, d in rows)


def checks(rows, name, checked):
    return "".join(
        f'<label class="pk"><input type="checkbox" name="{name}" value="{e(n)}"{" checked" if checked else ""}>'
        f'<span>{e(n)}</span></label>' for n, _ in rows)


def radios(name, options, required=True):
    req = " required" if required else ""
    return "".join(f'<label class="rd"><input type="radio" name="{name}" value="{e(o)}"{req}>'
                   f'<span>{e(o)}</span></label>' for o in options)


def options(items, placeholder=None):
    head = f'<option value="">{e(placeholder)}</option>' if placeholder else ""
    return head + "".join(f"<option>{e(o)}</option>" for o in items)


STYLE = """
.pg{padding:48px 0 72px}
.pg h1{font-family:var(--serif);font-size:clamp(2rem,4vw,2.8rem);margin:0 0 12px;color:var(--ink)}
.pg h2{font-family:var(--serif);font-size:1.6rem;margin:56px 0 8px;color:var(--ink)}
.pg p{line-height:1.65;max-width:70ch;color:var(--ink-soft);margin:0 0 14px}
.pg .lede{font-size:1.12rem;color:var(--ink)}
.small{font-family:var(--sans);font-size:13px;color:var(--muted)}
.jump{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0;font-family:var(--sans);font-size:14px}
.jump a{border:1px solid var(--line);border-radius:999px;padding:6px 14px;color:var(--ink);text-decoration:none;background:var(--card)}
.jump a:hover{border-color:var(--gold)}
.grid{list-style:none;padding:0;margin:18px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.grid li{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:16px 18px}
.grid.core li{border-top:3px solid var(--gold)}
.grid b{display:block;font-family:var(--serif);font-size:1.15rem;color:var(--ink);margin:0 0 6px}
.grid span{display:block;font-size:.95rem;line-height:1.5;color:var(--ink-soft)}
.steps{counter-reset:s;list-style:none;padding:0;margin:14px 0 0;max-width:70ch}
.steps li{counter-increment:s;position:relative;padding:0 0 14px 40px;line-height:1.6;color:var(--ink-soft)}
.steps li::before{content:counter(s);position:absolute;left:0;top:0;width:26px;height:26px;border-radius:50%;
  background:var(--gold-bright);color:#1a1a2e;font:600 13px/26px var(--sans);text-align:center}
.steps b{color:var(--ink)}
form.inq{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:24px;margin:18px 0 0;max-width:760px}
.inq fieldset{border:0;padding:0;margin:0 0 22px}
.inq legend{font-family:var(--serif);font-size:1.2rem;color:var(--ink);margin:0 0 10px;padding:0}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.f{display:flex;flex-direction:column;gap:6px;margin:0 0 14px;font-family:var(--sans);font-size:14px;color:var(--ink)}
.f small{color:var(--muted);font-size:12.5px}
.inq input[type=text],.inq input[type=email],.inq input[type=url],.inq input[type=number],.inq select,.inq textarea{
  font:inherit;font-size:16px;color:var(--ink);background:var(--paper);border:1px solid var(--line);
  border-radius:6px;padding:10px 12px;width:100%;box-sizing:border-box}
.inq textarea{min-height:130px;resize:vertical;line-height:1.5}
.inq input:focus,.inq select:focus,.inq textarea:focus{outline:2px solid var(--gold);outline-offset:1px}
.opts{display:flex;flex-wrap:wrap;gap:8px;font-family:var(--sans);font-size:14px}
.pk,.rd{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:999px;
  padding:7px 14px;background:var(--paper);color:var(--ink);cursor:pointer}
.pk:has(input:checked),.rd:has(input:checked){border-color:var(--gold);background:var(--paper-2)}
.pk input,.rd input{accent-color:var(--gold);margin:0}
.req{color:var(--gold)}
.agree{display:flex;gap:10px;align-items:flex-start;font-family:var(--sans);font-size:14px;color:var(--ink);margin:0 0 18px}
.agree input{margin-top:3px;accent-color:var(--gold)}
.send{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.done{border:1px solid var(--gold);border-radius:8px;background:var(--paper-2);padding:20px 22px;margin:18px 0 0;max-width:760px}
.done pre{white-space:pre-wrap;font:13px/1.55 ui-monospace,Menlo,monospace;background:var(--card);color:var(--ink);
  border:1px solid var(--line);border-radius:6px;padding:14px;max-height:320px;overflow:auto}
.never{max-width:70ch;padding-left:20px;line-height:1.7;color:var(--ink-soft)}
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:12px;margin:18px 0 0;max-width:900px}
.shelf img{width:100%;height:auto;aspect-ratio:2/3;object-fit:cover;border-radius:3px;box-shadow:0 4px 14px rgba(0,0,0,.25);display:block}
.who{display:flex;gap:20px;align-items:flex-start;max-width:760px;margin:16px 0 0}
.who img{border-radius:6px;flex:none}
.faq{max-width:760px;margin:12px 0 0}
.faq details{border-bottom:1px solid var(--line);padding:12px 0}
.faq summary{cursor:pointer;font-weight:600;color:var(--ink)}
.faq details p{margin:10px 0 0}
.up{display:block;margin:12px 0 0;color:var(--ink)}
.up.bad{color:#b3261e}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.inq input[type=file]{font:inherit;font-size:15px;color:var(--ink)}
@media (max-width:560px){form.inq{padding:18px 16px}.who{flex-direction:column}}
"""

# UPLOADS (author 2026-11-20: authors upload the manuscript and cover "for
# consideration"). Files go to the carrierpress-submissions worker
# (~/Projects/carrierpress-submissions), which writes them to a private R2
# bucket that deletes them after KEEP_DAYS. Leave UPLOADS False until that
# worker answers /__submit/health with storage:true, or the page offers a box
# that cannot work.
UPLOADS = False
UPLOAD_URL = "/__submit/file"
UPLOAD_MAX_MB = 95
KEEP_DAYS = 180
MANUSCRIPT_EXT = ".docx,.doc,.pdf,.rtf,.odt"
COVER_EXT = ".pdf,.jpg,.jpeg,.png,.tif,.tiff"

SCRIPT = r"""
(function(){
var f=document.getElementById("inq"),done=document.getElementById("inq-done"),
    pre=document.getElementById("inq-text"),mail=document.getElementById("inq-mail"),
    copy=document.getElementById("inq-copy"),btn=f.querySelector('button[type="submit"]'),
    st=document.getElementById("inq-status"),TO="__TO__",NF=__NF__,UP="__UP__",MAX=__MAX__*1048576;
function v(n){var el=f.elements[n];return el&&el.value!==undefined?String(el.value||"").trim():""}
function all(n){return Array.prototype.map.call(f.querySelectorAll('input[name="'+n+'"]:checked'),function(i){return i.value})}
function line(k,x){return x?k+": "+x+"\n":""}
function say(t,bad){if(!st)return;st.hidden=!t;st.textContent=t||"";st.className="small up"+(bad?" bad":"")}
function makeRef(){var d=new Date(),p=function(n){return(n<10?"0":"")+n},a="abcdefghijklmnopqrstuvwxyz0123456789",r="",b=new Uint8Array(6);
  (window.crypto||window.msCrypto).getRandomValues(b);for(var i=0;i<6;i++)r+=a[b[i]%36];
  return d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+"-"+r}
function chosen(){var out=[];["manuscript","cover"].forEach(function(k){var el=f.elements[k];if(el&&el.files&&el.files[0])out.push({kind:k,file:el.files[0],input:el})});return out}
function okType(item){var ext=(/\.[a-z0-9]+$/i.exec(item.file.name)||[""])[0].toLowerCase();return item.input.accept.split(",").indexOf(ext)>=0}
function send(ref,item,i,n,cb){
  var fd=new FormData();fd.append("kind",item.kind);fd.append("ref",ref);fd.append("name",v("name"));fd.append("email",v("email"));
  fd.append("title",v("title"));fd.append("website",v("website"));fd.append("file",item.file);
  var x=new XMLHttpRequest();x.open("POST",UP);
  x.upload.onprogress=function(e){if(e.lengthComputable)say("Uploading "+item.kind+" ("+(i+1)+" of "+n+"): "+Math.round(e.loaded/e.total*100)+" percent")};
  x.onload=function(){var r={};try{r=JSON.parse(x.responseText)}catch(_){}
    if(x.status===200&&r.ok)cb(null,r.file);else cb(r.error||("Upload failed ("+x.status+"). Try again, or send a link instead."))};
  x.onerror=function(){cb("The upload could not reach Carrier Press. Check your connection and try again.")};
  x.send(fd)}
function finish(ref,files){
  var pk=all("package"),ad=all("addon"),fm=all("format");
  var body="NEW AUTHOR INQUIRY, carrierpress.com/publish/\n"+(ref?"Reference: "+ref+"\n":"")+"\n"
    +line("Name",v("name"))+line("Pen name",v("pen"))+line("Email",v("email"))+line("Website or social",v("site"))
    +"\n"+line("Book title",v("title"))+line("Genre",v("genre"))+line("Word count",v("words"))
    +line("Manuscript stage",v("stage"))+line("Published before",v("before"))+line("Timeline",v("when"))
    +"\nFORMATS: "+(fm.length?fm.join(", ")+(fm.length===NF?" (all formats, ISBN bundle)":""):"none ticked")
    +"\nPACKAGE CHOSEN: "+v("tier")
    +"\nPUBLISHING PACKAGE ITEMS: "+(pk.length?pk.join(", "):"none ticked")
    +"\nADD-ONS: "+(ad.length?ad.join(", "):"none")+"\n"
    +(files.length?"\nFILES UPLOADED (private storage, reference "+ref+")\n"+files.join("\n")+"\n":"")
    +"\nSYNOPSIS\n"+v("synopsis")+"\n"
    +(v("sample")?"\nSAMPLE LINK\n"+v("sample")+"\n":"")
    +(v("notes")?"\nANYTHING ELSE\n"+v("notes")+"\n":"")
    +"\nThe author confirms they hold the rights to this work.\n";
  var subj="Author inquiry: "+v("title")+" ("+v("name")+")";
  var href="mailto:"+TO+"?subject="+encodeURIComponent(subj)+"&body="+encodeURIComponent(body);
  pre.textContent="To: "+TO+"\nSubject: "+subj+"\n\n"+body;
  mail.href=href;
  done.hidden=false;
  done.scrollIntoView({behavior:"smooth",block:"start"});
  window.location.href=href}
f.addEventListener("submit",function(ev){
  ev.preventDefault();
  if(!f.reportValidity())return;
  var items=UP?chosen():[],ref=UP?makeRef():"";
  for(var i=0;i<items.length;i++){
    if(!okType(items[i])){say("The "+items[i].kind+" must be one of: "+items[i].input.accept.split(",").join(" "),true);return}
    if(items[i].file.size>MAX){say("The "+items[i].kind+" is over "+(MAX/1048576)+" MB. Send a link to it instead.",true);return}}
  if(!items.length){finish(ref,[]);return}
  btn.disabled=true;var names=[];
  (function next(i){
    if(i===items.length){btn.disabled=false;say("Files uploaded. Opening your email app.");finish(ref,names);return}
    send(ref,items[i],i,items.length,function(err,name){
      if(err){btn.disabled=false;say(err,true);return}
      names.push(name);next(i+1)})})(0)
});
copy.addEventListener("click",function(){
  var t=pre.textContent;
  function ok(){copy.textContent="Copied"}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,function(){sel()})}else{sel()}
  function sel(){var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);
    try{document.execCommand("copy");ok()}catch(_){}}
});
})();
""".replace("__TO__", INBOX).replace("__NF__", str(len(FORMATS))).replace(
    "__UP__", UPLOAD_URL if UPLOADS else "").replace("__MAX__", str(UPLOAD_MAX_MB))


FILES_HTML = (
    f'<label class="f">Manuscript file<small>Word, PDF, RTF or ODT, up to {UPLOAD_MAX_MB} MB.</small>'
    f'<input type="file" name="manuscript" accept="{MANUSCRIPT_EXT}"></label>'
    f'<label class="f">Cover file<small>If you already have one. PDF, JPG, PNG or TIFF, up to {UPLOAD_MAX_MB} MB.</small>'
    f'<input type="file" name="cover" accept="{COVER_EXT}"></label>'
    f'<p class="small">Files go straight to private Carrier Press storage, are read only by the publisher, and are '
    f'deleted automatically after {KEEP_DAYS} days. If we publish your book, we keep a working copy under the contract.</p>'
    '<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>\n'
) if UPLOADS else ""
SAMPLE_HINT = ("Or share a Google Drive or Dropbox link instead of uploading." if UPLOADS else
               "A shared Google Drive or Dropbox link to the first three chapters. Optional, but it speeds things up.")
SEND_NOTE = (f"This uploads any files you chose, then opens your email app with the inquiry filled in, addressed to "
             f"{INBOX}. The inquiry is sent when you press send there." if UPLOADS else
             f"This opens your email app with the inquiry filled in, addressed to {INBOX}. "
             "Nothing is sent until you press send there.")


def page():
    canon = "https://carrierpress.com/publish/"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(TITLE)} | Carrier Press</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Press">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://carrierpress.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>{STYLE}</style>
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

<main id="main" class="pg">
<div class="wrap">
<h1>{e(TITLE)}</h1>
<p class="lede">Carrier Press is opening its list to a small number of outside authors. One package
takes a finished manuscript all the way to a published book: edited, typeset, given an ISBN and
released under the Carrier Press imprint on Amazon and through IngramSpark to bookstores and libraries.</p>
<p class="lede">Add audio, video, a website or a magazine feature when you want the book to reach further.</p>
<p>We read every inquiry ourselves and take on only the books we believe we can publish well, so not every
manuscript is accepted.</p>
<nav class="jump" aria-label="On this page"><a href="#promises">Our promises</a><a href="#package">The publishing package</a><a href="#complete">The complete package</a><a href="#addons">Add-on packages</a><a href="#books">Our books</a><a href="#how">How it works</a><a href="#faq">Questions</a><a href="#inquire">Send an inquiry</a></nav>

<h2 id="promises">Our promises to authors</h2>
<ul class="grid core">{cards(PROMISES)}</ul>
<p style="margin-top:22px"><b>Carrier Press will never:</b></p>
<ul class="never">{"".join(f"<li>{e(n[0].upper() + n[1:])}.</li>" for n in NEVERS)}</ul>

<h2 id="package">The publishing package</h2>
<p>Everything a manuscript needs to become a book on the shelf, in one package:
<b>${PACKAGE_PRICE:,}</b>, plus ISBNs for the formats you choose (${ISBN_EACH} each, or ${ISBN_ALL} for all {N_WORD}).
Your royalty is {ROYALTY}.</p>
<ul class="grid core">{cards(PACKAGE)}</ul>

<h2 id="complete">The complete package</h2>
<p>Everything in the publishing package, plus the whole release around it, in one price:
<b>${COMPLETE_PRICE:,}</b>. Same royalty, same payment terms, and no add-ons to choose.</p>
<ul class="grid core">{cards(COMPLETE)}</ul>
<p class="small">The launch campaign is a promise of work, not of sales: no one can promise how many copies a book will sell.</p>

<h2 id="addons">Add-on packages</h2>
<p>With the publishing package, each add-on is quoted on its own, so you choose only what your book needs.</p>
<ul class="grid">{cards(ADDONS)}</ul>
<p class="small">Audiobook, podcast and video editions are produced with AI narration and AI production tools.</p>

<h2 id="books">Books we have published</h2>
<p>Original fiction from the Carrier Press list, the first book of each series. <a href="/">See the whole catalog</a>.</p>
<div class="shelf">{shelf()}</div>

<h2 id="who">Who you work with</h2>
<div class="who"><img src="/assets/portrait.jpg" width="110" height="108" alt="Jeffrey L. Carrier" loading="lazy">
<p>Carrier Press is run by its publisher, Jeffrey L. Carrier, a novelist and a veteran of the U.S. Navy and
U.S. Air Force, from the Mississippi Gulf Coast. Your book is handled by the publisher from the first read to
release day. <a href="/#about">More about Jeffrey</a>.</p></div>

<h2 id="how">How it works</h2>
<ol class="steps">
<li><b>Send an inquiry.</b> Tell us about the book and what you would like done. It takes about five minutes.</li>
<li><b>We read your sample.</b> You get a personal reply within {REPLY_DAYS} days, yes or no, with any questions.</li>
<li><b>You get a written quote.</b> Scope, price, schedule, rights and royalties are set out in writing before any work begins. {CONTRACT_LINK}.</li>
<li><b>We make the book.</b> You approve the edit, the typeset pages and the listing before anything is released.</li>
</ol>

<h2 id="faq">Questions authors ask</h2>
<div class="faq">{"".join(f"<details><summary>{e(q)}</summary><p>{a if isinstance(a, Raw) else e(a)}</p></details>" for q, a in FAQ)}</div>

<h2 id="inquire">Send an inquiry</h2>
<p>Fields marked <span class="req">*</span> are required. Nothing here is a commitment on either side.</p>
<form class="inq" id="inq" action="mailto:{INBOX}" method="post" enctype="text/plain">
<fieldset><legend>About you</legend>
<div class="row">
<label class="f">Your name <span class="req">*</span><input type="text" name="name" autocomplete="name" required maxlength="120"></label>
<label class="f">Email <span class="req">*</span><input type="email" name="email" autocomplete="email" required maxlength="160"></label>
</div>
<div class="row">
<label class="f">Pen name<small>If you publish under another name.</small><input type="text" name="pen" maxlength="120"></label>
<label class="f">Website or social<small>Optional.</small><input type="url" name="site" placeholder="https://" maxlength="300"></label>
</div>
</fieldset>

<fieldset><legend>About the book</legend>
<div class="row">
<label class="f">Book title <span class="req">*</span><input type="text" name="title" required maxlength="200"></label>
<label class="f">Genre <span class="req">*</span><select name="genre" required>{options(GENRES, "Choose one")}</select></label>
</div>
<div class="row">
<label class="f">Word count<small>An estimate is fine.</small><input type="number" name="words" min="0" step="500" inputmode="numeric"></label>
<label class="f">Timeline<select name="when">{options(TIMELINES)}</select></label>
</div>
<div class="f">Where is the manuscript? <span class="req">*</span>
<div class="opts">{radios("stage", ["Complete and revised", "Complete first draft", "Still in progress"])}</div></div>
<div class="f">Published before?
<div class="opts">{radios("before", ["No, this is my first book", "Yes, self-published", "Yes, traditionally published"], False)}</div></div>
<label class="f">Synopsis <span class="req">*</span><small>What happens, who it is for, and why you wrote it. Up to 1,200 characters.</small>
<textarea name="synopsis" required maxlength="1200"></textarea></label>
{FILES_HTML}<label class="f">Link to a sample<small>{SAMPLE_HINT}</small>
<input type="url" name="sample" placeholder="https://" maxlength="500"></label>
</fieldset>

<fieldset><legend>What you would like</legend>
<div class="f">Which package? <span class="req">*</span>
<div class="opts">{radios("tier", TIERS)}</div></div>
<div class="f">Formats<div class="opts">{"".join(f'<label class="pk"><input type="checkbox" name="format" value="{e(x)}"{" checked" if x in ("Paperback", "Ebook") else ""}><span>{e(x)}</span></label>' for x in FORMATS)}</div>
<small>Each format gets its own ISBN. Choose all {N_WORD} and the ISBNs are discounted as a bundle.</small></div>
<div class="f">The publishing package<div class="opts">{checks(PACKAGE, "package", True)}</div>
<small>All six are ticked. Untick anything you already have, such as your own ISBN or finished edit.</small></div>
<div class="f">Add-on packages<div class="opts">{checks(ADDONS, "addon", False)}</div></div>
<label class="f">Anything else<small>Questions, other media you have in mind, or anything we should know.</small>
<textarea name="notes" maxlength="800"></textarea></label>
</fieldset>

<label class="agree"><input type="checkbox" name="rights" required><span>I wrote this book, or otherwise hold the rights to publish it. <span class="req">*</span></span></label>
<div class="send"><button class="btn btn-gold" type="submit">Send inquiry</button>
<span class="small">{SEND_NOTE}</span></div>
<p class="small up" id="inq-status" role="status" aria-live="polite" hidden></p>
</form>

<div class="done" id="inq-done" hidden>
<p><b>Your inquiry is ready.</b> Your email app should have opened with it filled in. Press send there and it is on its way.</p>
<p>If nothing opened, <a id="inq-mail" href="mailto:{INBOX}">try again</a>, or copy the inquiry below and email it to <a href="mailto:{INBOX}">{INBOX}</a>.</p>
<pre id="inq-text"></pre>
<button class="btn btn-ink" type="button" id="inq-copy">Copy inquiry</button>
</div>
<script>{SCRIPT}</script>
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


if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page(), encoding="utf-8")
    nav.patch(OUT)
    print("publish: wrote %s, inquiries to %s, %d package items, %d add-ons"
          % (OUT, INBOX, len(PACKAGE), len(ADDONS)))
