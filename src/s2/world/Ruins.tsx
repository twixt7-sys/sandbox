// EP35: a lost civilization's wall and what is dug out in front of it. The wall is the Builders' (older than anyone),
// stone by stone: every block knows whether it is original or a later repair, and how recent that repair is. `log`
// (0..1) is the REPAIR LOG view: original stone darkens to umber and every repair glows quartz cyan by how recent it
// is, so "half this wall is newer than us" can be seen. `fresh` lights the one stone replaced last night (frame 0's
// clue) and `place` sets tonight's stone into its gap. The finds (`gear`, `kitchen`, `wells`, `hands`) rise out of
// the ground (or appear on the wall's face) on their keys. Everything is voxels with no text and no real-world style:
// plain squared blocks, no columns, capitals, carvings or script.
import React, {useMemo} from 'react';
import * as THREE from 'three';
import type {Island} from './island';

const BOX = new THREE.BoxGeometry(1, 1, 1);
const lam = (c: string) => new THREE.MeshLambertMaterial({color: c});

// deterministic hash in [0, 1)
const h01 = (a: number, b: number, s: number) => {
	const v = Math.sin(a * 127.1 + b * 311.7 + s * 74.7) * 43758.5453;
	return v - Math.floor(v);
};

export const QUARTZ = '#4fd6ff';
const STONE = ['#8e8a7c', '#9b9686', '#807c70'];
const REPAIRED = ['#a7a292', '#b0ab9a'];
const UMBER = new THREE.Color('#4b3d33');
const LOG_C = [new THREE.Color('#2f7486'), new THREE.Color('#35aed2'), new THREE.Color('#4fd6ff'), new THREE.Color('#c4f6ff')];
const LOG_E = [0.12, 0.3, 0.55, 1.0];
const MOSS_M = lam('#5f7a4a');
const RUBBLE_M = lam('#857f70');

export type WallBlock = {i: number; r: number; x: number; y: number; z: number; w: number; tilt: number; tone: number; rep: number};

/** The wall's blocks: column i along the line, row r from the bottom. `rep` 0 = original, 1..3 = repaired (3 most
 * recent), 4 = last night's stone (frame 0's clue), 5 = tonight's stone (set by `place`). */
export const wallBlocks = (island: Island, a: [number, number], b: [number, number], profile: number[], fresh: [number, number], tonight: [number, number], seed = 35): WallBlock[] => {
	const n = profile.length;
	const dx = (b[0] - a[0]) / n;
	const dz = (b[1] - a[1]) / n;
	const out: WallBlock[] = [];
	for (let i = 0; i < n; i++) {
		const cx = a[0] + dx * (i + 0.5);
		const cz = a[1] + dz * (i + 0.5);
		const base = Math.max(island.waterLevel, island.heightAt(cx, cz)) - 0.22;
		for (let r = 0; r < profile[i]; r++) {
			const hv = h01(i, r, seed);
			const pRep = 0.3 + 0.09 * r;
			let rep = hv < pRep ? 1 + Math.min(2, Math.floor(h01(r, i, seed + 9) * 3)) : 0;
			if (i === fresh[0] && r === fresh[1]) rep = 4;
			if (i === tonight[0] && r === tonight[1]) rep = 5;
			out.push({
				i,
				r,
				x: cx + (h01(i, r, seed + 3) - 0.5) * 0.06,
				y: base + 0.25 + r * 0.5,
				z: cz + (h01(i, r, seed + 5) - 0.5) * 0.08,
				w: 0.74 + (h01(i, r, seed + 7) - 0.5) * 0.06,
				tilt: rep ? 0 : (h01(i, r, seed + 11) - 0.5) * 0.07,
				tone: Math.floor(h01(i, r, seed + 13) * 3),
				rep,
			});
		}
	}
	return out;
};

export const RuinWall: React.FC<{
	x: number;
	z: number;
	to: [number, number];
	profile: number[];
	fresh: [number, number];
	tonight: [number, number];
	island: Island;
	log: number;
	glow: number;
	place: number;
	seed?: number;
}> = ({x, z, to, profile, fresh, tonight, island, log, glow, place, seed = 35}) => {
	const blocks = useMemo(() => wallBlocks(island, [x, z], to, profile, fresh, tonight, seed), [island, x, z, to, profile, fresh, tonight, seed]);
	// one material per (tone, bucket) so the log can recolour each bucket as a whole
	const mats = useMemo(() => {
		const orig = STONE.map((c) => lam(c));
		const rep = [1, 2, 3, 4, 5].map((k) => lam(REPAIRED[k % 2]));
		return {orig, rep};
	}, []);
	const ang = Math.atan2(to[1] - z, to[0] - x);
	// the repair log: original stone sinks to umber, repairs glow by recency
	const L = Math.max(0, Math.min(1, log));
	mats.orig.forEach((m, k) => {
		m.color.set(STONE[k]).lerp(UMBER, L);
	});
	mats.rep.forEach((m, k) => {
		const bucket = Math.min(3, k); // 0..2 = repairs by recency, 3 = last night and tonight
		const base = new THREE.Color(REPAIRED[(k + 1) % 2]);
		m.color.copy(base).lerp(LOG_C[bucket], L);
		const g = LOG_E[bucket] * L + (k >= 3 ? 0.55 * glow * (1 - L) : 0);
		m.emissive.copy(LOG_C[bucket]).multiplyScalar(g);
		if (k >= 3 && L < 1) m.color.lerp(LOG_C[3], 0.6 * glow * (1 - L));
	});
	return (
		<group>
			{blocks.map((bk, k) => {
				if (bk.rep === 5 && place <= 0.001) return null;
				const drop = bk.rep === 5 ? (1 - place) * 1.1 : 0;
				const m = bk.rep === 0 ? mats.orig[bk.tone] : mats.rep[bk.rep - 1];
				return (
					<mesh key={k} geometry={BOX} material={m} position={[bk.x, bk.y + drop, bk.z]} rotation={[0, -ang + bk.tilt, bk.tilt * 0.4]} scale={[bk.w, 0.46, 0.9]} castShadow receiveShadow />
				);
			})}
			{/* footings down into the turf, so a column never floats over a terrace step */}
			{profile.map((_, i) => {
				const cx = x + ((to[0] - x) / profile.length) * (i + 0.5);
				const cz = z + ((to[1] - z) / profile.length) * (i + 0.5);
				const g = Math.max(island.waterLevel, island.heightAt(cx, cz));
				return <mesh key={`f${i}`} geometry={BOX} material={mats.orig[i % 3]} position={[cx, g - 0.7, cz]} rotation={[0, -ang, 0]} scale={[0.8, 1.0, 0.94]} receiveShadow />;
			})}
			{/* moss on the old tops, and a few fallen blocks in front */}
			{blocks
				.filter((bk) => bk.rep === 0 && !blocks.some((o) => o.i === bk.i && o.r === bk.r + 1))
				.map((bk, k) => (
					<mesh key={`m${k}`} geometry={BOX} material={MOSS_M} position={[bk.x, bk.y + 0.25, bk.z]} rotation={[0, -ang, 0]} scale={[bk.w * 0.9, 0.06, 0.8]} receiveShadow />
				))}
			{[0.18, 0.47, 0.8].map((f, k) => {
				const rx = x + (to[0] - x) * f + 0.2;
				const rz = z + (to[1] - z) * f + 0.95 + k * 0.15;
				return <mesh key={`r${k}`} geometry={BOX} material={RUBBLE_M} position={[rx, Math.max(island.waterLevel, island.heightAt(rx, rz)) + 0.12, rz]} rotation={[0.25, 0.6 + k, 0.15]} scale={[0.62, 0.4, 0.7]} castShadow receiveShadow />;
			})}
		</group>
	);
};

// ---------------------------------------------------------------- the finds

const BRONZE = lam('#b48a45');
const BRONZE2 = lam('#7a5a2c');
const PIT = lam('#3e2c1e');
const PIT_RIM = lam('#6b4e32');
const FLAG = lam('#b8ae96');
const LOWWALL = lam('#8a8576');
const TABLE = lam('#a39b86');
const IRON = lam('#3a3a3e');
const SOOT = lam('#1c1a1a');
const BOWL = lam('#b8774a');
const SAND = lam('#e2cf98');
const MORTAR = lam('#e3d8bc');
const CLAY = lam('#6e3a22');

type Box = [number, number, number, number, number, number, THREE.Material, number?];

const GEAR: Box[] = (() => {
	const out: Box[] = [];
	for (let k = 0; k < 12; k++) {
		const a = (k / 12) * Math.PI * 2;
		out.push([Math.cos(a) * 0.98, Math.sin(a) * 0.98, 0, 0.3, 0.24, 0.22, BRONZE, a]);
	}
	for (let k = 0; k < 16; k++) {
		const a = (k / 16) * Math.PI * 2;
		out.push([Math.cos(a) * 0.74, Math.sin(a) * 0.74, 0, 0.34, 0.2, 0.26, k % 2 ? BRONZE : BRONZE2, a + Math.PI / 2]);
	}
	for (let k = 0; k < 3; k++) out.push([0, 0, 0, 1.36, 0.14, 0.18, BRONZE2, (k / 3) * Math.PI]);
	out.push([0, 0, 0, 0.38, 0.38, 0.34, BRONZE], [0, 0, 0.12, 0.16, 0.16, 0.2, SOOT]);
	return out;
})();

const KITCHEN: Box[] = (() => {
	const out: Box[] = [];
	const W = 3.4;
	const D = 2.3;
	out.push([0, 0.04, 0, W, 0.08, D, FLAG]);
	// low walls (the room's foundations), with a doorway in the front
	out.push([0, 0.24, -D / 2, W + 0.3, 0.48, 0.3, LOWWALL], [-W / 2, 0.24, 0, 0.3, 0.48, D, LOWWALL], [W / 2, 0.24, 0, 0.3, 0.48, D, LOWWALL]);
	out.push([-W / 4 - 0.35, 0.18, D / 2, W / 2 - 0.5, 0.36, 0.3, LOWWALL], [W / 4 + 0.35, 0.18, D / 2, W / 2 - 0.5, 0.36, 0.3, LOWWALL]);
	// one long table for everyone, benches on both sides, bowls along it
	out.push([0.2, 0.48, 0.05, 2.3, 0.1, 0.56, TABLE], [-0.7, 0.24, 0.05, 0.16, 0.42, 0.4, TABLE], [1.1, 0.24, 0.05, 0.16, 0.42, 0.4, TABLE]);
	out.push([0.2, 0.2, -0.48, 2.2, 0.1, 0.22, TABLE], [0.2, 0.2, 0.58, 2.2, 0.1, 0.22, TABLE]);
	for (let k = 0; k < 6; k++) out.push([-0.65 + k * 0.34, 0.58, k % 2 ? 0.2 : -0.1, 0.13, 0.08, 0.13, BOWL]);
	// the hearth at the west end with a great pot on it
	out.push([-1.25, 0.42, -0.55, 0.62, 0.84, 0.7, LOWWALL], [-1.25, 0.38, -0.2, 0.36, 0.36, 0.06, SOOT]);
	out.push([-1.25, 1.02, -0.55, 0.62, 0.42, 0.62, IRON], [-1.25, 1.25, -0.55, 0.7, 0.06, 0.7, IRON]);
	return out;
})();

const WELL = (cx: number, cz: number): Box[] => {
	const out: Box[] = [];
	for (let k = 0; k < 8; k++) {
		const a = (k / 8) * Math.PI * 2;
		out.push([cx + Math.cos(a) * 0.56, 0.26, cz + Math.sin(a) * 0.56, 0.38, 0.52, 0.38, LOWWALL, -a]);
	}
	out.push([cx, 0.42, cz, 0.82, 0.18, 0.82, SAND]);
	return out;
};
const WELLS: Box[] = [...WELL(0, 0), ...WELL(1.5, 0.55), [0.75, 0.1, -0.6, 1.4, 0.2, 0.7, SAND, 0.3], [-0.2, 0.06, 0.9, 0.9, 0.12, 0.6, SAND, -0.4]];

// two child's handprints pressed into a mortar patch on the wall's face (seen straight on)
const HAND = (cx: number, s: number, flip: number): Box[] => {
	const out: Box[] = [[cx, 0, 0.012, 0.1 * s, 0.1 * s, 0.02, CLAY]];
	for (let k = 0; k < 4; k++) out.push([cx + (-0.036 + k * 0.024) * s, 0.09 * s + (k === 1 || k === 2 ? 0.012 * s : 0), 0.012, 0.018 * s, 0.075 * s, 0.02, CLAY]);
	out.push([cx + flip * 0.068 * s, 0.012 * s, 0.012, 0.05 * s, 0.022 * s, 0.02, CLAY, flip * 0.5]);
	return out;
};
const HANDS: Box[] = [[0, 0.02, 0, 0.78, 0.5, 0.02, MORTAR], ...HAND(-0.15, 1.15, -1), ...HAND(0.15, 1.15, 1).map((b) => [b[0], b[1] - 0.06, b[2], b[3], b[4], b[5], b[6], b[7]] as Box)];

/** One find: `gear` (a toothed wheel half out of a dug pit), `kitchen` (a great room with one long table and a hearth),
 * `wells` (two wells filled to the brim with sand), `hands` (a child's handprints in the mortar, on the wall's face at
 * height `y` above the ground), `pit` (just a dug pit: the dig spreading). `rise` 0..1 unearths it (the hands fade
 * up instead). */
export const Find: React.FC<{kind: string; x: number; z: number; face: number; island: Island; rise: number; y?: number; scale?: number}> = ({kind, x, z, face, island, rise, y = 0, scale = 1}) => {
	if (rise <= 0.001) return null;
	// the hands sit on the wall's face: take the ground under the wall (0.47 behind them), not the terrace in front
	const rot = (face * Math.PI) / 180;
	const gx = kind === 'hands' ? x - Math.sin(rot) * 0.47 : x;
	const gz = kind === 'hands' ? z - Math.cos(rot) * 0.47 : z;
	const g = Math.max(island.waterLevel, island.heightAt(gx, gz));
	const parts = kind === 'gear' ? GEAR : kind === 'kitchen' ? KITCHEN : kind === 'wells' ? WELLS : kind === 'pit' ? [] : HANDS;
	const dug = Math.min(1, rise * 1.6);
	if (kind === 'hands') {
		const k = Math.min(1, rise);
		return (
			<group position={[x, g + y, z]} rotation={[0, rot, 0]} scale={[scale, scale * k, scale]}>
				{parts.map(([px, py, pz, sx, sy, sz, m, rz], i) => (
					<mesh key={i} geometry={BOX} material={m} position={[px, py, pz]} rotation={[0, 0, rz ?? 0]} scale={[sx, sy, sz]} receiveShadow />
				))}
			</group>
		);
	}
	const sink = kind === 'gear' ? 0.62 - 1.6 * (1 - rise) : -0.5 * (1 - rise);
	return (
		<group>
			<group position={[x, g, z]} rotation={[0, rot, 0]}>
				{(kind === 'gear' || kind === 'pit') && (
					<>
						<mesh geometry={BOX} material={PIT} position={[0, 0.0, 0.1]} scale={[2.5 * dug * scale, 0.1, 1.5 * dug * scale]} receiveShadow />
						<mesh geometry={BOX} material={PIT_RIM} position={[0, -0.01, 0.1]} scale={[3.0 * dug * scale, 0.1, 2.0 * dug * scale]} receiveShadow />
					</>
				)}
			</group>
			<group position={[x, g + sink * scale, z]} rotation={[kind === 'gear' ? -0.18 : 0, rot, 0]} scale={scale}>
				{parts.map(([px, py, pz, sx, sy, sz, m, r], i) => (
					<mesh
						key={i}
						geometry={BOX}
						material={m}
						position={[px, py, pz]}
						rotation={kind === 'gear' ? [0, 0, r ?? 0] : [0, r ?? 0, 0]}
						scale={[sx, sy, sz]}
						castShadow
						receiveShadow
					/>
				))}
			</group>
		</group>
	);
};
