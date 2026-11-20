/* Handoff on carrierpress.com/apps/handoff/ (2026-11-20): the invited parent's
   way in, and the way back in from another browser. Neither needs a key: the
   other parent's key covers the arrangement (author 2026-11-20, "A, creator
   covers"). The gate holds the record and sets an HttpOnly party cookie on a
   good answer; this page never sees or stores it.

     POST /__gate/handoff/join     {code, name}     -> {ok, recoveryCode} or {ok:false, reason, message}
     POST /__gate/handoff/recover  {recoveryCode}   -> {ok}               or {ok:false, reason, message}

   The recovery code is shown once and kept nowhere by this page: not in
   localStorage, not in the address bar. Plain script, no libraries. */
(function () {
  "use strict";
  var APP = "/handoff/app/";
  var UNREACHABLE = "Could not reach the record. Check your connection and try again.";

  function post(call, body) {
    return fetch("/__gate/handoff/" + call, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    }).then(function (r) {
      return r.json().catch(function () { return { ok: false, message: UNREACHABLE }; });
    }).catch(function () { return { ok: false, message: UNREACHABLE }; });
  }

  function say(el, text, bad) {
    el.textContent = text;
    el.className = "hj-note" + (bad ? " bad" : "");
  }

  function failed(res) {
    return (res && typeof res.message === "string" && res.message) || UNREACHABLE;
  }

  function pad(n) { return String(n).padStart(2, "0"); }
  function now() {
    var d = new Date();
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()) + " " + pad(d.getHours()) + ":" + pad(d.getMinutes());
  }

  function recoveryFile(code, name) {
    return [
      "HANDOFF RECOVERY CODE",
      "",
      "Your name in the record: " + name,
      "Saved: " + now(),
      "",
      code,
      "",
      "This code opens your place in the shared record in any browser:",
      "open carrierpress.com/apps/handoff/ and enter it under",
      "\"Coming back in a new browser?\", or open Handoff, go to Account,",
      "and enter it under Recovery code.",
      "It is shown once. Nobody can show it to you again, and anyone",
      "holding it can write in the record as you. Keep it private.",
      ""
    ].join("\n");
  }

  function download(text, filename) {
    var url = URL.createObjectURL(new Blob([text], { type: "text/plain;charset=utf-8" }));
    var a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  /* ---- Joining, from an invite link: /apps/handoff/?join=CODE ---- */
  var join = document.getElementById("hj-join");
  var code = "";
  try { code = (new URLSearchParams(location.search).get("join") || "").trim(); } catch (e) { code = ""; }
  if (join && code) {
    var form = document.getElementById("hj-join-form");
    var nameIn = document.getElementById("hj-name");
    var note = form.querySelector(".hj-note");
    var done = join.querySelector(".hj-done");
    var shown = join.querySelector(".hj-code");
    join.hidden = false;
    join.scrollIntoView({ block: "start" });
    document.getElementById("hj-title").focus({ preventScroll: true });

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var name = nameIn.value.trim();
      if (!name) { say(note, "Type the name the other parent will see beside what you write.", true); nameIn.focus(); return; }
      var btn = form.querySelector("button");
      btn.disabled = true;
      say(note, "Joining.", false);
      post("join", { code: code, name: name }).then(function (res) {
        if (!res.ok || typeof res.recoveryCode !== "string") {
          btn.disabled = false;
          say(note, failed(res), true);
          return;
        }
        // The invite is used up: take it out of the address bar so a reload
        // does not offer to join again.
        try { history.replaceState(null, "", location.pathname + location.hash); } catch (e) {}
        form.hidden = true;
        shown.textContent = res.recoveryCode;
        done.hidden = false;
        join.querySelector(".hj-save").addEventListener("click", function () {
          download(recoveryFile(res.recoveryCode, name), "handoff-recovery-code.txt");
        });
        shown.setAttribute("tabindex", "-1");
        shown.focus();
      });
    });
  }

  /* ---- Coming back in another browser, with the recovery code ---- */
  var back = document.getElementById("hj-back-form");
  if (back) {
    var input = document.getElementById("hj-recovery");
    var backNote = back.querySelector(".hj-note");
    var open = document.querySelector("#hj-back .hj-open");
    back.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var rc = input.value.trim();
      if (!rc) { say(backNote, "Paste the recovery code you saved when you started or joined.", true); input.focus(); return; }
      var btn = back.querySelector("button");
      btn.disabled = true;
      say(backNote, "Checking the code.", false);
      post("recover", { recoveryCode: rc }).then(function (res) {
        btn.disabled = false;
        if (!res.ok) { say(backNote, failed(res), true); return; }
        input.value = "";
        back.hidden = true;
        open.hidden = false;
        open.insertAdjacentHTML("afterbegin", "<span>You are back in, in this browser. </span>");
        open.querySelector("a").focus();
      });
    });
  }
})();
