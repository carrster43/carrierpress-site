/* The paywall on the app landing pages. The server decides who gets in; this
   only sends the key to it, and tells the app the key is in, so a buyer does
   not paste it twice. */
(function () {
  var box = document.getElementById("gate");
  if (!box) return;
  var slug = box.getAttribute("data-slug");
  var appUrl = "/" + slug + "/app/";
  var form = box.querySelector("form");
  var input = box.querySelector("input");
  var note = box.querySelector(".gate-note");
  var openBox = box.querySelector(".gate-open");
  var locked = /[?&]locked=1\b/.test(location.search);

  var MESSAGES = {
    invalid: "That key was not recognised. Check it against your Gumroad receipt.",
    tier: "That Carrier Press Access key is on the Books tier, which does not open the apps.",
    lapsed: "That subscription has ended. Renew it in your Gumroad library, then try the key again.",
    revoked: "That purchase was refunded or is in dispute, so its key no longer opens the app.",
    offline: "Gumroad did not answer. Your key may be fine, so please try again in a minute."
  };

  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function drop(k) { try { localStorage.removeItem(k); } catch (e) {} }
  function keyIn(k) { try { var r = JSON.parse(get(k)); return r && typeof r.key === "string" ? r.key : null; } catch (e) { return null; } }

  var SHARED = "carrierPressLicense";
  var RECORDS = {
    cleared: ["web.license"], whoserves: ["webLicense"], boatready: ["boatreadyLicense", SHARED],
    conceptionzodiac: [SHARED], cancelled: [SHARED], downpour: [SHARED], cast: ["web.member"]
  };

  /* Write the key where this app's own screens look for it. Each shape is the
     one that app's lib/webLicense.web.ts stores. */
  function seed(key, res) {
    var at = new Date().toISOString();
    var rec = function (product) {
      var r = { key: key, okAt: at, checkedAt: at };
      if (product) r.product = product;
      return JSON.stringify(r);
    };
    var flag = "unlocked:" + slug, access = res.product === "access";
    if (slug === "cleared") return put("web.license", rec(access ? "access" : null));
    if (slug === "whoserves") return put("webLicense", rec(access ? "access" : null));
    if (slug === "cast") {
      if (res.product === "member") return put("web.member", JSON.stringify({ key: key, okAt: Date.now() }));
      var owned = [];
      try { owned = JSON.parse(get("web.books")) || []; } catch (e) {}
      if (owned.indexOf(res.book) < 0) owned.push(res.book);
      return put("web.books", JSON.stringify(owned.sort()));
    }
    put(flag, "1");
    if (access) { put(SHARED, rec("access")); put(flag + ":access", "1"); }
    if (res.product === "sub") { put("boatreadyLicense", rec("sub")); put(flag + ":access", "1"); }
  }

  function unseed() {
    (RECORDS[slug] || []).forEach(drop);
    drop("unlocked:" + slug); drop("unlocked:" + slug + ":access");
    if (slug === "cast") drop("web.books");
  }

  function post(path, body) {
    return fetch(path, { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json(); });
  }
  function say(text, bad) { note.textContent = text; note.className = "gate-note" + (bad ? " bad" : ""); }
  function showOpen() { form.hidden = true; openBox.hidden = false; say("", false); }

  function tryStoredKeys(list) {
    if (!list.length) return Promise.resolve(false);
    var key = list[0];
    return post("/__gate/unlock", { slug: slug, key: key }).then(function (res) {
      if (!res.ok) return tryStoredKeys(list.slice(1));
      seed(key, res);
      return true;
    }).catch(function () { return false; });
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var key = input.value.trim();
    if (!key) return say("Paste the license key from your Gumroad receipt.", true);
    var btn = form.querySelector("button");
    btn.disabled = true;
    say("Checking your key.", false);
    post("/__gate/unlock", { slug: slug, key: key }).then(function (res) {
      if (res.ok) { seed(key, res); location.href = appUrl; return; }
      btn.disabled = false;
      say(MESSAGES[res.reason] || MESSAGES.offline, true);
    }).catch(function () { btn.disabled = false; say(MESSAGES.offline, true); });
  });

  box.querySelector(".gate-forget").addEventListener("click", function () {
    post("/__gate/forget", { slug: slug }).then(function () {
      unseed();
      openBox.hidden = true; form.hidden = false;
      say("Your key is gone from this browser.", false);
    }).catch(function () { say("That did not go through. Please try again.", true); });
  });

  if (locked) {
    say("This app opens with a license key.", false);
    box.scrollIntoView({ block: "center" });
  }

  /* Someone who bought before the paywall has a key in this browser already. */
  fetch("/__gate/status?slug=" + encodeURIComponent(slug), { credentials: "same-origin" })
    .then(function (r) { return r.json(); })
    .then(function (st) {
      if (st.unlocked) return showOpen();
      var keys = (RECORDS[slug] || []).map(keyIn).filter(Boolean);
      return tryStoredKeys(keys).then(function (ok) {
        if (!ok) return;
        if (locked) location.replace(appUrl); else showOpen();
      });
    }).catch(function () {});

  /* The sample questions on Cleared's page. */
  Array.prototype.forEach.call(document.querySelectorAll(".pf-q"), function (q) {
    Array.prototype.forEach.call(q.querySelectorAll("button"), function (b) {
      b.addEventListener("click", function () {
        q.classList.add("done");
        b.classList.add(b.hasAttribute("data-right") ? "right" : "wrong");
        Array.prototype.forEach.call(q.querySelectorAll("button"), function (o) {
          o.disabled = true;
          if (o.hasAttribute("data-right")) o.classList.add("right");
        });
        q.querySelector(".pf-why").hidden = false;
      });
    });
  });

  /* Cast's few lines, read by this browser's own voices, as the app does. */
  var hear = document.getElementById("pf-hear");
  if (hear) {
    if (!("speechSynthesis" in window)) { hear.hidden = true; return; }
    var lines = document.querySelectorAll("#pf-lines [data-voice]");
    var speaking = false;
    hear.addEventListener("click", function () {
      if (speaking) { speechSynthesis.cancel(); speaking = false; hear.textContent = "Hear these lines"; return; }
      var all = speechSynthesis.getVoices();
      if (!all.length) { hear.textContent = "This browser has no voices to read these"; hear.disabled = true; return; }
      var en = all.filter(function (v) { return /^en/i.test(v.lang); });
      var slots = {};
      var next = 0;
      speaking = true;
      hear.textContent = "Stop";
      Array.prototype.forEach.call(lines, function (l, i) {
        var u = new SpeechSynthesisUtterance(l.textContent);
        var who = l.getAttribute("data-voice");
        if (!(who in slots)) slots[who] = next++;
        if (en.length) u.voice = en[slots[who] % en.length];
        if (i === lines.length - 1) u.onend = function () { speaking = false; hear.textContent = "Hear these lines"; };
        speechSynthesis.speak(u);
      });
    });
  }
})();
