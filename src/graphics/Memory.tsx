import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Memory graphics (EP20, Arc 4): two nations remembering one war. Each side's memorial is a carved tablet (all text drawn
 * here, never generated), and each tablet comes with the frame it chooses: a gilt crop that darkens everything outside it.
 * On a cue the frame opens and the plate shows what the chronicle left out. Lanterns are small code-drawn lights for
 * mourning on both banks.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
/** `ease` that stays at 0 for an absent cue. */
const at = (t: number, s: number, dur: number) => (Number.isFinite(s) ? ease(t, s, dur) : 0);
const cue = (timing: ReturnType<typeof useTiming>, c: Cue | undefined) => (c ? cueTime(timing, c) : Infinity);

/**
 * ChronicleFrame: `frame: [x, y, w, h]` (plate px) is the view a chronicle keeps. Everything outside it darkens (`dim`,
 * default 0.8) behind a gilt border with corner brackets, from `start` (else the shot start). `openAt` widens the frame
 * past the plate edges while the darkness lifts and the border fades, so the plate shows what was cropped out.
 * `dim: 0` draws the border alone (EP20's final shot frames both stones in one picture). `label` sits on the top edge.
 * Pin with `local: true` so the frame rides the camera move.
 */
export const ChronicleFrame: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [fx, fy, fw, fh] = g.frame as number[];
	const t0 = g.start ? cueTime(timing, g.start) : span.start;
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.2;
	const tOpen = cue(timing, g.openAt);
	const show = (g.instant ? 1 : ease(t, t0, 0.5)) * out(t, tEnd, 0.3);
	const p = at(t, tOpen, g.openDur ?? 1.1);
	const x = lerp(fx, -80, p);
	const y = lerp(fy, -80, p);
	const w = lerp(fw, W + 160, p);
	const h = lerp(fh, H + 160, p);
	const dim = (g.dim ?? 0.8) * (1 - p);
	const c = palette.amber;
	const b = 46;
	const border = (1 - ease(t, tOpen + 0.15, 0.6)) * show;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				{dim > 0.001 && (
					<path
						d={`M-200,-200 H${W + 200} V${H + 200} H-200 Z M${x},${y} V${y + h} H${x + w} V${y} Z`}
						fill="#05090c"
						fillRule="evenodd"
						opacity={dim * show}
					/>
				)}
				<g opacity={border} style={{filter: 'drop-shadow(0 1px 6px rgba(0,0,0,0.85))'}}>
					<rect x={x} y={y} width={w} height={h} fill="none" stroke={c} strokeOpacity={0.7} strokeWidth={2} />
					<rect x={x + 9} y={y + 9} width={w - 18} height={h - 18} fill="none" stroke={c} strokeOpacity={0.3} strokeWidth={1.2} />
					{[
						[x, y, 1, 1],
						[x + w, y, -1, 1],
						[x, y + h, 1, -1],
						[x + w, y + h, -1, -1],
					].map(([cx, cy, sx, sy], i) => (
						<path key={i} d={`M${cx},${cy + sy * b} V${cy} H${cx + sx * b}`} fill="none" stroke={c} strokeWidth={5} strokeLinecap="square" />
					))}
				</g>
			</svg>
			{g.label && (
				<div style={{position: 'absolute', left: x + w / 2, top: y - 17, transform: 'translateX(-50%)', opacity: border, ...kicker, fontSize: 22, color: c, background: '#0b1216', padding: '6px 14px 4px', whiteSpace: 'nowrap'}}>
					{g.label}
				</div>
			)}
		</AbsoluteFill>
	);
};

/**
 * Tablet: a carved memorial inscription. `at: [x, y]` is its top-left (or top-centre with `align: "center"`), `width`
 * (default 560). `kicker` (amber caps) names whose stone it is; `lines` are cut into the stone letter by letter from
 * `start` over `dur` (default 1.4 s; a chisel `sfx` belongs on the same cue). `size` sets the carved type (default 46).
 * `sealAt` stamps an ember `seal` (default "TRUE") on its corner; `leftOut: {text, at}` adds a mist italic line under
 * the stone naming what it leaves out. `end` fades it (else the shot end). Pin with `local: true` to stand it on a plate.
 */
export const Tablet: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [ax, ay] = g.at as number[];
	const width = g.width ?? 560;
	const size = g.size ?? 46;
	const lines: string[] = g.lines ?? [];
	const t0 = g.start ? cueTime(timing, g.start) : span.start;
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.15;
	const dur = g.dur ?? 1.4;
	const show = (g.instant ? 1 : ease(t, t0 - 0.25, 0.4)) * out(t, tEnd, 0.3);
	const total = lines.reduce((n, l) => n + l.length, 0) || 1;
	const tSeal = cue(timing, g.sealAt);
	const seal = at(t, tSeal, 0.35);
	const leftOut = g.leftOut as {text: string; at: Cue} | undefined;
	const lo = leftOut ? at(t, cueTime(timing, leftOut.at), 0.5) : 0;
	let done = 0;
	return (
		<AbsoluteFill style={{opacity: show, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', top: ay, left: ax, width, transform: g.align === 'center' ? 'translateX(-50%)' : undefined}}>
				{g.kicker && <div style={{...kicker, fontSize: g.kickerSize ?? 24, color: palette.amber, marginBottom: 12, textShadow: '0 2px 10px rgba(0,0,0,0.9)', textAlign: g.align === 'center' ? 'center' : 'left'}}>{g.kicker}</div>}
				<div
					style={{
						position: 'relative',
						padding: `${size * 0.55}px ${size * 0.6}px ${size * 0.5}px`,
						background: 'linear-gradient(170deg, #3b4349 0%, #2a3136 55%, #20262a 100%)',
						border: '1.5px solid rgba(239,230,210,0.22)',
						borderRadius: 4,
						boxShadow: 'inset 0 2px 0 rgba(255,255,255,0.08), inset 0 -3px 8px rgba(0,0,0,0.45), 0 10px 40px rgba(0,0,0,0.55)',
						textAlign: 'center',
					}}
				>
					{lines.map((ln, i) => {
						const a = done / total;
						done += ln.length;
						const k = Math.max(0, Math.min(1, (ease(t, t0, dur, Easing.linear) - a) / (ln.length / total)));
						return (
							<div
								key={i}
								style={{
									fontFamily: fonts.display,
									fontWeight: 700,
									fontSize: size,
									lineHeight: 1.12,
									letterSpacing: '0.1em',
									color: '#ddd2b8',
									whiteSpace: 'nowrap',
									textShadow: '0 -1px 0 rgba(0,0,0,0.85), 0 1px 0 rgba(255,255,255,0.14)',
									clipPath: `inset(0 ${(1 - k) * 100}% 0 0)`,
								}}
							>
								{ln}
							</div>
						);
					})}
					{Number.isFinite(tSeal) && (
						<div
							style={{
								position: 'absolute',
								right: -22,
								top: -26,
								...kicker,
								fontWeight: 800,
								fontSize: g.sealSize ?? 28,
								color: palette.ember,
								padding: '8px 16px 6px',
								border: `3px solid ${palette.ember}`,
								borderRadius: 6,
								background: 'rgba(8,12,16,0.78)',
								boxShadow: `0 0 ${26 * seal}px rgba(244,196,110,${0.4 * seal})`,
								opacity: Math.min(1, seal * 1.6),
								transform: `rotate(-7deg) scale(${lerp(1.5, 1, seal)})`,
							}}
						>
							{g.seal ?? 'True'}
						</div>
					)}
				</div>
				{leftOut && (
					<div style={{marginTop: 14, textAlign: g.align === 'center' ? 'center' : 'left', opacity: lo, transform: `translateY(${(1 - lo) * 10}px)`, whiteSpace: 'nowrap'}}>
						<span style={{...kicker, fontSize: 22, color: palette.rust, marginRight: 14, textShadow: '0 2px 10px rgba(0,0,0,0.9)'}}>Left out</span>
						<span style={{fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 40, color: palette.mist, textShadow: '0 2px 14px rgba(0,0,0,0.9)'}}>{leftOut.text}</span>
					</div>
				)}
			</div>
		</AbsoluteFill>
	);
};

/**
 * TruthRows: short lesson rows that land one by one on `rows: [{text, at}]` (*word* = amber italic), centred from `y`
 * (default 760), then `sum` (string or lines; *word* = ember italic) with an optional `sumKicker` at `sumAt`, while the
 * rows step back. `size` (default 64).
 */
export const TruthRows: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const rows: {text: string; at: Cue}[] = g.rows ?? [];
	const y = g.y ?? 760;
	const size = g.size ?? 64;
	const tSum = cue(timing, g.sumAt);
	const s = at(t, tSum, 0.6);
	const o = out(t, g.end ? cueTime(timing, g.end) : span.end + 0.2, 0.35);
	const sum: string[] = Array.isArray(g.sum) ? g.sum : g.sum ? [g.sum] : [];
	const words = (txt: string, em: string) =>
		txt.split(' ').map((w, k) => (
			<span key={k} style={{marginRight: '0.24em', ...(w.startsWith('*') ? {color: em, fontStyle: 'italic'} : {})}}>
				{w.replace(/\*/g, '')}
			</span>
		));
	return (
		<AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', top: y, width: '100%', textAlign: 'center'}}>
				{rows.map((r, i) => {
					const p = ease(t, cueTime(timing, r.at) - 0.05, 0.45);
					return (
						<div key={i} style={{fontFamily: fonts.display, fontWeight: 600, fontSize: size, lineHeight: 1.12, color: palette.parchment, opacity: p * lerp(1, 0.35, s), transform: `translateY(${(1 - p) * 16}px)`, textShadow: '0 4px 30px rgba(0,0,0,0.85)'}}>
							{words(r.text, palette.amber)}
						</div>
					);
				})}
				{sum.length > 0 && (
					<div style={{marginTop: 34, opacity: s, transform: `translateY(${(1 - s) * 16}px)`}}>
						{g.sumKicker && <div style={{...kicker, fontSize: 26, color: palette.amber, marginBottom: 10, textShadow: '0 2px 10px rgba(0,0,0,0.9)'}}>{g.sumKicker}</div>}
						{sum.map((ln, i) => (
							<div key={i} style={{fontFamily: fonts.display, fontWeight: 600, fontSize: g.sumSize ?? 80, lineHeight: 1.06, color: palette.parchment, textShadow: '0 4px 34px rgba(0,0,0,0.85)'}}>
								{words(ln, palette.ember)}
							</div>
						))}
					</div>
				)}
			</div>
		</AbsoluteFill>
	);
};

/**
 * Lanterns: small memorial lanterns on posts at `at: [[x, y], …]` (the foot of the post), lit one after another from
 * `start` (`stagger`, default 0.35 s) with a warm, gently flickering glow. `size` scales them (default 1). Pin with
 * `local: true`.
 */
export const MemorialLanterns: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const pts: number[][] = g.at ?? [];
	const t0 = g.start ? cueTime(timing, g.start) : span.start;
	const k = g.size ?? 1;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<radialGradient id="lanternGlow">
						<stop offset="0%" stopColor="#ffd98a" stopOpacity={0.85} />
						<stop offset="35%" stopColor="#f4a94b" stopOpacity={0.35} />
						<stop offset="100%" stopColor="#e9a94b" stopOpacity={0} />
					</radialGradient>
				</defs>
				{pts.map(([x, y], i) => {
					const lit = g.instant ? 1 : ease(t, t0 + i * (g.stagger ?? 0.35), 0.7);
					const fl = 0.9 + 0.06 * Math.sin(t * 9.3 + i * 2.1) + 0.04 * Math.sin(t * 23.7 + i);
					const top = y - 70 * k;
					return (
						<g key={i}>
							<circle cx={x} cy={top + 12 * k} r={120 * k * fl} fill="url(#lanternGlow)" opacity={lit} />
							<rect x={x - 2.5 * k} y={top + 26 * k} width={5 * k} height={44 * k} fill="#14100c" />
							<path d={`M${x - 10 * k},${top} H${x + 10 * k} L${x + 8 * k},${top + 26 * k} H${x - 8 * k} Z`} fill={lit > 0.05 ? '#ffcf7a' : '#3a3026'} fillOpacity={0.4 + 0.6 * lit * fl} stroke="#1a140e" strokeWidth={2.2 * k} />
							<path d={`M${x - 12 * k},${top} H${x + 12 * k} L${x},${top - 9 * k} Z`} fill="#1a140e" />
						</g>
					);
				})}
			</svg>
		</AbsoluteFill>
	);
};

export const MEMORY: Record<string, React.FC<GraphicProps>> = {
	chronicleFrame: ChronicleFrame,
	tablet: Tablet,
	truthRows: TruthRows,
	lanterns: MemorialLanterns,
};
