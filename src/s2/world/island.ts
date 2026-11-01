// The Season 2 world: one voxel island, generated from a seed. Every episode builds on the same island
// ("the Isle"), so its shape is fixed by `ISLE_SEED`; episodes change what lives on it, not the ground.
import {clamp, fbm, hash2, smoothstep} from '../rng';

export type Biome = 'water' | 'sand' | 'meadow' | 'forest' | 'rock' | 'snow';

export type Column = {
	i: number;
	j: number;
	x: number;
	z: number;
	/** top of the column (world units; one voxel = 1) */
	top: number;
	/** bottom of the column (the island's underside) */
	bottom: number;
	biome: Biome;
	/** 0..1 per-column random, for colour variation and patchy effects */
	r: number;
	/** distance from centre, 0..1 */
	d: number;
};

export type Tree = {x: number; z: number; y: number; h: number; r: number; col: number};

export type Island = {
	n: number;
	columns: Column[];
	grid: (Column | undefined)[][];
	trees: Tree[];
	waterLevel: number;
	heightAt: (x: number, z: number) => number;
	columnAt: (x: number, z: number) => Column | undefined;
};

export const ISLE_SEED = 26;
export const ISLE_N = 46;

// Landmarks in world units (x right, z towards the camera). Episodes refer to these by name.
export const LANDMARKS = {
	peak: [-9, -9] as [number, number],
	lake: [7, 5] as [number, number],
	meadow: [3, -3] as [number, number],
	forest: [-8, 7] as [number, number],
};

const gauss = (x: number, z: number, cx: number, cz: number, s: number) => Math.exp(-((x - cx) ** 2 + (z - cz) ** 2) / (2 * s * s));

export const buildIsland = (seed = ISLE_SEED, n = ISLE_N): Island => {
	const half = n / 2;
	const columns: Column[] = [];
	const grid: (Column | undefined)[][] = Array.from({length: n}, () => Array(n).fill(undefined));
	const waterLevel = 2;
	for (let i = 0; i < n; i++) {
		for (let j = 0; j < n; j++) {
			const x = i - half + 0.5;
			const z = j - half + 0.5;
			const d0 = Math.hypot(x, z) / (half - 1.5);
			const coast = (fbm(x * 0.09, z * 0.09, seed + 3) - 0.5) * 0.42;
			const d = d0 + coast;
			if (d > 1) continue;
			const rolling = 2.6 + fbm(x * 0.11, z * 0.11, seed) * 3.2;
			const mountain = gauss(x, z, LANDMARKS.peak[0], LANDMARKS.peak[1], 4.8) * 9.4 + gauss(x, z, -3, -13, 3.5) * 3.0;
			const lakeDip = gauss(x, z, LANDMARKS.lake[0], LANDMARKS.lake[1], 3.6) * 4.2;
			// River: from the mountain's foot down to the lake, wobbling.
			const tRiver = clamp(((x + 5) * 12 + (z + 4) * 9) / (12 * 12 + 9 * 9));
			const rx = -5 + 12 * tRiver + Math.sin(tRiver * 7) * 1.6;
			const rz = -4 + 9 * tRiver - Math.sin(tRiver * 5) * 1.2;
			const riverDist = Math.hypot(x - rx, z - rz);
			const river = tRiver > 0.02 && tRiver < 0.98 ? (1 - smoothstep(0.6, 1.6, riverDist)) * 2.2 : 0;
			const edgeDrop = smoothstep(0.82, 1.0, d) * 1.5;
			let top = Math.round(rolling + mountain - lakeDip - river - edgeDrop);
			top = Math.max(1, top);
			const r = hash2(i, j, seed + 99);
			let biome: Biome;
			if (top <= waterLevel && (lakeDip > 0.6 || river > 0.5)) biome = 'water';
			else if (top <= waterLevel + 1 && (lakeDip > 0.25 || river > 0.15 || d > 0.9)) biome = 'sand';
			else if (top >= 12) biome = 'snow';
			else if (top >= 8) biome = 'rock';
			else if (fbm(x * 0.12, z * 0.12, seed + 41) + (x < -2 && z > 0 ? 0.12 : -0.1) > 0.6 && mountain < 4) biome = 'forest';
			else biome = 'meadow';
			if (biome === 'water') top = waterLevel;
			const depth = 3 + (1 - clamp(d0)) * 9 + fbm(x * 0.2, z * 0.2, seed + 7) * 4;
			const col: Column = {i, j, x, z, top, bottom: -depth, biome, r, d: clamp(d0)};
			columns.push(col);
			grid[i][j] = col;
		}
	}
	const trees: Tree[] = [];
	columns.forEach((c, idx) => {
		if (c.biome === 'forest' && c.r < 0.62) {
			trees.push({x: c.x + (hash2(c.i, c.j, 5) - 0.5) * 0.4, z: c.z + (hash2(c.i, c.j, 6) - 0.5) * 0.4, y: c.top, h: 1.3 + hash2(c.i, c.j, 7) * 1.1, r: hash2(c.i, c.j, 8), col: idx});
		} else if (c.biome === 'meadow' && c.r < 0.035) {
			trees.push({x: c.x, z: c.z, y: c.top, h: 1.1 + c.r * 10, r: hash2(c.i, c.j, 8), col: idx});
		}
	});
	const columnAt = (x: number, z: number) => {
		const i = Math.floor(x + half);
		const j = Math.floor(z + half);
		return i >= 0 && j >= 0 && i < n && j < n ? grid[i][j] : undefined;
	};
	const heightAt = (x: number, z: number) => columnAt(x, z)?.top ?? -40;
	return {n, columns, grid, trees, waterLevel, heightAt, columnAt};
};

let cached: Island | null = null;
/** The shared island (built once per tab). */
export const isle = () => (cached ??= buildIsland());
