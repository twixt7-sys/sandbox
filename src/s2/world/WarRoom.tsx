// EP36: the war room's threads, laid on the Isle. Every reason a side has for war is a coloured thread pinned from its
// camp to what it wants (a thread can be braided in two colours: an alliance), and the war starts where the threads
// meet: a knot on a tall pin stuck in the contested ruin, glowing flashpoint lime. `draw` (0..1) runs a thread out
// from its source pin like a needle, `taut` (0..1) pulls its sag out, brightens it and makes it hum, and the knot's
// `flare` (0..1) is the flashpoint. Camps are plain canvas tents (no device, no emblem: the sides are told apart only
// by plain colours). Everything is voxels and a pure function of time; nothing here fights or falls.
import React, {useMemo} from 'react';
import * as THREE from 'three';
import {loopFreq} from '../keys';
import type {Island} from './island';

export const FLASH = '#c8f04a';
const BOX = new THREE.BoxGeometry(1, 1, 1);
const OUTLINE = new THREE.MeshBasicMaterial({color: '#12151c', side: THREE.BackSide});
const mats = new Map<string, THREE.MeshLambertMaterial>();
const lam = (hex: string, glow = 0) => {
	const k = `${hex}|${glow.toFixed(2)}`;
	if (!mats.has(k)) {
		const mm = new THREE.MeshLambertMaterial({color: hex});
		if (glow > 0) mm.emissive = new THREE.Color(hex).multiplyScalar(glow);
		mats.set(k, mm);
	}
	return mats.get(k)!;
};
const q = (v: number, s = 20) => Math.round(Math.max(0, Math.min(1, v)) * s) / s;
const Y_UP = new THREE.Vector3(0, 1, 0);
const X_AX = new THREE.Vector3(1, 0, 0);

const ground = (island: Island, x: number, z: number) => Math.max(island.waterLevel, island.heightAt(x, z));

/** A map pin: a thin dark pole and a round head (a small cube cluster) in the side's colour. */
const Pin: React.FC<{x: number; y: number; z: number; h: number; color: string; head?: number}> = ({x, y, z, h, color, head = 0.36}) => (
	<group position={[x, y, z]}>
		<mesh geometry={BOX} material={lam('#3b3530')} position={[0, h / 2, 0]} scale={[0.1, h, 0.1]} castShadow />
		<mesh geometry={BOX} material={lam(color, 0.25)} position={[0, h + head * 0.3, 0]} scale={[head, head, head]} castShadow />
		<mesh geometry={BOX} material={OUTLINE} position={[0, h + head * 0.3, 0]} scale={[head + 0.07, head + 0.07, head + 0.07]} />
	</group>
);

/** One thread from pin A (x, z, height y0 above the ground) to pin B (`to`, height y1), sagging by `sag` (in units at
 * its middle) until `taut` pulls it straight. Drawn as a chain of short boxes so it reads at ⅓ resolution. */
export const Thread: React.FC<{
	x: number;
	z: number;
	to: [number, number];
	y0: number;
	y1: number;
	color: string;
	color2?: string;
	island: Island;
	t: number;
	loopT?: number;
	draw: number;
	taut: number;
	sag?: number;
	pins?: boolean;
	width?: number;
}> = ({x, z, to, y0, y1, color, color2, island, t, loopT, draw, taut, sag = 1.4, pins = true, width = 0.2}) => {
	const a = useMemo(() => new THREE.Vector3(x, ground(island, x, z) + y0, z), [island, x, z, y0]);
	const b = useMemo(() => new THREE.Vector3(to[0], ground(island, to[0], to[1]) + y1, to[1]), [island, to, y1]);
	if (draw <= 0.001) return null;
	const len = a.distanceTo(b);
	const n = Math.max(6, Math.round(len / 0.45));
	const tt = Math.max(0, Math.min(1, taut));
	const s = sag * (1 - 0.92 * tt);
	// a taut thread hums: a small sideways shiver, strongest mid-span, whole cycles per loop
	const hum = tt * 0.06 * Math.sin(t * loopFreq(31, loopT));
	const side = new THREE.Vector3().subVectors(b, a).cross(Y_UP).normalize();
	const pt = (f: number) => {
		const p = new THREE.Vector3().lerpVectors(a, b, f);
		const bow = 4 * f * (1 - f);
		p.y -= s * bow;
		p.addScaledVector(side, hum * bow);
		return p;
	};
	const glow = 0.18 + 0.5 * tt;
	const segs: React.ReactNode[] = [];
	const shown = Math.min(1, draw);
	for (let k = 0; k < n; k++) {
		const f0 = k / n;
		if (f0 >= shown) break;
		const f1 = Math.min((k + 1) / n, shown);
		const p0 = pt(f0);
		const p1 = pt(f1);
		const d = new THREE.Vector3().subVectors(p1, p0);
		const l = d.length();
		if (l < 1e-4) continue;
		const quat = new THREE.Quaternion().setFromUnitVectors(X_AX, d.clone().normalize());
		const mid = new THREE.Vector3().addVectors(p0, p1).multiplyScalar(0.5);
		const c = color2 && k % 2 === 1 ? color2 : color;
		segs.push(<mesh key={k} geometry={BOX} material={lam(c, q(glow))} position={mid} quaternion={quat} scale={[l + 0.03, width, width]} castShadow />);
	}
	return (
		<group>
			{pins && <Pin x={a.x} y={ground(island, x, z)} z={a.z} h={y0} color={color} />}
			{segs}
		</group>
	);
};

/** The flashpoint: a tall war pin stuck in the contested ground with a knot at its head where every thread meets.
 * `rise` (0..1) pushes the pin in, `flare` (0..1) makes the knot blaze (and swell); it breathes gently otherwise. */
export const Knot: React.FC<{x: number; z: number; y: number; island: Island; t: number; loopT?: number; rise: number; flare: number; color?: string}> = ({x, z, y, island, t, loopT, rise, flare, color = FLASH}) => {
	if (rise <= 0.001) return null;
	const g = ground(island, x, z);
	const top = g + y + (1 - rise) * 3;
	const br = 0.5 + 0.5 * Math.sin(t * loopFreq(2.2, loopT));
	const f = Math.max(0, Math.min(1, flare));
	const sc = 0.62 + 0.06 * br + 0.5 * f;
	const glow = q(0.35 + 0.15 * br + 0.6 * f);
	const parts: [number, number, number, number][] = [
		[0, 0, 0, 1],
		[0.28, 0.12, 0.1, 0.62],
		[-0.26, -0.08, 0.14, 0.58],
		[0.06, 0.26, -0.22, 0.55],
		[-0.1, -0.24, -0.2, 0.5],
	];
	return (
		<group>
			<mesh geometry={BOX} material={lam('#2e2925')} position={[x, (g + top) / 2 - 0.2, z]} scale={[0.16, top - g + 0.4, 0.16]} castShadow />
			<group position={[x, top, z]} scale={[sc, sc, sc]}>
				{parts.map(([px, py, pz, s], k) => (
					<group key={k}>
						<mesh geometry={BOX} material={lam(color, glow)} position={[px, py, pz]} scale={[s * 0.55, s * 0.55, s * 0.55]} rotation={[0.4 * k, 0.7 * k, 0.2 * k]} castShadow />
						{k === 0 && <mesh geometry={BOX} material={OUTLINE} position={[px, py, pz]} scale={[0.6, 0.6, 0.6]} />}
					</group>
				))}
				{f > 0.02 && (
					<>
						<mesh geometry={BOX} position={[0, 0, 0]} scale={[1.05 + 0.35 * f, 1.05 + 0.35 * f, 1.05 + 0.35 * f]}>
							<meshBasicMaterial color={color} transparent opacity={0.45 * f} depthWrite={false} blending={THREE.AdditiveBlending} />
						</mesh>
						{[0, 1, 2, 3, 4, 5, 6, 7].map((k) => {
							const a = (k / 8) * Math.PI * 2 + 0.4;
							const r = 0.9 + 0.5 * f;
							return <mesh key={`s${k}`} geometry={BOX} material={lam('#f4ffd0', 1)} position={[Math.cos(a) * r, Math.sin(a) * r, 0.1]} scale={[0.16 * f, 0.16 * f, 0.16 * f]} />;
						})}
					</>
				)}
			</group>
		</group>
	);
};

const CANVAS = '#d8ccb0';
const CANVAS_D = '#b9ab8c';

/** A war camp: `n` plain canvas ridge tents round (x, z), each with a door flap in the side's colour, rising out of
 * the ground with `rise` (and folding back down as it falls: the camp is struck). */
export const Camp: React.FC<{x: number; z: number; face: number; color: string; n?: number; r?: number; island: Island; rise: number}> = ({x, z, face, color, n = 3, r = 1.6, island, rise}) => {
	if (rise <= 0.001) return null;
	const out: React.ReactNode[] = [];
	for (let k = 0; k < n; k++) {
		const g = Math.max(0, Math.min(1, (rise - k * 0.12) / 0.64));
		if (g <= 0.001) continue;
		const a = (face * Math.PI) / 180 + (k / n) * Math.PI * 2 + 0.4;
		const tx = x + Math.cos(a) * r;
		const tz = z + Math.sin(a) * r;
		const y = ground(island, tx, tz);
		const rot = -a + Math.PI / 2;
		out.push(
			<group key={k} position={[tx, y, tz]} rotation={[0, rot, 0]} scale={[1, g, 1]}>
				{/* two canvas slopes meeting at a ridge, gable ends front and back */}
				<mesh geometry={BOX} material={lam(CANVAS)} position={[-0.36, 0.42, 0]} rotation={[0, 0, -0.72]} scale={[0.08, 1.12, 1.5]} castShadow receiveShadow />
				<mesh geometry={BOX} material={lam(CANVAS_D)} position={[0.36, 0.42, 0]} rotation={[0, 0, 0.72]} scale={[0.08, 1.12, 1.5]} castShadow receiveShadow />
				<mesh geometry={BOX} material={OUTLINE} position={[0, 0.42, 0]} scale={[1.14, 0.94, 1.56]} />
				<mesh geometry={BOX} material={lam(CANVAS)} position={[0, 0.38, 0.72]} scale={[0.86, 0.66, 0.06]} castShadow />
				<mesh geometry={BOX} material={lam(color)} position={[0, 0.26, 0.76]} scale={[0.3, 0.46, 0.04]} />
				<mesh geometry={BOX} material={lam('#5a3c28')} position={[0, 0.86, 0]} scale={[0.07, 0.12, 1.6]} />
			</group>,
		);
	}
	return <group>{out}</group>;
};
