import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile} from 'remotion';
import {rng} from '../lib/random';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Resource-crisis graphics (EP03 onward): a draining level gauge, a power brown-out flicker,
 * an animated allocation map (one supply split between two needs), plate bands behind a
 * stacked lesson, and a dusk grade with city lights for a plate.
 */

const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const WATER = '#7fd3ec';
const WATER_DEEP = '#2b8fb3';

/** Vertical level gauge that drains from `from`% to `to`% between two cues, leaving dated water marks behind. */
export const LevelGauge: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const t1 = cueTime(timing, g.end, t0 + 2.5);
	const from = g.from ?? 100;
	const to = g.to ?? 12;
	const x = g.x ?? 820;
	const top = g.top ?? 400;
	const h = g.height ?? 560;
	const w = 64;
	const p = ease(t, t0, t1 - t0, Easing.inOut(Easing.cubic));
	const level = lerp(from, to, p);
	const o = ease(t, span.start + 0.2, 0.5) * out(t, span.end + 0.1, 0.35);
	const marks: {at: number; label: string}[] = g.marks ?? [];
	const y = (v: number) => top + h * (1 - v / 100);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', left: x - 140, width: w + 280, top: top - 112, textAlign: 'center'}}>
				<div style={{...kicker, fontSize: 22, color: palette.mist, textShadow: '0 2px 10px rgba(0,0,0,0.7)'}}>{g.label ?? 'Reservoir'}</div>
				<div style={{fontFamily: fonts.display, fontWeight: 600, fontSize: 64, lineHeight: 1.1, fontVariantNumeric: 'tabular-nums', color: level < 30 ? palette.ember : palette.parchment, textShadow: '0 3px 20px rgba(0,0,0,0.7)'}}>{Math.round(level)}%</div>
			</div>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				<defs>
					<linearGradient id="gauge-water" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stopColor={WATER} stopOpacity={0.95} />
						<stop offset="100%" stopColor={WATER_DEEP} stopOpacity={0.95} />
					</linearGradient>
				</defs>
				<rect x={x} y={top} width={w} height={h} rx={10} fill="rgba(8,13,22,0.62)" stroke="rgba(239,230,210,0.7)" strokeWidth={2} />
				<rect x={x + 6} y={y(level)} width={w - 12} height={Math.max(0, top + h - 6 - y(level))} rx={6} fill="url(#gauge-water)" style={{filter: 'drop-shadow(0 0 12px rgba(127,211,236,0.6))'}} />
				{marks.map((m) => {
					const passed = level <= m.at;
					return (
						<g key={m.label} opacity={passed ? 1 : 0.35}>
							<line x1={x - 16} x2={x + w} y1={y(m.at)} y2={y(m.at)} stroke={palette.amber} strokeWidth={2} strokeDasharray="6 5" />
						</g>
					);
				})}
			</svg>
			{marks.map((m) => (
				<div key={m.label} style={{position: 'absolute', left: x - 330, width: 306, top: y(m.at) - 22, textAlign: 'right', fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 40, color: palette.parchment, opacity: level <= m.at ? 0.95 : 0.3, textShadow: '0 2px 12px rgba(0,0,0,0.85)'}}>
					{m.label}
				</div>
			))}
		</AbsoluteFill>
	);
};

/** Brown-out: the frame dips dark in short stutters on a cue, then settles dimmer (`settle`). */
export const Flicker: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const d = t - t0;
	const stutters = [0, 0.14, 0.31, 0.62];
	let a = 0;
	for (const s of stutters) a = Math.max(a, d >= s && d < s + 0.07 ? 0.55 : 0);
	const settle = (g.settle ?? 0.25) * ease(t, t0 + 0.6, 0.8);
	return <AbsoluteFill style={{background: `rgba(4,8,16,${Math.max(a, settle)})`}} />;
};

/** Small glyphs for the allocation map. */
const Wheat: React.FC<{c: string}> = ({c}) => (
	<g stroke={c} strokeWidth={4} fill="none" strokeLinecap="round">
		<path d="M0,40 L0,-34" />
		{[-24, -10, 4, 18].map((yy) => (
			<g key={yy}>
				<path d={`M0,${yy} q-14,-6 -16,-18`} />
				<path d={`M0,${yy} q14,-6 16,-18`} />
			</g>
		))}
	</g>
);
const Gear: React.FC<{c: string; rot: number}> = ({c, rot}) => (
	<g transform={`rotate(${rot})`} fill="none" stroke={c} strokeWidth={4}>
		<circle r={22} />
		<circle r={8} />
		{Array.from({length: 8}, (_, i) => {
			const a = (i / 8) * Math.PI * 2;
			return <line key={i} x1={Math.cos(a) * 22} y1={Math.sin(a) * 22} x2={Math.cos(a) * 34} y2={Math.sin(a) * 34} strokeWidth={8} />;
		})}
	</g>
);

/**
 * Allocation map: one reservoir feeding two needs through channels whose width tracks the share.
 * `shifts`: [{at: cue, left: 0..1}], left = share to the left node. The starved node dims and desaturates.
 */
export const Allocation: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const shifts: {at: any; left: number}[] = g.shifts ?? [];
	let left = g.initial ?? 0.5;
	for (const s of shifts) {
		const ts = cueTime(timing, s.at);
		left = lerp(left, s.left, ease(t, ts, 0.8, Easing.inOut(Easing.cubic)));
	}
	const right = 1 - left;
	const o = ease(t, span.start - 0.1, 0.5) * out(t, span.end + 0.1, 0.3);
	const draw = ease(t, span.start, 0.9, Easing.inOut(Easing.cubic));
	const R = {x: 540, y: 520};
	const L = {x: 250, y: 960};
	const Rt = {x: 830, y: 960};
	const pathL = `M${R.x - 30},${R.y + 120} C${R.x - 40},${R.y + 300} ${L.x + 40},${L.y - 300} ${L.x},${L.y - 130}`;
	const pathR = `M${R.x + 30},${R.y + 120} C${R.x + 40},${R.y + 300} ${Rt.x - 40},${Rt.y - 300} ${Rt.x},${Rt.y - 130}`;
	const flow = t * 90;
	const node = (pt: {x: number; y: number}, share: number, label: string, img: string, kind: 'wheat' | 'gear') => {
		const vit = clamp01((share - 0.2) / 0.4); // 0 = starved, 1 = thriving
		const col = vit > 0.5 ? palette.ember : palette.fog;
		return (
			<div style={{position: 'absolute', left: pt.x - 120, top: pt.y - 120, width: 240, textAlign: 'center'}}>
				<div style={{width: 240, height: 240, borderRadius: '50%', overflow: 'hidden', border: `3px solid ${vit > 0.5 ? palette.ember : 'rgba(159,177,184,0.7)'}`, boxShadow: `0 0 ${10 + 40 * vit}px rgba(127,211,236,${0.15 + 0.35 * vit})`, position: 'relative'}}>
					<Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: g[`pos_${kind}`] ?? '50% 50%', transform: 'scale(1.5)', filter: `grayscale(${1 - vit}) brightness(${0.35 + 0.65 * vit})`}} />
				</div>
				<svg width={120} height={100} viewBox="-60 -50 120 100" style={{position: 'absolute', left: 60, top: -110, overflow: 'visible'}}>
					{kind === 'wheat' ? <Wheat c={col} /> : <Gear c={col} rot={t * 120 * vit} />}
				</svg>
				<div style={{marginTop: 18, ...kicker, fontSize: 26, color: palette.parchment, textShadow: '0 2px 12px rgba(0,0,0,0.8)'}}>{label}</div>
				<div style={{fontFamily: fonts.display, fontWeight: 600, fontSize: 60, lineHeight: 1.05, fontVariantNumeric: 'tabular-nums', color: col}}>{Math.round(share * 100)}%</div>
			</div>
		);
	};
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: 336, width: '100%', textAlign: 'center', ...kicker, fontSize: 26, color: palette.amber}}>{g.kicker ?? "Who gets what's left?"}</div>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				<defs>
					<radialGradient id="res-water">
						<stop offset="0%" stopColor={WATER} />
						<stop offset="100%" stopColor={WATER_DEEP} />
					</radialGradient>
				</defs>
				{/* reservoir: ring + the 12% that is left */}
				<circle cx={R.x} cy={R.y} r={120} fill="rgba(8,13,22,0.7)" stroke={palette.parchment} strokeWidth={2.5} />
				<circle cx={R.x} cy={R.y} r={120} fill="none" stroke={palette.amber} strokeWidth={1.5} strokeDasharray="5 7" opacity={0.6} transform={`rotate(-90 ${R.x} ${R.y})`} />
				<circle cx={R.x} cy={R.y} r={120 * Math.sqrt(g.remaining ?? 0.12) * 1.6} fill="url(#res-water)" style={{filter: 'drop-shadow(0 0 16px rgba(127,211,236,0.7))'}} />
				{[pathL, pathR].map((d, i) => {
					const share = i === 0 ? left : right;
					return (
						<g key={i}>
							<path d={d} fill="none" stroke="rgba(239,230,210,0.25)" strokeWidth={50} strokeLinecap="round" pathLength={1} strokeDasharray={`${draw} 1`} />
							<path d={d} fill="none" stroke={WATER} strokeWidth={4 + share * 38} strokeLinecap="round" opacity={0.25 + 0.75 * share} pathLength={1} strokeDasharray={`${draw} 1`} style={{filter: 'drop-shadow(0 0 10px rgba(127,211,236,0.55))'}} />
							{draw > 0.99 && <path d={d} fill="none" stroke="#e8fbff" strokeWidth={2 + share * 8} strokeLinecap="round" strokeDasharray="10 34" strokeDashoffset={-flow * (0.3 + share)} opacity={0.35 + 0.5 * share} />}
						</g>
					);
				})}
			</svg>
			<div style={{position: 'absolute', top: R.y - 34, width: '100%', textAlign: 'center', ...kicker, fontSize: 20, color: palette.mist, textShadow: '0 2px 10px rgba(0,0,0,0.9)'}}>{g.source ?? 'Reservoir'}</div>
			{node(L, left, g.leftLabel ?? 'Farms', g.leftImg, 'wheat')}
			{node(Rt, right, g.rightLabel ?? 'Workshops', g.rightImg, 'gear')}
		</AbsoluteFill>
	);
};

/** Three horizontal bands of plates (the whole crisis at once), darkened behind a lesson. */
export const PlateBands: React.FC<GraphicProps> = ({g, t, span}) => {
	const bands: {src: string; pos?: string}[] = g.bands;
	const h = H / bands.length;
	return (
		<AbsoluteFill>
			{bands.map((b, i) => {
				const p = ease(t, span.start - 0.2 + i * 0.12, 0.6);
				return (
					<div key={i} style={{position: 'absolute', left: 0, top: i * h, width: W, height: h, overflow: 'hidden', opacity: p}}>
						<Img src={staticFile(b.src)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: b.pos ?? '50% 50%', transform: `scale(${lerp(1.12, 1.04, (t - span.start) / Math.max(1, span.end - span.start))}) translateX(${(i % 2 ? -1 : 1) * lerp(0, 18, (t - span.start) / 5)}px)`}} />
						<div style={{position: 'absolute', inset: 0, background: `rgba(6,11,20,${g.dim ?? 0.62})`}} />
						{i > 0 && <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: 2, background: palette.amber, opacity: 0.5}} />}
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

/** Stacked lesson lines joined by down-arrows; each lands on its cue. The last line is the payoff (amber, larger). */
export const LessonStack: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const items: {text: string; at: any}[] = g.items;
	const o = out(t, span.end + 0.1, 0.35);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: g.top ?? 400, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18}}>
				{items.map((it, i) => {
					const p = ease(t, cueTime(timing, it.at) - 0.08, 0.55);
					const last = i === items.length - 1;
					return (
						<React.Fragment key={i}>
							{i > 0 && (
								<svg width={40} height={60} viewBox="0 0 40 60" style={{opacity: p}}>
									<line x1={20} y1={0} x2={20} y2={50 * p} stroke={palette.amber} strokeWidth={3} />
									<path d="M8,40 L20,54 L32,40" fill="none" stroke={palette.amber} strokeWidth={3} opacity={p > 0.8 ? 1 : 0} />
								</svg>
							)}
							<div
								style={{
									fontFamily: fonts.display,
									fontWeight: 700,
									fontSize: last ? 104 : 84,
									letterSpacing: '0.05em',
									color: last ? palette.ember : palette.parchment,
									fontStyle: last ? 'italic' : undefined,
									opacity: p,
									transform: `translateY(${(1 - p) * 18}px)`,
									textShadow: '0 4px 30px rgba(0,0,0,0.75)',
									whiteSpace: 'nowrap',
								}}
							>
								{it.text}
							</div>
						</React.Fragment>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

const LIGHTS = (() => {
	const r = rng(303);
	return Array.from({length: 120}, () => ({x: r() * W, y: 440 + r() * 330, s: 1.5 + r() * 2.5, ph: r() * 6.28}));
})();

/**
 * Dusk over a daytime plate: warm horizon, deep-blue sky and land, city windows lighting up,
 * a glowing pool reflecting them. `lights` = [x0,y0,x1,y1] band for windows, `pool` = [x,y,rx,ry].
 */
export const DuskGrade: React.FC<GraphicProps> = ({g, t, span}) => {
	const p = g.instant ? 1 : ease(t, span.start, 1.6);
	const [px, py, prx, pry] = g.pool ?? [540, 1460, 170, 90];
	const lit = ease(t, span.start + 0.5, 1.5);
	return (
		<AbsoluteFill style={{opacity: p}}>
			<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(10,18,44,0.78) 0%, rgba(40,34,70,0.55) 16%, rgba(214,120,60,0.32) 24%, rgba(10,16,32,0.6) 32%, rgba(6,10,22,0.72) 100%)'}} />
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				{LIGHTS.map((l, i) => (
					<circle key={i} cx={l.x} cy={l.y} r={l.s} fill="#ffcf7a" opacity={lit * (0.55 + 0.45 * Math.sin(t * 1.3 + l.ph)) * (i / LIGHTS.length < lit ? 1 : 0)} style={{filter: 'drop-shadow(0 0 4px rgba(255,190,100,0.9))'}} />
				))}
			</svg>
			<AbsoluteFill style={{background: `radial-gradient(ellipse ${prx}px ${pry}px at ${px}px ${py}px, rgba(160,226,246,0.6) 0%, rgba(90,180,220,0.25) 55%, rgba(60,140,200,0) 100%)`}} />
		</AbsoluteFill>
	);
};

export const CRISIS: Record<string, React.FC<GraphicProps>> = {
	levelGauge: LevelGauge,
	flicker: Flicker,
	allocation: Allocation,
	plateBands: PlateBands,
	lessonStack: LessonStack,
	duskGrade: DuskGrade,
};
