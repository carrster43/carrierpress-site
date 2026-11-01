/*
 * The book in 3D, and on your table. Added by books.py (every book page) and
 * build.py (the homepage best seller and Top 10).
 *
 * THE GENERATORS MARK SLOTS, THIS FILE FILLS THEM. A slot is any element with
 * data-b3 plus the book's data-title, data-cover and, when the print edition's
 * page count is known, data-pages (so the spine is the real thickness):
 *
 *   data-b3="inline"  a book page. The slot holds .bk-cover; "See it in 3D"
 *                     swaps the flat cover for the book, in place.
 *   data-b3="dialog"  the homepage lead. "See it in 3D" opens the book in one
 *                     shared dialog over the page.
 *   data-b3="mini"    a Top 10 row. One small "3D" button, same dialog.
 *
 * Where make_book_panels.py has cut them from the print wrap, the slot also
 * carries data-trim, data-spine-in, data-spine and data-back: the book is then
 * its real trim and thickness, with its real spine and back.
 *
 * In the viewer: drag, or focus it and use the arrow keys, to turn the book.
 * Esc closes.
 *
 * SEE IT ON YOUR TABLE, only where the phone can place a model in the room:
 *   iPhone and iPad  AR Quick Look. The model is written as USDZ right here in
 *                    the browser from the same scene, at true size.
 *   Android Chrome   WebXR immersive-ar with hit-test: point at a table, tap.
 * Nobody is shown a door that does not open.
 *
 * NOTHING LOADS UNTIL IT IS ASKED FOR. three.js (vendored at /vendor/three/,
 * MIT, r180) loads on the first press, the USDZ writer only on an iPhone that
 * asks for the table. No third-party request. With no WebGL no button is drawn
 * and the page is exactly what it was. prefers-reduced-motion: the book does
 * not turn by itself.
 */
const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
const THREE_URL = "/vendor/three/three.module.min.js";
const USDZ_URL = "/vendor/three/addons/exporters/USDZExporter.js";

// A trade paperback is about 9 inches tall; the width follows the cover's own
// proportions. Metres, because AR is at true size. White paper is 0.002252 in
// a page on KDP's own spine calculator; the covers add a little.
const H = 0.2286;
const PAGE = 0.002252 * 0.0254;
const BOARDS = 0.0012;
const DEFAULT_DEPTH = 0.018;

function webgl() {
  try {
    const c = document.createElement("canvas");
    return !!(c.getContext("webgl2") || c.getContext("webgl"));
  } catch (_) {
    return false;
  }
}

const CSS = `
.b3-acts{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0}
.b3-btn{font:600 14px/1 var(--sans);padding:10px 14px;border-radius:999px;border:1px solid var(--line);
  background:var(--paper-2);color:var(--ink);cursor:pointer}
.b3-btn:hover,.b3-btn:focus-visible{border-color:var(--gold)}
.b3-btn[hidden]{display:none}
.b3-btn[aria-busy=true]{opacity:.6;cursor:progress}
.b3-mini{align-self:flex-start;margin-top:6px;font:700 12px/1 var(--sans);padding:6px 9px;border-radius:999px;
  border:1px solid var(--line);background:transparent;color:var(--ink-soft);cursor:pointer}
.b3-mini:hover,.b3-mini:focus-visible{border-color:var(--gold);color:var(--ink)}
.b3-stage{position:relative;width:100%;aspect-ratio:4/5;border-radius:6px;overflow:hidden;
  background:radial-gradient(circle at 50% 40%,var(--paper-2),transparent 75%)}
.b3-stage canvas{display:block;width:100%;height:100%;touch-action:none;cursor:grab;outline:none}
.b3-stage canvas:active{cursor:grabbing}
.b3-stage canvas:focus-visible{box-shadow:inset 0 0 0 2px var(--gold)}
.b3-hint{font:13px/1.4 var(--sans);color:var(--muted);margin:8px 0 0}
.b3-dlg{width:min(420px,calc(100vw - 32px));max-height:calc(100dvh - 32px);overflow:auto;padding:18px;
  border:1px solid var(--line);border-radius:12px;background:var(--paper);color:var(--ink)}
.b3-dlg::backdrop{background:rgba(7,8,15,.72)}
.b3-dlg h2{font:400 1.3rem/1.25 var(--serif);margin:0 0 12px;padding-right:40px}
.b3-x{position:absolute;top:12px;right:12px;width:36px;height:36px;border-radius:50%;
  border:1px solid var(--line);background:var(--paper-2);color:var(--ink);font:20px/1 var(--sans);cursor:pointer}
.b3-x:hover,.b3-x:focus-visible{border-color:var(--gold)}
.b3-dlg .b3-stage{max-width:none}
.b3-ar{position:fixed;inset:0;display:none;font:15px/1.4 var(--sans)}
.b3-ar p{position:absolute;left:16px;right:16px;top:16px;margin:0;padding:10px 14px;border-radius:8px;
  background:rgba(7,8,15,.75);color:#ece8dd;text-align:center}
.b3-ar button{position:absolute;left:50%;bottom:28px;transform:translateX(-50%);font:600 15px/1 var(--sans);
  padding:12px 22px;border-radius:999px;border:0;background:#e8c84a;color:#07080f}
@media(max-width:700px){.bk-fig .b3-stage{max-width:300px}}
`;

function button(text, cls = "b3-btn") {
  const b = document.createElement("button");
  b.type = "button";
  b.className = cls;
  b.textContent = text;
  return b;
}

async function busy(btn, fn) {
  if (btn.getAttribute("aria-busy")) return;
  btn.setAttribute("aria-busy", "true");
  try {
    await fn();
  } catch (err) {
    console.warn("book3d:", err);
  } finally {
    btn.removeAttribute("aria-busy");
  }
}

let threeP = null;
const loadThree = () => (threeP = threeP || import(THREE_URL));

/** Which "on your table" route this browser has: "quicklook", "webxr" or null. */
const arRoute = (() => {
  if (document.createElement("a").relList.supports("ar")) return Promise.resolve("quicklook");
  if (navigator.xr && navigator.xr.isSessionSupported) {
    return navigator.xr.isSessionSupported("immersive-ar").then((ok) => (ok ? "webxr" : null), () => null);
  }
  return Promise.resolve(null);
})();

function tableButton(book) {
  const b = button("See it on your table");
  b.hidden = true;
  arRoute.then((route) => {
    if (!route) return;
    b.hidden = false;
    b.addEventListener("click", () => busy(b, () => (route === "quicklook" ? quickLookOpen(book) : webxrPlace(book))));
  });
  return b;
}

/** The book a slot describes. */
function bookOf(slot) {
  const ds = slot.dataset;
  const pages = parseInt(ds.pages, 10);
  const trim = (ds.trim || "").split("x").map(Number);
  const spineIn = parseFloat(ds.spineIn);
  return {
    title: ds.title || "this book",
    cover: ds.cover,
    spine: ds.spine || null,
    back: ds.back || null,
    h: trim[1] > 0 ? trim[1] * 0.0254 : H,
    depth: spineIn > 0 ? spineIn * 0.0254 : pages > 0 ? pages * PAGE + BOARDS : DEFAULT_DEPTH,
  };
}

/** The cover as a loaded image. Reuses one already on the page when it has
 *  loaded. Not img.decode(): that can wait indefinitely in a tab that is not
 *  painting. */
function image(src) {
  const onPage = [...document.images].find((i) => i.complete && i.naturalWidth && i.src.endsWith(src));
  if (onPage) return Promise.resolve(onPage);
  return new Promise((ok, fail) => {
    const img = new Image();
    img.onload = () => ok(img);
    img.onerror = fail;
    img.src = src;
  });
}

/** Cover, and the wrap's spine and back where they exist. A spine or back
 *  that fails to load falls back to the drawn one; the cover must load. */
async function artOf(book) {
  const opt = (src) => (src ? image(src).catch(() => null) : Promise.resolve(null));
  const [cover, spine, back] = await Promise.all([image(book.cover), opt(book.spine), opt(book.back)]);
  return { cover, spine, back };
}

// ---------------------------------------------------------------- the book

/** The cover's own colour, from a strip down its left edge, for spine and back. */
function spineColour(img) {
  const c = document.createElement("canvas");
  c.width = 8;
  c.height = 64;
  const g = c.getContext("2d");
  g.drawImage(img, 0, 0, img.naturalWidth * 0.06, img.naturalHeight, 0, 0, 8, 64);
  const d = g.getImageData(0, 0, 8, 64).data;
  let r = 0, gr = 0, b = 0;
  for (let i = 0; i < d.length; i += 4) { r += d[i]; gr += d[i + 1]; b += d[i + 2]; }
  const n = d.length / 4;
  return [r / n, gr / n, b / n].map(Math.round);
}

function canvasOf(w, h, paint) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  paint(c.getContext("2d"), w, h);
  return c;
}

function pages(w, h, vertical) {
  return canvasOf(w, h, (g) => {
    g.fillStyle = "#f3ecdc";
    g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(120,104,80,.18)";
    const n = vertical ? w : h;
    for (let i = 0; i < n; i += 3) {
      if (vertical) g.fillRect(i, 0, 1, h);
      else g.fillRect(0, i, w, 1);
    }
  });
}

function buildBook(THREE, art, book) {
  const img = art.cover;
  const H = book.h;
  const W = H * (img.naturalWidth / img.naturalHeight);
  const D = book.depth;
  const [r, g, b] = spineColour(img);
  const base = `rgb(${r},${g},${b})`;
  const ink = 0.299 * r + 0.587 * g + 0.114 * b > 150 ? "#151a33" : "#f6f1e4";

  // Spine text reads top to bottom, as on a book printed in the US. The canvas
  // keeps the spine's proportions so a thin book gets smaller type.
  const sw = Math.max(32, Math.round(1000 * D / H));
  const spine = art.spine || canvasOf(sw, 1000, (c, w, h) => {
    c.fillStyle = base;
    c.fillRect(0, 0, w, h);
    c.save();
    c.translate(w / 2, 0);
    c.rotate(Math.PI / 2);
    c.fillStyle = ink;
    c.textBaseline = "middle";
    let px = Math.min(40, Math.round(w * 0.55));
    c.font = `${px}px Georgia,serif`;
    const room = h * 0.72;
    while (c.measureText(book.title).width > room && px > 10) c.font = `${(px -= 2)}px Georgia,serif`;
    c.fillText(book.title, h * 0.05, 0);
    c.font = `${Math.min(22, Math.round(w * 0.32))}px Georgia,serif`;
    c.textAlign = "right";
    c.fillText("Carrier Press", h * 0.96, 0);
    c.restore();
  });
  const back = art.back || canvasOf(64, 96, (c, w, h) => {
    c.fillStyle = base;
    c.fillRect(0, 0, w, h);
    c.fillStyle = "rgba(0,0,0,.12)";
    c.fillRect(0, 0, w, h);
  });

  const tex = (src) => {
    const t = src instanceof HTMLImageElement ? new THREE.Texture(src) : new THREE.CanvasTexture(src);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 4;
    t.needsUpdate = true;
    return t;
  };
  const mat = (src, rough) => new THREE.MeshStandardMaterial({ map: tex(src), roughness: rough, metalness: 0 });

  // Six faces, one material each, because the USDZ writer takes one per mesh.
  const group = new THREE.Group();
  const face = (w, h, m, place) => {
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m);
    place(mesh);
    group.add(mesh);
  };
  face(W, H, mat(img, 0.55), (m) => { m.position.z = D / 2; });
  face(W, H, mat(back, 0.6), (m) => { m.rotation.y = Math.PI; m.position.z = -D / 2; });
  face(D, H, mat(spine, 0.6), (m) => { m.rotation.y = -Math.PI / 2; m.position.x = -W / 2; });
  face(D, H, mat(pages(64, 512, true), 0.9), (m) => { m.rotation.y = Math.PI / 2; m.position.x = W / 2; });
  const edge = mat(pages(256, 64, false), 0.9);
  face(W, D, edge, (m) => { m.rotation.x = -Math.PI / 2; m.position.y = H / 2; });
  face(W, D, edge, (m) => { m.rotation.x = Math.PI / 2; m.position.y = -H / 2; });
  group.userData.size = { W, H, D };
  return group;
}

function lights(THREE, scene) {
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8170, 1.6));
  const key = new THREE.DirectionalLight(0xffffff, 1.8);
  key.position.set(0.6, 0.8, 1);
  scene.add(key);
}

function dispose(root) {
  root.traverse((o) => {
    if (o.geometry) o.geometry.dispose();
    if (o.material) {
      if (o.material.map) o.material.map.dispose();
      o.material.dispose();
    }
  });
}

// -------------------------------------------------------------- the viewer

/** Render the turnable book into `host` (stage + hint appended before
 *  `before`). Returns { close }. Esc on the canvas calls onEscape. */
async function mountViewer(book, host, before, onEscape) {
  const THREE = await loadThree();
  const art = await artOf(book);

  const stage = document.createElement("div");
  stage.className = "b3-stage";
  const canvas = document.createElement("canvas");
  canvas.tabIndex = 0;
  canvas.setAttribute("role", "img");
  canvas.setAttribute("aria-label", `${book.title}, shown as a book you can turn. Drag, or use the arrow keys.`);
  stage.appendChild(canvas);
  const hint = document.createElement("p");
  hint.className = "b3-hint";
  hint.textContent = "Drag to turn the book. Arrow keys work too.";
  host.insertBefore(stage, before);
  host.insertBefore(hint, before);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  lights(THREE, scene);
  const model = buildBook(THREE, art, book);
  scene.add(model);
  const camera = new THREE.PerspectiveCamera(30, 4 / 5, 0.01, 10);
  camera.position.set(0, 0, 0.53);

  const size = () => {
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  const ro = new ResizeObserver(size);
  ro.observe(stage);
  size();

  // Turn: yaw around the spine axis, a little pitch. Start angled so the
  // spine and the page edges both show, which is what says "object".
  let yaw = -0.55, pitch = 0.12, spin = !still, drag = null;
  canvas.addEventListener("pointerdown", (ev) => {
    drag = { x: ev.clientX, y: ev.clientY, yaw, pitch };
    spin = false;
    canvas.setPointerCapture(ev.pointerId);
  });
  canvas.addEventListener("pointermove", (ev) => {
    if (!drag) return;
    yaw = drag.yaw + (ev.clientX - drag.x) * 0.012;
    pitch = Math.max(-0.7, Math.min(0.7, drag.pitch + (ev.clientY - drag.y) * 0.008));
  });
  const end = () => { drag = null; };
  canvas.addEventListener("pointerup", end);
  canvas.addEventListener("pointercancel", end);
  canvas.addEventListener("keydown", (ev) => {
    const k = { ArrowLeft: [-0.2, 0], ArrowRight: [0.2, 0], ArrowUp: [0, -0.1], ArrowDown: [0, 0.1] }[ev.key];
    if (k) {
      ev.preventDefault();
      spin = false;
      yaw += k[0];
      pitch = Math.max(-0.7, Math.min(0.7, pitch + k[1]));
    } else if (ev.key === "Escape" && onEscape) {
      onEscape();
    }
  });

  let last = performance.now();
  renderer.setAnimationLoop((now) => {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    if (spin) yaw += dt * 0.5;
    model.rotation.set(pitch, yaw, 0);
    renderer.render(scene, camera);
  });
  canvas.focus({ preventScroll: true });

  return {
    close() {
      renderer.setAnimationLoop(null);
      ro.disconnect();
      dispose(model);
      renderer.dispose();
      stage.remove();
      hint.remove();
    },
  };
}

// ----------------------------------------------- slot: inline (book pages)

function setupInline(slot) {
  const book = bookOf(slot);
  const flat = slot.querySelector(".bk-cover");
  const acts = document.createElement("div");
  acts.className = "b3-acts";
  const see = button("See it in 3D");
  acts.append(see, tableButton(book));
  slot.appendChild(acts);
  see.addEventListener("pointerenter", loadThree, { once: true });
  see.addEventListener("focus", loadThree, { once: true });

  let viewer = null;
  const close = () => {
    viewer.close();
    viewer = null;
    flat.hidden = false;
    see.textContent = "See it in 3D";
    see.focus();
  };
  see.addEventListener("click", () => {
    if (viewer) return close();
    busy(see, async () => {
      viewer = await mountViewer(book, slot, flat, close);
      flat.hidden = true;
      see.textContent = "Back to the cover";
    });
  });
}

// ----------------------------------------- slots: dialog and mini (home)

let dlg = null;

/** One dialog for the whole page, built on first use. */
function dialog() {
  if (dlg) return dlg;
  const el = document.createElement("dialog");
  el.className = "b3-dlg";
  el.setAttribute("aria-labelledby", "b3-dlg-h");
  const h = document.createElement("h2");
  h.id = "b3-dlg-h";
  const x = button("×", "b3-x");
  x.setAttribute("aria-label", "Close");
  const acts = document.createElement("div");
  acts.className = "b3-acts";
  el.append(h, x, acts);
  document.body.appendChild(el);
  dlg = { el, h, acts, viewer: null, opener: null };
  x.addEventListener("click", () => el.close());
  // A click on the backdrop lands on the dialog element itself.
  el.addEventListener("click", (ev) => { if (ev.target === el) el.close(); });
  el.addEventListener("close", () => {
    if (dlg.viewer) dlg.viewer.close();
    dlg.viewer = null;
    if (dlg.opener) dlg.opener.focus();
  });
  return dlg;
}

async function openDialog(book, opener) {
  const d = dialog();
  d.opener = opener;
  d.h.textContent = book.title;
  d.acts.replaceChildren(tableButton(book));
  // three.js can take a moment on the first open; say so rather than show nothing.
  const wait = document.createElement("p");
  wait.className = "b3-hint";
  wait.textContent = "Opening the book.";
  d.el.insertBefore(wait, d.acts);
  d.el.showModal();
  // Esc is the dialog's own cancel, so the viewer needs no handler for it.
  const v = await mountViewer(book, d.el, d.acts, null).finally(() => wait.remove());
  // Closed while three.js was still loading: do not leave a render loop behind.
  if (d.el.open) d.viewer = v;
  else v.close();
}

function setupDialog(slot) {
  const book = bookOf(slot);
  const see = button("See it in 3D");
  slot.classList.add("b3-acts");
  slot.append(see, tableButton(book));
  see.addEventListener("pointerenter", loadThree, { once: true });
  see.addEventListener("focus", loadThree, { once: true });
  see.addEventListener("click", () => busy(see, () => openDialog(book, see)));
}

function setupMini(slot) {
  const book = bookOf(slot);
  const see = button("3D", "b3-mini");
  see.setAttribute("aria-label", `See ${book.title} in 3D`);
  slot.replaceWith(see);
  see.addEventListener("pointerenter", loadThree, { once: true });
  see.addEventListener("click", () => busy(see, () => openDialog(book, see)));
}

// ------------------------------------------------------- on your table: iOS

async function quickLookOpen(book) {
  const [THREE, { USDZExporter }] = await Promise.all([loadThree(), import(USDZ_URL)]);
  const scene = new THREE.Scene();
  const model = buildBook(THREE, await artOf(book), book);
  // Standing on the table, cover toward the visitor.
  model.position.y = model.userData.size.H / 2;
  scene.add(model);
  const bytes = await new USDZExporter().parseAsync(scene, {
    quickLookCompatible: true,
    ar: { anchoring: { type: "plane" }, planeAnchoring: { alignment: "horizontal" } },
  });
  dispose(model);
  const url = URL.createObjectURL(new Blob([bytes], { type: "model/vnd.usdz+zip" }));
  const a = document.createElement("a");
  a.rel = "ar";
  // True size is the point, so Quick Look is asked not to let it be pinched.
  a.href = url + "#allowsContentScaling=0";
  a.appendChild(document.createElement("img"));
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}

// --------------------------------------------------- on your table: Android

async function webxrPlace(book) {
  const THREE = await loadThree();
  const art = await artOf(book);

  const overlay = document.createElement("div");
  overlay.className = "b3-ar";
  const say = document.createElement("p");
  say.textContent = "Point the camera at a table, then tap to set the book down.";
  const done = button("Done");
  overlay.append(say, done);
  document.body.appendChild(overlay);
  // A tap on the overlay's own button is not a tap on the table.
  overlay.addEventListener("beforexrselect", (ev) => ev.preventDefault());

  const session = await navigator.xr.requestSession("immersive-ar", {
    requiredFeatures: ["hit-test"],
    optionalFeatures: ["dom-overlay"],
    domOverlay: { root: overlay },
  });
  overlay.style.display = "block";

  const canvas = document.createElement("canvas");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.xr.enabled = true;
  renderer.xr.setReferenceSpaceType("local");
  const scene = new THREE.Scene();
  lights(THREE, scene);
  const camera = new THREE.PerspectiveCamera();

  const model = buildBook(THREE, art, book);
  const placed = new THREE.Group();
  model.position.y = model.userData.size.H / 2;
  placed.add(model);
  placed.visible = false;
  scene.add(placed);

  const reticle = new THREE.Mesh(
    new THREE.RingGeometry(0.05, 0.065, 40).rotateX(-Math.PI / 2),
    new THREE.MeshBasicMaterial({ color: 0xe8c84a })
  );
  reticle.matrixAutoUpdate = false;
  reticle.visible = false;
  scene.add(reticle);

  await renderer.xr.setSession(session);
  const viewerSpace = await session.requestReferenceSpace("viewer");
  const source = await session.requestHitTestSource({ space: viewerSpace });

  session.addEventListener("select", () => {
    if (!reticle.visible) return;
    reticle.matrix.decompose(placed.position, placed.quaternion, placed.scale);
    // Face the visitor: turn about the vertical toward the camera.
    const cam = renderer.xr.getCamera();
    const dx = cam.position.x - placed.position.x, dz = cam.position.z - placed.position.z;
    placed.quaternion.setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.atan2(dx, dz));
    placed.visible = true;
    say.textContent = "Tap somewhere else to move it.";
  });
  done.addEventListener("click", () => session.end());

  renderer.setAnimationLoop((_, frame) => {
    if (frame) {
      const hit = frame.getHitTestResults(source)[0];
      const pose = hit && hit.getPose(renderer.xr.getReferenceSpace());
      reticle.visible = !!pose;
      if (pose) reticle.matrix.fromArray(pose.transform.matrix);
    }
    renderer.render(scene, camera);
  });

  await new Promise((resolve) => session.addEventListener("end", resolve, { once: true }));
  renderer.setAnimationLoop(null);
  source.cancel();
  dispose(scene);
  renderer.dispose();
  overlay.remove();
}

// ------------------------------------------------------------------- start

const slots = [...document.querySelectorAll("[data-b3]")];
if (slots.length && webgl()) {
  const style = document.createElement("style");
  style.textContent = CSS;
  document.head.appendChild(style);
  const setup = { inline: setupInline, dialog: setupDialog, mini: setupMini };
  for (const slot of slots) {
    const fn = setup[slot.dataset.b3];
    if (fn && slot.dataset.cover) fn(slot);
  }
}
