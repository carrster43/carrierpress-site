// LOCAL ONLY (the app repos are not on the CI runner). Exports the content the
// free help pages are built from, straight out of each app's own code, so a
// page can never say something the app does not:
//
//   node --experimental-strip-types --no-warnings export_app_help.ts
//   python3 make_app_help.py        # build.py runs it too
//
// help_data/endorsed.json   Endorsed (~/Projects/Cleared): every REVIEWED pack's
//                           exam note, first guide section and first
//                           FREE_QUESTIONS questions: exactly what the app
//                           gives away before the paywall (lib/practice.ts).
// help_data/boatready.json  Boat Ready (~/Projects/BoatReady): requirementsFor()
//                           run for a base boat in each length band, then
//                           again with each one thing changed, so a page can
//                           say what that one thing adds. Bands come from
//                           scanning lengths for where the answer changes.
//
// Re-run after either app's content changes, then rebuild and commit.
import { writeFileSync, mkdirSync } from "node:fs";
import { SHELF } from "../Cleared/lib/content/index.ts";
import { FREE_QUESTIONS } from "../Cleared/lib/content/types.ts";
import { requirementsFor, citation, DISCLAIMER, RULES_AS_OF } from "../BoatReady/lib/requirements.ts";

mkdirSync("help_data", { recursive: true });

// ── Endorsed ────────────────────────────────────────────────────────────────
const packs = SHELF.map((p: any) => ({
  id: p.id, title: p.title, mode: p.mode, examBy: p.examBy, blurb: p.blurb,
  totalQuestions: p.questions.length, totalSections: p.sections.length,
  sectionTitles: p.sections.map((s: any) => s.title),
  first: p.sections[0],
  questions: p.questions.slice(0, FREE_QUESTIONS),
}));
writeFileSync("help_data/endorsed.json", JSON.stringify({ free: FREE_QUESTIONS, packs }, null, 1) + "\n");

// ── Boat Ready ──────────────────────────────────────────────────────────────
const BASE = { propulsion: "outboard", water: "inland", peopleAboard: 4, isCanoeOrKayak: false,
  hasFixedFireSystem: false, hasEnclosedFuelOrEngineSpace: false, hasInstalledToilet: false,
  operatesAtNight: false };
const reqs = (v: any) => requirementsFor(v).map((r: any) => ({ id: r.id, title: r.title, carry: r.carry,
  detail: r.detail, severity: r.severity, cite: citation(r) }));
const sig = (v: any) => JSON.stringify(reqs(v));

// One thing changed at a time, each against the band's base boat.
const VARIANTS: [string, any][] = [
  ["Is used between sunset and sunrise or in poor visibility", { operatesAtNight: true }],
  ["Is used on coastal waters or the Great Lakes", { water: "coastal" }],
  ["Has a closed space where fuel vapour can collect, or a permanent fuel tank", { hasEnclosedFuelOrEngineSpace: true }],
  ["Has an inboard gasoline engine", { propulsion: "inboard-gas", hasEnclosedFuelOrEngineSpace: true }],
  ["Has an installed toilet", { hasInstalledToilet: true }],
];

function diff(a: any[], b: any[]) {
  const byId = new Map(a.map((r) => [r.id, r]));
  const added = b.filter((r) => !byId.has(r.id) || JSON.stringify(byId.get(r.id)) !== JSON.stringify(r));
  const gone = a.filter((r) => !b.some((x) => x.id === r.id)).map((r) => r.title);
  return { added, gone };
}

function band(slug: string, name: string, lo: number, hi: number, base: any, variants = VARIANTS) {
  const at = (L: number, extra: any = {}) => ({ ...base, ...extra, lengthFt: L });
  // Where inside the band the base answer changes (quarter-foot scan).
  const steps: number[] = [];
  let prev = sig(at(lo));
  for (let L = lo + 0.25; L < hi; L += 0.25) {
    const s = sig(at(L));
    if (s !== prev) { steps.push(L); prev = s; }
  }
  return {
    slug, name, lo, hi,
    base: reqs(at(lo)),
    within: steps.map((L) => ({ from: L, ...diff(reqs(at(lo)), reqs(at(L))) })),
    variants: variants.map(([label, extra]) => ({ label, ...diff(reqs(at(lo)), reqs(at(lo, extra))) }))
      .filter((d) => d.added.length || d.gone.length),
  };
}

const KAYAK = { ...BASE, propulsion: "manual", isCanoeOrKayak: true };
const bands = [
  band("kayak-and-canoe", "a kayak or canoe", 8, 16, KAYAK, VARIANTS.slice(0, 2)),
  band("under-16-feet", "a boat under 16 feet", 10, 16, BASE),
  band("16-to-26-feet", "a boat 16 to 26 feet", 16, 26, BASE),
  band("26-to-40-feet", "a boat 26 to 40 feet", 26, 40, BASE),
  band("40-to-65-feet", "a boat 40 to 65 feet", 40, 65, BASE),
];
writeFileSync("help_data/boatready.json",
  JSON.stringify({ rulesAsOf: RULES_AS_OF, disclaimer: DISCLAIMER, base: BASE, bands }, null, 1) + "\n");

console.log(`endorsed: ${packs.length} packs; boatready: ${bands.length} bands, rules as of ${RULES_AS_OF}`);
