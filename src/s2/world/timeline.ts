// Resolves `episode.world` (the Season 2 world timeline) against the narration timing.
import {cueTime} from '../../lib/timing';
import type {Cue, Timing} from '../../types';
import {integrate, Key, loopFreq, RawKey, resolveKeys, sample} from '../keys';
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
	/** EP34+: a dolly zoom. While this key eases in, the frame's half-height at the target (dist · tan(fov / 2)) is
	 * interpolated instead of the distance, so the subject holds its size while the lens changes and the sky behind
	 * it swells (longer lens) or falls away (wider lens). Absent: dist and fov ease separately, as before. */
	dolly?: boolean;
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
	fields?: {plots: {x: number; z: number; w: number; d: number}[]; ripe: RawKey[]; /** EP31+: 0..1 the fields burn (flames, then char) */ burn?: RawKey[]};
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
		/** EP31+: keyed single figures (a named person in the story), optionally carrying a torch (state `dark` puts it out) */
		figures?: {keys: PredKeyRaw[]; tunic?: string; torch?: boolean; scale?: number}[];
		/** EP31+: one tunic colour per crowd centre (two villages side by side) */
		tints?: string[];
		/** EP31+: the crowd stands still and faces this point */
		watch?: [number, number];
		/** EP32+: 0..1 keys for `watch` (they only stand and face it while > 0.5; absent: always, as in EP31) */
		watchOn?: RawKey[];
		/** EP33+: 0..1 the crowd looks up at the sky (heads tilted back, faces to an overhead camera) */
		look?: RawKey[];
		/** EP33+: 0..1 the share of the crowd holding a lit lamp */
		lamps?: RawKey[];
	};
	/** EP32+: the strata. The island's cut sides carry the war as a layer (`war`: its bottom and top, in world y, keyed
	 * so it can sink as centuries pile on), `centuries` thin bands laid on top of it (0..`max` shown), `fade` (0 vivid ..
	 * 1 forgotten: it greys into the clay), `flood` (0..1: the war's colour climbs up through every century to the
	 * surface) and `veins`: consequences that run from the war layer up to the grass inside a box (x0, x1, z0, z1),
	 * each switched on by `on` (0..1). */
	strata?: StrataRaw;
	/** EP33+: the fear map. Each fear is a shadow on the Isle (`dark` 0..1, a soft creeping disc of radius `r`) and
	 * each belief a light that answers one (`lit` 0..1 grows a lamplit disc of radius `light` from its centre, with a
	 * lamplight rim and, with `lamp`, a lamp post at the centre). `xk` / `zk` move a zone (an eclipse's shadow);
	 * `umbra` zones stay mostly dark inside other lights (lamps burning in the dark); a `rift` is a crack of light
	 * along the segment to `to` (`dark` keys how far it has opened). */
	fears?: FearRaw[];
	/** EP34+: the two skies. The creation myth is a painted dome over the Isle (a sphere of radius `r` centred `y`
	 * below the grass, painted inside: lapis with gilt stars, a gold horizon band and the First Lamp falling at
	 * `lamp`), seen from outside as the sky behind the island. `tears` are holes torn in the paint (each at dome
	 * azimuth / elevation in degrees, radius in degrees; `open` 0..1 grows it, `patch` 0..1 paints it over in fresher
	 * paint), through which the true sky shows (the void). `sheer` 0..1 thins the whole painting (the lamp stays
	 * longest) and `star` is a real falling star whose head runs `from` -> `to` as `fall` goes 0..1. Dome azimuth
	 * follows the camera's: a point at dome az A shows behind the island from a camera at az A + 180. */
	sky?: SkyRaw;
};

export type SkyRaw = {
	r?: number;
	y?: number;
	paint?: RawKey[];
	sheer?: RawKey[];
	lamp?: {az: number; el: number};
	tears?: {az: number; el: number; r: number; open: RawKey[]; patch?: RawKey[]; seed?: number}[];
	star?: {from: [number, number, number]; to: [number, number, number]; fall: RawKey[]};
};
export type SkyNow = {
	r: number;
	y: number;
	paint: number;
	sheer: number;
	lamp: {az: number; el: number};
	tears: {az: number; el: number; r: number; open: number; patch: number; seed: number}[];
	star: {from: [number, number, number]; to: [number, number, number]; fall: number} | null;
};

export type FearRaw = {
	id: string;
	x: number;
	z: number;
	r: number;
	kind?: 'zone' | 'umbra' | 'rift';
	dark?: RawKey[];
	lit?: RawKey[];
	light?: number;
	lamp?: boolean;
	/** how strongly the lit disc tints the ground (default 1; the rim and the push-back are unchanged) */
	glow?: number;
	xk?: RawKey[];
	zk?: RawKey[];
	to?: [number, number];
	label?: string;
	answer?: string;
};
export type FearNow = {id: string; x: number; z: number; r: number; kind: 'zone' | 'umbra' | 'rift'; dark: number; lit: number; light: number; lamp: boolean; glow: number; to?: [number, number]; label?: string; answer?: string};

export type StrataRaw = {
	war: {y0: RawKey[]; y1: RawKey[]};
	surface?: number;
	max?: number;
	centuries?: RawKey[];
	fade?: RawKey[];
	flood?: RawKey[];
	veins?: {box: [number, number, number, number]; color: string; on: RawKey[]; label?: string}[];
};
export type Strata = {y0: number; y1: number; surface: number; max: number; n: number; fade: number; flood: number; veins: {box: [number, number, number, number]; color: string; on: number; label?: string}[]};

/** EP27+ small props. EP29: `offerings` (a candle ring). EP30: `shrine` (an altar between standing stones built up by
 * `rise`; `lights` its candles, `tithe` sheep, `sheaves` and shed `plates` laid before it, `paint` 0..2 the figures
 * painted on its stones). */
export type PropRaw = {
	kind: 'cairn' | 'offerings' | 'shrine' | 'statue' | 'standard' | 'border' | 'relic' | 'lanterns' | 'sheaves' | 'bones' | 'ruin';
	/** EP34 `bones`: a giant's skeleton lying in the ground, unearthed by `rise` (0 buried .. 1 half out); `ruin`: broken
	 * pillars older than anyone, rising out of the ground with `rise`; both turn by `face` and scale by `r` / 2.2 */
	/** EP33 `lanterns`: `n` boats with lamps floating on the water within radius `r`, lit one by one with `lights` (0..1);
	 * `sheaves`: harvest sheaves laid in a ring of radius `r`, popping in one at a time with `sheaves` (a count) */
	n?: number;
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
	/** EP31 `statue`: 0..1 gilded half, 0..1 tarred half, figure scale */
	gild?: RawKey[];
	tar?: RawKey[];
	grow?: RawKey[];
	/** EP31 `standard`: the cloth's colour */
	color?: string;
	/** EP32 `statue`: 0..1 the gilded torch is still in her hand (absent: always) */
	torch?: RawKey[];
	/** EP32 `border`: a line of boundary stones from (x, z) to `to`, rising from the middle outward with `rise`; `skip`
	 * leaves a gap [from, to] along the line (a statue standing on it) */
	to?: [number, number];
	skip?: [number, number];
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
	props: {kind: PropRaw['kind']; x: number; z: number; stones: Key[]; lights: Key[]; r: number; face?: number; tithe?: Key[]; sheaves?: Key[]; plates?: Key[]; rise?: Key[]; paint?: Key[]; gild?: Key[]; tar?: Key[]; grow?: Key[]; color?: string; torch?: Key[]; to?: [number, number]; skip?: [number, number]; n?: number}[];
	/** EP30+ (null before) */
	fields: {plots: {x: number; z: number; w: number; d: number}[]; ripe: Key[]; burn?: Key[]} | null;
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
		figures?: {keys: PredKey[]; tunic: string; torch: boolean; scale: number}[];
		tints?: string[];
		watch?: [number, number];
		watchOn?: Key[];
		look?: Key[];
		lamps?: Key[];
	} | null;
	/** EP32+ (absent before) */
	strata?: {war: {y0: Key[]; y1: Key[]}; surface: number; max: number; centuries: Key[]; fade: Key[]; flood: Key[]; veins: {box: [number, number, number, number]; color: string; on: Key[]; label?: string}[]};
	/** EP33+ (absent before) */
	fears?: {raw: FearRaw; dark: Key[]; lit: Key[]; xk: Key[]; zk: Key[]}[];
	/** EP34+ (absent before) */
	sky?: {raw: SkyRaw; paint: Key[]; sheer: Key[]; tears: {open: Key[]; patch: Key[]}[]; fall: Key[]};
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
		...(p.kind === 'statue' || p.kind === 'standard'
			? {face: p.face ?? 0, rise: resolveKeys(timing, p.rise), gild: resolveKeys(timing, p.gild), tar: resolveKeys(timing, p.tar), grow: resolveKeys(timing, p.grow), ...(p.color ? {color: p.color} : {}), ...(p.torch ? {torch: resolveKeys(timing, p.torch)} : {})}
			: {}),
		// EP32+
		...(p.kind === 'border' ? {rise: resolveKeys(timing, p.rise), to: p.to ?? [p.x, p.z], ...(p.skip ? {skip: p.skip} : {})} : {}),
		...(p.kind === 'relic' ? {face: p.face ?? 0, rise: resolveKeys(timing, p.rise)} : {}),
		// EP33+
		...(p.kind === 'lanterns' ? {n: p.n ?? 6} : {}),
		...(p.kind === 'sheaves' ? {n: p.n ?? 8, sheaves: resolveKeys(timing, p.sheaves)} : {}),
		// EP34+
		...(p.kind === 'bones' || p.kind === 'ruin' ? {face: p.face ?? 0, rise: resolveKeys(timing, p.rise)} : {}),
	})),
	fields: raw.fields ? {plots: raw.fields.plots, ripe: resolveKeys(timing, raw.fields.ripe), ...(raw.fields.burn ? {burn: resolveKeys(timing, raw.fields.burn)} : {})} : null,
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
				...(raw.people.tints ? {tints: raw.people.tints} : {}),
				...(raw.people.watch ? {watch: raw.people.watch} : {}),
				...(raw.people.watchOn ? {watchOn: resolveKeys(timing, raw.people.watchOn)} : {}),
				...(raw.people.look ? {look: resolveKeys(timing, raw.people.look)} : {}),
				...(raw.people.lamps ? {lamps: resolveKeys(timing, raw.people.lamps)} : {}),
				...(raw.people.figures
					? {figures: raw.people.figures.map((f) => ({keys: f.keys.map((k) => ({t: cueTime(timing, k.at), x: k.x, z: k.z, state: k.state ?? 'idle', face: k.face, dur: k.dur ?? 0})).sort((a, b) => a.t - b.t), tunic: f.tunic ?? '#8a5a3a', torch: !!f.torch, scale: f.scale ?? 1}))}
					: {}),
				...(raw.people.gather ? {gather: {at: raw.people.gather.at, r: raw.people.gather.r ?? 3, keys: resolveKeys(timing, raw.people.gather.keys)}} : {}),
			}
		: null,
	rings: (raw.layers?.rings ?? []).map((r) => ({x: r.x, z: r.z, r: r.r, on: cueTime(timing, r.on), off: r.off ? cueTime(timing, r.off) : Infinity, color: r.color ?? '#f4c46e'})),
	...(raw.strata
		? {
				strata: {
					war: {y0: resolveKeys(timing, raw.strata.war.y0), y1: resolveKeys(timing, raw.strata.war.y1)},
					surface: raw.strata.surface ?? 2.55,
					max: raw.strata.max ?? 10,
					centuries: resolveKeys(timing, raw.strata.centuries),
					fade: resolveKeys(timing, raw.strata.fade),
					flood: resolveKeys(timing, raw.strata.flood),
					veins: (raw.strata.veins ?? []).map((v) => ({box: v.box, color: v.color, on: resolveKeys(timing, v.on), ...(v.label ? {label: v.label} : {})})),
				},
			}
		: {}),
	...(raw.fears ? {fears: raw.fears.map((f) => ({raw: f, dark: resolveKeys(timing, f.dark), lit: resolveKeys(timing, f.lit), xk: resolveKeys(timing, f.xk), zk: resolveKeys(timing, f.zk)}))} : {}),
	...(raw.sky
		? {
				sky: {
					raw: raw.sky,
					paint: resolveKeys(timing, raw.sky.paint),
					sheer: resolveKeys(timing, raw.sky.sheer),
					tears: (raw.sky.tears ?? []).map((tr) => ({open: resolveKeys(timing, tr.open), patch: resolveKeys(timing, tr.patch)})),
					fall: resolveKeys(timing, raw.sky.star?.fall),
				},
			}
		: {}),
});

/** EP34+: the painted sky at time t (null when the episode has none). */
export const skyAt = (w: World, t: number): SkyNow | null => {
	const sk = w.sky;
	if (!sk) return null;
	return {
		r: sk.raw.r ?? 56,
		y: sk.raw.y ?? -2,
		paint: sample(sk.paint, t, 1),
		sheer: sample(sk.sheer, t, 0),
		lamp: sk.raw.lamp ?? {az: 180, el: 18},
		tears: (sk.raw.tears ?? []).map((tr, i) => ({az: tr.az, el: tr.el, r: tr.r, open: sample(sk.tears[i].open, t, 0), patch: sample(sk.tears[i].patch, t, 0), seed: tr.seed ?? i * 7 + 3})),
		star: sk.raw.star ? {from: sk.raw.star.from, to: sk.raw.star.to, fall: sample(sk.fall, t, 0)} : null,
	};
};

/** EP34+: a point on the painted dome (dome azimuth / elevation in degrees) in world coordinates. */
export const domePoint = (s: {r: number; y: number}, az: number, el: number): [number, number, number] => {
	const a = (az * Math.PI) / 180;
	const e = (el * Math.PI) / 180;
	return [Math.sin(a) * Math.cos(e) * s.r, s.y + Math.sin(e) * s.r, Math.cos(a) * Math.cos(e) * s.r];
};

/** EP33+: the fear map at time t (null when the episode has none). */
export const fearsAt = (w: World, t: number): FearNow[] | null => {
	if (!w.fears) return null;
	return w.fears.map((f) => ({
		id: f.raw.id,
		x: f.xk.length ? sample(f.xk, t, f.raw.x) : f.raw.x,
		z: f.zk.length ? sample(f.zk, t, f.raw.z) : f.raw.z,
		r: f.raw.r,
		kind: f.raw.kind ?? 'zone',
		dark: sample(f.dark, t, 0),
		lit: sample(f.lit, t, 0),
		light: f.raw.light ?? f.raw.r * 1.05,
		lamp: !!f.raw.lamp,
		glow: f.raw.glow ?? 1,
		...(f.raw.to ? {to: f.raw.to} : {}),
		...(f.raw.label ? {label: f.raw.label} : {}),
		...(f.raw.answer ? {answer: f.raw.answer} : {}),
	}));
};

const sm01 = (v: number) => {
	const p = Math.max(0, Math.min(1, v));
	return p * p * (3 - 2 * p);
};
/** EP33+: how the fear map falls on a ground point: `dark` 0..1 (after the lights push it back), `lit` 0..1 inside a
 * lit disc, `rim` 0..1 on a light's growing edge, `crack` 0..1 on a rift. `n` (0..1, per column) roughens the
 * shadows' edges, which creep slowly with t. */
export const fearLight = (fs: FearNow[], x: number, z: number, n: number, t: number, loopT?: number) => {
	// the edges creep in whole cycles per episode, so the loop has no seam
	const w1 = loopFreq(0.7, loopT);
	const w2 = loopFreq(0.45, loopT);
	let cover = 0;
	let tint = 0;
	let rim = 0;
	let crack = 0;
	for (const f of fs) {
		if (f.kind === 'rift') {
			if (f.dark <= 0.001 || !f.to) continue;
			const vx = f.to[0] - f.x;
			const vz = f.to[1] - f.z;
			const L2 = vx * vx + vz * vz || 1;
			const u = Math.max(0, Math.min(1, ((x - f.x) * vx + (z - f.z) * vz) / L2));
			const d = Math.hypot(x - (f.x + vx * u), z - (f.z + vz * u));
			// the crack opens from its middle outward
			if (Math.abs(u - 0.5) * 2 < f.dark) crack = Math.max(crack, 1 - sm01(d / (0.55 + 0.5 * n)));
			continue;
		}
		if (f.lit <= 0.001) continue;
		const R = f.light * (1 - (1 - Math.min(1, f.lit)) ** 3);
		const d = Math.hypot(x - f.x, z - f.z);
		const cv = (1 - sm01((d - R + 0.5) / 1.0)) * Math.min(1, f.lit * 1.5);
		cover = Math.max(cover, cv);
		tint = Math.max(tint, cv * f.glow);
		rim = Math.max(rim, (Math.abs(d - R) < 0.55 ? 1 : Math.max(0, 1 - (Math.abs(d - R) - 0.55) / 0.4)) * Math.min(1, f.lit * 2));
	}
	let dark = 0;
	for (const f of fs) {
		if (f.kind === 'rift' || f.dark <= 0.001) continue;
		const d = Math.hypot(x - f.x, z - f.z);
		const a = Math.atan2(z - f.z, x - f.x);
		const edge = f.r * (0.94 + 0.08 * Math.sin(a * 3 + t * w1) + 0.05 * Math.sin(a * 5 - t * w2)) - n * 0.6;
		const k = f.dark * (1 - sm01((d - edge + 0.5) / 1.0));
		dark = Math.max(dark, k * (1 - cover * (f.kind === 'umbra' ? 0.3 : 1)));
	}
	return {dark, lit: tint, rim, crack};
};

/** EP32+: the strata at time t (null when the episode has none). */
export const strataAt = (w: World, t: number): Strata | null => {
	const st = w.strata;
	if (!st) return null;
	return {
		y0: sample(st.war.y0, t, -1.3),
		y1: sample(st.war.y1, t, -0.5),
		surface: st.surface,
		max: st.max,
		n: sample(st.centuries, t, st.max),
		fade: sample(st.fade, t, 0),
		flood: sample(st.flood, t, 0),
		veins: st.veins.map((v) => ({box: v.box, color: v.color, on: sample(v.on, t, 0), label: v.label})),
	};
};

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
	if (cur.dolly && !cur.cut && idx > 0) {
		const half = (f: number) => Math.tan(((f / 2) * Math.PI) / 180);
		const fov = lerp(from.fov ?? 24, cur.fov ?? 24);
		const h = lerp(from.dist * half(from.fov ?? 24), cur.dist * half(cur.fov ?? 24));
		return {az, el: lerp(from.el, cur.el), dist: h / half(fov), at: [lerp(from.target[0], cur.target[0]), lerp(from.target[1], cur.target[1]), lerp(from.target[2], cur.target[2])], fov};
	}
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
