/*
 * Browser audio host.
 *
 * All the synthesis lives in ../dsp/rain-dsp.js, which the Expo app uses too.
 * This file is only the AudioWorklet shell around it: take a profile over the
 * port, build the state, and fill the output buffer.
 */
import { createRainState, renderRain } from "./dsp/rain-dsp.js";

class RainProcessor extends AudioWorkletProcessor {
  constructor(options) {
    super();
    this.st = null;
    this.port.onmessage = (e) => {
      const d = e.data;
      if (d.type === "profile") this.st = createRainState(d.profile, d.seed >>> 0, sampleRate);
      else if (d.type === "stop") this.st = null;
    };
    const o = options && options.processorOptions;
    if (o && o.profile) this.st = createRainState(o.profile, (o.seed || 1) >>> 0, sampleRate);
  }

  process(inputs, outputs) {
    const out = outputs[0];
    const L = out[0], R = out[1] || out[0];
    if (!this.st) { L.fill(0); if (R !== L) R.fill(0); return true; }
    renderRain(this.st, L, R, L.length);
    return true;
  }
}

registerProcessor("rain-processor", RainProcessor);
