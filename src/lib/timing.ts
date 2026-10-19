import {createContext, useContext} from 'react';
import {Easing, interpolate} from 'remotion';
import type {Cue, Timing} from '../types';

export const TimingContext = createContext<Timing | null>(null);

export const useTiming = () => {
	const t = useContext(TimingContext);
	if (!t) throw new Error('TimingContext missing');
	return t;
};

const norm = (w: string) => w.toLowerCase().replace(/[^a-z0-9']/g, '');

/** Absolute seconds for a cue (same semantics as pipeline/common.py:resolve_cue). */
export const cueTime = (timing: Timing, cue: Cue | undefined, fallback = 0): number => {
	if (!cue) return fallback;
	const offset = cue.offset ?? 0;
	if (cue.shot) {
		const s = timing.shots.find((x) => x.id === cue.shot);
		if (!s) throw new Error(`Unknown shot cue ${cue.shot}`);
		return s.start + offset;
	}
	const line = timing.lines.find((l) => l.id === cue.line);
	if (!line) throw new Error(`Unknown line cue ${cue.line}`);
	if (!cue.word) return line.start + offset;
	const w = line.words.find((x) => norm(x.text) === norm(cue.word!));
	if (!w) throw new Error(`Word "${cue.word}" not in ${cue.line}`);
	return w.start + offset;
};

/** 0..1 progress from `start` over `dur` seconds, eased. */
export const ease = (t: number, start: number, dur: number, easing = Easing.bezier(0.22, 1, 0.36, 1)) =>
	interpolate(t, [start, start + dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing});

export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;
