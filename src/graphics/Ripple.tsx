import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, palette} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Ripple graphics (EP22, Arc 5): one cheap ability followed outward into society. Free healing is drawn in code as a
 * soft jade glow under a hand (`mendGlow`, pinned to the plate with `"local": true`); its consequences spread from that
 * point as concentric rings on a city map (`rippleMap`), each ring lighting one changed institution, and the last,
 * dashed ring finds the one death the magic can't explain. `ringTag` numbers each consequence as we meet it.
 */

/** EP22's motif colour: the mending light. */
export const MEND = '#a6e3c4';
const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const tone = (c: string | undefined, fallback: string) => (c ? ((palette as Record<string, string>)[c] ?? c) : fallback);

/**
 * MendGlow: the healing touch at plate point `at: [x, y]`. The glow (radius `r`, default 70) warms in from `start` and
 * breathes; each cue in `pulses` brightens it and sends one ring out to `ringMax` px (default 260) over `ringDur` s.
 * `core: false` draws only the rings (a wave sweeping across a plate from an off-frame origin, `ringFrom` px to start).
 * `failAt` makes the glow gutter (two flickers) and go out, leaving a faint rust ember: the one it couldn't save.
 * Sparks rise from the core while it's lit. Pin it with `"local": true`.
 */
export const MendGlow: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [x, y] = g.at;
	const r = g.r ?? 70;
	const c = tone(g.color, MEND);
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.2;
	const pulses: number[] = (g.pulses ?? []).map((q: Cue) => cueTime(timing, q));
	const tFail = g.failAt ? cueTime(timing, g.failAt) : Infinity;
	const ringMax = g.ringMax ?? 260;
	const ringDur = g.ringDur ?? 1.2;
	const ringFrom = g.ringFrom ?? r * 0.6;
	const vis = out(t, tEnd, 0.35);
	// Gutter: two quick dips, then out over 0.7 s.
	const fail = Number.isFinite(tFail)
		? Math.max(0, 1 - ease(t, tFail + 0.45, 0.7)) * (t > tFail && t < tFail + 0.12 ? 0.35 : 1) * (t > tFail + 0.24 && t < tFail + 0.33 ? 0.5 : 1)
		: 1;
	const ember = Number.isFinite(tFail) ? ease(t, tFail + 0.6, 0.6) * 0.7 : 0;
	const warm = g.core === false ? 0 : ease(t, t0, 0.7);
	const boost = pulses.reduce((m, p) => Math.max(m, t >= p ? Math.exp(-(t - p) * 2.2) : 0), 0);
	const breathe = 0.85 + 0.15 * Math.sin(t * 2 * Math.PI * 0.55);
	const core = warm * fail * (breathe + 0.6 * boost);
	const id = `mend-${Math.round(x)}-${Math.round(y)}`;
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			<svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<radialGradient id={id}>
						<stop offset="0%" stopColor="#f4fff8" stopOpacity={0.95} />
						<stop offset="22%" stopColor={c} stopOpacity={0.75} />
						<stop offset="60%" stopColor={c} stopOpacity={0.18} />
						<stop offset="100%" stopColor={c} stopOpacity={0} />
					</radialGradient>
				</defs>
				{core > 0.001 && (
					<g style={{mixBlendMode: 'screen'}}>
						<circle cx={x} cy={y} r={r * (2.2 + 0.5 * boost)} fill={`url(#${id})`} opacity={core * 0.55} />
						<circle cx={x} cy={y} r={r} fill={`url(#${id})`} opacity={Math.min(1, core)} />
						{Array.from({length: 9}, (_, i) => {
							const period = 1.6 + (i % 3) * 0.35;
							const ph = ((t + i * 0.37) % period) / period;
							const sx = x + Math.sin(i * 2.3) * r * 0.7 + Math.sin(t * 1.3 + i) * 8;
							const sy = y - ph * r * 2.1;
							return <circle key={i} cx={sx} cy={sy} r={2.2 + (i % 2)} fill="#f4fff8" opacity={core * Math.sin(ph * Math.PI) * 0.8} />;
						})}
					</g>
				)}
				{ember > 0 && <circle cx={x} cy={y} r={r * 0.35} fill={palette.rust} opacity={ember * 0.45} style={{filter: 'blur(10px)'}} />}
				{pulses.map((p, i) => {
					const q = ease(t, p, ringDur, Easing.out(Easing.cubic));
					if (t < p || q >= 1) return null;
					return <circle key={i} cx={x} cy={y} r={lerp(ringFrom, ringMax, q)} fill="none" stroke={c} strokeWidth={lerp(g.ringWidth ?? 5, 1, q)} opacity={(1 - q) * 0.9} style={{filter: `drop-shadow(0 0 8px ${c})`}} />;
				})}
			</svg>
		</AbsoluteFill>
	);
};

type Ring = {r: number; at: Cue; kicker: string; label?: string; angle?: number; side?: 'left' | 'right'; lost?: boolean};

/** Concentric-ring glyph; ring `hi` (1-based) drawn in `hc`. The series' ripple mark. */
export const RingGlyph: React.FC<{c: string; hc?: string; hi?: number; size?: number}> = ({c, hc, hi = 0, size = 30}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none" strokeWidth={1.6}>
		<circle cx={12} cy={12} r={2} fill={c} stroke="none" />
		{[5, 8, 11].map((rr, i) => (
			<circle key={rr} cx={12} cy={12} r={rr} stroke={i + 1 === hi ? (hc ?? c) : c} strokeOpacity={i + 1 === hi ? 1 : 0.45} strokeWidth={i + 1 === hi ? 2.2 : 1.4} />
		))}
	</svg>
);

/**
 * RippleMap: rings of consequence spreading from `origin: [x, y]`. `rings: [{r, at, kicker, label, angle, side, lost}]`:
 * at `at` a bright wavefront runs out to radius `r` and settles as a thin jade ring; a pin lights where it lands
 * (`angle` in degrees, 0 = right, -90 = up) with an amber kicker and a serif italic `label`, set to the `side` of the
 * pin (default: away from centre). A `lost` ring is a dashed mist circle with a rust "?" pin and rust kicker.
 * `idle` sends a faint ring out every 1.6 s from `start`. `instant` shows every ring settled from the start (a recap).
 * `liftAt` moves the whole map to `lift: {to: [x, y], s}` to make room, and `lessonKicker` / `lessonText` (string or
 * lines; *word* = ember italic) land at `lessonTop` (default 960) on `lessonAt`. Usable local or as an overlay.
 */
export const RippleMap: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [ox, oy] = g.origin;
	const rings: Ring[] = g.rings;
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.25;
	const vis = (g.instant ? 1 : ease(t, t0, 0.4)) * out(t, tEnd, 0.3);
	const tLift = g.liftAt ? cueTime(timing, g.liftAt) : Infinity;
	const lift = Number.isFinite(tLift) ? ease(t, tLift, 0.8) : 0;
	const [lx, ly] = g.lift?.to ?? [ox, oy];
	const ls = lerp(1, g.lift?.s ?? 1, lift);
	const tLesson = g.lessonAt ? cueTime(timing, g.lessonAt) : Infinity;
	const lk = Number.isFinite(tLesson) ? ease(t, tLesson, 0.5) : 0;
	const lessonLines: string[] = Array.isArray(g.lessonText) ? g.lessonText : g.lessonText ? [g.lessonText] : [];
	const idle = g.idle ? Array.from({length: 24}, (_, i) => t0 + i * 1.6).filter((p) => p <= t && t - p < 2.4) : [];
	const tx = (lx - ox) * lift;
	const ty = (ly - oy) * lift;
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', inset: 0, transform: `translate(${tx}px, ${ty}px) scale(${ls})`, transformOrigin: `${ox}px ${oy}px`}}>
				<svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					{idle.map((p) => {
						const q = Math.min(1, (t - p) / 2.4);
						return <circle key={p} cx={ox} cy={oy} r={lerp(20, rings[0]?.r ?? 160, q)} fill="none" stroke={MEND} strokeWidth={2} opacity={(1 - q) * 0.5} />;
					})}
					<circle cx={ox} cy={oy} r={9} fill={MEND} style={{filter: `drop-shadow(0 0 10px ${MEND})`}} />
					{rings.map((rg, i) => {
						const ta = g.instant ? -1e9 : cueTime(timing, rg.at);
						const run = ease(t, ta, 0.9, Easing.out(Easing.cubic));
						if (run <= 0) return null;
						const flash = g.instant ? 0 : Math.exp(-Math.max(0, t - ta - 0.6) * 3) * (t >= ta ? 1 : 0);
						const c = rg.lost ? palette.mist : MEND;
						return (
							<g key={i}>
								<circle cx={ox} cy={oy} r={rg.r * run} fill="none" stroke={c} strokeWidth={rg.lost ? 3 : 3.5} strokeDasharray={rg.lost ? '14 12' : undefined} opacity={0.75} style={{filter: rg.lost ? undefined : `drop-shadow(0 0 6px ${MEND})`}} />
								{flash > 0.01 && <circle cx={ox} cy={oy} r={rg.r * run} fill="none" stroke="#f4fff8" strokeWidth={9 * flash} opacity={0.6 * flash} />}
							</g>
						);
					})}
				</svg>
				{rings.map((rg, i) => {
					const ta = g.instant ? -1e9 : cueTime(timing, rg.at);
					const pin = g.instant ? 1 : ease(t, ta + 0.55, 0.4, Easing.out(Easing.back(1.8)));
					const txt = g.instant ? 1 : ease(t, ta + 0.7, 0.45);
					if (pin <= 0) return null;
					const a = ((rg.angle ?? -90) * Math.PI) / 180;
					const px = ox + Math.cos(a) * rg.r;
					const py = oy + Math.sin(a) * rg.r;
					const side = rg.side ?? (Math.cos(a) >= 0 ? 'right' : 'left');
					const kc = rg.lost ? palette.rust : palette.amber;
					return (
						<React.Fragment key={i}>
							<div
								style={{
									position: 'absolute',
									left: px - 22,
									top: py - 22,
									width: 44,
									height: 44,
									borderRadius: 22,
									transform: `scale(${pin})`,
									background: rg.lost ? 'rgba(11,18,22,0.85)' : 'rgba(11,18,22,0.75)',
									border: `3px ${rg.lost ? 'dashed' : 'solid'} ${rg.lost ? palette.rust : MEND}`,
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
									fontFamily: fonts.display,
									fontWeight: 700,
									fontSize: 30,
									color: rg.lost ? palette.rust : MEND,
									boxShadow: rg.lost ? undefined : `0 0 18px ${MEND}`,
								}}
							>
								{rg.lost ? '?' : ''}
							</div>
							<div
								style={{
									position: 'absolute',
									top: py - 34,
									...(side === 'right' ? {left: px + 36} : {right: 1080 - px + 36}),
									textAlign: side === 'right' ? 'left' : 'right',
									opacity: txt,
									transform: `translateY(${(1 - txt) * 10}px)`,
									whiteSpace: 'nowrap',
								}}
							>
								<div style={{...kicker, fontSize: 27, color: kc, textShadow: '0 2px 10px rgba(0,0,0,0.95)'}}>{rg.kicker}</div>
								{rg.label && (
									<div style={{marginTop: 4, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 50, lineHeight: 1.05, color: palette.parchment, textShadow: '0 2px 16px rgba(0,0,0,0.95), 0 0 4px rgba(0,0,0,0.8)'}}>{rg.label}</div>
								)}
							</div>
						</React.Fragment>
					);
				})}
			</div>
			{lessonLines.length > 0 && (
				<div style={{position: 'absolute', top: g.lessonTop ?? 960, left: 60, right: 60, textAlign: 'center', opacity: lk, transform: `translateY(${(1 - lk) * 16}px)`}}>
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

/** Consequence tag: like `tag`, with a ring glyph ("RING II · WAR"); ring `numeral` lit in ember. `lost: true` turns it rust. */
export const RingTag: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start, span.start);
	const a = ease(t, t0, 0.5);
	const b = ease(t, t0 + 0.15, 0.6);
	const o = out(t, g.end ? cueTime(timing, g.end) : span.end, 0.3);
	const c = g.lost ? palette.rust : palette.amber;
	const romans = ['I', 'II', 'III', 'IV', 'V'];
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: g.top ?? 336, left: 90}}>
				<div style={{display: 'inline-flex', alignItems: 'center', gap: 12, ...kicker, fontSize: 26, color: c, border: `1.5px ${g.lost ? 'dashed' : 'solid'} ${c}`, padding: '8px 18px 6px 12px', background: 'rgba(11,18,22,0.55)', clipPath: `inset(0 ${(1 - a) * 100}% 0 0)`}}>
					<RingGlyph c={c} hc={g.lost ? palette.rust : MEND} hi={romans.indexOf(g.numeral) + 1} size={30} />
					<span>
						Ring {g.numeral} · <span style={{color: g.lost ? palette.rust : palette.ember}}>{g.kicker}</span>
					</span>
				</div>
				<div style={{marginTop: 16, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 500, fontSize: 64, color: palette.parchment, opacity: b, transform: `translateY(${(1 - b) * 14}px)`, textShadow: '0 3px 24px rgba(0,0,0,0.8)'}}>
					{g.text}
				</div>
			</div>
		</AbsoluteFill>
	);
};

export const RIPPLE: Record<string, React.FC<GraphicProps>> = {
	mendGlow: MendGlow,
	rippleMap: RippleMap,
	ringTag: RingTag,
};
