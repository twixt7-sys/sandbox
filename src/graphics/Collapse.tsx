import React from 'react';
import {AbsoluteFill, Easing, Img, random, staticFile} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Collapse graphics (EP19, Arc 4): an empire's strains drawn as one feedback loop. Each strain is a medallion (cut from
 * its plate) on a ring around the empire's seal; arrows join them and the last arrow closes the loop. A pulse then runs
 * round faster and faster, and every time it passes a strain a crack spreads through the seal, until one ordinary event
 * splits the seal in two. A matching tag numbers each strain as a crack as we meet it.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

type Node = {label: string; note?: string; src?: string; x?: number; y?: number; zoom?: number};

/** A small cracked-disc glyph (the series' crack mark), drawn in `c`. */
export const CrackGlyph: React.FC<{c: string; size?: number}> = ({c, size = 30}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth={1.8} strokeLinejoin="round" strokeLinecap="round">
		<circle cx={12} cy={12} r={9.5} />
		<path d="M12 2.5 L10.5 8 L13.5 11 L10 15.5 L12 21.5" />
		<path d="M13.5 11 L18 12.5" strokeWidth={1.3} />
	</svg>
);

/** Angle the pulse has travelled `tau` s after the spin starts: speed w0·e^(k·tau), so θ = w0/k·(e^(k·tau) − 1). */
const travelled = (tau: number, w0: number, k: number) => (tau <= 0 ? 0 : (w0 / k) * (Math.exp(k * tau) - 1));

/** Point on a circle at angle `a` (0 = up, clockwise). */
const polar = (cx: number, cy: number, r: number, a: number): [number, number] => [cx + r * Math.sin(a), cy - r * Math.cos(a)];

/** A jagged crack from the seal's centre towards angle `a`, as a polyline of `steps` points. */
const crackPath = (cx: number, cy: number, r: number, a: number, seed: number, steps = 6) => {
	const pts: [number, number][] = [[cx, cy]];
	for (let s = 1; s <= steps; s++) {
		const f = s / steps;
		const wob = (random(`${seed}-${s}`) - 0.5) * 0.5;
		pts.push(polar(cx, cy, r * f, a + wob * (1 - f * 0.4)));
	}
	return pts;
};

/** The empire's seal: an invented gate-tower device inside two rings, with the empire's name beneath. */
const SealFace: React.FC<{r: number; label: string}> = ({r, label}) => (
	<g>
		<circle r={r} fill="#1c2329" stroke={palette.amber} strokeWidth={3} />
		<circle r={r - 12} fill="none" stroke={palette.amber} strokeOpacity={0.45} strokeWidth={1.5} />
		{Array.from({length: 24}, (_, i) => {
			const [x, y] = polar(0, 0, r - 6, (i / 24) * Math.PI * 2);
			return <circle key={i} cx={x} cy={y} r={1.8} fill={palette.amber} fillOpacity={0.6} />;
		})}
		{/* Gate tower: three merlons, a body, an arched door, two side lights. */}
		<g transform={`translate(0 ${-r * 0.2}) scale(${r / 118})`} fill="none" stroke={palette.ember} strokeWidth={3} strokeLinejoin="round">
			<path d="M-34 34 V-18 H-24 V-30 H-12 V-18 H-6 V-30 H6 V-18 H12 V-30 H24 V-18 H34 V34 Z" fill="rgba(244,196,110,0.12)" />
			<path d="M-12 34 V8 A12 12 0 0 1 12 8 V34" />
			<path d="M-22 -4 V4 M22 -4 V4" />
			<path d="M-52 34 H52" />
		</g>
		<text y={r * 0.5} textAnchor="middle" fill={palette.parchment} style={{...kicker, fontWeight: 800, fontSize: 22 * (r / 118), letterSpacing: '0.28em'}}>
			{label}
		</text>
	</g>
);

/**
 * CrackLoop: `nodes: [{label, note, src, x, y, zoom}]` on a ring of `radius` round `center`, clockwise from the top,
 * around the empire's seal (`label` = its name). Medallions pop in on `nodesAt[i]` (portraits cut from `src` centred on
 * plate point x, y at `zoom`); arrow i (node i → i+1) draws on `arrowsAt[i]`; the closing arrow (last → first) draws in
 * rust on `closeAt`. From `spinAt` a pulse runs round at w0·e^(k·τ) rad/s, lighting each node as it passes, and each pass
 * adds a crack through the seal pointing at that node. `breakAt` splits the seal in two (with `breakLabel`, default
 * TWO HEIRS) and stops the pulse. `liftAt` shrinks the loop up and `lessonKicker` / `lessonText` (*word* = ember
 * italic) land beneath it at `lessonAt`. Sits in the diagram block on `nightSky` over a dimmed plate.
 */
export const CrackLoop: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const nodes: Node[] = g.nodes;
	const n = nodes.length;
	const [cx, cy] = g.center ?? [540, 770];
	const R = g.radius ?? 250;
	const mr = g.medallion ?? 86;
	const sealR = g.sealRadius ?? 112;
	const t0 = cueTime(timing, g.start, span.start);
	const vis = ease(t, t0, 0.45) * out(t, span.end + 0.25, 0.3);
	const nodeT: number[] = (g.nodesAt ?? []).map((c: Cue) => cueTime(timing, c));
	const arrowT: number[] = (g.arrowsAt ?? []).map((c: Cue) => cueTime(timing, c));
	const tClose = g.closeAt ? cueTime(timing, g.closeAt) : 1e9;
	const tSpin = g.spinAt ? cueTime(timing, g.spinAt) : 1e9;
	const tBreak = g.breakAt ? cueTime(timing, g.breakAt) : 1e9;
	const tLift = g.liftAt ? cueTime(timing, g.liftAt) : 1e9;
	const tLesson = g.lessonAt ? cueTime(timing, g.lessonAt) : 1e9;
	const w0 = g.w0 ?? 1.6;
	const k = g.k ?? 0.95;

	// The pulse runs until the break, then coasts to a stop over 0.5 s.
	const brk = ease(t, tBreak, 0.6, Easing.out(Easing.cubic));
	const tauRaw = Math.min(t, tBreak) - tSpin;
	const coast = t > tBreak && tBreak > tSpin ? w0 * Math.exp(k * (tBreak - tSpin)) * 0.25 * brk : 0;
	const theta = travelled(tauRaw, w0, k) + coast;
	const speed = tauRaw > 0 ? w0 * Math.exp(k * tauRaw) : 0;
	const step = (Math.PI * 2) / n;
	const passes = theta / step; // node passes so far (continuous)
	const spinOn = ease(t, tSpin - 0.1, 0.3) * (1 - brk);
	const lift = ease(t, tLift, 0.8);
	const gap = (mr + 16) / R;

	const maxCracks = g.cracks ?? 10;
	const cracks = Array.from({length: maxCracks}, (_, i) => {
		const a = ((i + 1) % n) * step + (random(`crack-${i}`) - 0.5) * 0.7;
		const pts = crackPath(0, 0, sealR * (0.78 + 0.22 * random(`len-${i}`)), a, i);
		return {pts, grow: Math.max(0, Math.min(1, passes - i))};
	});
	// The split: a jagged seam top to bottom; each half slides out and tilts away.
	const seam = Array.from({length: 9}, (_, i): [number, number] => [(random(`seam-${i}`) - 0.5) * 26 * (i % 8 ? 1 : 0), -sealR - 4 + (i / 8) * (sealR * 2 + 8)]);
	const seamD = seam.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');
	const leftClip = `M${-sealR - 20} ${-sealR - 20} L${seam[0][0]} ${-sealR - 20} ${seam.map(([x, y]) => `L${x} ${y}`).join(' ')} L${seam[8][0]} ${sealR + 20} L${-sealR - 20} ${sealR + 20} Z`;
	const rightClip = `M${sealR + 20} ${-sealR - 20} L${seam[0][0]} ${-sealR - 20} ${seam.map(([x, y]) => `L${x} ${y}`).join(' ')} L${seam[8][0]} ${sealR + 20} L${sealR + 20} ${sealR + 20} Z`;
	const apart = lerp(0, g.apart ?? 34, brk);
	const tilt = lerp(0, 7, brk);
	const flash = ease(t, tBreak - 0.04, 0.08) * (1 - ease(t, tBreak + 0.1, 0.5));

	const lessonLines: string[] = Array.isArray(g.lessonText) ? g.lessonText : g.lessonText ? [g.lessonText] : [];
	const lk = ease(t, tLesson, 0.5);
	const top = g.top ?? cy - R - mr - 50;

	const seal = (
		<g>
			<SealFace r={sealR} label={g.label} />
			{cracks.map((c, i) =>
				c.grow > 0 ? (
					<polyline
						key={i}
						points={c.pts.map(([x, y]) => `${x},${y}`).join(' ')}
						fill="none"
						stroke={palette.ember}
						strokeWidth={2.6}
						strokeLinejoin="round"
						strokeLinecap="round"
						pathLength={1}
						strokeDasharray={`${c.grow} 1`}
						style={{filter: 'drop-shadow(0 0 5px rgba(244,196,110,0.9))'}}
					/>
				) : null,
			)}
		</g>
	);

	return (
		<AbsoluteFill style={{opacity: vis}}>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse 80% 60% at 50% 42%, rgba(7,14,30,0.5) 0%, rgba(7,14,30,0.82) 100%)'}} />
			<AbsoluteFill style={{transform: `translateY(${lerp(0, g.liftY ?? 0, lift)}px) scale(${lerp(1, g.liftScale ?? 0.64, lift)})`, transformOrigin: `${cx}px ${top}px`}}>
				<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					<defs>
						<marker id="crackArrow" viewBox="0 0 10 10" refX={6} refY={5} markerWidth={5} markerHeight={5} orient="auto-start-reverse">
							<path d="M0 0 L10 5 L0 10 Z" fill={palette.amber} />
						</marker>
						<marker id="crackArrowRust" viewBox="0 0 10 10" refX={6} refY={5} markerWidth={5} markerHeight={5} orient="auto-start-reverse">
							<path d="M0 0 L10 5 L0 10 Z" fill={palette.rust} />
						</marker>
					</defs>
					{/* Faint guide ring under the arrows. */}
					<circle cx={cx} cy={cy} r={R} fill="none" stroke={palette.fog} strokeOpacity={0.12 * ease(t, t0, 0.6)} strokeWidth={1.5} strokeDasharray="4 10" />
					{nodes.map((_, i) => {
						const last = i === n - 1;
						const at = last ? tClose : arrowT[i] ?? 1e9;
						const p = ease(t, at, last ? 0.7 : 0.45);
						if (p <= 0) return null;
						const a0 = i * step + gap;
						const a1 = (i + 1) * step - gap;
						const [x0, y0] = polar(cx, cy, R, a0);
						const [x1, y1] = polar(cx, cy, R, a1);
						const heat = Math.min(1, speed / 9);
						const col = last ? palette.rust : palette.amber;
						return (
							<path
								key={i}
								d={`M${x0} ${y0} A${R} ${R} 0 0 1 ${x1} ${y1}`}
								fill="none"
								stroke={col}
								strokeWidth={(last ? 5 : 4) + 2 * heat * (1 - brk)}
								strokeLinecap="round"
								pathLength={1}
								strokeDasharray={`${p} 1`}
								markerEnd={p > 0.98 ? `url(#${last ? 'crackArrowRust' : 'crackArrow'})` : undefined}
								opacity={lerp(1, 0.45, brk)}
								style={{filter: last ? `drop-shadow(0 0 ${6 + 10 * (1 - ease(t, tClose + 0.6, 0.8))}px rgba(185,84,58,0.9))` : undefined}}
							/>
						);
					})}
					{/* The pulse: a bright head with a trail that lengthens with speed. */}
					{spinOn > 0 &&
						(() => {
							const trail = Math.min(1.6, 0.18 + speed * 0.09);
							const a1 = theta;
							const a0 = theta - trail;
							const [hx, hy] = polar(cx, cy, R, a1);
							const [sx, sy] = polar(cx, cy, R, a0);
							return (
								<g opacity={spinOn}>
									<path d={`M${sx} ${sy} A${R} ${R} 0 ${trail > Math.PI ? 1 : 0} 1 ${hx} ${hy}`} fill="none" stroke={palette.ember} strokeOpacity={0.55} strokeWidth={9} strokeLinecap="round" style={{filter: 'blur(3px)'}} />
									<circle cx={hx} cy={hy} r={11} fill={palette.ember} style={{filter: 'drop-shadow(0 0 14px rgba(244,196,110,1))'}} />
								</g>
							);
						})()}
					{/* The seal, whole or split. */}
					<g transform={`translate(${cx} ${cy})`} opacity={ease(t, t0 + 0.1, 0.5)}>
						<clipPath id="sealL">
							<path d={leftClip} />
						</clipPath>
						<clipPath id="sealR">
							<path d={rightClip} />
						</clipPath>
						<g transform={`translate(${-apart} ${apart * 0.25}) rotate(${-tilt})`} clipPath="url(#sealL)">
							{seal}
						</g>
						<g transform={`translate(${apart} ${apart * 0.25}) rotate(${tilt})`} clipPath="url(#sealR)">
							{seal}
						</g>
						{brk > 0 && <path d={seamD} fill="none" stroke={palette.rust} strokeWidth={3} opacity={flash} style={{filter: 'drop-shadow(0 0 12px rgba(185,84,58,1))'}} />}
					</g>
				</svg>
				{g.breakAt && (
					<div style={{position: 'absolute', top: cy + sealR + 18, width: '100%', textAlign: 'center', ...kicker, fontWeight: 800, fontSize: 26, color: palette.rust, opacity: ease(t, tBreak + 0.1, 0.4), textShadow: '0 2px 10px rgba(0,0,0,0.9)'}}>
						{g.breakLabel ?? 'Two heirs'}
					</div>
				)}
				{nodes.map((nd, i) => {
					const a = i * step;
					const [x, y] = polar(cx, cy, R, a);
					const pop = ease(t, nodeT[i] ?? t0, 0.45, Easing.out(Easing.back(1.4)));
					// Lit when the pulse passes (the fractional part of passes - i, near 0).
					const since = passes - i;
					const lap = since - Math.floor(since);
					const lit = spinOn * (since >= 0 ? Math.max(0, 1 - lap * 3) : 0);
					const z = nd.zoom ?? 0.32;
					const below = y > cy - R * 0.5;
					const dim = lerp(1, 0.55, brk);
					return (
						<React.Fragment key={i}>
							<div
								style={{
									position: 'absolute',
									left: x - mr,
									top: y - mr,
									width: mr * 2,
									height: mr * 2,
									borderRadius: '50%',
									overflow: 'hidden',
									border: `3px solid ${lit > 0.05 ? palette.ember : palette.amber}`,
									boxShadow: `0 0 ${10 + 30 * lit}px rgba(244,196,110,${0.25 + 0.6 * lit}), inset 0 0 22px rgba(0,0,0,0.65)`,
									transform: `scale(${Math.max(0.001, pop) * (1 + 0.06 * lit)}) translateY(${brk * (i % 2 ? 10 : 6)}px)`,
									opacity: Math.min(1, pop * 1.5),
									background: '#1c2329',
								}}
							>
								{nd.src && (
									<Img
										src={staticFile(nd.src)}
										style={{position: 'absolute', width: 1080 * z, height: 1920 * z, left: mr - (nd.x ?? 540) * z, top: mr - (nd.y ?? 960) * z, filter: `saturate(${0.85 * dim}) brightness(${dim + 0.25 * lit})`}}
									/>
								)}
								<div style={{position: 'absolute', inset: 0, borderRadius: '50%', boxShadow: 'inset 0 0 22px rgba(0,0,0,0.65)'}} />
							</div>
							<div
								style={{
									position: 'absolute',
									left: x - 170,
									width: 340,
									top: below ? y + mr + 10 : y - mr - 46,
									textAlign: 'center',
									...kicker,
									fontWeight: 800,
									fontSize: 25,
									letterSpacing: '0.16em',
									color: lit > 0.05 ? palette.parchment : palette.ember,
									opacity: Math.min(1, pop * 1.5) * lerp(1, 0.7, brk),
									textShadow: '0 1px 4px #000, 0 0 14px rgba(0,0,0,0.95)',
								}}
							>
								{nd.label}
							</div>
						</React.Fragment>
					);
				})}
			</AbsoluteFill>
			{lessonLines.length > 0 && (
				<div style={{position: 'absolute', top: g.lessonTop ?? 900, left: 60, right: 60, textAlign: 'center', opacity: lk, transform: `translateY(${(1 - lk) * 16}px)`}}>
					{g.lessonKicker && <div style={{...kicker, fontSize: 30, color: palette.amber, textShadow: '0 2px 12px rgba(0,0,0,0.9)'}}>{g.lessonKicker}</div>}
					{lessonLines.map((ln, li) => {
						const lp = ease(t, tLesson + 0.15 + li * 0.25, 0.6);
						return (
							<div key={li} style={{marginTop: li ? 0 : 14, fontFamily: fonts.display, fontWeight: 600, fontSize: g.lessonSize ?? 92, lineHeight: 1.04, color: palette.parchment, opacity: lp, textShadow: '0 4px 30px rgba(0,0,0,0.8)'}}>
								{ln.split(' ').map((w, k2) => (
									<span key={k2} style={w.startsWith('*') ? {color: palette.ember, fontStyle: 'italic'} : undefined}>
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

/** Strain tag: like `tag`, with a cracked-disc glyph and numeral ("CRACK I · FAMINE") so each strain reads as one crack in the loop. */
export const CrackTag: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start, span.start);
	const a = ease(t, t0, 0.5);
	const b = ease(t, t0 + 0.15, 0.6);
	const o = out(t, span.end, 0.3);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: g.top ?? 336, left: 90}}>
				<div style={{display: 'inline-flex', alignItems: 'center', gap: 12, ...kicker, fontSize: 26, color: palette.amber, border: `1.5px solid ${palette.amber}`, padding: '8px 18px 6px 12px', background: 'rgba(11,18,22,0.5)', clipPath: `inset(0 ${(1 - a) * 100}% 0 0)`}}>
					<CrackGlyph c={palette.amber} size={30} />
					<span>
						{g.word ?? 'Crack'} {g.numeral} · <span style={{color: palette.ember}}>{g.kicker}</span>
					</span>
				</div>
				<div style={{marginTop: 16, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 500, fontSize: 64, color: palette.parchment, opacity: b, transform: `translateY(${(1 - b) * 14}px)`, textShadow: '0 3px 24px rgba(0,0,0,0.7)'}}>
					{g.text}
				</div>
			</div>
		</AbsoluteFill>
	);
};

export const COLLAPSE: Record<string, React.FC<GraphicProps>> = {
	crackLoop: CrackLoop,
	crackTag: CrackTag,
};
