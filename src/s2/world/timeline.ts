// Resolves `episode.world` (the Season 2 world timeline) against the narration timing.
import {cueTime} from '../../lib/timing';
import type {Cue, Timing} from '../../types';
import {integrate, Key, RawKey, resolveKeys, sample} from '../keys';
import type {Cam} from './Stage';

export type CamKey = {
	at: Cue;
	dur?: number;
	cut?: boolean;
	az: number;
	el: number;
	dist: number;
	target: [number, number, number];
	fov?: number;
	drift?: number;
	/** EP27+: ride with a dragon. The target becomes the dragon's position (+ `ahead` units along its heading, + `up`),
	 * and `az` is measured from directly behind it (0 = over its tail, positive = orbit to the camera's right). */
	follow?: {dragon: string; ahead?: number; up?: number; look?: [number, number, number]; back?: number};
};
export type Mood = 'day' | 'dusk' | 'gloom' | 'winter' | 'night' | 'golden';
export type LightKey = {at: Cue; dur?: number; mood: Mood};
export type PredKeyRaw = {at: Cue; x: number; z: number; state?: string; face?: number; dur?: number};
export type PredatorRaw = {id: string; scale?: number; keys: PredKeyRaw[]; adorn?: boolean};
export type RingRaw = {x: number; z: number; r: number; on: Cue; off?: Cue; color?: string};

export type WorldRaw = {
	clock?: {label?: string; keys: RawKey[]};
	speed?: RawKey[];
	camera: CamKey[];
	light?: LightKey[];
	herd?: {count: RawKey[]; max?: number; base?: number; centers?: [number, number][]; skin?: 'mossback' | 'sheep'; centersB?: [number, number][]};
	/** HUD predator count (the agents on screen follow it, but the HUD reads this) */
	pred?: RawKey[];
	predators?: PredatorRaw[];
	layers?: {graze?: RawKey[]; snow?: RawKey[]; forest?: RawKey[]; ripple?: Cue[]; rings?: RingRaw[]; dust?: {at: Cue; x: number; z: number; r?: number}[]};
	/** Ambient life, on by default in Season 2: birds circling, pollen motes, glints on water. */
	ambient?: {birds?: number; motes?: number; glints?: boolean};
	/** Shadow-only flyers (a teaser): invisible to the camera, but their shadow crosses the ground from `from` to `to`. */
	flyers?: {kind?: string; at: Cue; dur: number; from: [number, number]; to: [number, number]; height?: number; scale?: number}[];
	/** Seamless loop: at this cue (hide it under a wipe) sim time jumps so it reaches 0 exactly at the episode's end, so
	 * the herd is back where frame 0 has it when the video loops. */
	simLoop?: Cue;
	/** EP27+: extra keyed numbers for the HUD and graphs (e.g. "trade"); the world reads the same keys. */
	series?: Record<string, RawKey[]>;
	/** EP27+: flying voxel dragons (keys may carry an altitude `y`; without it the dragon stands on the ground). */
	dragons?: DragonRaw[];
	/** EP27+: the village layer (buildings, roofs, char, pens/barns, the move to a second site, roads, carts, a tower). */
	settlement?: SettlementRaw;
	/** EP28+: trees to clear (x, z, radius), e.g. along a hook's line of sight */
	clearTrees?: [number, number, number][];
	/** EP28+: more settlements on the Isle (e.g. the human valley beside a new species' village). */
	settlements?: SettlementRaw[];
	/** EP28+: a people walking the Isle (the Fenn): a crowd of `count` around their homes, a keyed `hero`, and their
	 * look (`eyes`, `wet`, `glow`, each 0..1: night eyes, wet teal skin with fins instead of ears, glow spots). */
	folk?: {count: RawKey[]; centers: [number, number][]; centersB?: [number, number][]; site?: RawKey[]; eyes?: RawKey[]; wet?: RawKey[]; glow?: RawKey[]; hero?: PredKeyRaw[]; spread?: number};
	/** EP27+: small props, e.g. a cairn whose stones stack on their keys (`stones`). */
	props?: PropRaw[];
	/** EP30+: crop fields (rectangles of voxel columns) whose crop grows from bare soil (0) through green (0.5) to a
	 * golden harvest (1); a stripped field (grazed bare) is just `ripe` back at 0. */
	fields?: {plots: {x: number; z: number; w: number; d: number}[]; ripe: RawKey[]};
	/** EP29+: mortal people living on the clock (born, ageing, replaced each generation) and the Undying ruler. */
	people?: {
		count: RawKey[];
		centers: [number, number][];
		spread?: number;
		life?: number;
		royal?: RawKey[];
		queue?: {from: [number, number]; dir: [number, number]; count: RawKey[]; gap?: number};
		consort?: {x: number; z: number; face?: number; show: RawKey[]; life?: number};
		ruler?: {keys: PredKeyRaw[]; dais?: {x: number; z: number; face?: number}};
		/** EP30+: the `royal` share wears this robe colour with a hood instead of violet and a circlet (keepers) */
		robe?: string;
		/** EP30+: 0..1 the crowd walks from its homes to a ring around `at` (radius `r`) and faces in (a gathering) */
		gather?: {at: [number, number]; r?: number; keys: RawKey[]};
	};
};

/** EP27+ small props. EP29: `offerings` (a candle ring). EP30: `shrine` (an altar between standing stones built up by
 * `rise`; `lights` its candles, `tithe` sheep, `sheaves` and shed `plates` laid before it, `paint` 0..2 the figures
 * painted on its stones). */
export type PropRaw = {
	kind: 'cairn' | 'offerings' | 'shrine';
	x: number;
	z: number;
	stones?: RawKey[];
	lights?: RawKey[];
	r?: number;
	face?: number;
	tithe?: RawKey[];
	sheaves?: RawKey[];
	plates?: RawKey[];
	rise?: RawKey[];
	paint?: RawKey[];
};

export type DragonKeyRaw = {at: Cue; x: number; z: number; y?: number; state?: string; face?: number; dur?: number; ease?: string};
export type DragonRaw = {id: string; scale?: number; keys: DragonKeyRaw[]};
export type DragonKey = {t: number; x: number; z: number; y: number | null; state: string; face?: number; dur: number; ease: string};

export type BuildingRaw = {
	kind?: 'house' | 'hall' | 'barn' | 'tower' | 'greathall' | 'library';
	/** site A (before the move) and optional site B (after it); without `b` the building stays at `a` */
	a: [number, number];
	b?: [number, number];
	w?: number;
	d?: number;
	h?: number;
	face?: number;
	/** visible only at one site: 'a' leaves at the move, 'b' arrives with it */
	only?: 'a' | 'b';
	/** EP28+: this building's own rise keys (0 unbuilt .. 1 standing), e.g. houses giving way to one great hall */
	show?: RawKey[];
	/** EP28+: at site B it stands on stilts this many units above the ground (a hall on a lake) */
	stiltsB?: number;
};
export type SettlementRaw = {
	buildings: BuildingRaw[];
	/** 0 thatch .. 1 slate/turf (each building switches at its own moment as the value passes it) */
	roof?: RawKey[];
	/** 0 whole .. 1 every roof burnt (each building chars as the value passes it) */
	char?: RawKey[];
	/** smoke intensity over charred roofs */
	smoke?: RawKey[];
	/** pens: 0 open fences .. 1 covered barns over them */
	pens?: {a: [number, number]; b?: [number, number]; r?: number}[];
	cover?: RawKey[];
	/** 0 at site A .. 1 at site B (buildings, pens and herd move, staggered) */
	place?: RawKey[];
	roads?: {a?: [number, number][]; b?: [number, number][]};
	/** 0 road A .. 1 road B */
	route?: RawKey[];
	/** carts on the road: the visible count follows this series (also the HUD's TRADE) */
	tradeKey?: string;
	/** lanterns on the carts (night travel) 0..1 */
	lanterns?: RawKey[];
	/** a watchtower with a bell: rises with `tower` (0..1); the bell swings on each `rings` cue */
	tower?: {x: number; z: number; h?: number; keys: RawKey[]; rings?: Cue[]};
	/** EP28+: 0..1 houses sink into the earth (turf mounds; a nocturnal people living underground) */
	sink?: RawKey[];
	/** EP28+: 0..1 walls turn to dressed stone and stand taller (built to last centuries) */
	stone?: RawKey[];
	/** EP28+: 0..1 walls open into pillars (a hall with no walls, only windows) */
	open?: RawKey[];
	/** EP28+: 0..1 light patterns flicker on the buildings (a people who speak in light) */
	glow?: RawKey[];
};

export type Settlement = {
	buildings: BuildingRaw[];
	roof: Key[];
	char: Key[];
	smoke: Key[];
	pens: {a: [number, number]; b?: [number, number]; r?: number}[];
	cover: Key[];
	place: Key[];
	roads: {a: [number, number][]; b: [number, number][]};
	route: Key[];
	tradeKey: string;
	lanterns: Key[];
	tower: {x: number; z: number; h: number; keys: Key[]; rings: number[]} | null;
	/** EP28+ (empty for EP27) */
	showK: (Key[] | null)[];
	sink: Key[];
	stone: Key[];
	open: Key[];
	glow: Key[];
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
	predators: {id: string; scale: number; keys: PredKey[]; adorn?: boolean}[];
	graze: Key[];
	snow: Key[];
	forest: Key[];
	ripples: number[];
	rings: Ring[];
	dust: {t: number; x: number; z: number; r?: number}[];
	ambient: {birds: number; motes: number; glints: boolean};
	flyers: {kind: string; t: number; dur: number; from: [number, number]; to: [number, number]; height: number; scale: number}[];
	simLoop: number | null;
	/** the episode's length: ambient motion repeats over it, so the loop has no seam */
	loopT: number;
	series: Record<string, Key[]>;
	herdSkin: 'mossback' | 'sheep';
	herdCenters: [number, number][];
	herdCentersB: [number, number][] | null;
	dragons: {id: string; scale: number; keys: DragonKey[]}[];
	settlement: Settlement | null;
	clearTrees: [number, number, number][];
	/** every settlement, the first one included (EP28+: more than one) */
	settlements: Settlement[];
	folk: {count: Key[]; centers: [number, number][]; centersB: [number, number][] | null; site: Key[]; eyes: Key[]; wet: Key[]; glow: Key[]; hero: PredKey[]; spread: number} | null;
	props: {kind: PropRaw['kind']; x: number; z: number; stones: Key[]; lights: Key[]; r: number; face?: number; tithe?: Key[]; sheaves?: Key[]; plates?: Key[]; rise?: Key[]; paint?: Key[]}[];
	/** EP30+ (null before) */
	fields: {plots: {x: number; z: number; w: number; d: number}[]; ripe: Key[]} | null;
	/** EP29+ (null before) */
	people: {
		count: Key[];
		centers: [number, number][];
		spread: number;
		life: number;
		royal: Key[];
		queue: {from: [number, number]; dir: [number, number]; count: Key[]; gap?: number} | null;
		consort: {x: number; z: number; face?: number; show: Key[]; life: number} | null;
		ruler: {keys: PredKey[]; dais?: {x: number; z: number; face?: number}} | null;
		robe?: string;
		gather?: {at: [number, number]; r: number; keys: Key[]};
	} | null;
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
		...(p.adorn ? {adorn: true} : {}),
	})),
	graze: resolveKeys(timing, raw.layers?.graze),
	snow: resolveKeys(timing, raw.layers?.snow),
	forest: resolveKeys(timing, raw.layers?.forest),
	ripples: (raw.layers?.ripple ?? []).map((c) => cueTime(timing, c)),
	dust: (raw.layers?.dust ?? []).map((d) => ({t: cueTime(timing, d.at), x: d.x, z: d.z, r: d.r})),
	ambient: {birds: raw.ambient?.birds ?? 9, motes: raw.ambient?.motes ?? 40, glints: raw.ambient?.glints ?? true},
	flyers: (raw.flyers ?? []).map((f) => ({kind: f.kind ?? 'dragon', t: cueTime(timing, f.at), dur: f.dur, from: f.from, to: f.to, height: f.height ?? 30, scale: f.scale ?? 1})),
	simLoop: raw.simLoop ? cueTime(timing, raw.simLoop) : null,
	loopT: timing.duration,
	herdSkin: raw.herd?.skin ?? 'mossback',
	herdCenters: raw.herd?.centers ?? [[8, -2]],
	herdCentersB: raw.herd?.centersB ?? null,
	series: Object.fromEntries(Object.entries(raw.series ?? {}).map(([k, v]) => [k, resolveKeys(timing, v)])),
	dragons: (raw.dragons ?? []).map((d) => ({
		id: d.id,
		scale: d.scale ?? 1,
		keys: d.keys
			.map((k) => ({t: cueTime(timing, k.at), x: k.x, z: k.z, y: k.y ?? null, state: k.state ?? 'perch', face: k.face, dur: k.dur ?? 0, ease: k.ease ?? 'smooth'}))
			.sort((a, b) => a.t - b.t),
	})),
	settlement: raw.settlement ? resolveSettlement(raw.settlement, timing) : null,
	clearTrees: raw.clearTrees ?? [],
	settlements: [...(raw.settlement ? [raw.settlement] : []), ...(raw.settlements ?? [])].map((st) => resolveSettlement(st, timing)),
	folk: raw.folk
		? {
				count: resolveKeys(timing, raw.folk.count),
				centers: raw.folk.centers,
				centersB: raw.folk.centersB ?? null,
				site: resolveKeys(timing, raw.folk.site),
				eyes: resolveKeys(timing, raw.folk.eyes),
				wet: resolveKeys(timing, raw.folk.wet),
				glow: resolveKeys(timing, raw.folk.glow),
				hero: (raw.folk.hero ?? []).map((k) => ({t: cueTime(timing, k.at), x: k.x, z: k.z, state: k.state ?? 'idle', face: k.face, dur: k.dur ?? 0})).sort((a, b) => a.t - b.t),
				spread: raw.folk.spread ?? 2.6,
			}
		: null,
	props: (raw.props ?? []).map((p) => ({
		kind: p.kind,
		x: p.x,
		z: p.z,
		stones: resolveKeys(timing, p.stones),
		lights: resolveKeys(timing, p.lights),
		r: p.r ?? 2.2,
		// EP30+ (absent before, so older episodes resolve exactly as they did)
		...(p.kind === 'shrine'
			? {face: p.face ?? 0, tithe: resolveKeys(timing, p.tithe), sheaves: resolveKeys(timing, p.sheaves), plates: resolveKeys(timing, p.plates), rise: resolveKeys(timing, p.rise), paint: resolveKeys(timing, p.paint)}
			: {}),
	})),
	fields: raw.fields ? {plots: raw.fields.plots, ripe: resolveKeys(timing, raw.fields.ripe)} : null,
	people: raw.people
		? {
				count: resolveKeys(timing, raw.people.count),
				centers: raw.people.centers,
				spread: raw.people.spread ?? 2.6,
				life: raw.people.life ?? 70,
				royal: resolveKeys(timing, raw.people.royal),
				queue: raw.people.queue ? {...raw.people.queue, count: resolveKeys(timing, raw.people.queue.count)} : null,
				consort: raw.people.consort ? {...raw.people.consort, show: resolveKeys(timing, raw.people.consort.show), life: raw.people.consort.life ?? 60} : null,
				ruler: raw.people.ruler
					? {
							keys: raw.people.ruler.keys.map((k) => ({t: cueTime(timing, k.at), x: k.x, z: k.z, state: k.state ?? 'idle', face: k.face, dur: k.dur ?? 0})).sort((a, b) => a.t - b.t),
							dais: raw.people.ruler.dais,
						}
					: null,
				...(raw.people.robe ? {robe: raw.people.robe} : {}),
				...(raw.people.gather ? {gather: {at: raw.people.gather.at, r: raw.people.gather.r ?? 3, keys: resolveKeys(timing, raw.people.gather.keys)}} : {}),
			}
		: null,
	rings: (raw.layers?.rings ?? []).map((r) => ({x: r.x, z: r.z, r: r.r, on: cueTime(timing, r.on), off: r.off ? cueTime(timing, r.off) : Infinity, color: r.color ?? '#f4c46e'})),
});

function resolveSettlement(st: SettlementRaw, timing: Timing): Settlement {
	return {
		buildings: st.buildings,
		roof: resolveKeys(timing, st.roof),
		char: resolveKeys(timing, st.char),
		smoke: resolveKeys(timing, st.smoke),
		pens: st.pens ?? [],
		cover: resolveKeys(timing, st.cover),
		place: resolveKeys(timing, st.place),
		roads: {a: st.roads?.a ?? [], b: st.roads?.b ?? []},
		route: resolveKeys(timing, st.route),
		tradeKey: st.tradeKey ?? 'trade',
		lanterns: resolveKeys(timing, st.lanterns),
		tower: st.tower ? {x: st.tower.x, z: st.tower.z, h: st.tower.h ?? 7, keys: resolveKeys(timing, st.tower.keys), rings: (st.tower.rings ?? []).map((c) => cueTime(timing, c))} : null,
		showK: st.buildings.map((b) => (b.show ? resolveKeys(timing, b.show) : null)),
		sink: resolveKeys(timing, st.sink),
		stone: resolveKeys(timing, st.stone),
		open: resolveKeys(timing, st.open),
		glow: resolveKeys(timing, st.glow),
	};
}

const smooth = (p: number) => p * p * (3 - 2 * p);
const lerpAngle = (a: number, b: number, p: number) => {
	let d = ((b - a + 540) % 360) - 180;
	return a + d * p;
};

/** Camera at time t: eases from the previous pose to each key over `dur` s (or cuts), plus a slow orbit drift. */
export const cameraAt = (w: World, t: number, ground?: (x: number, z: number) => number): Cam => {
	const cams = w.cams.map((k) => followKey(w, k, t, ground));
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

/** A follow key resolved at time t: its target and azimuth follow the dragon (other keys pass through unchanged). */
const followKey = (w: World, k: World['cams'][number], t: number, ground?: (x: number, z: number) => number): World['cams'][number] => {
	if (!k.follow || !ground) return k;
	const d = w.dragons.find((dd) => dd.id === k.follow!.dragon);
	const p = d ? dragonAt(d.keys, t, ground) : null;
	if (!p) return k;
	if (k.follow.look) {
		// over the shoulder at a fixed point: the camera sits `back` units behind the dragon on the line from `look`
		// through it, `up` above it, aimed at `look` (so the dragon is in the foreground and the point stays framed)
		const L = k.follow.look;
		const D = Math.hypot(p.x - L[0], p.z - L[2]);
		const H = D + (k.follow.back ?? 9);
		const V = p.y + (k.follow.up ?? 4) - L[1];
		const az = (Math.atan2(p.x - L[0], p.z - L[2]) * 180) / Math.PI;
		return {...k, az: az + k.az, el: (Math.atan2(V, H) * 180) / Math.PI, dist: Math.hypot(H, V), drift: 0, target: [L[0] + k.target[0], L[1] + k.target[1], L[2] + k.target[2]]};
	}
	const h = (p.heading * Math.PI) / 180;
	const dir = [Math.cos(h), -Math.sin(h)];
	const ahead = k.follow.ahead ?? 4;
	const behindAz = (Math.atan2(-dir[0], -dir[1]) * 180) / Math.PI;
	return {...k, az: behindAz + k.az, drift: 0, target: [p.x + dir[0] * ahead + k.target[0], p.y + (k.follow.up ?? 0) + k.target[1], p.z + dir[1] * ahead + k.target[2]]};
};

/** Lighting moods. `el` / `az` place the sun (degrees): golden hour is a low sun from the east for long shadows and a warm rim. */
export const MOODS: Record<Mood, {sun: number; warm: number; hemi: number; sky: [string, string, string]; sat: number; el: number; az: number}> = {
	day: {sun: 1.0, warm: 0.35, hemi: 0.95, sky: ['#22375e', '#13244a', '#091228'], sat: 1, el: 49, az: 35},
	dusk: {sun: 0.85, warm: 1.0, hemi: 0.75, sky: ['#4a3150', '#24203f', '#0d1024'], sat: 0.95, el: 30, az: 60},
	gloom: {sun: 0.45, warm: 0.15, hemi: 0.55, sky: ['#1a2230', '#11161f', '#070a10'], sat: 0.35, el: 49, az: 35},
	winter: {sun: 0.9, warm: 0.0, hemi: 1.05, sky: ['#2e4669', '#1a2c4c', '#0b162c'], sat: 0.85, el: 40, az: 35},
	night: {sun: 0.35, warm: 0.0, hemi: 0.5, sky: ['#141d38', '#0b1228', '#050812'], sat: 0.8, el: 49, az: 35},
	// golden hour: a low sun from the camera's right (the hook pose looks from az 24), long shadows, a warm glow
	golden: {sun: 1.3, warm: 1.0, hemi: 0.85, sky: ['#b8704a', '#4e3354', '#151634'], sat: 1.08, el: 16, az: 58},
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
		el: l(from.el, to.el),
		az: l(from.az, to.az),
		sky: [mixHex(from.sky[0], to.sky[0], p), mixHex(from.sky[1], to.sky[1], p), mixHex(from.sky[2], to.sky[2], p)] as [string, string, string],
	};
};

export const simTime = (w: World, t: number) => {
	const s = integrate(w.speed, t, 1);
	if (w.simLoop === null || t < w.simLoop) return s;
	// after the (hidden) loop reset, sim time runs at the same speed but lands on 0 at the episode's end
	return s - integrate(w.speed, w.loopT, 1);
};
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

// ---------------------------------------------------------------- EP27+: the dragon's flight

const AIR_STATES = new Set(['fly', 'glide', 'dive']);
export type DragonPose = {x: number; y: number; z: number; heading: number; air: number; bank: number; state: string; since: number; roar: number};

const dragonPos = (keys: DragonKey[], t: number, ground: (x: number, z: number) => number): [number, number, number, number] | null => {
	if (!keys.length || t < keys[0].t) return null;
	let i = 0;
	while (i + 1 < keys.length && keys[i + 1].t <= t) i++;
	const k = keys[i];
	const yOf = (kk: DragonKey) => (kk.y === null ? ground(kk.x, kk.z) : kk.y);
	if (k.dur > 0 && i > 0) {
		const pk = keys[i - 1];
		const p = Math.min(1, (t - k.t) / k.dur);
		const e = k.ease === 'linear' ? p : smooth(p);
		return [pk.x + (k.x - pk.x) * e, yOf(pk) + (yOf(k) - yOf(pk)) * e, pk.z + (k.z - pk.z) * e, i];
	}
	return [k.x, yOf(k), k.z, i];
};

/** A dragon's pose at t: position (keys with `dur` move from the previous key), heading from its motion (or `face`),
 * `air` 0 perched .. 1 flying (blended over 0.5 s), and a bank into turns. */
export const dragonAt = (keys: DragonKey[], t: number, ground: (x: number, z: number) => number): DragonPose | null => {
	const p = dragonPos(keys, t, ground);
	if (!p) return null;
	const k = keys[p[3]];
	if (k.state === 'hidden') return null;
	const a = dragonPos(keys, t - 0.08, ground) ?? p;
	const b = dragonPos(keys, t + 0.08, ground) ?? p;
	const dx = b[0] - a[0];
	const dz = b[2] - a[2];
	const moving = Math.hypot(dx, dz) > 0.02;
	const heading = moving ? (Math.atan2(-dz, dx) * 180) / Math.PI : (k.face ?? findDragonFace(keys, p[3]));
	// bank: heading change rate (deg/s) -> roll
	let bank = 0;
	if (moving) {
		// turn rate from two short chords; when there's no history before the first key (frame 0), the window shifts
		// forward, so a steady circle banks the same on frame 0 as on the loop's last frame
		const shift = Math.max(0, keys[0].t - (t - 0.2));
		const q1 = dragonPos(keys, t - 0.2 + shift, ground) ?? p;
		const q2 = dragonPos(keys, t - 0.08 + shift, ground) ?? p;
		const q3 = dragonPos(keys, t + 0.08 + shift, ground) ?? p;
		const h0 = Math.atan2(-(q2[2] - q1[2]), q2[0] - q1[0]);
		const h1 = Math.atan2(-(q3[2] - q2[2]), q3[0] - q2[0]);
		let dh = h1 - h0;
		while (dh > Math.PI) dh -= 2 * Math.PI;
		while (dh < -Math.PI) dh += 2 * Math.PI;
		bank = Math.max(-0.5, Math.min(0.5, dh * 2.2));
	}
	const prev = p[3] > 0 ? keys[p[3] - 1] : k;
	const since = t - k.t;
	const airNow = AIR_STATES.has(k.state) ? 1 : 0;
	const airPrev = AIR_STATES.has(prev.state) ? 1 : 0;
	const air = airPrev + (airNow - airPrev) * smooth(Math.min(1, since / 0.5));
	const roar = k.state === 'roar' ? smooth(Math.min(1, since / 0.25)) * (1 - smooth(Math.min(1, Math.max(0, (since - 0.9) / 0.5)))) : 0;
	return {x: p[0], y: p[1], z: p[2], heading, air, bank: bank * air, state: k.state, since, roar};
};

const findDragonFace = (keys: DragonKey[], i: number): number => {
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

/** A HUD series by key: the herd, the predator count, or an episode's extra `series` (EP27: trade). */
export const seriesAt = (w: World, key: string, t: number) => (key === 'herd' ? herdCount(w, t) : key === 'pred' ? sample(w.pred, t, 0) : sample(w.series[key] ?? [], t, 0));
