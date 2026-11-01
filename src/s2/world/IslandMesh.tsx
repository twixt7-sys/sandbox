// Renders the voxel island: terrain columns (with soil/rock strata on the cut sides), trees and water.
// Colours can change per frame (grazing, seasons) through `tint`, without rebuilding geometry.
import React, {useLayoutEffect, useMemo, useRef} from 'react';
import * as THREE from 'three';
import {Column, Island} from './island';

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

/** Patch a Lambert material: per-instance column top -> strata colours on the cut sides, plus faint voxel banding. */
const strataMaterial = () => {
	const m = new THREE.MeshLambertMaterial({vertexColors: false});
	m.onBeforeCompile = (shader) => {
		shader.vertexShader = shader.vertexShader
			.replace('#include <common>', '#include <common>\nattribute float aTop;\nvarying float vTop;\nvarying float vWY;\nvarying float vUp;')
			.replace(
				'#include <project_vertex>',
				'#include <project_vertex>\nvTop = aTop;\nvec4 wpS = modelMatrix * instanceMatrix * vec4(transformed, 1.0);\nvWY = wpS.y;\nvUp = normal.y;',
			);
		shader.fragmentShader = shader.fragmentShader
			.replace('#include <common>', '#include <common>\nvarying float vTop;\nvarying float vWY;\nvarying float vUp;')
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
					c *= mod(floor(y), 2.0) < 1.0 ? 0.92 : 1.0;
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
};

export const IslandMesh: React.FC<Props> = ({island, tint, treeScale, lift, treeTint, t}) => {
	const terrain = useRef<THREE.InstancedMesh>(null);
	const trunks = useRef<THREE.InstancedMesh>(null);
	const crowns = useRef<THREE.InstancedMesh>(null);
	const crownTops = useRef<THREE.InstancedMesh>(null);
	const box = useMemo(() => new THREE.BoxGeometry(1, 1, 1), []);
	const terrainMat = useMemo(() => strataMaterial(), []);
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
	useLayoutEffect(() => {
		const m = terrain.current!;
		island.columns.forEach((c, k) => {
			tmpC.copy(base[k]);
			if (c.biome === 'water') {
				const s = 0.04 * Math.sin(t * 2.2 + c.x * 0.9 + c.z * 0.7);
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
