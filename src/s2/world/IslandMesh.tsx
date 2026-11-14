// Renders the voxel island: terrain columns (with soil/rock strata on the cut sides), trees and water.
// Colours can change per frame (grazing, seasons) through `tint`, without rebuilding geometry.
import React, {useLayoutEffect, useMemo, useRef} from 'react';
import * as THREE from 'three';
import {loopFreq} from '../keys';
import {Column, Island} from './island';
import type {Strata} from './timeline';

export const BIOME_COLORS: Record<string, string[]> = {
	water: ['#3f86b0', '#4790b9', '#3a7ca5'],
	sand: ['#dcc895', '#d4bf8a', '#e2cf9f'],
	meadow: ['#86bb5c', '#7cb254', '#8fc266', '#79ab50'],
	forest: ['#557f3c', '#4f7838', '#5b8742'],
	rock: ['#8c9097', '#80858d', '#979ba1'],
	snow: ['#eef3f5', '#e4ebee', '#f6f9fa'],
};
export const DIRT = ['#8f6c46', '#86633f', '#977450'];

const tmpM = new THREE.Matrix4();
const tmpC = new THREE.Color();
const tmpC2 = new THREE.Color();

// EP32+: the war as a layer of the island (`world.strata`), with centuries laid on top and consequences running up
// through them as veins. Injected only when an episode has strata, so every older episode compiles the same shader.
const STRATA_GLSL = `
					vec3 wpat = vec3(0.19, 0.14, 0.16);
					{
						vec2 cell = floor(vec2(vWX + vWZ, y) * 3.0);
						float h = fract(sin(dot(cell, vec2(12.9898, 78.233))) * 43758.5453);
						if (h > 0.86) wpat = uWarFleck;
						else if (h > 0.8) wpat = vec3(0.82, 0.78, 0.7);
						else if (h > 0.7) wpat = vec3(0.42, 0.17, 0.13);
					}
					float sy0 = uWar.x;
					float sy1 = uWar.y;
					float th = (uWar.z - sy1) / max(1.0, uCen.y);
					if (y > sy1 && th > 0.01) {
						float k = floor((y - sy1) / th);
						float fk = fract((y - sy1) / th);
						if (k < uCen.x && y < uWar.z + 0.6) {
							vec3 cb = mod(k, 2.0) < 1.0 ? vec3(0.56, 0.43, 0.3) : vec3(0.48, 0.36, 0.25);
							if (fk > 0.8) cb *= 0.6;
							c = cb;
						}
						if (k < uCen.z * uCen.y) c = fk > 0.8 ? wpat * 0.7 : wpat;
					}
					if (y >= sy0 && y <= sy1) c = mix(wpat, c * 0.85, uWar.w);
					for (int i = 0; i < 4; i++) {
						vec4 b = uVeinBox[i];
						vec4 vc = uVeinCol[i];
						if (vc.w > 0.001 && vWX > b.x && vWX < b.y && vWZ > b.z && vWZ < b.w && y > sy0 && y < sy1 + vc.w * (vTop - sy1)) {
							float e = min(min(vWX - b.x, b.y - vWX), min(vWZ - b.z, b.w - vWZ));
							c = e < 0.1 ? vc.rgb * 0.55 : vc.rgb;
						}
					}
					c = mix(vec3(dot(c, vec3(0.299, 0.587, 0.114))), c, uCen.w);`;

type StrataU = {uWar: {value: THREE.Vector4}; uCen: {value: THREE.Vector4}; uWarFleck: {value: THREE.Color}; uVeinBox: {value: THREE.Vector4[]}; uVeinCol: {value: THREE.Vector4[]}};

/** Patch a Lambert material: per-instance column top -> strata colours on the cut sides, plus faint voxel banding. */
const strataMaterial = (u?: StrataU) => {
	const m = new THREE.MeshLambertMaterial({vertexColors: false});
	m.onBeforeCompile = (shader) => {
		if (u) Object.assign(shader.uniforms, u);
		shader.vertexShader = shader.vertexShader
			.replace('#include <common>', '#include <common>\nattribute float aTop;\nvarying float vTop;\nvarying float vWY;\nvarying float vUp;' + (u ? '\nvarying float vWX;\nvarying float vWZ;' : ''))
			.replace(
				'#include <project_vertex>',
				'#include <project_vertex>\nvTop = aTop;\nvec4 wpS = modelMatrix * instanceMatrix * vec4(transformed, 1.0);\nvWY = wpS.y;\nvUp = normal.y;' + (u ? '\nvWX = wpS.x;\nvWZ = wpS.z;' : ''),
			);
		shader.fragmentShader = shader.fragmentShader
			.replace(
				'#include <common>',
				'#include <common>\nvarying float vTop;\nvarying float vWY;\nvarying float vUp;' +
					(u ? '\nvarying float vWX;\nvarying float vWZ;\nuniform vec4 uWar;\nuniform vec4 uCen;\nuniform vec3 uWarFleck;\nuniform vec4 uVeinBox[4];\nuniform vec4 uVeinCol[4];' : ''),
			)
			.replace(
				'#include <color_fragment>',
				`#include <color_fragment>
				if (vUp < 0.5 && vWY < vTop - 0.45) {
					float y = vWY;
					vec3 soil = vec3(0.45, 0.31, 0.20);
					vec3 clay = vec3(0.50, 0.36, 0.25);
					vec3 rock = vec3(0.40, 0.41, 0.45);
					vec3 deep = vec3(0.25, 0.25, 0.32);
					vec3 c = y > 4.5 ? rock * 1.15 : (y > vTop - 2.2 ? soil : (y > -1.5 ? clay : (y > -6.0 ? rock : deep)));
					c *= mod(floor(y), 2.0) < 1.0 ? 0.92 : 1.0;${u ? STRATA_GLSL : ''}
					diffuseColor.rgb = c;
				}
				if (vUp < -0.5) diffuseColor.rgb = vec3(0.16, 0.16, 0.22);`,
			);
	};
	return m;
};

type Props = {
	island: Island;
	/** per-column colour override, e.g. grazing: (col, base) => colour */
	tint?: (c: Column, base: THREE.Color, out: THREE.Color) => void;
	/** 0..1 tree visibility per tree index (saplings eaten, forests thinning) */
	treeScale?: (idx: number) => number;
	/** per-column vertical offset (the World Engine "ripple"); trees ride along */
	lift?: (c: Column) => number;
	/** mutate a tree part colour in place (snow, desaturation); part 0 trunk, 1 crown, 2 crown top */
	treeTint?: (c: THREE.Color, k: number, part: number) => void;
	t: number;
	/** the episode's length: the water shimmer repeats over it (seamless loop); omit outside episodes */
	loopT?: number;
	/** EP32+: the war layer, the centuries on it and the veins through them (omit: the cut sides as before) */
	strata?: Strata | null;
	/** EP32+: the mood's saturation, applied to the strata */
	sat?: number;
};

export const IslandMesh: React.FC<Props> = ({island, tint, treeScale, lift, treeTint, t, loopT, strata, sat = 1}) => {
	const terrain = useRef<THREE.InstancedMesh>(null);
	const trunks = useRef<THREE.InstancedMesh>(null);
	const crowns = useRef<THREE.InstancedMesh>(null);
	const crownTops = useRef<THREE.InstancedMesh>(null);
	const box = useMemo(() => new THREE.BoxGeometry(1, 1, 1), []);
	const hasStrata = !!strata;
	const su = useMemo<StrataU | undefined>(
		() =>
			hasStrata
				? {
						uWar: {value: new THREE.Vector4()},
						uCen: {value: new THREE.Vector4()},
						uWarFleck: {value: new THREE.Color('#46c2a0')},
						uVeinBox: {value: [0, 1, 2, 3].map(() => new THREE.Vector4())},
						uVeinCol: {value: [0, 1, 2, 3].map(() => new THREE.Vector4())},
					}
				: undefined,
		[hasStrata],
	);
	const terrainMat = useMemo(() => strataMaterial(su), [su]);
	if (su && strata) {
		su.uWar.value.set(strata.y0, strata.y1, strata.surface, strata.fade);
		su.uCen.value.set(strata.n, strata.max, strata.flood, sat);
		for (let i = 0; i < 4; i++) {
			const v = strata.veins[i];
			if (v) {
				su.uVeinBox.value[i].set(v.box[0], v.box[1], v.box[2], v.box[3]);
				tmpC.set(v.color);
				su.uVeinCol.value[i].set(tmpC.r, tmpC.g, tmpC.b, v.on);
			} else su.uVeinCol.value[i].set(0, 0, 0, 0);
		}
	}
	const plainMat = useMemo(() => new THREE.MeshLambertMaterial(), []);
	const base = useMemo(
		() =>
			island.columns.map((c) => {
				const pal = BIOME_COLORS[c.biome];
				return new THREE.Color(pal[Math.floor(c.r * pal.length) % pal.length]);
			}),
		[island],
	);

	const geo = useMemo(() => {
		const g = box.clone();
		const tops = new Float32Array(island.columns.length);
		island.columns.forEach((c, k) => {
			tops[k] = c.biome === 'water' ? c.top - 0.25 : c.top;
		});
		g.setAttribute('aTop', new THREE.InstancedBufferAttribute(tops, 1));
		return g;
	}, [island, box]);

	// Matrices every frame (the ripple can lift any column); the strata shader reads the un-lifted top, so the
	// lifted column keeps its colours.
	useLayoutEffect(() => {
		const m = terrain.current!;
		const tops = geo.getAttribute('aTop') as THREE.InstancedBufferAttribute;
		island.columns.forEach((c, k) => {
			const dy = lift ? lift(c) : 0;
			const top = (c.biome === 'water' ? c.top - 0.25 : c.top) + dy;
			const h = top - c.bottom;
			tmpM.makeScale(1, h, 1).setPosition(c.x, c.bottom + h / 2, c.z);
			m.setMatrixAt(k, tmpM);
			tops.setX(k, top);
		});
		tops.needsUpdate = true;
		m.instanceMatrix.needsUpdate = true;
	});

	// Colours every frame (cheap: ~1.7k columns).
	const shimmer = loopFreq(2.2, loopT);
	useLayoutEffect(() => {
		const m = terrain.current!;
		island.columns.forEach((c, k) => {
			tmpC.copy(base[k]);
			if (c.biome === 'water') {
				const s = 0.04 * Math.sin(t * shimmer + c.x * 0.9 + c.z * 0.7);
				tmpC.offsetHSL(0, 0, s);
			}
			if (tint) {
				tint(c, tmpC, tmpC2);
				tmpC.copy(tmpC2);
			}
			m.setColorAt(k, tmpC);
		});
		if (m.instanceColor) m.instanceColor.needsUpdate = true;
	});

	useLayoutEffect(() => {
		const tr = trunks.current!;
		const cr = crowns.current!;
		const ct = crownTops.current!;
		island.trees.forEach((tree, k) => {
			const s = treeScale ? treeScale(k) : 1;
			const dy = lift ? lift(island.columns[tree.col]) : 0;
			const h = tree.h * Math.max(0.0001, s);
			tmpM.makeScale(0.28, h * 0.55, 0.28).setPosition(tree.x, tree.y + dy + (h * 0.55) / 2, tree.z);
			tr.setMatrixAt(k, tmpM);
			const cw = (0.95 + tree.r * 0.3) * Math.max(0.0001, s);
			tmpM.makeScale(cw, h * 0.5, cw).setPosition(tree.x, tree.y + dy + h * 0.55 + (h * 0.5) / 2 - 0.1, tree.z);
			cr.setMatrixAt(k, tmpM);
			tmpM.makeScale(cw * 0.55, h * 0.3, cw * 0.55).setPosition(tree.x, tree.y + dy + h * 1.02 + (h * 0.3) / 2 - 0.12, tree.z);
			ct.setMatrixAt(k, tmpM);
			const paint = (m: THREE.InstancedMesh, hex: string, part: number) => {
				tmpC.set(hex);
				if (treeTint) treeTint(tmpC, k, part);
				m.setColorAt(k, tmpC);
			};
			paint(tr, '#6a4a30', 0);
			paint(cr, tree.r < 0.5 ? '#2f6a3c' : '#3a7a44', 1);
			paint(ct, tree.r < 0.5 ? '#3d7f48' : '#4a8c50', 2);
		});
		[tr, cr, ct].forEach((m) => {
			m.instanceMatrix.needsUpdate = true;
			if (m.instanceColor) m.instanceColor.needsUpdate = true;
		});
	});

	const nt = island.trees.length;
	return (
		<group>
			<instancedMesh ref={terrain} args={[geo, terrainMat, island.columns.length]} castShadow receiveShadow frustumCulled={false} />
			<instancedMesh ref={trunks} args={[box, plainMat, nt]} castShadow receiveShadow frustumCulled={false} />
			<instancedMesh ref={crowns} args={[box, plainMat, nt]} castShadow receiveShadow frustumCulled={false} />
			<instancedMesh ref={crownTops} args={[box, plainMat, nt]} receiveShadow frustumCulled={false} />
		</group>
	);
};
