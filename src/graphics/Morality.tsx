import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {Cue, Timing} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Morality graphics (EP14 onward). `verdictScale`: a drawn balance that weighs two moral systems. The beam tips on
 * cues, each pan carries a caps label and a verdict word that can be replaced on later cues, and the pans glow when
 * the scale comes level. Repeat it with the same pans across shots and start each copy where the last one ended, so
 * it reads as one scale tipping one way, then the other.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const shadow = '0 3px 18px rgba(0,0,0,0.9)';
const tone = (c: string | undefined, fallback: string) => (c ? ((palette as Record<string, string>)[c] ?? c) : fallback);

type Word = {text: string; at: Cue; color?: string};

/** Beam angle (degrees, + = left pan down) from `[[cue, deg], …]`; each tip eases over 0.7 s with a small overshoot. */
const angle = (timing: Timing, t: number, tilts: [Cue, number][] | undefined) => {
	let a = 0;
	for (const [cue, deg] of tilts ?? []) a = lerp(a, deg, ease(t, cueTime(timing, cue), 0.7, Easing.out(Easing.back(1.6))));
	return a;
};

/**
 * Verdict scale: pivot at `[x, y]` (default 540, 560), `size` multiplier (default 1), `pans: [{label}, {label}]`
 * (left, right), `tilts: [[cue, degrees], …]` (+ tips the left pan down; about ±14), `words: [[Word…], [Word…]]` per
 * pan, each `{text, at, color?}` replacing the one before (cross-fade), `glowAt` (cue: both pans warm to ember, for
 * "both are right"), `start` cue (fade-in), optional `end`.
 */
export const VerdictScale: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const k: number = g.size ?? 1;
	const [px, py] = [g.x ?? W / 2, g.y ?? 560];
	const half = 250 * k;
	const chain = 170 * k;
	const t0 = cueTime(timing, g.start, span.start);
	const fresh = t0 > span.start + 0.05;
	const o = (fresh ? ease(t, t0, 0.45) : 1) * (1 - ease(t, (g.end ? cueTime(timing, g.end) : span.end + 0.1) - 0.3, 0.3));
	const deg = angle(timing, t, g.tilts);
	const rad = (deg * Math.PI) / 180;
	const glow = g.glowAt ? ease(t, cueTime(timing, g.glowAt), 0.6) : 0;
	const ends = [-1, 1].map((s) => [px + s * half * Math.cos(rad), py - s * half * Math.sin(rad)] as const);
	const pans: {label: string}[] = g.pans ?? [];
	const words: Word[][] = g.words ?? [[], []];
	const line = palette.amber;
	return (
		<AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
			{/* Soft dark pool so the scale reads over any plate. */}
			<div style={{position: 'absolute', left: px - 470 * k, top: py - 150 * k, width: 940 * k, height: 560 * k, background: 'radial-gradient(ellipse at 50% 50%, rgba(6,10,13,0.55) 0%, rgba(6,10,13,0.35) 50%, rgba(6,10,13,0) 72%)'}} />
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible', filter: 'drop-shadow(0 2px 8px rgba(0,0,0,0.85))'}}>
				{/* Post and foot */}
				<line x1={px} y1={py - 40 * k} x2={px} y2={py + 300 * k} stroke={line} strokeWidth={5 * k} strokeLinecap="round" />
				<path d={`M${px - 90 * k},${py + 312 * k} Q${px},${py + 270 * k} ${px + 90 * k},${py + 312 * k} Z`} fill={line} opacity={0.9} />
				<circle cx={px} cy={py - 52 * k} r={11 * k} fill="none" stroke={line} strokeWidth={4 * k} />
				{/* Beam */}
				<line x1={ends[0][0]} y1={ends[0][1]} x2={ends[1][0]} y2={ends[1][1]} stroke={line} strokeWidth={6 * k} strokeLinecap="round" />
				<path d={`M${px - 16 * k},${py + 4 * k} L${px},${py - 22 * k} L${px + 16 * k},${py + 4 * k} Z`} fill={line} />
				{ends.map(([ex, ey], i) => {
					const by = ey + chain;
					const c = glow > 0 ? `rgba(244,196,110,${0.25 + 0.75 * glow})` : 'transparent';
					return (
						<g key={i}>
							<circle cx={ex} cy={ey} r={7 * k} fill={line} />
							<line x1={ex} y1={ey} x2={ex - 92 * k} y2={by} stroke={line} strokeWidth={2.5 * k} />
							<line x1={ex} y1={ey} x2={ex + 92 * k} y2={by} stroke={line} strokeWidth={2.5 * k} />
							<ellipse cx={ex} cy={by + 4 * k} rx={130 * k} ry={34 * k} fill={c} opacity={0.35 * glow} />
							<path d={`M${ex - 108 * k},${by} Q${ex},${by + 46 * k} ${ex + 108 * k},${by} Z`} fill="rgba(233,169,75,0.18)" stroke={glow > 0.5 ? palette.ember : line} strokeWidth={4 * k} />
						</g>
					);
				})}
			</svg>
			{ends.map(([ex, ey], i) => {
				const by = ey + chain + 60 * k;
				const list = words[i] ?? [];
				return (
					<div key={i} style={{position: 'absolute', left: ex - 200 * k, width: 400 * k, top: by, textAlign: 'center'}}>
						<div style={{...kicker, fontSize: 30 * k, color: glow > 0.5 ? palette.ember : palette.amber, textShadow: shadow}}>{pans[i]?.label}</div>
						<div style={{display: 'grid', marginTop: 6 * k}}>
							{list.map((w, j) => {
								const a = ease(t, cueTime(timing, w.at), 0.35);
								const next = list[j + 1] ? ease(t, cueTime(timing, list[j + 1].at), 0.3) : 0;
								const v = a * (1 - next);
								return (
									<div
										key={j}
										style={{
											gridArea: '1 / 1',
											fontFamily: fonts.display,
											fontStyle: 'italic',
											fontWeight: 600,
											fontSize: 54 * k,
											lineHeight: 1.02,
											color: tone(w.color, palette.parchment),
											textShadow: shadow,
											opacity: v,
											transform: `translateY(${(1 - a) * 12 - next * 10}px) scale(${1 + (1 - a) * 0.06})`,
										}}
									>
										{w.text}
									</div>
								);
							})}
						</div>
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

export const MORALITY: Record<string, React.FC<GraphicProps>> = {
	verdictScale: VerdictScale,
};
