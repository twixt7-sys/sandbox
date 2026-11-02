import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, staticFile} from 'remotion';
import {Logo, useBrand} from '../brand/Logo';
import {rng} from '../lib/random';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Celestial graphics (EP02 onward): a code-drawn sun that can vanish and return over any plate,
 * a 24-hour celestial clock, opening gates, a glowing sun-ring, a premise -> consequences tree,
 * a "don't / do" method card and a large comment CTA card.
 * Graphics flagged `"local": true` in episode.json render inside the plate's camera move, so they
 * stay pinned to objects in the picture (the sun in the sky, the ring on the wall).
 */

const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.24em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

/** Night colour: deep blue-black (series motif). */
const NIGHT = '5,10,24';

const STARS = (() => {
	const r = rng(2024);
	return Array.from({length: 90}, () => ({x: r() * W, y: r() ** 1.4 * 820, s: 0.8 + r() * 2.2, ph: r() * 6.28, o: 0.35 + r() * 0.65}));
})();

const Stars: React.FC<{t: number; o: number}> = ({t, o}) =>
	o <= 0 ? null : (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0, opacity: o}}>
			{STARS.map((s, i) => (
				<circle key={i} cx={s.x} cy={s.y} r={s.s} fill="#e8eefc" opacity={s.o * (0.65 + 0.35 * Math.sin(t * 2.1 + s.ph))} />
			))}
		</svg>
	);

/** The golden sun disc with corona. `k` 0..1 = size/brightness. */
const SunDisc: React.FC<{x: number; y: number; r: number; k: number; flash?: number}> = ({x, y, r, k, flash = 0}) => {
	if (k <= 0.001 && flash <= 0.001) return null;
	const rr = r * k;
	return (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
			<defs>
				<radialGradient id="sun-corona">
					<stop offset="0%" stopColor="#fff3cf" stopOpacity={0.9} />
					<stop offset="18%" stopColor="#ffd77a" stopOpacity={0.45} />
					<stop offset="50%" stopColor="#f7c763" stopOpacity={0.12} />
					<stop offset="100%" stopColor="#e9a94b" stopOpacity={0} />
				</radialGradient>
				<radialGradient id="sun-disc">
					<stop offset="0%" stopColor="#ffffff" />
					<stop offset="70%" stopColor="#fffbe8" />
					<stop offset="92%" stopColor="#ffe9a6" />
					<stop offset="100%" stopColor="#ffd377" />
				</radialGradient>
				<radialGradient id="sun-bloom">
					<stop offset="0%" stopColor="#fffdf0" stopOpacity={1} />
					<stop offset="30%" stopColor="#fff1c4" stopOpacity={0.8} />
					<stop offset="60%" stopColor="#ffd98a" stopOpacity={0.3} />
					<stop offset="100%" stopColor="#f4c46e" stopOpacity={0} />
				</radialGradient>
				<radialGradient id="sun-streak">
					<stop offset="0%" stopColor="#fffbea" stopOpacity={0.95} />
					<stop offset="100%" stopColor="#ffe3a0" stopOpacity={0} />
				</radialGradient>
			</defs>
			<circle cx={x} cy={y} r={r * 13 * Math.max(k, flash * 1.4)} fill="url(#sun-corona)" opacity={Math.min(1, 0.85 * k + flash)} />
			<circle cx={x} cy={y} r={r * 4.2 * Math.max(k, flash)} fill="url(#sun-bloom)" opacity={Math.min(1, k + flash)} />
			{/* anamorphic glare streak */}
			<ellipse cx={x} cy={y} rx={r * 9 * Math.max(k, flash)} ry={r * 0.09 + 2} fill="url(#sun-streak)" opacity={Math.min(1, 0.7 * k + flash)} />
			{rr > 0.5 && <circle cx={x} cy={y} r={rr * 1.18} fill="#ffe7a8" opacity={0.55} />}
			{rr > 0.5 && <circle cx={x} cy={y} r={rr} fill="url(#sun-disc)" />}
		</svg>
	);
};

/**
 * Sun over a plate. mode "vanish": shining at the start, gone at `start` (darkness spreads out from where it was);
 * "night": already dark; "return": dark, re-ignites at `start` and the darkness recedes to `endLevel`.
 * `glow` = [x, y] of a warm light (e.g. city gates) that wakes up once it is dark.
 */
export const SunCycle: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const mode: 'vanish' | 'night' | 'return' = g.mode ?? 'vanish';
	const x = g.x ?? 740;
	const y = g.y ?? 330;
	const r = g.r ?? 62;
	const t0 = mode === 'night' ? -1 : cueTime(timing, g.start);
	const level = g.level ?? 0.86;
	let sunK = 1;
	let flash = 0;
	let ring = 0;
	let darkInner = 0;
	let darkOuter = 0;
	let radius = 2600;
	if (mode === 'vanish') {
		const k = clamp01((t - t0) / (g.duration ?? 0.42));
		sunK = 1 - Easing.in(Easing.cubic)(k);
		flash = t >= t0 ? Math.sin(Math.PI * clamp01((t - t0) / 0.5)) * 0.8 : 0;
		ring = t >= t0 ? clamp01((t - t0) / 1.1) : 0;
		radius = interpolate(t, [t0 + 0.05, t0 + 1.4], [0, 2700], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.quad)});
		darkInner = darkOuter = t >= t0 ? level : 0;
	} else if (mode === 'night') {
		sunK = 0;
		darkInner = darkOuter = level;
	} else {
		const k = ease(t, t0, 1.8, Easing.out(Easing.cubic));
		sunK = k;
		flash = t >= t0 ? Math.sin(Math.PI * clamp01((t - t0) / 0.9)) * 0.5 : 0;
		darkOuter = lerp(level, g.endLevel ?? 0.45, ease(t, t0 + 0.2, 3.2));
		darkInner = lerp(level, (g.endLevel ?? 0.45) * 0.6, ease(t, t0, 2.6));
		radius = interpolate(t, [t0, t0 + 3], [0, 1500], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	}
	const soft = 380;
	const inner = Math.max(0, radius - soft);
	const dark =
		mode === 'vanish'
			? `radial-gradient(circle at ${x}px ${y}px, rgba(${NIGHT},${darkInner}) 0px, rgba(${NIGHT},${darkInner}) ${inner}px, rgba(${NIGHT},0) ${radius}px)`
			: `radial-gradient(circle at ${x}px ${y}px, rgba(${NIGHT},${darkInner}) 0px, rgba(${NIGHT},${darkInner}) ${inner}px, rgba(${NIGHT},${darkOuter}) ${radius + 200}px)`;
	const night = mode === 'vanish' ? ease(t, t0 + 0.4, 1.2) : mode === 'night' ? 1 : 1 - ease(t, t0 + 0.3, 1.6);
	const [gx, gy] = g.glow ?? [0, 0];
	const glowO = g.glow ? night * (0.55 + 0.08 * Math.sin(t * 7.3) + 0.05 * Math.sin(t * 13.1)) : 0;
	return (
		<AbsoluteFill>
			{/* Warm daylight wash around the sun, gone with it. */}
			<AbsoluteFill style={{background: `radial-gradient(circle at ${x}px ${y}px, rgba(255,214,140,${0.28 * sunK}) 0px, rgba(255,200,120,0) 900px)`}} />
			<AbsoluteFill style={{background: dark}} />
			<Stars t={t} o={night * 0.9} />
			{glowO > 0 && (
				<AbsoluteFill style={{background: `radial-gradient(ellipse 170px 120px at ${gx}px ${gy}px, rgba(244,180,90,${glowO}) 0%, rgba(233,169,75,${glowO * 0.35}) 45%, rgba(233,169,75,0) 100%)`}} />
			)}
			<SunDisc x={x} y={y} r={r} k={sunK} flash={flash} />
			{ring > 0 && ring < 1 && (
				<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
					<circle cx={x} cy={y} r={r * (1 + ring * 5)} fill="none" stroke={palette.ember} strokeWidth={3 * (1 - ring)} opacity={(1 - ring) * 0.85} />
					<circle cx={x} cy={y} r={r * (1 + ring * 2.4)} fill="none" stroke="#fff3cf" strokeWidth={1.5} opacity={(1 - ring) * 0.6} />
				</svg>
			)}
		</AbsoluteFill>
	);
};

/** Glowing outline + inner light inside a carved ring on the plate (the missing sun). */
export const RingGlow: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const [cx, cy] = g.at ?? [540, 602];
	const r = g.r ?? 110;
	const sweep = ease(t, t0, 1.1, Easing.inOut(Easing.cubic));
	const glow = ease(t, t0 + 0.5, 1.2) * (0.85 + 0.15 * Math.sin(t * 3.1));
	const c = 2 * Math.PI * r;
	return (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
			<defs>
				<radialGradient id="ring-in">
					<stop offset="0%" stopColor="#ffe3a0" stopOpacity={0.0} />
					<stop offset="70%" stopColor="#f4c46e" stopOpacity={0.18} />
					<stop offset="100%" stopColor="#e9a94b" stopOpacity={0.5} />
				</radialGradient>
				<radialGradient id="ring-halo">
					<stop offset="0%" stopColor="#f4c46e" stopOpacity={0} />
					<stop offset="55%" stopColor="#f4c46e" stopOpacity={0} />
					<stop offset="68%" stopColor="#f4c46e" stopOpacity={0.4} />
					<stop offset="100%" stopColor="#e9a94b" stopOpacity={0} />
				</radialGradient>
			</defs>
			<circle cx={cx} cy={cy} r={r * 2.3} fill="url(#ring-halo)" opacity={glow * 0.8} />
			<circle cx={cx} cy={cy} r={r} fill="url(#ring-in)" opacity={glow} />
			<circle
				cx={cx}
				cy={cy}
				r={r}
				fill="none"
				stroke={palette.ember}
				strokeWidth={5}
				strokeDasharray={c}
				strokeDashoffset={c * (1 - sweep)}
				transform={`rotate(-90 ${cx} ${cy})`}
				opacity={0.9}
				style={{filter: 'drop-shadow(0 0 10px rgba(244,196,110,0.9))'}}
			/>
		</svg>
	);
};

/** Two carved stone doors (sun-ring emblem split down the seam) that swing open on a cue. */
export const Gates: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const p = ease(t, t0, g.duration ?? 1.3, Easing.inOut(Easing.cubic));
	if (p >= 0.999) return null;
	const leak = clamp01(p * 6) * (1 - p);
	const door = (side: 'L' | 'R') => {
		const sign = side === 'L' ? 1 : -1;
		return (
			<div
				style={{
					position: 'absolute',
					top: 0,
					[side === 'L' ? 'left' : 'right']: 0,
					width: W / 2,
					height: H,
					transformOrigin: side === 'L' ? 'left center' : 'right center',
					transform: `rotateY(${sign * -84 * p}deg)`,
					background: `linear-gradient(${side === 'L' ? 90 : 270}deg, #0e141b 0%, #1a232c 60%, #222c35 100%)`,
					overflow: 'hidden',
					boxShadow: 'inset 0 0 120px rgba(0,0,0,0.7)',
				}}
			>
				<Img src={staticFile('textures/paper.png')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', opacity: 0.16}} />
				<div style={{position: 'absolute', inset: 46, border: '2px solid rgba(233,169,75,0.35)', [side === 'L' ? 'borderRight' : 'borderLeft']: 'none'}} />
				<div style={{position: 'absolute', inset: 70, border: '1px solid rgba(233,169,75,0.18)', [side === 'L' ? 'borderRight' : 'borderLeft']: 'none'}} />
				<svg width={W / 2} height={H} style={{position: 'absolute', inset: 0}}>
					{/* half of the sun-ring emblem on each door; the whole ring forms on the seam */}
					<g transform={`translate(${side === 'L' ? W / 2 : 0} 860)`} fill="none" stroke={palette.amber} opacity={0.75}>
						<circle r={170} strokeWidth={6} />
						<circle r={128} strokeWidth={2} opacity={0.6} />
						{Array.from({length: 24}, (_, i) => {
							const a = (i / 24) * Math.PI * 2;
							const r1 = 190;
							const r2 = i % 2 ? 222 : 250;
							return <line key={i} x1={Math.cos(a) * r1} y1={Math.sin(a) * r1} x2={Math.cos(a) * r2} y2={Math.sin(a) * r2} strokeWidth={3} />;
						})}
					</g>
				</svg>
			</div>
		);
	};
	return (
		<AbsoluteFill style={{perspective: 1700, opacity: 1 - ease(t, t0 + (g.duration ?? 1.3) * 0.7, 0.4)}}>
			{door('L')}
			{door('R')}
			<div style={{position: 'absolute', left: W / 2 - 3 - p * 70, width: 6 + p * 140, top: 0, height: H, background: `linear-gradient(90deg, rgba(244,196,110,0) 0%, rgba(255,214,140,${0.85 * leak}) 50%, rgba(244,196,110,0) 100%)`}} />
		</AbsoluteFill>
	);
};

/** The sun glyph used inside diagrams. */
const SunGlyph: React.FC<{size: number; o?: number; hollow?: boolean}> = ({size, o = 1, hollow}) => (
	<svg width={size} height={size} viewBox="-50 -50 100 100" style={{opacity: o, overflow: 'visible'}}>
		{Array.from({length: 12}, (_, i) => {
			const a = (i / 12) * Math.PI * 2;
			return <line key={i} x1={Math.cos(a) * 30} y1={Math.sin(a) * 30} x2={Math.cos(a) * (i % 2 ? 40 : 46)} y2={Math.sin(a) * (i % 2 ? 40 : 46)} stroke={palette.ember} strokeWidth={3.5} strokeLinecap="round" />;
		})}
		{hollow ? <circle r={21} fill="none" stroke={palette.ember} strokeWidth={5} /> : <circle r={21} fill={palette.ember} />}
	</svg>
);

/**
 * 24-hour celestial clock. The sun orbits `laps` times between start and end; each pass through the
 * one-hour dark sector (at the bottom = midnight) hides it, and a night counter ticks up. It settles in the sector.
 */
export const CelestialClock: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const t1 = cueTime(timing, g.end, t0 + 3.5);
	const laps = g.laps ?? 3;
	const cx = 540;
	const cy = g.y ?? 800;
	const R = 290;
	const sector = 15; // 1 of 24 hours
	const intro = ease(t, span.start - 0.1, 0.7);
	const o = intro * out(t, span.end + 0.1, 0.35);
	// Sun angle (0 = top/noon, clockwise). Each lap lingers in the dark sector so the gap reads.
	const lapT = (t1 - t0) / (laps + 0.5);
	const u = (t - t0) / lapT;
	const lap = Math.floor(Math.max(0, u));
	const f = Math.max(0, u) - lap;
	const linger = 0.3;
	const darkA0 = 180 - sector / 2;
	let ang: number;
	if (u < 0) ang = 120 + u * 20;
	else if (u >= laps + 0.5) ang = 180;
	else if (lap === laps) {
		// last half lap: glide into midnight and stop
		ang = lerp(0, 180, Easing.out(Easing.cubic)(clamp01(f * 2)));
	} else {
		const a0 = darkA0; // enter dark
		const dayFrac = 1 - linger;
		if (f < dayFrac * (a0 / 345)) ang = (f / (dayFrac * (a0 / 345))) * a0;
		else if (f < dayFrac * (a0 / 345) + linger) ang = a0 + ((f - dayFrac * (a0 / 345)) / linger) * sector;
		else ang = a0 + sector + ((f - dayFrac * (a0 / 345) - linger) / (dayFrac * (1 - a0 / 345))) * (345 - a0);
	}
	const norm = ((ang % 360) + 360) % 360;
	const inDark = norm >= darkA0 && norm <= darkA0 + sector;
	const nights = Math.min(laps + 1, u < 0 ? 0 : lap + (norm >= darkA0 ? 1 : 0));
	const settled = ease(t, t1 - 0.2, 0.6);
	const rad = ((norm - 90) * Math.PI) / 180;
	const sx = cx + Math.cos(rad) * R;
	const sy = cy + Math.sin(rad) * R;
	const dimDial = inDark ? 0.55 : 1;
	const arc = (a0: number, a1: number, r: number) => {
		const p = (a: number) => [cx + Math.cos(((a - 90) * Math.PI) / 180) * r, cy + Math.sin(((a - 90) * Math.PI) / 180) * r];
		const [x0, y0] = p(a0);
		const [x1, y1] = p(a1);
		return `M${x0},${y0} A${r},${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1},${y1}`;
	};
	const rIn = R - 70;
	const P = (a: number, r: number) => `${cx + Math.cos(((a - 90) * Math.PI) / 180) * r},${cy + Math.sin(((a - 90) * Math.PI) / 180) * r}`;
	const sectorPath = `M${P(darkA0, rIn)} L${P(darkA0, R + 40)} A${R + 40},${R + 40} 0 0 1 ${P(darkA0 + sector, R + 40)} L${P(darkA0 + sector, rIn)} A${rIn},${rIn} 0 0 0 ${P(darkA0, rIn)} Z`;
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: 360, width: '100%', textAlign: 'center'}}>
				<div style={{...kicker, fontSize: 28, color: palette.amber}}>{g.kicker ?? 'Every night · same hour'}</div>
				<div style={{marginTop: 12, ...kicker, fontSize: 24, color: palette.mist, opacity: 0.85, fontVariantNumeric: 'tabular-nums'}}>
					{nights > laps ? 'Night 10,000' : `Night ${Math.max(1, nights)}`}
				</div>
			</div>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, transform: `scale(${0.94 + 0.06 * intro})`, transformOrigin: `${cx}px ${cy}px`}}>
				<defs>
					<radialGradient id="clock-face">
						<stop offset="0%" stopColor="#0b1530" stopOpacity={0.75} />
						<stop offset="100%" stopColor="#050a18" stopOpacity={0.55} />
					</radialGradient>
					<radialGradient id="sector-glow">
						<stop offset="0%" stopColor="#000" stopOpacity={0.95} />
						<stop offset="100%" stopColor="#02040c" stopOpacity={0.95} />
					</radialGradient>
				</defs>
				<circle cx={cx} cy={cy} r={R + 70} fill="url(#clock-face)" />
				<g opacity={dimDial}>
					<circle cx={cx} cy={cy} r={R} fill="none" stroke="rgba(239,230,210,0.55)" strokeWidth={2} />
					<circle cx={cx} cy={cy} r={R + 56} fill="none" stroke="rgba(233,169,75,0.35)" strokeWidth={1.5} />
					<circle cx={cx} cy={cy} r={R - 70} fill="none" stroke="rgba(239,230,210,0.18)" strokeWidth={1} />
					{Array.from({length: 24}, (_, i) => {
						const a = ((i * 15 - 90) * Math.PI) / 180;
						const big = i % 6 === 0;
						return <line key={i} x1={cx + Math.cos(a) * (R + 8)} y1={cy + Math.sin(a) * (R + 8)} x2={cx + Math.cos(a) * (R + (big ? 40 : 24))} y2={cy + Math.sin(a) * (R + (big ? 40 : 24))} stroke={palette.parchment} strokeWidth={big ? 3 : 1.5} opacity={0.75} />;
					})}
					{/* daylight arc travelled so far this lap */}
					{!inDark && norm > 1 && <path d={arc(norm < darkA0 ? 0 : darkA0 + sector, norm, R)} fill="none" stroke={palette.amber} strokeWidth={5} opacity={0.75} />}
				</g>
				{/* the missing hour */}
				<path d={sectorPath} fill="url(#sector-glow)" />
				<path d={arc(darkA0, darkA0 + sector, R + 40)} fill="none" stroke={palette.ember} strokeWidth={3} />
				<line x1={cx + Math.cos(((darkA0 - 90) * Math.PI) / 180) * rIn} y1={cy + Math.sin(((darkA0 - 90) * Math.PI) / 180) * rIn} x2={cx + Math.cos(((darkA0 - 90) * Math.PI) / 180) * (R + 40)} y2={cy + Math.sin(((darkA0 - 90) * Math.PI) / 180) * (R + 40)} stroke={palette.ember} strokeWidth={1.5} opacity={0.8} />
				<line x1={cx + Math.cos(((darkA0 + sector - 90) * Math.PI) / 180) * rIn} y1={cy + Math.sin(((darkA0 + sector - 90) * Math.PI) / 180) * rIn} x2={cx + Math.cos(((darkA0 + sector - 90) * Math.PI) / 180) * (R + 40)} y2={cy + Math.sin(((darkA0 + sector - 90) * Math.PI) / 180) * (R + 40)} stroke={palette.ember} strokeWidth={1.5} opacity={0.8} />
				{/* hand: from the inner ring outward, so it never crosses the centre figure */}
				<line x1={cx + Math.cos(rad) * rIn} y1={cy + Math.sin(rad) * rIn} x2={cx + Math.cos(rad) * (R - 40)} y2={cy + Math.sin(rad) * (R - 40)} stroke={palette.parchment} strokeWidth={2} opacity={0.6} />
			</svg>
			{!inDark && (
				<div style={{position: 'absolute', left: sx - 45, top: sy - 45, filter: 'drop-shadow(0 0 16px rgba(244,196,110,0.9))'}}>
					<SunGlyph size={90} />
				</div>
			)}
			<div style={{position: 'absolute', top: cy - 120, width: '100%', textAlign: 'center', color: palette.parchment}}>
				<div style={{fontFamily: fonts.display, fontWeight: 600, fontSize: 150, lineHeight: 1, fontVariantNumeric: 'tabular-nums', color: inDark || settled > 0.5 ? palette.ember : palette.parchment}}>60</div>
				<div style={{...kicker, fontSize: 22, marginTop: 8, color: palette.mist}}>minutes of dark</div>
			</div>
			<div style={{position: 'absolute', top: cy + R + 58, width: '100%', textAlign: 'center', ...kicker, fontSize: 24, color: palette.ember, opacity: 0.4 + 0.6 * Math.max(inDark ? 1 : 0, settled)}}>
				1 hour of 24
			</div>
		</AbsoluteFill>
	);
};

/** Premise at the top, lines branch to three consequences (circular plate thumbnails), then "= a civilization". */
export const ConsequenceTree: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const tTop = cueTime(timing, g.start);
	const tLines = cueTime(timing, g.branch);
	const beats: number[] = (g.beats ?? []).map((c: any) => cueTime(timing, c));
	const tSum = cueTime(timing, g.sum);
	const o = out(t, span.end + 0.1, 0.35);
	const top = ease(t, tTop - 0.05, 0.6);
	const lines = ease(t, tLines, 0.7, Easing.inOut(Easing.cubic));
	const sum = ease(t, tSum, 0.7);
	const items: {label: string; plate: string; pos?: string}[] = g.items;
	const xs = [210, 540, 870];
	const yTop = 470;
	const yBar = 640;
	const yMed = 840;
	const rMed = 128;
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: yTop - 110, width: '100%', display: 'flex', justifyContent: 'center', opacity: top}}>
				<div style={{filter: 'drop-shadow(0 0 18px rgba(244,196,110,0.7))'}}>
					<SunGlyph size={70} hollow />
				</div>
			</div>
			<div style={{position: 'absolute', top: yTop - 26, width: '100%', textAlign: 'center', opacity: top, transform: `translateY(${(1 - top) * 14}px)`}}>
				<div style={{fontFamily: fonts.display, fontWeight: 700, fontSize: 70, letterSpacing: '0.06em', color: palette.parchment, textShadow: '0 4px 30px rgba(0,0,0,0.6)'}}>
					ONE <span style={{color: palette.ember, fontStyle: 'italic', fontWeight: 600, letterSpacing: '0.02em'}}>IMPOSSIBLE</span> RULE
				</div>
			</div>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				<g stroke={palette.amber} strokeWidth={2.5} fill="none" opacity={0.9}>
					<line x1={540} y1={yTop + 70} x2={540} y2={lerp(yTop + 70, yBar, clamp01(lines * 2))} />
					{lines > 0.5 && <line x1={540 - (540 - xs[0]) * clamp01((lines - 0.5) * 2)} y1={yBar} x2={540 + (xs[2] - 540) * clamp01((lines - 0.5) * 2)} y2={yBar} />}
					{xs.map((x, i) => {
						const p = ease(t, beats[i] ?? tLines + 0.6, 0.35);
						return <line key={i} x1={x} y1={yBar} x2={x} y2={lerp(yBar, yMed - rMed - 6, p)} />;
					})}
				</g>
				{xs.map((x, i) => {
					const p = ease(t, beats[i] ?? tLines + 0.6, 0.35);
					return p > 0 ? <path key={i} d={`M${x - 9},${yMed - rMed - 20} L${x},${yMed - rMed - 6} L${x + 9},${yMed - rMed - 20}`} stroke={palette.amber} strokeWidth={2.5} fill="none" opacity={p} /> : null;
				})}
			</svg>
			{items.map((it, i) => {
				const p = ease(t, (beats[i] ?? tLines + 0.6) + 0.1, 0.6);
				const s = lerp(1.7, 1, p);
				return (
					<div key={it.label} style={{position: 'absolute', left: xs[i] - rMed, top: yMed - rMed, width: rMed * 2, opacity: p}}>
						<div style={{width: rMed * 2, height: rMed * 2, borderRadius: '50%', overflow: 'hidden', border: `3px solid ${sum > 0.5 ? palette.ember : 'rgba(239,230,210,0.85)'}`, boxShadow: `0 0 ${30 + 30 * sum}px rgba(244,196,110,${0.25 + 0.35 * sum})`, transform: `scale(${s})`}}>
							<Img src={staticFile(it.plate)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: it.pos ?? '50% 50%', transform: `scale(${lerp(1.3, 1.6, p)})`}} />
						</div>
						<div style={{marginTop: 26, textAlign: 'center', ...kicker, fontSize: 25, letterSpacing: '0.16em', color: palette.parchment, textShadow: '0 2px 12px rgba(0,0,0,0.8)'}}>{it.label}</div>
					</div>
				);
			})}
			<div style={{position: 'absolute', top: yMed + rMed + 96, width: '100%', textAlign: 'center', opacity: sum}}>
				<div style={{margin: '0 auto', width: 760 * sum, height: 1.5, background: palette.amber, opacity: 0.8}} />
				<div style={{marginTop: 16, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 56, color: palette.ember}}>{g.sumText ?? '= a whole civilization'}</div>
			</div>
		</AbsoluteFill>
	);
};

/** Method card: a cloud of random facts gets struck out, then the one question takes its place. */
export const Method: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const tA = cueTime(timing, g.start);
	const tStrike = cueTime(timing, g.strike);
	const tB = cueTime(timing, g.second);
	const o = out(t, span.end + 0.1, 0.35);
	const a = ease(t, tA - 0.05, 0.5);
	const strike = ease(t, tStrike, 0.45, Easing.inOut(Easing.quad));
	const b = ease(t, tB - 0.05, 0.6);
	const facts: string[] = g.facts ?? [];
	const r = rng(77);
	const chips = facts.map((f, i) => ({f, x: 110 + r() * 760, y: 330 + r() * 340, rot: (r() - 0.5) * 14, d: r() * 0.9}));
	const lineB = timing.lines.find((l) => l.id === g.second.line)!;
	const qWords = (g.question as string).split(' ');
	const startIdx = lineB.words.findIndex((w) => w.start >= tB - 0.01);
	return (
		<AbsoluteFill style={{opacity: o}}>
			{chips.map((c, i) => {
				const ci = ease(t, tA + c.d, 0.4) * (1 - 0.75 * strike) * (1 - b);
				return (
					<div key={i} style={{position: 'absolute', left: c.x, top: c.y, transform: `translate(-50%,-50%) rotate(${c.rot}deg) scale(${0.9 + 0.1 * ci})`, opacity: ci * 0.75, whiteSpace: 'nowrap', fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 500, fontSize: 36, color: palette.fog, border: '1px solid rgba(159,177,184,0.35)', padding: '6px 16px', background: 'rgba(11,18,22,0.45)'}}>
						{c.f}
					</div>
				);
			})}
			<div style={{position: 'absolute', top: 720, width: '100%', textAlign: 'center', opacity: a * (1 - 0.6 * b), transform: `translateY(${-b * 300}px) scale(${1 - 0.25 * b})`}}>
				<div style={{...kicker, fontSize: 26, color: palette.rust}}>Don&apos;t</div>
				<div style={{position: 'relative', display: 'inline-block', marginTop: 8, fontFamily: fonts.display, fontWeight: 600, fontSize: 84, color: palette.parchment, textShadow: '0 4px 30px rgba(0,0,0,0.6)'}}>
					start with 100 facts
					<div style={{position: 'absolute', left: -12, top: '54%', height: 6, width: `calc(${strike * 100}% + 24px)`, background: palette.rust, transform: 'rotate(-2deg)'}} />
				</div>
			</div>
			<div style={{position: 'absolute', top: 760, width: '100%', textAlign: 'center', opacity: b}}>
				<div style={{...kicker, fontSize: 26, color: palette.amber}}>Start with</div>
				<div style={{marginTop: 18, padding: '0 90px', fontFamily: fonts.display, fontWeight: 600, fontSize: 104, lineHeight: 1.04, color: palette.parchment, textShadow: '0 4px 36px rgba(0,0,0,0.6)'}}>
					{qWords.map((raw, k) => {
						const w = lineB.words[startIdx + 2 + k];
						const p = w ? ease(t, w.start - 0.08, 0.35) : b;
						const em = raw.startsWith('*');
						return (
							<span key={k} style={{display: 'inline-block', marginRight: '0.22em', opacity: 0.15 + 0.85 * p, transform: `translateY(${(1 - p) * 16}px)`, color: em ? palette.ember : undefined, fontStyle: em ? 'italic' : undefined}}>
								{raw.replace(/\*/g, '')}
							</span>
						);
					})}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** End card for a comment CTA: full logo, episode, the CTA in large type (spoken line shown verbatim). */
export const CtaCard: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const brand = useBrand();
	const t0 = cueTime(timing, g.start);
	const tCta = cueTime(timing, g.ctaAt);
	const a = ease(t, t0 + 0.1, 0.8);
	const b = ease(t, tCta - 0.1, 0.7);
	const fade = out(t, span.end - 0.55, 0.5);
	const lines: string[] = g.lines;
	return (
		<AbsoluteFill style={{opacity: fade}}>
			{/* Keeps type legible as the sun brightens the landscape behind it. */}
			<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,10,24,0) 12%, rgba(5,10,24,0.5) 24%, rgba(5,10,24,0.55) 66%, rgba(5,10,24,0) 80%)', opacity: a}} />
			{brand && (
				<div style={{position: 'absolute', top: 300, width: '100%', display: 'flex', justifyContent: 'center', opacity: a, transform: `translateY(${(1 - a) * 12}px)`}}>
					<Logo brand={brand} height={124} />
				</div>
			)}
			<div style={{position: 'absolute', top: 452, width: '100%', textAlign: 'center', opacity: a}}>
				<div style={{...kicker, fontSize: 24, color: palette.amber}}>{g.episode}</div>
				<div style={{marginTop: 14, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 52, color: palette.parchment, textShadow: '0 3px 20px rgba(0,0,0,0.8)'}}>{g.title}</div>
			</div>
			<div style={{position: 'absolute', top: 760, width: '100%', textAlign: 'center', opacity: a}}>
				<div style={{...kicker, fontSize: 28, color: palette.ember}}>{g.kicker ?? 'Your turn'}</div>
			</div>
			<div style={{position: 'absolute', top: 820, left: 70, right: 70, textAlign: 'center'}}>
				{lines.map((ln, i) => {
					const p = ease(t, tCta - 0.1 + i * 0.25, 0.6);
					return (
						<div key={i} style={{fontFamily: fonts.display, fontWeight: 600, fontSize: g.size ?? 92, lineHeight: 1.08, color: ln.startsWith('*') ? palette.ember : palette.parchment, fontStyle: ln.startsWith('*') ? 'italic' : undefined, opacity: p, transform: `translateY(${(1 - p) * 18}px)`, textShadow: '0 4px 34px rgba(0,0,0,0.75)'}}>
							{ln.replace(/\*/g, '')}
						</div>
					);
				})}
			</div>
			<div style={{position: 'absolute', top: 1180, width: '100%', display: 'flex', justifyContent: 'center', opacity: b}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 18, fontFamily: fonts.ui, fontWeight: 700, fontSize: 36, color: '#151a1d', background: palette.amber, padding: '18px 36px 16px', borderRadius: 999, transform: `scale(${0.96 + 0.04 * b})`}}>
					<svg width={38} height={38} viewBox="0 0 24 24" fill="none" stroke="#151a1d" strokeWidth={2.4} strokeLinejoin="round" strokeLinecap="round">
						{/* `icon: "follow"` swaps the comment bubble for a follow (person +) mark; `"share"` for a paper plane; `"save"` for a bookmark. */}
						{g.icon === 'save' ? (
							<path d="M6 3h12v18l-6-4.5L6 21z" />
						) : g.icon === 'share' ? (
							<path d="M21 3 3 10.5l7 2.8M21 3l-7.5 18-3.5-7.7M21 3 10 13.3" />
						) : g.icon === 'follow' ? (
							<>
								<circle cx={9} cy={8} r={4} />
								<path d="M2 20c0-4 3-6 7-6s7 2 7 6M19 7v6M16 10h6" />
							</>
						) : (
							<path d="M4 5h16v11H9l-5 4z" />
						)}
					</svg>
					{g.button ?? 'Comment below'}
				</div>
			</div>
		</AbsoluteFill>
	);
};

export const CELESTIAL: Record<string, React.FC<GraphicProps>> = {
	sunCycle: SunCycle,
	ringGlow: RingGlow,
	gates: Gates,
	celestialClock: CelestialClock,
	consequenceTree: ConsequenceTree,
	method: Method,
	ctaCard: CtaCard,
};
