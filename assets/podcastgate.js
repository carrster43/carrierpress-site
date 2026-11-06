/* The members' podcast. The server decides who gets audio; this only sends the
   key to it and shows the players once it says yes. */
(function () {
  var box = document.getElementById("pc-gate");
  if (!box) return;
  var form = box.querySelector("form");
  var input = box.querySelector("input");
  var note = box.querySelector(".gate-note");
  var open = box.querySelector(".pc-open");
  var MESSAGES = {
    invalid: "That key was not recognised. Check it against your Gumroad receipt.",
    tier: "That Carrier Press Access key is on the Apps tier, which does not include the podcast.",
    lapsed: "That membership has ended. Renew it in your Gumroad library, then try the key again.",
    revoked: "That purchase was refunded or is in dispute, so its key no longer opens the podcast.",
    offline: "Gumroad did not answer. Your key may be fine, so please try again in a minute."
  };
  function each(sel, fn) { Array.prototype.forEach.call(document.querySelectorAll(sel), fn); }
  function say(text, bad) { note.textContent = text; note.className = "gate-note" + (bad ? " bad" : ""); }
  function show(unlocked) {
    each("audio[data-src]", function (a) {
      if (unlocked) { if (!a.getAttribute("src")) a.setAttribute("src", a.getAttribute("data-src")); }
      else { a.pause(); a.removeAttribute("src"); }
      a.hidden = !unlocked;
    });
    each(".pc-lock", function (el) { el.hidden = unlocked; });
    form.hidden = unlocked;
    open.hidden = !unlocked;
    say("", false);
  }
  function post(path, body) {
    return fetch(path, { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json(); });
  }
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var key = input.value.trim();
    if (!key) return say("Paste the license key from your Gumroad receipt.", true);
    say("Checking your key.", false);
    post("/__gate/unlock", { slug: "podcast", key: key }).then(function (res) {
      if (res.ok) { input.value = ""; show(true); }
      else say(MESSAGES[res.reason] || MESSAGES.offline, true);
    }).catch(function () { say(MESSAGES.offline, true); });
  });
  box.querySelector(".pc-forget").addEventListener("click", function () {
    post("/__gate/forget", { slug: "podcast" }).then(function () { show(false); });
  });
  fetch("/__gate/status?slug=podcast", { credentials: "same-origin" })
    .then(function (r) { return r.ok ? r.json() : { unlocked: false }; })
    .then(function (res) { show(!!res.unlocked); })
    .catch(function () { show(false); });
})();
