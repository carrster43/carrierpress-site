/*
 * The Reading Room: every book and app in one ring, in a browser, in VR, or as
 * a table-top hologram. Data comes from the page (make_immersive.py writes it
 * into #room-data); nothing here is generated, and nothing leaves the site.
 *
 * Units are metres. The visitor stands at the origin, eyes at 1.6 m.
 * Bays sit on a ring of radius RING: one per book section, in catalogue order,
 * then the apps, APPS_PER_BAY to a bay.
 *
 * Two layouts of the same objects. In the room (browser and VR) the visitor
 * stands at the centre, so the press mark turns overhead and the motes drift
 * well clear of their face. As a hologram the visitor looks down on the room
 * from outside, so the mark stands on its column of light in the middle.
 */
import * as THREE from "/vendor/three/three.module.min.js";

const data = JSON.parse(document.getElementById("room-data").textContent);
const stage = document.getElementById("stage");
const hint = document.getElementById("ir-hint");
const pick = document.getElementById("ir-pick");
const vrBtn = document.getElementById("enter-vr");
const arBtn = document.getElementById("enter-ar");
const still = matchMedia("(prefers-reduced-motion: reduce)").matches;

const RING = 5;
const APPS_PER_BAY = 12;
const APP_BAYS = Math.ceil(data.apps.length / APPS_PER_BAY);
const BAYS = data.bays.length + APP_BAYS;
// The flat width of one bay, less a margin so neighbours do not touch.
const BAY_W = 2 * RING * Math.sin(Math.PI / BAYS) * 0.94;
const EYE = 1.6;
const GOLD = 0xe8c84a;
// The room as a hologram: about a metre across, at table height, in front.
const HOLO_SCALE = 0.09;
const HOLO_AT = new THREE.Vector3(0, 0.85, -0.9);

// ------------------------------------------------------------------ renderer
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
} catch {
  hint.textContent = "";
  throw new Error("No WebGL: the plain list below stands in for the room.");
}
document.getElementById("ir-fallback").remove();
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.xr.enabled = true;
stage.prepend(renderer.domElement);

const scene = new THREE.Scene();
const sky = new THREE.Color(0x07080f);
scene.background = sky;
scene.fog = new THREE.Fog(0x07080f, 9, 22);

const camera = new THREE.PerspectiveCamera(70, 1, 0.02, 60);
camera.position.set(0, EYE, 0);

// Everything the visitor sees lives in `world`, so hologram mode can shrink
// and place it in one move.
const world = new THREE.Group();
scene.add(world);
const room = new THREE.Group(); // floor and walls: hidden as a hologram
world.add(room);

// ------------------------------------------------------------------ helpers
function canvasTexture(w, h, draw) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

function wrap(ctx, text, maxW) {
  const words = String(text).split(/\s+/);
  const lines = [];
  let line = "";
  for (const w of words) {
    const next = line ? line + " " + w : w;
    if (ctx.measureText(next).width > maxW && line) {
      lines.push(line);
      line = w;
    } else line = next;
  }
  if (line) lines.push(line);
  return lines;
}

const SERIF = "Georgia, 'Iowan Old Style', Palatino, serif";
const SANS = "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif";

/** A bay heading: the shelf in small caps over the series name. */
function headingTexture(name, shelf) {
  return canvasTexture(1024, 160, (g, w, h) => {
    g.textAlign = "center";
    g.fillStyle = "#b9b4a6";
    g.font = `600 30px ${SANS}`;
    g.fillText(String(shelf || "").toUpperCase(), w / 2, 48);
    g.fillStyle = "#f2d76b";
    g.font = `400 64px ${SERIF}`;
    g.fillText(name, w / 2, 124, w - 40);
  });
}

/** An app as a card: name, its one line, and where it stands. */
function appTexture(a) {
  return canvasTexture(512, 320, (g, w, h) => {
    g.fillStyle = "#1a1c2c";
    g.fillRect(0, 0, w, h);
    g.strokeStyle = "#2b2e42";
    g.lineWidth = 4;
    g.strokeRect(2, 2, w - 4, h - 4);
    g.fillStyle = "#ece8dd";
    g.font = `400 46px ${SERIF}`;
    g.fillText(a.t, 28, 70, w - 56);
    g.fillStyle = "#b9b4a6";
    g.font = `400 26px ${SANS}`;
    wrap(g, a.line, w - 56).slice(0, 4).forEach((l, i) => g.fillText(l, 28, 122 + i * 36));
    g.fillStyle = "#e8c84a";
    g.font = `600 24px ${SANS}`;
    g.fillText(a.status.toUpperCase(), 28, h - 30, w - 56);
  });
}

/** The panel that floats in front of a pick in VR. */
function pickTexture(item) {
  return canvasTexture(768, 300, (g, w, h) => {
    g.fillStyle = "rgba(7,8,15,0.92)";
    g.fillRect(0, 0, w, h);
    g.strokeStyle = "#e8c84a";
    g.lineWidth = 4;
    g.strokeRect(2, 2, w - 4, h - 4);
    g.fillStyle = "#ece8dd";
    g.font = `400 48px ${SERIF}`;
    wrap(g, item.t, w - 60).slice(0, 2).forEach((l, i) => g.fillText(l, 30, 76 + i * 58));
    g.fillStyle = "#f2d76b";
    g.font = `600 30px ${SANS}`;
    g.fillText("Select again to open its page", 30, h - 40);
  });
}

// ------------------------------------------------------------------ the room
// Floor: a dark disc with faint rings, like a chart's compass rose seen from above.
const floorTex = canvasTexture(1024, 1024, (g, w) => {
  const c = w / 2;
  g.fillStyle = "#0b0c16";
  g.fillRect(0, 0, w, w);
  g.strokeStyle = "rgba(232,200,74,0.18)";
  for (let r = 60; r < c; r += 60) {
    g.lineWidth = r % 240 === 0 ? 3 : 1;
    g.beginPath();
    g.arc(c, c, r, 0, Math.PI * 2);
    g.stroke();
  }
  g.lineWidth = 1;
  for (let i = 0; i < BAYS; i++) {
    const a = (i / BAYS) * Math.PI * 2;
    g.beginPath();
    g.moveTo(c, c);
    g.lineTo(c + Math.cos(a) * c, c + Math.sin(a) * c);
    g.stroke();
  }
});
const floor = new THREE.Mesh(
  new THREE.CircleGeometry(RING + 3, 96),
  new THREE.MeshBasicMaterial({ map: floorTex })
);
floor.rotation.x = -Math.PI / 2;
room.add(floor);

// A low wall of light behind the bays, so the ring reads as a room.
const wall = new THREE.Mesh(
  new THREE.CylinderGeometry(RING + 0.6, RING + 0.6, 3.6, 96, 1, true),
  new THREE.MeshBasicMaterial({ color: 0x10121f, side: THREE.BackSide })
);
wall.position.y = 1.8;
room.add(wall);

// The hologram column at the centre: a shaded cylinder of scanning light with
// the press mark turning above it. It stays in both modes; it is the point.
const holoMat = new THREE.ShaderMaterial({
  transparent: true,
  depthWrite: false,
  blending: THREE.AdditiveBlending,
  side: THREE.DoubleSide,
  uniforms: { uTime: { value: 0 }, uColor: { value: new THREE.Color(GOLD) } },
  vertexShader: `
    varying vec2 vUv; varying vec3 vN; varying vec3 vView;
    void main(){
      vUv = uv;
      vec4 mv = modelViewMatrix * vec4(position, 1.0);
      vN = normalize(normalMatrix * normal);
      vView = normalize(-mv.xyz);
      gl_Position = projectionMatrix * mv;
    }`,
  fragmentShader: `
    uniform float uTime; uniform vec3 uColor;
    varying vec2 vUv; varying vec3 vN; varying vec3 vView;
    void main(){
      float rim = pow(1.0 - abs(dot(vN, vView)), 2.0);
      float scan = 0.55 + 0.45 * sin(vUv.y * 120.0 - uTime * 4.0);
      float fade = smoothstep(1.0, 0.15, vUv.y);
      float a = (0.12 + rim * 0.9) * scan * fade;
      gl_FragColor = vec4(uColor * a, a);
    }`,
});
const column = new THREE.Group(); // shown only as a hologram
column.add(new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.6, 1.4, 64, 1, true), holoMat));
column.children[0].position.y = 0.7;
const base = new THREE.Mesh(
  new THREE.CylinderGeometry(0.66, 0.72, 0.06, 64),
  new THREE.MeshBasicMaterial({ color: 0x1a1c2c })
);
base.position.y = 0.03;
column.add(base);
world.add(column);

// In the room, a ring of the same light on the floor around the visitor.
const halo = new THREE.Mesh(
  new THREE.RingGeometry(0.9, 1.0, 96),
  new THREE.MeshBasicMaterial({ color: GOLD, transparent: true, opacity: 0.35, side: THREE.DoubleSide })
);
halo.rotation.x = -Math.PI / 2;
halo.position.y = 0.005;
room.add(halo);

const mark = new THREE.Mesh(
  new THREE.PlaneGeometry(0.85, 0.6),
  new THREE.MeshBasicMaterial({ transparent: true, side: THREE.DoubleSide, depthWrite: false })
);
world.add(mark);
new THREE.TextureLoader().load("/assets/logo-mark-light.png", (t) => {
  t.colorSpace = THREE.SRGBColorSpace;
  mark.material.map = t;
  mark.material.needsUpdate = true;
});

// Motes of light, rising.
const MOTES = 220;
const motePos = new Float32Array(MOTES * 3);
let moteTop = 2;
/** Scatter the motes inside radius [r0, r1] and height [0, top]. */
function scatter(r0, r1, top) {
  moteTop = top;
  for (let i = 0; i < MOTES; i++) {
    const r = r0 + Math.random() * (r1 - r0);
    const a = Math.random() * Math.PI * 2;
    motePos.set([Math.cos(a) * r, Math.random() * top, Math.sin(a) * r], i * 3);
  }
}
const moteGeo = new THREE.BufferGeometry();
moteGeo.setAttribute("position", new THREE.BufferAttribute(motePos, 3));
const motes = new THREE.Points(
  moteGeo,
  new THREE.PointsMaterial({
    color: GOLD,
    size: 0.03,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  })
);
world.add(motes);

// ------------------------------------------------------------------ the bays
const pickables = []; // meshes a pointer or controller can select
const loader = new THREE.TextureLoader();

function bayFrame(i) {
  // Bay 0 is straight ahead (-z); the ring runs to the right from there.
  const a = (i / BAYS) * Math.PI * 2;
  const g = new THREE.Group();
  g.position.set(Math.sin(a) * RING, 0, -Math.cos(a) * RING);
  g.lookAt(0, 0, 0);
  world.add(g);
  return g;
}

function heading(g, name, shelf, top) {
  const m = new THREE.Mesh(
    new THREE.PlaneGeometry(BAY_W, BAY_W * 0.156),
    new THREE.MeshBasicMaterial({ map: headingTexture(name, shelf), transparent: true })
  );
  m.position.y = top + BAY_W * 0.12;
  g.add(m);
}

/** Lay `n` tiles of w x h into a grid no wider than a bay, centred near eye height. */
function grid(n, w, h, gap) {
  const cols = Math.max(1, Math.min(n, Math.floor((BAY_W + gap) / (w + gap))));
  const rows = Math.ceil(n / cols);
  const totalH = rows * h + (rows - 1) * gap;
  const top = Math.max(EYE + totalH / 2 - 0.2, totalH + 0.35);
  const at = (k) => {
    const r = Math.floor(k / cols);
    const inRow = Math.min(cols, n - r * cols);
    const c = k - r * cols;
    const rowW = inRow * w + (inRow - 1) * gap;
    return [-rowW / 2 + w / 2 + c * (w + gap), top - h / 2 - r * (h + gap)];
  };
  return { at, top };
}

data.bays.forEach((bay, i) => {
  const g = bayFrame(i);
  const W = 0.26, H = 0.39, GAP = 0.05;
  const { at, top } = grid(bay.items.length, W, H, GAP);
  heading(g, bay.name, bay.shelf, top);
  bay.items.forEach((item, k) => {
    const [x, y] = at(k);
    const mat = new THREE.MeshBasicMaterial({ color: 0x2b2e42 });
    const m = new THREE.Mesh(new THREE.PlaneGeometry(W, H), mat);
    m.position.set(x, y, 0);
    m.userData = { item, kind: "book" };
    g.add(m);
    pickables.push(m);
    loader.load(item.img, (t) => {
      t.colorSpace = THREE.SRGBColorSpace;
      t.anisotropy = 4;
      mat.map = t;
      mat.color.set(0xffffff);
      mat.needsUpdate = true;
    });
  });
});

for (let b = 0; b < APP_BAYS; b++) {
  const rows = data.apps.slice(b * APPS_PER_BAY, (b + 1) * APPS_PER_BAY);
  const g = bayFrame(data.bays.length + b);
  const W = Math.min(0.56, (BAY_W - 0.1) / 3), H = W * 0.625, GAP = 0.05;
  const { at, top } = grid(rows.length, W, H, GAP);
  heading(g, b === 0 ? "Apps" : "Apps, continued", "Carrier Ventures", top);
  rows.forEach((a, k) => {
    const [x, y] = at(k);
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(W, H),
      new THREE.MeshBasicMaterial({ map: appTexture(a) })
    );
    m.position.set(x, y, 0);
    m.userData = { item: a, kind: "app" };
    g.add(m);
    pickables.push(m);
  });
}

// ------------------------------------------------------------------ picking
const ray = new THREE.Raycaster();
let hovered = null;
let picked = null;
const pickPanel = new THREE.Mesh(
  new THREE.PlaneGeometry(0.9, 0.35),
  new THREE.MeshBasicMaterial({ transparent: true, depthTest: false })
);
pickPanel.renderOrder = 10;
pickPanel.visible = false;

function setHover(m) {
  if (hovered === m) return;
  if (hovered) hovered.scale.setScalar(1);
  hovered = m;
  if (hovered) hovered.scale.setScalar(1.08);
}

function choose(m) {
  if (!m) return;
  const { item } = m.userData;
  if (renderer.xr.isPresenting) {
    // In a headset a page load would drop the visitor out of the room without
    // warning, so the first select only names the thing; the second goes.
    if (picked === m) {
      const session = renderer.xr.getSession();
      session.addEventListener("end", () => location.assign(item.url), { once: true });
      session.end();
      return;
    }
    picked = m;
    pickPanel.material.map?.dispose();
    pickPanel.material.map = pickTexture(item);
    pickPanel.material.needsUpdate = true;
    m.parent.add(pickPanel);
    pickPanel.position.set(m.position.x, m.position.y - 0.42, 0.25);
    pickPanel.visible = true;
    return;
  }
  picked = m;
  pick.hidden = false;
  pick.replaceChildren();
  const s = document.createElement("strong");
  s.textContent = item.t;
  pick.append(s);
  if (item.status || item.line) {
    const sp = document.createElement("span");
    sp.textContent = [item.line, item.status].filter(Boolean).join(" · ");
    pick.append(sp);
  }
  const a = document.createElement("a");
  a.href = item.url;
  a.textContent = m.userData.kind === "book" ? "Open the book's page" : "Open the app's page";
  pick.append(a);
}

// ------------------------------------------------------------------ browser look
// Drag to turn, tap to choose. Yaw and pitch only: the visitor stays put, which
// is kinder to stomachs than flying about, and true to standing in a room.
let yaw = 0, pitch = 0, drag = null;
const ndc = new THREE.Vector2();

function aim() {
  camera.rotation.set(pitch, yaw, 0, "YXZ");
}

function hitAt(ev) {
  const r = renderer.domElement.getBoundingClientRect();
  ndc.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(ndc, camera);
  return ray.intersectObjects(pickables, false)[0]?.object ?? null;
}

const el = renderer.domElement;
el.addEventListener("pointerdown", (ev) => {
  drag = { x: ev.clientX, y: ev.clientY, yaw, pitch, moved: false };
  el.setPointerCapture(ev.pointerId);
});
el.addEventListener("pointermove", (ev) => {
  if (!drag) {
    if (ev.pointerType === "mouse") setHover(hitAt(ev));
    return;
  }
  const dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
  if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
  yaw = drag.yaw + dx * 0.005;
  pitch = THREE.MathUtils.clamp(drag.pitch + dy * 0.004, -0.9, 0.9);
  aim();
});
el.addEventListener("pointerup", (ev) => {
  if (drag && !drag.moved) choose(hitAt(ev));
  drag = null;
});
el.tabIndex = 0;
el.setAttribute("role", "img");
el.setAttribute("aria-label", "A ring of book covers and app cards around a column of light. Arrow keys turn; the same books and apps are listed below as links.");
el.addEventListener("keydown", (ev) => {
  const k = { ArrowLeft: [0.15, 0], ArrowRight: [-0.15, 0], ArrowUp: [0, 0.1], ArrowDown: [0, -0.1] }[ev.key];
  if (!k) return;
  ev.preventDefault();
  yaw += k[0];
  pitch = THREE.MathUtils.clamp(pitch + k[1], -0.9, 0.9);
  aim();
});

// ------------------------------------------------------------------ XR
const controllers = [0, 1].map((i) => {
  const c = renderer.xr.getController(i);
  const line = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3(0, 0, -1)]),
    new THREE.LineBasicMaterial({ color: GOLD, transparent: true, opacity: 0.7 })
  );
  line.scale.z = 8;
  c.add(line);
  c.addEventListener("select", () => choose(c.userData.hit));
  scene.add(c);
  return c;
});
const tmp = new THREE.Matrix4();

function xrHover() {
  let any = null;
  for (const c of controllers) {
    tmp.identity().extractRotation(c.matrixWorld);
    ray.ray.origin.setFromMatrixPosition(c.matrixWorld);
    ray.ray.direction.set(0, 0, -1).applyMatrix4(tmp);
    const hit = ray.intersectObjects(pickables, false)[0];
    c.userData.hit = hit?.object ?? null;
    c.children[0].scale.z = hit ? hit.distance : 8;
    any = any || c.userData.hit;
  }
  setHover(any);
}

let holo = false;
let markY = 3.3;

function enterHologram(on) {
  holo = on;
  room.visible = !on;
  column.visible = on;
  mark.scale.setScalar(on ? 1 : 1.8);
  markY = on ? 1.65 : 3.3;
  // Point size is in metres but ignores the world's scale, so shrink it with
  // the room or the motes swamp the hologram.
  motes.material.size = on ? 0.03 * HOLO_SCALE : 0.03;
  if (on) scatter(0, 0.5, 2);
  else scatter(1.4, RING - 0.8, 3.4);
  moteGeo.attributes.position.needsUpdate = true;
  scene.background = on ? null : sky;
  scene.fog = on ? null : new THREE.Fog(0x07080f, 9, 22);
  world.scale.setScalar(on ? HOLO_SCALE : 1);
  world.position.copy(on ? HOLO_AT : new THREE.Vector3());
}

async function start(mode) {
  const session = await navigator.xr.requestSession(mode, {
    requiredFeatures: ["local-floor"],
  });
  enterHologram(mode === "immersive-ar");
  renderer.xr.setReferenceSpaceType("local-floor");
  await renderer.xr.setSession(session);
  pick.hidden = true;
  session.addEventListener("end", () => {
    enterHologram(false);
    pickPanel.visible = false;
    picked = null;
    camera.position.set(0, EYE, 0);
    aim();
    resize();
  });
}

async function offer(btn, mode) {
  if (!navigator.xr) return false;
  try {
    if (!(await navigator.xr.isSessionSupported(mode))) return false;
  } catch {
    return false;
  }
  btn.hidden = false;
  btn.addEventListener("click", () =>
    start(mode).catch((err) => {
      hint.textContent = "The headset declined: " + (err?.message || err);
    })
  );
  return true;
}

// ------------------------------------------------------------------ loop
const clock = new THREE.Clock();
const up = moteGeo.attributes.position;

function frame() {
  const dt = Math.min(clock.getDelta(), 0.05);
  const t = clock.elapsedTime;
  holoMat.uniforms.uTime.value = t;
  if (!still) {
    mark.rotation.y = t * 0.5;
    mark.position.y = markY + Math.sin(t * 1.2) * 0.04;
    for (let i = 0; i < MOTES; i++) {
      let y = up.getY(i) + dt * (0.15 + (i % 7) * 0.03);
      if (y > moteTop) y = 0;
      up.setY(i, y);
    }
    up.needsUpdate = true;
  }
  if (renderer.xr.isPresenting) xrHover();
  renderer.render(scene, camera);
}

function resize() {
  if (renderer.xr.isPresenting) return;
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
addEventListener("resize", resize);
// ?hologram previews the table-top layout on a flat screen, over the dark
// room colour since there is no real room behind it to show.
const preview = new URLSearchParams(location.search).has("hologram");
enterHologram(preview);
if (preview) {
  scene.background = sky;
  camera.position.set(0, 1.3, -0.15);
  pitch = -0.55;
}
mark.position.y = markY;
resize();
aim();
renderer.setAnimationLoop(frame);

const [vr, ar] = await Promise.all([offer(vrBtn, "immersive-vr"), offer(arBtn, "immersive-ar")]);
const touch = matchMedia("(pointer: coarse)").matches;
hint.textContent =
  (touch ? "Drag to look around, tap a cover to open it." : "Drag to look around, click a cover to open it.") +
  (vr || ar ? "" : " On a VR headset's browser this page also offers Enter VR.");
