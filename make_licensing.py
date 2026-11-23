#!/usr/bin/env python3
"""
/licensing/<slug>/ : the sales pages for the three apps sold to organisations,
not to the person using them (author 2026-11-22, "Sales page + inquiry"):

    Plan Finder      licensed to Medicare agencies
    GED Completion   contracted by adult education programs
    Waitlist         licensed to clinics and counseling centers

    python3 make_licensing.py

WHAT EACH PAGE CARRIES. What the app does, a sample of it working, what a
licence or pilot includes, the rules it is built inside, and an inquiry form.
NO PRICES: the author has set no rate card for these three, so every licence is
quoted in writing after a conversation. Add a price constant if that changes.

THE SAMPLES COME FROM THE APPS' OWN CODE, never written by hand. The learner and
the client are invented; every sentence they are shown was produced by running
the app's functions on 2026-11-22:
    GED Completion  lib/readiness.ts (readiness, suggestedOrder,
                    describeReadiness, diagnosticHeadline) and lib/reentry.ts
                    (planReturn), repo at 08c6a9d. Twelve answers a subject:
                    Language Arts 6, Math 5, Science 8, Social Studies 10.
    Waitlist        lib/modules.ts (MODULES), lib/instruments.ts (score,
                    describeChange, CADENCE_DAYS, MEANINGFUL_CHANGE) and
                    lib/crisis.ts (NOT_THERAPY, ALWAYS_AVAILABLE,
                    CRISIS_RESOURCES), repo at 0583c4a.
    Plan Finder     lib/compliance.ts (COVERAGE_DISCLAIMER, NO_STEERING,
                    ESTIMATE_NOTE, HANDOFF_NOTE), repo at cccc4c1, plus the live
                    sample comparison on GitHub Pages (planfinder-web).
If the app's wording changes, rerun it and paste the new output here.

PLAN FINDER AND THE MEDICARE RULES. The page sells software to agencies and
says nothing that markets a plan to a beneficiary. Plan Finder is deliberately
NOT a TPMO (PlanFinder lib/compliance.ts: flat licence, no steering, no
enrollment path), so the page does not recite the CMS TPMO disclaimer as if
Carrier Labs represented plans; that would claim a status it does not hold. It
carries a plain statement instead: Carrier Labs sells and represents no plan,
is not connected with Medicare, enrolls no one, and where to see every option
(Medicare.gov, 1-800-MEDICARE, SHIP). An agency's own TPMO obligations stay
with the agency, and the page says so. No Sprout, no season bar, no tip ask, no
waiting list, no cross-promotion on any of the three pages: they are written
for a buyer, and they are not patched by nav.py for that reason.

HOW THE FORM SENDS. Exactly as /publish/ (make_publish.py): no server. Send
builds a plain text email and opens the visitor's mail app addressed to INBOX;
if it does not open, the page shows the inquiry with a Copy button. The
carrierpress.com catch-all (ImprovMX, `*` to Gmail) delivers any address on the
domain, so one address lets Gmail file every licensing inquiry together, and
the subject names the app.

Customers never see merged or old app names here. No em or en dashes.
"""
import html, pathlib

from make_publish import STYLE as PUBLISH_STYLE

INBOX = "licensing@carrierpress.com"
DOMAIN = "carrierpress.com"
e = html.escape


class Raw(str):
    """Already HTML; must not be escaped."""


def url(slug):
    return "/licensing/%s/" % slug


# ---------------------------------------------------------------------------
# PLAN FINDER
# ---------------------------------------------------------------------------
PF_DEMO = "https://carrster43.github.io/planfinder-web/sample"
# lib/compliance.ts, verbatim (cccc4c1).
PF_SCREEN = [
    ("How plans are ranked", "Plans are ranked only on what you told us: your medicines, your doctors, and how you weigh "
     "cost against coverage. No insurer pays to appear higher, and your agency cannot change the order."),
    ("What the estimate is", "This is an estimate built from the plan's published costs and the medicines you listed. It is "
     "not a quote and it is not a guarantee. Formularies and networks change, and only your agent can confirm what a plan "
     "will actually cost you."),
    ("What the tool covers", "This tool compares the plans loaded by your agency. It may not include every plan available "
     "in your area. It is not connected to Medicare or to any government agency, and it does not enrol you in anything."),
    ("The hand-off", "Nothing here enrols you. Take this comparison to your agent, who is licensed to check it against your "
     "prescriptions and doctors and complete an application with you."),
]
PLANFINDER = dict(
    slug="planfinder", name="Plan Finder", buyer="agency",
    title="Plan Finder for Medicare agencies",
    desc=("A guided Medicare Advantage comparison your agents run with a client, ranked only on the client's own "
          "medicines, doctors and priorities. Licensed to agencies. It compares; your licensed agent enrolls."),
    lede=[
        "A guided Medicare Advantage comparison your agents run with a client across the table. Plans are ranked only "
        "on what the client said: their medicines, their doctors, and how they weigh cost against coverage.",
        "A plan that does not cover one of their medicines is shown and flagged in plain words, never quietly dropped "
        "down the list. That one sentence can spare a client a four figure surprise at the pharmacy.",
    ],
    cta=("Open the sample comparison", PF_DEMO, "Invented plans and an invented client, no account needed"),
    what=[
        ("The whole picture, ranked", "Premium, the yearly cost of the client's own medicines and the worst-case "
         "out of pocket figure, side by side for every plan in the county."),
        ("Medicines checked plan by plan", "Each plan says whether it covers each medicine, needs prior approval, "
         "or charges a share of the price instead of a fixed amount."),
        ("Doctors checked against the network", "Each plan says how many of the client's doctors it lists, with a "
         "standing reminder to confirm with the practice."),
        ("Your agency's name on it", "Your agency name, colour and phone number on the comparison your client sees."),
        ("Seats for your whole team", "One licence covers the agents you invite. An admin adds and removes them."),
        ("Never locked out mid-appointment", "If a payment is late, your agents keep access while it is sorted out, "
         "so no client is left waiting in the room."),
    ],
    sample_h="See it working",
    sample=Raw(
        '<p>The sample comparison runs the real ranking on invented plans, an invented county and an invented client '
        'taking four medicines. It shows the two plans with no monthly premium being disqualified: one does not cover a '
        'medicine, the other has no drug coverage at all.</p>'
        '<p><a class="btn btn-gold" href="%s" target="_blank" rel="noopener">Open the sample comparison</a></p>'
        '<p>Every comparison carries these lines, word for word, where your client reads them:</p>'
        '<ul class="grid">%s</ul>'
        % (PF_DEMO, "".join('<li><b>%s</b><span>%s</span></li>' % (e(h), e(t)) for h, t in PF_SCREEN))),
    includes_h="What a licence includes",
    includes=[
        ("Your counties' plans", "We load the plans sold in the counties you serve from CMS's published plan files, "
         "and refresh them each year before the enrollment period."),
        ("Agent seats", "A seat for each agent you name, managed by your admin."),
        ("Your branding, kept honest", "Name, colour and phone number. Branding stops there on purpose, so no setting "
         "can make one plan look better than another."),
        ("Saved comparisons", "Each finished comparison is stored exactly as it was shown to the client."),
        ("Set-up with you", "We set the agency up with your admin before the first client sees it."),
    ],
    next_line="Coming next, shaped by the first agencies: a printable comparison for the client to take home.",
    rules_h="Built inside the Medicare marketing rules",
    rules=Raw(
        '<p>Plan Finder is a comparison tool. It is built so that the three things that would turn a tool into marketing '
        'are not there to switch on:</p>'
        '<ul class="grid core">'
        '<li><b>No pay per lead or per enrollment</b><span>Your agency pays a flat licence. Nothing is paid per lead, '
        'per enrollment or as a share of commission, and there is no place in the system to record such a term.</span></li>'
        '<li><b>No steering</b><span>The ranking takes no carrier preference and no agency setting. The order comes '
        'only from what the client said.</span></li>'
        '<li><b>No enrollment</b><span>The comparison ends with a hand-off to your licensed agent. There is no way to '
        'submit an application through it.</span></li></ul>'
        '<p>Your agency\'s own marketing obligations, including the CMS disclaimer where your agency is a third party '
        'marketing organization, stay with your agency and its compliance team. We are glad to walk your compliance '
        'reviewer through how it works before you sign.</p>'),
    disclaimer=("Carrier Labs LLC does not sell, offer, market or represent any Medicare plan, is not paid for leads "
                "or enrollments, and is not connected with or endorsed by Medicare, CMS or any government agency. Plan "
                "Finder does not enroll anyone in a plan. For information on all of your Medicare options, contact "
                "Medicare.gov or 1-800-MEDICARE (TTY 1-877-486-2048), or your State Health Insurance Assistance "
                "Program (SHIP)."),
    faq=[
        ("Is Plan Finder sold to people on Medicare?", "No. It is licensed to agencies and used by their licensed "
         "agents with a client. Nothing on it is sold to a beneficiary."),
        ("Can we favour the carriers we contract with?", "No. There is no setting for it, by design. The order comes only "
         "from the client's own medicines, doctors and priorities, and every comparison tells the client so."),
        ("Where does the plan data come from?", "From the plan files CMS publishes each year, loaded for the counties you "
         "serve. The comparison tells the client it covers the plans your agency loaded, which may not be every plan in "
         "the area."),
        ("Does it check provider networks?", "It shows how many of the client's doctors a plan lists, and always tells "
         "the client to confirm with the practice, because provider directories are often wrong."),
        ("How is it priced?", "Per agency, by the number of agent seats. Tell us your team size in the form and we send "
         "a written quote."),
    ],
    org_types=["Independent agency", "Agency with several offices", "Field marketing organization", "Other"],
    size_label="Licensed agents who would use it",
    region_label="States you write business in",
    interests=["A walkthrough call", "A quote for our team", "A review for our compliance team", "Something else"],
    privacy="/planfinder/privacy/",
)

# ---------------------------------------------------------------------------
# GED COMPLETION
# ---------------------------------------------------------------------------
# Output of the app's own code on an invented learner (see the docstring).
GED_HEADLINE = "You can sit Social Studies now, without studying for it."
GED_ORDER = [
    ("Social Studies", 70, "You could sit Social Studies now. Book it before you talk yourself out of it."),
    ("Science", 90, "Science is close. A few sessions on the parts that tripped you up, then book it."),
    ("Math", 115, "Math needs some work first. That is normal, and it is the one to give real time to."),
    ("Language Arts", 150, "Language Arts needs some work first. That is normal, and it is the one to give real time to."),
]
GED_RETURNS = [
    ("Back after five days, one subject passed", "1 down.", "Next session on Science."),
    ("Back after five weeks, one subject passed", "Welcome back. Still 1 passed.",
     "Pick up on Science. One session, then see how you feel."),
    ("Back after four months, two subjects passed",
     "Welcome back. You still have 2 subjects passed, and they do not expire.",
     "Let us redo the diagnostic before anything else. It is twenty minutes and it is usually good news."),
    ("Back after four months, nothing passed yet", "Welcome back. Nothing you did is lost and nothing has expired.",
     "Let us redo the diagnostic before anything else. It is twenty minutes and it is usually good news."),
]


def ged_sample():
    order = "".join('<li><b>%s</b> <span class="small">(%d minute test)</span><br>%s</li>' % (e(s), m, e(t))
                    for s, m, t in GED_ORDER)
    back = "".join('<li><b>%s</b><span>&ldquo;%s&rdquo; %s</span></li>' % (e(w), e(g), e(n)) for w, g, n in GED_RETURNS)
    return Raw(
        '<p>An invented learner answers twelve diagnostic questions in each subject. This is what the app says back, '
        'word for word. It never shows them a percentage: every line ends in something to do.</p>'
        '<div class="done" style="margin-top:12px"><p><b>%s</b></p><ol class="steps">%s</ol></div>'
        '<p style="margin-top:18px">The order is the point. The subject they can already pass comes first, and shorter '
        'tests come first within each group, because a 70 minute sitting fits around a shift and a passed subject is '
        'still passed when life gets in the way in month three.</p>'
        '<h3 style="font-family:var(--serif);margin:28px 0 6px">When someone comes back</h3>'
        '<p>The moment that decides whether a learner finishes is the day they open the app after weeks away. The app '
        'never counts the days back to them, never mentions what they missed, and has no streak to break. A test checks '
        'every greeting it can produce for those words.</p>'
        '<ul class="grid">%s</ul>' % (e(GED_HEADLINE), order, back))


GED = dict(
    slug="gedcompletion", name="GED Completion", buyer="program",
    title="GED Completion for adult education programs",
    desc=("A GED completion engine for workforce boards, adult education programs, corrections and employers: "
          "diagnostic first, the nearest winnable test next, no streaks, and a staff roster that shows who has gone quiet."),
    lede=[
        "Most adults who stall on the GED do not stall on the teaching. They stall between tests, when a shift changes, "
        "a child is sick, or the next subject looks like a wall. GED Completion is built for that gap.",
        "It starts with a short diagnostic, tells each learner which subject they could sit now, orders the rest so the "
        "next win comes early, and gives your staff a roster of who has gone quiet so someone can call.",
    ],
    cta=("Ask about a pilot", "#inquire", "Tell us about your program"),
    what=[
        ("Diagnostic first", "A short diagnostic in each subject sorts it into sit it now, nearly there, or study first. "
         "It refuses to guess on too few answers."),
        ("The next win comes early", "Subjects they can pass now come first, and shorter tests first within each group."),
        ("No streaks, no shame", "No streak, no days-since counter, nothing that resets. Coming back is welcomed, every time."),
        ("A roster for your staff", "Who has passed what, what they are working on, and when they last studied, so a "
         "caseworker knows who to ring this week."),
        ("A line staff cannot cross", "Staff never see a learner's diagnostic answers or their shift and childcare "
         "pattern. The learner is told exactly what staff can see, on the screen where they connect."),
        ("Joining is the learner's choice", "Connecting to a program is optional, and the app says so."),
    ],
    sample_h="See it working",
    sample=None,  # ged_sample(), filled in below
    includes_h="What a pilot includes",
    includes=[
        ("One program, one cohort", "A pilot starts with one board, program, facility or employer and the learners "
         "you choose."),
        ("Diagnostic questions written with you", "The diagnostic question set is finished with the first program, "
         "so it fits the learners you serve."),
        ("Staff accounts", "Accounts for your caseworkers and instructors, scoped to your program only."),
        ("Set-up with your lead", "We set up your program with you and look at who is moving, and who is not, with "
         "your lead during the pilot."),
    ],
    next_line=("Coming next, planned with a corrections partner: a build that runs without open internet, for "
               "facilities where learners cannot go online."),
    rules_h="What it is, and what it is not",
    rules=Raw(
        '<p>GED Completion keeps learners moving toward the test. It does not teach the subjects, does not book tests and '
        'does not predict scores: booking happens at GED.com, and the app says so. It pairs well with the instruction '
        'your program already gives.</p>'),
    disclaimer=("GED is a registered trademark of the American Council on Education, and the GED test is administered "
                "by GED Testing Service. GED Completion is made by Carrier Labs LLC and is not affiliated with or "
                "endorsed by either."),
    faq=[
        ("Who pays?", "The program, the board, the facility or the employer. It is free to every learner."),
        ("Does it replace our instruction?", "No. It works alongside it. It tells a learner what to sit next and keeps "
         "them coming back; your instructors still teach."),
        ("What can our staff see?", "Each learner's subject status (passed, working on, diagnosed) and when and how long "
         "they studied. Not their diagnostic answers, and not their availability or childcare."),
        ("Does it work offline?", "The first version needs a connection. An offline build for facilities is the next "
         "stage, planned with a corrections partner."),
        ("How is it priced?", "Per learner seat per year, quoted in writing for your program. Tell us roughly how many "
         "learners in the form."),
    ],
    org_types=["Workforce development board", "Adult education program", "Corrections facility", "Employer",
               "Library or nonprofit", "Other"],
    size_label="Learners you would enroll",
    region_label="State or area you serve",
    interests=["A walkthrough call", "A pilot", "A written quote", "Something else"],
    privacy="/gedcompletion/privacy/",
)
GED["sample"] = ged_sample()

# ---------------------------------------------------------------------------
# WAITLIST
# ---------------------------------------------------------------------------
# lib/modules.ts MODULES (title, subtitle, minutes, step titles), 0583c4a.
WL_COURSES = [
    ("Why the waiting is its own problem", "Start here. Five minutes, no exercises.", 5,
     ["The wait is not neutral", "What this is and is not", "One thing before you go"]),
    ("Doing things first, feeling like it later",
     "The one with the best evidence behind it, and the least appealing premise.", 12,
     ["The order is backwards from what you would expect", "What has fallen away",
      "Make one of them absurdly small, and give it a time", "Afterwards, write down what actually happened"]),
    ("Arguing with your own thinking, on paper", "The core CBT exercise. Harder than it looks, worth doing badly.", 15,
     ["Thoughts are not observations", "Catch one", "Both columns, and the second one is the work",
      "Write the version that fits both columns"]),
    ("Worry, on an appointment", "For the kind of anxiety that runs all day and peaks at 3am.", 10,
     ["Trying to stop is what keeps it going", "Pick the slot", "During the day: write it, do not work it",
      "In the slot: sort them into two piles"]),
]
# lib/crisis.ts and lib/instruments.ts, verbatim.
WL_NOT_THERAPY = ("Waitlist is not therapy and it is not a therapist. It is structured self-help for the months before "
                  "your first appointment, so you are not doing nothing while you wait. Keep the appointment. Nothing "
                  "here replaces it, and nothing here is a reason to stop or change any medicine you take.")
WL_ALWAYS = "If things get bad, you do not have to wait for your appointment. Call or text 988, any time."
WL_SAME = ("About the same as last time. Scores move around a few points on their own, so that is not a step "
           "backwards.")
WL_CRISIS = ["988 Suicide and Crisis Lifeline", "988 by text", "Crisis Text Line (text 741741)",
             "Veterans Crisis Line (988, then 1)", "Emergency services (911)"]


def wl_sample():
    courses = "".join(
        '<li><b>%s</b><span>%s %d minutes.</span><span class="small" style="margin-top:8px">%s</span></li>'
        % (e(t), e(s), m, e(" · ".join(steps))) for t, s, m, steps in WL_COURSES)
    return Raw(
        '<p>Four short self-guided courses, each a handful of steps, with the exercise written into the app. The titles '
        'and lengths below are the app\'s own.</p>'
        '<ul class="grid">%s</ul>'
        '<h3 style="font-family:var(--serif);margin:28px 0 6px">The check-in every two weeks</h3>'
        '<p>The PHQ-9 and GAD-7 both ask about the last two weeks, so the check-in is offered every 14 days and not '
        'before. No chart is drawn until there are three check-ins, and a change of under 5 points is reported as what '
        'it is. This is the app\'s line for it, word for word:</p>'
        '<div class="done"><p>&ldquo;%s&rdquo;</p></div>'
        '<h3 style="font-family:var(--serif);margin:28px 0 6px">When someone answers item 9</h3>'
        '<p>Any answer above zero on PHQ-9 item 9, about thoughts of being better off dead or of self-harm, puts crisis '
        'resources on screen above the score, whatever the total says. That rule is part of the scoring itself and is '
        'tested at every value. A permanent Help now tab is on every screen, works with no signal, and does not record '
        'that it was opened. It lists: %s.</p>'
        '<p>Everywhere the app is used, it says: &ldquo;%s&rdquo;</p>'
        % (courses, e(WL_SAME), e(", ".join(WL_CRISIS)), e(WL_ALWAYS)))


WAITLIST = dict(
    slug="waitlist", name="Waitlist", buyer="organization",
    title="Waitlist for clinics and counseling centers",
    desc=("Structured self-guided CBT and a symptom check every two weeks for people waiting for a first appointment. "
          "Licensed to clinics, university counseling centers and employee assistance programs."),
    lede=[
        "Between a referral and a first appointment there are often months, and most people spend them doing nothing "
        "because nothing was offered. Waitlist gives that time a shape.",
        "Four short self-guided CBT courses, a PHQ-9 and GAD-7 check-in every two weeks, and crisis resources one tap "
        "away on every screen. It is free to the person waiting. The clinic pays.",
    ],
    cta=("Ask about a licence", "#inquire", "Tell us about your waiting list"),
    what=[
        ("Four short CBT courses", "Behavioural activation, thought records and worry time, five to fifteen minutes "
         "each, written for someone who has never done CBT."),
        ("A check-in every two weeks", "PHQ-9 and GAD-7 on their own two-week window, never more often, with change "
         "under 5 points reported as about the same."),
        ("Crisis resources that cannot be missed", "A permanent Help now tab in a colour used nowhere else, and item 9 "
         "handled before the score."),
        ("Honest about what it is", "It tells people it is not therapy on sign-in, on the courses, on the crisis screen "
         "and in their account, and tells them to keep the appointment."),
        ("Private by design", "Each person's records are theirs alone: no clinician or staff account can read them, "
         "and nothing ranks or triages them."),
    ],
    sample_h="See what it does",
    sample=None,  # wl_sample(), filled in below
    includes_h="What a licence includes",
    includes=[
        ("Access for everyone you refer", "Free to every person on your waiting list, for as long as they wait."),
        ("The instruments at their exact wording", "The PHQ-9 and GAD-7 are loaded from the official source at their "
         "exact published wording, never retyped or shortened."),
        ("Set-up with your clinical lead", "We walk your clinical lead through every screen and the crisis flow before "
         "anyone is referred."),
    ],
    next_line=("Coming next, built only under a partner clinic's clinical governance: a summary the person can choose "
               "to bring to their first appointment."),
    rules_h="What it is, and what it is not",
    rules=Raw(
        '<p>&ldquo;%s&rdquo;</p>'
        '<p>That is the app\'s own wording, shown to every person who uses it. Waitlist records answers. It does not '
        'diagnose, does not rank anyone\'s urgency and does not alert anyone, so no one should be referred to it in '
        'place of care. The crisis lines in it are United States lines, and it says so.</p>' % e(WL_NOT_THERAPY)),
    disclaimer=("Waitlist is structured self-help made by Carrier Labs LLC. It is not therapy, not a diagnosis and not "
                "a crisis service. If someone is in danger, call or text 988, or call 911."),
    faq=[
        ("Who pays?", "The clinic, the university or the employer. It is free to every person using it."),
        ("Can our clinicians see what patients enter?", "Not in this version. Each person's records are theirs alone, "
         "which is what keeps it self-help. A summary the person chooses to share is the next stage, built with a "
         "partner clinic under its clinical governance."),
        ("Does it triage or alert anyone?", "No. It records answers and shows crisis resources. Deciding someone is in "
         "danger is a clinical act, and the app does not make it."),
        ("Is it only for the United States?", "For now, yes. The crisis numbers are US lines and the app says so."),
        ("How is it priced?", "Per organisation, by the number of people you refer. Tell us roughly how many are on "
         "your waiting list and we send a written quote."),
    ],
    org_types=["Clinic or group practice", "University counseling center", "Employee assistance program",
               "Health system", "Other"],
    size_label="People on your waiting list (roughly)",
    region_label="State or area you serve",
    interests=["A walkthrough call", "A licence quote", "A review by our clinical lead", "Something else"],
    privacy="/waitlist/privacy/",
)
WAITLIST["sample"] = wl_sample()

PRODUCTS = [PLANFINDER, GED, WAITLIST]

# The hero button on each app's /apps/<slug>/ page (make_app_pages.py reads it).
HERO = {
    "planfinder": (url("planfinder"), "For agencies: licence Plan Finder", "See the sample and ask for a quote"),
    "gedcompletion": (url("gedcompletion"), "For programs: ask about a pilot", "See it working and get in touch"),
    "waitlist": (url("waitlist"), "For clinics: ask about a licence", "See what it does and get in touch"),
}
TIMELINES = ["Just looking", "Within a month", "Within 3 months", "Later this year"]

STYLE = PUBLISH_STYLE + """
.lic-cta{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:22px 0 0}
.disc{border-left:3px solid var(--gold);background:var(--card);padding:14px 18px;margin:22px 0 0;max-width:760px;
  font-family:var(--sans);font-size:14px;line-height:1.6;color:var(--ink-soft)}
.grid .small{display:block}
.done ol.steps{margin-top:8px}
"""

SCRIPT = r"""
(function(){
var f=document.getElementById("inq"),done=document.getElementById("inq-done"),
    pre=document.getElementById("inq-text"),mail=document.getElementById("inq-mail"),
    copy=document.getElementById("inq-copy"),TO="__TO__",APP="__APP__",PAGE="__PAGE__";
function v(n){var el=f.elements[n];return el&&el.value!==undefined?String(el.value||"").trim():""}
function all(n){return Array.prototype.map.call(f.querySelectorAll('input[name="'+n+'"]:checked'),function(i){return i.value})}
function line(k,x){return x?k+": "+x+"\n":""}
f.addEventListener("submit",function(ev){
  ev.preventDefault();
  if(!f.reportValidity())return;
  var want=all("want");
  var body="NEW LICENSING INQUIRY, "+APP+", carrierpress.com"+PAGE+"\n\n"
    +line("Name",v("name"))+line("Role",v("role"))+line("Email",v("email"))+line("Phone",v("phone"))
    +"\n"+line("Organization",v("org"))+line("Type",v("type"))+line("Where",v("region"))
    +line("__SIZE__",v("size"))+line("Timeline",v("when"))
    +"\nINTERESTED IN: "+(want.length?want.join(", "):"not ticked")+"\n"
    +(v("notes")?"\nANYTHING ELSE\n"+v("notes")+"\n":"");
  var subj="Licensing inquiry: "+APP+" ("+v("org")+")";
  var href="mailto:"+TO+"?subject="+encodeURIComponent(subj)+"&body="+encodeURIComponent(body);
  pre.textContent="To: "+TO+"\nSubject: "+subj+"\n\n"+body;
  mail.href=href;done.hidden=false;
  done.scrollIntoView({behavior:"smooth",block:"start"});
  window.location.href=href});
copy.addEventListener("click",function(){
  var t=pre.textContent;function ok(){copy.textContent="Copied"}
  function sel(){var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);
    try{document.execCommand("copy");ok()}catch(_){}}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,sel)}else{sel()}});
})();
"""


def cards(rows, cls="grid"):
    return '<ul class="%s">%s</ul>' % (cls, "".join('<li><b>%s</b><span>%s</span></li>' % (e(n), e(d)) for n, d in rows))


def opts(items, placeholder=None):
    head = '<option value="">%s</option>' % e(placeholder) if placeholder else ""
    return head + "".join("<option>%s</option>" % e(o) for o in items)


def body_of(x):
    return x if isinstance(x, Raw) else "<p>%s</p>" % e(x)


def page(p):
    slug, name = p["slug"], p["name"]
    canon = "https://%s%s" % (DOMAIN, url(slug))
    cta_label, cta_href, cta_sub = p["cta"]
    ext = ' target="_blank" rel="noopener"' if cta_href.startswith("http") else ""
    script = (SCRIPT.replace("__TO__", INBOX).replace("__APP__", name)
              .replace("__PAGE__", url(slug)).replace("__SIZE__", p["size_label"]))
    faq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q), e(a)) for q, a in p["faq"])
    want = "".join('<label class="pk"><input type="checkbox" name="want" value="%s"><span>%s</span></label>'
                   % (e(w), e(w)) for w in p["interests"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(p["title"])} | Carrier Labs</title>
<meta name="description" content="{e(p["desc"])}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carrier Labs">
<meta property="og:title" content="{e(p["title"])}">
<meta property="og:description" content="{e(p["desc"])}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://{DOMAIN}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
<style>{STYLE}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="/apps/{e(slug)}/">
      <img class="mark-dark" src="/assets/logo-mark-small.png" alt="" width="34" height="24">
      <img class="mark-light" src="/assets/logo-mark-light-small.png" alt="" width="34" height="24">
      <span>{e(name)}</span>
    </a>
    <nav class="nav" aria-label="Main">
      <a class="nav-cta" href="#inquire">Get in touch</a>
    </nav>
  </div>
</header>

<main id="main" class="pg">
<div class="wrap">
<h1>{e(p["title"])}</h1>
{"".join('<p class="lede">%s</p>' % e(x) for x in p["lede"])}
<div class="lic-cta"><a class="btn btn-gold" href="{e(cta_href)}"{ext}>{e(cta_label)}</a>
<span class="small">{e(cta_sub)}</span></div>
<nav class="jump" aria-label="On this page"><a href="#what">What it does</a><a href="#sample">{e(p["sample_h"])}</a><a href="#includes">{e(p["includes_h"])}</a><a href="#rules">{e(p["rules_h"])}</a><a href="#faq">Questions</a><a href="#inquire">Get in touch</a></nav>

<h2 id="what">What it does</h2>
{cards(p["what"], "grid core")}

<h2 id="sample">{e(p["sample_h"])}</h2>
{body_of(p["sample"])}

<h2 id="includes">{e(p["includes_h"])}</h2>
<p>Every licence is quoted in writing for your {e(p["buyer"])}, after a short conversation about what you need.</p>
{cards(p["includes"])}
<p class="small" style="margin-top:14px">{e(p["next_line"])}</p>

<h2 id="rules">{e(p["rules_h"])}</h2>
{body_of(p["rules"])}
<p class="disc">{e(p["disclaimer"])}</p>

<h2 id="faq">Questions</h2>
<div class="faq">{faq}</div>

<h2 id="inquire">Get in touch</h2>
<p>Tell us a little about your organization and we reply personally, by email, within a week. Fields marked <span class="req">*</span> are required. Nothing here is a commitment on either side.</p>
<form class="inq" id="inq" action="mailto:{INBOX}" method="post" enctype="text/plain">
<fieldset><legend>About you</legend>
<div class="row">
<label class="f">Your name <span class="req">*</span><input type="text" name="name" autocomplete="name" required maxlength="120"></label>
<label class="f">Your role<input type="text" name="role" autocomplete="organization-title" maxlength="120"></label>
</div>
<div class="row">
<label class="f">Work email <span class="req">*</span><input type="email" name="email" autocomplete="email" required maxlength="160"></label>
<label class="f">Phone<small>Optional, if you would rather talk.</small><input type="tel" name="phone" autocomplete="tel" maxlength="40"></label>
</div>
</fieldset>
<fieldset><legend>About your organization</legend>
<div class="row">
<label class="f">Organization <span class="req">*</span><input type="text" name="org" autocomplete="organization" required maxlength="160"></label>
<label class="f">Type <span class="req">*</span><select name="type" required>{opts(p["org_types"], "Choose one")}</select></label>
</div>
<div class="row">
<label class="f">{e(p["region_label"])}<input type="text" name="region" maxlength="160"></label>
<label class="f">{e(p["size_label"])}<small>An estimate is fine.</small><input type="number" name="size" min="0" inputmode="numeric"></label>
</div>
<label class="f">Timeline<select name="when">{opts(TIMELINES)}</select></label>
<div class="f">What would help<div class="opts">{want}</div></div>
<label class="f">Anything else<small>Questions, or what you would want it to do for you.</small>
<textarea name="notes" maxlength="1200"></textarea></label>
</fieldset>
<div class="send"><button class="btn btn-gold" type="submit">Send inquiry</button>
<span class="small">This opens your email app with the inquiry filled in, addressed to {INBOX}. Nothing is sent until you press send there.</span></div>
</form>

<div class="done" id="inq-done" hidden>
<p><b>Your inquiry is ready.</b> Your email app should have opened with it filled in. Press send there and it is on its way.</p>
<p>If nothing opened, <a id="inq-mail" href="mailto:{INBOX}">try again</a>, or copy the inquiry below and email it to <a href="mailto:{INBOX}">{INBOX}</a>.</p>
<pre id="inq-text"></pre>
<button class="btn btn-ink" type="button" id="inq-copy">Copy inquiry</button>
</div>
<script>{script}</script>
</div>
</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="colophon">
      <span>{e(name)} is made by Carrier Labs LLC.</span>
      <span><a href="/apps/{e(slug)}/">About {e(name)}</a> · <a href="{e(p["privacy"])}">Privacy</a></span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def check(text):
    bad = [c for c in ("—", "–") if c in text]
    if bad:
        raise SystemExit("licensing: an em or en dash is in the copy; the house rule forbids them")


if __name__ == "__main__":
    for p in PRODUCTS:
        out = pathlib.Path(url(p["slug"]).strip("/")) / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        text = page(p)
        check(text)
        out.write_text(text, encoding="utf-8")
        print("licensing: wrote %s, inquiries to %s" % (out, INBOX))
