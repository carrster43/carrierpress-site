import type { Profile } from "./profiles";

export type MaterialKey =
  | "window" | "tent" | "tin_roof" | "car_roof" | "umbrella"
  | "deck" | "leaves" | "stone" | "puddle";

export declare const MATERIALS: Record<MaterialKey, Profile>;
export declare const MATERIAL_CODES: Record<MaterialKey, string>;
