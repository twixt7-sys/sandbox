import React from 'react';
import {AbsoluteFill, Easing, interpolate} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Power graphics (EP16 onward, Arc 4: Kingdoms and Power): who wears the crown vs who actually holds what people need.
 * The crown glyph is shared with the atlas (`crown` feature), so the same mark sits on the palace, travels to the real
 * holder on the map, and splits into TITLE / POWER on the lesson card.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 800, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

/**
 * Crown glyph centred on (0, 0), about 100 × 64 at s = 1. `ghost`: a dashed outline only (the title without the
 * power); otherwise amber-gold with ember jewels and a glow of `glow` (0..1).
 */
export const CrownGlyph: React.FC<{s?: number; ghost?: boolean; glow?: number; color?: string}> = ({s = 1, ghost, glow = 0, color}) => {
	const body = 'M-50,30 L-50,-12 L-26,8 L0,-34 L26,8 L50,-12 L50,30 Z';
	const tips: [number, number][] = [
		[-50, -12],
		[0, -34],
		[50, -12],
	];
	if (ghost) {
		const c = color ?? palette.mist;
		return (
			<g transform={`scale(${s})`} fill="none" stroke={c} strokeWidth={3 / s} strokeDasharray={`${9 / s} ${7 / s}`} strokeLinejoin="round" opacity={0.85}>
				<path d={body} />
				<line x1={-50} y1={18} x2={50} y2={18} />
				{tips.map(([x, y], i) => (
					<circle key={i} cx={x} cy={y - 5} r={5} strokeDasharray="none" />
				))}
			</g>
		);
	}
	const c = color ?? palette.amber;
	return (
		<g transform={`scale(${s})`} style={{filter: `drop-shadow(0 0 ${4 + 18 * glow}px rgba(244,196,110,${0.35 + 0.5 * glow}))`}}>
			<path d={body} fill={c} stroke="#7a5418" strokeWidth={2.5 / s} strokeLinejoin="round" />
			<rect x={-50} y={14} width={100} height={16} fill="#c98a2f" stroke="#7a5418" strokeWidth={2 / s} />
			{[-30, 0, 30].map((x) => (
				<circle key={x} cx={x} cy={22} r={4} fill={palette.rust} />
			))}
			{tips.map(([x, y], i) => (
				<circle key={i} cx={x} cy={y - 5} r={6} fill={palette.ember} stroke="#7a5418" strokeWidth={1.5 / s} />
			))}
		</g>
	);
};

/** Granary glyph for the atlas: a gabled storehouse between two round silos, centred on (0, 0). */
export const GranaryGlyph: React.FC = () => (
	<g stroke="#7a5418" strokeWidth={1.6} strokeLinejoin="round">
		{[-30, 30].map((x) => (
			<g key={x}>
				<rect x={x - 9} y={-14} width={18} height={34} fill={palette.parchment} opacity={0.9} />
				<path d={`M${x - 11},-14 L${x},-28 L${x + 11},-14 Z`} fill={palette.amber} />
			</g>
		))}
		<rect x={-20} y={-6} width={40} height={26} fill={palette.parchment} />
		<path d="M-25,-6 L0,-30 L25,-6 Z" fill={palette.amber} />
		<rect x={-7} y={4} width={14} height={16} fill="#5c3d10" />
		<line x1={0} y1={4} x2={0} y2={20} stroke={palette.amber} strokeWidth={1.2} />
	</g>
);

/**
 * TitlePower (EP16 lesson): one crown that splits in two on `splitAt`. The left copy stays as a dashed outline (THE
 * TITLE, `left`), the right one turns gold and glows (THE POWER, `right`); each column's kicker and italic `text`
 * (use "\n" for a second line) write in on `leftAt` / `rightAt`. `items: [{text, at}]` light as chips in a 2-wide grid
 * under the card (who can hold the power), and `sum` + `sumAt` closes it with one serif line. `top` (default 400).
 */
export const TitlePower: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const top = g.top ?? 400;
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.1;
	const appear = ease(t, t0, 0.5, Easing.out(Easing.back(1.4)));
	const split = ease(t, cueTime(timing, g.splitAt, t0 + 0.8), 0.7, Easing.inOut(Easing.cubic));
	const lA = ease(t, cueTime(timing, g.leftAt ?? g.splitAt, t0 + 0.9) + 0.1, 0.45);
	const rA = ease(t, cueTime(timing, g.rightAt ?? g.splitAt, t0 + 1.2) + 0.1, 0.45);
	const o = out(t, tEnd, 0.3);
	const cx = 540;
	const dx = 250 * split;
	const items: {text: string; at: any}[] = g.items ?? [];
	const sumP = g.sumAt ? ease(t, cueTime(timing, g.sumAt) - 0.05, 0.5) : 0;
	const col = (side: 'left' | 'right', a: number, data: {kicker: string; text: string}) => (
		<div
			style={{
				position: 'absolute',
				top: top + 150,
				left: side === 'left' ? cx - 250 - 230 : cx + 250 - 230,
				width: 460,
				textAlign: 'center',
				opacity: a,
				transform: `translateY(${(1 - a) * 12}px)`,
			}}
		>
			<div style={{...kicker, fontSize: 32, color: side === 'left' ? palette.fog : palette.amber}}>{data.kicker}</div>
			<div style={{marginTop: 10, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 60, lineHeight: 1.02, color: side === 'left' ? palette.mist : palette.ember, whiteSpace: 'pre-line', textShadow: '0 3px 18px rgba(0,0,0,0.9)'}}>
				{data.text}
			</div>
		</div>
	);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				{/* the split seam */}
				<line x1={cx} y1={top - 40} x2={cx} y2={top + 330} stroke={palette.amber} strokeOpacity={0.5 * split} strokeWidth={2} strokeDasharray="4 10" />
				<g transform={`translate(${cx - dx} ${top + 40}) scale(${0.6 + 0.4 * appear})`} opacity={Math.min(1, appear * 2)}>
					<CrownGlyph s={1.1} ghost={split > 0.5} glow={0} color={split > 0.5 ? palette.mist : undefined} />
				</g>
				<g transform={`translate(${cx + dx} ${top + 40}) scale(${0.6 + 0.4 * appear})`} opacity={Math.min(1, appear * 2) * Math.min(1, split * 4)}>
					<CrownGlyph s={1.1} glow={rA} />
				</g>
				<text x={cx} y={top + 62} textAnchor="middle" fill={palette.rust} opacity={split} style={{fontFamily: fonts.display, fontWeight: 700, fontSize: 84}}>
					≠
				</text>
			</svg>
			{col('left', lA, g.left)}
			{col('right', rA, g.right)}
			<div style={{position: 'absolute', top: top + 430, left: 120, width: 840, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '22px 26px'}}>
				{items.map((it, i) => {
					const p = ease(t, cueTime(timing, it.at) - 0.08, 0.35, Easing.out(Easing.back(1.6)));
					return (
						<div
							key={i}
							style={{
								...kicker,
								fontSize: 32,
								width: 380,
								textAlign: 'center',
								padding: '18px 0 15px',
								color: palette.ember,
								border: `2px solid ${palette.ember}`,
								borderRadius: 999,
								background: 'rgba(8,12,16,0.55)',
								opacity: 0.12 + 0.88 * p,
								transform: `scale(${0.9 + 0.1 * p})`,
								boxShadow: `0 0 ${22 * p}px rgba(244,196,110,${0.25 * p})`,
							}}
						>
							{it.text}
						</div>
					);
				})}
			</div>
			{g.sum && (
				<div style={{position: 'absolute', top: top + 690, width: '100%', textAlign: 'center', fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 64, color: palette.parchment, opacity: sumP, transform: `translateY(${(1 - sumP) * 10}px)`}}>
					{g.sum}
				</div>
			)}
		</AbsoluteFill>
	);
};

/**
 * GrainSack: a tied burlap sack of grain standing on the ground, a few grains spilled (EP16). `at: [x, y]` = centre of
 * the base, `size` (height, default 120), `tone: "day" | "dusk"`, `lean` (degrees). Pin with `local: true`.
 */
export const GrainSack: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [x, y] = g.at;
	const h = g.size ?? 120;
	const w = h * 0.78;
	const dusk = g.tone === 'dusk';
	const cloth = dusk ? ['#8a6b47', '#5a4430', '#3a2b1f'] : ['#c4a06a', '#8d6c43', '#5a4430'];
	const p = g.start ? ease(t, cueTime(timing, g.start, span.start), 0.4) : 1;
	const body = `M${-w * 0.42},0 C${-w * 0.56},${-h * 0.35} ${-w * 0.5},${-h * 0.66} ${-w * 0.2},${-h * 0.78} L${w * 0.2},${-h * 0.78} C${w * 0.5},${-h * 0.66} ${w * 0.56},${-h * 0.35} ${w * 0.42},0 Z`;
	const grains = [
		[-0.62, -0.02], [-0.7, 0.0], [-0.55, 0.015], [0.6, 0.0], [0.68, -0.01], [0.52, 0.02], [0.75, 0.012],
	];
	return (
		<AbsoluteFill style={{opacity: p * (g.opacity ?? 1)}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<g transform={`translate(${x} ${y}) rotate(${g.lean ?? 0})`}>
					<ellipse cx={w * 0.05} cy={2} rx={w * 0.62} ry={h * 0.06} fill="rgba(8,6,4,0.5)" style={{filter: `blur(${h * 0.03}px)`}} />
					<path d={body} fill={cloth[0]} stroke={cloth[2]} strokeWidth={2} />
					{/* shading on the right flank, weave lines */}
					<path d={`M${w * 0.1},0 C${w * 0.38},${-h * 0.3} ${w * 0.4},${-h * 0.6} ${w * 0.2},${-h * 0.78} C${w * 0.5},${-h * 0.66} ${w * 0.56},${-h * 0.35} ${w * 0.42},0 Z`} fill={cloth[1]} opacity={0.7} />
					{[0.25, 0.45, 0.65].map((u) => (
						<path key={u} d={`M${-w * 0.45},${-h * u} Q0,${-h * u + h * 0.04} ${w * 0.45},${-h * u}`} fill="none" stroke={cloth[2]} strokeOpacity={0.35} strokeWidth={1.2} />
					))}
					{/* neck, tie and the open grain top */}
					<path d={`M${-w * 0.2},${-h * 0.78} L${-w * 0.14},${-h * 0.9} L${w * 0.14},${-h * 0.9} L${w * 0.2},${-h * 0.78} Z`} fill={cloth[0]} stroke={cloth[2]} strokeWidth={1.5} />
					<rect x={-w * 0.17} y={-h * 0.82} width={w * 0.34} height={h * 0.05} fill="#6b3f22" />
					<ellipse cx={0} cy={-h * 0.92} rx={w * 0.2} ry={h * 0.05} fill={dusk ? '#b8913f' : '#e3bd62'} stroke={cloth[2]} strokeWidth={1} />
					{grains.map(([gx, gy], i) => (
						<ellipse key={i} cx={gx * w} cy={gy * h} rx={h * 0.018} ry={h * 0.011} fill={dusk ? '#b8913f' : '#e3bd62'} transform={`rotate(${i * 37} ${gx * w} ${gy * h})`} />
					))}
				</g>
			</svg>
		</AbsoluteFill>
	);
};

/**
 * KeyRing: a heavy iron ring of long keys hanging from a point (a belt, a hand), swinging gently (EP16: the granary
 * keeper's keys, which SDXL would not paint). `at: [x, y]` = the hanging point, `size` (ring radius, default 26),
 * `count` (keys, default 5), `start` cue to fade in. Pin with `local: true`.
 */
export const KeyRing: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [x, y] = g.at;
	const r = g.size ?? 26;
	const n = g.count ?? 5;
	const p = g.start ? ease(t, cueTime(timing, g.start, span.start), 0.4) : 1;
	const sway = Math.sin(t * 1.7) * 3;
	const iron = '#77736a';
	const hi = '#d8d2c0';
	return (
		<AbsoluteFill style={{opacity: p * (g.opacity ?? 1)}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<g transform={`translate(${x} ${y}) rotate(${sway})`} style={{filter: 'drop-shadow(0 2px 3px rgba(0,0,0,0.7))'}}>
					<circle cx={0} cy={r} r={r} fill="none" stroke={iron} strokeWidth={r * 0.22} />
					<circle cx={0} cy={r} r={r} fill="none" stroke={hi} strokeWidth={r * 0.06} strokeDasharray={`${r * 0.8} ${r * 2.2}`} />
					{Array.from({length: n}, (_, i) => {
						const a = ((i - (n - 1) / 2) / n) * 1.6;
						const bx = Math.sin(a) * r;
						const by = r + Math.cos(a) * r;
						const len = r * (2.2 + 0.35 * ((i * 7) % 3));
						return (
							<g key={i} transform={`translate(${bx} ${by}) rotate(${(-a * 180) / Math.PI * 0.6})`}>
								<circle cx={0} cy={r * 0.28} r={r * 0.26} fill="none" stroke={iron} strokeWidth={r * 0.12} />
								<rect x={-r * 0.06} y={r * 0.5} width={r * 0.12} height={len} fill={iron} />
								<rect x={0} y={r * 0.5 + len - r * 0.4} width={r * 0.32} height={r * 0.14} fill={iron} />
								<rect x={0} y={r * 0.5 + len - r * 0.15} width={r * 0.24} height={r * 0.14} fill={iron} />
								<rect x={-r * 0.03} y={r * 0.55} width={r * 0.03} height={len * 0.8} fill={hi} opacity={0.6} />
							</g>
						);
					})}
				</g>
			</svg>
		</AbsoluteFill>
	);
};

/** Small helper so other files can ease a crown along an arc between two points. */
export const arcPoint = (a: [number, number], b: [number, number], u: number, lift = 0.25): [number, number] => {
	const mx = (a[0] + b[0]) / 2;
	const my = (a[1] + b[1]) / 2 - Math.hypot(b[0] - a[0], b[1] - a[1]) * lift;
	const q = interpolate(u, [0, 1], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return [lerp(lerp(a[0], mx, q), lerp(mx, b[0], q), q), lerp(lerp(a[1], my, q), lerp(my, b[1], q), q)];
};

export const POWER: Record<string, React.FC<GraphicProps>> = {
	titlePower: TitlePower,
	grainSack: GrainSack,
	keyRing: KeyRing,
};
