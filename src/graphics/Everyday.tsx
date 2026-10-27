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
 * `end` fades it (else the shot end). Seal-only mode: give just `value` (no `seen`): a dot on the clue, a short leader to
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
			<div style={{position: 'absolute', top: by, ...blockPos, width: g.width, textAlign: align}}>
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

export const EVERYDAY: Record<string, React.FC<GraphicProps>> = {
	inferChain: InferChain,
};
