// Resolves `episode.world` (the Season 2 world timeline) against the narration timing.
import {cueTime} from '../../lib/timing';
import type {Cue, Timing} from '../../types';
import {integrate, Key, RawKey, resolveKeys, sample} from '../keys';
import type {Cam} from './Stage';

export type CamKey = {at: Cue; dur?: number; cut?: boolean; az: number; el: number; dist: number; target: [number, number, number]; fov?: number; drift?: number};
export type Mood = 'day' | 'dusk' | 'gloom' | 'winter' | 'night';
export type LightKey = {at: Cue; dur?: number; mood: Mood};
export type PredKeyRaw = {at: Cue; x: number; z: number; state?: string; face?: number; dur?: number};
export type PredatorRaw = {id: string; scale?: number; keys: PredKeyRaw[]};
export type RingRaw = {x: number; z: number; r: number; on: Cue; off?: Cue; color?: string};

export type WorldRaw = {
	clock?: {label?: string; keys: RawKey[]};
	speed?: RawKey[];
	camera: CamKey[];
	light?: LightKey[];
	herd?: {count: RawKey[]; max?: number; base?: number; centers?: [number, number][]};
	/** HUD predator count (the agents on screen follow it, but the HUD reads this) */
	pred?: RawKey[];
	predators?: PredatorRaw[];
	layers?: {graze?: RawKey[]; snow?: RawKey[]; forest?: RawKey[]; ripple?: Cue[]; rings?: RingRaw[]};
};

export type PredKey = {t: number; x: number; z: number; state: string; face?: number; dur: number};
export type Ring = {x: number; z: number; r: number; on: number; off: number; color: string};

export type World = {
	clock: Key[];
	clockLabel: string;
	speed: Key[];
	cams: (Omit<CamKey, 'at'> & {t: number})[];
	lights: {t: number; dur: number; mood: Mood}[];
	herd: Key[];
	herdMax: number;
	pred: Key[];
	predators: {id: string; scale: number; keys: PredKey[]}[];
	graze: Key[];
	snow: Key[];
	forest: Key[];
	ripples: number[];
	rings: Ring[];
};

export const resolveWorld = (raw: WorldRaw, timing: Timing): World => ({
	clock: resolveKeys(timing, raw.clock?.keys),
	clockLabel: raw.clock?.label ?? 'YEAR',
	speed: resolveKeys(timing, raw.speed),
	cams: raw.camera.map((c) => ({...c, t: cueTime(timing, c.at)})).sort((a, b) => a.t - b.t),
	lights: (raw.light ?? []).map((l) => ({t: cueTime(timing, l.at), dur: l.dur ?? 1.2, mood: l.mood})).sort((a, b) => a.t - b.t),
	herd: resolveKeys(timing, raw.herd?.count),
	herdMax: raw.herd?.max ?? 400,
	pred: resolveKeys(timing, raw.pred),
	predators: (raw.predators ?? []).map((p) => ({
		id: p.id,
		scale: p.scale ?? 1,
		keys: p.keys.map((k) => ({t: cueTime(timing, k.at), x: k.x, z: k.z, state: k.state ?? 'idle', face: k.face, dur: k.dur ?? 0})).sort((a, b) => a.t - b.t),
	})),
	graze: resolveKeys(timing, raw.layers?.graze),
	snow: resolveKeys(timing, raw.layers?.snow),
	forest: resolveKeys(timing, raw.layers?.forest),
	ripples: (raw.layers?.ripple ?? []).map((c) => cueTime(timing, c)),
	rings: (raw.layers?.rings ?? []).map((r) => ({x: r.x, z: r.z, r: r.r, on: cueTime(timing, r.on), off: r.off ? cueTime(timing, r.off) : Infinity, color: r.color ?? '#f4c46e'})),
});

const smooth = (p: number) => p * p * (3 - 2 * p);
const lerpAngle = (a: number, b: number, p: number) => {
	let d = ((b - a + 540) % 360) - 180;
	return a + d * p;
};

/** Camera at time t: eases from the previous pose to each key over `dur` s (or cuts), plus a slow orbit drift. */
export const cameraAt = (w: World, t: number): Cam => {
	const cams = w.cams;
	let cur = cams[0];
	let prev = cams[0];
	for (const c of cams) {
		if (c.t <= t) {
			prev = cur;
			cur = c;
		}
	}
	// Pose reached at the end of each transition; compute the "from" pose recursively (the previous key's final pose).
	const idx = cams.indexOf(cur);
	const from = idx > 0 ? cams[idx - 1] : cur;
	const dur = cur.dur ?? 1.4;
	const p = cur.cut || idx === 0 ? 1 : smooth(Math.min(1, Math.max(0, (t - cur.t) / dur)));
	// Drift: each key may add a slow orbit (deg/s) that accumulates while it is the active key.
	const driftFrom = (from.drift ?? 0) * Math.max(0, cur.t - from.t);
	const driftCur = (cur.drift ?? 0) * Math.max(0, t - cur.t);
	void prev;
	const az0 = from.az + driftFrom;
	const az = lerpAngle(az0, cur.az, p) + driftCur;
	const lerp = (a: number, b: number) => a + (b - a) * p;
	return {
		az,
		el: lerp(from.el, cur.el),
		dist: lerp(from.dist, cur.dist),
		at: [lerp(from.target[0], cur.target[0]), lerp(from.target[1], cur.target[1]), lerp(from.target[2], cur.target[2])],
		fov: lerp(from.fov ?? 24, cur.fov ?? 24),
	};
};

export const MOODS: Record<Mood, {sun: number; warm: number; hemi: number; sky: [string, string, string]; sat: number}> = {
	day: {sun: 1.0, warm: 0.35, hemi: 0.95, sky: ['#22375e', '#13244a', '#091228'], sat: 1},
	dusk: {sun: 0.85, warm: 1.0, hemi: 0.75, sky: ['#4a3150', '#24203f', '#0d1024'], sat: 0.95},
	gloom: {sun: 0.45, warm: 0.15, hemi: 0.55, sky: ['#1a2230', '#11161f', '#070a10'], sat: 0.35},
	winter: {sun: 0.9, warm: 0.0, hemi: 1.05, sky: ['#2e4669', '#1a2c4c', '#0b162c'], sat: 0.85},
	night: {sun: 0.35, warm: 0.0, hemi: 0.5, sky: ['#141d38', '#0b1228', '#050812'], sat: 0.8},
};

const mixHex = (a: string, b: string, p: number) => {
	const pa = parseInt(a.slice(1), 16);
	const pb = parseInt(b.slice(1), 16);
	const ch = (s: number) => Math.round(((pa >> s) & 255) * (1 - p) + ((pb >> s) & 255) * p);
	return `#${((1 << 24) | (ch(16) << 16) | (ch(8) << 8) | ch(0)).toString(16).slice(1)}`;
};

/** Lighting mood at t, blended across keys. */
export const moodAt = (w: World, t: number) => {
	if (!w.lights.length) return MOODS.day;
	let i = 0;
	while (i + 1 < w.lights.length && w.lights[i + 1].t <= t) i++;
	const cur = w.lights[i];
	const from = i > 0 ? MOODS[w.lights[i - 1].mood] : MOODS[cur.mood];
	const to = MOODS[cur.mood];
	const p = t < cur.t ? 0 : smooth(Math.min(1, (t - cur.t) / cur.dur));
	const l = (a: number, b: number) => a + (b - a) * p;
	return {
		sun: l(from.sun, to.sun),
		warm: l(from.warm, to.warm),
		hemi: l(from.hemi, to.hemi),
		sat: l(from.sat, to.sat),
		sky: [mixHex(from.sky[0], to.sky[0], p), mixHex(from.sky[1], to.sky[1], p), mixHex(from.sky[2], to.sky[2], p)] as [string, string, string],
	};
};

export const simTime = (w: World, t: number) => integrate(w.speed, t, 1);
export const herdCount = (w: World, t: number) => sample(w.herd, t, 0);
export const clockAt = (w: World, t: number) => sample(w.clock, t, 0);

/** Predator pose at time t. */
export type PredPose = {x: number; z: number; face: number; state: string; since: number; moving: boolean; until: number};
export const predatorAt = (keys: PredKey[], t: number): PredPose | null => {
	if (!keys.length || t < keys[0].t) return null;
	let i = 0;
	while (i + 1 < keys.length && keys[i + 1].t <= t) i++;
	const k = keys[i];
	const n = keys[i + 1];
	let x = k.x;
	let z = k.z;
	let moving = false;
	// A key with dur > 0 walks from the previous key's spot to its own over `dur` seconds.
	if (k.dur > 0 && i > 0) {
		const pk = keys[i - 1];
		const p = Math.min(1, (t - k.t) / k.dur);
		const e = smooth(p);
		x = pk.x + (k.x - pk.x) * e;
		z = pk.z + (k.z - pk.z) * e;
		moving = p < 1 && Math.hypot(k.x - pk.x, k.z - pk.z) > 0.05;
	}
	let face = k.face ?? 0;
	if (k.face === undefined) {
		const pk = i > 0 ? keys[i - 1] : k;
		const dx = k.x - pk.x;
		const dz = k.z - pk.z;
		face = Math.hypot(dx, dz) > 0.05 ? (Math.atan2(-dz, dx) * 180) / Math.PI : findFace(keys, i);
	}
	return {x, z, face, state: k.state, since: k.t, moving, until: n ? n.t : Infinity};
};

const findFace = (keys: PredKey[], i: number): number => {
	for (let j = i; j >= 0; j--) {
		if (keys[j].face !== undefined) return keys[j].face!;
		if (j > 0) {
			const dx = keys[j].x - keys[j - 1].x;
			const dz = keys[j].z - keys[j - 1].z;
			if (Math.hypot(dx, dz) > 0.05) return (Math.atan2(-dz, dx) * 180) / Math.PI;
		}
	}
	return 0;
};
