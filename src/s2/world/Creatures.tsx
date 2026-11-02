// Voxel creatures for the Season 2 diorama. Built from boxes so they read as pixel art at the stage's 1/3 resolution.
import React, {useLayoutEffect, useMemo, useRef} from 'react';
import * as THREE from 'three';
import {hash2, wander} from '../rng';
import {Island} from './island';

const matCache = new Map<string, THREE.MeshLambertMaterial>();
const mat = (hex: string, emissive = false) => {
	const key = hex + (emissive ? 'e' : '');
	if (!matCache.has(key)) {
		const m = new THREE.MeshLambertMaterial({color: hex});
		if (emissive) m.emissive = new THREE.Color(hex);
		matCache.set(key, m);
	}
	return matCache.get(key)!;
};
const BOX = new THREE.BoxGeometry(1, 1, 1);
/** Inverted-hull outline: a slightly larger back-faced dark box behind each part, like the sprite's 1-px outline. */
const OUTLINE = new THREE.MeshBasicMaterial({color: '#12151c', side: THREE.BackSide});
const OL = 0.09;

type Part = {s: [number, number, number]; p: [number, number, number]; c: string; r?: [number, number, number]; e?: boolean; leg?: number};

// The Grimmaw: charcoal hide with darker stripes, a ridge of rust plates, a bone skull-mask and underslung jaw,
// long front legs and lower hips (matches the field-card sprite generated for EP26). Faces +x, feet at y = 0.
const HIDE = '#686c78';
const HIDE2 = '#5c606b';
const STRIPE = '#3a3d46';
const BONE = '#d6c6a5';
const BONE2 = '#c4b18c';
const RUST = '#b65a30';
const RUST2 = '#cf7038';

const GRIMMAW_BODY: Part[] = [
	{s: [1.35, 1.25, 1.15], p: [0.45, 1.5, 0], c: HIDE},
	{s: [1.25, 1.0, 1.02], p: [-0.65, 1.3, 0], c: HIDE2},
	{s: [1.7, 0.32, 0.92], p: [-0.05, 0.98, 0], c: '#7a7d86'},
	{s: [0.14, 1.0, 1.18], p: [-0.25, 1.38, 0], c: STRIPE},
	{s: [0.14, 1.15, 1.18], p: [0.2, 1.5, 0], c: STRIPE},
	{s: [0.14, 1.1, 1.18], p: [0.62, 1.55, 0], c: STRIPE},
	{s: [0.12, 0.9, 1.05], p: [-0.85, 1.32, 0], c: STRIPE},
	// neck + head
	{s: [0.55, 0.65, 0.78], p: [1.22, 1.5, 0], c: HIDE},
	{s: [0.75, 0.62, 0.74], p: [1.6, 1.42, 0], c: HIDE},
	{s: [0.66, 0.3, 0.8], p: [1.66, 1.72, 0], c: BONE},
	{s: [0.58, 0.3, 0.64], p: [1.92, 1.18, 0], c: BONE2},
	{s: [0.3, 0.14, 0.5], p: [2.1, 1.38, 0], c: BONE},
	{s: [0.12, 0.42, 0.12], p: [1.42, 2.02, 0.26], c: BONE, r: [0, 0, 0.55]},
	{s: [0.12, 0.42, 0.12], p: [1.42, 2.02, -0.26], c: BONE, r: [0, 0, 0.55]},
	{s: [0.09, 0.09, 0.06], p: [1.82, 1.5, 0.38], c: '#ffb347', e: true},
	{s: [0.09, 0.09, 0.06], p: [1.82, 1.5, -0.38], c: '#ffb347', e: true},
	// spine plates (front ones tallest)
	{s: [0.22, 0.62, 0.2], p: [0.75, 2.33, 0], c: RUST2},
	{s: [0.22, 0.58, 0.2], p: [0.4, 2.3, 0], c: RUST},
	{s: [0.22, 0.52, 0.2], p: [0.05, 2.22, 0], c: RUST2},
	{s: [0.22, 0.46, 0.2], p: [-0.3, 2.04, 0], c: RUST},
	{s: [0.22, 0.4, 0.2], p: [-0.65, 1.95, 0], c: RUST2},
	{s: [0.2, 0.34, 0.18], p: [-1.0, 1.86, 0], c: RUST},
	// tail
	{s: [0.75, 0.46, 0.46], p: [-1.55, 1.24, 0], c: HIDE2, r: [0, 0, 0.18]},
	{s: [0.6, 0.3, 0.3], p: [-2.12, 1.08, 0], c: HIDE2, r: [0, 0, 0.28]},
	{s: [0.18, 0.28, 0.14], p: [-1.55, 1.58, 0], c: RUST},
	{s: [0.16, 0.22, 0.12], p: [-2.05, 1.3, 0], c: RUST2},
];
// Legs: pivot at the top (hip / shoulder); `leg` = gait phase index.
const LEGS: {pivot: [number, number, number]; len: number; w: number; phase: number}[] = [
	{pivot: [0.72, 1.18, 0.4], len: 1.18, w: 0.4, phase: 0},
	{pivot: [0.72, 1.18, -0.4], len: 1.18, w: 0.4, phase: Math.PI},
	{pivot: [-0.78, 1.0, 0.36], len: 1.0, w: 0.42, phase: Math.PI},
	{pivot: [-0.78, 1.0, -0.36], len: 1.0, w: 0.42, phase: 0},
];

export type GrimmawPose = {
	x: number;
	y: number;
	z: number;
	/** heading in degrees (0 = +x) */
	face: number;
	scale: number;
	/** walk cycle phase (radians); amplitude 0 = standing */
	gait: number;
	stride: number;
	/** 0 standing .. 1 lying down (sleep) */
	rest: number;
	/** 0 upright .. 1 rolled on its side (starving) */
	roll: number;
	/** 0 normal .. 1 grey */
	pale: number;
	/** 0 whole .. 1 fully dissolved into flying voxels */
	dissolve: number;
	/** 0 .. 1 display call: head up, jaw open, body rocks back */
	roar?: number;
	breath: number;
	seed: number;
};

const greyOf = (hex: string, p: number) => {
	const c = new THREE.Color(hex);
	const g = c.r * 0.3 + c.g * 0.59 + c.b * 0.11;
	return c.lerp(new THREE.Color(g * 0.9 + 0.12, g * 0.9 + 0.12, g * 0.95 + 0.14), p);
};

export const Grimmaw: React.FC<{pose: GrimmawPose}> = ({pose}) => {
	const {rest, roll, pale, dissolve, gait, stride, breath} = pose;
	const roar = pose.roar ?? 0;
	if (dissolve >= 1) return null;
	const bob = Math.abs(Math.sin(gait)) * 0.06 * stride;
	const drop = rest * 0.72;
	const mats = (hex: string, e?: boolean) => (pale > 0.01 ? new THREE.MeshLambertMaterial({color: greyOf(hex, pale), emissive: e ? greyOf(hex, pale) : undefined}) : mat(hex, e));
	// Flying-apart offsets for the dissolve: each part rises and spins away, staggered by a per-part delay.
	const fly = (k: number) => {
		if (dissolve <= 0) return {dy: 0, dx: 0, dz: 0, s: 1, rot: 0};
		const delay = hash2(k, pose.seed, 3) * 0.45;
		const p = Math.max(0, Math.min(1, (dissolve - delay) / 0.55));
		return {
			dy: p * p * 3.2,
			dx: (hash2(k, pose.seed, 4) - 0.5) * p * 1.6,
			dz: (hash2(k, pose.seed, 5) - 0.5) * p * 1.6,
			s: 1 - p,
			rot: p * (hash2(k, pose.seed, 6) - 0.5) * 6,
		};
	};
	return (
		<group position={[pose.x, pose.y, pose.z]} rotation={[0, (pose.face * Math.PI) / 180, 0]} scale={pose.scale}>
			<group position={[0, bob - drop, 0]} rotation={[roll * 1.25, 0, roar * 0.12]}>
				{GRIMMAW_BODY.map((pt, k) => {
					const f = fly(k);
					if (f.s <= 0.01) return null;
					// Head parts dip when resting; torso breathes.
					const isHead = pt.p[0] > 1.0 && pt.p[1] > 1.0;
					const isJaw = isHead && pt.c === BONE2;
					const headDip = isHead ? rest * 0.55 - roar * 0.32 + (isJaw ? roar * 0.3 : 0) : 0;
					const by = pt.p[0] > -1.2 && pt.p[0] < 1.0 ? 1 + breath * 0.025 : 1;
					return (
						<group key={k} position={[pt.p[0] + f.dx, pt.p[1] - headDip + f.dy, pt.p[2] + f.dz]} rotation={[(pt.r?.[0] ?? 0) + f.rot, (pt.r?.[1] ?? 0) + f.rot, pt.r?.[2] ?? 0]}>
							<mesh geometry={BOX} material={mats(pt.c, pt.e && rest < 0.5)} scale={[pt.s[0] * f.s, pt.s[1] * by * f.s, pt.s[2] * f.s]} castShadow />
							{!pt.e && f.s > 0.5 && <mesh geometry={BOX} material={OUTLINE} scale={[pt.s[0] * f.s + OL, pt.s[1] * by * f.s + OL, pt.s[2] * f.s + OL]} />}
						</group>
					);
				})}
				{LEGS.map((lg, k) => {
					const f = fly(100 + k);
					if (f.s <= 0.01) return null;
					const swing = Math.sin(gait + lg.phase) * 0.45 * stride;
					const fold = rest * 1.35;
					return (
						<group key={`l${k}`} position={[lg.pivot[0] + f.dx, lg.pivot[1] + f.dy, lg.pivot[2] + f.dz]} rotation={[0, 0, swing + (k < 2 ? fold : -fold)]} scale={f.s}>
							<mesh geometry={BOX} material={mats(k < 2 ? HIDE : HIDE2)} position={[0, -lg.len / 2, 0]} scale={[lg.w, lg.len, lg.w]} castShadow />
							<mesh geometry={BOX} material={OUTLINE} position={[0, -lg.len / 2, 0]} scale={[lg.w + OL, lg.len + OL, lg.w + OL]} />
							<mesh geometry={BOX} material={mats(BONE)} position={[0.14, -lg.len + 0.05, 0]} scale={[0.34, 0.1, lg.w * 0.95]} castShadow />
						</group>
					);
				})}
			</group>
		</group>
	);
};

// ---------------------------------------------------------------- the herd (instanced)

export type HerdAgent = {hx: number; hz: number; herd: number; r: number; baby: boolean};

// Cream wool with dark moss tufts on the back: reads as a herd from far away (pale dots on green).
const MOSS = ['#2f5d2c', '#386b33', '#2a5227', '#41763a'];

/** Herd homes: agents 0..base-1 live in herds on the meadows; later indices (births / a boom) spread further. */
export const buildHerd = (island: Island, max: number, base: number, centers: [number, number][], seed = 11): HerdAgent[] => {
	const ok = (x: number, z: number) => {
		const c = island.columnAt(x, z);
		return !!c && (c.biome === 'meadow' || c.biome === 'sand') && c.d < 0.93;
	};
	const agents: HerdAgent[] = [];
	for (let i = 0; i < max; i++) {
		const boom = i >= base;
		const herd = Math.floor(hash2(i, 1, seed) * centers.length);
		const spread = boom ? 7.5 : 4.6;
		let hx = centers[herd][0];
		let hz = centers[herd][1];
		for (let tries = 0; tries < 24; tries++) {
			const a = hash2(i, tries, seed + 1) * Math.PI * 2;
			const rr = Math.sqrt(hash2(i, tries, seed + 2)) * spread;
			const x = centers[herd][0] + Math.cos(a) * rr;
			const z = centers[herd][1] + Math.sin(a) * rr;
			if (ok(x, z)) {
				hx = x;
				hz = z;
				break;
			}
		}
		agents.push({hx, hz, herd, r: hash2(i, 9, seed), baby: boom});
	}
	return agents;
};

const m4 = new THREE.Matrix4();
const m4b = new THREE.Matrix4();
const q = new THREE.Quaternion();
const e3 = new THREE.Euler();
const v3 = new THREE.Vector3();
const s3 = new THREE.Vector3();
const col = new THREE.Color();

// Part layout of one mossback (faces +x, feet at 0): legs block, pale belly, mossy back, head.
const MB_PARTS: {s: [number, number, number]; p: [number, number, number]}[] = [
	{s: [0.56, 0.18, 0.34], p: [0, 0.09, 0]},
	{s: [0.84, 0.42, 0.58], p: [0, 0.39, 0]},
	{s: [0.5, 0.12, 0.36], p: [-0.06, 0.64, 0]},
	{s: [0.3, 0.3, 0.3], p: [0.5, 0.46, 0]},
];
const MB_COLORS = ['#3a2c20', '#ece2c6', '', '#4a3828'];

/**
 * The herd: `count` agents visible (fractional = the last one fading), wandering around their homes in simulation
 * time `s`. Agents beyond `base` are born small and grow. `pale` greys them (a starving boom).
 */
export const Herd: React.FC<{island: Island; agents: HerdAgent[]; count: number; s: number; t: number; pale?: number; born?: (i: number) => number}> = ({island, agents, count, s, t, pale = 0, born}) => {
	const refs = [useRef<THREE.InstancedMesh>(null), useRef<THREE.InstancedMesh>(null), useRef<THREE.InstancedMesh>(null), useRef<THREE.InstancedMesh>(null)];
	const outline = useRef<THREE.InstancedMesh>(null);
	const m = useMemo(() => new THREE.MeshLambertMaterial(), []);
	useLayoutEffect(() => {
		agents.forEach((a, i) => {
			const vis = Math.max(0, Math.min(1, count - i));
			const grow = born ? born(i) : 1;
			const sc = vis <= 0 ? 0.0001 : (0.35 + 0.65 * vis) * (a.baby ? 0.55 + 0.45 * grow : 1) * (0.92 + a.r * 0.16);
			// wander in sim time around home, herd centre drifting slowly
			const w = 0.13 + a.r * 0.05;
			let x = a.hx + wander(s * w, i * 2 + 1) * 1.8 + wander(s * 0.03, a.herd + 50) * 2.2;
			let z = a.hz + wander(s * w, i * 2 + 2) * 1.8 + wander(s * 0.03, a.herd + 70) * 2.2;
			const c = island.columnAt(x, z);
			if (!c || c.biome === 'water' || c.biome === 'rock' || c.biome === 'snow' || c.d > 0.95) {
				x = a.hx;
				z = a.hz;
			}
			const x2 = a.hx + wander((s + 0.2) * w, i * 2 + 1) * 1.8 + wander((s + 0.2) * 0.03, a.herd + 50) * 2.2;
			const z2 = a.hz + wander((s + 0.2) * w, i * 2 + 2) * 1.8 + wander((s + 0.2) * 0.03, a.herd + 70) * 2.2;
			const head = Math.atan2(-(z2 - z), x2 - x);
			const y = island.heightAt(x, z);
			const hop = Math.max(0, Math.sin(s * 3.1 + i * 1.7)) * 0.06;
			e3.set(0, head, 0);
			q.setFromEuler(e3);
			m4.compose(v3.set(x, y + hop, z), q, s3.set(sc, sc, sc));
			const graze = Math.sin(t * 1.3 + i * 2.3) > 0.55 ? -0.14 : 0;
			// outline hull around the wool body
			m4b.compose(v3.set(0, 0.39, 0), q.identity(), s3.set(0.84 + 0.1, 0.42 + 0.1, 0.58 + 0.1));
			outline.current!.setMatrixAt(i, m4.clone().multiply(m4b));
			MB_PARTS.forEach((pt, k) => {
				m4b.compose(v3.set(pt.p[0], pt.p[1] + (k === 3 ? graze : 0), pt.p[2]), q.identity(), s3.set(pt.s[0], pt.s[1], pt.s[2]));
				const mm = m4.clone().multiply(m4b);
				const r = refs[k].current!;
				r.setMatrixAt(i, mm);
				const hex = k === 2 ? MOSS[Math.floor(a.r * MOSS.length)] : MB_COLORS[k];
				col.set(hex);
				if (pale > 0) {
					const g = col.r * 0.3 + col.g * 0.59 + col.b * 0.11;
					col.lerp(new THREE.Color(g, g, g * 1.04), pale);
				}
				r.setColorAt(i, col);
			});
			e3.set(0, head, 0);
			q.setFromEuler(e3);
		});
		// Only draw the agents that are alive (indices >= count are scaled to zero anyway): far fewer vertices.
		const live = Math.min(agents.length, Math.ceil(count) + 1);
		outline.current!.count = live;
		outline.current!.instanceMatrix.needsUpdate = true;
		refs.forEach((r) => {
			r.current!.count = live;
			r.current!.instanceMatrix.needsUpdate = true;
			if (r.current!.instanceColor) r.current!.instanceColor.needsUpdate = true;
		});
	});
	return (
		<group>
			{refs.map((r, k) => (
				// only the wool body casts a shadow (the legs, moss and head are too small to read in one; this halves the shadow pass)
				<instancedMesh key={k} ref={r} args={[BOX, m, agents.length]} castShadow={k === 1} frustumCulled={false} />
			))}
			<instancedMesh ref={outline} args={[BOX, OUTLINE, agents.length]} frustumCulled={false} />
		</group>
	);
};
