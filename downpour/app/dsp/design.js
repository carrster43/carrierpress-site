/*
 * The Rain Designer: a rain described by what causes it, turned into the one
 * Profile the engine (rain-dsp.js) already knows how to play.
 *
 * A design is up to three materials, each at its own level, under four
 * controls that act on all of them:
 *
 *   intensity  drizzle .. downpour      how many drops arrive
 *   dropSize   fine .. heavy            how big each one is
 *   wind       still .. gusty           how hard the rain comes in waves
 *   distance   under it .. far off      how much air and wall is in between
 *
 * Every control at its MIDDLE (distance at 0, "under it") gives back the
 * material exactly as authored, so a one-layer default design is the same
 * rain the app has always made. test/design.test.mjs holds that.
 *
 * Layering needs no new engine: the droplet voices of every layer are simply
 * put in one list (rain-dsp.js loops over any number of them), and the hiss
 * and body, which the engine has one of each, are merged by power.
 *
 * Sliders move in steps of 1/20 and levels in steps of 1/10, the same grid
 * the share code uses, so a shared rain comes back exactly as it was sent.
 *
 * Pure and dependency free: runs in Node, the browser and Expo alike.
 */
import { MATERIALS, MATERIAL_CODES } from "./materials.js";

export const MAX_LAYERS = 3;
export const SLIDER_STEPS = 20;
export const LEVEL_STEPS = 10;
export const CONTROLS = ["intensity", "dropSize", "wind", "distance"];

export const DEFAULT_DESIGN = Object.freeze({
  layers: Object.freeze([Object.freeze({ material: "tent", level: 1 })]),
  intensity: 0.5,
  dropSize: 0.5,
  wind: 0.5,
  distance: 0,
});

const clamp01 = (x) => Math.max(0, Math.min(1, x));
const snap = (x, steps) => Math.round(clamp01(x) * steps) / steps;
const num = (x, dflt) => (typeof x === "number" && Number.isFinite(x) ? x : dflt);
const clone = (p) => JSON.parse(JSON.stringify(p));

/** Any stored, typed or decoded value, made into a valid design. */
export function normalizeDesign(raw) {
  const o = raw && typeof raw === "object" ? raw : {};
  const seen = new Set();
  const layers = [];
  for (const l of Array.isArray(o.layers) ? o.layers : []) {
    if (!l || typeof l !== "object" || !(l.material in MATERIALS) || seen.has(l.material)) continue;
    seen.add(l.material);
    layers.push({ material: l.material, level: Math.max(1 / LEVEL_STEPS, snap(num(l.level, 1), LEVEL_STEPS)) });
    if (layers.length === MAX_LAYERS) break;
  }
  if (layers.length === 0) layers.push({ ...DEFAULT_DESIGN.layers[0] });
  const d = { layers };
  for (const k of CONTROLS) d[k] = snap(num(o[k], DEFAULT_DESIGN[k]), SLIDER_STEPS);
  return d;
}

/*
 * The four controls, applied to one material. Each mapping is centred so the
 * middle is a no-op, and spans about what Slower and Lower used to do at
 * their ends (Slower cut drops to 0.42x; Lower dropped pitch to 0.70x).
 */
export function shapeProfile(material, c) {
  const p = clone(material);
  const i = c.intensity - 0.5;           // -0.5 .. 0.5
  const s = c.dropSize - 0.5;
  const w = c.wind - 0.5;
  const x = c.distance;                  //  0 .. 1

  const rateMul = Math.pow(2, i * 2.6);          // 0.41x .. 2.46x drops
  const freqMul = Math.pow(2, -s * 1.4);         // heavy drops sound lower
  const decayMul = Math.pow(2, s * 0.8);         // and ring a little longer
  const dropDb = s * 6 - x * 9;                  // bigger is louder, far is quieter

  p.droplets = p.droplets.map(([f, d, rate, pan, lvl]) => [
    f * freqMul, d * decayMul, rate * rateMul, pan * (1 - 0.35 * x), lvl + dropDb,
  ]);
  p.hiss_db += i * 8 - x * 2;                    // the sheet thickens with the rain
  p.hiss_lp *= Math.pow(2, -x * 1.3);            // walls and air take the top off
  p.body_db += s * 4 + x * 3;
  p.gust_depth_db *= Math.pow(2, w * 3);
  p.gust_rate_hz *= Math.pow(2, w * 2);
  return p;
}

const toPow = (db) => Math.pow(10, db / 10);
const toDb = (pow) => 10 * Math.log10(Math.max(pow, 1e-12));

/** The design as the single Profile the engine plays. */
export function designProfile(design) {
  const d = normalizeDesign(design);
  // Three layers at full level must not be three times as loud: the gains
  // are scaled so their total power never passes that of one full layer.
  const power = d.layers.reduce((a, l) => a + l.level * l.level, 0);
  const norm = 1 / Math.sqrt(Math.max(1, power));
  const shaped = d.layers.map((l) => ({
    p: shapeProfile(MATERIALS[l.material], d),
    g: l.level * norm,
  }));
  if (shaped.length === 1 && shaped[0].g === 1) {
    return { ...shaped[0].p, label: shaped[0].p.label };
  }

  // Hiss and body: total power from every layer, with the filter corners
  // taken as a power weighted mean on a log scale (that is how they sound).
  const merge = (dbKey, fKeys) => {
    let tot = 0;
    const logs = fKeys.map(() => 0);
    for (const { p, g } of shaped) {
      const pw = toPow(p[dbKey]) * g * g;
      tot += pw;
      fKeys.forEach((k, j) => { logs[j] += pw * Math.log(p[k]); });
    }
    return { db: toDb(tot), f: logs.map((v) => Math.exp(v / tot)) };
  };
  const hiss = merge("hiss_db", ["hiss_hp", "hiss_lp"]);
  const body = merge("body_db", ["body_lp"]);

  const gsum = shaped.reduce((a, l) => a + l.g, 0);
  const mean = (k) => shaped.reduce((a, l) => a + l.p[k] * l.g, 0) / gsum;

  return {
    label: d.layers.map((l) => MATERIALS[l.material].label).join(" + "),
    blurb: "",
    hiss_hp: hiss.f[0], hiss_lp: hiss.f[1], hiss_db: hiss.db,
    body_lp: body.f[0], body_db: body.db,
    droplets: shaped.flatMap(({ p, g }) =>
      p.droplets.map(([f, dms, rate, pan, lvl]) => [f, dms, rate, pan, lvl + 20 * Math.log10(g)])),
    gust_depth_db: mean("gust_depth_db"),
    gust_rate_hz: mean("gust_rate_hz"),
  };
}

// ------------------------------------------------------------- words ---
const WORDS = {
  intensity: ["Drizzle", "Light", "Steady", "Heavy", "Downpour"],
  dropSize: ["Mist", "Fine", "Medium", "Large", "Heavy drops"],
  wind: ["Still", "Calm", "Breezy", "Gusty", "Stormy"],
  distance: ["Under it", "Close", "Sheltered", "Indoors", "Far off"],
};

/** A slider position in words: what a person reads, and what VoiceOver says. */
export function controlWord(key, value) {
  const w = WORDS[key];
  return w[Math.min(w.length - 1, Math.floor(clamp01(value) * w.length))];
}

/** One line for the lock screen and the hero card. */
export function describeDesign(design) {
  const d = normalizeDesign(design);
  const bits = [controlWord("intensity", d.intensity)];
  if (Math.abs(d.wind - 0.5) > 0.2) bits.push(controlWord("wind", d.wind).toLowerCase());
  if (d.distance > 0.15) bits.push(controlWord("distance", d.distance).toLowerCase());
  return bits.join(", ");
}

// --------------------------------------------------------- share codes ---
/*
 * A rain as a few characters: one letter and one level digit per layer, a
 * dash, then the four controls as base-36 digits on the 1/20 grid.
 *   "T" level 1, defaults            ->  "TA-AAA0"
 *   Tent full + Leaves at 0.4, heavy ->  "TAL4-GAA0"
 * There is nothing to host: the code IS the rain.
 */
const LETTER_TO_MATERIAL = Object.fromEntries(Object.entries(MATERIAL_CODES).map(([k, v]) => [v, k]));
const digit = (n) => n.toString(36).toUpperCase();

export function encodeDesign(design) {
  const d = normalizeDesign(design);
  const layers = d.layers.map((l) => MATERIAL_CODES[l.material] + digit(Math.round(l.level * LEVEL_STEPS))).join("");
  const controls = CONTROLS.map((k) => digit(Math.round(d[k] * SLIDER_STEPS))).join("");
  return `${layers}-${controls}`;
}

/** The design a code stands for, or null if it is not one. Forgiving about
 *  case, spaces and any words pasted around it ("my rain: TA-AAA0"). */
export function decodeDesign(text) {
  if (typeof text !== "string") return null;
  const m = text.toUpperCase().match(/\b((?:[A-Z][1-9A]){1,3})-([0-9A-K]{4})\b/);
  if (!m) return null;
  const layers = [];
  for (let i = 0; i < m[1].length; i += 2) {
    const material = LETTER_TO_MATERIAL[m[1][i]];
    if (!material) return null;
    layers.push({ material, level: parseInt(m[1][i + 1], 36) / LEVEL_STEPS });
  }
  const d = { layers };
  CONTROLS.forEach((k, j) => { d[k] = parseInt(m[2][j], 36) / SLIDER_STEPS; });
  const out = normalizeDesign(d);
  return out.layers.length === layers.length ? out : null;   // duplicates are not a code
}

/** Slower / Lower from before the Designer, as positions on its controls. */
export function designFromTreatments(material, t) {
  return normalizeDesign({
    layers: [{ material, level: 1 }],
    intensity: t && t.slower ? 0.2 : 0.5,
    dropSize: t && t.lower ? 0.75 : 0.5,
    wind: t && t.slower ? 0.35 : 0.5,
    distance: t && t.lower ? 0.35 : 0,
  });
}
