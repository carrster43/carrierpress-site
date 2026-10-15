/*
 * Downpour - the rain synthesis itself, with no audio host in it.
 *
 * This file is shared verbatim by the browser AudioWorklet and by the Expo
 * app's react-native-audio-api worklet. It therefore obeys the stricter of the
 * two runtimes: no classes, no closures held across calls, no imports. All
 * state lives in one plain object of typed arrays, which is what a React
 * Native worklet runtime is able to carry between invocations.
 *
 * The 'worklet' directives are what let React Native's worklet runtime take
 * these functions onto the audio thread. They are an inert string literal in
 * a plain browser, so the same file runs unmodified in an AudioWorklet.
 *
 * It is a port of render_rain.py. The one substantive change is the droplet
 * layer: the renderer FFT-convolves a sparse Poisson impulse train with a
 * decaying-sine kernel, and that convolution is linear and time invariant, so
 * feeding the same impulses to a single two-pole resonator gives the identical
 * result for two multiplies per sample.
 */

export const CTRL_SR = 100;
export const LIMIT_KNEE = 0.89;
const CLICK_LEN = 10;

const Q_ORDER2 = [0.70710678];
const Q_ORDER4 = [0.54119610, 1.30656296];

const COEF = 5;                 // b0, b1, b2, a1, a2 per biquad section
const Z_PER_SECTION = 4;        // z1, z2 for each of two channels

function db(x) {
  'worklet';
  return Math.pow(10, x / 20);
}

// ------------------------------------------------------------------ prng ---
function rngNext(st) {
  'worklet';
  // mulberry32, kept in a Uint32Array so the state survives the worklet hop
  let a = (st.rng[0] + 0x6d2b79f5) >>> 0;
  st.rng[0] = a;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}

function gaussNext(st) {
  'worklet';
  if (st.gaussHas[0]) { st.gaussHas[0] = 0; return st.gaussSpare[0]; }
  let u = rngNext(st);
  if (u <= 0) u = 1e-9;
  const v = rngNext(st);
  const mag = Math.sqrt(-2 * Math.log(u));
  st.gaussSpare[0] = mag * Math.sin(2 * Math.PI * v);
  st.gaussHas[0] = 1;
  return mag * Math.cos(2 * Math.PI * v);
}

// --------------------------------------------------------------- biquads ---
function writeSection(coef, idx, kind, fc, q, sr) {
  'worklet';
  const w0 = 2 * Math.PI * Math.min(fc, sr * 0.49) / sr;
  const cw = Math.cos(w0);
  const alpha = Math.sin(w0) / (2 * q);
  const a0 = 1 + alpha;
  let b0, b1, b2;
  if (kind === 1) {                       // lowpass
    b0 = (1 - cw) / 2; b1 = 1 - cw; b2 = (1 - cw) / 2;
  } else {                                // highpass
    b0 = (1 + cw) / 2; b1 = -(1 + cw); b2 = (1 + cw) / 2;
  }
  const o = idx * COEF;
  coef[o] = b0 / a0; coef[o + 1] = b1 / a0; coef[o + 2] = b2 / a0;
  coef[o + 3] = (-2 * cw) / a0; coef[o + 4] = (1 - alpha) / a0;
}

/* Transposed direct form II, one section, one channel. */
function runSection(coef, z, idx, ch, x) {
  'worklet';
  const o = idx * COEF;
  const zo = idx * Z_PER_SECTION + ch * 2;
  const y = coef[o] * x + z[zo];
  z[zo]     = coef[o + 1] * x - coef[o + 3] * y + z[zo + 1];
  z[zo + 1] = coef[o + 2] * x - coef[o + 4] * y;
  return y;
}

function runChain(coef, z, first, count, ch, x) {
  'worklet';
  let y = x;
  for (let i = 0; i < count; i++) y = runSection(coef, z, first + i, ch, y);
  return y;
}

// ------------------------------------------------- arrivals and gust ---
// Declared above createRainState on purpose: the worklets babel plugin
// rewrites these into const bindings, which have a temporal dead zone and
// do not hoist the way a function declaration does.
/* Exponential inter-arrival gap: the same Poisson process, sampled exactly. */
function nextGap(st, rate) {
  'worklet';
  let u = rngNext(st);
  if (u <= 0) u = 1e-9;
  return (-Math.log(u) / rate) * st.sr;
}

function nextGust(st) {
  'worklet';
  const a = st.gust[0];
  st.gust[2] = a * st.gust[2] + (1 - a) * (gaussNext(st) * st.gust[1]);
  const clipped = Math.max(-3, Math.min(3, st.gust[2]));
  return db(clipped * st.gust[3]);
}

// ------------------------------------------------------------ night arcs ---
/*
 * A Night Arc (dsp/arcs.js) is a profile that carries `arc`: keyframe profiles
 * with the SAME droplet voices, the time of each, a gain for each, and an
 * optional loop length. The audio thread glides between them on its own clock,
 * so an arc keeps moving with the screen locked and no JS timer is involved.
 *
 * Per key the flat array holds, for each voice, [freq, decay_ms, rate,
 * level_db], then the eight globals below.
 */
const ARC_GLOBALS = 8;   // hiss_hp, hiss_lp, hiss_db, body_lp, body_db, gust_depth, gust_rate, gain
const ARC_EVERY = 50;    // control ticks between full recomputes (0.5 s)

function arcStride(nv) {
  'worklet';
  return nv * 4 + ARC_GLOBALS;
}

/* Where t (seconds) falls: writes key index and eased fraction into st.arcPos. */
function arcLocate(st, t) {
  'worklet';
  const nk = st.arcInfo[0];
  const loop = st.arcInfo[1];
  const T = st.arcT;
  let x = t;
  if (loop > 0 && x >= loop) x = x % loop;
  if (x >= T[nk - 1]) { st.arcPos[0] = nk - 1; st.arcPos[1] = 0; return; }
  let k = 0;
  while (k < nk - 2 && x >= T[k + 1]) k++;
  const span = T[k + 1] - T[k];
  const u = span > 0 ? Math.max(0, Math.min(1, (x - T[k]) / span)) : 1;
  st.arcPos[0] = k;
  st.arcPos[1] = u * u * (3 - 2 * u);   // smoothstep: no corner at a keyframe
}

/* One value between key k and k+1. geo: interpolate on a log scale. */
function arcVal(st, k, u, idx, geo) {
  'worklet';
  const S = arcStride(st.nv);
  const a = st.arcK[k * S + idx];
  if (u === 0 || k + 1 >= st.arcInfo[0]) return a;
  const b = st.arcK[(k + 1) * S + idx];
  if (geo) return a * Math.pow(b / a, u);
  return a + (b - a) * u;
}

/* The gain alone, every control tick, so a fade in or out is smooth. */
function arcGain(st, t) {
  'worklet';
  arcLocate(st, t);
  st.master[0] = arcVal(st, st.arcPos[0], st.arcPos[1], st.nv * 4 + 7, false);
}

/* Everything else: voices, filters, levels and gust. */
function arcApply(st, t) {
  'worklet';
  arcLocate(st, t);
  const k = st.arcPos[0], u = st.arcPos[1];
  const sr = st.sr, nv = st.nv;
  for (let i = 0; i < nv; i++) {
    const f0 = arcVal(st, k, u, i * 4, true);
    const decayMs = arcVal(st, k, u, i * 4 + 1, true);
    const w = 2 * Math.PI * f0 / sr;
    const r = Math.exp(-1 / ((decayMs / 1000) * sr));
    st.vA1[i] = 2 * r * Math.cos(w);
    st.vA2[i] = r * r;
    st.vDrive[i] = Math.sin(w);
    st.vRate[i] = arcVal(st, k, u, i * 4 + 2, true);
    st.vLevel[i] = db(arcVal(st, k, u, i * 4 + 3, false));
  }
  const g = nv * 4;
  writeSection(st.hissCoef, 0, 0, arcVal(st, k, u, g, true), Q_ORDER2[0], sr);
  const lp = arcVal(st, k, u, g + 1, true);
  writeSection(st.hissCoef, 1, 1, lp, Q_ORDER4[0], sr);
  writeSection(st.hissCoef, 2, 1, lp, Q_ORDER4[1], sr);
  st.hissLevel = db(arcVal(st, k, u, g + 2, false));
  const blp = arcVal(st, k, u, g + 3, true);
  writeSection(st.bodyCoef, 0, 1, blp, Q_ORDER4[0], sr);
  writeSection(st.bodyCoef, 1, 1, blp, Q_ORDER4[1], sr);
  st.bodyLevel = db(arcVal(st, k, u, g + 4, false));
  const a = Math.exp(-2 * Math.PI * arcVal(st, k, u, g + 6, true) / CTRL_SR);
  st.gust[0] = a;
  st.gust[1] = 1 / Math.sqrt(1 - a * a);
  st.gust[3] = arcVal(st, k, u, g + 5, false);
}

/* Called once per control tick from renderRain, only when there is an arc. */
function arcTick(st) {
  'worklet';
  const ticks = st.arcInfo[2];
  const t = ticks / CTRL_SR;
  arcGain(st, t);
  if (ticks % ARC_EVERY === 0) arcApply(st, t);
  st.arcInfo[2] = ticks + 1;
}

// ----------------------------------------------------------------- state ---
/*
 * Build every coefficient and every piece of running state up front, so the
 * render loop allocates nothing and the whole thing can sit in a worklet.
 */
export function createRainState(profile, seed, sampleRate) {
  'worklet';
  const sr = sampleRate;
  const nv = profile.droplets.length;

  // hiss chain: 1 highpass section then 2 lowpass sections (Butterworth 2 + 4)
  const hissCoef = new Float64Array(3 * COEF);
  writeSection(hissCoef, 0, 0, profile.hiss_hp, Q_ORDER2[0], sr);
  writeSection(hissCoef, 1, 1, profile.hiss_lp, Q_ORDER4[0], sr);
  writeSection(hissCoef, 2, 1, profile.hiss_lp, Q_ORDER4[1], sr);

  const bodyCoef = new Float64Array(2 * COEF);
  writeSection(bodyCoef, 0, 1, profile.body_lp, Q_ORDER4[0], sr);
  writeSection(bodyCoef, 1, 1, profile.body_lp, Q_ORDER4[1], sr);

  const dcCoef = new Float64Array(1 * COEF);
  writeSection(dcCoef, 0, 0, 32, Q_ORDER2[0], sr);

  const st = {
    sr, nv,
    hissCoef, hissZ: new Float64Array(3 * Z_PER_SECTION),
    bodyCoef, bodyZ: new Float64Array(2 * Z_PER_SECTION),
    dcCoef,   dcZ:   new Float64Array(1 * Z_PER_SECTION),
    hissLevel: db(profile.hiss_db),
    bodyLevel: db(profile.body_db),

    vA1: new Float64Array(nv), vA2: new Float64Array(nv),
    vDrive: new Float64Array(nv), vLevel: new Float64Array(nv),
    vGainL: new Float64Array(nv), vGainR: new Float64Array(nv),
    vRate: new Float64Array(nv),
    vY1: new Float64Array(nv), vY2: new Float64Array(nv),
    vCountdown: new Float64Array(nv),
    vClickLeft: new Int32Array(nv), vClickAmp: new Float64Array(nv),

    rng: new Uint32Array(1),
    gaussSpare: new Float64Array(1), gaussHas: new Int32Array(1),

    gust: new Float64Array(6),   // a, drive, state, depth, cur, next
    ctrl: new Int32Array(2),     // stride, count

    // Night arc: [key count (0 or 1 = none), loop seconds, ticks elapsed, spare]
    arcInfo: new Float64Array(4),
    arcT: new Float64Array(1), arcK: new Float64Array(1),
    arcPos: new Float64Array(2),
    master: new Float64Array(1),
  };
  st.master[0] = 1;

  const arc = profile.arc;
  if (arc && arc.keys && arc.keys.length > 1) {
    const nk = arc.keys.length;
    const S = arcStride(nv);
    st.arcInfo[0] = nk;
    st.arcInfo[1] = arc.loop || 0;
    st.arcT = new Float64Array(nk);
    st.arcK = new Float64Array(nk * S);
    for (let k = 0; k < nk; k++) {
      const p = arc.keys[k];
      st.arcT[k] = arc.at[k];
      for (let i = 0; i < nv; i++) {
        const d = p.droplets[i];
        st.arcK[k * S + i * 4] = d[0];
        st.arcK[k * S + i * 4 + 1] = d[1];
        st.arcK[k * S + i * 4 + 2] = d[2];
        st.arcK[k * S + i * 4 + 3] = d[4];
      }
      const g = k * S + nv * 4;
      st.arcK[g] = p.hiss_hp; st.arcK[g + 1] = p.hiss_lp; st.arcK[g + 2] = p.hiss_db;
      st.arcK[g + 3] = p.body_lp; st.arcK[g + 4] = p.body_db;
      st.arcK[g + 5] = p.gust_depth_db; st.arcK[g + 6] = p.gust_rate_hz;
      st.arcK[g + 7] = arc.gain ? arc.gain[k] : 1;
    }
  }
  st.rng[0] = (seed >>> 0) || 1;

  for (let i = 0; i < nv; i++) {
    const d = profile.droplets[i];
    const f0 = d[0], decayMs = d[1], rate = d[2], pan = d[3], levelDb = d[4];
    const w = 2 * Math.PI * f0 / sr;
    const r = Math.exp(-1 / ((decayMs / 1000) * sr));
    st.vA1[i] = 2 * r * Math.cos(w);
    st.vA2[i] = r * r;
    st.vDrive[i] = Math.sin(w);        // normalises the resonator peak to ~1
    st.vLevel[i] = db(levelDb);
    st.vGainL[i] = Math.sqrt((1 - pan) / 2);
    st.vGainR[i] = Math.sqrt((1 + pan) / 2);
    st.vRate[i] = rate;
    st.vCountdown[i] = nextGap(st, rate);
  }

  const a = Math.exp(-2 * Math.PI * profile.gust_rate_hz / CTRL_SR);
  st.gust[0] = a;
  st.gust[1] = 1 / Math.sqrt(1 - a * a);
  st.gust[2] = 0;
  st.gust[3] = profile.gust_depth_db;
  st.ctrl[0] = Math.max(1, Math.round(sr / CTRL_SR));
  st.ctrl[1] = 0;
  st.gust[4] = 1;
  st.gust[5] = nextGust(st);
  return st;
}

/* A bent ceiling rather than a corner, so dense overlaps cost nothing audible. */
export function softLimit(x) {
  'worklet';
  const mag = x < 0 ? -x : x;
  if (mag <= LIMIT_KNEE) return x;
  const head = 1 - LIMIT_KNEE;
  const bent = LIMIT_KNEE + head * Math.tanh((mag - LIMIT_KNEE) / head);
  return x < 0 ? -bent : bent;
}

// ---------------------------------------------------------------- render ---
/* Fills n frames of L and R. Allocates nothing. */
export function renderRain(st, L, R, n) {
  'worklet';
  const nv = st.nv;
  const stride = st.ctrl[0];

  for (let i = 0; i < n; i++) {
    if (st.ctrl[1] === 0) {
      if (st.arcInfo[0] > 1) arcTick(st);
      st.gust[4] = st.gust[5]; st.gust[5] = nextGust(st);
    }
    const t = st.ctrl[1] / stride;
    const gust = st.gust[4] + (st.gust[5] - st.gust[4]) * t;
    st.ctrl[1] = (st.ctrl[1] + 1) % stride;

    let dropL = 0, dropR = 0;
    for (let v = 0; v < nv; v++) {
      st.vCountdown[v] -= 1;
      let x = 0;
      while (st.vCountdown[v] <= 0) {
        const amp = Math.exp(gaussNext(st) * 0.55);      // lognormal(0, 0.55)
        x += amp * st.vDrive[v];
        st.vClickLeft[v] = CLICK_LEN;
        st.vClickAmp[v] = amp;
        st.vCountdown[v] += nextGap(st, st.vRate[v]);
      }
      const y = st.vA1[v] * st.vY1[v] - st.vA2[v] * st.vY2[v] + x;
      st.vY2[v] = st.vY1[v]; st.vY1[v] = y;
      let s = y;
      if (st.vClickLeft[v] > 0) {         // the impact, before the ring
        s += gaussNext(st) * 0.6 * st.vClickAmp[v];
        st.vClickLeft[v] -= 1;
      }
      s *= st.vLevel[v];
      dropL += s * st.vGainL[v];
      dropR += s * st.vGainR[v];
    }

    // body is lifted 6x because a 4th-order lowpass has taken most of its energy
    const hL = runChain(st.hissCoef, st.hissZ, 1, 2, 0, runSection(st.hissCoef, st.hissZ, 0, 0, gaussNext(st)));
    const hR = runChain(st.hissCoef, st.hissZ, 1, 2, 1, runSection(st.hissCoef, st.hissZ, 0, 1, gaussNext(st)));
    const bL = runChain(st.bodyCoef, st.bodyZ, 0, 2, 0, gaussNext(st)) * 6;
    const bR = runChain(st.bodyCoef, st.bodyZ, 0, 2, 1, gaussNext(st)) * 6;

    // master is exactly 1 without an arc, so this changes nothing there
    const yL = (st.hissLevel * hL + st.bodyLevel * bL + dropL) * gust * st.master[0];
    const yR = (st.hissLevel * hR + st.bodyLevel * bR + dropR) * gust * st.master[0];

    L[i] = softLimit(runSection(st.dcCoef, st.dcZ, 0, 0, yL));
    R[i] = softLimit(runSection(st.dcCoef, st.dcZ, 0, 1, yR));
  }
}
