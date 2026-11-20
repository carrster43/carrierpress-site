// Check a Handoff export without trusting anyone (2026-11-20).
//
// Runs entirely in this browser: nothing pasted here is sent anywhere. It finds
// every line of the export's VERIFICATION DATA that parses as a message with
// the seven chain fields, recomputes each hash with the formula the record
// uses (Handoff lib/chain.ts, the same as the phone's database), and walks the
// chain the way the server does. Same formula, same verdicts: Handoff's tests
// hold both to vectors made on Postgres 17.
(function () {
  "use strict";
  var FIELDS = ["seq", "author_ref", "author_name", "sent_at", "body", "content_hash", "chain_hash"];
  var TS = /^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?\s*(Z|[+-]\d{2}(?::?\d{2})?)$/i;
  var pad = function (n, w) { return String(n).padStart(w, "0"); };

  function stamp(sentAt) {
    var m = TS.exec(String(sentAt).trim());
    if (!m) throw new Error("bad timestamp");
    var zone = m[8], off = 0;
    if (zone.toUpperCase() !== "Z") {
      var d = zone.slice(1).replace(":", "");
      off = (zone[0] === "-" ? -1 : 1) * (Number(d.slice(0, 2)) * 60 + Number(d.slice(2, 4) || "0"));
    }
    var wall = new Date(0);
    wall.setUTCFullYear(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
    wall.setUTCHours(Number(m[4]), Number(m[5]), Number(m[6]), 0);
    var micros = BigInt(wall.getTime()) * 1000n + BigInt((m[7] || "").padEnd(6, "0")) - BigInt(off) * 60000000n;
    var frac = ((micros % 1000000n) + 1000000n) % 1000000n;
    var u = new Date(Number((micros - frac) / 1000n));
    return pad(u.getUTCFullYear(), 4) + "-" + pad(u.getUTCMonth() + 1, 2) + "-" + pad(u.getUTCDate(), 2) + "T" +
      pad(u.getUTCHours(), 2) + ":" + pad(u.getUTCMinutes(), 2) + ":" + pad(u.getUTCSeconds(), 2) + "." + pad(frac, 6) + "+00";
  }

  async function sha(text) {
    var buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
    return Array.from(new Uint8Array(buf), function (b) { return b.toString(16).padStart(2, "0"); }).join("");
  }

  function rowsIn(text) {
    var rows = [];
    text.split(/\r?\n/).forEach(function (line) {
      var t = line.trim();
      if (t[0] !== "{") return;
      try {
        var o = JSON.parse(t);
        var has = function (f) { return Object.prototype.hasOwnProperty.call(o, f); };
        // A message outside the exported period is printed as hashes only
        // (seq, content_hash, chain_hash): it carries the chain, not its text.
        if (FIELDS.every(has)) rows.push(o);
        else if (has("seq") && has("content_hash") && has("chain_hash") && Object.keys(o).length === 3) { o.hashOnly = true; rows.push(o); }
      } catch (e) { /* not a data line */ }
    });
    return rows.sort(function (a, b) { return a.seq - b.seq; });
  }

  async function verify(rows) {
    var prev = "", checked = 0, linked = 0;
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i], content = null;
      if (r.hashOnly) {
        content = r.content_hash;
        linked += 1;
      } else {
        try {
          if (r.author_ref !== null) content = await sha([String(r.seq), r.author_ref, r.author_name, stamp(r.sent_at), r.body].join("\x1f"));
        } catch (e) { content = null; }
      }
      var chain = content === null ? null : await sha(prev + content);
      if (content !== r.content_hash || chain !== r.chain_hash) return { ok: false, checked: checked, linked: linked, firstBadSeq: r.seq };
      prev = r.chain_hash;
      checked += 1;
    }
    return { ok: true, checked: checked, linked: linked, firstBadSeq: null };
  }

  window.HandoffVerify = { rowsIn: rowsIn, verify: verify, stamp: stamp };

  var form = typeof document !== "undefined" && document.getElementById("hv-form");
  if (!form) return;
  var out = document.getElementById("hv-result");
  var say = function (cls, html) { out.className = "hv-result " + cls; out.innerHTML = html; out.hidden = false; out.focus(); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  async function check(text) {
    var rows = rowsIn(text);
    if (!rows.length) return say("hv-none", "No verification data found. Paste the whole export, including the VERIFICATION DATA section at the end.");
    var v = await verify(rows);
    var first = rows[0].seq, last = rows[rows.length - 1];
    var gap = rows.some(function (r, i) { return i > 0 && r.seq !== rows[i - 1].seq + 1; });
    if (v.ok && first === 1 && !gap) {
      var full = v.checked - v.linked;
      say("hv-ok", "<strong>Consistent.</strong> " + v.checked + " messages, numbered 1 to " + last.seq + ". " +
        (v.linked ? full + " in the exported period recomputed from their text, and " + v.linked + " outside it linked by their hashes, " : "Every hash recomputed from the text, ") +
        "all matching.<br>Final chain hash: <code>" + esc(last.chain_hash) + "</code>" +
        "<br>Compare that hash and the count with the other parent's copy: a record cut short at the end still checks out on its own.");
    } else if (v.ok) {
      say("hv-ok", "<strong>Consistent from message " + first + ".</strong> " + v.checked + " messages checked, every hash matching." +
        (gap ? " Some numbers in the run are missing, so this is not the whole record." : " The record starts before message " + first + ", so the earlier part is not checked here."));
    } else {
      say("hv-bad", "<strong>Not consistent at message " + esc(v.firstBadSeq) + ".</strong> " + v.checked +
        " messages before it check out. From that message on, something was changed, removed or reordered after it was recorded.");
    }
  }

  form.addEventListener("submit", function (ev) { ev.preventDefault(); check(form.elements.record.value); });
  var file = document.getElementById("hv-file");
  if (file) file.addEventListener("change", function () {
    var f = file.files && file.files[0];
    if (f) f.text().then(function (t) { form.elements.record.value = t; check(t); });
  });
})();
