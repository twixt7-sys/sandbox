import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Everyday graphics (EP15 onward): reading a whole people from one ordinary habit. An evidence chain is inked onto the
 * plate itself: a pen loop round the clue, a leader, then what we see → what it means → ∴ the value, sealed in ember.
 * Pin with `local: true` so the ink rides the camera move.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const shadow = 'drop-shadow(0 1px 5px rgba(0,0,0,0.85))';

/** A hand-drawn pen loop: an ellipse with a gentle wobble, run about 1.12 turns so the ends overlap like ink. */
const loopPath = (cx: number, cy: number, rx: number, ry: number, seed = 1) => {
	const N = 72;
	const turns = 1.12;
	const a0 = -2.2 + seed * 0.7;
	const pts = Array.from({length: N + 1}, (_, i) => {
		const u = i / N;
		const a = a0 + u * turns * Math.PI * 2;
		const wob = 1 + 0.045 * Math.sin(a * 3 + seed) + 0.03 * Math.sin(a * 5 + seed * 2) + 0.06 * u;
		return [cx + Math.cos(a) * rx * wob, cy + Math.sin(a) * ry * wob] as const;
	});
	return 'M' + pts.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(' L');
};

/** The ember value seal: "∴" then the value in spaced caps inside a thin ember frame. */
const Seal: React.FC<{text: string; p: number; size?: number}> = ({text, p, size = 30}) => (
	<div style={{display: 'inline-flex', alignItems: 'center', gap: 14, opacity: Math.min(1, p * 1.6), transform: `scale(${0.82 + 0.18 * p})`, transformOrigin: 'left center'}}>
		<span style={{fontFamily: fonts.display, fontWeight: 700, fontSize: size * 1.6, lineHeight: 1, color: palette.amber, textShadow: '0 2px 12px rgba(0,0,0,0.9)'}}>∴</span>
		<span
			style={{
				...kicker,
				fontWeight: 800,
				fontSize: size,
				color: palette.ember,
				padding: `${size * 0.32}px ${size * 0.6}px ${size * 0.26}px`,
				border: `2.5px solid ${palette.ember}`,
				borderRadius: 6,
				background: 'rgba(8,12,16,0.62)',
				boxShadow: `0 0 ${24 * p}px rgba(244,196,110,${0.35 * p})`,
				whiteSpace: 'nowrap',
			}}
		>
			{text}
		</span>
	</div>
);

/**
 * InferChain: `at: [x, y]` the clue, `loop: [rx, ry]` (default [90, 60]) the pen loop round it, `box: [x, y]` where the
 * text block hangs (its top edge; `align` "left" | "right" | "center" says which edge of the block sits on x), `width`.
 * Tiers: `seen` (caps, amber) from `start`; `means` (serif italic) at `meansAt`; `value` (∴ + ember seal) at `valueAt`.
 * `end` fades it (else the shot end). `backdrop: true` puts a soft dark glow behind the text block. Seal-only mode: give just `value` (no `seen`): a dot on the clue, a short leader to
 * `box`, and the seal, for pinning several values onto one wide plate. `noLoop: true` skips the loop.
 */
export const InferChain: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [cx, cy] = g.at;
	const [rx, ry] = g.loop ?? [90, 60];
	const [bx, by] = g.box;
	const align: 'left' | 'right' | 'center' = g.align ?? 'left';
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.1;
	const sealOnly = !g.seen;
	const loop = g.noLoop || sealOnly ? 0 : ease(t, t0 - 0.05, 0.55, Easing.inOut(Easing.quad));
	const dot = sealOnly ? ease(t, t0 - 0.05, 0.35, Easing.out(Easing.back(1.8))) : 0;
	const lead = ease(t, t0 + (sealOnly ? 0.05 : 0.35), 0.35);
	const seen = ease(t, t0 + 0.5, 0.4);
	const means = g.meansAt ? ease(t, cueTime(timing, g.meansAt) - 0.05, 0.45) : 0;
	const vT = g.valueAt ? cueTime(timing, g.valueAt) : t0 + 0.25;
	const value = ease(t, vT - 0.05, 0.45, Easing.out(Easing.back(1.6)));
	const o = out(t, tEnd, 0.3) * (g.opacity ?? 1);
	// Leader: from the edge of the loop (or the dot) toward the block's anchor, a soft curve.
	const ang = Math.atan2(by - cy, bx - cx);
	const sx = cx + Math.cos(ang) * (sealOnly ? 12 : rx * 1.08);
	const sy = cy + Math.sin(ang) * (sealOnly ? 12 : ry * 1.08);
	const ex = bx;
	const ey = by + (sealOnly ? 30 : 22);
	const mx = (sx + ex) / 2 + (ey - sy) * 0.12;
	const my = (sy + ey) / 2 - (ex - sx) * 0.12;
	const c = g.color ?? palette.amber;
	const blockPos: React.CSSProperties =
		align === 'left' ? {left: bx + 14} : align === 'right' ? {right: W - bx + 14} : {left: bx, transform: 'translateX(-50%)'};
	return (
		<AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				{loop > 0 && (
					<path d={loopPath(cx, cy, rx, ry, g.seed ?? 1)} fill="none" stroke={c} strokeWidth={4.5} strokeLinecap="round" pathLength={1} strokeDasharray={`${loop} 1`} style={{filter: shadow}} />
				)}
				{sealOnly && <circle cx={cx} cy={cy} r={9 * dot} fill={palette.ember} style={{filter: shadow}} />}
				{sealOnly && <circle cx={cx} cy={cy} r={22 * dot} fill="none" stroke={palette.ember} strokeWidth={2} opacity={0.7 * dot} />}
				<path d={`M${sx},${sy} Q${mx},${my} ${ex},${ey}`} fill="none" stroke={c} strokeWidth={2.5} strokeLinecap="round" pathLength={1} strokeDasharray={`${lead} 1`} style={{filter: shadow}} />
			</svg>
			<div
				style={{
					position: 'absolute',
					top: by,
					...blockPos,
					width: g.width,
					textAlign: align,
					...(g.backdrop && !sealOnly
						? {background: `radial-gradient(ellipse at 50% 50%, rgba(6,10,13,${0.6 * seen}) 0%, rgba(6,10,13,${0.4 * seen}) 55%, rgba(6,10,13,0) 75%)`, padding: '26px 60px 22px', margin: '-26px -60px 0'}
						: {}),
				}}
			>
				{!sealOnly && (
					<>
						<div style={{...kicker, fontSize: 30, color: c, opacity: seen, transform: `translateY(${(1 - seen) * 10}px)`, textShadow: '0 2px 12px rgba(0,0,0,0.95)'}}>{g.seen}</div>
						{g.means && (
							<div
								style={{
									marginTop: 4,
									fontFamily: fonts.display,
									fontStyle: 'italic',
									fontWeight: 600,
									fontSize: g.size ?? 56,
									lineHeight: 1.04,
									color: palette.parchment,
									opacity: means,
									transform: `translateY(${(1 - means) * 12}px)`,
									textShadow: '0 3px 18px rgba(0,0,0,0.95), 0 0 40px rgba(0,0,0,0.6)',
								}}
							>
								{g.means}
							</div>
						)}
					</>
				)}
				{g.value && (
					<div style={{marginTop: sealOnly ? 0 : 14, display: 'flex', justifyContent: align === 'left' ? 'flex-start' : align === 'right' ? 'flex-end' : 'center', opacity: value > 0.001 ? 1 : 0}}>
						<Seal text={g.value} p={value} size={g.sealSize ?? 30} />
					</div>
				)}
			</div>
		</AbsoluteFill>
	);
};

/**
 * Bench: a plain backless timber bench standing in a street, seen slightly from above (EP15; SDXL would not paint one
 * in the road). `at: [x, y]` = centre of the ground line, `length` (default 220), `height` (seat height, default
 * length × 0.22), `tone: "day" | "dusk"`, `cups` (number of small clay cups on the seat). Pin with `local: true`.
 */
export const Bench: React.FC<GraphicProps> = ({g}) => {
	const [cx, cy] = g.at;
	const L = g.length ?? 220;
	const h = g.height ?? L * 0.22;
	const th = Math.max(4, L * 0.05); // seat thickness
	const depth = L * 0.09; // visible top face
	const x0 = cx - L / 2;
	const x1 = cx + L / 2;
	const top = cy - h;
	const dusk = g.tone === 'dusk';
	const wood = dusk ? ['#7a5a3e', '#4a3324', '#2a1c14'] : ['#a07448', '#66422a', '#36231a'];
	const leg = L * 0.045;
	const legX = [x0 + L * 0.1, x1 - L * 0.1 - leg];
	const cups = g.cups ?? 0;
	return (
		<AbsoluteFill style={{opacity: g.opacity ?? 1}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<ellipse cx={cx + L * 0.04} cy={cy + 2} rx={L * 0.58} ry={depth * 0.75} fill="rgba(10,8,6,0.45)" style={{filter: `blur(${L * 0.025}px)`}} />
				{legX.map((lx, i) => (
					<g key={i}>
						<rect x={lx} y={top + th - 1} width={leg} height={h - th + 1} fill={wood[2]} />
						<rect x={lx + depth * 0.5} y={top - depth + th} width={leg * 0.9} height={h - th + depth * 0.4} fill={wood[2]} opacity={0.8} />
					</g>
				))}
				{/* top face (lit), then front edge */}
				<path d={`M${x0},${top} L${x0 + depth * 0.6},${top - depth} L${x1 + depth * 0.6},${top - depth} L${x1},${top} Z`} fill={wood[0]} />
				<path d={`M${x0 + L * 0.02},${top - depth * 0.45} L${x1 + L * 0.0},${top - depth * 0.45}`} stroke={wood[1]} strokeWidth={1} opacity={0.6} />
				<rect x={x0} y={top} width={L} height={th} fill={wood[1]} />
				{Array.from({length: cups}, (_, i) => {
					const ux = cx + (i - (cups - 1) / 2) * L * 0.5;
					const cw = L * 0.06;
					const ch = L * 0.07;
					return <path key={i} d={`M${ux - cw / 2},${top - depth * 0.5 - ch} L${ux + cw / 2},${top - depth * 0.5 - ch} L${ux + cw * 0.38},${top - depth * 0.5} L${ux - cw * 0.38},${top - depth * 0.5} Z`} fill={dusk ? '#8c4f33' : '#b8673f'} />;
				})}
			</svg>
		</AbsoluteFill>
	);
};

export const EVERYDAY: Record<string, React.FC<GraphicProps>> = {
	inferChain: InferChain,
	bench: Bench,
};
