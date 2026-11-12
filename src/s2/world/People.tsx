// EP29+: ordinary mortal people on the Isle and the one who never dies. Everyone in the crowd lives on the episode's
// clock (YEARS): each person is born, grows up, greys and fades out over their own lifespan, and the next generation
// takes their place in a new colour, so a time-lapse visibly turns the valley over while the Undying Queen stands
// unchanged. Extra pieces: an heir queue (waiting heirs who age in line), a consort who ages beside her and is
// replaced, a `royal` share of the crowd (violet tunics: titles spreading through the generations), and the dais she
// stands on. Faces +x, feet at y = 0. All a pure function of time.
import React from 'react';
import * as THREE from 'three';
import {sample} from '../keys';
import {clamp, hash2, wander} from '../rng';
import type {Island} from './island';
import {clockAt, predatorAt, World} from './timeline';

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
const OL = 0.07;

const B: React.FC<{s: [number, number, number]; p: [number, number, number]; c: string; e?: boolean; o?: boolean; r?: [number, number, number]}> = ({s, p, c, e, o = true, r}) => (
	<group position={p} rotation={r ?? [0, 0, 0]}>
		<mesh geometry={BOX} material={m(c, e)} scale={s} castShadow receiveShadow />
		{o && <mesh geometry={BOX} material={OUTLINE} scale={[s[0] + OL, s[1] + OL, s[2] + OL]} />}
	</group>
);

// the Queen (matched to the field-card sprite): deep violet robe, lavender lining, silver hair, a thin gold circlet
export const VIOLET = '#6a43a0';
const VIOLET_D = '#4c3070';
const LAVENDER = '#bba4c7';
const SILVER = '#ece2e0';
const GOLD = '#e9b85a';
const TRIM = '#d7a9a3';
const SKIN = ['#e8c39e', '#d9a77e', '#b9825c', '#8e5c3e'];
const HAIR = ['#3a2618', '#5a3a22', '#8a5a2e', '#1e1a18', '#a8783a'];
const GREY = '#d9d6d0';
const TUNICS = ['#8a5a3a', '#4f7a8c', '#7a8a4a', '#a0603c', '#5a6a9a', '#9a8a5a', '#6a8a6a', '#a87a4a', '#5a5a6a', '#8a4a4a'];

/** One mortal. `age` 0..1 of their life (child -> adult -> elder); `royal` dresses them in violet with a circlet. */
export const Person: React.FC<{age: number; seed: number; gen: number; gait: number; stride: number; royal?: boolean; tunic?: string; robe?: string}> = ({age, seed, gen, gait, stride, royal, tunic, robe}) => {
	const skin = SKIN[Math.floor(hash2(seed, gen, 31) * SKIN.length)];
	const hair0 = HAIR[Math.floor(hash2(seed, gen, 32) * HAIR.length)];
	const grey = clamp((age - 0.62) / 0.25);
	const hair = mix(hair0, GREY, grey);
	// EP30+: `robe` turns the royal share into hooded keepers in that colour (no gold)
	const hooded = royal && !!robe;
	const coat = hooded ? robe! : royal ? VIOLET : (tunic ?? TUNICS[Math.floor(hash2(seed, gen, 33) * TUNICS.length)]);
	const stoop = clamp((age - 0.8) / 0.2) * 0.22;
	const swing = Math.sin(gait) * 0.5 * stride * (1 - stoop * 2);
	const bob = Math.abs(Math.sin(gait)) * 0.04 * stride;
	return (
		<group position={[0, bob, 0]}>
			{[1, -1].map((side) => (
				<group key={side} position={[0, 0.62, side * 0.12]} rotation={[0, 0, side * swing]}>
					<B s={[0.16, 0.6, 0.16]} p={[0, -0.3, 0]} c={'#4a3a2e'} />
				</group>
			))}
			<group position={[0, 0.62, 0]} rotation={[0, 0, -stoop]}>
				<B s={[0.38, 0.62, 0.36]} p={[0, 0.3, 0]} c={coat} />
				{royal && !hooded && <B s={[0.06, 0.5, 0.2]} p={[0.19, 0.3, 0]} c={GOLD} o={false} />}
				{hooded && <B s={[0.4, 0.42, 0.38]} p={[0, -0.12, 0]} c={coat} />}
				{[1, -1].map((side) => (
					<group key={side} position={[0, 0.54, side * 0.24]} rotation={[0, 0, -side * swing * 0.8]}>
						<B s={[0.11, 0.46, 0.11]} p={[0, -0.23, 0]} c={coat} />
					</group>
				))}
				<group position={[0.02, 0.82, 0]}>
					<B s={[0.36, 0.36, 0.34]} p={[0, 0, 0]} c={skin} />
					<B s={[0.04, 0.05, 0.05]} p={[0.18, 0.04, 0.08]} c={'#14100c'} o={false} />
					<B s={[0.04, 0.05, 0.05]} p={[0.18, 0.04, -0.08]} c={'#14100c'} o={false} />
					<B s={[0.38, 0.12, 0.38]} p={[-0.02, 0.2, 0]} c={hair} />
					<B s={[0.12, 0.26, 0.36]} p={[-0.15, 0.04, 0]} c={hair} />
					{royal && !hooded && <B s={[0.4, 0.06, 0.4]} p={[0, 0.25, 0]} c={GOLD} o={false} />}
					{hooded && <B s={[0.42, 0.16, 0.42]} p={[-0.03, 0.22, 0]} c={coat} />}
					{hooded && <B s={[0.16, 0.34, 0.42]} p={[-0.17, 0.02, 0]} c={coat} />}
				</group>
			</group>
		</group>
	);
};

/** The Undying Queen: a tall, still figure in a long violet robe. `look` 0..1 lifts her head (watching the sky). */
export const Queen: React.FC<{look?: number}> = ({look = 0}) => (
	<group>
		{/* the robe, flaring to the ground */}
		<B s={[0.78, 0.5, 0.74]} p={[-0.03, 0.25, 0]} c={VIOLET_D} />
		<B s={[0.62, 0.6, 0.6]} p={[-0.02, 0.78, 0]} c={VIOLET} />
		<B s={[0.5, 0.56, 0.48]} p={[0, 1.34, 0]} c={VIOLET} />
		{/* the lavender lining down the front, the gold trim at the hem */}
		<B s={[0.06, 1.2, 0.26]} p={[0.32, 0.62, 0]} c={LAVENDER} o={false} />
		<B s={[0.8, 0.07, 0.76]} p={[-0.03, 0.04, 0]} c={TRIM} o={false} />
		{/* sleeves, hands folded in front holding the hourglass */}
		{[1, -1].map((side) => (
			<group key={side} position={[0.02, 1.5, side * 0.28]} rotation={[0, 0, 0.55]}>
				<B s={[0.16, 0.52, 0.16]} p={[0, -0.26, 0]} c={VIOLET} />
			</group>
		))}
		<B s={[0.14, 0.2, 0.14]} p={[0.36, 1.12, 0]} c={GOLD} />
		<B s={[0.1, 0.06, 0.24]} p={[0.32, 1.12, 0]} c={'#efe3c4'} o={false} />
		{/* high collar */}
		<B s={[0.4, 0.14, 0.4]} p={[-0.02, 1.66, 0]} c={VIOLET_D} />
		<group position={[0.02, 1.9, 0]} rotation={[0, 0, look * 0.45]}>
			<B s={[0.36, 0.38, 0.34]} p={[0, 0, 0]} c={'#f1d6c4'} />
			<B s={[0.04, 0.05, 0.05]} p={[0.18, 0.04, 0.08]} c={'#2a1838'} o={false} />
			<B s={[0.04, 0.05, 0.05]} p={[0.18, 0.04, -0.08]} c={'#2a1838'} o={false} />
			{/* long silver hair down her back */}
			<B s={[0.4, 0.12, 0.38]} p={[-0.02, 0.21, 0]} c={SILVER} />
			<B s={[0.16, 1.0, 0.36]} p={[-0.2, -0.38, 0]} c={SILVER} />
			<B s={[0.42, 0.07, 0.4]} p={[0, 0.17, 0]} c={GOLD} o={false} />
			<B s={[0.06, 0.1, 0.08]} p={[0.2, 0.2, 0]} c={GOLD} e o={false} />
		</group>
	</group>
);

/** The dais: a stepped stone platform with a throne and two violet banners. Faces +x. */
export const Dais: React.FC = () => (
	<group>
		<B s={[3.4, 0.3, 3.0]} p={[0, 0.15, 0]} c={'#8f8c86'} />
		<B s={[2.6, 0.3, 2.4]} p={[-0.2, 0.45, 0]} c={'#a9a49a'} />
		<B s={[0.8, 0.4, 1.0]} p={[-0.9, 0.8, 0]} c={'#8f8c86'} />
		<B s={[0.3, 1.5, 1.0]} p={[-1.2, 1.35, 0]} c={'#9b968c'} />
		<B s={[0.32, 0.2, 0.7]} p={[-1.2, 2.2, 0]} c={GOLD} />
		{[1, -1].map((side) => (
			<group key={side} position={[-1.4, 0.6, side * 1.25]}>
				<B s={[0.12, 3.0, 0.12]} p={[0, 1.5, 0]} c={'#5a3c28'} o={false} />
				<B s={[0.06, 1.3, 0.56]} p={[0.06, 2.3, 0]} c={VIOLET} />
				<B s={[0.07, 0.12, 0.56]} p={[0.06, 1.6, 0]} c={GOLD} o={false} />
			</group>
		))}
	</group>
);

/** The person in slot i at clock year y: their generation, and how far through their life they are (0..1). */
export const lifeAt = (i: number, y: number, life: number) => {
	const L = life * (0.8 + 0.4 * hash2(i, 7, 29));
	const off = hash2(i, 8, 29) * L;
	const u = (y + off) / L;
	const gen = Math.floor(u);
	return {gen, age: u - gen};
};

/** Scale over a life: born small, grown by 0.2, shrinks out over the last 4 %. */
const lifeScale = (age: number) => {
	const grow = 0.5 + 0.5 * clamp(age / 0.2);
	const pop = clamp(age / 0.02);
	const fade = 1 - clamp((age - 0.96) / 0.04);
	return grow * Math.min(pop, fade);
};

export const PeopleLayer: React.FC<{world: World; island: Island; t: number; s: number}> = ({world, island, t, s}) => {
	const pw = world.people;
	if (!pw) return null;
	const year = clockAt(world, t);
	const count = sample(pw.count, t, 0);
	const royal = sample(pw.royal, t, 0);
	const N = Math.ceil(count);
	const nodes: React.ReactNode[] = [];
	// EP30+: the crowd gathering in a ring (absent before: g = 0 changes nothing)
	const ga = pw.gather;
	const gat = ga ? sample(ga.keys, t, 0) : 0;
	for (let i = 0; i < N; i++) {
		const vis = clamp(count - i);
		const {gen, age} = lifeAt(i, year, pw.life);
		const sc = lifeScale(age) * vis;
		if (sc < 0.02) continue;
		const c = pw.centers[i % pw.centers.length];
		const a0 = hash2(i, 1, 29) * Math.PI * 2;
		const r0 = Math.sqrt(hash2(i, 2, 29)) * pw.spread;
		let hx = c[0] + Math.cos(a0) * r0;
		let hz = c[1] + Math.sin(a0) * r0;
		let gi = 0;
		if (ga && gat > 0) {
			gi = clamp((gat - hash2(i, 5, 29) * 0.35) / 0.65);
			gi = gi * gi * (3 - 2 * gi);
			const ang = i * 2.39996;
			const rr = ga.r * (0.75 + 0.5 * hash2(i, 6, 29));
			hx += (ga.at[0] + Math.cos(ang) * rr - hx) * gi;
			hz += (ga.at[1] + Math.sin(ang) * rr - hz) * gi;
		}
		const sp = 0.25 + hash2(i, 4, 29) * 0.15;
		const wa = 1.2 * (1 - gi);
		const x = hx + wander(s * sp, i * 3 + 1) * wa;
		const z = hz + wander(s * sp, i * 3 + 2) * wa;
		const x2 = hx + wander((s + 0.2) * sp, i * 3 + 1) * wa;
		const z2 = hz + wander((s + 0.2) * sp, i * 3 + 2) * wa;
		const col = island.columnAt(x, z);
		if (!col || col.biome === 'water') continue;
		const moving = gi < 0.98 && Math.hypot(x2 - x, z2 - z) > 0.02;
		const head = gi > 0.5 && ga ? Math.atan2(-(ga.at[1] - z), ga.at[0] - x) : Math.atan2(-(z2 - z), x2 - x);
		nodes.push(
			<group key={i} position={[x, island.heightAt(x, z), z]} rotation={[0, head, 0]} scale={sc}>
				<Person age={age} seed={i} gen={gen} gait={s * 7 + i} stride={moving ? 1 : 0} royal={hash2(i, gen, 34) < royal} robe={pw.robe} />
			</group>,
		);
	}
	// the heir queue: each slot's heir waits, greys and fades in line; the next one steps in
	if (pw.queue) {
		const q = pw.queue;
		const qn = sample(q.count, t, 0);
		const gap = q.gap ?? 0.9;
		const len = Math.hypot(q.dir[0], q.dir[1]) || 1;
		const [dx, dz] = [q.dir[0] / len, q.dir[1] / len];
		const face = Math.atan2(dz, -dx);
		for (let k = 0; k < Math.ceil(qn); k++) {
			const vis = clamp(qn - k);
			const {gen, age} = lifeAt(500 + k, year, pw.life);
			// heirs join the line grown up: their visible life is the second half of it
			const a = 0.45 + age * 0.55;
			const sc = Math.min(1, clamp(age / 0.04), 1 - clamp((age - 0.95) / 0.05)) * vis;
			if (sc < 0.02) continue;
			const x = q.from[0] + dx * gap * k;
			const z = q.from[1] + dz * gap * k;
			nodes.push(
				<group key={`q${k}`} position={[x, island.heightAt(x, z), z]} rotation={[0, face, 0]} scale={sc}>
					<Person age={a} seed={500 + k} gen={gen} gait={0} stride={0} royal />
				</group>,
			);
		}
	}
	if (pw.consort) {
		const cs = pw.consort;
		const show = sample(cs.show, t, 0);
		if (show > 0.02) {
			const L = cs.life;
			const u = year / L + 0.35;
			const gen = Math.floor(u);
			const age = 0.3 + (u - gen) * 0.7;
			const sc = Math.min(clamp((u - gen) / 0.05), 1 - clamp((u - gen - 0.95) / 0.05)) * show;
			if (sc > 0.02)
				nodes.push(
					<group key="consort" position={[cs.x, island.heightAt(cs.x, cs.z) + 0.6, cs.z]} rotation={[0, ((cs.face ?? 0) * Math.PI) / 180, 0]} scale={1.1 * sc}>
						<Person age={age} seed={900} gen={gen} gait={0} stride={0} tunic={'#3f5a7a'} />
					</group>,
				);
		}
	}
	if (pw.ruler) {
		const d = pw.ruler.dais;
		if (d)
			nodes.push(
				<group key="dais" position={[d.x, island.heightAt(d.x, d.z), d.z]} rotation={[0, ((d.face ?? 0) * Math.PI) / 180, 0]}>
					<Dais />
				</group>,
			);
		const p = predatorAt(pw.ruler.keys, t);
		if (p && p.state !== 'hidden') {
			const since = t - p.since;
			const span = p.until - p.since;
			const look = p.state === 'alert' ? clamp(since / 0.4) * (Number.isFinite(span) ? 1 - clamp((since - span + 0.5) / 0.5) : 1) : 0;
			const y = d && Math.hypot(p.x - d.x, p.z - d.z) < 1.6 ? island.heightAt(d.x, d.z) + 0.6 : island.heightAt(p.x, p.z);
			nodes.push(
				<group key="queen" position={[p.x, y, p.z]} rotation={[0, (p.face * Math.PI) / 180, 0]} scale={1.2}>
					<Queen look={look} />
				</group>,
			);
		}
	}
	return <group>{nodes}</group>;
};

/** EP29's tease for EP30: small offering lights around a spot (people leaving candles for something they fear).
 * `level` 0..1 lights them one by one around the ring; each flame flickers. */
export const Offerings: React.FC<{x: number; z: number; r: number; island: Island; t: number; level: number}> = ({x, z, r, island, t, level}) => {
	if (level <= 0.01) return null;
	const n = 9;
	return (
		<group>
			{Array.from({length: n}, (_, k) => {
				const on = clamp((level - (k / n) * 0.7) / 0.3);
				if (on <= 0.01) return null;
				const a = (k / n) * Math.PI * 2 + 0.3;
				const px = x + Math.cos(a) * r;
				const pz = z + Math.sin(a) * r;
				const fl = 0.75 + 0.25 * Math.sin(t * 17 + k * 2.3);
				return (
					<group key={k} position={[px, island.heightAt(px, pz), pz]} scale={on * 1.6}>
						<B s={[0.16, 0.42, 0.16]} p={[0, 0.21, 0]} c={'#efe3c4'} o={false} />
						<B s={[0.14 * fl, 0.22 * fl, 0.14 * fl]} p={[0, 0.54, 0]} c={'#ffc96a'} e o={false} />
					</group>
				);
			})}
		</group>
	);
};

// ---------------------------------------------------------------- EP30: the shrine and the standing stones

const STONE = '#9b968c';
const STONE_D = '#8a8680';
const MADDER = '#e0687f';
const SHEAF = '#e3c27a';
const SHEAF_D = '#b98a4e';
const PLATE = '#cf7038';

/** The tithe: one sheep (white wool, dark head and legs), standing. Faces +x. */
const Sheep: React.FC = () => (
	<group>
		<B s={[0.56, 0.18, 0.34]} p={[0, 0.09, 0]} c={'#2b2622'} o={false} />
		<B s={[0.84, 0.42, 0.58]} p={[0, 0.39, 0]} c={'#f3efe4'} />
		<B s={[0.3, 0.3, 0.3]} p={[0.5, 0.46, 0]} c={'#24201d'} />
	</group>
);

/**
 * EP30's shrine to the Grimmaw: a stone platform and altar between two standing stones banded in madder, a candle ring
 * (`lights`), and what the village lays before it: `tithe` sheep, `sheaves` of the first harvest and shed `plates`
 * (medicine). Each count pops in one at a time; `rise` builds it up out of the ground; `paint` 0..2 paints a hero on one
 * standing stone and a beast on the other (two tellings of the same story). Faces +x (towards the village).
 */
export const Shrine: React.FC<{x: number; z: number; face: number; r: number; island: Island; t: number; lights: number; tithe: number; sheaves: number; plates: number; rise: number; paint?: number}> = ({x, z, face, r, island, t, lights, tithe, sheaves, plates, rise, paint = 0}) => {
	// `rise` 0..1: the shrine is built up out of the ground (0: no shrine at all)
	if (rise <= 0.001) return null;
	const y = island.heightAt(x, z) - (1 - rise) * 3.2;
	const pop = (k: number) => {
		const v = clamp(k);
		return v < 1 ? 1 - (1 - v) ** 3 + Math.sin(v * Math.PI) * 0.15 : 1;
	};
	return (
		<group>
			<group position={[x, y, z]} rotation={[0, (face * Math.PI) / 180, 0]} scale={1.0}>
				<B s={[2.6, 0.24, 2.2]} p={[0, 0.12, 0]} c={'#8f8c86'} />
				<B s={[0.9, 0.62, 1.1]} p={[-0.2, 0.55, 0]} c={'#a9a49a'} />
				<B s={[1.1, 0.12, 1.3]} p={[-0.2, 0.92, 0]} c={'#bdb6a8'} />
				{[1, -1].map((side) => (
					<group key={side} position={[-0.9, 0.24, side * 0.98]}>
						<B s={[0.46, 2.3, 0.5]} p={[0, 1.15, 0]} c={side > 0 ? STONE : STONE_D} r={[side * 0.05, 0, 0.03]} />
						<B s={[0.5, 0.22, 0.54]} p={[0, 1.75, 0]} c={MADDER} o={false} />
						<B s={[0.5, 0.1, 0.54]} p={[0, 1.42, 0]} c={MADDER} o={false} />
						{/* `paint` 0..2: a hero in gold on one stone, then a beast in rust on the other */}
						{side > 0 ? <Painted kind="hero" color={'#f4c46e'} k={clamp(paint)} /> : <Painted kind="beast" color={'#d0603f'} k={clamp(paint - 1)} />}
					</group>
				))}
				{Array.from({length: 4}, (_, k) => {
					const v = pop(plates - k);
					if (v <= 0.01) return null;
					return (
						<group key={`p${k}`} position={[-0.45 + k * 0.17, 1.02, -0.36 + k * 0.24]} rotation={[0, k * 0.7, 0.25]} scale={v}>
							<B s={[0.22, 0.08, 0.3]} p={[0, 0, 0]} c={PLATE} />
						</group>
					);
				})}
				{Array.from({length: 6}, (_, k) => {
					const v = pop(sheaves - k);
					if (v <= 0.01) return null;
					const zz = -0.75 + (k % 6) * 0.3;
					return (
						<group key={`s${k}`} position={[0.42, 0.24, zz]} rotation={[0, 0, -0.18]} scale={v}>
							<B s={[0.22, 0.72, 0.22]} p={[0, 0.36, 0]} c={SHEAF} />
							<B s={[0.26, 0.08, 0.26]} p={[0, 0.3, 0]} c={SHEAF_D} o={false} />
						</group>
					);
				})}
				{Array.from({length: 6}, (_, k) => {
					const v = pop(tithe - k);
					if (v <= 0.01) return null;
					const zz = (k % 2 ? 1 : -1) * (0.45 + Math.floor(k / 2) * 0.9) - 0.0;
					return (
						<group key={`t${k}`} position={[1.55 + Math.floor(k / 2) * 0.35, 0.24, zz * 0.8]} rotation={[0, Math.PI, 0]} scale={v * 0.85}>
							<Sheep />
						</group>
					);
				})}
			</group>
			<Offerings x={x} z={z} r={r} island={island} t={t} level={lights} />
		</group>
	);
};

/** A figure painted on a standing stone's face (EP30's tease for EP31): `hero` (a person, arms raised) or a beast in
 * profile; `k` 0..1 paints it in. Drawn just proud of the stone's +x face. */
const Painted: React.FC<{kind: 'hero' | 'beast'; color: string; k: number}> = ({kind, color, k}) => {
	if (k <= 0.01) return null;
	const parts: [number, number, number, number, number?][] =
		kind === 'hero'
			? [[0, 1.98, 0.2, 0.2], [0, 1.58, 0.26, 0.52], [0.24, 1.94, 0.07, 0.36, 0.6], [-0.24, 1.94, 0.07, 0.36, -0.6], [0.09, 1.12, 0.08, 0.42], [-0.09, 1.12, 0.08, 0.42]]
			: [[0, 1.58, 0.62, 0.26], [0.36, 1.72, 0.2, 0.18], [0.22, 1.36, 0.07, 0.24], [-0.22, 1.36, 0.07, 0.24], [-0.1, 1.76, 0.36, 0.08], [-0.38, 1.66, 0.14, 0.07]];
	return (
		<group position={[0.27, -0.5, 0]} scale={[1, 1.3, 1.25]}>
			{parts.map(([z, y, w, h, r], i) => (
				<B key={i} s={[0.03, h * k, w]} p={[0, y, z]} c={color} e o={false} r={[r ?? 0, 0, 0]} />
			))}
		</group>
	);
};
