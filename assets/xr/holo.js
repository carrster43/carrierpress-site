/*
 * The holographic layer for the ordinary pages. No library, about 4 KB.
 *
 * 1. SURFACES. Book covers and app cards tilt toward the pointer and catch a
 *    moving foil sheen, like a hologram sticker turned in the light. Mouse and
 *    pen on hover; on a phone, while a finger is held on the card. With
 *    prefers-reduced-motion it does nothing at all.
 *
 * 2. THE DOOR. On a browser that can open a WebXR session (a Quest, Vision Pro
 *    or PC VR browser, or Android Chrome for the hologram), a small "View in VR"
 *    button appears that goes to /immersive/. Everywhere else nothing is drawn,
 *    so no visitor is shown a door that does not open.
 *
 * Added to the pages nav.py owns, by nav.py, so one file and one tag cover them.
 */
(function () {
  var SEL = ".book a.cover, .bestseller .lead-cover, .magnet-cover, .bk-cover, .ap-card";
  var still = matchMedia("(prefers-reduced-motion: reduce)").matches;

  var css =
    ".holo{transform-style:preserve-3d;will-change:transform}" +
    ".bk-cover.holo{line-height:0;border-radius:3px}" +
    ".holo-sheen{position:absolute;inset:0;pointer-events:none;border-radius:inherit;opacity:0;" +
    "transition:opacity .25s ease;mix-blend-mode:color-dodge;" +
    "background:" +
    "radial-gradient(circle at var(--hx,50%) var(--hy,50%),rgba(255,255,255,.55),transparent 42%)," +
    "linear-gradient(115deg,transparent 20%,rgba(255,0,170,.28) calc(var(--hx,50%) - 18%)," +
    "rgba(0,229,255,.30) var(--hx,50%),rgba(232,200,74,.32) calc(var(--hx,50%) + 18%),transparent 80%)}" +
    ".holo.is-holo .holo-sheen{opacity:.75}" +
    "@media (prefers-color-scheme:dark){.holo.is-holo .holo-sheen{opacity:.55}}" +
    // A card is text on paper, where color-dodge washes out to white: a plain
    // faint foil reads there instead.
    ".ap-card .holo-sheen{mix-blend-mode:normal}.ap-card.is-holo .holo-sheen{opacity:.2}" +
    ".xr-door{position:fixed;right:16px;bottom:16px;z-index:60;font:600 15px/1 -apple-system,'Segoe UI',Roboto,sans-serif;" +
    "padding:12px 18px;border-radius:999px;border:1px solid #e8c84a;background:rgba(13,14,24,.86);color:#f2d76b;" +
    "text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.35)}" +
    ".xr-door:hover,.xr-door:focus-visible{background:#e8c84a;color:#0d0e18}";

  function addStyle() {
    var s = document.createElement("style");
    s.textContent = css;
    document.head.appendChild(s);
  }

  function arm(el) {
    if (el.dataset.holo) return;
    el.dataset.holo = "1";
    el.classList.add("holo");
    if (getComputedStyle(el).position === "static") el.style.position = "relative";
    var sheen = document.createElement("span");
    sheen.className = "holo-sheen";
    sheen.setAttribute("aria-hidden", "true");
    el.appendChild(sheen);

    var frame = 0;
    function tilt(x, y) {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(function () {
        var r = el.getBoundingClientRect();
        var px = Math.min(1, Math.max(0, (x - r.left) / r.width));
        var py = Math.min(1, Math.max(0, (y - r.top) / r.height));
        // Cards are wide and covers are tall; a wide card tilts less so its
        // text stays readable while it moves.
        var max = r.width > r.height ? 4 : 10;
        el.style.setProperty("--hx", (px * 100).toFixed(1) + "%");
        el.style.setProperty("--hy", (py * 100).toFixed(1) + "%");
        el.style.transform =
          "perspective(800px) rotateX(" + ((0.5 - py) * max).toFixed(2) + "deg) rotateY(" +
          ((px - 0.5) * max).toFixed(2) + "deg) translateY(-4px)";
        el.classList.add("is-holo");
      });
    }
    function rest() {
      cancelAnimationFrame(frame);
      el.style.transform = "";
      el.classList.remove("is-holo");
    }
    el.addEventListener("pointermove", function (ev) {
      if (ev.pointerType === "touch" && !ev.isPrimary) return;
      tilt(ev.clientX, ev.clientY);
    });
    el.addEventListener("pointerleave", rest);
    el.addEventListener("pointercancel", rest);
    el.addEventListener("pointerup", function (ev) {
      if (ev.pointerType === "touch") rest();
    });
  }

  function surfaces() {
    if (still) return;
    var list = document.querySelectorAll(SEL);
    for (var i = 0; i < list.length; i++) arm(list[i]);
  }

  function door() {
    if (!navigator.xr || location.pathname.indexOf("/immersive/") === 0) return;
    var modes = ["immersive-vr", "immersive-ar"];
    Promise.all(modes.map(function (m) {
      return navigator.xr.isSessionSupported(m).catch(function () { return false; });
    })).then(function (ok) {
      if (!ok[0] && !ok[1]) return;
      var a = document.createElement("a");
      a.className = "xr-door";
      a.href = "/immersive/";
      a.textContent = ok[0] ? "View in VR" : "View as hologram";
      document.body.appendChild(a);
    });
  }

  function go() {
    addStyle();
    surfaces();
    door();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go);
  else go();
})();
