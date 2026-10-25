import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Tradition graphics (EP12 onward): a festival and the punishment it grew from, shown as a then/now mirror.
 * `eraShift` dissolves the plate into its matching plate from another century, `originLedger` pairs each
 * festive custom with its original purpose in two columns, and `headCount` counts figures at dawn and leaves
 * the missing ones as empty outlines.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

/**
 * Era shift: the matching plate from another century (`src`, e.g. "ep12/plates/then.jpg") laid over this shot's plate.
 * `from` is its opacity at the shot start (0 or 1); each of `keys: [{at: Cue, to, dur}]` fades it to `to`.
 * Mid-fade it softens slightly (`blur`, default 6 px) and cools or warms with `tint`, so the change reads as time, not a cut.
 * Use `local: true` so it shares the plate's camera move and the two plates stay registered.
 */
export const EraShift: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	let o = g.from ?? 0;
	let mid = 0;
	for (const k of g.keys ?? []) {
		const t0 = cueTime(timing, k.at);
		const dur = k.dur ?? 1.0;
		const p = ease(t, t0, dur, Easing.inOut(Easing.cubic));
		mid = Math.max(mid, Math.sin(Math.PI * p));
		o = lerp(o, k.to, p);
	}
	if (o <= 0.001 && mid <= 0.001) return null;
	const blur = (g.blur ?? 6) * mid;
	return (
		<AbsoluteFill style={{opacity: o}}>
			<Img src={staticFile(g.src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: blur > 0.05 ? `blur(${blur}px)` : undefined}} />
			{mid > 0.01 && <AbsoluteFill style={{background: g.tint ?? 'rgba(170,200,220,0.18)', opacity: mid, mixBlendMode: 'screen'}} />}
		</AbsoluteFill>
	);
};

/** 48×48 line icons for customs. */
const CustomIcon: React.FC<{name: string; c: string}> = ({name, c}) => {
	const st = {stroke: c, strokeWidth: 3, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, fill: 'none'};
	switch (name) {
		case 'bell':
			return (
				<g {...st}>
					<path d="M24 6 V10" />
					<path d="M14 34 C14 22 15 12 24 12 C33 12 34 22 34 34 L38 38 H10 Z" fill={c} fillOpacity={0.2} />
					<circle cx={24} cy={42} r={3} />
				</g>
			);
		case 'fire':
			return (
				<g {...st}>
					<path d="M24 6 C30 14 36 20 34 30 C33 37 28 41 24 41 C19 41 14 37 14 30 C14 23 19 20 20 14 C23 18 24 21 24 24 C27 20 27 12 24 6 Z" fill={c} fillOpacity={0.2} />
					<path d="M10 44 L38 38 M10 38 L38 44" />
				</g>
			);
		case 'dawn':
			// Gate arch with the sun rising behind it.
			return (
				<g {...st}>
					<path d="M6 42 H42" />
					<path d="M14 42 V24 A10 10 0 0 1 34 24 V42" />
					<path d="M19 42 V27 A5 5 0 0 1 29 27 V42" fill={c} fillOpacity={0.25} />
					<path d="M24 4 V9 M9 12 L12.5 15.5 M39 12 L35.5 15.5" />
				</g>
			);
		default:
			return <circle cx={24} cy={24} r={10} {...st} />;
	}
};

/**
 * Origin ledger: a two-column card at `top` (default 336). Header kickers `now` and `then`; `rows: [{icon, now, then,
 * nowAt, thenAt}]`. The NOW side of each row writes in on `nowAt`; on `thenAt` an amber link draws across and the
 * original purpose appears on the THEN side in ember italic, while the NOW text dims. `thenHeaderAt` reveals the THEN
 * column header (default: the first `thenAt`). Repeat it on consecutive shots with the same cues; state comes from
 * episode time. `instant: true` skips the fade-in (for a carried-over ledger).
 */
export const OriginLedger: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const rows: {icon: string; now: string; then: string; nowAt?: any; thenAt?: any}[] = g.rows;
	const top = g.top ?? 336;
	const rowH = g.rowH ?? 116;
	const t0 = cueTime(timing, g.start, span.start);
	const show = g.instant ? 1 : ease(t, t0, 0.45);
	const o = out(t, g.end ? cueTime(timing, g.end) : span.end + 0.1, 0.3);
	const thenTimes = rows.map((r) => (r.thenAt ? cueTime(timing, r.thenAt) : 1e9));
	const thenHead = ease(t, g.thenHeaderAt ? cueTime(timing, g.thenHeaderAt) : Math.min(...thenTimes) - 0.3, 0.4);
	const midX = W / 2;
	const card = {left: 70, right: W - 70};
	return (
		<AbsoluteFill style={{opacity: show * o}}>
			{/* Dark card behind the ledger so it reads over a busy festival plate. */}
			<div
				style={{
					position: 'absolute',
					left: card.left,
					width: card.right - card.left,
					top: top,
					height: 78 + rows.length * rowH,
					background: 'linear-gradient(180deg, rgba(8,13,16,0.72), rgba(8,13,16,0.5))',
					borderTop: `1.5px solid rgba(233,169,75,0.6)`,
					borderBottom: `1.5px solid rgba(233,169,75,0.3)`,
				}}
			/>
			<div style={{position: 'absolute', top: top + 22, left: card.left + 30, ...kicker, fontSize: 24, color: palette.amber}}>{g.nowLabel ?? 'Now'}</div>
			<div style={{position: 'absolute', top: top + 22, left: midX + 40, ...kicker, fontSize: 24, color: palette.ember, opacity: thenHead, transform: `translateX(${(1 - thenHead) * 14}px)`}}>
				{g.thenLabel ?? 'Then'}
			</div>
			{/* Centre rule between the columns, drawn with the THEN header. */}
			<div style={{position: 'absolute', left: midX - 0.75, top: top + 16, width: 1.5, height: (62 + rows.length * rowH - 30) * thenHead, background: 'rgba(239,230,210,0.25)'}} />
			{rows.map((r, i) => {
				const y = top + 78 + i * rowH;
				const pn = r.nowAt ? ease(t, cueTime(timing, r.nowAt) - 0.08, 0.45) : 1;
				const tt = thenTimes[i];
				const link = ease(t, tt - 0.1, 0.35);
				const pt = ease(t, tt + 0.1, 0.45);
				const c = pt > 0.02 ? palette.ember : palette.amber;
				return (
					<React.Fragment key={i}>
						<svg width={56} height={56} viewBox="0 0 48 48" style={{position: 'absolute', left: card.left + 24, top: y + (rowH - 56) / 2 - 6, opacity: pn}}>
							<CustomIcon name={r.icon} c={c} />
						</svg>
						<div
							style={{
								position: 'absolute',
								left: card.left + 96,
								width: midX - card.left - 120,
								top: y + 10,
								fontFamily: fonts.display,
								fontWeight: 600,
								fontSize: 50,
								lineHeight: 1.05,
								color: palette.parchment,
								opacity: pn * lerp(1, 0.55, pt),
								transform: `translateY(${(1 - pn) * 12}px)`,
								whiteSpace: 'nowrap',
							}}
						>
							{r.now}
						</div>
						<svg width={W} height={rowH} style={{position: 'absolute', left: 0, top: y, overflow: 'visible'}}>
							<path
								d={`M${midX - 30},${rowH / 2 - 6} L${midX + 22},${rowH / 2 - 6}`}
								stroke={palette.amber}
								strokeWidth={2.5}
								pathLength={1}
								strokeDasharray={`${link} 1`}
								opacity={link}
							/>
							<path d={`M${midX + 14},${rowH / 2 - 14} L${midX + 24},${rowH / 2 - 6} L${midX + 14},${rowH / 2 + 2}`} fill="none" stroke={palette.amber} strokeWidth={2.5} opacity={link > 0.9 ? 1 : 0} />
						</svg>
						<div
							style={{
								position: 'absolute',
								left: midX + 40,
								width: card.right - midX - 60,
								top: y + 6,
								fontFamily: fonts.display,
								fontStyle: 'italic',
								fontWeight: 600,
								fontSize: g.thenSize ?? 50,
								lineHeight: 1.0,
								color: palette.ember,
								opacity: pt,
								transform: `translateX(${(1 - pt) * 16}px)`,
								textShadow: '0 2px 18px rgba(0,0,0,0.8)',
							}}
						>
							{r.then}
						</div>
					</React.Fragment>
				);
			})}
		</AbsoluteFill>
	);
};

/** Small hooded figure, 40×56, drawn in `c`; `lit` fills it. */
const Figure: React.FC<{c: string; lit: number; dashed?: boolean}> = ({c, lit, dashed}) => (
	<g stroke={c} strokeWidth={2.5} strokeLinejoin="round" fill={c} fillOpacity={0.85 * lit} strokeDasharray={dashed ? '4 5' : undefined}>
		<path d="M20 2 C12 2 9 9 10 16 C6 22 3 34 2 54 H38 C37 34 34 22 30 16 C31 9 28 2 20 2 Z" />
	</g>
);

/**
 * Head count: `rows` × `cols` hooded figures centred on `y` (default 980), lit one by one from `start` over `dur` s
 * (amber), with the last `missing` left as dashed empty outlines that dim further: absence, never shown harm.
 * Optional `kicker` above (amber caps) and `note` below (serif italic) on `noteAt`.
 */
export const HeadCount: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const cols = g.cols ?? 12;
	const rows = g.rows ?? 2;
	const n = cols * rows;
	const missing = g.missing ?? 4;
	const t0 = cueTime(timing, g.start, span.start);
	const dur = g.dur ?? 1.1;
	const show = ease(t, t0 - 0.3, 0.35) * out(t, span.end + 0.1, 0.3);
	const gap = g.gap ?? 64;
	const y = g.y ?? 980;
	const x0 = W / 2 - ((cols - 1) * gap) / 2;
	const done = ease(t, t0 + dur * 0.7, 0.5);
	const noteP = g.noteAt ? ease(t, cueTime(timing, g.noteAt), 0.5) : 0;
	return (
		<AbsoluteFill style={{opacity: show}}>
			{g.kicker && <div style={{position: 'absolute', top: y - rows * 40 - 80, width: '100%', textAlign: 'center', ...kicker, fontSize: 26, color: palette.amber, textShadow: '0 2px 14px rgba(0,0,0,0.9)'}}>{g.kicker}</div>}
			<svg width={W} height={rows * 80 + 40} style={{position: 'absolute', left: 0, top: y - rows * 40 - 20, overflow: 'visible', filter: 'drop-shadow(0 2px 8px rgba(0,0,0,0.85))'}}>
				{Array.from({length: n}, (_, i) => {
					const r = Math.floor(i / cols);
					const col = i % cols;
					const counted = n - missing;
					const isMissing = i >= counted;
					const ti = t0 + (i / Math.max(1, counted - 1)) * dur;
					const lit = isMissing ? 0 : ease(t, ti, 0.12);
					const pop = isMissing ? 0 : ease(t, ti, 0.08) * (1 - ease(t, ti + 0.1, 0.3));
					const c = isMissing ? palette.mist : palette.amber;
					const op = isMissing ? lerp(0.0, lerp(0.9, 0.6, ease(t, t0 + dur + 0.9, 0.8)), done) : 0.35 + 0.65 * lit;
					return (
						<g key={i} transform={`translate(${x0 + col * gap - 20 * (1 + 0.15 * pop)} ${20 + r * 80 - 4 * pop}) scale(${1 + 0.15 * pop})`} opacity={op}>
							<Figure c={c} lit={lit} dashed={isMissing} />
						</g>
					);
				})}
			</svg>
			{g.note && (
				<div style={{position: 'absolute', top: y + rows * 40 + 24, width: '100%', textAlign: 'center', fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 60, color: palette.ember, opacity: noteP, transform: `translateY(${(1 - noteP) * 12}px)`, textShadow: '0 3px 20px rgba(0,0,0,0.9)'}}>
					{g.note}
				</div>
			)}
		</AbsoluteFill>
	);
};

export const TRADITION = {
	eraShift: EraShift,
	originLedger: OriginLedger,
	headCount: HeadCount,
};
