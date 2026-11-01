/*
 * The book in 3D, on every /books/<slug>/ page. Added by books.py.
 *
 * 1. SEE IT IN 3D. A button under the cover swaps the flat cover for the book
 *    as an object: the real cover on the front, a spine and back in the cover's
 *    own colour, page edges. Drag, or focus it and use the arrow keys, to turn
 *    it. Esc or "Back to the cover" puts the picture back.
 *
 * 2. SEE IT ON YOUR TABLE. Where the phone can place a model in the room:
 *      iPhone and iPad  AR Quick Look. The model is written as USDZ right here
 *                       in the browser from the same scene, at true size.
 *      Android Chrome   WebXR immersive-ar with hit-test: point at a table,
 *                       tap, and the book stands there.
 *    The button appears only where one of those exists, so nobody is shown a
 *    door that does not open.
 *
 * NOTHING LOADS UNTIL IT IS ASKED FOR. This file is small; three.js (vendored
 * at /vendor/three/, MIT, r180) loads on the first press, and the USDZ writer
 * only on an iPhone that asks for the table. No third-party request. With no
 * WebGL no button is drawn and the page is exactly what it was.
 *
 * prefers-reduced-motion: the book does not turn by itself.
 */
const fig = document.querySelector(".bk-fig");
const cover = fig && fig.querySelector(".bk-cover img");
const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
const THREE_URL = "/vendor/three/three.module.min.js";
const USDZ_URL = "/vendor/three/addons/exporters/USDZExporter.js";

// A trade paperback is about 9 inches tall; the width follows the cover's
// own proportions. Metres, because AR is at true size.
const H = 0.2286;
const DEPTH = 0.022;

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
.b3-stage{position:relative;width:100%;aspect-ratio:4/5;border-radius:6px;overflow:hidden;
  background:radial-gradient(circle at 50% 40%,var(--paper-2),transparent 75%)}
.b3-stage canvas{display:block;width:100%;height:100%;touch-action:none;cursor:grab;outline:none}
.b3-stage canvas:active{cursor:grabbing}
.b3-stage canvas:focus-visible{box-shadow:inset 0 0 0 2px var(--gold)}
.b3-hint{font:13px/1.4 var(--sans);color:var(--muted);margin:8px 0 0}
.b3-ar{position:fixed;inset:0;display:none;font:15px/1.4 var(--sans)}
.b3-ar p{position:absolute;left:16px;right:16px;top:16px;margin:0;padding:10px 14px;border-radius:8px;
  background:rgba(7,8,15,.75);color:#ece8dd;text-align:center}
.b3-ar button{position:absolute;left:50%;bottom:28px;transform:translateX(-50%);font:600 15px/1 var(--sans);
  padding:12px 22px;border-radius:999px;border:0;background:#e8c84a;color:#07080f}
@media(max-width:700px){.b3-stage{max-width:300px}}
`;

function button(text) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "b3-btn";
  b.textContent = text;
  return b;
}

function title() {
  const h = document.querySelector(".bk h1");
  return h ? h.textContent.trim() : "this book";
}

if (fig && cover && webgl() && cover.getAttribute("width") !== cover.getAttribute("height")) {
  const style = document.createElement("style");
  style.textContent = CSS;
  document.head.appendChild(style);

  const acts = document.createElement("div");
  acts.className = "b3-acts";
  const see = button("See it in 3D");
  const table = button("See it on your table");
  table.hidden = true;
  acts.append(see, table);
  fig.appendChild(acts);

  let three = null;
  const loadThree = () => (three = three || import(THREE_URL));
  // Warm the engine while the pointer is on its way to the button.
  see.addEventListener("pointerenter", loadThree, { once: true });
  see.addEventListener("focus", loadThree, { once: true });

  let viewer = null;
  see.addEventListener("click", async () => {
    if (viewer) return viewer.close();
    see.setAttribute("aria-busy", "true");
    try {
      viewer = await openViewer(await loadThree(), () => {
        viewer = null;
        see.textContent = "See it in 3D";
        see.focus();
      });
      see.textContent = "Back to the cover";
    } catch (err) {
      console.warn("book3d:", err);
    } finally {
      see.removeAttribute("aria-busy");
    }
  });

  const quickLook = document.createElement("a").relList.supports("ar");
  if (quickLook) {
    table.hidden = false;
    table.addEventListener("click", () => busy(table, () => quickLookOpen(loadThree)));
  } else if (navigator.xr && navigator.xr.isSessionSupported) {
    navigator.xr.isSessionSupported("immersive-ar").then((ok) => {
      if (!ok) return;
      table.hidden = false;
      table.addEventListener("click", () => busy(table, () => webxrPlace(loadThree)));
    }).catch(() => {});
  }
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

function buildBook(THREE, img, name) {
  const W = H * (img.naturalWidth / img.naturalHeight);
  const [r, g, b] = spineColour(img);
  const base = `rgb(${r},${g},${b})`;
  const ink = 0.299 * r + 0.587 * g + 0.114 * b > 150 ? "#151a33" : "#f6f1e4";

  // Spine text reads top to bottom, as on a book printed in the US.
  const spine = canvasOf(96, 1000, (c, w, h) => {
    c.fillStyle = base;
    c.fillRect(0, 0, w, h);
    c.save();
    c.translate(w / 2, 0);
    c.rotate(Math.PI / 2);
    c.fillStyle = ink;
    c.textBaseline = "middle";
    let px = 40;
    c.font = `${px}px Georgia,serif`;
    const room = h * 0.72;
    while (c.measureText(name).width > room && px > 14) c.font = `${(px -= 2)}px Georgia,serif`;
    c.fillText(name, h * 0.05, 0);
    c.font = "22px Georgia,serif";
    c.textAlign = "right";
    c.fillText("Carrier Press", h * 0.96, 0);
    c.restore();
  });
  const back = canvasOf(64, 96, (c, w, h) => {
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
  const book = new THREE.Group();
  const face = (w, h, m, place) => {
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m);
    place(mesh);
    book.add(mesh);
  };
  face(W, H, mat(img, 0.55), (m) => { m.position.z = DEPTH / 2; });
  face(W, H, mat(back, 0.6), (m) => { m.rotation.y = Math.PI; m.position.z = -DEPTH / 2; });
  face(DEPTH, H, mat(spine, 0.6), (m) => { m.rotation.y = -Math.PI / 2; m.position.x = -W / 2; });
  face(DEPTH, H, mat(pages(64, 512, true), 0.9), (m) => { m.rotation.y = Math.PI / 2; m.position.x = W / 2; });
  const edge = mat(pages(256, 64, false), 0.9);
  face(W, DEPTH, edge, (m) => { m.rotation.x = -Math.PI / 2; m.position.y = H / 2; });
  face(W, DEPTH, edge, (m) => { m.rotation.x = Math.PI / 2; m.position.y = -H / 2; });
  book.userData.size = { W, H, D: DEPTH };
  return book;
}

/** The page's own cover once it has loaded. Not img.decode(): that can wait
 *  indefinitely in a tab that is not painting. */
function coverImage() {
  if (cover.complete && cover.naturalWidth) return Promise.resolve(cover);
  return new Promise((ok, fail) => {
    cover.addEventListener("load", () => ok(cover), { once: true });
    cover.addEventListener("error", fail, { once: true });
  });
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

async function openViewer(THREE, onClose) {
  const img = await coverImage();
  const name = title();
  const flat = fig.querySelector(".bk-cover");

  const stage = document.createElement("div");
  stage.className = "b3-stage";
  const canvas = document.createElement("canvas");
  canvas.tabIndex = 0;
  canvas.setAttribute("role", "img");
  canvas.setAttribute("aria-label", `${name}, shown as a book you can turn. Drag, or use the arrow keys.`);
  stage.appendChild(canvas);
  const hint = document.createElement("p");
  hint.className = "b3-hint";
  hint.textContent = "Drag to turn the book. Arrow keys work too.";

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  lights(THREE, scene);
  const book = buildBook(THREE, img, name);
  scene.add(book);
  const camera = new THREE.PerspectiveCamera(30, 4 / 5, 0.01, 10);
  camera.position.set(0, 0, 0.53);

  flat.hidden = true;
  fig.insertBefore(stage, flat);
  fig.insertBefore(hint, flat);

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
  const keys = (ev) => {
    const k = { ArrowLeft: [-0.2, 0], ArrowRight: [0.2, 0], ArrowUp: [0, -0.1], ArrowDown: [0, 0.1] }[ev.key];
    if (k) {
      ev.preventDefault();
      spin = false;
      yaw += k[0];
      pitch = Math.max(-0.7, Math.min(0.7, pitch + k[1]));
    } else if (ev.key === "Escape") {
      close();
    }
  };
  canvas.addEventListener("keydown", keys);

  let last = performance.now();
  renderer.setAnimationLoop((now) => {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    if (spin) yaw += dt * 0.5;
    book.rotation.set(pitch, yaw, 0);
    renderer.render(scene, camera);
  });
  canvas.focus({ preventScroll: true });

  function close() {
    renderer.setAnimationLoop(null);
    ro.disconnect();
    dispose(book);
    renderer.dispose();
    stage.remove();
    hint.remove();
    flat.hidden = false;
    onClose();
  }
  return { close };
}

// ------------------------------------------------------- on your table: iOS

async function quickLookOpen(loadThree) {
  const [THREE, { USDZExporter }] = await Promise.all([loadThree(), import(USDZ_URL)]);
  const scene = new THREE.Scene();
  const book = buildBook(THREE, await coverImage(), title());
  // Standing on the table, cover toward the visitor.
  book.position.y = book.userData.size.H / 2;
  scene.add(book);
  const bytes = await new USDZExporter().parseAsync(scene, {
    quickLookCompatible: true,
    ar: { anchoring: { type: "plane" }, planeAnchoring: { alignment: "horizontal" } },
  });
  dispose(book);
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

async function webxrPlace(loadThree) {
  const THREE = await loadThree();
  const img = await coverImage();

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

  const book = buildBook(THREE, img, title());
  const placed = new THREE.Group();
  book.position.y = book.userData.size.H / 2;
  placed.add(book);
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
