/* The home page search box (build.py search_html). Two sources:
   1. Our books and apps, from the inline #ss-data JSON the generator writes, so
      the list cannot drift from the catalogue. Focus or click shows every
      product; typing narrows it. Each word typed must start a word in the title,
      the subline or the kind.
   2. Classics we can make for you (author 2026-11-23): public domain books we
      do not print yet, from the static index under /pd/. It loads only once
      someone types, and only the pieces the typed words need. A click opens
      /request/?b=<book number>&r=<rank>. */
(function () {
  var q = document.getElementById("ss-q"), list = document.getElementById("ss-list"),
      status = document.getElementById("ss-status"), dataEl = document.getElementById("ss-data");
  if (!q || !list || !dataEl) return;
  var items;
  try { items = JSON.parse(dataEl.textContent); } catch (err) { return; }
  items.forEach(function (it, i) {
    it.id = "ss-o" + i;
    it.hay = " " + fold(it.t + " " + it.s + " " + it.k + " " + (it.x || ""));
    delete it.x;
  });
  var shown = [], active = -1;

  /* ---------- suggestions (author 2026-11-23, "put suggestions in the search bar") ----------
     Each one is checked to return results (our own books, or classics, or both).
     The empty box rotates them as its hint; focusing it lists the first few. */
  // "True crime" sits in the first five on purpose: it leads to our own American
  // Firsts (catalog.json shelf "search" words), the books we sell today.
  var SUGGEST = ["World War I", "True crime", "Sherlock Holmes", "Ghost stories", "Civil War",
                 "Jane Austen", "Pirates", "Mark Twain", "Ancient Egypt", "Murder mystery"];
  var hintAt = -1;
  setInterval(function () {
    if (document.activeElement === q || q.value) return;
    hintAt = (hintAt + 1) % SUGGEST.length;
    q.placeholder = "Try “" + SUGGEST[hintAt] + "”";
  }, 3200);

  // Lowercase, accents and punctuation off, so "Mabuse," and "mabuse" match.
  // Must agree with fold() in the index builder.
  function fold(s) {
    return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, " ");
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function match() {
    // Each word typed must start a word somewhere: "king" finds The King in
    // Yellow, not "Making Things".
    var words = fold(q.value).split(" ").filter(Boolean);
    return items.filter(function (it) {
      return words.every(function (w) { return it.hay.indexOf(" " + w) !== -1; });
    });
  }

  /* ---------- classics (public domain index) ---------- */
  var PD_MAX = 8, PD_SHARD = 500;
  // Words the index leaves out (the index builder's stop list), plus one letter words, so
  // "World War I" asks only for "world" and "war".
  var STOP = {};
  ("a an and the of in on to for by with from at as or its it is be are was were this " +
   "that these those into over under upon about after before than then de la le du des et en")
    .split(" ").forEach(function (w) { STOP[w] = 1; });
  var wordFiles = {}, recFiles = {}, decoded = {};
  var pd = { query: null, items: [], pending: false }, timer = null;

  function getJSON(cache, url) {
    if (!cache[url]) cache[url] = fetch(url).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).catch(function (err) { delete cache[url]; throw err; });
    return cache[url];
  }
  // Every rank whose book carries a word starting with `w`, sorted, no repeats.
  function ranksFor(shard, w) {
    if (decoded[w]) return decoded[w];
    var out = [];
    Object.keys(shard).forEach(function (tok) {
      if (tok.lastIndexOf(w, 0) !== 0) return;
      var prev = 0, d = shard[tok];
      for (var i = 0; i < d.length; i++) { prev += d[i]; out.push(prev); }
    });
    out.sort(function (a, b) { return a - b; });
    return (decoded[w] = out.filter(function (x, i) { return i === 0 || x !== out[i - 1]; }));
  }
  // Ranks found in every list, smallest (most read) first, at most PD_MAX.
  function intersect(lists) {
    lists.sort(function (a, b) { return a.length - b.length; });
    var sets = lists.slice(1).map(function (l) { var s = {}; l.forEach(function (x) { s[x] = 1; }); return s; });
    var hits = [];
    for (var i = 0; i < lists[0].length && hits.length < PD_MAX; i++) {
      var x = lists[0][i];
      if (sets.every(function (s) { return s[x]; })) hits.push(x);
    }
    return hits;
  }
  // Names the index cannot spell: the "I" in World War I is one letter, so it is
  // dropped and "world war" alone also finds The War of the Worlds. The books
  // themselves are filed under the years, so search on those.
  var ALIAS = [[/\b(world war ii|ww ?ii|ww ?2|second world war)\b/g, "world war 1939"],
               [/\b(world war i|ww ?i|ww ?1|first world war|great war)\b/g, "world war 1914"]];
  function pdSearch(text) {
    var f = " " + fold(text).trim() + " ";
    ALIAS.forEach(function (a) { f = f.replace(a[0], a[1]); });
    var words = f.split(" ").filter(function (w) { return w.length >= 2 && !STOP[w]; });
    if (!words.length) return Promise.resolve([]);
    return Promise.all(words.map(function (w) {
      return getJSON(wordFiles, "/pd/w/" + w.slice(0, 2) + ".json")
        .then(function (shard) { return ranksFor(shard, w); }, function () { return []; });
    })).then(function (lists) {
      var ranks = intersect(lists), need = {};
      ranks.forEach(function (r) { need[Math.floor(r / PD_SHARD)] = 1; });
      return Promise.all(Object.keys(need).map(function (n) {
        return getJSON(recFiles, "/pd/r/" + n + ".json").then(function (recs) { return [n, recs]; });
      })).then(function (pairs) {
        var byShard = {};
        pairs.forEach(function (p) { byShard[p[0]] = p[1]; });
        return ranks.map(function (r, i) {
          var rec = byShard[Math.floor(r / PD_SHARD)][r % PD_SHARD];
          return { id: "ss-p" + i, k: "Classic", t: rec[1], s: rec[2],
                   u: "/request/?b=" + rec[0] + "&r=" + r };
        });
      });
    });
  }
  function queuePd() {
    var text = q.value.trim();
    if (text === pd.query) return;
    clearTimeout(timer);
    pd.query = text; pd.items = [];
    if (fold(text).replace(/ /g, "").length < 3) { pd.pending = false; return; }
    pd.pending = true;
    timer = setTimeout(function () {
      pdSearch(text).then(function (found) {
        if (q.value.trim() !== text) return;              // the visitor kept typing
        pd.items = found; pd.pending = false; render(true);
      }, function () {
        if (q.value.trim() !== text) return;
        pd.items = []; pd.pending = false; render(true);  // index unreachable: our own results stand alone
      });
    }, 180);
  }

  /* ---------- autofill ----------
     Typing at the end of the box completes it in place, selected, like a browser
     address bar: keep typing to replace it, Backspace to drop it, Tab or the right
     arrow to take it. A suggestion or one of our titles that starts with what was
     typed wins; otherwise the last word completes to the commonest word in the
     classics index that starts with it. */
  function completion(typed) {
    var low = typed.toLowerCase();
    if (low.replace(/\s/g, "").length < 2) return Promise.resolve(null);
    var phrase = SUGGEST.concat(items.map(function (it) { return it.t; })).filter(function (p) {
      return p.length > typed.length && p.toLowerCase().lastIndexOf(low, 0) === 0;
    })[0];
    if (phrase) return Promise.resolve(phrase);
    if (!/[a-z0-9]$/i.test(typed)) return Promise.resolve(null);
    var words = fold(typed).trim().split(" "), w = words[words.length - 1];
    if (w.length < 2) return Promise.resolve(null);
    return getJSON(wordFiles, "/pd/w/" + w.slice(0, 2) + ".json").then(function (shard) {
      var best = null, most = 20;                    // ignore words fewer than 20 books carry
      Object.keys(shard).forEach(function (tok) {
        if (tok.length > w.length && tok.lastIndexOf(w, 0) === 0 && shard[tok].length > most) {
          best = tok; most = shard[tok].length;
        }
      });
      return best ? typed + best.slice(w.length) : null;
    }, function () { return null; });
  }
  function autofill(ev) {
    if (!ev || ev.inputType !== "insertText") return;   // never on delete or paste
    var typed = q.value;
    if (q.selectionStart !== typed.length) return;
    completion(typed).then(function (full) {
      if (!full || q.value !== typed || q.selectionStart !== typed.length) return;
      // A title or suggestion shows in its own casing ("The King in Yellow");
      // a single word completion is built on what was typed, so it keeps theirs.
      q.value = full;
      q.setSelectionRange(typed.length, q.value.length);
      render();
    });
  }

  function option(it) {
    if (it.fill) {
      return '<li class="ss-opt ss-sug" role="option" id="' + it.id + '" aria-selected="false">' +
        '<a href="/?q=' + encodeURIComponent(it.fill) + '" tabindex="-1">' +
        '<svg class="ss-sugico" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">' +
        '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/>' +
        '<path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' +
        '<span class="ss-txt"><strong>' + esc(it.fill) + "</strong></span></a></li>";
    }
    var img = it.k === "Classic" ? '<span class="ss-pdcover" aria-hidden="true"></span>'
      : it.i ? '<img src="' + esc(it.i) + '" alt="" loading="lazy" decoding="async" class="' +
          (it.k === "App" ? "ss-app" : "ss-cover") + '">' : '<span class="ss-noimg"></span>';
    return '<li class="ss-opt" role="option" id="' + it.id + '" aria-selected="false">' +
      '<a href="' + esc(it.u) + '" tabindex="-1">' + img +
      '<span class="ss-txt"><strong>' + esc(it.t) + "</strong>" +
      (it.s ? "<small>" + esc(it.s) + "</small>" : "") + "</span></a></li>";
  }
  function render(fromPd) {
    if (!fromPd) queuePd();
    var local = match();
    // An empty box leads with a few suggested searches, then every product.
    var sugs = q.value.trim() ? [] : SUGGEST.slice(0, 5).map(function (s, i) {
      return { id: "ss-s" + i, fill: s, k: "Try" };
    });
    shown = sugs.concat(local, pd.items);
    var keep = fromPd && active >= 0 ? active : -1;
    active = -1;
    q.removeAttribute("aria-activedescendant");
    var html = "", last = null;
    if (sugs.length) {
      html += '<li class="ss-group" role="presentation">Try a search</li>';
      sugs.forEach(function (it) { html += option(it); });
    }
    local.forEach(function (it) {
      if (it.k !== last) {
        html += '<li class="ss-group" role="presentation">' + esc(it.k === "App" ? "Apps" : it.k) + "</li>";
        last = it.k;
      }
      html += option(it);
    });
    if (pd.items.length) {
      html += '<li class="ss-group" role="presentation">Classics we can make for you</li>';
      pd.items.forEach(function (it) { html += option(it); });
      html += '<li class="ss-note" role="presentation">Not in print with us yet. Pick one and we will ' +
        "email you the day our edition is out.</li>";
    } else if (pd.pending) {
      html += '<li class="ss-note" role="presentation">Searching every classic…</li>';
    }
    if (!shown.length && !pd.pending) html = '<li class="ss-empty" role="presentation">No match. Try a shorter word, or browse every shelf below.</li>';
    list.innerHTML = html;
    var n = local.length, c = pd.items.length;
    status.textContent = (n || c)
      ? [n ? n + (n === 1 ? " product" : " products") : "", c ? c + (c === 1 ? " classic" : " classics") : ""]
          .filter(Boolean).join(", ")
      : pd.pending ? "" : "No matches";
    open();
    if (keep >= 0) setActive(keep);
  }
  function open() { list.hidden = false; q.setAttribute("aria-expanded", "true"); }
  function close() {
    list.hidden = true; q.setAttribute("aria-expanded", "false");
    q.removeAttribute("aria-activedescendant"); active = -1;
  }
  function setActive(n) {
    var opts = list.querySelectorAll(".ss-opt");
    if (!opts.length) return;
    if (active >= 0 && opts[active]) opts[active].setAttribute("aria-selected", "false");
    active = (n + opts.length) % opts.length;
    var el = opts[active];
    el.setAttribute("aria-selected", "true");
    q.setAttribute("aria-activedescendant", el.id);
    el.scrollIntoView({ block: "nearest" });
  }
  function fill(text) { q.value = text; q.focus(); q.setSelectionRange(text.length, text.length); render(); }
  function go(n) {
    var it = shown[n];
    if (!it) return;
    if (it.fill) fill(it.fill); else location.href = it.u;
  }

  q.addEventListener("focus", function () { render(); });
  q.addEventListener("click", function () { if (list.hidden) render(); });
  q.addEventListener("input", function (ev) { render(); autofill(ev); });
  q.addEventListener("keydown", function (ev) {
    var filled = q.selectionEnd > q.selectionStart && q.selectionEnd === q.value.length;
    if (ev.key === "Tab" && filled && !ev.shiftKey) {   // take the autofill
      ev.preventDefault(); q.setSelectionRange(q.value.length, q.value.length);
    }
    else if (ev.key === "ArrowDown") { ev.preventDefault(); if (list.hidden) render(); setActive(active + 1); }
    else if (ev.key === "ArrowUp") { ev.preventDefault(); if (list.hidden) render(); setActive(active - 1); }
    else if (ev.key === "Escape") { if (!list.hidden) { ev.preventDefault(); close(); } else { q.value = ""; } }
    else if (ev.key === "Enter") {
      if (active >= 0) { ev.preventDefault(); go(active); }
      else if (shown.length && q.value.trim()) { ev.preventDefault(); go(0); }
    }
  });
  list.addEventListener("mousedown", function (ev) { ev.preventDefault(); }); // keep focus while clicking
  list.addEventListener("click", function (ev) {      // a suggestion fills the box, it does not navigate
    var li = ev.target.closest && ev.target.closest(".ss-sug");
    if (!li) return;
    ev.preventDefault();
    var it = shown.filter(function (s) { return s.id === li.id; })[0];
    if (it) fill(it.fill);
  });
  // /?q=... (a suggestion link opened in a new tab, or a shared search) prefills the box.
  var pre = new URLSearchParams(location.search).get("q");
  if (pre) { q.value = pre.slice(0, 80); }
  document.addEventListener("click", function (ev) {
    if (!ev.target.closest || !ev.target.closest(".ss-form")) close();
  });
  q.addEventListener("blur", function () { setTimeout(function () {
    if (document.activeElement !== q) close();
  }, 120); });
})();
