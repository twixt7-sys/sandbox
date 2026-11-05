// EP27+: the voxel dragon. Built from boxes with the Grimmaw's dark inverted-hull outline, in the field-card sprite's
// palette: rust-red hide, ochre belly, dark rust wing membranes on pale bone fingers, swept-back pale horns, one amber
// eye. Faces +x, feet at y = 0 when perched. Wings pivot at the shoulders: raised and half-spread when perched (the
// sprite's pose), flapping in flight, spread flat in a glide.
import React from 'react';
import * as THREE from 'three';
import {loopFreq} from '../keys';
import type {DragonPose} from './timeline';

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
const BOX = new THREE.BoxGeometry(1, 1, 1);
const OUTLINE = new THREE.MeshBasicMaterial({color: '#12151c', side: THREE.BackSide});
const OL = 0.1;

const RED = '#a8402c';
const RED2 = '#8f3424';
const RED3 = '#c0553a';
const BELLY = '#d39a55';
const MEMB = '#7a2c22';
const MEMB2 = '#93382a';
const BONE = '#e3cfa6';
const EYE = '#ffb347';

type P = {s: [number, number, number]; p: [number, number, number]; c: string; r?: [number, number, number]; e?: boolean; o?: boolean};

// body, neck, head, tail (no legs, no wings)
const BODY: P[] = [
	{s: [2.3, 1.05, 1.1], p: [0, 1.55, 0], c: RED},
	{s: [1.9, 0.32, 0.92], p: [0.1, 1.02, 0], c: BELLY},
	{s: [0.95, 1.12, 1.04], p: [1.05, 1.72, 0], c: RED3},
	{s: [0.5, 0.75, 0.86], p: [1.3, 1.45, 0], c: BELLY},
	// neck rising forward
	{s: [0.8, 0.55, 0.58], p: [1.75, 2.25, 0], c: RED, r: [0, 0, 0.75]},
	{s: [0.7, 0.5, 0.52], p: [2.15, 2.8, 0], c: RED3, r: [0, 0, 1.0]},
	{s: [0.3, 0.55, 0.42], p: [2.0, 2.62, 0], c: BELLY, r: [0, 0, 0.9]},
	// head
	{s: [0.95, 0.5, 0.6], p: [2.6, 3.22, 0], c: RED},
	{s: [0.55, 0.3, 0.46], p: [3.25, 3.1, 0], c: RED3},
	{s: [0.5, 0.14, 0.4], p: [3.2, 2.9, 0], c: BELLY},
	{s: [0.75, 0.12, 0.12], p: [2.15, 3.55, 0.2], c: BONE, r: [0, 0, -0.45]},
	{s: [0.75, 0.12, 0.12], p: [2.15, 3.55, -0.2], c: BONE, r: [0, 0, -0.45]},
	{s: [0.1, 0.1, 0.06], p: [2.85, 3.3, 0.31], c: EYE, e: true, o: false},
	{s: [0.1, 0.1, 0.06], p: [2.85, 3.3, -0.31], c: EYE, e: true, o: false},
	// spines
	{s: [0.18, 0.32, 0.14], p: [0.8, 2.2, 0], c: RED2},
	{s: [0.18, 0.3, 0.14], p: [0.3, 2.15, 0], c: RED2},
	{s: [0.18, 0.28, 0.14], p: [-0.2, 2.12, 0], c: RED2},
	{s: [0.18, 0.26, 0.14], p: [-0.7, 2.08, 0], c: RED2},
	// tail (tapering, ends in a small spade)
	{s: [1.3, 0.62, 0.62], p: [-1.65, 1.45, 0], c: RED, r: [0, 0, 0.12]},
	{s: [1.2, 0.44, 0.44], p: [-2.8, 1.22, 0], c: RED2, r: [0, 0, 0.08]},
	{s: [1.1, 0.3, 0.3], p: [-3.9, 1.06, 0], c: RED, r: [0, 0, 0.05]},
	{s: [0.9, 0.2, 0.2], p: [-4.85, 0.98, 0], c: RED2},
	{s: [0.5, 0.12, 0.55], p: [-5.45, 0.98, 0], c: RED3},
];
const LEGS: {pivot: [number, number, number]; len: number; w: number}[] = [
	{pivot: [0.85, 1.25, 0.42], len: 1.2, w: 0.34},
	{pivot: [0.85, 1.25, -0.42], len: 1.2, w: 0.34},
	{pivot: [-0.75, 1.2, 0.45], len: 1.15, w: 0.4},
	{pivot: [-0.75, 1.2, -0.45], len: 1.15, w: 0.4},
];
// One wing in local coords: the shoulder at the origin, the wing extending along +z (the left side); mirrored for the right.
const WING_INNER: P[] = [
	{s: [0.28, 0.2, 2.3], p: [0.15, 0, 1.15], c: BONE},
	{s: [1.9, 0.08, 2.2], p: [-0.85, 0, 1.15], c: MEMB},
];
const WING_OUTER: P[] = [
	{s: [0.22, 0.16, 2.6], p: [0.2, 0, 1.3], c: BONE},
	{s: [0.14, 0.12, 2.5], p: [-0.6, 0, 1.15], c: BONE, r: [0, 0.5, 0]},
	{s: [0.14, 0.12, 2.2], p: [-1.35, 0, 0.95], c: BONE, r: [0, 0.95, 0]},
	{s: [1.5, 0.07, 2.4], p: [-0.55, 0, 1.25], c: MEMB2},
	{s: [1.2, 0.07, 1.4], p: [-1.6, 0, 0.75], c: MEMB},
];

const Part: React.FC<{pt: P; cast?: boolean}> = ({pt, cast = true}) => (
	<group position={pt.p} rotation={pt.r ?? [0, 0, 0]}>
		<mesh geometry={BOX} material={m(pt.c, pt.e)} scale={pt.s} castShadow={cast} receiveShadow />
		{pt.o !== false && <mesh geometry={BOX} material={OUTLINE} scale={[pt.s[0] + OL, pt.s[1] + OL, pt.s[2] + OL]} />}
	</group>
);

/** Wing: `lift` raises it (radians), `spread` 0 folded .. 1 open (the outer half swings out), `sweep` pulls it back. */
const Wing: React.FC<{side: 1 | -1; lift: number; spread: number; sweep: number}> = ({side, lift, spread, sweep}) => {
	const fold = (1 - spread) * 2.0;
	return (
		<group position={[0.55, 2.05, side * 0.5]} rotation={[-side * lift, side * sweep, 0]} scale={[1, 1, side]}>
			{WING_INNER.map((pt, k) => (
				<Part key={k} pt={pt} />
			))}
			<group position={[0.15, 0, 2.25]} rotation={[-fold * 0.35, -fold * 0.55, 0]}>
				{WING_OUTER.map((pt, k) => (
					<Part key={k} pt={pt} />
				))}
			</group>
		</group>
	);
};

export const Dragon: React.FC<{pose: DragonPose; scale: number; t: number; loopT?: number}> = ({pose, scale, t, loopT}) => {
	const air = pose.air;
	const roar = pose.roar;
	const flapW = loopFreq(7.2, loopT);
	const breathW = loopFreq(1.9, loopT);
	const glide = pose.state === 'glide' ? 1 : 0;
	const flap = Math.sin(t * flapW) * (1 - glide);
	// perched: raised, half-spread (the sprite's pose), breathing; flying: flapping through a wide arc
	const breath = Math.sin(t * breathW);
	const liftPerch = 1.05 + breath * 0.05 + roar * 0.25;
	const liftAir = 0.18 + flap * 0.62 + glide * -0.06;
	const lift = liftPerch * (1 - air) + liftAir * air;
	const spread = (0.45 + roar * 0.5) * (1 - air) + 1 * air;
	const sweep = 0.38 * (1 - air) + 0.05 * air;
	// in flight the body levels out, legs tuck back, tail streams; the whole model banks into turns
	const bob = air * flap * -0.12;
	const legTuck = air * 1.2;
	const headUp = roar * 0.35;
	return (
		<group position={[pose.x, pose.y, pose.z]} rotation={[0, (pose.heading * Math.PI) / 180, 0]} scale={scale}>
			<group rotation={[pose.bank, 0, air * -0.06 + roar * 0.12]} position={[0, bob - air * 1.0, 0]}>
				{BODY.map((pt, k) => {
					const isHead = pt.p[0] > 1.6 && pt.p[1] > 2.0;
					return (
						<group key={k} position={[0, isHead ? headUp : pt.p[0] > -1 && pt.p[0] < 1.4 ? breath * 0.02 : 0, 0]}>
							<Part pt={pt} />
						</group>
					);
				})}
				{LEGS.map((lg, k) => (
					<group key={`l${k}`} position={lg.pivot} rotation={[0, 0, k < 2 ? legTuck : legTuck * 0.9]}>
						<mesh geometry={BOX} material={m(k < 2 ? RED3 : RED)} position={[0, -lg.len / 2, 0]} scale={[lg.w, lg.len, lg.w]} castShadow receiveShadow />
						<mesh geometry={BOX} material={OUTLINE} position={[0, -lg.len / 2, 0]} scale={[lg.w + OL, lg.len + OL, lg.w + OL]} />
						<mesh geometry={BOX} material={m(BONE)} position={[0.14, -lg.len + 0.05, 0]} scale={[0.36, 0.1, lg.w]} receiveShadow />
					</group>
				))}
				<Wing side={1} lift={lift} spread={spread} sweep={sweep} />
				<Wing side={-1} lift={lift} spread={spread} sweep={sweep} />
			</group>
		</group>
	);
};
