/*
 * Night Arcs: rain that changes over the night on a planned path.
 *
 * A recording cannot do this without a separate eight hour file per path;
 * Downpour's rain is generated, so an arc is a handful of keyframes and the
 * audio thread glides between them (rain-dsp.js, "night arcs").
 *
 * Each keyframe sets some of the Designer's four controls at a minute mark.
 * Anything a keyframe leaves out stays where the person set it, and the first
 * keyframe is always their own design, so an arc starts from THEIR rain.
 * Layers never change inside an arc: every keyframe has the same droplet
 * voices, which is what lets the engine glide instead of switching.
 */
import { designProfile, normalizeDesign } from "./design.js";

export const ARCS = {
  storm: {
    label: "Storm passing",
    blurb: "Builds for twenty minutes to a heavy, gusty peak, breaks, and eases to a light drizzle by the ninety minute mark.",
    keys: [
      { at: 0 },
      { at: 20, set: { intensity: 0.95, wind: 0.9, dropSize: 0.7 } },
      { at: 35, set: { intensity: 0.8, wind: 0.7, dropSize: 0.65 } },
      { at: 60, set: { intensity: 0.45, wind: 0.45 } },
      { at: 90, set: { intensity: 0.15, wind: 0.25, dropSize: 0.4 } },
    ],
  },
  winddown: {
    label: "Wind down",
    blurb: "Starts as you set it, then over an hour grows lighter, lower and further off, until it is barely there.",
    keys: [
      { at: 0 },
      { at: 60, set: { intensity: 0.15, dropSize: 0.65, wind: 0.25, distance: 0.7 }, gain: 0.3 },
    ],
  },
  showers: {
    label: "Rolling showers",
    blurb: "Rain that comes and goes in waves, about every half hour, for as long as it plays.",
    loop: 30,
    keys: [
      { at: 0 },
      { at: 10, set: { intensity: 0.85, wind: 0.75 } },
      { at: 22, set: { intensity: 0.25, wind: 0.35 } },
      { at: 30 },
    ],
  },
};

export const ARC_KEYS = Object.keys(ARCS);

/** The design at one keyframe: the person's design with that key's settings. */
function keyDesign(design, key) {
  return normalizeDesign({ ...design, ...(key.set || {}) });
}

/**
 * The design as a Profile, with the arc riding along for the audio thread.
 * No arc (or an unknown one) gives the plain profile, unchanged.
 * `timeScale` shrinks minutes for tests; the app never passes it.
 */
export function programProfile(design, arcKey, timeScale = 1) {
  const base = designProfile(design);
  const arc = arcKey ? ARCS[arcKey] : null;
  if (!arc) return base;
  return {
    ...base,
    arc: {
      keys: arc.keys.map((k) => designProfile(keyDesign(design, k))),
      at: arc.keys.map((k) => k.at * 60 * timeScale),
      gain: arc.keys.map((k) => (typeof k.gain === "number" ? k.gain : 1)),
      loop: arc.loop ? arc.loop * 60 * timeScale : 0,
    },
  };
}

/**
 * Where an arc stands `minutes` in, as a design: what the screen and the drop
 * view show. Mirrors the engine's timing (loop, hold at the end, smoothstep)
 * on the controls rather than on the raw profile numbers.
 */
export function arcDesignAt(design, arcKey, minutes) {
  const d = normalizeDesign(design);
  const arc = arcKey ? ARCS[arcKey] : null;
  if (!arc) return d;
  const keys = arc.keys.map((k) => keyDesign(d, k));
  const at = arc.keys.map((k) => k.at);
  let t = Math.max(0, minutes);
  if (arc.loop && t >= arc.loop) t %= arc.loop;
  if (t >= at[at.length - 1]) return keys[keys.length - 1];
  let k = 0;
  while (k < at.length - 2 && t >= at[k + 1]) k++;
  const raw = (t - at[k]) / (at[k + 1] - at[k]);
  const u = raw * raw * (3 - 2 * raw);
  const mix = (a, b) => a + (b - a) * u;
  return {
    layers: d.layers,
    intensity: mix(keys[k].intensity, keys[k + 1].intensity),
    dropSize: mix(keys[k].dropSize, keys[k + 1].dropSize),
    wind: mix(keys[k].wind, keys[k + 1].wind),
    distance: mix(keys[k].distance, keys[k + 1].distance),
  };
}
