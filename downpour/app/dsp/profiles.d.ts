export type Droplet = [freqHz: number, decayMs: number, hitsPerSec: number, pan: number, levelDb: number];

export interface Profile {
  label: string;
  blurb: string;
  hiss_hp: number; hiss_lp: number; hiss_db: number;
  body_lp: number; body_db: number;
  droplets: Droplet[];
  gust_depth_db: number; gust_rate_hz: number;
}

export type SurfaceKey = "window" | "tent" | "tin_roof" | "car_roof" | "umbrella";
export interface Treatments { slower?: boolean; lower?: boolean }

export declare const PROFILES: Record<SurfaceKey, Profile>;
export declare function slower(p: Profile): Profile;
export declare function lower(p: Profile): Profile;
export declare function buildProfile(key: SurfaceKey, treatments: Treatments): Profile;
