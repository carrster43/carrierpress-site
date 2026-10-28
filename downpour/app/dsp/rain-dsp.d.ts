import type { Profile } from "./profiles";

/** Opaque bag of typed arrays. Built once, mutated in place by renderRain. */
export interface RainState { readonly __brand: unique symbol }

export declare const CTRL_SR: number;
export declare const LIMIT_KNEE: number;

export declare function createRainState(profile: Profile, seed: number, sampleRate: number): RainState;
export declare function renderRain(st: RainState, L: Float32Array, R: Float32Array, n: number): void;
export declare function softLimit(x: number): number;
