/** Deterministic PRNG so every render of a scene is identical. */
export const rng = (seed: number) => {
	let s = seed >>> 0;
	return () => {
		s = (s + 0x6d2b79f5) >>> 0;
		let t = s;
		t = Math.imul(t ^ (t >>> 15), t | 1);
		t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
};

export type RidgeOpts = {
	baseY: number;
	amp: number;
	rough?: number;
	octaves?: number;
	/** Ridged multifractal: sharp crests instead of rolling hills. */
	ridged?: boolean;
	x0?: number;
	x1?: number;
	step?: number;
	bottom?: number;
};

/** 1-D fractal value noise ridge: returns an SVG path closed to the bottom of the frame. */
export const ridgePath = (seed: number, opts: RidgeOpts) => {
	const {x0 = -260, x1 = 1340, bottom = 2100} = opts;
	const pts = ridgePoints(seed, opts).map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`);
	return `M${x0},${bottom} L${pts.join(' L')} L${x1},${bottom} Z`;
};

/** Height of a ridge at x (for placing towers, trees, figures on it). */
export const ridgeYAt = (seed: number, opts: RidgeOpts, x: number) => {
	const pts = ridgePoints(seed, opts);
	const i = pts.findIndex((p) => p[0] >= x);
	if (i <= 0) return pts[0][1];
	const [xa, ya] = pts[i - 1];
	const [xb, yb] = pts[i];
	return ya + ((yb - ya) * (x - xa)) / (xb - xa);
};

export const ridgePoints = (
	seed: number,
	{baseY, amp, rough = 0.55, octaves = 6, ridged = false, x0 = -260, x1 = 1340, step = 8}: RidgeOpts,
): [number, number][] => {
	const r = rng(seed);
	const layers = Array.from({length: octaves}, (_, o) => {
		const n = 2 + 2 ** o;
		return {n, pts: Array.from({length: n + 2}, () => r() * 2 - 1), a: rough ** o};
	});
	const norm = layers.reduce((s, l) => s + l.a, 0);
	const pts: [number, number][] = [];
	for (let x = x0; x <= x1; x += step) {
		const u = (x - x0) / (x1 - x0);
		let y = 0;
		for (const l of layers) {
			const f = u * l.n;
			const i = Math.floor(f);
			const k = f - i;
			const sm = k * k * (3 - 2 * k);
			const v = l.pts[i] * (1 - sm) + l.pts[i + 1] * sm;
			y += (ridged ? (1 - Math.abs(v)) ** 2 * 2 - 1 : v) * l.a;
		}
		pts.push([x, baseY - (y / norm) * amp]);
	}
	return pts;
};

export const mix = (a: string, b: string, p: number) => {
	const pa = a.match(/\w\w/g)!.map((h) => parseInt(h, 16));
	const pb = b.match(/\w\w/g)!.map((h) => parseInt(h, 16));
	return '#' + pa.map((v, i) => Math.round(v + (pb[i] - v) * p).toString(16).padStart(2, '0')).join('');
};
