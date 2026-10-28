import type { Profile } from "./profiles";
import type { Design, ControlKey } from "./design";

export type ArcKey = "storm" | "winddown" | "showers";
export interface ArcKeyframe { at: number; set?: Partial<Record<ControlKey, number>>; gain?: number }
export interface Arc { label: string; blurb: string; loop?: number; keys: ArcKeyframe[] }

export declare const ARCS: Record<ArcKey, Arc>;
export declare const ARC_KEYS: ArcKey[];
export declare function programProfile(design: Design, arcKey: ArcKey | null, timeScale?: number): Profile;
export declare function arcDesignAt(design: Design, arcKey: ArcKey | null, minutes: number): Design;
