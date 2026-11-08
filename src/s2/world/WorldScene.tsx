// Assembles the diorama for one frame from the resolved world timeline: island layers, herd, predators, lighting.
import React, {createContext, useContext, useMemo} from 'react';
import * as THREE from 'three';
import {clamp, hash2, smoothstep} from '../rng';
import {loopFreq, sample} from '../keys';
import {buildHerd, Grimmaw, GrimmawPose, Herd, HerdAgent} from './Creatures';
import {Column, Island, isle} from './island';
import {BIOME_COLORS, DIRT, IslandMesh} from './IslandMesh';
import {Cam, camPose, Lights, Stage, sunDir} from './Stage';
import {cameraAt, dragonAt, herdCount, moodAt, predatorAt, simTime, World} from './timeline';
import {Dragon} from './Dragon';
import {Cairn, roadAt, SettlementLayer} from './Settlement';
import {FolkLayer} from './Folk';

export type S2State = {world: World; t: number; cam: Cam; island: Island; agents: HerdAgent[]; agentsB?: HerdAgent[]};
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
const GLINT = new THREE.Color('#fff8e8');
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
	// a display call: rises in 0.25 s, holds, settles by 1.4 s
	const roar = p.state === 'roar' ? smoothstep(0, 0.25, since) * (1 - smoothstep(0.85, 1.4, since)) : 0;
	// alert: the head comes up to watch the sky, then settles back over `until`
	const span = p.until - p.since;
	// gaze (EP27+): the alert pose held from its first frame (frame 0 and the loop frame look up at the dragon)
	const alert = p.state === 'gaze' ? 1 : p.state === 'alert' ? smoothstep(0, 0.35, since) * (Number.isFinite(span) ? 1 - smoothstep(Math.max(0.35, span - 0.45), Math.max(0.4, span), since) : 1) : 0;
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
		roar,
		alert,
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
const PixelStars: React.FC<{t: number; level: number; loopT?: number}> = ({t, level, loopT}) => (
	<div style={{position: 'absolute', inset: 0}}>
		{STARS.map((s, i) => {
			const tw = 0.45 + 0.55 * Math.max(0, Math.sin(t * loopFreq(s.sp, loopT) + s.ph));
			return <div key={i} style={{position: 'absolute', left: s.x, top: s.y, width: s.big ? 6 : 3, height: s.big ? 6 : 3, background: '#dfe9ff', opacity: level * tw * (s.big ? 0.9 : 0.6)}} />;
		})}
	</div>
);

/** A ring of voxel dust puffs (a stomp, a landing): expands, rises a little and fades over `life` seconds. */
const DUST_BOX = new THREE.BoxGeometry(1, 1, 1);
const Dust: React.FC<{t: number; at: number; x: number; z: number; y: number; r?: number; life?: number}> = ({t, at, x, z, y, r = 2.6, life = 1.0}) => {
	const age = t - at;
	if (age < 0 || age > life) return null;
	const p = age / life;
	const ease = 1 - (1 - p) ** 2;
	return (
		<group position={[x, y, z]}>
			{Array.from({length: 14}, (_, k) => {
				const a = (k / 14) * Math.PI * 2 + hash2(k, 3, 9) * 0.4;
				const rr = 0.6 + ease * r * (0.7 + hash2(k, 4, 9) * 0.5);
				const s = (0.55 - 0.4 * p) * (0.8 + hash2(k, 5, 9) * 0.5);
				const m = new THREE.MeshLambertMaterial({color: '#d8c49a', transparent: true, opacity: 0.85 * (1 - p)});
				return <mesh key={k} geometry={DUST_BOX} material={m} position={[Math.cos(a) * rr, 0.2 + ease * 0.7 * (0.5 + hash2(k, 6, 9)), Math.sin(a) * rr]} scale={[s, s, s]} />;
			})}
		</group>
	);
};

// ---------------------------------------------------------------- ambient life (Season 2 default)

const BIRD_BOX = new THREE.BoxGeometry(1, 1, 1);
const BIRD_MAT = new THREE.MeshLambertMaterial({color: '#2b2a33'});
/** Small voxel birds circling the island in two loose flocks, wings flapping. Each flock laps the Isle a whole number
 * of times per episode (and every flap and bob repeats too), so the birds are where frame 0 has them at the loop. */
const Birds: React.FC<{t: number; n: number; loopT?: number}> = ({t, n, loopT}) => {
	const orbit = loopFreq(0.1, loopT);
	const bob = loopFreq(1.1, loopT);
	const flapW = loopFreq(8.5, loopT);
	return (
		<group>
			{Array.from({length: n}, (_, i) => {
				const f = i % 2;
				const R = (f ? 25 : 19) + (i % 3) * 1.4;
				const w = f ? -orbit : orbit;
				const a = (f ? 2.1 : 0.4) + w * t + i * 0.09 + (i % 4) * 0.05;
				const y = (f ? 19 : 16) + Math.sin(t * bob + i) * 0.7 + (i % 3) * 0.6;
				const flap = Math.sin(t * flapW + i * 1.7) * 0.75;
				const heading = -a + (w > 0 ? 0 : Math.PI);
				return (
					<group key={i} position={[Math.cos(a) * R, y, Math.sin(a) * R]} rotation={[0, heading, 0]} scale={0.9}>
						<mesh geometry={BIRD_BOX} material={BIRD_MAT} scale={[0.2, 0.16, 0.55]} castShadow />
						<group rotation={[0, 0, flap]}>
							<mesh geometry={BIRD_BOX} material={BIRD_MAT} position={[0.38, 0, 0]} scale={[0.62, 0.05, 0.26]} />
						</group>
						<group rotation={[0, 0, -flap]}>
							<mesh geometry={BIRD_BOX} material={BIRD_MAT} position={[-0.38, 0, 0]} scale={[0.62, 0.05, 0.26]} />
						</group>
					</group>
				);
			})}
		</group>
	);
};

const MOTE_BOX = new THREE.BoxGeometry(1, 1, 1);
const moteM4 = new THREE.Matrix4();
const moteQ = new THREE.Quaternion();
const moteV = new THREE.Vector3();
const moteS = new THREE.Vector3();
/** Drifting pollen / firefly motes over the meadows: one or two pixels each at the stage's resolution, twinkling. */
const Motes: React.FC<{t: number; n: number; island: Island; warm: number; loopT?: number}> = ({t, n, island, warm, loopT}) => {
	const ref = React.useRef<THREE.InstancedMesh>(null);
	const mat = useMemo(() => new THREE.MeshBasicMaterial({color: '#fff4cf'}), []);
	const homes = useMemo(() => {
		const out: [number, number, number][] = [];
		let k = 0;
		while (out.length < n && k < n * 20) {
			const x = (hash2(k, 1, 71) - 0.5) * 36;
			const z = (hash2(k, 2, 71) - 0.5) * 36;
			const c = island.columnAt(x, z);
			if (c && (c.biome === 'meadow' || c.biome === 'forest' || c.biome === 'sand')) out.push([x, z, c.top]);
			k++;
		}
		return out;
	}, [island, n]);
	React.useLayoutEffect(() => {
		const m = ref.current!;
		mat.color.set(warm > 0.6 ? '#ffd889' : '#f4f7dc');
		const [wx, wz, wy, wt] = [0.21, 0.17, 0.6, 2.4].map((w) => loopFreq(w, loopT));
		homes.forEach(([hx, hz, top], i) => {
			const x = hx + Math.sin(t * wx + i * 1.3) * 1.6;
			const z = hz + Math.cos(t * wz + i * 2.1) * 1.6;
			const y = top + 1.1 + Math.sin(t * wy + i) * 0.9 + (i % 3) * 0.4;
			const tw = 0.6 + 0.4 * Math.max(0, Math.sin(t * wt + i * 1.9));
			moteM4.compose(moteV.set(x, y, z), moteQ.identity(), moteS.setScalar(0.16 * tw));
			m.setMatrixAt(i, moteM4);
		});
		m.instanceMatrix.needsUpdate = true;
	});
	return <instancedMesh ref={ref} args={[MOTE_BOX, mat, homes.length]} frustumCulled={false} />;
};

/**
 * A shadow-only flyer (the next episode's dragon): invisible to the camera, it still casts its winged shadow. It is
 * kept flat and only ripples its wingtips: under a low sun any height change throws the shadow a long way.
 */
const SHADOW_ONLY = new THREE.MeshBasicMaterial({colorWrite: false, depthWrite: false});
const Flyer: React.FC<{t: number; f: World['flyers'][number]; sun: [number, number, number]; island: Island}> = ({t, f, sun, island}) => {
	const p = (t - f.t) / f.dur;
	if (p < 0 || p > 1) return null;
	const gx = f.from[0] + (f.to[0] - f.from[0]) * p;
	const gz = f.from[1] + (f.to[1] - f.from[1]) * p;
	const gy = Math.max(island.waterLevel, island.heightAt(gx, gz));
	const q: [number, number, number] = [gx + sun[0] * f.height, gy + sun[1] * f.height, gz + sun[2] * f.height];
	const heading = Math.atan2(-(f.to[1] - f.from[1]), f.to[0] - f.from[0]);
	const flap = 0.88 + 0.12 * Math.sin(t * 6.2);
	return (
		<group position={q} rotation={[0, heading, 0]} scale={f.scale}>
			<mesh geometry={BIRD_BOX} material={SHADOW_ONLY} scale={[6.5, 0.35, 1.4]} castShadow />
			<mesh geometry={BIRD_BOX} material={SHADOW_ONLY} position={[4.3, 0, 0]} scale={[2.3, 0.3, 0.75]} castShadow />
			<mesh geometry={BIRD_BOX} material={SHADOW_ONLY} position={[-5.6, 0, 0]} scale={[5.6, 0.25, 0.5]} castShadow />
			<mesh geometry={BIRD_BOX} material={SHADOW_ONLY} position={[-8.7, 0, 0]} scale={[1.0, 0.25, 1.1]} castShadow />
			{[1, -1].map((side) => (
				<group key={side} scale={[1, 1, flap]}>
					<mesh geometry={BIRD_BOX} material={SHADOW_ONLY} position={[0.5, 0, side * 3.7]} scale={[3.8, 0.2, 6.2]} castShadow />
					<mesh geometry={BIRD_BOX} material={SHADOW_ONLY} position={[-0.8, 0, side * 7.8]} scale={[2.4, 0.2, 2.6]} castShadow />
					<mesh geometry={BIRD_BOX} material={SHADOW_ONLY} position={[-2.2, 0, side * 5.2]} scale={[1.4, 0.2, 1.2]} castShadow />
				</group>
			))}
		</group>
	);
};

export type WorldSceneProps = {world: World; t: number; herdCenters: [number, number][]; herdBase: number};

export const useWorldState = (world: World, t: number, herdCenters: [number, number][], herdBase: number): S2State => {
	const island = isle();
	const agents = useMemo(() => buildHerd(island, world.herdMax, herdBase, herdCenters), [island, world.herdMax, herdBase, herdCenters]);
	const agentsB = useMemo(() => (world.herdCentersB ? buildHerd(island, world.herdMax, herdBase, world.herdCentersB) : undefined), [island, world.herdMax, herdBase, world.herdCentersB]);
	return {world, t, cam: cameraAt(world, t, (x, z) => Math.max(island.waterLevel, island.heightAt(x, z))), island, agents, agentsB};
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
	const {world, t, cam, island, agents, agentsB} = state;
	const ROAD_C = useMemo(() => new THREE.Color('#a88458'), []);
	const births = useMemo(() => birthTimes(world, world.herdMax), [world]);
	// EP27+: land cleared for the village (both sites, the pens and the tower): no trees inside the buildings
	const cleared = useMemo(() => {
		const out = new Set<number>();
		if (!world.settlements.length && !world.clearTrees.length) return out;
		const spots: [number, number, number][] = [...world.clearTrees];
		for (const st of world.settlements) {
		for (const b of st.buildings) {
			const r = b.kind === 'greathall' ? 4.2 : b.kind === 'hall' ? 2.4 : 1.6;
			spots.push([b.a[0], b.a[1], r]);
			if (b.b) spots.push([b.b[0], b.b[1], r]);
		}
		for (const p of st.pens) {
			spots.push([p.a[0], p.a[1], (p.r ?? 2.4) + 1.2]);
			if (p.b) spots.push([p.b[0], p.b[1], (p.r ?? 2.4) + 1.2]);
		}
		if (st.tower) spots.push([st.tower.x, st.tower.z, 1.6]);
		// a lane through the trees along each road (the carts must be seen under the canopy)
		for (const road of [st.roads.a, st.roads.b])
			for (let i = 0; i + 1 < road.length; i++)
				for (let f = 0; f <= 1; f += 0.1) spots.push([road[i][0] + (road[i + 1][0] - road[i][0]) * f, road[i][1] + (road[i + 1][1] - road[i][1]) * f, 0.8]);
		}
		island.trees.forEach((tr, k) => {
			if (spots.some(([x, z, r]) => Math.hypot(tr.x - x, tr.z - z) < r)) out.add(k);
		});
		return out;
	}, [world, island]);
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
		if (world.ambient.glints && c.biome === 'water') {
			const g = hash2(c.i, c.j, Math.floor(t * 6) + 77);
			if (g > 0.9) out.lerp(GLINT, ((g - 0.9) / 0.1) * 0.75);
		}
		if (graze > 0 && (c.biome === 'meadow' || (c.biome === 'forest' && graze > 0.5))) {
			const thr = c.biome === 'forest' ? (graze - 0.5) * 1.6 : graze * 1.08;
			if (c.r < thr) out.copy(DIRT_C[Math.floor(c.r * 97) % DIRT_C.length]);
			else if (c.r < thr + 0.12) out.lerp(DIRT_C[0], 0.45);
		}
		if (c.biome !== 'water')
			for (const st of world.settlements) {
				const r = roadAt(st, t, c.x, c.z);
				if (r > 0) out.lerp(ROAD_C, r * (0.75 + 0.15 * c.r));
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
		if (cleared.has(k)) return 0;
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
			backdrop={<PixelStars t={t} level={0.35 + 0.45 * (1 - mood.sun)} loopT={world.loopT} />}
		>
			{/* Distance haze in the void's colour: the far side of the island recedes a little (diorama depth). */}
			<fog attach="fog" args={[mood.sky[1], cam.dist * 0.98, cam.dist + 120]} />
			<Lights sun={mood.sun} warm={mood.warm} hemi={mood.hemi} az={mood.az} el={mood.el} />
			<IslandMesh island={island} t={t} tint={tint} treeScale={treeScale} treeTint={treeTint} lift={lift} loopT={world.loopT} />
			<Herd
				island={island}
				agents={agents}
				count={count}
				s={s}
				t={t}
				loopT={world.loopT}
				pale={herdPale}
				skin={world.herdSkin}
				agentsB={agentsB}
				site={world.settlement ? sample(world.settlement.place, t, 0) : 0}
				born={(i) => {
					const b = births[i].filter((x) => x <= t).pop();
					return b === undefined ? 1 : clamp((t - b) / 4.5);
				}}
			/>
			{poses.map((p, i) => (p ? <Grimmaw key={i} pose={p} /> : null))}
			{world.settlements.map((st, i) => (
				<SettlementLayer key={`st${i}`} world={world} island={island} t={t} s={s} settlement={st} />
			))}
			{world.folk && <FolkLayer world={world} island={island} t={t} s={s} />}
			{world.dragons.map((d) => {
				const dp = dragonAt(d.keys, t, (x, z) => Math.max(island.waterLevel, island.heightAt(x, z)));
				return dp ? <Dragon key={d.id} pose={dp} scale={d.scale} t={t} loopT={world.loopT} /> : null;
			})}
			{world.props.map((p, i) => (p.kind === 'cairn' ? <Cairn key={`c${i}`} x={p.x} z={p.z} y={island.heightAt(p.x, p.z)} stones={sample(p.stones, t, 0)} /> : null))}
			{world.ambient.birds > 0 && <Birds t={t} n={world.ambient.birds} loopT={world.loopT} />}
			{world.ambient.motes > 0 && <Motes t={t} n={world.ambient.motes} island={island} warm={mood.warm} loopT={world.loopT} />}
			{world.flyers.map((f, i) => (
				<Flyer key={`f${i}`} t={t} f={f} sun={sunDir(mood.az, mood.el)} island={island} />
			))}
			{world.dust.map((d, i) => (
				<Dust key={`d${i}`} t={t} at={d.t} x={d.x} z={d.z} y={island.heightAt(d.x, d.z)} r={d.r} />
			))}
		</Stage>
	);
};

export {BIOME_COLORS};
