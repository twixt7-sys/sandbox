import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, palette} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Ledger graphics (EP23, Arc 5: creative costs of magic). A caster's ledger of the memories she has left, drawn in code
 * on a dark gilt-edged card: each spell strikes one line in rust, the words fade to a ghost and a small mote of light
 * drifts off the page (the memory leaving, shown with tenderness, never injury). The last line can breathe as the
 * choice hangs on it. `fadingName` lets a name painted on a plate fade letter by letter.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const at = (t: number, s: number, dur: number, e?: (x: number) => number) => (Number.isFinite(s) ? ease(t, s, dur, e) : 0);
const tone = (c: string | undefined, fallback: string) => (c ? ((palette as Record<string, string>)[c] ?? c) : fallback);

/** EP23's motif colour: memory, a pale rose. */
export const MEMORY_ROSE = '#f3b9c8';
const CARD_W = 800;
const ROW_TOP = 190;
const ROW_H = 112;

type Line = {num: string; text: string; at?: Cue; strikeAt?: Cue};
type Box = {x: number; y: number; s: number};

/**
 * Memory ledger: a dark card (800 px wide at s 1, height grows with `lines`) at `at: {x, y, s}` (top-left and scale).
 * Header: `kicker` in the motif colour, `title` in serif italic. `lines: [{num, text, at, strikeAt}]`: each line is
 * written left to right on `at` and struck on `strikeAt` (a rust stroke; the words fade to a ghost; a mote of light
 * lifts off the line and drifts away). Cues are absolute, so a corner copy in a later shot shows earlier lines written
 * and struck. A ring of points in the header (one per line) dims to rust as lines are struck. `active` marks the line
 * of the current shot; `hoverAt` makes that line breathe in the motif colour from the cue (the choice). `instant`
 * skips the fade-in; `liftAt` / `lift: {x, y, s}` glide the card; `prices: [{text, at}]` land as pills centred at
 * `pricesTop`; `lessonKicker` / `lessonText` (lines, *word* = ember italic) land at `lessonAt` from `lessonTop`.
 */
export const MemoryLedger: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const lines: Line[] = g.lines ?? [];
	const motif = tone(g.motif, MEMORY_ROSE);
	const t0 = cueTime(timing, g.start, span.start);
	const vis = (g.instant ? 1 : ease(t, t0, 0.5)) * out(t, (g.end ? cueTime(timing, g.end) : span.end) + 0.25, 0.3);
	const base: Box = g.at ?? {x: 140, y: 380, s: 1};
	const tLift = g.liftAt ? cueTime(timing, g.liftAt) : Infinity;
	const lift: Box = g.lift ?? base;
	const mv = at(t, tLift, 0.8, Easing.inOut(Easing.cubic));
	const box = {x: lerp(base.x, lift.x, mv), y: lerp(base.y, lift.y, mv), s: lerp(base.s, lift.s, mv)};
	const wT = lines.map((l) => (l.at ? cueTime(timing, l.at) : -1e9));
	const sT = lines.map((l) => (l.strikeAt ? cueTime(timing, l.strikeAt) : Infinity));
	const tHover = g.hoverAt ? cueTime(timing, g.hoverAt) : Infinity;
	const cardH = ROW_TOP + lines.length * ROW_H + 30;
	const prices: {text: string; at: Cue}[] = g.prices ?? [];
	const lessonLines: string[] = g.lessonText ?? [];
	const tLesson = g.lessonAt ? cueTime(timing, g.lessonAt) : Infinity;
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			{g.dim ? <AbsoluteFill style={{background: `radial-gradient(ellipse 85% 60% at 50% 42%, rgba(7,14,30,${g.dim * 0.7}) 0%, rgba(7,14,30,${g.dim}) 100%)`}} /> : null}
			<div style={{position: 'absolute', left: box.x, top: box.y, width: CARD_W, height: cardH, transformOrigin: '0 0', transform: `scale(${box.s}) rotate(-0.8deg)`}}>
				<div
					style={{
						position: 'absolute',
						inset: 0,
						borderRadius: 10,
						background: 'radial-gradient(ellipse 90% 80% at 40% 30%, #1d2a3a 0%, #131c28 65%, #0c121b 100%)',
						border: '2px solid rgba(233,169,75,0.55)',
						boxShadow: '0 20px 60px rgba(0,0,0,0.7), inset 0 0 70px rgba(0,0,0,0.55), inset 0 0 0 10px rgba(233,169,75,0.06)',
					}}
				/>
				{/* Inner gilt rule. */}
				<div style={{position: 'absolute', inset: 14, borderRadius: 6, border: '1px solid rgba(233,169,75,0.28)'}} />
				<div style={{position: 'absolute', left: 52, top: 44, ...kicker, fontSize: 24, color: motif}}>{g.kicker ?? 'What I remember'}</div>
				<div style={{position: 'absolute', left: 50, top: 76, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 80, lineHeight: '88px', color: palette.parchment}}>{g.title}</div>
				{/* Header ring: one point per memory; struck memories go dark. */}
				<svg width={CARD_W} height={cardH} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					{(() => {
						const cx = 690;
						const cy = 104;
						const r = 50;
						const breathe = 0.85 + 0.15 * Math.sin(t * 3.4);
						return (
							<g>
								<circle cx={cx} cy={cy} r={r} fill="none" stroke={palette.amber} strokeOpacity={0.45} strokeWidth={2} />
								<circle cx={cx} cy={cy} r={r * 0.62} fill="none" stroke={palette.amber} strokeOpacity={0.22} strokeWidth={1} strokeDasharray="3 5" />
								{lines.map((_, i) => {
									const a = -Math.PI / 2 + (i * 2 * Math.PI) / lines.length;
									const x = cx + r * Math.cos(a);
									const y = cy + r * Math.sin(a);
									const gone = at(t, sT[i] + 0.2, 0.5);
									const on = 1 - gone;
									return (
										<g key={i}>
											{on > 0.02 && <circle cx={x} cy={y} r={13} fill={motif} opacity={0.45 * on * breathe} style={{filter: 'blur(5px)'}} />}
											<circle cx={x} cy={y} r={7} fill={on > 0.5 ? motif : 'none'} stroke={on > 0.5 ? motif : palette.rust} strokeWidth={2} opacity={0.5 + 0.5 * on} />
										</g>
									);
								})}
							</g>
						);
					})()}
					<line x1={52} y1={176} x2={CARD_W - 52} y2={176} stroke={palette.amber} strokeOpacity={0.35} strokeWidth={1.5} />
				</svg>
				{lines.map((l, i) => {
					const top = ROW_TOP + i * ROW_H;
					const wp = ease(t, wT[i], 0.7, Easing.inOut(Easing.quad));
					const sp = at(t, sT[i], 0.4, Easing.out(Easing.cubic));
					const ghost = at(t, sT[i] + 0.25, 0.8);
					const isOn = g.active === i;
					const hov = Number.isFinite(tHover) && isOn ? ease(t, tHover, 0.5) * (0.75 + 0.25 * Math.sin((t - tHover) * 4.2)) : 0;
					// The memory leaving: a mote rises from the end of the struck line and drifts up and away.
					const mt = Number.isFinite(sT[i]) ? (t - sT[i] - 0.15) / 1.8 : -1;
					return (
						<div key={i} style={{position: 'absolute', left: 0, top, width: CARD_W, height: ROW_H}}>
							{hov > 0 && <div style={{position: 'absolute', left: 30, right: 30, top: 8, bottom: 8, borderRadius: 12, background: motif, opacity: 0.2 * hov, filter: 'blur(6px)'}} />}
							{isOn && <div style={{position: 'absolute', left: 24, top: 18, width: 6, height: ROW_H - 36, borderRadius: 3, background: motif, opacity: 0.9}} />}
							<div
								style={{
									position: 'absolute',
									left: 48,
									top: 26,
									width: 58,
									height: 58,
									borderRadius: 29,
									border: `2px solid ${sp > 0.5 ? palette.rust : 'rgba(239,230,210,0.7)'}`,
									textAlign: 'center',
									lineHeight: '54px',
									fontFamily: fonts.display,
									fontWeight: 700,
									fontSize: 26,
									color: sp > 0.5 ? palette.rust : palette.parchment,
									opacity: 1 - 0.35 * ghost,
								}}
							>
								{l.num}
							</div>
							<div style={{position: 'absolute', left: 130, right: 52, top: 20, height: 74, borderBottom: `1.5px dashed rgba(239,230,210,${0.32 - 0.2 * wp})`}}>
								<div
									style={{
										position: 'relative',
										display: 'inline-block',
										whiteSpace: 'nowrap',
										fontFamily: fonts.display,
										fontStyle: 'italic',
										fontWeight: 600,
										fontSize: g.lineSize ?? 54,
										lineHeight: '74px',
										color: hov > 0 ? palette.ember : palette.parchment,
										textShadow: hov > 0 ? `0 0 ${24 * hov}px ${motif}` : undefined,
										opacity: 1 - 0.68 * ghost,
										clipPath: `inset(-30px ${(1 - wp) * 100}% -30px -10px)`,
									}}
								>
									{l.text}
									{sp > 0 && <div style={{position: 'absolute', left: -8, right: -12, top: '54%', height: 5, borderRadius: 3, background: palette.rust, transform: `scaleX(${sp}) rotate(-1.2deg)`, transformOrigin: 'left', boxShadow: '0 1px 6px rgba(0,0,0,0.6)'}} />}
									{mt > 0 && mt < 1 && (
										<div
											style={{
												position: 'absolute',
												right: -24,
												top: 26,
												width: 22,
												height: 22,
												borderRadius: 11,
												background: '#fff4f7',
												boxShadow: `0 0 18px 8px ${motif}`,
												opacity: Math.sin(mt * Math.PI) * 0.95,
												transform: `translate(${mt * 120 + Math.sin(mt * 9) * 14}px, ${-mt * 300}px) scale(${1 - 0.5 * mt})`,
											}}
										/>
									)}
								</div>
							</div>
						</div>
					);
				})}
			</div>
			{prices.length > 0 && (
				<div style={{position: 'absolute', top: g.pricesTop ?? 760, left: 70, right: 70, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '18px 20px'}}>
					{prices.map((p, i) => {
						const pp = ease(t, cueTime(timing, p.at), 0.45, Easing.out(Easing.back(1.6)));
						return (
							<div
								key={i}
								style={{
									...kicker,
									fontWeight: 800,
									fontSize: 32,
									color: palette.parchment,
									padding: '14px 30px 12px',
									borderRadius: 40,
									border: `2px solid ${motif}`,
									background: 'rgba(12,18,27,0.75)',
									boxShadow: `0 0 ${22 * pp}px rgba(243,185,200,0.35)`,
									opacity: pp,
									transform: `translateY(${(1 - pp) * 14}px) scale(${0.9 + 0.1 * pp})`,
								}}
							>
								{p.text}
							</div>
						);
					})}
				</div>
			)}
			{lessonLines.length > 0 && (
				<div style={{position: 'absolute', top: g.lessonTop ?? 1000, left: 60, right: 60, textAlign: 'center'}}>
					{g.lessonKicker && <div style={{...kicker, fontSize: 28, color: motif, marginBottom: 18, opacity: ease(t, tLesson - 0.15, 0.5)}}>{g.lessonKicker}</div>}
					{lessonLines.map((ln, li) => {
						const lp = ease(t, tLesson + li * 0.25, 0.6);
						return (
							<div key={li} style={{fontFamily: fonts.display, fontWeight: 600, fontSize: g.lessonSize ?? 84, lineHeight: 1.06, color: palette.parchment, opacity: lp, transform: `translateY(${(1 - lp) * 16}px)`, textShadow: '0 4px 30px rgba(0,0,0,0.8)'}}>
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
 * Fading name (`local`): a name painted on a plate at `at: [x, y]` (centre), fitted to `width` px, `rotate` deg, in
 * `color` (default dark paint) with a faint highlight so it reads as painted on. From `fadeAt` the letters fade one by
 * one over `fadeDur` s (left to right), each blurring and lifting slightly, leaving a faint ghost (`ghost`, default 0.06).
 */
export const FadingName: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [x, y] = g.at;
	const text: string = g.text ?? '';
	const letters = text.split('');
	const t0 = cueTime(timing, g.start, span.start);
	const tFade = g.fadeAt ? cueTime(timing, g.fadeAt) : Infinity;
	const dur = g.fadeDur ?? 1.2;
	const ghost = g.ghost ?? 0.06;
	const size = g.size ?? Math.round((g.width ?? 220) / Math.max(3, letters.length * 0.62));
	const vis = ease(t, t0, 0.3) * out(t, span.end + 0.2, 0.3);
	const col = tone(g.color, '#2b2116');
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, -50%) rotate(${g.rotate ?? 0}deg)`, whiteSpace: 'nowrap'}}>
				{letters.map((ch, i) => {
					const st = tFade + (i / Math.max(1, letters.length - 1)) * (dur - 0.5);
					const f = at(t, st, 0.5);
					return (
						<span
							key={i}
							style={{
								display: 'inline-block',
								fontFamily: fonts.display,
								fontWeight: 700,
								fontSize: size,
								letterSpacing: '0.12em',
								textTransform: 'uppercase',
								color: col,
								textShadow: '0 1px 0 rgba(255,240,210,0.35)',
								opacity: 1 - (1 - ghost) * f,
								filter: f > 0 ? `blur(${f * 3}px)` : undefined,
								transform: `translateY(${-f * 6}px)`,
							}}
						>
							{ch === ' ' ? ' ' : ch}
						</span>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

export const LEDGER = {
	memoryLedger: MemoryLedger,
	fadingName: FadingName,
};
