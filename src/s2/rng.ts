// Deterministic helpers for Season 2 worlds. Every frame must be computable on its own (Remotion renders frames
// out of order across tabs), so nothing here keeps state between frames: only seeded functions of (seed, x, t).

/** mulberry32: small, fast, seeded PRNG. */
export const rng = (seed: number) => {
	let a = seed >>> 0;
	return () => {
		a = (a + 0x6d2b79f5) >>> 0;
		let t = a;
		t = Math.imul(t ^ (t >>> 15), t | 1);
		t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
};

/** Integer hash -> [0, 1). */
export const hash2 = (x: number, y: number, seed = 0) => {
	let h = (x * 374761393 + y * 668265263 + seed * 2147483647) | 0;
	h = Math.imul(h ^ (h >>> 13), 1274126177);
	h ^= h >>> 16;
	return (h >>> 0) / 4294967296;
};

const smooth = (t: number) => t * t * (3 - 2 * t);

/** 2D value noise in [0, 1). */
export const noise2 = (x: number, y: number, seed = 0) => {
	const xi = Math.floor(x);
	const yi = Math.floor(y);
	const xf = smooth(x - xi);
	const yf = smooth(y - yi);
	const a = hash2(xi, yi, seed);
	const b = hash2(xi + 1, yi, seed);
	const c = hash2(xi, yi + 1, seed);
	const d = hash2(xi + 1, yi + 1, seed);
	return a + (b - a) * xf + (c - a) * yf + (a - b - c + d) * xf * yf;
};

/** Fractal value noise, 0..1. */
export const fbm = (x: number, y: number, seed = 0, octaves = 4) => {
	let s = 0;
	let amp = 0.5;
	let f = 1;
	let norm = 0;
	for (let i = 0; i < octaves; i++) {
		s += noise2(x * f, y * f, seed + i * 17) * amp;
		norm += amp;
		amp *= 0.5;
		f *= 2;
	}
	return s / norm;
};

/** 1D smooth noise in [-1, 1] for wandering paths. */
export const wander = (t: number, seed: number) => noise2(t, seed * 13.37, seed) * 2 - 1;

export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const smoothstep = (a: number, b: number, x: number) => {
	const t = clamp((x - a) / (b - a));
	return t * t * (3 - 2 * t);
};
