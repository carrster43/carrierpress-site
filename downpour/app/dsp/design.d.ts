import type { Profile, Treatments } from "./profiles";
import type { MaterialKey } from "./materials";

export interface Layer { material: MaterialKey; level: number }
export type ControlKey = "intensity" | "dropSize" | "wind" | "distance";
export interface Design {
  layers: Layer[];
  intensity: number;
  dropSize: number;
  wind: number;
  distance: number;
}

export declare const MAX_LAYERS: number;
export declare const SLIDER_STEPS: number;
export declare const LEVEL_STEPS: number;
export declare const CONTROLS: ControlKey[];
export declare const DEFAULT_DESIGN: Readonly<Design>;

export declare function normalizeDesign(raw: unknown): Design;
export declare function shapeProfile(material: Profile, controls: Pick<Design, ControlKey>): Profile;
export declare function designProfile(design: Design): Profile;
export declare function controlWord(key: ControlKey, value: number): string;
export declare function describeDesign(design: Design): string;
export declare function encodeDesign(design: Design): string;
export declare function decodeDesign(text: string): Design | null;
export declare function designFromTreatments(material: MaterialKey, t: Treatments): Design;
