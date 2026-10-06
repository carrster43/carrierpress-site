/*
 * The five surfaces, transcribed verbatim from PROFILES in render_rain.py.
 * These are the product, not a mix: each one is a different place to be
 * standing in the rain, and the numbers are what make it that place.
 *
 * droplets entries are [freq_hz, decay_ms, hits_per_sec, pan, level_db]
 */
export const PROFILES = {
  window: {
    label: "Window",
    blurb: "Rain on glass from a dry room. Bright, glassy ticks over a thin sheet.",
    hiss_hp: 500, hiss_lp: 7500, hiss_db: -12.0,
    body_lp: 260, body_db: -16.0,
    droplets: [
      [1400, 9, 260, -0.70, -20.0],
      [2300, 6, 340, 0.60, -22.0],
      [3600, 4, 420, -0.25, -25.0],
      [850, 14, 90, 0.35, -21.0],
    ],
    gust_depth_db: 2.2, gust_rate_hz: 0.012,
  },

  tent: {
    label: "Tent",
    blurb: "A taut nylon fly over an enclosed volume. Every drop a damped thud with real low end.",
    hiss_hp: 330, hiss_lp: 5200, hiss_db: -13.5,
    body_lp: 420, body_db: -13.0,
    droplets: [
      [330, 26, 110, -0.55, -17.0],
      [560, 18, 165, 0.50, -18.5],
      [900, 12, 230, -0.20, -20.0],
      [1500, 8, 300, 0.30, -22.5],
      [2600, 5, 180, 0.00, -26.0],
    ],
    gust_depth_db: 2.4, gust_rate_hz: 0.010,
  },

  tin_roof: {
    label: "Tin roof",
    blurb: "Corrugated metal. The brightest surface in the line, and the only one that rings.",
    hiss_hp: 420, hiss_lp: 8200, hiss_db: -13.0,
    body_lp: 350, body_db: -14.5,
    droplets: [
      [120, 70, 45, 0.15, -19.0],
      [1100, 42, 190, -0.60, -19.0],
      [1850, 34, 250, 0.55, -20.5],
      [3100, 22, 300, -0.25, -23.0],
      [4600, 14, 200, 0.35, -27.0],
    ],
    gust_depth_db: 2.6, gust_rate_hz: 0.011,
  },

  car_roof: {
    label: "Car roof",
    blurb: "A sealed cabin. The strongest low end here, with a thin glass tick on top.",
    hiss_hp: 280, hiss_lp: 4200, hiss_db: -14.0,
    body_lp: 300, body_db: -11.0,
    droplets: [
      [95, 45, 60, 0.10, -18.0],
      [420, 20, 200, -0.50, -18.0],
      [750, 14, 260, 0.45, -19.5],
      [1250, 9, 280, -0.20, -22.0],
      [2900, 6, 150, 0.30, -26.0],
    ],
    gust_depth_db: 2.0, gust_rate_hz: 0.009,
  },

  umbrella: {
    label: "Umbrella",
    blurb: "Same nylon as the tent, opposite acoustic. Almost no body, and the world stays open.",
    hiss_hp: 420, hiss_lp: 6800, hiss_db: -12.5,
    body_lp: 200, body_db: -21.0,
    droplets: [
      [250, 20, 55, 0.10, -21.0],
      [700, 14, 190, -0.60, -18.0],
      [1200, 10, 250, 0.60, -19.0],
      [2000, 7, 280, -0.30, -21.5],
      [3400, 4, 200, 0.35, -25.0],
    ],
    gust_depth_db: 2.8, gust_rate_hz: 0.014,
  },
};

const clone = (p) => JSON.parse(JSON.stringify(p));

/*
 * Fewer, more spaced drops. Reads as lighter rain easing off rather than rain
 * played at a different speed, which is what people mean by gentle rain.
 */
export function slower(p) {
  const q = clone(p);
  q.droplets = q.droplets.map(([f, d, rate, pan, lvl]) => [f, d, rate * 0.42, pan, lvl]);
  q.hiss_db -= 3.0;
  q.gust_rate_hz *= 0.6;
  return q;
}

/*
 * Darker and heavier. Pulls the top off the sheet, pushes the body up, and
 * drops every resonance a fourth or so. Tends to suit sleep best, because
 * there is nothing bright left to catch on.
 */
export function lower(p) {
  const q = clone(p);
  q.hiss_lp *= 0.60;
  q.hiss_db -= 2.0;
  q.body_lp *= 1.15;
  q.body_db += 3.0;
  q.droplets = q.droplets.map(([f, d, rate, pan, lvl]) => [f * 0.70, d * 1.25, rate, pan, lvl]);
  return q;
}

/* Any surface times any combination of treatments is a separate listening. */
export function buildProfile(key, treatments) {
  let p = clone(PROFILES[key]);
  if (treatments.slower) p = slower(p);
  if (treatments.lower) p = lower(p);
  return p;
}
