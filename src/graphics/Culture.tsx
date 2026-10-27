import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, staticFile} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {Cue, Timing} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Culture graphics (EP13 onward): two rule-sets compared side by side. `splitFrame` cuts the screen in two along a
 * drawn seam (a border) and plays a plate in each half; `mirrorLedger` sets two cultures' rules and reasons in
 * matching columns. Arc 3 episodes that compare peoples (EP14 honour, EP15 invisible details) can reuse both.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const shadow = '0 3px 18px rgba(0,0,0,0.9)';

/** `ease` that stays at 0 for an absent cue (start = Infinity). */
const ez = (t: number, start: number, dur: number, easing?: (x: number) => number) => (Number.isFinite(start) ? ease(t, start, dur, easing) : 0);

/** Piecewise level from `[[cue, value], …]` steps, each eased in over 0.35 s (half brightness, row lighting). */
const steps = (timing: Timing, t: number, list: [Cue, number][] | undefined, initial = 1) => {
	if (!list?.length) return initial;
	let v = list[0][1];
	for (let i = 1; i < list.length; i++) {
		const [c, val] = list[i];
		v = lerp(v, val, ease(t, cueTime(timing, c), 0.35));
	}
	return v;
};

type Half = {
	src: string;
	from?: {s?: number; x?: number; y?: number};
	to?: {s?: number; x?: number; y?: number};
	focus?: [Cue, number][];
	kicker?: string;
	kickerAt?: Cue;
	text?: string;
	textAt?: Cue;
	stamp?: string;
	stampAt?: Cue;
	heard?: string;
	heardAt?: Cue;
	labelY: number;
	labelX?: number;
	align?: 'left' | 'right';
};

/**
 * Split frame: `halves` (top, bottom) each show a plate (`src` under public/) inside their half, framed by
 * `from`/`to` {s, x, y} across the shot (s scales the full 1080×1920 plate; x/y shift it from the half's centre).
 * `seam` is the dividing y; it draws left to right from `seamAt` over `seamDur`. Each half can dim (`focus` steps,
 * 1 = lit, 0.4 = dimmed) and carries a label block at `labelY`: amber caps `kicker`, serif `text`, a rust `stamp`
 * slammed beside the text, and a rust italic `heard` line (what that side understood). Use with `local: true` on a
 * shot with `plateMotion: "still"` so the loop tail can redraw it.
 */
export const SplitFrame: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const seam: number = g.seam ?? H / 2;
	const tSeam = cueTime(timing, g.seamAt, span.start);
	const seamP = ez(t, tSeam, g.seamDur ?? 0.6, Easing.inOut(Easing.cubic));
	const p = interpolate(t, [span.start, span.end], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const halves: Half[] = g.halves;
	return (
		<AbsoluteFill style={{background: '#05080a'}}>
			{halves.map((h, i) => {
				const top = i === 0 ? 0 : seam;
				const hh = i === 0 ? seam : H - seam;
				const s = lerp(h.from?.s ?? 1, h.to?.s ?? h.from?.s ?? 1, p);
				const x = lerp(h.from?.x ?? 0, h.to?.x ?? h.from?.x ?? 0, p);
				const y = lerp(h.from?.y ?? 0, h.to?.y ?? h.from?.y ?? 0, p);
				const lit = steps(timing, t, h.focus);
				return (
					<div key={i} style={{position: 'absolute', left: 0, top, width: W, height: hh, overflow: 'hidden'}}>
						<Img
							src={staticFile(h.src)}
							style={{position: 'absolute', left: 0, top: hh / 2 - H / 2, width: W, height: H, transform: `translate(${x}px, ${y}px) scale(${s})`, transformOrigin: '50% 50%'}}
						/>
						<AbsoluteFill style={{background: '#070b10', opacity: (1 - lit) * 0.85}} />
						{/* Dark band behind the label block, in as soon as any of its parts arrives. */}
						<div
							style={{
								position: 'absolute',
								left: 0,
								right: 0,
								top: h.labelY - top - 70,
								height: 330,
								background: 'linear-gradient(180deg, rgba(5,8,10,0) 0%, rgba(5,8,10,0.6) 28%, rgba(5,8,10,0.6) 62%, rgba(5,8,10,0) 100%)',
								opacity: Math.max(...[h.kickerAt, h.textAt, h.heardAt].map((c) => (c ? ez(t, cueTime(timing, c) - 0.2, 0.4) : 0))),
							}}
						/>
						{/* Soft shade on the seam side so each half reads as its own picture. */}
						<AbsoluteFill style={{background: `linear-gradient(${i === 0 ? '0deg' : '180deg'}, rgba(5,8,10,0.55) 0%, rgba(5,8,10,0) 18%)`}} />
					</div>
				);
			})}
			{/* Seam: the border, an amber hairline with a centre diamond, drawn left to right. */}
			<div style={{position: 'absolute', left: 0, top: seam - 3, width: W * seamP, height: 6, background: '#05080a'}} />
			<div style={{position: 'absolute', left: 0, top: seam - 1, width: W * seamP, height: 2, background: palette.amber, boxShadow: '0 0 12px rgba(233,169,75,0.6)'}} />
			<div
				style={{
					position: 'absolute',
					left: W / 2 - 11,
					top: seam - 11,
					width: 22,
					height: 22,
					background: '#05080a',
					border: `2px solid ${palette.amber}`,
					transform: `rotate(45deg) scale(${ez(t, tSeam + (g.seamDur ?? 0.6) * 0.5, 0.3, Easing.out(Easing.back(2)))})`,
				}}
			/>
			{halves.map((h, i) => <HalfLabel key={i} h={h} t={t} timing={timing} />)}
		</AbsoluteFill>
	);
};

const HalfLabel: React.FC<{h: Half; t: number; timing: Timing}> = ({h, t, timing}) => {
	const at = (c?: Cue) => (c ? cueTime(timing, c) : Infinity);
	const k = ez(t, at(h.kickerAt), 0.4);
	const tx = ez(t, at(h.textAt), 0.45);
	const st = ez(t, at(h.stampAt), 0.22, Easing.out(Easing.back(2.2)));
	const hd = ez(t, at(h.heardAt), 0.45);
	const right = h.align === 'right';
	return (
		<div style={{position: 'absolute', top: h.labelY, ...(right ? {right: W - (h.labelX ?? 910)} : {left: h.labelX ?? 90}), textAlign: right ? 'right' : 'left'}}>
			{h.kicker && (
				<div
					style={{
						...kicker,
						display: 'inline-block',
						fontSize: 26,
						color: palette.amber,
						border: `1.5px solid ${palette.amber}`,
						padding: '10px 18px 8px',
						background: 'rgba(11,18,22,0.55)',
						clipPath: `inset(0 ${(1 - k) * 100}% 0 0)`,
					}}
				>
					{h.kicker}
				</div>
			)}
			{h.text && (
				<div style={{display: 'flex', alignItems: 'center', justifyContent: right ? 'flex-end' : 'flex-start', gap: 26, marginTop: 10}}>
					<div style={{fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 104, lineHeight: 1.05, color: palette.parchment, opacity: tx, transform: `translateY(${(1 - tx) * 16}px)`, textShadow: shadow}}>
						{h.text}
					</div>
					{h.stamp && (
						<div
							style={{
								...kicker,
								fontSize: 40,
								fontWeight: 800,
								color: palette.rust,
								border: `4px solid ${palette.rust}`,
								padding: '10px 18px 6px',
								background: 'rgba(11,10,10,0.6)',
								opacity: Math.min(1, st * 1.4),
								transform: `rotate(-7deg) scale(${lerp(1.5, 1, Math.min(1, st))})`,
								boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
							}}
						>
							{h.stamp}
						</div>
					)}
				</div>
			)}
			{h.heard && (
				<div style={{marginTop: 14, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 74, lineHeight: 1.05, color: '#e0866a', opacity: hd, transform: `translateY(${(1 - hd) * 14}px)`, textShadow: shadow}}>
					{h.heard}
				</div>
			)}
		</div>
	);
};

type Row = {label: string; cells: [string, string]; at: Cue};

/**
 * Mirror ledger: two culture `columns` under a centre seam that draws down from `start`; each of `rows`
 * ({label, cells: [left, right], at}) lights on its cue, the first row amber (the rule) and later rows parchment
 * (the reason). `clashAt` sends an arrow from each column into the seam with a rust spark; `sum` (two lines, `*`
 * marks ember italic) lands at `sumAt`. Sits in the diagram block (y 340–1150) on `nightSky`.
 */
export const MirrorLedger: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start, span.start);
	const head = ez(t, t0, 0.5);
	const seamP = ez(t, t0 + 0.1, 0.9, Easing.inOut(Easing.cubic));
	const rows: Row[] = g.rows;
	const tClash = cueTime(timing, g.clashAt, Infinity);
	const clash = ez(t, tClash, 0.45, Easing.out(Easing.cubic));
	const spark = ez(t, tClash + 0.3, 0.3, Easing.out(Easing.back(2.5)));
	const sumP = ez(t, cueTime(timing, g.sumAt, Infinity), 0.55);
	const fade = 1 - ez(t, span.end - 0.35, 0.35);
	const cols = [300, 780];
	const rowY = (i: number) => 500 + i * 175;
	const clashY = rowY(rows.length) - 20;
	return (
		<AbsoluteFill style={{opacity: fade}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				<line x1={540} y1={370} x2={540} y2={370 + (clashY - 400) * seamP} stroke={palette.amber} strokeOpacity={0.55} strokeWidth={2} strokeDasharray="10 8" />
				{[0, 1].map((i) => {
					const dir = i === 0 ? 1 : -1;
					const x0 = cols[i];
					const x1 = 540 - dir * 34;
					const xe = lerp(x0, x1, clash);
					return (
						<g key={i} opacity={clash > 0 ? 1 : 0}>
							<line x1={x0} y1={clashY} x2={xe} y2={clashY} stroke={palette.amber} strokeWidth={3} />
							<path d={`M${xe - dir * 16},${clashY - 11} L${xe},${clashY} L${xe - dir * 16},${clashY + 11}`} fill="none" stroke={palette.amber} strokeWidth={3} />
						</g>
					);
				})}
				<g transform={`translate(540 ${clashY}) scale(${spark})`} opacity={Math.min(1, spark)}>
					{Array.from({length: 8}, (_, k) => {
						const a = (k / 8) * Math.PI * 2 + Math.PI / 8;
						return <line key={k} x1={Math.cos(a) * 12} y1={Math.sin(a) * 12} x2={Math.cos(a) * (k % 2 ? 26 : 38)} y2={Math.sin(a) * (k % 2 ? 26 : 38)} stroke={palette.rust} strokeWidth={4} strokeLinecap="round" />;
					})}
					<circle r={7} fill={palette.rust} />
				</g>
			</svg>
			{(g.columns as string[]).map((c, i) => (
				<div key={c} style={{position: 'absolute', top: 370, left: cols[i] - 220, width: 440, textAlign: 'center', ...kicker, fontSize: 34, color: palette.amber, opacity: head, transform: `translateY(${(1 - head) * 10}px)`}}>
					{c}
				</div>
			))}
			{rows.map((r, i) => {
				const a = ez(t, cueTime(timing, r.at), 0.5);
				const y = rowY(i);
				return (
					<React.Fragment key={r.label}>
						<div style={{position: 'absolute', top: y - 60, width: '100%', textAlign: 'center', ...kicker, fontSize: 22, color: palette.fog, opacity: a}}>
							<span style={{background: '#09122a', padding: '0 14px'}}>{r.label}</span>
						</div>
						{r.cells.map((cell, j) => (
							<div
								key={j}
								style={{
									position: 'absolute',
									top: y - 6,
									left: cols[j] - 230,
									width: 460,
									textAlign: 'center',
									fontFamily: fonts.display,
									fontStyle: i === 0 ? 'italic' : undefined,
									fontWeight: 600,
									fontSize: i === 0 ? 64 : 56,
									lineHeight: 1.05,
									color: i === 0 ? palette.ember : palette.parchment,
									opacity: a,
									transform: `translateY(${(1 - a) * 14}px)`,
									textShadow: '0 3px 20px rgba(0,0,0,0.6)',
								}}
							>
								{cell}
							</div>
						))}
					</React.Fragment>
				);
			})}
			<div style={{position: 'absolute', top: clashY + 50, width: '100%', textAlign: 'center'}}>
				{(g.sum as string[]).map((ln, i) => {
					const em = ln.startsWith('*');
					const q = ez(t, cueTime(timing, g.sumAt, Infinity) + i * 0.2, 0.55);
					return (
						<div key={i} style={{fontFamily: fonts.display, fontWeight: 600, fontStyle: em ? 'italic' : undefined, fontSize: em ? 112 : 84, lineHeight: 1.04, color: em ? palette.ember : palette.parchment, opacity: q * sumP, transform: `translateY(${(1 - q) * 18}px)`, textShadow: '0 4px 30px rgba(0,0,0,0.6)'}}>
							{ln.replace(/\*/g, '')}
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};


/*
 * EP11: `shroud`: a linen-wrapped body lying on a bier or table, drawn over a plate when the
 * image model will not paint one (SDXL avoids bodies). Pin with `local: true`.
 */

/**
 * Shroud: `at: [x, y]` = centre of the body's base line, `length` (default 260), `height` (default 44), head end on the
 * `head: "left" | "right"` side, optional `sprigs` (herb count, default 5), `start` cue (else visible from the shot start).
 */
export const Shroud: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const [cx, cy] = g.at;
	const L = g.length ?? 260;
	const h = g.height ?? 44;
	const dir = g.head === 'right' ? -1 : 1;
	const o = g.start ? ease(t, cueTime(timing, g.start), 0.5) : 1;
	const x0 = cx - L / 2;
	// Smooth profile (u 0..1 along the body, head at u=0): round head, neck dip, chest, long body, raised feet.
	const bump = (u: number, c: number, w: number) => Math.exp(-(((u - c) / w) ** 2));
	const prof = (u: number) => Math.min(1, Math.sin((Math.PI / 2) * Math.min(1, u / 0.04, (1 - u) / 0.03)) ** 0.5) *
		(0.8 * bump(u, 0.08, 0.075) + 0.6 * bump(u, 0.3, 0.17) + 0.5 * bump(u, 0.56, 0.24) + 0.4 * bump(u, 0.8, 0.13) + 0.5 * bump(u, 0.94, 0.055));
	const X = (u: number) => (dir > 0 ? x0 + u * L : x0 + (1 - u) * L);
	const N = 80;
	const top = Array.from({length: N + 1}, (_, i) => [X(i / N), cy - Math.min(1, prof(i / N)) * h] as const);
	const d = `M${X(0)},${cy} ` + top.map(([x, y]) => `L${x.toFixed(1)},${y.toFixed(1)}`).join(' ') + ` L${X(1)},${cy} Z`;
	const n = g.sprigs ?? 5;
	return (
		<AbsoluteFill style={{opacity: o * (g.opacity ?? 1)}}>
			<svg width={1080} height={1920} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<linearGradient id="shroud-linen" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor="#fbf5e8" />
						<stop offset="0.45" stopColor="#e6dbc4" />
						<stop offset="1" stopColor="#9c8c70" />
					</linearGradient>
				</defs>
				<ellipse cx={cx} cy={cy + 3} rx={L * 0.55} ry={h * 0.3} fill="rgba(40,26,12,0.5)" style={{filter: 'blur(7px)'}} />
				<path d={d} fill="url(#shroud-linen)" opacity={0.94} style={{filter: 'blur(1.3px)'}} />
				{/* Wrapping bands: soft arcs over the body at intervals. */}
				{[0.16, 0.28, 0.4, 0.52, 0.64, 0.76, 0.86].map((u, i) => {
					const x = X(u);
					const y = cy - Math.min(1, prof(u)) * h;
					return <path key={i} d={`M${x - 3 * dir},${cy - 1} Q${x + 7 * dir},${(cy + y) / 2} ${x + 2 * dir},${y + 1}`} stroke="rgba(130,110,80,0.4)" strokeWidth={1.6} style={{filter: 'blur(0.6px)'}} fill="none" />;
				})}
				{Array.from({length: n}, (_, i) => {
					const u = 0.2 + (0.62 * i) / Math.max(1, n - 1);
					const x = X(u);
					const y = cy - Math.min(1, prof(u)) * h + 1;
					return (
						<g key={i} stroke="#5d7a3a" strokeWidth={2.2} strokeLinecap="round" fill="none" opacity={0.9}>
							<path d={`M${x - 14},${y + 3} Q${x},${y - 6} ${x + 14},${y - 2}`} />
							<path d={`M${x - 4},${y - 1} l-5,-8 M${x + 4},${y - 3} l4,-8`} />
						</g>
					);
				})}
			</svg>
		</AbsoluteFill>
	);
};

export const CULTURE: Record<string, React.FC<GraphicProps>> = {
	shroud: Shroud,
	splitFrame: SplitFrame,
	mirrorLedger: MirrorLedger,
};
