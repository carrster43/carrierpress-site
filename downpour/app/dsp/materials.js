/*
 * Every material the Rain Designer can put under the rain.
 *
 * The first five are PROFILES from profiles.js, untouched, so they stay the
 * verbatim transcription of render_rain.py that test/dsp.test.mjs pins. The
 * four below were added 2026-10-14 for the Designer (the 4.3 redesign) and
 * exist only here: render_rain.py does not know them.
 *
 * Same rule as profiles.js: a material is mostly its droplet decay. Hard,
 * dense things (stone) answer in one or two milliseconds; hollow things
 * (a deck) ring for tens; water on water (a puddle) is sparse and long.
 *
 * droplets entries are [freq_hz, decay_ms, hits_per_sec, pan, level_db]
 */
import { PROFILES } from "./profiles.js";

const ADDED = {
  deck: {
    label: "Porch deck",
    blurb: "Rain on wooden boards. Hollow knocks with a soft low ring under them.",
    hiss_hp: 350, hiss_lp: 5600, hiss_db: -14.0,
    body_lp: 380, body_db: -14.0,
    droplets: [
      [180, 30, 70, 0.20, -19.0],
      [420, 18, 180, -0.50, -18.5],
      [780, 11, 240, 0.50, -20.0],
      [1400, 7, 260, -0.20, -23.0],
      [2500, 4, 150, 0.30, -27.0],
    ],
    gust_depth_db: 2.3, gust_rate_hz: 0.011,
  },

  leaves: {
    label: "Forest leaves",
    blurb: "A canopy overhead. Thousands of small soft taps, wide and airy, almost no thud.",
    hiss_hp: 600, hiss_lp: 9000, hiss_db: -11.0,
    body_lp: 220, body_db: -20.0,
    droplets: [
      [600, 7, 160, 0.00, -26.0],
      [900, 5, 300, -0.80, -27.0],
      [1600, 4, 380, 0.80, -27.0],
      [2600, 3, 420, -0.30, -28.0],
      [4200, 2.5, 360, 0.40, -30.0],
    ],
    gust_depth_db: 3.2, gust_rate_hz: 0.016,
  },

  stone: {
    label: "Stone path",
    blurb: "Rain on flagstones. Hard, splashy and bright, with nothing hollow underneath.",
    hiss_hp: 700, hiss_lp: 9500, hiss_db: -12.0,
    body_lp: 240, body_db: -19.0,
    droplets: [
      [700, 5, 140, 0.30, -24.0],
      [1800, 3, 300, -0.60, -23.0],
      [3200, 2, 380, 0.60, -24.0],
      [5200, 1.5, 420, -0.20, -27.0],
    ],
    gust_depth_db: 2.2, gust_rate_hz: 0.012,
  },

  puddle: {
    label: "Puddle",
    blurb: "Drops landing in standing water. Sparse, round plinks over a quiet patter.",
    hiss_hp: 450, hiss_lp: 6000, hiss_db: -13.5,
    body_lp: 300, body_db: -15.5,
    droplets: [
      [600, 20, 90, 0.20, -22.0],
      [1100, 45, 18, -0.40, -20.0],
      [1650, 38, 22, 0.50, -21.0],
      [2400, 30, 26, -0.10, -23.0],
    ],
    gust_depth_db: 2.0, gust_rate_hz: 0.010,
  },
};

export const MATERIALS = { ...PROFILES, ...ADDED };

/*
 * One stable letter per material, for share codes. Never reuse or reorder a
 * letter: a code someone sent last month must still rebuild the same rain.
 */
export const MATERIAL_CODES = {
  window: "W", tent: "T", tin_roof: "M", car_roof: "C", umbrella: "U",
  deck: "D", leaves: "L", stone: "S", puddle: "P",
};
