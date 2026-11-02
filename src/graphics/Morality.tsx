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
					<div key={i} style={{position: 'absolute', left: ex - 165 * k, width: 330 * k, top: by, textAlign: 'center', padding: `${14 * k}px 0`, margin: `${-14 * k}px 0`, background: 'radial-gradient(ellipse at 50% 50%, rgba(6,10,13,0.6) 0%, rgba(6,10,13,0.4) 50%, rgba(6,10,13,0) 75%)'}}>
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
											whiteSpace: 'pre-line',
											fontFamily: fonts.display,
											fontStyle: 'italic',
											fontWeight: 600,
											fontSize: 54 * k,
											lineHeight: 1.02,
											color: w.color === 'rust' ? '#d8714f' : tone(w.color, palette.parchment),
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

/**
 * Watch post: a weathered wooden post with a cross-peg, a long curved brass horn hung from it on a cord, and optional
 * rust `cloth` tied below the peg (EP14: the oath left behind; SDXL would not paint it). `at: [x, y]` = foot of the
 * post, `height` (default 460), `horn` (default true), `cloth` (default false), `flip` puts the horn on the left,
 * `shade` (0–1, default 0) darkens it for dusk plates. Pin with `local: true`.
 */
export const WatchPost: React.FC<GraphicProps> = ({g, t}) => {
	const [x, y] = g.at;
	const h: number = g.height ?? 460;
	const k = h / 460;
	const dir = g.flip ? -1 : 1;
	const top = y - h;
	const peg = top + 70 * k;
	const sway = Math.sin(t * 1.3) * 2.5;
	const id = `wp-${x}-${y}`;
	const hx = x + dir * 26 * k;
	const hornTop = peg + 80 * k;
	// Horn: a curved tapering tube hanging mouth-down, drawn as a filled band between two offset curves.
	const horn = `M${hx - 6 * k},${hornTop} C${hx - 8 * k},${hornTop + 90 * k} ${hx + dir * 20 * k},${hornTop + 150 * k} ${hx + dir * 70 * k},${hornTop + 170 * k}
		L${hx + dir * 88 * k},${hornTop + 140 * k}
		C${hx + dir * 40 * k},${hornTop + 130 * k} ${hx + 10 * k},${hornTop + 80 * k} ${hx + 6 * k},${hornTop} Z`;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: g.opacity ?? 1, filter: g.shade ? `brightness(${1 - 0.55 * g.shade})` : undefined}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<linearGradient id={`${id}-wood`} x1="0" y1="0" x2="1" y2="0">
						<stop offset="0" stopColor="#2b2017" />
						<stop offset="0.35" stopColor="#5d4632" />
						<stop offset="0.7" stopColor="#47362a" />
						<stop offset="1" stopColor="#1d1611" />
					</linearGradient>
					<linearGradient id={`${id}-brass`} x1="0" y1="0" x2="1" y2="1">
						<stop offset="0" stopColor="#f1d38a" />
						<stop offset="0.45" stopColor="#b8873a" />
						<stop offset="1" stopColor="#5e3f17" />
					</linearGradient>
				</defs>
				{/* Ground shadow */}
				<ellipse cx={x + dir * 30 * k} cy={y + 4 * k} rx={70 * k} ry={12 * k} fill="rgba(0,0,0,0.35)" />
				{/* Post, slightly tapered, with a weathered top */}
				<path d={`M${x - 17 * k},${y} L${x - 13 * k},${top + 8 * k} Q${x},${top - 6 * k} ${x + 13 * k},${top + 8 * k} L${x + 17 * k},${y} Z`} fill={`url(#${id}-wood)`} />
				{[0.22, 0.48, 0.71].map((f) => (
					<line key={f} x1={x - 6 * k} y1={top + h * f} x2={x - 4 * k} y2={top + h * f + 40 * k} stroke="rgba(0,0,0,0.35)" strokeWidth={2 * k} />
				))}
				{/* Peg */}
				<path d={`M${x},${peg} L${x + dir * 34 * k},${peg - 6 * k} L${x + dir * 34 * k},${peg + 4 * k} L${x},${peg + 10 * k} Z`} fill="#3a2b1f" />
				<g transform={`rotate(${sway} ${x + dir * 26 * k} ${peg})`}>
					{/* Cord */}
					<path d={`M${x + dir * 26 * k},${peg} Q${hx - 14 * k},${peg + 40 * k} ${hx - 2 * k},${hornTop + 4 * k}`} fill="none" stroke="#2a1f16" strokeWidth={3 * k} />
					{g.horn !== false && (
						<>
							<path d={horn} fill={`url(#${id}-brass)`} stroke="#3d2810" strokeWidth={1.5 * k} />
							<ellipse cx={hx + dir * 79 * k} cy={hornTop + 155 * k} rx={22 * k} ry={9 * k} transform={`rotate(${dir * -62} ${hx + dir * 79 * k} ${hornTop + 155 * k})`} fill="#2e1d0a" stroke="#d9b264" strokeWidth={2.5 * k} />
							<rect x={hx - 9 * k} y={hornTop - 6 * k} width={18 * k} height={9 * k} rx={2 * k} fill="#d9b264" />
							<path d={`M${hx - 2 * k},${hornTop + 30 * k} C${hx - 3 * k},${hornTop + 90 * k} ${hx + dir * 20 * k},${hornTop + 135 * k} ${hx + dir * 60 * k},${hornTop + 152 * k}`} fill="none" stroke="rgba(255,240,200,0.55)" strokeWidth={2 * k} />
						</>
					)}
				</g>
				{g.cloth && (
					<path
						d={`M${x - 15 * k},${peg + 34 * k} q${-dir * 10 * k},${18 * k} 0,${26 * k} L${x - dir * (60 + 8 * Math.sin(t * 2.1)) * k},${peg + (70 + 6 * Math.sin(t * 1.7)) * k} L${x - dir * (52 + 6 * Math.sin(t * 2.4)) * k},${peg + 46 * k} Z`}
						fill="#a8432c"
						stroke="#5f2214"
						strokeWidth={1.2 * k}
					/>
				)}
			</svg>
		</AbsoluteFill>
	);
};

export const MORALITY: Record<string, React.FC<GraphicProps>> = {
	verdictScale: VerdictScale,
	watchPost: WatchPost,
};
