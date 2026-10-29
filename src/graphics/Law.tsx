import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, palette} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Law graphics (EP18, Arc 4): a society read through its laws. `lawText` writes an invented law clause by clause (drawn in
 * code, never generated), then lights each clause with the fear behind it; `glints` lights watchers in a plate's windows.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

type Clause = {n: string; text: string; at: Cue; litAt?: Cue; fear?: string; fearKicker?: string};

/** Rust wax seal at the foot of the law. */
const Seal: React.FC<{size?: number}> = ({size = 74}) => (
	<svg width={size} height={size} viewBox="0 0 40 40">
		<path d="M20 2 C26 3 29 1 32 6 C36 9 39 13 38 20 C39 27 35 31 31 35 C27 39 22 38 18 38 C12 38 8 36 5 31 C1 27 2 22 2 18 C2 12 5 8 9 5 C12 2 16 2 20 2 Z" fill={palette.rust} />
		<circle cx={20} cy={20} r={12.5} fill="none" stroke="#e2a089" strokeOpacity={0.55} strokeWidth={1.4} />
		<path d="M20 11 V29 M13 16 H27 M14.5 24 Q20 30 25.5 24" fill="none" stroke="#e2a089" strokeOpacity={0.7} strokeWidth={1.6} strokeLinecap="round" />
	</svg>
);

/**
 * LawText: a law on a dark vellum card. `kicker` (amber caps, the kingdom) and `title` (serif italic) head it; each of
 * `clauses: [{n, text, at, litAt?, fear?, fearKicker?}]` writes in left to right on `at` with its numeral. On `litAt` the
 * clause warms to ember with a glow and the fear behind it appears beneath (`fearKicker`, default "Fear", then `fear` in
 * serif italic); once any clause is lit the unlit ones dim. `liftAt` shrinks the card up (`liftScale`, default 0.62) and
 * `lessonKicker` / `lessonText` (lines; *word* = ember italic) land beneath it at `lessonAt` (`lessonTop`, default 900).
 * `instant: true` skips the fade-in, for a card carried across a cut. Sits in the diagram block (y 340–1150) on `nightSky`.
 */
export const LawText: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const clauses: Clause[] = g.clauses;
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end, span.end) : span.end;
	const vis = (g.instant ? 1 : ease(t, t0, 0.45)) * out(t, Math.min(tEnd, span.end + 0.25), 0.3);
	const writes = clauses.map((c) => cueTime(timing, c.at));
	const lits = clauses.map((c) => (c.litAt ? cueTime(timing, c.litAt) : 1e9));
	const anyLit = ease(t, Math.min(...lits), 0.4);
	const tLift = g.liftAt ? cueTime(timing, g.liftAt) : 1e9;
	const tLesson = g.lessonAt ? cueTime(timing, g.lessonAt) : 1e9;
	const lift = ease(t, tLift, 0.8);
	const lk = ease(t, tLesson, 0.5);
	const top = g.top ?? 352;
	const head = ease(t, t0 + 0.05, 0.6);
	const sealP = ease(t, writes[writes.length - 1] + 0.5, 0.4, Easing.out(Easing.back(2)));
	const lessonLines: string[] = Array.isArray(g.lessonText) ? g.lessonText : g.lessonText ? [g.lessonText] : [];

	return (
		<AbsoluteFill style={{opacity: vis}}>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse 85% 60% at 50% 42%, rgba(7,14,30,0.6) 0%, rgba(7,14,30,0.85) 100%)'}} />
			<AbsoluteFill style={{transform: `scale(${lerp(1, g.liftScale ?? 0.62, lift)})`, transformOrigin: `540px ${top - 16}px`, opacity: lerp(1, 0.85, lift)}}>
				<div
					style={{
						position: 'absolute',
						left: 96,
						right: 96,
						top,
						padding: '40px 54px 46px',
						background: 'linear-gradient(180deg, rgba(30,27,22,0.92) 0%, rgba(20,19,17,0.94) 100%)',
						border: `2px solid ${palette.amber}`,
						outline: `1px solid rgba(233,169,75,0.35)`,
						outlineOffset: 8,
						boxShadow: '0 20px 60px rgba(0,0,0,0.6), inset 0 0 60px rgba(0,0,0,0.5)',
					}}
				>
					<div style={{textAlign: 'center', opacity: head, transform: `translateY(${(1 - head) * 10}px)`}}>
						<div style={{...kicker, fontSize: 26, color: palette.amber}}>{g.kicker}</div>
						<div style={{marginTop: 6, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 70, lineHeight: 1.05, color: palette.parchment}}>{g.title}</div>
						<div style={{margin: '18px auto 8px', height: 1.5, width: 520 * head, background: palette.amber, opacity: 0.7}} />
					</div>
					{clauses.map((c, i) => {
						const w = ease(t, writes[i], 0.6, Easing.inOut(Easing.quad));
						const lit = ease(t, lits[i], 0.5);
						const flare = ease(t, lits[i], 0.15) * (1 - ease(t, lits[i] + 0.2, 0.8));
						const fear = ease(t, lits[i] + 0.2, 0.5);
						const dim = 1 - 0.55 * anyLit * (1 - lit);
						const col = lit > 0 ? palette.ember : palette.parchment;
						return (
							<div key={i} style={{position: 'relative', marginTop: 26, opacity: dim}}>
								{/* Warm glow behind a lit clause. */}
								<div style={{position: 'absolute', left: -30, right: -30, top: -14, bottom: -14, borderRadius: 18, background: `radial-gradient(ellipse 60% 70% at 40% 50%, rgba(244,196,110,${0.16 * lit + 0.22 * flare}) 0%, rgba(244,196,110,0) 75%)`}} />
								<div style={{display: 'flex', alignItems: 'baseline', gap: 22, clipPath: `inset(-20px ${(1 - w) * 100}% -20px -20px)`}}>
									<div style={{width: 64, flex: 'none', textAlign: 'right', fontFamily: fonts.display, fontWeight: 700, fontSize: 44, color: lit > 0 ? palette.amber : palette.rust}}>{c.n}.</div>
									<div style={{fontFamily: fonts.display, fontWeight: 600, fontSize: g.size ?? 54, lineHeight: 1.08, color: lit > 0.5 ? col : palette.parchment, textShadow: `0 0 ${24 * lit}px rgba(244,196,110,${0.45 * lit})`}}>{c.text}</div>
								</div>
								{c.fear && (
									<div style={{marginLeft: 86, marginTop: 8, display: 'flex', alignItems: 'baseline', gap: 14, opacity: fear, transform: `translateX(${(1 - fear) * -14}px)`}}>
										<div style={{...kicker, fontSize: 21, color: palette.amber, flex: 'none'}}>← {c.fearKicker ?? 'Fear'}</div>
										<div style={{fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 500, fontSize: 42, color: palette.mist}}>{c.fear}</div>
									</div>
								)}
							</div>
						);
					})}
					<div style={{position: 'absolute', right: 40, bottom: -34, opacity: sealP, transform: `scale(${0.6 + 0.4 * sealP}) rotate(-8deg)`}}>
						<Seal />
					</div>
				</div>
			</AbsoluteFill>
			{lessonLines.length > 0 && (
				<div style={{position: 'absolute', top: g.lessonTop ?? 900, left: 60, right: 60, textAlign: 'center', opacity: lk, transform: `translateY(${(1 - lk) * 16}px)`}}>
					{g.lessonKicker && <div style={{...kicker, fontSize: 30, color: palette.amber, textShadow: '0 2px 12px rgba(0,0,0,0.9)'}}>{g.lessonKicker}</div>}
					{lessonLines.map((ln, li) => {
						const lp = ease(t, (g.lessonLineAt?.[li] ? cueTime(timing, g.lessonLineAt[li]) : tLesson + 0.15 + li * 0.25), 0.6);
						return (
							<div key={li} style={{marginTop: li ? 0 : 14, fontFamily: fonts.display, fontWeight: 600, fontSize: g.lessonSize ?? 92, lineHeight: 1.06, color: palette.parchment, opacity: lp, transform: `translateY(${(1 - lp) * 12}px)`, textShadow: '0 4px 30px rgba(0,0,0,0.8)'}}>
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

/**
 * Glints: watchers behind shutters. `points: [[x, y], …]` on the plate (use `local: true`) light one by one from `start`
 * over `dur` (default 1.2 s) as small warm slits with a soft halo; `outAt` dims them all again together. `color` defaults to amber.
 */
export const Glints: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const pts: [number, number][] = g.points;
	const t0 = cueTime(timing, g.start, span.start);
	const dur = g.dur ?? 1.2;
	const tOut = g.outAt ? cueTime(timing, g.outAt) : 1e9;
	const dimTo = g.dimTo ?? 0.15;
	const c = g.color ?? palette.amber;
	const fade = 1 - (1 - dimTo) * ease(t, tOut, 0.6);
	return (
		<AbsoluteFill style={{opacity: out(t, span.end + 0.2, 0.3)}}>
			{pts.map(([x, y], i) => {
				const s = t0 + (i / Math.max(1, pts.length - 1)) * dur;
				const p = ease(t, s, 0.25);
				const pulse = ease(t, s, 0.1) * (1 - ease(t, s + 0.1, 0.5));
				const sz = g.size ?? 1;
				return (
					<div key={i} style={{position: 'absolute', left: x, top: y, opacity: p * fade}}>
						<div style={{position: 'absolute', left: -34 * sz, top: -34 * sz, width: 68 * sz, height: 68 * sz, borderRadius: '50%', background: `radial-gradient(circle, ${c}99 0%, ${c}00 70%)`, transform: `scale(${1 + 0.6 * pulse})`}} />
						<div style={{position: 'absolute', left: -3 * sz, top: -13 * sz, width: 6 * sz, height: 26 * sz, borderRadius: 3, background: palette.ember, boxShadow: `0 0 ${10 * sz}px ${c}`}} />
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

export const LAW: Record<string, React.FC<GraphicProps>> = {
	lawText: LawText,
	glints: Glints,
};
