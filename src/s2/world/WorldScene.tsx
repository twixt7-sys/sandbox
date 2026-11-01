// Assembles the diorama for one frame from the resolved world timeline: island layers, herd, predators, lighting.
import React, {createContext, useContext, useMemo} from 'react';
import * as THREE from 'three';
import {clamp, hash2, smoothstep} from '../rng';
import {sample} from '../keys';
import {buildHerd, Grimmaw, GrimmawPose, Herd, HerdAgent} from './Creatures';
import {Column, Island, isle} from './island';
import {BIOME_COLORS, DIRT, IslandMesh} from './IslandMesh';
import {Cam, camPose, Lights, Stage} from './Stage';
import {cameraAt, herdCount, moodAt, predatorAt, simTime, World} from './timeline';

export type S2State = {world: World; t: number; cam: Cam; island: Island; agents: HerdAgent[]};
export const S2Context = createContext<S2State | null>(null);
export const useS2 = () => {
	const c = useContext(S2Context);
	if (!c) throw new Error('S2Context missing');
	return c;
};

/** World point -> frame pixel position (1080x1920), using the same camera as the stage. */
export const project = (cam: Cam, p: [number, number, number], width = 1080, height = 1920) => {
	const c = new THREE.PerspectiveCamera(cam.fov ?? 24, width / height, 1, 400);
	const pos = camPose(cam);
	c.position.set(pos[0], pos[1], pos[2]);
	c.lookAt(cam.at[0], cam.at[1], cam.at[2]);
	c.updateMatrixWorld();
	c.updateProjectionMatrix();
	const v = new THREE.Vector3(p[0], p[1], p[2]).project(c);
	return {x: ((v.x + 1) / 2) * width, y: ((1 - v.y) / 2) * height, behind: v.z > 1};
};

const DIRT_C = DIRT.map((h) => new THREE.Color(h));
const SNOW_C = new THREE.Color('#eef4f6');
const ICE_C = new THREE.Color('#a9d3e6');
const ringCol = new THREE.Color();
const grey = (c: THREE.Color, sat: number) => {
	if (sat >= 0.999) return c;
	const g = c.r * 0.3 + c.g * 0.59 + c.b * 0.11;
	return c.lerp(new THREE.Color(g, g, g * 1.03), 1 - sat);
};

/** Predator pose from its key state at time t (walk cycle in sim time s). */
export const grimmawPose = (island: Island, keys: World['predators'][number], t: number, s: number, idx: number): GrimmawPose | null => {
	const p = predatorAt(keys.keys, t);
	if (!p || p.state === 'hidden' || p.state === 'gone') return null;
	const since = t - p.since;
	let rest = 0;
	let roll = 0;
	let pale = 0;
	let dissolve = 0;
	if (p.state === 'sleep') rest = smoothstep(0, 0.9, since);
	if (p.state === 'lie') {
		rest = smoothstep(0, 0.8, since);
		roll = smoothstep(0.5, 1.6, since);
		pale = smoothstep(0.3, 2.2, since);
	}
	if (p.state === 'dissolve') {
		dissolve = clamp(since / 1.3);
		// keep whatever pose it had (a starved one dissolves lying down)
		const prev = keys.keys.filter((k) => k.t < p.since).pop();
		if (prev?.state === 'lie') {
			rest = 1;
			roll = 1;
			pale = 1;
		}
		if (prev?.state === 'sleep') rest = 1;
	}
	if (p.state === 'appear') dissolve = 1 - clamp(since / 1.0);
	// spawn / despawn: a quick scale pop (births, deaths in a cycle), not the "deleted" fly-apart
	let pop = 1;
	if (p.state === 'spawn') pop = 1 - (1 - clamp(since / 0.45)) ** 3;
	if (p.state === 'despawn') pop = 1 - clamp(since / 0.4);
	if (pop <= 0.001) return null;
	const y = island.heightAt(p.x, p.z);
	return {
		x: p.x,
		y,
		z: p.z,
		face: p.face,
		scale: keys.scale * pop,
		gait: s * 6.5 + idx,
		stride: p.moving ? 1 : 0,
		rest,
		roll,
		pale,
		dissolve,
		breath: Math.sin(t * (rest > 0.5 ? 1.6 : 2.6) + idx),
		seed: idx * 7 + Math.floor(p.since * 10),
	};
};

/** A few slow voxel clouds circling the island (depth and scale for the floating diorama). */
const CLOUD_MAT = new THREE.MeshLambertMaterial({color: '#eef2f6', transparent: true, opacity: 0.9});
const CLOUD_BOX = new THREE.BoxGeometry(1, 1, 1);
const CLOUDS = Array.from({length: 6}, (_, i) => ({
	r: 30 + (i % 3) * 6,
	a0: i * 1.05 + 0.3,
	y: 16 + (i % 2) * 6 + (i % 3) * 2,
	speed: 0.018 + (i % 3) * 0.006,
	blocks: Array.from({length: 4 + (i % 3)}, (_, k) => [k * 1.6 - 3, (k % 2) * 0.9, ((k * 7) % 3) - 1, 2.4 + ((k * 5) % 3) * 0.6] as [number, number, number, number]),
}));
const Clouds: React.FC<{t: number; sat: number}> = ({t}) => (
	<group>
		{CLOUDS.map((c, i) => {
			const a = c.a0 + t * c.speed;
			return (
				<group key={i} position={[Math.cos(a) * c.r, c.y, Math.sin(a) * c.r]} rotation={[0, -a, 0]}>
					{c.blocks.map(([x, y, z, s], k) => (
						<mesh key={k} geometry={CLOUD_BOX} material={CLOUD_MAT} position={[x, y, z]} scale={[s * 1.4, s * 0.7, s]} />
					))}
				</group>
			);
		})}
	</group>
);

/** Twinkling pixel stars in the void around the island (on the 3-px grid, deterministic per frame). */
const STARS = Array.from({length: 80}, (_, i) => ({
	x: Math.floor(hash2(i, 1, 77) * 360) * 3,
	y: Math.floor(hash2(i, 2, 77) * 640) * 3,
	big: hash2(i, 3, 77) > 0.85,
	ph: hash2(i, 4, 77) * 6.28,
	sp: 0.6 + hash2(i, 5, 77) * 1.8,
}));
const PixelStars: React.FC<{t: number; level: number}> = ({t, level}) => (
	<div style={{position: 'absolute', inset: 0}}>
		{STARS.map((s, i) => {
			const tw = 0.45 + 0.55 * Math.max(0, Math.sin(t * s.sp + s.ph));
			return <div key={i} style={{position: 'absolute', left: s.x, top: s.y, width: s.big ? 6 : 3, height: s.big ? 6 : 3, background: '#dfe9ff', opacity: level * tw * (s.big ? 0.9 : 0.6)}} />;
		})}
	</div>
);

export type WorldSceneProps = {world: World; t: number; herdCenters: [number, number][]; herdBase: number};

export const useWorldState = (world: World, t: number, herdCenters: [number, number][], herdBase: number): S2State => {
	const island = isle();
	const agents = useMemo(() => buildHerd(island, world.herdMax, herdBase, herdCenters), [island, world.herdMax, herdBase, herdCenters]);
	return {world, t, cam: cameraAt(world, t), island, agents};
};

/** For each herd index, the times its slot was (re)filled: count crossing i upwards. Babies grow from these. */
const birthTimes = (w: World, max: number) => {
	const out: number[][] = Array.from({length: max}, () => []);
	let prev = herdCount(w, 0);
	for (let t = 0.05; t < 80; t += 0.05) {
		const c = herdCount(w, t);
		if (c > prev) for (let i = Math.floor(prev); i < Math.min(max, Math.ceil(c)); i++) out[i].push(t);
		prev = c;
	}
	return out;
};

export const WorldScene: React.FC<{state: S2State}> = ({state}) => {
	const {world, t, cam, island, agents} = state;
	const births = useMemo(() => birthTimes(world, world.herdMax), [world]);
	const mood = moodAt(world, t);
	const s = simTime(world, t);
	const graze = sample(world.graze, t, 0);
	const snow = sample(world.snow, t, 0);
	const forest = sample(world.forest, t, 1);
	const count = herdCount(world, t);
	// The herd greys as a boom starves: tied to the graze layer being stripped.
	const herdPale = clamp((graze - 0.6) / 0.4) * 0.6;
	const rings = world.rings
		.map((r) => {
			const on = clamp((t - r.on) / 0.9);
			const off = r.off === Infinity ? 1 : 1 - clamp((t - r.off) / 0.5);
			const w = Math.min(on, off);
			return {...r, w, R: r.r * (1 - (1 - on) ** 3)};
		})
		.filter((r) => r.w > 0);

	const tint = (c: Column, base: THREE.Color, out: THREE.Color) => {
		out.copy(base);
		if (graze > 0 && (c.biome === 'meadow' || (c.biome === 'forest' && graze > 0.5))) {
			const thr = c.biome === 'forest' ? (graze - 0.5) * 1.6 : graze * 1.08;
			if (c.r < thr) out.copy(DIRT_C[Math.floor(c.r * 97) % DIRT_C.length]);
			else if (c.r < thr + 0.12) out.lerp(DIRT_C[0], 0.45);
		}
		if (snow > 0 && c.biome !== 'snow') {
			const k = smoothstep(c.r * 0.85, c.r * 0.85 + 0.15, snow);
			if (k > 0) out.lerp(c.biome === 'water' ? ICE_C : SNOW_C, k * (c.biome === 'water' ? 0.55 : 0.88));
		}
		// Territories: land outside every active ring dims, so the claimed valleys read at a glance.
		if (rings.length) {
			const inAny = rings.some((r) => Math.hypot(c.x - r.x, c.z - r.z) < r.R + 1.05);
			if (!inAny) out.multiplyScalar(1 - 0.38 * Math.max(...rings.map((r) => r.w)));
		}
		for (const r of rings) {
			const d = Math.hypot(c.x - r.x, c.z - r.z);
			if (d < r.R + 0.8) {
				ringCol.set(r.color);
				const border = Math.abs(d - r.R) < 1.05 ? 0.9 : 0;
				const inside = d < r.R ? 0.3 + 0.12 * Math.sin(t * 5 - d * 0.6) : 0;
				out.lerp(ringCol, Math.max(border, inside) * r.w);
			}
		}
		grey(out, mood.sat);
	};
	const treeScale = (k: number) => {
		const tr = island.trees[k];
		if (forest >= 1) return 1;
		return smoothstep(tr.r - 0.08, tr.r + 0.08, forest);
	};
	const treeTint = (c: THREE.Color, k: number, part: number) => {
		if (snow > 0 && part > 0) {
			const tr = island.trees[k];
			const sk = smoothstep(tr.r * 0.8, tr.r * 0.8 + 0.2, snow);
			if (part === 2) c.lerp(SNOW_C, sk * 0.9);
			else c.lerp(SNOW_C, sk * 0.35);
		}
		grey(c, mood.sat);
	};
	const lift = (c: Column) => {
		let dy = 0;
		for (const r0 of world.ripples) {
			const age = t - r0;
			if (age < 0 || age > 1.6) continue;
			const front = age * 26;
			const d = Math.hypot(c.x, c.z);
			const x = d - front;
			if (x > -3 && x < 0.5) dy += Math.sin(((x + 3) / 3.5) * Math.PI) * 0.75 * (1 - age / 1.6);
		}
		return dy;
	};
	const poses = world.predators.map((p, i) => grimmawPose(island, p, t, s, i));
	return (
		<Stage
			cam={cam}
			background={`radial-gradient(ellipse at 50% 42%, ${mood.sky[0]} 0%, ${mood.sky[1]} 48%, ${mood.sky[2]} 100%)`}
			backdrop={<PixelStars t={t} level={0.35 + 0.45 * (1 - mood.sun)} />}
		>
			{/* Distance haze in the void's colour: the far side of the island recedes a little (diorama depth). */}
			<fog attach="fog" args={[mood.sky[1], cam.dist * 0.98, cam.dist + 120]} />
			<Lights sun={mood.sun} warm={mood.warm} hemi={mood.hemi} />
			<IslandMesh island={island} t={t} tint={tint} treeScale={treeScale} treeTint={treeTint} lift={lift} />
			<Herd
				island={island}
				agents={agents}
				count={count}
				s={s}
				t={t}
				pale={herdPale}
				born={(i) => {
					const b = births[i].filter((x) => x <= t).pop();
					return b === undefined ? 1 : clamp((t - b) / 4.5);
				}}
			/>
			{poses.map((p, i) => (p ? <Grimmaw key={i} pose={p} /> : null))}
		</Stage>
	);
};

export {BIOME_COLORS};
