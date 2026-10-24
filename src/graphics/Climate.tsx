import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Climate graphics (EP09 onward): field-guide callouts pinned to a plate point, used to annotate how a costume,
 * a house or a store answers the weather. A ring on the point, an elbow leader out to the side, a caps label
 * and an optional italic line ("why"). Pin with `local: true` so it rides the camera move.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.2em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

/**
 * Callout: `at: [x, y]`, `label`, optional `note` (serif italic), `side: "left" | "right"` (default right),
 * `reach` (horizontal leader length, default 150), `rise` (vertical offset of the label, default -60), `start` cue,
 * optional `end` cue (else the shot end). `color` defaults to amber. `side: "up"` runs the leader straight up by
 * `-rise`, then `dx` sideways, and centres the label above its end (EP13: a note too wide for either side).
 */
export const Callout: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [x, y] = g.at;
	const c = g.color ?? palette.amber;
	const up = g.side === 'up';
	const dir = g.side === 'left' ? -1 : 1;
	const reach = g.reach ?? 150;
	const rise = g.rise ?? -60;
	const t0 = cueTime(timing, g.start);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.1;
	const ring = ease(t, t0 - 0.05, 0.35, Easing.out(Easing.back(1.8)));
	const lead = ease(t, t0 + 0.1, 0.35);
	const txt = ease(t, t0 + 0.3, 0.4);
	const o = out(t, tEnd, 0.3);
	const ex = up ? x : x + dir * 40;
	const ey = y + rise;
	const lx = up ? x + (g.dx ?? 0) : ex + dir * reach;
	const len = Math.hypot(ex - x, ey - y) || 1;
	const sx = x + ((ex - x) / len) * 20;
	const sy = y + ((ey - y) / len) * 20;
	return (
		<AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<circle cx={x} cy={y} r={7} fill={c} opacity={ring} />
				<circle cx={x} cy={y} r={20 * ring} fill="none" stroke={c} strokeWidth={2.5} opacity={ring} />
				<path
					d={`M${sx},${sy} L${ex},${ey} L${lx},${ey}`}
					fill="none"
					stroke={c}
					strokeWidth={2.5}
					pathLength={1}
					strokeDasharray={`${lead} 1`}
					style={{filter: 'drop-shadow(0 1px 4px rgba(0,0,0,0.8))'}}
				/>
			</svg>
			<div
				style={{
					position: 'absolute',
					...(up ? {bottom: H - ey + 12, left: lx, textAlign: 'center'} : {top: ey - 48, ...(dir > 0 ? {left: lx + 14} : {right: W - lx + 14}), textAlign: dir > 0 ? 'left' : 'right'}),
					whiteSpace: 'nowrap',
					opacity: txt,
					transform: up ? `translate(-50%, ${(1 - txt) * 12}px)` : `translateX(${(1 - txt) * dir * 12}px)`,
				}}
			>
				<div style={{...kicker, fontSize: 28, color: c, textShadow: '0 2px 12px rgba(0,0,0,0.9)'}}>{g.label}</div>
				{g.note && <div style={{marginTop: 2, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 54, lineHeight: 1.05, color: palette.parchment, textShadow: '0 3px 18px rgba(0,0,0,0.9)'}}>{g.note}</div>}
			</div>
		</AbsoluteFill>
	);
};

export const CLIMATE: Record<string, React.FC<GraphicProps>> = {
	callout: Callout,
};
