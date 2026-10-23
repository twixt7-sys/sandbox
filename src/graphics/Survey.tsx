import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Settlement graphics (EP07 onward): a running tally of reasons across the top of the frame
 * (one icon per reason, filled on its cue, summed on the lesson), and a surveyor's pin that drops
 * onto a plate point, asks "?", and ends in an overlap glow where every reason meets.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.2em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

/** 48×48 line icons, drawn in `c`. Unknown names fall back to a dot. */
const Icon: React.FC<{name: string; c: string; fill: number}> = ({name, c, fill}) => {
	const f = (o = 0.28) => ({fill: c, fillOpacity: o * fill});
	const st = {stroke: c, strokeWidth: 3, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, fill: 'none'};
	switch (name) {
		case 'water':
			return <path d="M24 6 C24 6 10 22 10 31 a14 14 0 0 0 28 0 C38 22 24 6 24 6 Z" {...st} {...f(0.35)} />;
		case 'soil':
			return (
				<g {...st}>
					<path d="M8 40 H40" />
					<path d="M24 40 V18" />
					<path d="M24 26 C16 26 12 20 12 14 C20 14 24 19 24 26 Z" {...f()} />
					<path d="M24 22 C31 22 36 17 36 10 C28 10 24 15 24 22 Z" {...f()} />
				</g>
			);
		case 'defence':
			return <path d="M24 5 L40 11 V24 C40 34 33 40 24 44 C15 40 8 34 8 24 V11 Z" {...st} {...f()} />;
		case 'trade':
			return (
				<g {...st}>
					<path d="M6 40 L24 24 L42 40" />
					<path d="M6 8 L24 24 L42 8" opacity={0.55} />
					<circle cx={24} cy={24} r={6} {...f(0.9)} />
				</g>
			);
		default:
			return <circle cx={24} cy={24} r={10} {...st} {...f()} />;
	}
};

/**
 * Reason tally: `items: [{icon, label, at: Cue}]` in a centred row at `top` (default 336). Slots show dim from `start`
 * (or the shot start); each fills on its cue. `sumAt` + `sum` draws a bracket and a payoff line beneath (*word* = ember italic).
 * Repeat the same graphic on consecutive shots with the same cues: state is computed from episode time, so it carries over.
 */
export const ReasonTally: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const items: {icon: string; label: string; at: any}[] = g.items;
	const t0 = cueTime(timing, g.start, span.start);
	const show = g.instant ? 1 : ease(t, t0, 0.5);
	const o = g.persist ? 1 : out(t, span.end + 0.1, 0.3);
	const top = g.top ?? 336;
	const gap = 150;
	const x0 = W / 2 - ((items.length - 1) * gap) / 2;
	const tSum = g.sumAt ? cueTime(timing, g.sumAt) : 1e9;
	const sum = ease(t, tSum, 0.7);
	return (
		<AbsoluteFill style={{opacity: show * o}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				{items.map((it, i) => {
					const tf = cueTime(timing, it.at);
					const p = ease(t, tf - 0.05, 0.45);
					const pop = ease(t, tf - 0.05, 0.2) * (1 - ease(t, tf + 0.2, 0.5));
					const c = p > 0.02 ? palette.amber : palette.parchment;
					const x = x0 + i * gap;
					return (
						<g key={i} transform={`translate(${x} ${top + 52})`} opacity={0.38 + 0.62 * p}>
							<circle r={46} fill="rgba(8,13,16,0.55)" stroke={c} strokeWidth={2} strokeDasharray={p > 0.02 ? undefined : '4 6'} />
							<circle r={46 + 14 * pop} fill="none" stroke={palette.ember} strokeWidth={2} opacity={pop} />
							<g transform={`translate(-24 -24) scale(${1 + 0.12 * pop})`} style={{transformOrigin: '24px 24px'}}>
								<Icon name={it.icon} c={c} fill={p} />
							</g>
							<text y={78} textAnchor="middle" fill={c} style={{...kicker, fontSize: 22, filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.9))'}}>
								{it.label}
							</text>
						</g>
					);
				})}
				{g.sumAt && (
					<g opacity={sum}>
						<path
							d={`M${x0 - 40},${top + 150} Q${x0 - 40},${top + 172} ${x0},${top + 172} L${W / 2 - 18},${top + 172} L${W / 2},${top + 190} L${W / 2 + 18},${top + 172} L${x0 + (items.length - 1) * gap},${top + 172} Q${x0 + (items.length - 1) * gap + 40},${top + 172} ${x0 + (items.length - 1) * gap + 40},${top + 150}`}
							fill="none"
							stroke={palette.amber}
							strokeWidth={2.5}
							pathLength={1}
							strokeDasharray={`${sum} 1`}
						/>
					</g>
				)}
			</svg>
			{g.sumAt && (
				<div style={{position: 'absolute', top: top + 210, width: '100%', textAlign: 'center', opacity: sum, transform: `translateY(${(1 - sum) * 16}px)`}}>
					{g.sumKicker && <div style={{...kicker, fontSize: 26, color: palette.amber, textShadow: '0 2px 14px rgba(0,0,0,0.8)'}}>{g.sumKicker}</div>}
					<div style={{marginTop: 6, fontFamily: fonts.display, fontWeight: 600, fontSize: g.size ?? 96, lineHeight: 1.08, color: palette.parchment, textShadow: '0 4px 34px rgba(0,0,0,0.8)'}}>
						{(g.sum as string).split(' ').map((w, i) => {
							const em = w.startsWith('*') || w.endsWith('*');
							return (
								<span key={i} style={{marginRight: '0.22em', color: em ? palette.ember : undefined, fontStyle: em ? 'italic' : undefined}}>
									{w.replace(/\*/g, '')}
								</span>
							);
						})}
					</div>
				</div>
			)}
		</AbsoluteFill>
	);
};

/**
 * Surveyor's pin dropped onto a plate point (pin with `local`): `at`, `start` (drop), optional `ask` cue (a "?" badge),
 * optional `glowAt` cue (converging rings + warm glow: every reason meets here), `fadeAt` cue (everything fades),
 * `stake: false` (glow only, e.g. carried over onto the finished city). `color` defaults to ember.
 */
export const SurveyPin: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const [x, y] = g.at;
	const c = g.color ?? palette.ember;
	const t0 = cueTime(timing, g.start);
	const drop = ease(t, t0, 0.55, Easing.out(Easing.back(1.6)));
	const vis = ease(t, t0, 0.15);
	const tAsk = g.ask ? cueTime(timing, g.ask) : 1e9;
	const ask = ease(t, tAsk, 0.4) * (g.glowAt ? 1 - ease(t, cueTime(timing, g.glowAt) - 0.2, 0.3) : 1);
	const tGlow = g.glowAt ? cueTime(timing, g.glowAt) : 1e9;
	const glow = ease(t, tGlow, 0.9);
	const pulse = (Math.sin((t - t0) * 3) + 1) / 2;
	const fade = g.fadeAt ? 1 - ease(t, cueTime(timing, g.fadeAt), 0.8) : 1;
	const stake = g.stake === false ? 0 : 1;
	return (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible', opacity: fade}}>
			<defs>
				<radialGradient id="survey-glow">
					<stop offset="0%" stopColor="#ffe2a0" stopOpacity={1} />
					<stop offset="40%" stopColor={palette.amber} stopOpacity={0.55} />
					<stop offset="100%" stopColor={palette.amber} stopOpacity={0} />
				</radialGradient>
			</defs>
			{glow > 0 && <circle cx={x} cy={y} r={70 + 190 * glow} fill="url(#survey-glow)" opacity={glow} style={{mixBlendMode: 'screen'}} />}
			{glow > 0 &&
				[0, 1, 2].map((k) => {
					const q = ease(t, tGlow + k * 0.18, 1.1, Easing.out(Easing.cubic));
					return <circle key={k} cx={x} cy={y} r={lerp(320, 30, q)} fill="none" stroke={c} strokeWidth={3.5} opacity={Math.min(1, q * (1 - q) * 4)} />;
				})}
			<ellipse cx={x} cy={y} rx={22 + 10 * pulse * vis} ry={(22 + 10 * pulse * vis) * 0.4} fill="none" stroke={c} strokeWidth={2} opacity={vis * 0.7 * stake} />
			<g transform={`translate(${x} ${y - (1 - drop) * 220})`} opacity={vis * stake}>
				<line x1={0} y1={0} x2={0} y2={-70} stroke={palette.parchment} strokeWidth={4} strokeLinecap="round" />
				<path d="M0,-70 L40,-58 L0,-44 Z" fill={c} />
			</g>
			<g transform={`translate(${x + 58} ${y - 120})`} opacity={ask}>
				<circle r={30} fill="rgba(8,13,16,0.7)" stroke={c} strokeWidth={2.5} />
				<text y={13} textAnchor="middle" fill={c} style={{fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 44}}>
					?
				</text>
			</g>
		</svg>
	);
};

export const SURVEY: Record<string, React.FC<GraphicProps>> = {
	reasonTally: ReasonTally,
	surveyPin: SurveyPin,
};
