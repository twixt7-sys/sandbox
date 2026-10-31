import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {rng} from '../lib/random';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, palette} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Sightline graphics (EP25, closing Arc 5): a terrifying caster with one tactical weakness. The Unmaker erases anything
 * she can see, and only what she can see. Her sight is drawn in code as a pale lilac beam on the plates (`gazeBeam`,
 * pinned with `"local": true`, reflecting off mirrors through `points`), what it erases dissolves cell by cell into the
 * dark (`unmake`), and the weakness is played out as a puzzle on a top-down courtyard plan (`sightPlan`): a real
 * line-of-sight cone, ray-cast against the cover every frame, so pillars, smoke, fog and walls cast true blind spots that
 * the heroes' route threads through.
 */

/** EP25's motif colour: her sight, a pale lilac. */
export const GAZE = '#c7b8f5';
const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const tone = (c: string | undefined, fallback: string) => (c ? ((palette as Record<string, string>)[c] ?? c) : fallback);
type P = [number, number];

/**
 * GazeBeam: her sight as a beam of pale light along `points: [[x, y], ...]` (plate px; the first point is her eye; each
 * further point is a mirror bounce or the end). `widths` gives the beam's width at each point (default 10 → 140).
 * It sweeps in from `start` (drawing out along the path over `draw` s, default 0.7) and fades at `end`. `sway: [dx, dy, period]`
 * swings the last point, as if she is looking around. Each cue in `flares` brightens it. Motes drift along it. Local.
 */
export const GazeBeam: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const pts0: P[] = g.points;
	const c = tone(g.color, GAZE);
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.2;
	const draw = ease(t, t0, g.draw ?? 0.7, Easing.out(Easing.cubic));
	const vis = out(t, tEnd, 0.35) * (g.instant ? 1 : ease(t, t0, 0.25));
	if (vis <= 0.001 || draw <= 0) return null;
	const sw: number[] = g.sway ?? [0, 0, 4];
	const phase = Math.sin(((t - t0) * 2 * Math.PI) / (sw[2] || 4));
	const pts: P[] = pts0.map((p, i) => (i === pts0.length - 1 ? [p[0] + sw[0] * phase, p[1] + sw[1] * phase] : p));
	const widths: number[] = g.widths ?? pts.map((_, i) => lerp(10, 140, i / Math.max(1, pts.length - 1)));
	const flares: number[] = (g.flares ?? []).map((q: Cue) => cueTime(timing, q));
	const boost = flares.reduce((m, p) => Math.max(m, t >= p ? Math.exp(-(t - p) * 2.5) : 0), 0);
	const breathe = 0.85 + 0.15 * Math.sin(t * 2 * Math.PI * 0.7);
	const a = (g.opacity ?? 0.8) * vis * (breathe + 0.5 * boost);
	// Segment lengths for the draw-on.
	const seg = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
	const total = seg.reduce((s, l) => s + l, 0);
	let budget = total * draw;
	const id = `gaze-${Math.round(pts0[0][0])}-${Math.round(pts0[0][1])}`;
	const polys: {quad: string; core: [P, P]; i: number; from: P; to: P}[] = [];
	for (let i = 0; i < seg.length && budget > 0; i++) {
		const f = Math.min(1, budget / seg[i]);
		budget -= seg[i];
		const p = pts[i];
		const q: P = [lerp(p[0], pts[i + 1][0], f), lerp(p[1], pts[i + 1][1], f)];
		const w0 = widths[i] / 2;
		const w1 = lerp(widths[i], widths[i + 1], f) / 2;
		const dx = q[0] - p[0];
		const dy = q[1] - p[1];
		const L = Math.hypot(dx, dy) || 1;
		const nx = -dy / L;
		const ny = dx / L;
		const quad = [
			[p[0] + nx * w0, p[1] + ny * w0],
			[q[0] + nx * w1, q[1] + ny * w1],
			[q[0] - nx * w1, q[1] - ny * w1],
			[p[0] - nx * w0, p[1] - ny * w0],
		]
			.map((v) => v.join(','))
			.join(' ');
		polys.push({quad, core: [p, q], i, from: p, to: q});
	}
	const motes = rng(31);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<filter id={`${id}-blur`} x="-50%" y="-50%" width="200%" height="200%">
						<feGaussianBlur stdDeviation={g.blur ?? 9} />
					</filter>
					{polys.map((s) => (
						<linearGradient key={s.i} id={`${id}-g${s.i}`} gradientUnits="userSpaceOnUse" x1={s.from[0]} y1={s.from[1]} x2={s.to[0]} y2={s.to[1]}>
							<stop offset="0%" stopColor={c} stopOpacity={s.i === 0 ? 0.85 : 0.6} />
							<stop offset="100%" stopColor={c} stopOpacity={s.i === polys.length - 1 && draw >= 1 ? 0.12 : 0.45} />
						</linearGradient>
					))}
				</defs>
				<g style={{mixBlendMode: 'screen'}} opacity={Math.min(1, a)}>
					{polys.map((s) => (
						<polygon key={s.i} points={s.quad} fill={`url(#${id}-g${s.i})`} filter={`url(#${id}-blur)`} />
					))}
					{polys.map((s) => (
						<line key={`c${s.i}`} x1={s.core[0][0]} y1={s.core[0][1]} x2={s.core[1][0]} y2={s.core[1][1]} stroke="#f3efff" strokeWidth={2.2} opacity={0.55} filter={`url(#${id}-blur)`} />
					))}
					{/* Bounce points flare like light caught in glass. */}
					{polys.slice(1).map((s) => (
						<circle key={`b${s.i}`} cx={s.from[0]} cy={s.from[1]} r={18 + 10 * boost} fill="#f3efff" opacity={0.7} filter={`url(#${id}-blur)`} />
					))}
					<circle cx={pts[0][0]} cy={pts[0][1]} r={7 + 4 * boost} fill="#f3efff" opacity={0.9} filter={`url(#${id}-blur)`} />
					{draw >= 1 &&
						Array.from({length: g.motes ?? 18}, (_, k) => {
							const sIdx = Math.floor(motes() * polys.length);
							const s = polys[sIdx];
							const speed = 0.18 + motes() * 0.2;
							const ph = (motes() + (t - t0) * speed) % 1;
							const off = (motes() - 0.5) * 0.8;
							const w = lerp(widths[s.i], widths[s.i + 1] ?? widths[s.i], ph) / 2;
							const dx = s.to[0] - s.from[0];
							const dy = s.to[1] - s.from[1];
							const L = Math.hypot(dx, dy) || 1;
							const mx = s.from[0] + dx * ph + (-dy / L) * w * off;
							const my = s.from[1] + dy * ph + (dx / L) * w * off;
							return <circle key={`m${k}`} cx={mx} cy={my} r={1.8 + (k % 3) * 0.8} fill="#f3efff" opacity={Math.sin(ph * Math.PI) * 0.85} />;
						})}
				</g>
			</svg>
		</AbsoluteFill>
	);
};

const inPoly = (x: number, y: number, poly: P[]) => {
	let inside = false;
	for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
		const [xi, yi] = poly[i];
		const [xj, yj] = poly[j];
		if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
	}
	return inside;
};

/**
 * Unmake: what her sight erases. `poly: [[x, y], ...]` (plate px) outlines the object. From `at` its edge lights lilac,
 * then from `at + edge` (default 0.5 s) it dissolves cell by cell (`cell` px, default 16) over `dur` s (default 1.2),
 * starting nearest `from: [x, y]` (where the gaze lands), into `void` (default a deep night gradient: the dark behind it).
 * Each cell sheds a mote of light that drifts up and away. Nothing is ever shown hurt: use it on things. Local.
 */
export const Unmake: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const poly: P[] = g.poly;
	const tA = cueTime(timing, g.at);
	const edgeDur = g.edge ?? 0.5;
	const dur = g.dur ?? 1.2;
	const cell = g.cell ?? 16;
	const c = tone(g.color, GAZE);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.2;
	const vis = out(t, tEnd, 0.3);
	if (t < tA - 0.05 || vis <= 0) return null;
	const xs = poly.map((p) => p[0]);
	const ys = poly.map((p) => p[1]);
	const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
	const [fx, fy] = g.from ?? [(x0 + x1) / 2, y0];
	const maxD = Math.max(...poly.map((p) => Math.hypot(p[0] - fx, p[1] - fy))) || 1;
	const r = rng(77);
	const cells: {x: number; y: number; d: number}[] = [];
	for (let y = y0; y < y1; y += cell) {
		for (let x = x0; x < x1; x += cell) {
			const jitter = r();
			if (!inPoly(x + cell / 2, y + cell / 2, poly)) continue;
			const d = Math.hypot(x + cell / 2 - fx, y + cell / 2 - fy) / maxD;
			cells.push({x, y, d: Math.min(1, d * 0.75 + jitter * 0.25)});
		}
	}
	const tD = tA + edgeDur;
	const edge = ease(t, tA, 0.35) * (1 - ease(t, tD + dur * 0.8, 0.5));
	const id = `unmake-${Math.round(x0)}-${Math.round(y0)}`;
	const gone = cells.filter((k) => t >= tD + k.d * dur);
	const path = poly.map((p, i) => `${i ? 'L' : 'M'}${p[0]},${p[1]}`).join(' ') + ' Z';
	const perim = poly.reduce((s, p, i) => s + Math.hypot(p[0] - poly[(i + 1) % poly.length][0], p[1] - poly[(i + 1) % poly.length][1]), 0);
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			<svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<clipPath id={`${id}-clip`}>
						{gone.map((k, i) => (
							<rect key={i} x={k.x - 0.5} y={k.y - 0.5} width={cell + 1} height={cell + 1} />
						))}
					</clipPath>
					<radialGradient id={`${id}-void`} cx="50%" cy="45%" r="70%">
						<stop offset="0%" stopColor={g.voidInner ?? '#1a2233'} />
						<stop offset="100%" stopColor={g.voidOuter ?? '#05070c'} />
					</radialGradient>
					<filter id={`${id}-blur`} x="-50%" y="-50%" width="200%" height="200%">
						<feGaussianBlur stdDeviation={4} />
					</filter>
				</defs>
				<g clipPath={`url(#${id}-clip)`}>
					<rect x={x0 - 2} y={y0 - 2} width={x1 - x0 + 4} height={y1 - y0 + 4} fill={`url(#${id}-void)`} />
				</g>
				{edge > 0.01 && (
					<g style={{mixBlendMode: 'screen'}}>
						<path d={path} fill="none" stroke={c} strokeWidth={10} opacity={edge * 0.55} filter={`url(#${id}-blur)`} />
						<path d={path} fill="none" stroke="#f3efff" strokeWidth={2.5} opacity={edge * 0.9} strokeDasharray={`${perim * Math.min(1, ease(t, tA, 0.45))} ${perim}`} />
						<path d={path} fill={c} opacity={edge * 0.12} />
					</g>
				)}
				<g style={{mixBlendMode: 'screen'}}>
					{cells.map((k, i) => {
						if (i % 3) return null;
						const tc = tD + k.d * dur;
						const q = (t - tc) / 1.3;
						if (q <= 0 || q >= 1) return null;
						const drift = Math.sin(i * 1.7) * 40;
						return <circle key={i} cx={k.x + cell / 2 + drift * q} cy={k.y + cell / 2 - q * (90 + (i % 5) * 18)} r={2 + (i % 3)} fill={i % 4 ? c : '#f3efff'} opacity={(1 - q) * 0.9} />;
					})}
				</g>
			</svg>
		</AbsoluteFill>
	);
};

type Block = {rect?: [number, number, number, number]; circle?: [number, number, number]; at?: Cue; until?: Cue; label?: string; labelAt?: P; kind?: 'stone' | 'smoke' | 'fog' | 'wall'};
type Label = {text: string; at: P; cue: Cue; until?: Cue; color?: string};

/** Nearest hit distance of ray (o, d) against a segment, a circle, or Infinity. */
const raySeg = (ox: number, oy: number, dx: number, dy: number, ax: number, ay: number, bx: number, by: number) => {
	const ex = bx - ax;
	const ey = by - ay;
	const den = dx * ey - dy * ex;
	if (Math.abs(den) < 1e-9) return Infinity;
	const tt = ((ax - ox) * ey - (ay - oy) * ex) / den;
	const u = ((ax - ox) * dy - (ay - oy) * dx) / den;
	return tt > 0 && u >= 0 && u <= 1 ? tt : Infinity;
};
const rayCircle = (ox: number, oy: number, dx: number, dy: number, cx: number, cy: number, r: number) => {
	const fx = ox - cx;
	const fy = oy - cy;
	const b = fx * dx + fy * dy;
	const cc = fx * fx + fy * fy - r * r;
	const disc = b * b - cc;
	if (disc < 0) return Infinity;
	const tt = -b - Math.sqrt(disc);
	return tt > 0 ? tt : Infinity;
};

/**
 * SightPlan: the weakness as a puzzle, a top-down courtyard plan. `yard: [x0, y0, x1, y1]` is the courtyard (screen px);
 * `eye: [x, y]` is where she watches from (a lilac eye on the wall). Her sight is a cone (`spread` degrees either side,
 * `range` px) that opens at `start` and sweeps `sweep: [fromDeg, toDeg, period]` (0 = right, 90 = down); it is ray-cast
 * against every `blocks` shape each frame, so cover casts true blind spots. Blocks: `{rect: [x0, y0, x1, y1]}` or
 * `{circle: [x, y, r]}`, with `kind` stone / smoke / fog / wall (look), optional `at` (grows in on a cue), `until`
 * (fades and stops blocking: a lantern burns off the fog) and a `label` (small caps, at `labelAt` or centred).
 * `route: [[x, y], ...]` is the heroes' path through the shadows; it draws on at `routeAt` (dotted amber) and three
 * tokens walk it by `moves: [{at, p}]` (p = 0–1 along the route). A token caught in the light turns rust. `labels` pin
 * extra notes (e.g. BLIND SPOT). `liftAt` / `lift: {to: [x, y], s}` and `lessonKicker` / `lessonText` / `lessonTop`
 * work as in `rippleMap`; `arcRow` (strings, last one ember) sets a small row of words above the lesson. `instant`
 * shows every block and the full route from the start (a recap). Overlay (not local).
 */
export const SightPlan: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [X0, Y0, X1, Y1] = g.yard as [number, number, number, number];
	const [ex, ey] = g.eye as P;
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.25;
	const vis = (g.instant || g.instantBoard ? 1 : ease(t, t0, 0.45)) * out(t, tEnd, 0.3);
	const open = g.instant || g.instantBoard ? 1 : ease(t, t0 + 0.25, 0.8, Easing.out(Easing.cubic));
	const sw: number[] = g.sweep ?? [60, 120, 5];
	const mid = (sw[0] + sw[1]) / 2;
	const amp = (sw[1] - sw[0]) / 2;
	const dirDeg = mid + amp * Math.sin(((t - (g.sweepZero ? cueTime(timing, g.sweepZero) : t0)) * 2 * Math.PI) / (sw[2] || 5));
	const spread = (g.spread ?? 30) * open;
	const range = g.range ?? 900;
	const blocks: Block[] = g.blocks ?? [];
	const grow = (b: Block) => {
		const a = g.instant || !b.at ? 1 : ease(t, cueTime(timing, b.at), 0.55, Easing.out(Easing.cubic));
		const u = b.until ? 1 - ease(t, cueTime(timing, b.until), 0.7) : 1;
		return a * u;
	};
	// Ray-cast the cone against the yard walls and the live blocks.
	const live = blocks.map((b) => ({b, k: grow(b)})).filter((x) => x.k > 0.02);
	const N = 220;
	const poly: P[] = [[ex, ey]];
	for (let i = 0; i <= N; i++) {
		const a = ((dirDeg - spread + (2 * spread * i) / N) * Math.PI) / 180;
		const dx = Math.cos(a);
		const dy = Math.sin(a);
		let best = range;
		// Yard walls (the eye sits on the top wall, so skip hits at ~0).
		for (const [ax, ay, bx, by] of [
			[X0, Y0, X1, Y0],
			[X1, Y0, X1, Y1],
			[X1, Y1, X0, Y1],
			[X0, Y1, X0, Y0],
		]) {
			const d = raySeg(ex, ey, dx, dy, ax, ay, bx, by);
			if (d > 2) best = Math.min(best, d);
		}
		for (const {b, k} of live) {
			if (k < 0.5 && b.kind !== 'smoke' && b.kind !== 'fog') continue;
			if (b.rect) {
				const [a0, b0, a1, b1] = b.rect;
				for (const [ax, ay, bx, by] of [
					[a0, b0, a1, b0],
					[a1, b0, a1, b1],
					[a1, b1, a0, b1],
					[a0, b1, a0, b0],
				])
					best = Math.min(best, raySeg(ex, ey, dx, dy, ax, ay, bx, by));
			} else if (b.circle) {
				const [cx, cy, r] = b.circle;
				best = Math.min(best, rayCircle(ex, ey, dx, dy, cx, cy, r * k));
			}
		}
		poly.push([ex + dx * best, ey + dy * best]);
	}
	const polyStr = poly.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
	// Route and tokens.
	const route: P[] = g.route ?? [];
	const segL = route.slice(1).map((p, i) => Math.hypot(p[0] - route[i][0], p[1] - route[i][1]));
	const routeLen = segL.reduce((s, l) => s + l, 0);
	const at = (p: number): P => {
		let d = Math.max(0, Math.min(1, p)) * routeLen;
		for (let i = 0; i < segL.length; i++) {
			if (d <= segL[i] || i === segL.length - 1) {
				const f = segL[i] ? Math.min(1, d / segL[i]) : 0;
				return [lerp(route[i][0], route[i + 1][0], f), lerp(route[i][1], route[i + 1][1], f)];
			}
			d -= segL[i];
		}
		return route[0];
	};
	const partial = (f: number): P[] => {
		const pts: P[] = [route[0]];
		let d = f * routeLen;
		for (let i = 0; i < segL.length && d > 0; i++) {
			const k = Math.min(1, d / (segL[i] || 1));
			pts.push([lerp(route[i][0], route[i + 1][0], k), lerp(route[i][1], route[i + 1][1], k)]);
			d -= segL[i];
		}
		return pts;
	};
	const moves: {at: Cue; p: number}[] = g.moves ?? [];
	let prog = g.instant ? g.instantP ?? 1 : g.p0 ?? 0;
	if (!g.instant) {
		for (const m of moves) {
			const tm = cueTime(timing, m.at);
			const k = ease(t, tm, m.p - prog > 0.3 ? 1.0 : 0.6, Easing.inOut(Easing.cubic));
			prog = lerp(prog, m.p, k);
		}
	}
	const routeOn = g.instant ? 1 : g.routeAt ? ease(t, cueTime(timing, g.routeAt), 0.9, Easing.inOut(Easing.cubic)) : 0;
	const tokensOn = route.length ? (g.instant ? 1 : ease(t, g.tokensAt ? cueTime(timing, g.tokensAt) : t0 + 0.3, 0.4)) : 0;
	// Lift.
	const tLift = g.liftAt ? cueTime(timing, g.liftAt) : Infinity;
	const lift = Number.isFinite(tLift) ? ease(t, tLift, 0.8) : 0;
	const cxm = (X0 + X1) / 2;
	const cym = (Y0 + Y1) / 2;
	const [lx, ly] = g.lift?.to ?? [cxm, cym];
	const ls = lerp(1, g.lift?.s ?? 1, lift);
	const tLesson = g.lessonAt ? cueTime(timing, g.lessonAt) : Infinity;
	const lk = Number.isFinite(tLesson) ? ease(t, tLesson, 0.5) : 0;
	const lessonLines: string[] = Array.isArray(g.lessonText) ? g.lessonText : g.lessonText ? [g.lessonText] : [];
	const arcRow: string[] = g.arcRow ?? [];
	const tArc = g.arcAt ? cueTime(timing, g.arcAt) : tLesson - 0.6;
	const labels: Label[] = g.labels ?? [];
	const gid = `plan-${Math.round(ex)}`;
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', inset: 0, transform: `translate(${(lx - cxm) * lift}px, ${(ly - cym) * lift}px) scale(${ls})`, transformOrigin: `${cxm}px ${cym}px`}}>
				<svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					<defs>
						<radialGradient id={`${gid}-cone`} gradientUnits="userSpaceOnUse" cx={ex} cy={ey} r={range}>
							<stop offset="0%" stopColor="#f3efff" stopOpacity={0.75} />
							<stop offset="25%" stopColor={GAZE} stopOpacity={0.5} />
							<stop offset="100%" stopColor={GAZE} stopOpacity={0.2} />
						</radialGradient>
						<pattern id={`${gid}-grid`} width={40} height={40} patternUnits="userSpaceOnUse" x={X0} y={Y0}>
							<path d="M40 0 L0 0 0 40" fill="none" stroke={palette.fog} strokeOpacity={0.09} strokeWidth={1} />
						</pattern>
						<filter id={`${gid}-soft`} x="-30%" y="-30%" width="160%" height="160%">
							<feGaussianBlur stdDeviation={14} />
						</filter>
						<filter id={`${gid}-edge`} x="-10%" y="-10%" width="120%" height="120%">
							<feGaussianBlur stdDeviation={2.5} />
						</filter>
					</defs>
					{/* The board: flagstones in shadow. */}
					<rect x={X0 - 26} y={Y0 - 26} width={X1 - X0 + 52} height={Y1 - Y0 + 52} rx={10} fill="rgba(5,9,18,0.82)" stroke={palette.amber} strokeOpacity={0.25} strokeWidth={1.5} />
					<rect x={X0} y={Y0} width={X1 - X0} height={Y1 - Y0} fill="#0a1424" />
					<rect x={X0} y={Y0} width={X1 - X0} height={Y1 - Y0} fill={`url(#${gid}-grid)`} />
					{/* Her sight. */}
					{open > 0.01 && (
						<g style={{mixBlendMode: 'screen'}}>
							<polygon points={polyStr} fill={`url(#${gid}-cone)`} filter={`url(#${gid}-edge)`} />
							<polygon points={polyStr} fill="none" stroke={GAZE} strokeOpacity={0.5} strokeWidth={1.5} />
						</g>
					)}
					{/* Walls of the yard, with the gate gap at the bottom. */}
					<path
						d={`M${(X0 + X1) / 2 + 50},${Y1} L${X1},${Y1} L${X1},${Y0} L${X0},${Y0} L${X0},${Y1} L${(X0 + X1) / 2 - 50},${Y1}`}
						fill="none"
						stroke={palette.mist}
						strokeOpacity={0.75}
						strokeWidth={10}
						strokeLinejoin="round"
					/>
					{/* Cover. */}
					{blocks.map((b, i) => {
						const k = grow(b);
						if (k <= 0.01) return null;
						const kind = b.kind ?? 'stone';
						if (kind === 'smoke' || kind === 'fog') {
							const [cx, cy, r] = b.circle ?? [0, 0, 0];
							const puffs = kind === 'smoke' ? 7 : 9;
							return (
								<g key={i} opacity={Math.min(1, k * 1.2)}>
									{Array.from({length: puffs}, (_, j) => {
										const a = (j / puffs) * Math.PI * 2 + t * (kind === 'smoke' ? 0.25 : 0.1);
										const rr = r * k * (kind === 'smoke' ? 0.55 : 0.6);
										return <circle key={j} cx={cx + Math.cos(a) * rr * 0.6} cy={cy + Math.sin(a) * rr * (kind === 'fog' ? 0.45 : 0.6)} r={rr} fill={kind === 'smoke' ? '#6f7c86' : '#a9b8c0'} opacity={kind === 'smoke' ? 0.55 : 0.4} filter={`url(#${gid}-soft)`} />;
									})}
									<circle cx={cx} cy={cy} r={r * k * 0.8} fill={kind === 'smoke' ? '#7d8a93' : '#b8c6cc'} opacity={0.5} filter={`url(#${gid}-soft)`} />
								</g>
							);
						}
						if (b.rect) {
							const [a0, b0, a1, b1] = b.rect;
							const h = (b1 - b0) * k;
							return <rect key={i} x={a0} y={b1 - h} width={a1 - a0} height={h} fill={kind === 'wall' ? '#3a4650' : '#2a3540'} stroke={palette.fog} strokeOpacity={0.8} strokeWidth={2.5} rx={3} />;
						}
						if (b.circle) {
							const [cx, cy, r] = b.circle;
							return (
								<g key={i}>
									<circle cx={cx} cy={cy} r={r * k} fill="#2a3540" stroke={palette.fog} strokeOpacity={0.8} strokeWidth={2.5} />
									<circle cx={cx} cy={cy} r={r * k * 0.55} fill="#070d16" stroke={palette.fog} strokeOpacity={0.5} strokeWidth={1.5} />
								</g>
							);
						}
						return null;
					})}
					{/* The heroes' route through the shadows. */}
					{route.length > 1 && routeOn > 0 && (
						<polyline points={partial(routeOn).map((p) => p.join(',')).join(' ')} fill="none" stroke={palette.amber} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" strokeDasharray="2 14" opacity={0.95} />
					)}
					{route.length > 1 && (
						<g opacity={routeOn}>
							<circle cx={route[route.length - 1][0]} cy={route[route.length - 1][1]} r={16} fill="none" stroke={palette.ember} strokeWidth={3} />
							<circle cx={route[route.length - 1][0]} cy={route[route.length - 1][1]} r={5} fill={palette.ember} />
						</g>
					)}
					{tokensOn > 0 &&
						[0, -0.035, -0.07].map((o, k) => {
							const [x, y] = at(prog + o);
							const lit = !!g.catch && inPoly(x, y, poly) && open > 0.5;
							const col = lit ? palette.rust : palette.amber;
							return (
								<g key={k} opacity={tokensOn}>
									<circle cx={x} cy={y} r={15} fill="#0b1216" stroke={col} strokeWidth={4} style={{filter: `drop-shadow(0 0 8px ${col})`}} />
									<circle cx={x} cy={y} r={5} fill={col} />
								</g>
							);
						})}
					{/* The eye on the wall. */}
					<g opacity={0.6 + 0.4 * open}>
						<circle cx={ex} cy={ey} r={30} fill="#0b1216" stroke={GAZE} strokeWidth={3} style={{filter: `drop-shadow(0 0 12px ${GAZE})`}} />
						<path d={`M${ex - 18},${ey} Q${ex},${ey - 13} ${ex + 18},${ey} Q${ex},${ey + 13} ${ex - 18},${ey} Z`} fill="none" stroke={GAZE} strokeWidth={2.5} />
						<circle cx={ex} cy={ey} r={5.5} fill="#f3efff" />
					</g>
				</svg>
				{/* Labels on cover and pockets. */}
				{blocks.map((b, i) => {
					if (!b.label) return null;
					const k = grow(b);
					const lo = g.instant ? 1 : b.at ? ease(t, cueTime(timing, b.at) + 0.2, 0.4) * (b.until ? 1 - ease(t, cueTime(timing, b.until), 0.4) : 1) : k;
					const [px, py] = b.labelAt ?? (b.circle ? [b.circle[0], b.circle[1]] : b.rect ? [(b.rect[0] + b.rect[2]) / 2, (b.rect[1] + b.rect[3]) / 2] : [0, 0]);
					return (
						<div key={`l${i}`} style={{position: 'absolute', left: px, top: py, transform: 'translate(-50%, -50%)', ...kicker, fontSize: 26, color: palette.parchment, opacity: lo, textShadow: '0 2px 10px rgba(0,0,0,1), 0 0 3px rgba(0,0,0,1)', whiteSpace: 'nowrap'}}>
							{b.label}
						</div>
					);
				})}
				{labels.map((lb, i) => {
					const tl = g.instant ? -1e9 : cueTime(timing, lb.cue);
					const o = ease(t, tl, 0.4) * (lb.until ? 1 - ease(t, cueTime(timing, lb.until), 0.3) : 1);
					if (o <= 0) return null;
					return (
						<div key={`x${i}`} style={{position: 'absolute', left: lb.at[0], top: lb.at[1], transform: `translate(-50%, -50%) translateY(${(1 - o) * 8}px)`, ...kicker, fontSize: 24, color: tone(lb.color, palette.amber), border: `1.5px dashed ${tone(lb.color, palette.amber)}`, padding: '6px 12px 4px', background: 'rgba(5,9,18,0.8)', opacity: o, whiteSpace: 'nowrap'}}>
							{lb.text}
						</div>
					);
				})}
			</div>
			{arcRow.length > 0 && (
				<div style={{position: 'absolute', top: g.arcTop ?? 860, left: 40, right: 40, textAlign: 'center', ...kicker, fontSize: 24, letterSpacing: '0.16em', whiteSpace: 'nowrap'}}>
					{arcRow.map((w, i) => {
						const last = i === arcRow.length - 1;
						const o = g.instant ? 1 : ease(t, tArc + i * 0.12, 0.35);
						return (
							<span key={i} style={{opacity: o, color: last ? palette.ember : palette.fog, textShadow: '0 2px 10px rgba(0,0,0,0.9)'}}>
								{w}
								{!last && <span style={{color: palette.fog, opacity: 0.5}}>{'  ·  '}</span>}
							</span>
						);
					})}
				</div>
			)}
			{lessonLines.length > 0 && (
				<div style={{position: 'absolute', top: g.lessonTop ?? 920, left: 60, right: 60, textAlign: 'center', opacity: lk, transform: `translateY(${(1 - lk) * 16}px)`}}>
					{g.lessonKicker && <div style={{...kicker, fontSize: 30, color: palette.amber, textShadow: '0 2px 12px rgba(0,0,0,0.9)'}}>{g.lessonKicker}</div>}
					{lessonLines.map((ln, li) => {
						const lp = ease(t, tLesson + 0.15 + li * 0.25, 0.6);
						return (
							<div key={li} style={{marginTop: li ? 0 : 14, fontFamily: fonts.display, fontWeight: 600, fontSize: g.lessonSize ?? 92, lineHeight: 1.04, color: palette.parchment, opacity: lp, textShadow: '0 4px 30px rgba(0,0,0,0.8)'}}>
								{ln.split(' ').map((w, k) => (
									<span key={k} style={w.startsWith('*') ? {color: palette.ember, fontStyle: 'italic'} : undefined}>
										{w.replace(/\*/g, '')}{' '}
									</span>
								))}
							</div>
						);
					})}
				</div>
			)}
		</AbsoluteFill>
	);
};

export const SIGHTLINE: Record<string, React.FC<GraphicProps>> = {
	gazeBeam: GazeBeam,
	unmake: Unmake,
	sightPlan: SightPlan,
};
