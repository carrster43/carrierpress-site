/* The home page search box (build.py search_html). Products come from the
   inline #ss-data JSON the generator writes, so the list cannot drift from the
   catalogue. Focus or click shows every product; typing narrows it. Each word
   typed must start a word in the title, the subline or the kind. */
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

  // Lowercase, accents and punctuation off, so "Mabuse," and "mabuse" match.
  function fold(s) {
    return s.toLowerCase().normalize("NFD").replace(/[^a-z0-9]+/g, " ");
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
  function render() {
    shown = match();
    active = -1;
    q.removeAttribute("aria-activedescendant");
    var html = "", last = null;
    shown.forEach(function (it) {
      if (it.k !== last) {
        html += '<li class="ss-group" role="presentation">' + esc(it.k === "App" ? "Apps" : it.k) + "</li>";
        last = it.k;
      }
      html += '<li class="ss-opt" role="option" id="' + it.id + '" aria-selected="false">' +
        '<a href="' + esc(it.u) + '" tabindex="-1">' +
        (it.i ? '<img src="' + esc(it.i) + '" alt="" loading="lazy" decoding="async" class="' +
          (it.k === "App" ? "ss-app" : "ss-cover") + '">' : '<span class="ss-noimg"></span>') +
        '<span class="ss-txt"><strong>' + esc(it.t) + "</strong>" +
        (it.s ? "<small>" + esc(it.s) + "</small>" : "") + "</span></a></li>";
    });
    if (!shown.length) html = '<li class="ss-empty" role="presentation">No match. Try a shorter word, or browse every shelf below.</li>';
    list.innerHTML = html;
    status.textContent = shown.length ? shown.length + (shown.length === 1 ? " product" : " products") : "No matches";
    open();
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
  function go(n) { var it = shown[n]; if (it) location.href = it.u; }

  q.addEventListener("focus", render);
  q.addEventListener("click", function () { if (list.hidden) render(); });
  q.addEventListener("input", render);
  q.addEventListener("keydown", function (ev) {
    if (ev.key === "ArrowDown") { ev.preventDefault(); if (list.hidden) render(); setActive(active + 1); }
    else if (ev.key === "ArrowUp") { ev.preventDefault(); if (list.hidden) render(); setActive(active - 1); }
    else if (ev.key === "Escape") { if (!list.hidden) { ev.preventDefault(); close(); } else { q.value = ""; } }
    else if (ev.key === "Enter") {
      if (active >= 0) { ev.preventDefault(); go(active); }
      else if (shown.length && q.value.trim()) { ev.preventDefault(); go(0); }
    }
  });
  list.addEventListener("mousedown", function (ev) { ev.preventDefault(); }); // keep focus while clicking
  document.addEventListener("click", function (ev) {
    if (!ev.target.closest || !ev.target.closest(".ss-form")) close();
  });
  q.addEventListener("blur", function () { setTimeout(function () {
    if (document.activeElement !== q) close();
  }, 120); });
})();
