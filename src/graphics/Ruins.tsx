import React, {useId} from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {rng} from '../lib/random';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Ruins / reverse-worldbuilding graphics (EP05 onward): a title lockup, survey rings that mark a clue
 * on the plate, dust in a light beam, amber reconstruction lines drawn over ruins, a "don't → do"
 * lesson card, and an ember dusk grade.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.24em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const clamp01 = (x: number) => Math.min(1, Math.max(0, x));

/** Episode title over the hook: amber caps kicker, then one large serif italic word with a mask reveal. */
export const TitleLockup: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start, span.start);
	const t1 = cueTime(timing, g.end, span.end);
	const a = ease(t, t0, 0.5);
	const b = ease(t, t0 + 0.2, 0.8);
	const o = out(t, t1, 0.4);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: g.y ?? 360, width: '100%', textAlign: 'center'}}>
				<div style={{...kicker, display: 'inline-block', fontSize: 40, color: palette.amber, clipPath: `inset(0 ${(1 - a) * 100}% 0 0)`, textShadow: '0 2px 18px rgba(0,0,0,0.7)'}}>{g.kicker}</div>
				<div
					style={{
						marginTop: -6,
						fontFamily: fonts.display,
						fontStyle: 'italic',
						fontWeight: 500,
						fontSize: g.size ?? 200,
						lineHeight: 1.1,
						color: palette.ember,
						letterSpacing: `${lerp(-0.04, 0, b)}em`,
						WebkitMaskImage: `linear-gradient(to top, #000 ${b * 120 - 20}%, transparent ${b * 120}%)`,
						maskImage: `linear-gradient(to top, #000 ${b * 120 - 20}%, transparent ${b * 120}%)`,
						transform: `translateY(${(1 - b) * 24}px)`,
						textShadow: '0 4px 36px rgba(0,0,0,0.6)',
						padding: '0 40px 30px',
					}}
				>
					{g.text}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Thin survey ring with cross-hair ticks that marks a clue on the plate (pin with `local`). */
export const EvidenceRing: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const [cx, cy] = g.at;
	const r = g.r ?? 90;
	const c = g.color ?? palette.amber;
	const sweep = ease(t, t0, 0.8, Easing.inOut(Easing.cubic));
	const ticks = ease(t, t0 + 0.5, 0.4);
	const circ = 2 * Math.PI * r;
	return (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0, filter: 'drop-shadow(0 0 6px rgba(0,0,0,0.6))'}}>
			<circle cx={cx} cy={cy} r={r} fill="none" stroke={c} strokeWidth={3} strokeDasharray={circ} strokeDashoffset={circ * (1 - sweep)} transform={`rotate(-90 ${cx} ${cy})`} opacity={0.95} />
			<circle cx={cx} cy={cy} r={r + 16} fill="none" stroke={c} strokeWidth={1.2} strokeDasharray="3 9" opacity={0.45 * ticks} />
			{[0, 90, 180, 270].map((deg) => (
				<line key={deg} x1={cx} y1={cy - r - 8} x2={cx} y2={cy - r - 8 - 22 * ticks} stroke={c} strokeWidth={3} transform={`rotate(${deg} ${cx} ${cy})`} opacity={ticks} />
			))}
		</svg>
	);
};

const MOTES = (() => {
	const r = rng(505);
	return Array.from({length: 46}, () => ({u: r(), v: r(), s: 1.2 + r() * 2.4, sp: 0.015 + r() * 0.03, ph: r() * 6.28}));
})();

/** Dust motes drifting slowly inside a light beam; `poly` = [top-left, top-right, bottom-right, bottom-left]. */
export const DustBeam: React.FC<GraphicProps> = ({g, t}) => {
	const [tl, tr, br, bl] = g.poly as number[][];
	return (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
			{MOTES.map((m, i) => {
				const v = (m.v + t * m.sp) % 1;
				const u = clamp01(m.u + 0.04 * Math.sin(t * 0.6 + m.ph));
				const top = [lerp(tl[0], tr[0], u), lerp(tl[1], tr[1], u)];
				const bot = [lerp(bl[0], br[0], u), lerp(bl[1], br[1], u)];
				const x = lerp(top[0], bot[0], v);
				const y = lerp(top[1], bot[1], v);
				const edge = Math.min(1, v * 6, (1 - v) * 6, u * 5, (1 - u) * 5);
				const o = edge * (0.35 + 0.35 * Math.sin(t * 2.1 + m.ph));
				return <circle key={i} cx={x} cy={y} r={m.s} fill="#fff0cc" opacity={Math.max(0, o)} style={{filter: 'blur(0.6px)'}} />;
			})}
		</svg>
	);
};

/**
 * Line drawing laid over a plate (pin with `local`): each SVG path draws in turn between `start` and `end`
 * (or all at once with `instant`). Closed paths get a faint fill. Optional `dash`, `color`, `width`, `fill`, and a `pulse` cue.
 */
export const GhostLines: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const id = useId().replace(/:/g, '');
	const shapes: {d: string}[] = g.shapes ?? [];
	const c = g.color ?? palette.amber;
	const t0 = cueTime(timing, g.start, 0);
	const t1 = cueTime(timing, g.end, t0 + 2);
	const p = g.instant ? 1 : ease(t, t0, t1 - t0, Easing.inOut(Easing.quad));
	const tp = g.pulse ? cueTime(timing, g.pulse) : -1e9;
	const pulse = ease(t, tp, 0.25) * (1 - ease(t, tp + 0.5, 0.9));
	const n = shapes.length;
	const win = n > 1 ? 0.35 : 1;
	return (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0, opacity: g.opacity ?? 1}}>
			<defs>
				{shapes.map((s, i) => {
					const q = clamp01((p - (n > 1 ? (i / (n - 1)) * (1 - win) : 0)) / win);
					return (
						<mask key={i} id={`${id}-m${i}`} maskUnits="userSpaceOnUse" x={0} y={0} width={W} height={H}>
							<path d={s.d} fill="none" stroke="#fff" strokeWidth={24} pathLength={1} strokeDasharray={`${q} 1`} />
						</mask>
					);
				})}
			</defs>
			<g style={{filter: `drop-shadow(0 0 ${6 + 10 * pulse}px ${c})`}}>
				{shapes.map((s, i) => {
					const q = clamp01((p - (n > 1 ? (i / (n - 1)) * (1 - win) : 0)) / win);
					const closed = /z\s*$/i.test(s.d);
					return (
						<g key={i}>
							{closed && <path d={s.d} fill={c} opacity={(g.fill ?? 0.14) * q} />}
							<path d={s.d} fill="none" stroke={c} strokeWidth={(g.width ?? 3.4) + 2.5 * pulse} strokeDasharray={g.dash} strokeLinejoin="round" strokeLinecap="round" mask={`url(#${id}-m${i})`} opacity={0.9} />
						</g>
					);
				})}
			</g>
		</svg>
	);
};

/** Lesson card: "Don't …" struck out in rust, then the method kicker and a large serif line (*word* = ember italic). */
export const ReverseCard: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const tA = cueTime(timing, g.dont);
	const tStrike = cueTime(timing, g.strike);
	const tK = cueTime(timing, g.startAt);
	const tB = cueTime(timing, g.doAt);
	const top = g.top ?? 380;
	const a = ease(t, tA - 0.05, 0.5) * (1 - ease(t, tK - 0.1, 0.4));
	const strike = ease(t, tStrike, 0.45, Easing.inOut(Easing.quad));
	const k = ease(t, tK - 0.05, 0.5);
	const b = ease(t, tB - 0.05, 0.6);
	const o = out(t, span.end + 0.1, 0.35);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top, width: '100%', textAlign: 'center', opacity: a, transform: `translateY(${(1 - a) * 14}px)`}}>
				<div style={{...kicker, fontSize: 28, color: palette.rust, textShadow: '0 2px 14px rgba(0,0,0,0.7)'}}>Don&apos;t</div>
				<div style={{position: 'relative', display: 'inline-block', marginTop: 10, fontFamily: fonts.display, fontWeight: 600, fontSize: 76, color: palette.parchment, textShadow: '0 4px 30px rgba(0,0,0,0.7)'}}>
					{g.dontText}
					<div style={{position: 'absolute', left: -12, top: '54%', height: 6, width: `calc(${strike * 100}% + 24px)`, background: palette.rust, transform: 'rotate(-1.5deg)'}} />
				</div>
			</div>
			<div style={{position: 'absolute', top, width: '100%', textAlign: 'center'}}>
				<div style={{...kicker, fontSize: 28, color: palette.amber, opacity: k, clipPath: `inset(0 ${(1 - k) * 100}% 0 0)`, textShadow: '0 2px 14px rgba(0,0,0,0.7)'}}>{g.doKicker}</div>
				<div style={{marginTop: 4, fontFamily: fonts.display, fontWeight: 600, fontSize: g.size ?? 124, lineHeight: 1.1, color: palette.parchment, opacity: b, transform: `translateY(${(1 - b) * 18}px)`, textShadow: '0 4px 36px rgba(0,0,0,0.7)', whiteSpace: 'nowrap'}}>
					{(g.doText as string).split(' ').map((w, i) => {
						const em = w.startsWith('*');
						return (
							<span key={i} style={{marginRight: '0.22em', color: em ? palette.ember : undefined, fontStyle: em ? 'italic' : undefined}}>
								{w.replace(/\*/g, '')}
							</span>
						);
					})}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Ember dusk over a daytime plate: deep blue sky, a warm band at the horizon, dark ground. No city lights (the city is a ruin). */
export const EmberDusk: React.FC<GraphicProps> = ({g, t, span}) => {
	const p = g.instant ? 1 : ease(t, span.start - 0.3, 1.4);
	const hz = g.horizon ?? 620;
	const pct = (y: number) => `${(y / H) * 100}%`;
	return (
		<AbsoluteFill
			style={{
				opacity: p,
				background: `linear-gradient(180deg, rgba(10,16,40,0.8) 0%, rgba(34,30,66,0.58) ${pct(hz - 280)}, rgba(206,112,58,0.34) ${pct(hz)}, rgba(24,20,34,0.5) ${pct(hz + 260)}, rgba(6,9,18,0.7) 100%)`,
			}}
		/>
	);
};

export const RUINS: Record<string, React.FC<GraphicProps>> = {
	titleLockup: TitleLockup,
	evidenceRing: EvidenceRing,
	dustBeam: DustBeam,
	ghostLines: GhostLines,
	reverseCard: ReverseCard,
	emberDusk: EmberDusk,
};
