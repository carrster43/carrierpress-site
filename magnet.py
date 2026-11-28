"""The free sample signup form, in one place (2026-11-27).

/free/ had the only working form; the journal posts, /weird-fiction/ and
/classics/ linked to it, which costs a click and loses readers on the way. Every
place now draws the same form from here, so the wording, the MailerLite form and
the consent line cannot drift apart.

MAGNET_FORM is the embedded form "Free sample: The King in Yellow
(carrierpress.com/free)"; it adds signups to the group TLO Readers
(192738353903305745), whose welcome automation (192738278727747164) sends the
sample from /free/*.epub and *.pdf. Double opt-in is on, so the first email is
the confirmation. No em or en dashes.
"""
import html

MAGNET_FORM = "204768097074152788"
ML_ACCOUNT = "2504319"
ACTION = f"https://assets.mailerlite.com/jsonp/{ML_ACCOUNT}/forms/{MAGNET_FORM}/subscribe"


def e(x):
    return html.escape(str(x), quote=True)


def form(fid="free"):
    """The form. `fid` must be unique on the page; its script finds the form by it."""
    return (f'<form id="{fid}-form" class="sp-form" action="{e(ACTION)}" method="post">'
            f'<label class="sp-label" for="{fid}-email">Your email</label>'
            f'<div class="sp-row"><input id="{fid}-email" type="email" name="fields[email]" '
            'required autocomplete="email" placeholder="you@example.com">'
            '<input type="hidden" name="ml-submit" value="1">'
            '<button class="btn btn-ink" type="submit">Send me the free sample</button></div>'
            '<p class="sp-fine">No spam. The list is kept by MailerLite, the mailing service Carrier Press '
            'uses. It holds your email, nothing else, and every email has a one click unsubscribe.</p>'
            '<p class="sp-done" hidden>Almost there. Check your inbox for a confirmation email from '
            'Jeffrey L. Carrier and click the link inside; your sample arrives right after. '
            'If it is not there, look in Promotions or Spam.</p></form>'
            f'<script>(function(){{var f=document.getElementById("{fid}-form");'
            'f.addEventListener("submit",function(ev){ev.preventDefault();'
            'fetch(f.action,{method:"POST",body:new FormData(f)}).then(function(r){return r.json();})'
            '.then(function(j){if(j&&j.success){f.querySelector(".sp-row").hidden=true;'
            'f.querySelector(".sp-done").hidden=false;}else{f.submit();}})'
            '.catch(function(){f.submit();});});})();</script>')


def block(fid, lead):
    """A compact signup box for the end of a page: one line of pitch, then the form."""
    return (f'<aside class="post-signup magnet-inline" aria-labelledby="{fid}-h">'
            f'<p id="{fid}-h"><strong>Free: the opening of <em>The King in Yellow</em>.</strong> {e(lead)}</p>'
            + form(fid) + '</aside>')
