// EP27+: the village layer on the Isle. Voxel buildings (thatch -> slate/turf roofs, char), open pens that become
// covered barns, a move from site A to site B (each building unbuilds at A and rises at B, staggered), roads painted on
// the voxels (route A or B), carts on the road (their count is the HUD's TRADE), lanterns for night travel, a
// watchtower with a bell, and a cairn whose stones stack on their keys. Everything is a pure function of time.
import React from 'react';
import * as THREE from 'three';
import {sample} from '../keys';
import {clamp, hash2, smoothstep} from '../rng';
import type {Island} from './island';
import type {BuildingRaw, Settlement, World} from './timeline';

const mats = new Map<string, THREE.MeshLambertMaterial>();
const m = (hex: string, emissive = false) => {
	const k = hex + (emissive ? 'e' : '');
	if (!mats.has(k)) {
		const mm = new THREE.MeshLambertMaterial({color: hex});
		if (emissive) mm.emissive = new THREE.Color(hex);
		mats.set(k, mm);
	}
	return mats.get(k)!;
};
const mix = (a: string, b: string, p: number) => (p <= 0.001 ? a : p >= 0.999 ? b : '#' + new THREE.Color(a).lerp(new THREE.Color(b), p).getHexString());
const BOX = new THREE.BoxGeometry(1, 1, 1);
const OUTLINE = new THREE.MeshBasicMaterial({color: '#12151c', side: THREE.BackSide});
const OL = 0.09;

const WALL = '#e3d4b3';
const WALL2 = '#d6c5a1';
const BEAM = '#6b4a30';
const STONE = '#8f8c86';
const THATCH = ['#d8b25a', '#c99f48'];
const SLATE = ['#5b6470', '#4b535e'];
const TURF = ['#6f9a48', '#5f8a3e'];
const CHAR = ['#2e2622', '#3d2f27'];
const WOOD = '#8a5a36';

const Box: React.FC<{s: [number, number, number]; p: [number, number, number]; c: string; o?: boolean; e?: boolean; cast?: boolean}> = ({s, p, c, o = true, e, cast = true}) => (
	<group position={p}>
		<mesh geometry={BOX} material={m(c, e)} scale={s} castShadow={cast} receiveShadow />
		{o && <mesh geometry={BOX} material={OUTLINE} scale={[s[0] + OL, s[1] + OL, s[2] + OL]} />}
	</group>
);

// ---------------------------------------------------------------- state (shared with the HUD)

export type BuildingState = {b: BuildingRaw; i: number; x: number; z: number; rise: number; char: number; roof: number};

const isHome = (b: BuildingRaw) => (b.kind ?? 'house') === 'house' || b.kind === 'hall';

/** Each building's site, rise (0 unbuilt .. 1 standing), char and roof switch at t. */
export const buildingStates = (st: Settlement, t: number): BuildingState[] => {
	const place = sample(st.place, t, 0);
	const charV = sample(st.char, t, 0);
	const roofV = sample(st.roof, t, 0);
	const n = st.buildings.length;
	return st.buildings.map((b, i) => {
		// staggered move: unbuild at A over the first half of its window, rise at B over the second
		const delay = (i / Math.max(1, n - 1)) * 0.55;
		const p = b.b || b.only ? clamp((place - delay) / 0.45) : 0;
		const atB = p >= 0.5;
		let rise = b.b || b.only ? (atB ? smoothstep(0.5, 1, p) : 1 - smoothstep(0, 0.5, p)) : 1;
		if (b.only === 'a' && atB) rise = 0;
		if (b.only === 'b' && !atB) rise = 0;
		const [x, z] = atB && b.b ? b.b : b.a;
		// burning and re-roofing order: a per-building threshold, so roofs go one by one
		const h = hash2(i, 5, 27);
		const char = clamp((charV - h * 0.75) / 0.25);
		const roof = clamp((roofV - h * 0.7) / 0.3);
		return {b, i, x, z, rise, char, roof};
	});
};

/** Standing roofs that aren't burnt (the HUD's ROOFS counter reads the same state the world draws). */
export const roofsIntact = (w: World, t: number) => {
	if (!w.settlement) return 0;
	return buildingStates(w.settlement, t).filter((s) => isHome(s.b) && s.char < 0.5 && !(s.b.only && s.rise < 0.5)).length;
};

const segDist = (x: number, z: number, a: [number, number], b: [number, number]) => {
	const dx = b[0] - a[0];
	const dz = b[1] - a[1];
	const l2 = dx * dx + dz * dz || 1;
	const u = clamp(((x - a[0]) * dx + (z - a[1]) * dz) / l2);
	return Math.hypot(x - (a[0] + dx * u), z - (a[1] + dz * u));
};
const pathDist = (x: number, z: number, pts: [number, number][]) => {
	let d = Infinity;
	for (let i = 0; i + 1 < pts.length; i++) d = Math.min(d, segDist(x, z, pts[i], pts[i + 1]));
	return d;
};

/** How strongly a column is painted as road at t (0..1). */
export const roadAt = (st: Settlement, t: number, x: number, z: number) => {
	const route = sample(st.route, t, 0);
	const ra = st.roads.a.length > 1 && pathDist(x, z, st.roads.a) < 0.8 ? 1 - route : 0;
	const rb = st.roads.b.length > 1 && pathDist(x, z, st.roads.b) < 0.8 ? route : 0;
	return Math.max(ra, rb);
};

const pathPoint = (pts: [number, number][], u: number): [number, number, number] => {
	const lens = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
	const total = lens.reduce((a, b) => a + b, 0);
	let d = u * total;
	for (let i = 0; i < lens.length; i++) {
		if (d <= lens[i] || i === lens.length - 1) {
			const f = clamp(d / lens[i]);
			const a = pts[i];
			const b = pts[i + 1];
			return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, Math.atan2(-(b[1] - a[1]), b[0] - a[0])];
		}
		d -= lens[i];
	}
	return [pts[0][0], pts[0][1], 0];
};

/** Where cart i of N is on a road at sim time s (wraps cleanly for negative s, e.g. after the loop reset). */
export const cartPose = (path: [number, number][], i: number, N: number, s: number) => {
	const dir = i % 2 ? -1 : 1;
	const raw = s * 0.035 * (0.9 + (i % 3) * 0.1) + i / Math.max(4, N) + hash2(i, 2, 9) * 0.1;
	let u = ((raw % 1) + 1) % 1;
	if (dir < 0) u = 1 - u;
	const [x, z, a] = pathPoint(path, u);
	return {x, z, a, dir};
};

export type Target = {kind: 'roof' | 'flock' | 'village' | 'cart'; p: [number, number, number]; r: number; on: boolean};

/**
 * What the dragon can see from the sky at t (EP27's dragon's-eye view). Every target is read from the same state the
 * world draws, so the TARGETS count on screen always matches the village: thatch roofs still standing, flocks in open
 * pens, the village itself while it sits on the open meadow, and carts on the open road by day.
 */
export const dragonTargets = (w: World, island: Island, t: number, s: number): Target[] => {
	const st = w.settlement;
	if (!st) return [];
	const out: Target[] = [];
	const g = (x: number, z: number) => Math.max(island.waterLevel, island.heightAt(x, z));
	for (const b of buildingStates(st, t)) {
		if (!isHome(b.b)) continue;
		out.push({kind: 'roof', p: [b.x, g(b.x, b.z) + 2.0, b.z], r: b.b.kind === 'hall' ? 2.0 : 1.3, on: b.roof < 0.5 && b.char < 0.5 && b.rise > 0.5});
	}
	const place = sample(st.place, t, 0);
	const cover = sample(st.cover, t, 0);
	const herd = sample(w.herd, t, 0);
	w.herdCenters.forEach(([x, z], i) => {
		const bx = w.herdCentersB?.[i]?.[0] ?? x;
		const bz = w.herdCentersB?.[i]?.[1] ?? z;
		const k = clamp(place);
		const hx = x + (bx - x) * k;
		const hz = z + (bz - z) * k;
		out.push({kind: 'flock', p: [hx, g(hx, hz) + 0.6, hz], r: 3.0, on: cover < 0.5 && herd > 1});
	});
	const homes = st.buildings.map((b) => b.a);
	const cx = homes.reduce((a, b) => a + b[0], 0) / homes.length;
	const cz = homes.reduce((a, b) => a + b[1], 0) / homes.length;
	out.push({kind: 'village', p: [cx, g(cx, cz) + 1.5, cz], r: 5.5, on: place < 0.5});
	const route = sample(st.route, t, 0);
	const lantern = sample(st.lanterns, t, 0);
	const trade = sample(w.series[st.tradeKey] ?? [], t, 0);
	const path = route < 0.5 ? st.roads.a : st.roads.b;
	const N = Math.ceil(trade);
	if (path.length > 1)
		for (let i = 0; i < N; i++) {
			const c = cartPose(path, i, N, s);
			out.push({kind: 'cart', p: [c.x, g(c.x, c.z) + 0.6, c.z], r: 0.9, on: route < 0.5 && lantern < 0.5 && trade - i > 0.5});
		}
	return out;
};

// ---------------------------------------------------------------- pieces

const Roof: React.FC<{w: number; d: number; y: number; colors: string[]; holes: number; tall?: number}> = ({w, d, y, colors, holes, tall = 1}) => (
	<group position={[0, y, 0]}>
		<Box s={[w + 0.34, 0.34 * tall, d + 0.34]} p={[0, 0.17 * tall, 0]} c={colors[0]} />
		{holes < 0.75 && <Box s={[w + 0.34, 0.32 * tall, d * 0.64]} p={[0, 0.5 * tall, 0]} c={colors[1]} />}
		{holes < 0.4 && <Box s={[w + 0.34, 0.3 * tall, d * 0.3]} p={[0, 0.8 * tall, 0]} c={colors[0]} />}
	</group>
);

const House: React.FC<{s: BuildingState}> = ({s}) => {
	const b = s.b;
	const kind = b.kind ?? 'house';
	const w = b.w ?? (kind === 'hall' ? 3.2 : kind === 'barn' ? 3.6 : 1.7);
	const d = b.d ?? (kind === 'hall' ? 2.2 : kind === 'barn' ? 2.4 : 1.4);
	const h = b.h ?? (kind === 'hall' ? 1.7 : kind === 'barn' ? 1.15 : 1.1);
	const newRoof = kind === 'barn' ? SLATE : s.i % 2 ? TURF : SLATE;
	let roof = s.roof >= 0.5 ? newRoof : THATCH;
	if (s.char > 0.05) roof = [mix(roof[0], CHAR[0], s.char), mix(roof[1], CHAR[1], s.char)];
	const wall = mix(kind === 'barn' ? WOOD : s.i % 3 ? WALL : WALL2, '#5a4a3e', s.char * 0.55);
	// a re-roofed building gives a little pop
	const pop = s.roof > 0 && s.roof < 1 ? 1 + Math.sin(s.roof * Math.PI) * 0.12 : 1;
	return (
		<group position={[0, 0, 0]} scale={[1, Math.max(0.0001, s.rise), 1]}>
			<Box s={[w + 0.12, 0.28, d + 0.12]} p={[0, 0.14, 0]} c={STONE} />
			<Box s={[w, h, d]} p={[0, 0.28 + h / 2, 0]} c={wall} />
			{kind !== 'barn' && <Box s={[0.12, 0.62, 0.42]} p={[w / 2 + 0.02, 0.6, 0]} c={BEAM} o={false} cast={false} />}
			{kind === 'barn' && <Box s={[0.1, 0.8, 1.2]} p={[w / 2 + 0.02, 0.68, 0]} c={'#4a3020'} o={false} cast={false} />}
			{kind === 'hall' && <Box s={[0.14, h, 0.14]} p={[0, 0.28 + h / 2, d / 2 + 0.02]} c={BEAM} o={false} cast={false} />}
			<group scale={[1, pop, 1]} position={[0, 0.28 + h, 0]}>
				<Roof w={w} d={d} y={0} colors={roof} holes={s.char} tall={kind === 'hall' ? 1.35 : 1} />
			</group>
		</group>
	);
};

const Fence: React.FC<{r: number}> = ({r}) => {
	const n = 14;
	return (
		<group>
			{Array.from({length: n}, (_, k) => {
				const a = (k / n) * Math.PI * 2;
				if (k === 0) return null; // the gate
				return <Box key={k} s={[0.14, 0.62, 0.14]} p={[Math.cos(a) * r, 0.31, Math.sin(a) * r]} c={WOOD} o={false} />;
			})}
			{Array.from({length: n}, (_, k) => {
				if (k === 0 || k === n - 1) return null;
				const a = ((k + 0.5) / n) * Math.PI * 2;
				const len = 2 * r * Math.sin(Math.PI / n);
				return (
					<group key={`r${k}`} position={[Math.cos(a) * r, 0.42, Math.sin(a) * r]} rotation={[0, -a, 0]}>
						<mesh geometry={BOX} material={m('#9a6a42')} scale={[0.08, 0.08, len]} castShadow receiveShadow />
					</group>
				);
			})}
		</group>
	);
};

const Cart: React.FC<{lantern: number}> = ({lantern}) => (
	<group>
		<Box s={[0.85, 0.32, 0.56]} p={[0, 0.34, 0]} c={WOOD} />
		<Box s={[0.7, 0.34, 0.5]} p={[-0.04, 0.66, 0]} c={'#efe3c4'} />
		<Box s={[0.2, 0.2, 0.08]} p={[0.18, 0.12, 0.3]} c={'#2c2420'} o={false} />
		<Box s={[0.2, 0.2, 0.08]} p={[0.18, 0.12, -0.3]} c={'#2c2420'} o={false} />
		{/* the pony */}
		<Box s={[0.6, 0.36, 0.26]} p={[0.92, 0.46, 0]} c={'#5a3c28'} />
		<Box s={[0.24, 0.3, 0.22]} p={[1.28, 0.7, 0]} c={'#4a3020'} />
		<Box s={[0.1, 0.3, 0.1]} p={[0.75, 0.15, 0]} c={'#3a2618'} o={false} />
		<Box s={[0.1, 0.3, 0.1]} p={[1.1, 0.15, 0]} c={'#3a2618'} o={false} />
		{lantern > 0.05 && (
			<>
				<Box s={[0.06, 0.6, 0.06]} p={[0.45, 1.1, 0]} c={'#3a2618'} o={false} cast={false} />
				<Box s={[0.34 * lantern + 0.02, 0.36 * lantern + 0.02, 0.34 * lantern + 0.02]} p={[0.45, 1.5, 0]} c={'#ffe08a'} e o={false} cast={false} />
			</>
		)}
	</group>
);

const SMOKE = Array.from({length: 8}, (_, k) => new THREE.MeshLambertMaterial({color: '#4b4744', transparent: true, opacity: (k + 1) / 8, depthWrite: false}));
const Smoke: React.FC<{t: number; level: number; seed: number}> = ({t, level, seed}) => (
	<group>
		{Array.from({length: 5}, (_, k) => {
			const age = (t * 0.55 + k / 5 + hash2(seed, k, 3) * 0.2) % 1;
			const o = level * (1 - age) * 0.9;
			if (o < 0.06) return null;
			const sc = 0.5 + age * 0.9;
			return (
				<mesh
					key={k}
					geometry={BOX}
					material={SMOKE[Math.min(7, Math.floor(o * 8))]}
					position={[Math.sin(age * 4 + seed) * 0.4 - age * 0.6, 2.2 + age * 3.4, Math.cos(age * 3 + seed) * 0.3]}
					scale={[sc, sc, sc]}
				/>
			);
		})}
	</group>
);

const Tower: React.FC<{x: number; z: number; y: number; h: number; rise: number; swing: number}> = ({x, z, y, h, rise, swing}) => {
	if (rise <= 0.001) return null;
	return (
		<group position={[x, y, z]} scale={[1, rise, 1]}>
			<Box s={[1.7, 0.4, 1.7]} p={[0, 0.2, 0]} c={'#7f7c77'} />
			<Box s={[1.3, h, 1.3]} p={[0, 0.4 + h / 2, 0]} c={'#a29d94'} />
			{[0.3, 0.6].map((f) => (
				<Box key={f} s={[1.36, 0.12, 1.36]} p={[0, 0.4 + h * f, 0]} c={'#8a857d'} o={false} />
			))}
			{/* the open belfry: four posts, a slate cap, the bell */}
			{[
				[0.5, 0.5],
				[-0.5, 0.5],
				[0.5, -0.5],
				[-0.5, -0.5],
			].map(([px, pz], k) => (
				<Box key={k} s={[0.22, 1.3, 0.22]} p={[px, 0.4 + h + 0.65, pz]} c={'#a29d94'} />
			))}
			<Box s={[1.7, 0.3, 1.7]} p={[0, 0.4 + h + 1.42, 0]} c={SLATE[0]} />
			<Box s={[1.1, 0.3, 1.1]} p={[0, 0.4 + h + 1.72, 0]} c={SLATE[1]} />
			<Box s={[0.5, 0.3, 0.5]} p={[0, 0.4 + h + 2.0, 0]} c={SLATE[0]} />
			<group position={[0, 0.4 + h + 1.25, 0]} rotation={[swing, 0, swing * 0.4]}>
				<Box s={[0.6, 0.55, 0.6]} p={[0, -0.38, 0]} c={'#e9a94b'} />
				<Box s={[0.74, 0.14, 0.74]} p={[0, -0.66, 0]} c={'#c98a34'} />
			</group>
		</group>
	);
};

/** The cairn: up to three stones stacked by their keys (the EP28 tease: something on the Isle learns to build). */
const CAIRN: {s: [number, number, number]; y: number; c: string; r: number}[] = [
	{s: [1.1, 0.42, 0.9], y: 0.21, c: '#9a968e', r: 0.2},
	{s: [0.82, 0.38, 0.7], y: 0.61, c: '#b2ada3', r: -0.35},
	{s: [0.56, 0.34, 0.5], y: 0.97, c: '#8c877f', r: 0.5},
];
export const Cairn: React.FC<{x: number; z: number; y: number; stones: number}> = ({x, z, y, stones}) => (
	<group position={[x, y, z]} scale={1.5}>
		{CAIRN.map((c, i) => {
			const k = clamp(stones - i);
			if (k <= 0.001) return null;
			const pop = k < 1 ? 1 - (1 - k) ** 3 + Math.sin(k * Math.PI) * 0.2 : 1;
			return (
				<group key={i} position={[0, c.y + (1 - k) * 0.6, 0]} rotation={[0, c.r, 0]} scale={pop}>
					<mesh geometry={BOX} material={m(c.c)} scale={c.s} castShadow receiveShadow />
					<mesh geometry={BOX} material={OUTLINE} scale={[c.s[0] + OL, c.s[1] + OL, c.s[2] + OL]} />
				</group>
			);
		})}
	</group>
);

// ---------------------------------------------------------------- the layer

export const SettlementLayer: React.FC<{world: World; island: Island; t: number; s: number}> = ({world, island, t, s}) => {
	const st = world.settlement;
	if (!st) return null;
	const states = buildingStates(st, t);
	const smoke = sample(st.smoke, t, 0);
	const cover = sample(st.cover, t, 0);
	const place = sample(st.place, t, 0);
	const route = sample(st.route, t, 0);
	const lantern = sample(st.lanterns, t, 0);
	const trade = sample(world.series[st.tradeKey] ?? [], t, 0);
	const path = route < 0.5 ? st.roads.a : st.roads.b;
	const N = Math.ceil(trade);
	let swing = 0;
	if (st.tower) for (const r of st.tower.rings) if (t >= r) swing += Math.sin((t - r) * 11) * 0.5 * Math.exp(-(t - r) * 1.6);
	return (
		<group>
			{states.map((bs) =>
				bs.rise > 0.001 ? (
					<group key={bs.i} position={[bs.x, island.heightAt(bs.x, bs.z), bs.z]} rotation={[0, ((bs.b.face ?? 0) * Math.PI) / 180, 0]}>
						<House s={bs} />
						{bs.char > 0.05 && smoke > 0.02 && <Smoke t={t} level={smoke * bs.char} seed={bs.i} />}
					</group>
				) : null,
			)}
			{st.pens.map((p, i) => {
				const pp = clamp((place - 0.3 - i * 0.1) / 0.4);
				const atB = p.b && pp >= 0.5;
				const rise = p.b ? (atB ? smoothstep(0.5, 1, pp) : 1 - smoothstep(0, 0.5, pp)) : 1;
				const [x, z] = atB ? p.b! : p.a;
				const r = p.r ?? 2.4;
				const y = island.heightAt(x, z);
				const barn = clamp((cover - i * 0.25) / 0.5);
				if (rise <= 0.001) return null;
				return (
					<group key={`p${i}`} position={[x, y, z]} scale={[1, rise, 1]}>
						<Fence r={r} />
						{barn > 0.001 && (
							<group scale={[1, smoothstep(0, 1, barn), 1]} position={[0, 0, -r - 0.9]}>
								<House s={{b: {kind: 'barn', a: [x, z], w: 2 * r + 0.4, d: 2.2}, i: 100 + i, x, z, rise: 1, char: 0, roof: 1}} />
							</group>
						)}
					</group>
				);
			})}
			{path.length > 1 &&
				Array.from({length: N}, (_, i) => {
					const vis = clamp(trade - i);
					const {x, z, a, dir} = cartPose(path, i, N, s);
					const y = island.heightAt(x, z);
					return (
						<group key={`c${i}`} position={[x, y, z]} rotation={[0, a + (dir < 0 ? Math.PI : 0), 0]} scale={0.85 * (0.3 + 0.7 * vis)}>
							<Cart lantern={lantern} />
						</group>
					);
				})}
			{st.tower && <Tower x={st.tower.x} z={st.tower.z} y={island.heightAt(st.tower.x, st.tower.z)} h={st.tower.h} rise={sample(st.tower.keys, t, 0)} swing={swing} />}
		</group>
	);
};
