import React from 'react';
import {AbsoluteFill, Easing, interpolate} from 'remotion';
import {Logo, useBrand} from '../brand/Logo';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, palette} from '../theme';
import type {Graphic, Shot, TimedShot} from '../types';
import {CELESTIAL} from './Celestial';
import {CLIMATE} from './Climate';
import {CRISIS} from './Crisis';
import {RUINS} from './Ruins';
import {SCALE} from './Scale';
import {SURVEY} from './Survey';
import {TERRAIN} from './Terrain';
import {TRADITION} from './Tradition';
import {WEATHER} from './Weather';

export type GraphicProps = {g: Graphic; t: number; shot: Shot; span: TimedShot};

const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

const kickerStyle: React.CSSProperties = {
	fontFamily: fonts.ui,
	fontWeight: 700,
	fontSize: 26,
	letterSpacing: '0.24em',
	textTransform: 'uppercase',
};

/** "Year 1 → 1000" counter with lore names flickering past: the lore dump that means nothing. */
const YearCounter: React.FC<GraphicProps> = ({g, t, shot, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const t1 = cueTime(timing, g.end, t0 + 1.6);
	// Clear the stage for the oversized word if the shot has one.
	const big = shot.graphics.find((x) => x.type === 'oversizedWord');
	const nextBig = big ? cueTime(timing, big.start) + 0.15 : span.end;
	const p = interpolate(t, [t0, t1], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});
	const year = Math.round(lerp(g.from, g.to, p));
	const vis = ease(t, t0 - 0.2, 0.35) * out(t, nextBig, 0.3);
	const labels: string[] = g.labels ?? [];
	const slot = (t1 - t0) / Math.max(1, labels.length);
	return (
		<AbsoluteFill style={{opacity: vis}}>
			<div style={{position: 'absolute', top: 310, width: '100%', textAlign: 'center', color: palette.parchment}}>
				<div style={{...kickerStyle, opacity: 0.7}}>Year</div>
				<div style={{fontFamily: fonts.display, fontWeight: 600, fontSize: 176, lineHeight: 1, fontVariantNumeric: 'tabular-nums', textShadow: '0 4px 30px rgba(0,0,0,0.5)'}}>{year}</div>
			</div>
			<div style={{position: 'absolute', top: 590, left: 140, width: 800, height: 2, background: 'rgba(239,230,210,0.35)'}}>
				<div style={{width: `${p * 100}%`, height: 2, background: palette.amber}} />
				{Array.from({length: 21}, (_, i) => (
					<div key={i} style={{position: 'absolute', left: `${i * 5}%`, top: i % 5 ? -5 : -10, width: 1.5, height: i % 5 ? 10 : 20, background: 'rgba(239,230,210,0.5)'}} />
				))}
			</div>
			{labels.map((label, i) => {
				const s = t0 + i * slot;
				const o = ease(t, s, 0.12) * (1 - ease(t, s + slot * 1.6, 0.25)) * 0.85;
				const x = 140 + ((i + 0.5) / labels.length) * 800;
				return (
					<div
						key={label}
						style={{
							position: 'absolute',
							top: i % 2 ? 616 : 538,
							left: x,
							transform: 'translateX(-50%)',
							whiteSpace: 'nowrap',
							fontFamily: fonts.display,
							fontStyle: 'italic',
							fontWeight: 500,
							fontSize: 34,
							color: palette.mist,
							opacity: o,
						}}
					>
						{label}
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

/** Oversized serif word that lands on a beat ("empty.", "not empty."). */
const OversizedWord: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const reveal = ease(t, t0, 0.9);
	const o = reveal * out(t, span.end + 0.15, 0.45);
	return (
		<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: o}}>
			<div
				style={{
					position: 'absolute',
					top: g.y ?? 640,
					fontFamily: fonts.display,
					fontStyle: 'italic',
					fontWeight: 500,
					fontSize: g.size ?? 230,
					letterSpacing: `${lerp(-0.04, 0.0, reveal)}em`,
					color: palette.parchment,
					WebkitMaskImage: `linear-gradient(to top, #000 ${reveal * 120 - 20}%, transparent ${reveal * 120}%)`,
					maskImage: `linear-gradient(to top, #000 ${reveal * 120 - 20}%, transparent ${reveal * 120}%)`,
					transform: `translateY(${(1 - reveal) * 30}px)`,
					textShadow: '0 4px 36px rgba(0,0,0,0.5)',
					padding: '40px 60px',
				}}
			>
				{g.text}
			</div>
		</AbsoluteFill>
	);
};

/** Word-synced statement; *word* marks the amber italic emphasis. */
const Statement: React.FC<GraphicProps> = ({g, t, shot, span}) => {
	const timing = useTiming();
	const line = timing.lines.find((l) => l.shot === shot.id)!;
	let wi = 0;
	const o = out(t, span.end + 0.2, 0.4);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: 470, left: 84, right: 40}}>
				{(g.lines as string[]).map((row, ri) => (
					<div key={ri} style={{fontFamily: fonts.display, fontWeight: 600, fontSize: 96, lineHeight: 1.06, whiteSpace: 'nowrap', color: palette.parchment, textShadow: '0 4px 40px rgba(0,0,0,0.45)'}}>
						{row.split(' ').map((raw, k) => {
							const word = line.words[wi++];
							const em = raw.startsWith('*');
							const p = word ? ease(t, word.start - 0.06, 0.35) : 1;
							return (
								<span
									key={k}
									style={{
										display: 'inline-block',
										marginRight: '0.24em',
										opacity: 0.12 + 0.88 * p,
										transform: `translateY(${(1 - p) * 18}px)`,
										color: em ? palette.amber : undefined,
										fontStyle: em ? 'italic' : undefined,
									}}
								>
									{raw.replace(/\*/g, '')}
								</span>
							);
						})}
					</div>
				))}
			</div>
		</AbsoluteFill>
	);
};

/** Editorial chip: kicker + one line. Used for LORE / LIVING WORLD. */
const Tag: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const a = ease(t, t0, 0.5);
	const b = ease(t, t0 + 0.15, 0.6);
	const o = out(t, span.end, 0.3);
	return (
		<AbsoluteFill style={{opacity: o}}>
			{/* Starts below the corner logo (top-left, y 236–302). */}
			<div style={{position: 'absolute', top: g.top ?? 336, left: 90}}>
				<div
					style={{
						...kickerStyle,
						display: 'inline-block',
						color: palette.amber,
						border: `1.5px solid ${palette.amber}`,
						padding: '10px 18px 8px',
						clipPath: `inset(0 ${(1 - a) * 100}% 0 0)`,
						background: 'rgba(11,18,22,0.35)',
					}}
				>
					{g.kicker}
				</div>
				<div style={{marginTop: 18, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 500, fontSize: 64, color: palette.parchment, opacity: b, transform: `translateY(${(1 - b) * 14}px)`, textShadow: '0 3px 24px rgba(0,0,0,0.6)'}}>
					{g.text}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Small dated label pinned to a point with a drawn leader line. */
const DateLabel: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const [x, y] = g.at ?? [540, 1010];
	const line = ease(t, t0, 0.5);
	const txt = ease(t, t0 + 0.25, 0.4);
	const o = out(t, span.end, 0.25);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', left: x - 0.75, top: y - 190, width: 1.5, height: 150 * line, background: palette.parchment, opacity: 0.8}} />
			<div style={{position: 'absolute', left: x - 6, top: y - 46, width: 12, height: 12, borderRadius: 6, border: `2px solid ${palette.parchment}`, opacity: line}} />
			<div style={{position: 'absolute', left: 0, right: 0, top: y - 250, textAlign: 'center', ...kickerStyle, fontSize: 30, color: palette.parchment, opacity: txt, textShadow: '0 2px 16px rgba(0,0,0,0.8)'}}>{g.text}</div>
		</AbsoluteFill>
	);
};

/** Running ledger of consequences at the top of the map. */
const Ledger: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const beats = (g.beats ?? []).map((c: any) => cueTime(timing, c));
	const o = ease(t, span.start + 0.3, 0.5) * out(t, span.end, 0.3);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: 236, width: '100%', textAlign: 'center'}}>
				<div style={{...kickerStyle, fontSize: 22, color: palette.fog}}>One event &nbsp;→&nbsp; living consequences</div>
				<div style={{marginTop: 14, display: 'flex', justifyContent: 'center', gap: 46}}>
					{(g.items as string[]).map((item, i) => {
						const p = ease(t, beats[i] ?? 1e9, 0.45);
						return (
							<div key={item} style={{fontFamily: fonts.display, fontWeight: 600, fontSize: 52, color: p > 0.01 ? palette.amber : palette.parchment, opacity: 0.25 + 0.75 * p, transform: `translateY(${(1 - p) * 6}px)`}}>
								{item}
								<div style={{height: 2, marginTop: 2, background: palette.amber, transform: `scaleX(${p})`, transformOrigin: 'left'}} />
							</div>
						);
					})}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Series lockup + CTA. Spoken CTA is shown verbatim here, so captions are off for this shot. */
const Endcard: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const brand = useBrand();
	const t0 = cueTime(timing, g.start);
	const cta = timing.lines.find((l) => l.shot === 'cta');
	const a = ease(t, t0 + 0.1, 0.9);
	const b = ease(t, t0 + 0.5, 0.8);
	const c = ease(t, (cta?.start ?? t0) + 0.05, 0.6);
	const d = ease(t, (cta?.words.find((w) => /building/i.test(w.text))?.start ?? t0 + 2) - 0.05, 0.6);
	const fade = out(t, span.end - 0.55, 0.5);
	return (
		<AbsoluteFill style={{opacity: fade, alignItems: 'center'}}>
			{/* Full logo replaces the corner logo here (the shot sets hideLogoBug). */}
			{brand && (
				<div style={{position: 'absolute', top: 290, width: '100%', display: 'flex', justifyContent: 'center', opacity: a, transform: `translateY(${(1 - a) * 12}px)`}}>
					<Logo brand={brand} height={150} />
				</div>
			)}
			<div style={{position: 'absolute', top: 470, width: '100%', textAlign: 'center', color: palette.parchment}}>
				<div style={{...kickerStyle, fontSize: 24, color: palette.amber, opacity: b}}>{g.episode}</div>
				<div style={{marginTop: 26, fontFamily: fonts.display, fontWeight: 600, fontSize: 104, letterSpacing: `${lerp(0.02, 0.06, a)}em`, opacity: a, textShadow: '0 6px 40px rgba(0,0,0,0.5)'}}>
					{String(g.series).toUpperCase()}
				</div>
				<div style={{margin: '18px auto 0', width: 360 * a, height: 1.5, background: palette.amber, opacity: 0.8}} />
				<div style={{marginTop: 22, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 500, fontSize: 64, opacity: b}}>{g.subtitle}</div>
			</div>
			<div style={{position: 'absolute', top: 1010, width: '100%', textAlign: 'center'}}>
				<div
					style={{
						display: 'inline-block',
						fontFamily: fonts.ui,
						fontWeight: 700,
						fontSize: 46,
						color: '#151a1d',
						background: palette.amber,
						padding: '22px 44px 20px',
						borderRadius: 999,
						opacity: c,
						transform: `translateY(${(1 - c) * 20}px) scale(${0.96 + 0.04 * c})`,
					}}
				>
					{g.cta}
				</div>
				<div style={{marginTop: 30, fontFamily: fonts.ui, fontWeight: 600, fontSize: 42, color: palette.parchment, opacity: d}}>{g.ctaSub}</div>
			</div>
		</AbsoluteFill>
	);
};

export const GRAPHICS: Record<string, React.FC<GraphicProps>> = {
	yearCounter: YearCounter,
	oversizedWord: OversizedWord,
	statement: Statement,
	tag: Tag,
	dateLabel: DateLabel,
	ledger: Ledger,
	endcard: Endcard,
	...CELESTIAL,
	...CRISIS,
	...RUINS,
	...WEATHER,
	...TERRAIN,
	...SURVEY,
	...SCALE,
	...CLIMATE,
	...TRADITION,
};
