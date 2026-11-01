// Keyframe helpers for Season 2 timelines. Every value in `episode.world` is keyed to spoken words (cues), resolved
// once per render tab against the measured narration timing, then sampled per frame as a pure function of time.
import type {Cue, Timing} from '../types';
import {cueTime} from '../lib/timing';
import {clamp} from './rng';

/** [cue, value] or [cue, value, easing] where easing is "linear" | "step" | "smooth" (default) */
export type RawKey<T = number> = [Cue, T] | [Cue, T, string];
export type Key<T = number> = {t: number; v: T; e: string};

export const resolveKeys = <T>(timing: Timing, raw: RawKey<T>[] | undefined): Key<T>[] =>
	(raw ?? []).map((k) => ({t: cueTime(timing, k[0]), v: k[1], e: k[2] ?? 'smooth'})).sort((a, b) => a.t - b.t);

const easeFn = (e: string, p: number) => {
	if (e === 'linear') return p;
	if (e === 'step') return p >= 1 ? 1 : 0;
	if (e === 'out') return 1 - (1 - p) * (1 - p);
	if (e === 'in') return p * p;
	return p * p * (3 - 2 * p);
};

/** Sample numeric keys: holds before the first and after the last key; the easing of key k+1 shapes the segment k->k+1. */
export const sample = (keys: Key<number>[], t: number, def = 0) => {
	if (!keys.length) return def;
	if (t <= keys[0].t) return keys[0].v;
	for (let i = 0; i < keys.length - 1; i++) {
		const a = keys[i];
		const b = keys[i + 1];
		if (t < b.t) {
			const p = b.t > a.t ? clamp((t - a.t) / (b.t - a.t)) : 1;
			return a.v + (b.v - a.v) * easeFn(b.e, p);
		}
	}
	return keys[keys.length - 1].v;
};

/** Integral of a piecewise-linear rate from 0 to t (e.g. simulation time from a speed curve). */
export const integrate = (keys: Key<number>[], t: number, def = 1) => {
	if (!keys.length) return t * def;
	let s = 0;
	let prevT = 0;
	let prevV = keys[0].v;
	const pts = [...keys.map((k) => ({t: k.t, v: k.v}))];
	for (const k of pts) {
		if (t <= k.t) {
			const p = k.t > prevT ? (t - prevT) / (k.t - prevT) : 1;
			const vt = prevV + (k.v - prevV) * p;
			return s + ((prevV + vt) / 2) * (t - prevT);
		}
		s += ((prevV + k.v) / 2) * (k.t - prevT);
		prevT = k.t;
		prevV = k.v;
	}
	return s + prevV * (t - prevT);
};

/** 0..1 window: rises over `fade` s after `on`, falls over `fade` s after `off`. */
export const windowed = (t: number, on: number, off = Infinity, fade = 0.4) =>
	clamp((t - on) / fade) * (off === Infinity ? 1 : 1 - clamp((t - off) / fade));
