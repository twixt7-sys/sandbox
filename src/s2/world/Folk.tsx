// EP28+: the Fenn, a small intelligent lakeshore people, as voxels with the Grimmaw's dark outline. One model morphs
// between the "lazy version" (a human with pointy ears: tan skin, hair, a tunic, small eyes) and the real Fenn, trait
// by trait: `eyes` (big dark night eyes), `wet` (glossy teal skin, fin frills instead of ears, a reed sash), `glow`
// (aqua spots that pulse, the way they speak). A crowd walks around their homes in sim time; a keyed hero can stack a
// stone. Faces +x, feet at y = 0.
import React from 'react';
import * as THREE from 'three';
import {loopFreq, sample} from '../keys';
import {clamp, hash2, wander} from '../rng';
import type {Island} from './island';
import {buildingStates} from './Settlement';
import {predatorAt, World} from './timeline';

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

export type FennLook = {eyes: number; wet: number; glow: number};

const SKIN_H = '#e2b48a';
const SKIN_F = '#4fc4a8';
const BACK_F = '#37977f';
const BELLY_F = '#a8dcc0';
const TUNIC = '#8a5a3a';
const HAIR = '#5a3a22';
const SASH = '#b89a5a';
const GLOW = '#7ff5d8';

/** One Fenn. `gait` drives the walk; `stack` 0..1 raises its arms with a stone overhead; `pulse` animates the glow. */
export const Fenn: React.FC<{look: FennLook; gait: number; stride: number; stack?: number; pulse: number; scale?: number}> = ({look, gait, stride, stack = 0, pulse, scale = 1}) => {
	const {eyes, wet, glow} = look;
	const skin = mix(SKIN_H, SKIN_F, wet);
	const back = mix(SKIN_H, BACK_F, wet);
	const belly = mix(SKIN_H, BELLY_F, wet);
	const swing = Math.sin(gait) * 0.55 * stride;
	const bob = Math.abs(Math.sin(gait)) * 0.04 * stride;
	const armUp = stack * 2.6;
	const eyeS = 0.06 + 0.11 * eyes;
	const g = glow * (0.55 + 0.45 * Math.max(0, Math.sin(pulse)));
	return (
		<group scale={scale}>
			<group position={[0, bob, 0]}>
				{/* legs (pivot at the hip) */}
				{[1, -1].map((side) => (
					<group key={side} position={[0, 0.62, side * 0.12]} rotation={[0, 0, side * swing]}>
						<B s={[0.16, 0.6, 0.16]} p={[0, -0.3, 0]} c={back} />
						<B s={[0.34 * (0.7 + 0.3 * wet), 0.08, 0.22]} p={[0.07, -0.6, 0]} c={wet > 0.5 ? skin : '#4a3424'} />
					</group>
				))}
				{/* body */}
				<B s={[0.34, 0.56, 0.34]} p={[0, 0.9, 0]} c={back} />
				<B s={[0.06, 0.44, 0.26]} p={[0.17, 0.88, 0]} c={belly} o={false} />
				{wet < 0.5 ? <B s={[0.38, 0.4, 0.38]} p={[0, 0.82, 0]} c={TUNIC} /> : <B s={[0.38, 0.08, 0.38]} p={[0, 0.78, 0]} c={SASH} r={[0.5, 0, 0]} />}
				{/* arms (pivot at the shoulder); raised overhead with a stone when stacking */}
				{[1, -1].map((side) => (
					<group key={side} position={[0, 1.12, side * 0.23]} rotation={[0, 0, -side * swing * 0.8 + armUp]}>
						<B s={[0.11, 0.48, 0.11]} p={[0, -0.24, 0]} c={skin} />
						{g > 0.02 && <B s={[0.05, 0.06, 0.05]} p={[0.06, -0.2, 0]} c={GLOW} e o={false} />}
						{g > 0.02 && <B s={[0.05, 0.06, 0.05]} p={[0.06, -0.36, 0]} c={GLOW} e o={false} />}
					</group>
				))}
				{stack > 0.05 && <B s={[0.36, 0.22, 0.3]} p={[0.02, 1.12 + 0.62 * Math.min(1, stack * 1.3), 0]} c={'#9a968e'} />}
				{/* head */}
				<group position={[0, 1.38, 0]}>
					<B s={[0.4, 0.36, 0.38]} p={[0, 0, 0]} c={skin} />
					<B s={[0.1, 0.1, 0.12]} p={[0.22, -0.05, 0]} c={skin} o={false} />
					{/* eyes: small and human, or large dark night eyes */}
					{[1, -1].map((side) => (
						<group key={side}>
							<B s={[0.04, eyeS, eyeS]} p={[0.2, 0.04, side * 0.1]} c={'#0c1014'} o={false} />
							{eyes > 0.4 && <B s={[0.02, 0.03, 0.03]} p={[0.215, 0.07, side * 0.12]} c={'#e8fff8'} e o={false} />}
						</group>
					))}
					{g > 0.02 && [1, -1].map((side) => <B key={`c${side}`} s={[0.05, 0.05, 0.03]} p={[0.12, -0.08, side * 0.2]} c={GLOW} e o={false} />)}
					{/* pointy ears (the lazy version) or fin frills (the Fenn) */}
					{wet < 0.5
						? [1, -1].map((side) => <B key={side} s={[0.06, 0.24, 0.07]} p={[-0.04, 0.12, side * 0.22]} c={skin} r={[side * -0.5, 0, 0.4]} />)
						: [1, -1].map((side) => (
								<group key={side}>
									<B s={[0.22, 0.2, 0.04]} p={[-0.06, 0.04, side * 0.22]} c={back} r={[side * -0.35, 0, 0.25]} />
									<B s={[0.05, 0.12, 0.04]} p={[-0.16, 0.18, side * 0.24]} c={back} r={[side * -0.35, 0, 0.5]} o={false} />
								</group>
							))}
					{wet < 0.5 ? <B s={[0.42, 0.1, 0.4]} p={[-0.02, 0.2, 0]} c={HAIR} /> : <B s={[0.24, 0.08, 0.06]} p={[-0.06, 0.2, 0]} c={back} o={false} />}
				</group>
			</group>
		</group>
	);
};

/** Fenn look at t (the editor's sliders: each trait morphs the body). */
export const fennLook = (w: World, t: number): FennLook => {
	const f = w.folk;
	if (!f) return {eyes: 1, wet: 1, glow: 1};
	return {eyes: clamp(sample(f.eyes, t, 1)), wet: clamp(sample(f.wet, t, 1)), glow: clamp(sample(f.glow, t, 1))};
};

/** A deck under (x, z): a building standing on stilts covers it (EP28: the hall on the lake). */
const deckAt = (w: World, island: Island, t: number, x: number, z: number): number | null => {
	for (const st of w.settlements)
		for (const b of buildingStates(st, t)) {
			if (!b.stilts || b.rise < 0.5) continue;
			const bw = (b.b.w ?? 5.6) / 2 + 0.7;
			const bd = (b.b.d ?? 5.6) / 2 + 0.7;
			if (Math.abs(x - b.x) < bw && Math.abs(z - b.z) < bd) return Math.max(island.waterLevel, island.heightAt(b.x, b.z)) + b.stilts;
		}
	return null;
};

/** The crowd and the hero. Agents beyond `count` aren't drawn; homes move from `centers` to `centersB` with `site`. */
export const FolkLayer: React.FC<{world: World; island: Island; t: number; s: number}> = ({world, island, t, s}) => {
	const f = world.folk;
	if (!f) return null;
	const look = fennLook(world, t);
	const count = sample(f.count, t, 0);
	const site = clamp(sample(f.site, t, 0));
	const N = Math.ceil(count);
	const pulseW = loopFreq(3.2, world.loopT);
	const nodes: React.ReactNode[] = [];
	for (let i = 0; i < N; i++) {
		const vis = clamp(count - i);
		const c = i % f.centers.length;
		const a0 = hash2(i, 1, 28) * Math.PI * 2;
		const r0 = Math.sqrt(hash2(i, 2, 28)) * f.spread;
		const cA = f.centers[c];
		const cB = f.centersB?.[c] ?? cA;
		const k = clamp((site - hash2(i, 3, 28) * 0.4) / 0.6);
		const hx = cA[0] + (cB[0] - cA[0]) * k + Math.cos(a0) * r0;
		const hz = cA[1] + (cB[1] - cA[1]) * k + Math.sin(a0) * r0;
		const sp = 0.25 + hash2(i, 4, 28) * 0.15;
		const x = hx + wander(s * sp, i * 3 + 1) * 1.3;
		const z = hz + wander(s * sp, i * 3 + 2) * 1.3;
		const x2 = hx + wander((s + 0.2) * sp, i * 3 + 1) * 1.3;
		const z2 = hz + wander((s + 0.2) * sp, i * 3 + 2) * 1.3;
		const head = Math.atan2(-(z2 - z), x2 - x);
		const moving = Math.hypot(x2 - x, z2 - z) > 0.02;
		const deck = deckAt(world, island, t, x, z);
		const ground = island.columnAt(x, z);
		if (deck === null && (!ground || ground.biome === 'water')) continue;
		const y = deck ?? island.heightAt(x, z);
		nodes.push(
			<group key={i} position={[x, y, z]} rotation={[0, head, 0]} scale={0.3 + 0.7 * vis}>
				<Fenn look={look} gait={s * 7 + i} stride={moving ? 1 : 0} pulse={t * pulseW + i * 0.7} />
			</group>,
		);
	}
	const hp = f.hero.length ? predatorAt(f.hero, t) : null;
	if (hp && hp.state !== 'hidden') {
		const since = t - hp.since;
		const stack = hp.state === 'stack' ? 1 : hp.state === 'lift' ? clamp(since / 0.5) : 0;
		nodes.push(
			<group key="hero" position={[hp.x, island.heightAt(hp.x, hp.z), hp.z]} rotation={[0, (hp.face * Math.PI) / 180, 0]} scale={1.15}>
				<Fenn look={look} gait={s * 7} stride={hp.moving ? 1 : 0} stack={stack} pulse={t * pulseW} />
			</group>,
		);
	}
	return <group>{nodes}</group>;
};
