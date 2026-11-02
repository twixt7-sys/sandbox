import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Pillar graphics (EP17, Arc 4): an empire drawn as a roof on pillars. The pillars rise as plain stone, then each one
 * turns out to be a person (a portrait cut from their plate) with the reason they hold it up; an absent alternative is an
 * empty, dashed pillar. A matching tag numbers each supporter as we meet them.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const STONE = 'repeating-linear-gradient(90deg, #4b555c 0px, #5f6a71 9px, #3d464c 13px, #4b555c 22px)';

type Pillar = {label: string; who?: string; src?: string; x?: number; y?: number; zoom?: number; empty?: boolean};

/** A small fluted column glyph (the series' pillar mark), drawn in `c`. */
export const PillarGlyph: React.FC<{c: string; size?: number}> = ({c, size = 30}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth={1.8} strokeLinejoin="round">
		<path d="M3 4 H21 L19 6.5 H5 Z" fill={c} fillOpacity={0.35} />
		<path d="M6.5 6.5 V18.5 M10.5 6.5 V18.5 M13.5 6.5 V18.5 M17.5 6.5 V18.5" />
		<path d="M4.5 18.5 H19.5 V21 H4.5 Z" fill={c} fillOpacity={0.35} />
	</svg>
);

/**
 * PillarStack: `label` on the entablature (rust caps), `pillars: [{label, src, x, y, zoom} | {label, empty: true}]`.
 * The roof shows from `start` (else the shot start); the pillars rise as stone from `riseAt`, staggered. `peopleAt[i]`
 * turns pillar i into its supporter: a portrait cut from `src` centred on plate point (x, y) at `zoom`, with its label;
 * an `empty` pillar fades to a dashed outline instead. `liftAt` shrinks the whole stack up to make room, and
 * `lessonKicker` / `lessonText` (string or lines; *word* = ember italic) land beneath it at `lessonAt`.
 * Geometry: pediment from `top` (default 380), pillars `pillarTop`..`pillarBase`, 5 pillars across x 162–918.
 */
export const PillarStack: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const pillars: Pillar[] = g.pillars;
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end, span.end) : span.end;
	const vis = (g.instant ? 1 : ease(t, t0, 0.45)) * out(t, Math.min(tEnd, span.end + 0.25), 0.3);
	const tRise = cueTime(timing, g.riseAt, -1e9);
	const people: number[] = (g.peopleAt ?? []).map((c: Cue) => cueTime(timing, c));
	const tLift = g.liftAt ? cueTime(timing, g.liftAt) : 1e9;
	const tLesson = g.lessonAt ? cueTime(timing, g.lessonAt) : 1e9;
	const lift = ease(t, tLift, 0.8);

	const top = g.top ?? 380;
	const beamTop = top + 96;
	const beamH = 78;
	const capTop = beamTop + beamH + 8;
	const pillarBase = g.pillarBase ?? 1090;
	const shaftTop = capTop + 30;
	const shaftH = pillarBase - 26 - shaftTop;
	const n = pillars.length;
	const pw = g.pillarWidth ?? 132;
	const gap = (756 - n * pw) / Math.max(1, n - 1);
	const x0 = 540 - 378;
	const roof = ease(t, t0 + 0.05, 0.6);

	const lessonLines: string[] = Array.isArray(g.lessonText) ? g.lessonText : g.lessonText ? [g.lessonText] : [];
	const lk = ease(t, tLesson, 0.5);

	return (
		<AbsoluteFill style={{opacity: vis}}>
			{/* Deep midnight under the diagram so the dimmed plate only hints at the palace. */}
			<AbsoluteFill style={{background: 'radial-gradient(ellipse 80% 60% at 50% 45%, rgba(7,14,30,0.55) 0%, rgba(7,14,30,0.82) 100%)'}} />
			<AbsoluteFill style={{transform: `translateY(${lerp(0, (g.liftY ?? 0), lift)}px) scale(${lerp(1, g.liftScale ?? 0.7, lift)})`, transformOrigin: `540px ${top - 20}px`}}>
				{/* Pediment + entablature: the empire itself. */}
				<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible', opacity: roof}}>
					<path d={`M${x0 - 22} ${beamTop} L540 ${top} L${x0 + 778} ${beamTop} Z`} fill="#20262c" stroke={palette.amber} strokeWidth={2.5} strokeLinejoin="round" />
					<path d={`M${x0 + 40} ${beamTop - 10} L540 ${top + 30} L${x0 + 716} ${beamTop - 10}`} fill="none" stroke={palette.amber} strokeOpacity={0.35} strokeWidth={1.5} />
					<rect x={x0 - 22} y={beamTop} width={800} height={beamH} fill="#2a3138" stroke={palette.amber} strokeWidth={2.5} />
					<rect x={x0 - 8} y={beamTop + beamH} width={772} height={8} fill="#343c43" stroke={palette.amber} strokeOpacity={0.6} strokeWidth={1.5} />
					{/* Stylobate: the ground the pillars stand on. */}
					<rect x={x0 - 30} y={pillarBase} width={816} height={16} fill="#2a3138" stroke={palette.amber} strokeOpacity={0.7} strokeWidth={2} opacity={ease(t, tRise - 0.3, 0.4)} />
				</svg>
				<div style={{position: 'absolute', top: beamTop + 18, width: '100%', textAlign: 'center', ...kicker, fontWeight: 800, fontSize: 40, letterSpacing: '0.3em', color: palette.rust, opacity: roof, textShadow: '0 2px 10px rgba(0,0,0,0.9)'}}>
					{g.label}
				</div>
				{pillars.map((p, i) => {
					const x = x0 + i * (pw + gap);
					const rise = ease(t, tRise + i * 0.12, 0.55, Easing.out(Easing.cubic));
					const tp = people[i] ?? 1e9;
					const turn = ease(t, tp, 0.5);
					const pop = ease(t, tp, 0.18) * (1 - ease(t, tp + 0.2, 0.6));
					const stoneO = p.empty ? 1 - turn : 1 - turn;
					const z = p.zoom ?? 0.5;
					return (
						<div key={i} style={{position: 'absolute', left: x, top: capTop, width: pw, height: pillarBase - capTop, transformOrigin: '50% 100%', transform: `scaleY(${Math.max(0.001, rise)})`, opacity: Math.min(1, rise * 2)}}>
							{/* Capital */}
							<div style={{position: 'absolute', left: -12, top: 0, width: pw + 24, height: 26, background: '#3a4349', border: `2px solid ${p.empty && turn > 0.5 ? 'rgba(233,169,75,0.5)' : palette.amber}`, borderRadius: 3, opacity: p.empty ? 1 - 0.6 * turn : 1}} />
							{/* Shaft: stone, then the supporter (or nothing). */}
							<div style={{position: 'absolute', left: 0, top: 30, width: pw, height: shaftH, overflow: 'hidden', borderLeft: `2px solid ${palette.amber}`, borderRight: `2px solid ${palette.amber}`, opacity: p.empty ? 1 - turn : 1}}>
								<div style={{position: 'absolute', inset: 0, background: STONE, opacity: stoneO}} />
								{p.src && turn > 0 && (
									<Img
										src={staticFile(p.src)}
										style={{position: 'absolute', width: 1080 * z, height: 1920 * z, left: pw / 2 - (p.x ?? 540) * z, top: shaftH / 2 - (p.y ?? 960) * z, opacity: turn, filter: 'saturate(0.9)'}}
									/>
								)}
								<div style={{position: 'absolute', inset: 0, boxShadow: 'inset 0 0 24px rgba(0,0,0,0.6)'}} />
							</div>
							{p.empty && (
								<div style={{position: 'absolute', left: 0, top: 30, width: pw, height: shaftH, border: `3px dashed ${palette.mist}`, borderRadius: 2, opacity: turn, background: `linear-gradient(180deg, rgba(159,177,184,${0.06 * turn}) 0%, rgba(159,177,184,${0.16 * turn}) 100%)`}} />
							)}
							{/* Base */}
							<div style={{position: 'absolute', left: -8, bottom: 0, width: pw + 16, height: 22, background: '#3a4349', border: `2px solid ${palette.amber}`, borderRadius: 2, opacity: p.empty ? 1 - 0.6 * turn : 1}} />
							{/* Reason label, low on the shaft. */}
							<div
								style={{
									position: 'absolute',
									left: -14,
									width: pw + 28,
									top: 30 + shaftH - 92,
									textAlign: 'center',
									...kicker,
									fontWeight: 800,
									fontSize: 21,
									letterSpacing: '0.14em',
									lineHeight: 1.25,
									color: p.empty ? palette.mist : palette.ember,
									opacity: turn,
									transform: `translateY(${(1 - turn) * 10}px) scale(${1 + 0.08 * pop})`,
									textShadow: '0 1px 4px #000, 0 0 14px rgba(0,0,0,0.95)',
								}}
							>
								<div style={{display: 'inline-block', padding: '7px 8px 5px', background: 'rgba(8,12,16,0.72)', borderTop: `1.5px solid ${p.empty ? palette.fog : palette.ember}`}}>{p.label}</div>
							</div>
							<div style={{position: 'absolute', left: -6, top: 30, width: pw + 12, height: shaftH, boxShadow: `0 0 ${30 * pop}px rgba(244,196,110,${0.5 * pop})`, pointerEvents: 'none'}} />
						</div>
					);
				})}
			</AbsoluteFill>
			{lessonLines.length > 0 && (
				<div style={{position: 'absolute', top: g.lessonTop ?? 920, left: 60, right: 60, textAlign: 'center', opacity: lk, transform: `translateY(${(1 - lk) * 16}px)`}}>
					{g.lessonKicker && <div style={{...kicker, fontSize: 30, color: palette.amber, textShadow: '0 2px 12px rgba(0,0,0,0.9)'}}>{g.lessonKicker}</div>}
					{lessonLines.map((ln, li) => {
						const lp = ease(t, tLesson + 0.15 + li * 0.25, 0.6);
						return (
							<div key={li} style={{marginTop: li ? 0 : 14, fontFamily: fonts.display, fontWeight: 600, fontSize: g.lessonSize ?? 96, lineHeight: 1.04, color: palette.parchment, opacity: lp, textShadow: '0 4px 30px rgba(0,0,0,0.8)'}}>
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

/** Supporter tag: like `tag`, with a pillar glyph and numeral ("I · BREAD") so each person reads as one pillar of the stack. */
export const PillarTag: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start, span.start);
	const a = ease(t, t0, 0.5);
	const b = ease(t, t0 + 0.15, 0.6);
	const o = out(t, span.end, 0.3);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: g.top ?? 336, left: 90}}>
				<div style={{display: 'inline-flex', alignItems: 'center', gap: 12, ...kicker, fontSize: 26, color: palette.amber, border: `1.5px solid ${palette.amber}`, padding: '8px 18px 6px 12px', background: 'rgba(11,18,22,0.5)', clipPath: `inset(0 ${(1 - a) * 100}% 0 0)`}}>
					<PillarGlyph c={palette.amber} size={30} />
					<span>
						Pillar {g.numeral} · <span style={{color: palette.ember}}>{g.kicker}</span>
					</span>
				</div>
				<div style={{marginTop: 16, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 500, fontSize: 64, color: palette.parchment, opacity: b, transform: `translateY(${(1 - b) * 14}px)`, textShadow: '0 3px 24px rgba(0,0,0,0.7)'}}>
					{g.text}
				</div>
			</div>
		</AbsoluteFill>
	);
};

export const PILLARS: Record<string, React.FC<GraphicProps>> = {
	pillarStack: PillarStack,
	pillarTag: PillarTag,
};
