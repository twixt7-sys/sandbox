import React, {createContext, useContext, useId} from 'react';
import {AbsoluteFill, Easing, interpolate, staticFile} from 'remotion';
import {rng} from '../lib/random';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import {arcPoint, CrownGlyph, GranaryGlyph} from '../graphics/Power';
import type {Cue} from '../types';
import type {SceneProps} from './registry';

/*
 * Data-driven fantasy map (EP06 onward; EP07 cities, EP10 chokepoints can reuse it).
 * The episode defines the map once in `episode.json → atlas.features`; each `atlas` shot lists which
 * features it shows and when they draw on (`shot.atlas.show`), so the same map can build up across shots.
 *
 * Feature kinds (all coordinates in 1080×1920 frame px):
 *   range   {pts, gaps?: [[x0,x1]], rows?, scale?, seed?}   hachured mountain glyphs along a spine (draws west→east)
 *   river   {pts, width?}                                    smooth river (draws from source)
 *   region  {d, color, opacity?}                             tinted territory
 *   fields  {box: [x0,y0,x1,y1], count?, seed?, avoid?: [[x,y,r]]} farm plots
 *   town    {at, size?, capital?, palace?}                   settlement glyph (`palace`: domed palace instead of houses)
 *   route   {pts, color?, dash?, flow?, width?}              road; `flow` sends caravan dots toward the end
 *   arrow   {pts, color?, stop?}                             movement arrow; `stop` ends it in a barred halt + snow
 *   cut     {at, size?}                                      rust ✕ (a link that never forms, a crossing shut)
 *   pattern {at, kind: wave|zig|dots, color?, w?}            culture marker (an accent, a weave)
 *   gate    {at}                                             small tower on a road
 *   coin    {at}                                             toll coin
 *   wash    {at, r, color?}                                  expanding influence
 *   label   {at, text, size?, color?, serif?, anchor?, rot?} map lettering
 *   key     {at, rows: [{text, symbol: arrow|cut|coin, color?, at: Cue}]} map legend; each row lights on its cue
 *   dunes   {box: [x0,y0,x1,y1], count?, seed?, avoid?}      desert crescents (EP08)
 *   well    {at, size?, color?}                              oasis well (water-blue ring + core; pulses)
 *   lock    {at, size?}                                      padlock snapping shut (put it beside a well)
 *   gorge   {pts, width?, seed?}                             chasm with cliff hachures on both rims (draws west→east; EP10)
 *   bridge  {at, len?, angle?}                               single stone span across a gorge or river (EP10's chokepoint)
 *   granary {at, size?}                                      storehouse between two silos, ringed like a town; pulses (EP16)
 *   crown   {at, from?, size?, ghost?}                       crown glyph; with `from` it flies along an arc from there to `at`
 *                                                            as it draws and glows on landing; `ghost` = dashed outline (EP16:
 *                                                            the title stays on the palace, the power moves to the guild)
 * Show entries: "id" (already there) or {id, at: Cue, dur?, until?: Cue, pulse?: Cue}.
 * Shot zoom: {from, to, origin?, at?: Cue, dur?}; with `at` the move runs on that cue, otherwise it eases over the whole shot.
 */

type Pt = [number, number];
export type AtlasFeature = {id: string; kind: string; [k: string]: any};
export const AtlasContext = createContext<{features: AtlasFeature[]} | undefined>(undefined);

type ShowEntry = string | {id: string; at?: Cue; dur?: number; until?: Cue; pulse?: Cue};

/** Catmull-Rom through points -> cubic Bézier path. */
export const smoothPath = (pts: Pt[]) => {
	let d = `M${pts[0][0]},${pts[0][1]}`;
	for (let i = 0; i < pts.length - 1; i++) {
		const p0 = pts[Math.max(0, i - 1)];
		const [p1, p2] = [pts[i], pts[i + 1]];
		const p3 = pts[Math.min(pts.length - 1, i + 2)];
		const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
		const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
		d += ` C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0]},${p2[1]}`;
	}
	return d;
};

/** Point and direction at fraction u (0..1, by length) along a polyline. */
const along = (pts: Pt[], u: number): {p: Pt; a: number} => {
	const segs = pts.slice(1).map((b, i) => Math.hypot(b[0] - pts[i][0], b[1] - pts[i][1]));
	let rest = Math.max(0, Math.min(1, u)) * segs.reduce((s, x) => s + x, 0);
	for (let i = 0; i < segs.length; i++) {
		if (rest <= segs[i] || i === segs.length - 1) {
			const k = segs[i] ? Math.min(1, rest / segs[i]) : 0;
			const [a, b] = [pts[i], pts[i + 1]];
			return {p: [lerp(a[0], b[0], k), lerp(a[1], b[1], k)], a: Math.atan2(b[1] - a[1], b[0] - a[0])};
		}
		rest -= segs[i];
	}
	return {p: pts[pts.length - 1], a: 0};
};

const yOnSpine = (pts: Pt[], x: number) => {
	const i = pts.findIndex((p) => p[0] >= x);
	if (i <= 0) return pts[i === 0 ? 0 : pts.length - 1][1];
	const [a, b] = [pts[i - 1], pts[i]];
	return lerp(a[1], b[1], (x - a[0]) / (b[0] - a[0]));
};

const xOnSpine = (pts: Pt[], y: number) => {
	const i = pts.findIndex((p, k) => k > 0 && (p[1] - y) * (pts[k - 1][1] - y) <= 0);
	if (i <= 0) return pts[0][0];
	const [a, b] = [pts[i - 1], pts[i]];
	return lerp(a[0], b[0], (y - a[1]) / (b[1] - a[1] || 1));
};

type Peak = {x: number; y: number; h: number; w: number; order: number};

/** Mountain glyphs scattered in rows along a spine; horizontal spines run west→east, vertical ones (spurs) south→north. */
const peaksFor = (f: AtlasFeature): Peak[] => {
	const pts: Pt[] = f.pts;
	const r = rng(f.seed ?? 7);
	const s = f.scale ?? 1;
	const rows = f.rows ?? 3;
	const vertical = Math.abs(pts[pts.length - 1][1] - pts[0][1]) > Math.abs(pts[pts.length - 1][0] - pts[0][0]);
	const out: Peak[] = [];
	const step = 34 * s * (vertical ? 1.4 : 1);
	const [lo, hi] = vertical ? [Math.min(...pts.map((p) => p[1])), Math.max(...pts.map((p) => p[1]))] : [pts[0][0], pts[pts.length - 1][0]];
	for (let row = 0; row < rows; row++) {
		const off = (row - (rows - 1) / 2) * 30 * s;
		for (let v = lo + (row % 2) * step * 0.5; v <= hi; v += step * (0.85 + r() * 0.35)) {
			const x = vertical ? xOnSpine(pts, v) + off + (r() - 0.5) * 18 : v + (r() - 0.5) * 12;
			const y = vertical ? v : yOnSpine(pts, v) + off + (r() - 0.5) * 8;
			if ((f.gaps ?? []).some(([a, b]: [number, number]) => x > a && x < b)) continue;
			const mid = 1 - Math.abs(row - (rows - 1) / 2) / Math.max(1, rows / 2);
			const h = (30 + r() * 26 + 14 * mid) * s;
			out.push({x, y, h, w: h * (1.05 + r() * 0.35), order: vertical ? (hi - v) / (hi - lo) : (v - lo) / (hi - lo)});
		}
	}
	return out.sort((a, b) => a.y - b.y);
};

const Mountain: React.FC<{k: Peak; p: number}> = ({k, p}) => {
	const q = Math.max(0, Math.min(1, (p - k.order * 0.75) / 0.25));
	if (q <= 0) return null;
	const {x, y, w} = k;
	const h = k.h * (0.6 + 0.4 * q);
	const top: Pt = [x + w * 0.04, y - h];
	const left = `M${x - w / 2},${y} L${top[0]},${top[1]} L${x + w / 2},${y} Z`;
	const shade = `M${x - w / 2},${y} L${top[0]},${top[1]} L${x + w * 0.02},${y} Z`;
	const cap = `M${top[0] - w * 0.13},${top[1] + h * 0.26} L${top[0]},${top[1]} L${top[0] + w * 0.15},${top[1] + h * 0.28} L${top[0] + w * 0.03},${top[1] + h * 0.2} Z`;
	return (
		<g opacity={q}>
			<path d={left} fill="#1b262c" />
			<path d={shade} fill="#0f171b" />
			{Array.from({length: 4}, (_, i) => {
				const u = 0.25 + i * 0.17;
				return <line key={i} x1={lerp(top[0], x - w / 2, u)} y1={lerp(top[1], y, u)} x2={lerp(top[0], x - w / 2, u) + w * 0.12} y2={lerp(top[1], y, u) + h * 0.05} stroke={palette.parchment} strokeOpacity={0.22} strokeWidth={1.2} />;
			})}
			<path d={cap} fill="#e6eef0" opacity={0.85} />
			<path d={`M${x - w / 2},${y} L${top[0]},${top[1]} L${x + w / 2},${y}`} fill="none" stroke={palette.parchment} strokeOpacity={0.75} strokeWidth={1.8} strokeLinejoin="round" />
		</g>
	);
};

/** Domed palace silhouette (EP10's capital): a terrace and three domes with spires. */
const Palace: React.FC = () => (
	<g fill={palette.parchment}>
		<rect x={-26} y={2} width={52} height={14} opacity={0.88} />
		<rect x={-18} y={-8} width={36} height={12} opacity={0.88} />
		{[[-13, -8, 7], [0, -10, 10], [13, -8, 7]].map(([x, y, r], i) => (
			<g key={i}>
				<path d={`M${x - r},${y} A${r},${r} 0 0 1 ${x + r},${y} Z`} fill={palette.amber} />
				<line x1={x} y1={y - r} x2={x} y2={y - r - 6} stroke={palette.amber} strokeWidth={1.6} />
			</g>
		))}
		{[-22, 22].map((x) => (
			<rect key={x} x={x - 2} y={-16} width={4} height={20} opacity={0.88} />
		))}
	</g>
);

const Town: React.FC<{at: Pt; size?: number; capital?: boolean; palace?: boolean}> = ({at, size = 1, capital, palace}) => (
	<g transform={`translate(${at[0]} ${at[1]}) scale(${size})`} fill={palette.parchment}>
		{palace && <Palace />}
		{!palace && [
			[-16, -4, 12], [0, -12, 16], [16, -2, 11], [-4, 9, 11], [11, 10, 9],
		].map(([dx, dy, s], i) => (
			<rect key={i} x={dx - s / 2} y={dy - s / 2} width={s} height={s} opacity={0.88} />
		))}
		{capital && <circle r={36} fill="none" stroke={palette.ember} strokeWidth={2} />}
		<circle r={capital ? 46 : 40} fill="none" stroke={palette.parchment} strokeOpacity={0.35} strokeWidth={1.5} strokeDasharray="3 6" />
	</g>
);

const Coin: React.FC<{s?: number}> = ({s = 1}) => (
	<g transform={`scale(${s})`}>
		<circle r={22} fill={palette.amber} />
		<circle r={16} fill="none" stroke="#7a5418" strokeWidth={2.5} />
		<rect x={-4} y={-9} width={8} height={18} fill="#7a5418" opacity={0.75} />
	</g>
);

const Gate: React.FC = () => (
	<g fill="#1b2328" stroke={palette.amber} strokeWidth={2.4}>
		<rect x={-11} y={-30} width={22} height={30} />
		<path d="M-14,-30 L-14,-38 L-8,-38 L-8,-33 L-3,-33 L-3,-38 L3,-38 L3,-33 L8,-33 L8,-38 L14,-38 L14,-30 Z" />
	</g>
);

const Arrowhead: React.FC<{p: Pt; a: number; c: string}> = ({p, a, c}) => (
	<path d="M-16,-11 L4,0 L-16,11" transform={`translate(${p[0]} ${p[1]}) rotate(${(a * 180) / Math.PI})`} fill="none" stroke={c} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" />
);

const KeySymbol: React.FC<{kind: string; c: string}> = ({kind, c}) => {
	if (kind === 'coin') return <Coin s={0.62} />;
	if (kind === 'cut')
		return (
			<g stroke={c} strokeWidth={5} strokeLinecap="round">
				<line x1={-10} y1={-10} x2={10} y2={10} />
				<line x1={10} y1={-10} x2={-10} y2={10} />
			</g>
		);
	return (
		<g stroke={c} strokeWidth={4.5} strokeLinecap="round" fill="none">
			<line x1={-22} y1={0} x2={8} y2={0} />
			<line x1={16} y1={-12} x2={16} y2={12} />
		</g>
	);
};

const pathLen1 = (p: number) => ({pathLength: 1, strokeDasharray: '1 1', strokeDashoffset: 1 - p});

/** A path that draws on from its start (dashed paths are revealed through a solid mask so the dash pattern holds). */
const DrawnPath: React.FC<{d: string; p: number; stroke: string; width: number; dash?: string}> = ({d, p, stroke, width, dash}) => {
	const id = useId().replace(/:/g, '');
	if (!dash) return <path d={d} fill="none" stroke={stroke} strokeWidth={width} strokeLinecap="round" opacity={0.92} {...pathLen1(p)} />;
	return (
		<g>
			<defs>
				<mask id={id} maskUnits="userSpaceOnUse" x={0} y={0} width={W} height={H}>
					<path d={d} fill="none" stroke="#fff" strokeWidth={width + 16} pathLength={1} strokeDasharray={`${p} 1`} />
				</mask>
			</defs>
			<path d={d} fill="none" stroke={stroke} strokeWidth={width} strokeLinecap="round" strokeDasharray={dash} opacity={0.92} mask={`url(#${id})`} />
		</g>
	);
};

const FLAKES = (() => {
	const r = rng(66);
	return Array.from({length: 7}, () => [(r() - 0.5) * 70, (r() - 0.5) * 40, 2 + r() * 2.5]);
})();

/** One feature at draw-progress p (0..1), with pulse (0..1) and the absolute time for looping motion. */
const Feature: React.FC<{f: AtlasFeature; p: number; pulse: number; t: number; t0: number}> = ({f, p, pulse, t, t0}) => {
	const c = f.color ?? palette.amber;
	switch (f.kind) {
		case 'range': {
			const peaks = peaksFor(f);
			return (
				<g>
					{peaks.map((k, i) => (
						<Mountain key={i} k={k} p={p} />
					))}
				</g>
			);
		}
		case 'river': {
			const d = smoothPath(f.pts);
			return (
				<g>
					<path d={d} fill="none" stroke="#284652" strokeWidth={f.width ?? 22} strokeLinecap="round" {...pathLen1(p)} />
					<path d={d} fill="none" stroke={palette.fog} strokeOpacity={0.7} strokeWidth={2.5} {...pathLen1(p)} />
				</g>
			);
		}
		case 'region':
			return <path d={f.d} fill={c} opacity={(f.opacity ?? 0.16) * p * (1 + pulse * 0.8)} />;
		case 'fields': {
			const r = rng(f.seed ?? 11);
			const [x0, y0, x1, y1] = f.box;
			const plots = Array.from({length: f.count ?? 40}, () => ({x: lerp(x0, x1, r()), y: lerp(y0, y1, r()), w: 22 + r() * 26, h: 14 + r() * 14, a: (r() - 0.5) * 24, k: r()}));
			const avoid: [number, number, number][] = f.avoid ?? [];
			return (
				<g>
					{plots
						.filter((q) => !avoid.some(([ax, ay, ar]) => Math.hypot(q.x - ax, q.y - ay) < ar))
						.map((q, i) => {
							const o = Math.max(0, Math.min(1, (p - q.k * 0.6) / 0.4));
							return (
								<g key={i} transform={`translate(${q.x} ${q.y}) rotate(${q.a})`} opacity={o * (0.55 + 0.45 * pulse)}>
									<rect x={-q.w / 2} y={-q.h / 2} width={q.w} height={q.h} fill={palette.amber} fillOpacity={0.12} stroke={palette.ember} strokeOpacity={0.45} strokeWidth={1.2} />
									<line x1={-q.w / 2 + 4} y1={0} x2={q.w / 2 - 4} y2={0} stroke={palette.ember} strokeOpacity={0.35} strokeWidth={1} />
								</g>
							);
						})}
				</g>
			);
		}
		case 'town':
			return (
				<g opacity={p}>
					<Town at={f.at} size={f.size} capital={f.capital} palace={f.palace} />
				</g>
			);
		case 'route': {
			const d = smoothPath(f.pts);
			const dots = f.flow && p >= 1 ? [0, 1, 2, 3] : [];
			return (
				<g>
					<DrawnPath d={d} p={p} stroke={c} width={(f.width ?? 4) + 2 * pulse} dash={f.dash} />
					{dots.map((k) => {
						const u = ((((t - t0) * 0.22 + k / 4) % 1) + 1) % 1;
						const {p: q} = along(f.pts, u);
						return <circle key={k} cx={q[0]} cy={q[1]} r={7} fill={palette.ember} opacity={Math.min(1, u * 8, (1 - u) * 8)} style={{filter: `drop-shadow(0 0 6px ${palette.amber})`}} />;
					})}
				</g>
			);
		}
		case 'arrow': {
			const pts: Pt[] = f.pts;
			const end = along(pts, p);
			const stop = f.stop ? ease(p, 0.92, 0.08) : 0;
			const last = pts[pts.length - 1];
			const a = along(pts, 0.999).a;
			return (
				<g opacity={0.95}>
					<DrawnPath d={smoothPath(pts)} p={p} stroke={c} width={5 + 2 * pulse} dash="14 10" />
					{p > 0 && !f.stop && <Arrowhead p={end.p} a={end.a} c={c} />}
					{p > 0 && f.stop && stop < 0.5 && <Arrowhead p={end.p} a={end.a} c={c} />}
					{f.stop && (
						<g opacity={stop} transform={`translate(${last[0]} ${last[1]}) rotate(${(a * 180) / Math.PI + 90})`}>
							<line x1={-24} y1={0} x2={24} y2={0} stroke={c} strokeWidth={6 + 2 * pulse} strokeLinecap="round" />
						</g>
					)}
					{f.stop &&
						FLAKES.map(([dx, dy, s], i) => (
							<circle key={i} cx={last[0] + dx} cy={last[1] + dy + 6 + (((t * 22 + i * 13) % 30) - 15)} r={s} fill="#e6eef0" opacity={stop * 0.8} />
						))}
				</g>
			);
		}
		case 'cut': {
			const s = interpolate(p, [0, 0.6, 1], [0.4, 1.2, 1]);
			return (
				<g transform={`translate(${f.at[0]} ${f.at[1]}) scale(${s * (1 + 0.25 * pulse) * (f.size ?? 1)})`} opacity={Math.min(1, p * 3)} stroke={palette.rust} strokeWidth={6} strokeLinecap="round" style={{filter: 'drop-shadow(0 0 6px rgba(0,0,0,0.9))'}}>
					<line x1={-14} y1={-14} x2={14} y2={14} />
					<line x1={14} y1={-14} x2={-14} y2={14} />
				</g>
			);
		}
		case 'pattern': {
			const [x, y] = f.at;
			const w = f.w ?? 150;
			const ph = (t - t0) * 50;
			const pts =
				f.pattern === 'zig'
					? Array.from({length: 14}, (_, i) => `${i ? 'L' : 'M'}${x - w / 2 + (i * w) / 13},${y + ((i + Math.floor(ph / 10)) % 2 ? -9 : 9)}`)
					: f.pattern === 'dots'
						? []
						: Array.from({length: 32}, (_, i) => `${i ? 'L' : 'M'}${x - w / 2 + (i * w) / 31},${y + Math.sin((i * w) / 31 / 12 + ph / 14) * 9}`);
			return (
				<g opacity={p * (0.85 + 0.15 * pulse)}>
					{f.pattern === 'dots' ? (
						Array.from({length: 7}, (_, i) => <circle key={i} cx={x - w / 2 + (i * w) / 6} cy={y} r={4 + 2.5 * Math.max(0, Math.sin(ph / 12 - i * 0.9))} fill={c} />)
					) : (
						<path d={pts.join(' ')} fill="none" stroke={c} strokeWidth={3} strokeLinejoin="miter" />
					)}
				</g>
			);
		}
		case 'gate':
			return (
				<g opacity={p} transform={`translate(${f.at[0]} ${f.at[1]})`}>
					<Gate />
				</g>
			);
		case 'coin': {
			const s = interpolate(p, [0, 0.6, 1], [0.3, 1.15, 1]) * (1 + 0.2 * pulse);
			const bob = Math.sin((t - t0) * 2.2) * 3;
			return (
				<g opacity={Math.min(1, p * 2.5)} transform={`translate(${f.at[0]} ${f.at[1] + bob})`}>
					<Coin s={s} />
				</g>
			);
		}
		case 'wash': {
			const id = `wash-${f.id}`;
			return (
				<g>
					<defs>
						<radialGradient id={id}>
							<stop offset="0%" stopColor={c} stopOpacity={0.34} />
							<stop offset="65%" stopColor={c} stopOpacity={0.12} />
							<stop offset="100%" stopColor={c} stopOpacity={0} />
						</radialGradient>
					</defs>
					<circle cx={f.at[0]} cy={f.at[1]} r={40 + (f.r - 40) * p} fill={`url(#${id})`} opacity={Math.min(1, p * 2)} />
					{[0, 1, 2].map((k) => {
						const q = Math.max(0, Math.min(1, p * 1.3 - k * 0.15));
						return <circle key={k} cx={f.at[0]} cy={f.at[1]} r={60 + (f.r * 0.85 - 60) * q} fill="none" stroke={c} strokeOpacity={0.4 * q * (1 - k * 0.25) * (1 - 0.6 * q)} strokeWidth={1.6} />;
					})}
				</g>
			);
		}
		case 'gorge': {
			const pts: Pt[] = f.pts;
			const d = smoothPath(pts);
			const w = f.width ?? 40;
			const r = rng(f.seed ?? 31);
			const ticks = Array.from({length: 90}, (_, i) => ({u: (i + r() * 0.6) / 90, side: i % 2 ? 1 : -1, len: 8 + r() * 12}));
			return (
				<g>
					<path d={d} fill="none" stroke={palette.parchment} strokeOpacity={0.55} strokeWidth={w + 7} strokeLinecap="round" {...pathLen1(p)} />
					<path d={d} fill="none" stroke="#070b0e" strokeWidth={w} strokeLinecap="round" {...pathLen1(p)} />
					<g opacity={0.3}>
						<DrawnPath d={d} p={p} stroke={palette.fog} width={2} dash="10 14" />
					</g>
					{ticks
						.filter((k) => k.u < p)
						.map((k, i) => {
							const {p: q, a} = along(pts, k.u);
							const nx = -Math.sin(a) * k.side;
							const ny = Math.cos(a) * k.side;
							const x0 = q[0] + nx * (w / 2 + 3);
							const y0 = q[1] + ny * (w / 2 + 3);
							return <line key={i} x1={x0} y1={y0} x2={x0 + nx * k.len} y2={y0 + ny * k.len} stroke={palette.parchment} strokeOpacity={0.4} strokeWidth={1.4} />;
						})}
				</g>
			);
		}
		case 'bridge': {
			const len = f.len ?? 70;
			const s = interpolate(p, [0, 0.6, 1], [0.3, 1.15, 1]);
			return (
				<g opacity={Math.min(1, p * 2.5)} transform={`translate(${f.at[0]} ${f.at[1]}) rotate(${f.angle ?? 0}) scale(${s})`}>
					<circle r={len * 0.75} fill="none" stroke={palette.ember} strokeOpacity={0.55 * pulse} strokeWidth={3} />
					<rect x={-9} y={-len / 2} width={18} height={len} fill="#2a2420" stroke={palette.ember} strokeWidth={2.5 + 2 * pulse} style={{filter: `drop-shadow(0 0 ${4 + 10 * pulse}px ${palette.amber})`}} />
					{[-1, 1].map((e) => (
						<g key={e}>
							<line x1={-14} y1={(e * len) / 2} x2={14} y2={(e * len) / 2} stroke={palette.ember} strokeWidth={4} strokeLinecap="round" />
							<line x1={-9} y1={(e * len) / 2 - e * 4} x2={9} y2={(e * len) / 2 - e * 4} stroke={palette.ember} strokeOpacity={0.5} strokeWidth={1.5} />
						</g>
					))}
					{[-0.18, 0.18].map((u) => (
						<line key={u} x1={-5} y1={u * len} x2={5} y2={u * len} stroke={palette.ember} strokeOpacity={0.6} strokeWidth={1.5} />
					))}
				</g>
			);
		}
		case 'label': {
			const [x, y] = f.at;
			return (
				<text
					x={x}
					y={y + (1 - p) * 10}
					textAnchor={f.anchor ?? 'middle'}
					fill={f.color ?? palette.parchment}
					opacity={p}
					transform={f.rot ? `rotate(${f.rot} ${x} ${y})` : undefined}
					style={
						f.serif
							? {fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: f.size ?? 56, letterSpacing: '0.02em', filter: 'drop-shadow(0 2px 10px rgba(0,0,0,0.8))'}
							: {fontFamily: fonts.ui, fontWeight: 700, fontSize: f.size ?? 28, letterSpacing: '0.2em', textTransform: 'uppercase', filter: 'drop-shadow(0 2px 8px rgba(0,0,0,0.8))'}
					}
				>
					{f.text}
				</text>
			);
		}
		case 'dunes': {
			const r = rng(f.seed ?? 31);
			const [x0, y0, x1, y1] = f.box;
			const ds = Array.from({length: f.count ?? 60}, () => ({x: lerp(x0, x1, r()), y: lerp(y0, y1, r()), w: 26 + r() * 34, k: r()}));
			const avoid: [number, number, number][] = f.avoid ?? [];
			return (
				<g fill="none" strokeLinecap="round">
					{ds
						.filter((q) => !avoid.some(([ax, ay, ar]) => Math.hypot(q.x - ax, q.y - ay) < ar))
						.map((q, i) => {
							const o = Math.max(0, Math.min(1, (p - q.k * 0.6) / 0.4));
							const h = q.w * 0.42;
							return (
								<g key={i} opacity={o}>
									<path d={`M${q.x - q.w},${q.y} Q${q.x - q.w * 0.2},${q.y - h} ${q.x + q.w * 0.15},${q.y - h * 0.9} Q${q.x + q.w * 0.5},${q.y - h * 0.5} ${q.x + q.w},${q.y}`} stroke={palette.ember} strokeOpacity={0.3} strokeWidth={1.6} />
									<path d={`M${q.x + q.w * 0.15},${q.y - h * 0.9} Q${q.x + q.w * 0.1},${q.y - h * 0.3} ${q.x + q.w * 0.35},${q.y}`} stroke={palette.ember} strokeOpacity={0.18} strokeWidth={1.2} />
								</g>
							);
						})}
				</g>
			);
		}
		case 'well': {
			// Oasis well: a water-blue ring with a bright core; pulses when its cue hits.
			const wc = f.color ?? '#7fd3ec';
			const s = interpolate(p, [0, 0.6, 1], [0.3, 1.15, 1]) * (f.size ?? 1) * (1 + 0.25 * pulse);
			return (
				<g opacity={Math.min(1, p * 2.5)} transform={`translate(${f.at[0]} ${f.at[1]}) scale(${s})`}>
					<circle r={26} fill={wc} opacity={0.14 + 0.06 * Math.sin((t - t0) * 2.4)} />
					<circle r={15} fill="#0f2a33" stroke={wc} strokeWidth={3.5} />
					<circle r={6} fill={wc} style={{filter: `drop-shadow(0 0 6px ${wc})`}} />
				</g>
			);
		}
		case 'lock': {
			// Padlock snapping onto a well (amber body, shackle closes as it lands).
			const s = interpolate(p, [0, 0.5, 1], [0.4, 1.2, 1]) * (1 + 0.2 * pulse);
			const shut = interpolate(p, [0.4, 1], [10, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
			return (
				<g opacity={Math.min(1, p * 3)} transform={`translate(${f.at[0]} ${f.at[1]}) scale(${s * (f.size ?? 1)})`}>
					<path d={`M-9,${-4 - shut} L-9,${-14 - shut} A9,9 0 0 1 9,${-14 - shut} L9,-4`} fill="none" stroke={palette.parchment} strokeWidth={4} strokeLinecap="round" />
					<rect x={-14} y={-6} width={28} height={22} rx={4} fill={palette.amber} stroke="#7a5418" strokeWidth={2} />
					<circle cx={0} cy={4} r={3} fill="#5c3d10" />
				</g>
			);
		}
		case 'granary': {
			const s = interpolate(p, [0, 0.6, 1], [0.3, 1.15, 1]) * (f.size ?? 1);
			return (
				<g opacity={Math.min(1, p * 2.5)} transform={`translate(${f.at[0]} ${f.at[1]}) scale(${s})`}>
					<circle r={58 + 10 * pulse} fill="none" stroke={palette.ember} strokeOpacity={0.15 + 0.6 * pulse} strokeWidth={2.5} />
					<circle r={50} fill="none" stroke={palette.parchment} strokeOpacity={0.35} strokeWidth={1.5} strokeDasharray="3 6" />
					<GranaryGlyph />
				</g>
			);
		}
		case 'crown': {
			const s = f.size ?? 0.6;
			if (f.from) {
				const u = Easing.inOut(Easing.cubic)(p);
				const [x, y] = arcPoint(f.from, f.at, u, f.lift ?? 0.3);
				const glow = ease(p, 0.85, 0.15) * (0.7 + 0.3 * Math.sin((t - t0) * 3)) + pulse;
				return (
					<g transform={`translate(${x} ${y}) scale(${1 + 0.15 * Math.sin(u * Math.PI)})`}>
						<CrownGlyph s={s} glow={Math.min(1, glow)} />
					</g>
				);
			}
			const k = interpolate(p, [0, 0.6, 1], [0.4, 1.15, 1]) * (1 + 0.15 * pulse);
			return (
				<g opacity={Math.min(1, p * 2.5)} transform={`translate(${f.at[0]} ${f.at[1]}) scale(${k})`}>
					<CrownGlyph s={s} ghost={f.ghost} glow={pulse} />
				</g>
			);
		}
		default:
			throw new Error(`Unknown atlas feature kind ${f.kind}`);
	}
};

/** Map legend: rows dim until their cue, then light (symbol + text) and stay lit. Rendered in the scene, not as a graphic. */
const Key: React.FC<{f: AtlasFeature; p: number; t: number}> = ({f, t, p}) => {
	const timing = useTiming();
	const [x, y] = f.at;
	return (
		<g opacity={p}>
			<text x={x} y={y} fill={palette.fog} style={{fontFamily: fonts.ui, fontWeight: 700, fontSize: 22, letterSpacing: '0.24em', textTransform: 'uppercase'}}>
				{f.title ?? 'Map key'}
			</text>
			<line x1={x} y1={y + 14} x2={x + (f.width ?? 380)} y2={y + 14} stroke={palette.parchment} strokeOpacity={0.25} strokeWidth={1.2} />
			{(f.rows as {text: string; symbol: string; color?: string; at: Cue}[]).map((r, i) => {
				const q = ease(t, cueTime(timing, r.at) - 0.08, 0.45);
				const c = r.color ?? palette.amber;
				const ry = y + 52 + i * (f.gap ?? 50);
				return (
					<g key={i} opacity={0.28 + 0.72 * q}>
						<g transform={`translate(${x + 26} ${ry - 11}) scale(${0.9 + 0.1 * q})`}>
							<KeySymbol kind={r.symbol} c={c} />
						</g>
						<text x={x + 74 + (1 - q) * 6} y={ry} fill={q > 0.05 ? palette.ember : palette.parchment} style={{fontFamily: fonts.display, fontWeight: 600, fontSize: f.size ?? 46}}>
							{r.text}
						</text>
					</g>
				);
			})}
		</g>
	);
};

export const AtlasScene: React.FC<SceneProps> = ({progress, t, shot}) => {
	const timing = useTiming();
	const atlas = useContext(AtlasContext);
	if (!atlas) throw new Error('atlas scene needs episode.atlas');
	const span = timing.shots.find((s) => s.id === shot.id)!;
	const cfg = shot.atlas ?? {};
	const byId = new Map(atlas.features.map((f) => [f.id, f]));
	const show: ShowEntry[] = cfg.show ?? [];
	const zf = cfg.zoom ?? {from: 1.06, to: 1.0};
	// `zoom.at` + `dur`: a timed camera move on a cue (EP10's pull-back) instead of easing over the whole shot.
	const zp = zf.at ? ease(t, cueTime(timing, zf.at), zf.dur ?? 1.6, Easing.inOut(Easing.cubic)) : interpolate(progress, [0, 1], [0, 1], {easing: Easing.out(Easing.quad)});
	const zoom = lerp(zf.from, zf.to, zp);
	const base = ease(t, span.start - 0.3, 0.6);

	const items = show.map((e) => {
		const entry = typeof e === 'string' ? {id: e} : e;
		const f = byId.get(entry.id);
		if (!f) throw new Error(`Unknown atlas feature ${entry.id}`);
		const t0 = entry.at ? cueTime(timing, entry.at) : -1e9;
		const dur = entry.dur ?? 1;
		const p = entry.at ? ease(t, t0, dur, Easing.inOut(Easing.cubic)) : 1;
		const gone = entry.until ? 1 - ease(t, cueTime(timing, entry.until) - 0.15, 0.35) : 1;
		const tp = entry.pulse ? cueTime(timing, entry.pulse) : -1e9;
		const pulse = ease(t, tp, 0.2) * (1 - ease(t, tp + 0.45, 0.8));
		return {f, p: p * gone, pulse, t0: entry.at ? t0 : span.start};
	});

	return (
		<AbsoluteFill style={{backgroundColor: '#0d1519'}}>
			<AbsoluteFill style={{transform: `scale(${zoom})`, transformOrigin: zf.origin ?? '50% 40%'}}>
				<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
					<rect width={W} height={H} fill="#111b20" />
					<image href={staticFile('textures/paper.png')} width={W} height={H} preserveAspectRatio="none" />
					<g opacity={base}>
						<rect x={64} y={322} width={W - 128} height={876} fill="none" stroke={palette.parchment} strokeOpacity={0.28} strokeWidth={1.5} />
						<rect x={76} y={334} width={W - 152} height={852} fill="none" stroke={palette.parchment} strokeOpacity={0.12} strokeWidth={1} />
						{/* faint graticule */}
						{Array.from({length: 7}, (_, i) => (
							<line key={`v${i}`} x1={76 + (i + 1) * 116} y1={334} x2={76 + (i + 1) * 116} y2={1186} stroke={palette.parchment} strokeOpacity={0.04} />
						))}
						{Array.from({length: 6}, (_, i) => (
							<line key={`h${i}`} x1={76} y1={334 + (i + 1) * 122} x2={W - 76} y2={334 + (i + 1) * 122} stroke={palette.parchment} strokeOpacity={0.04} />
						))}
					</g>
					<defs>
						<clipPath id="atlas-frame">
							<rect x={76} y={334} width={W - 152} height={852} />
						</clipPath>
					</defs>
					<g clipPath="url(#atlas-frame)">
						{items
							.filter((it) => it.f.kind !== 'key' && it.p > 0)
							.map((it) => (
								<Feature key={it.f.id} f={it.f} p={it.p} pulse={it.pulse} t={t} t0={it.t0} />
							))}
					</g>
					{items
						.filter((it) => it.f.kind === 'key' && it.p > 0)
						.map((it) => (
							<Key key={it.f.id} f={it.f} p={it.p} t={t} />
						))}
					<g opacity={base * 0.6} transform="translate(900 1130)">
						<path d="M0,-30 L9,8 L0,0 L-9,8 Z" fill={palette.parchment} />
						<text y={36} textAnchor="middle" fill={palette.parchment} style={{fontFamily: fonts.display, fontSize: 26, fontWeight: 600}}>
							N
						</text>
					</g>
				</svg>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
