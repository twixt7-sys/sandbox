import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Scale graphics (EP08 onward): the camera "pulls back" from one picture into the bigger system around it.
 */

/**
 * The previous shot's picture (`src`, a file under public/) starts full-frame, matching that shot's last
 * framing (`from: {s, x, y}`, same meaning as `plateFrame`), shrinks into a framed inset at `to: [cx, cy, w]`
 * on the new shot (the cup lands in the cistern, the caravan on its map route), holds, then fades.
 * `start` (default: shot start), `dur` (shrink, 0.8 s), `hold` (0.5 s), `fade` (0.45 s).
 */
export const PullBack: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start, span.start);
	const dur = g.dur ?? 0.8;
	const e = ease(t, t0, dur, Easing.inOut(Easing.cubic));
	const gone = ease(t, t0 + dur + (g.hold ?? 0.5), g.fade ?? 0.45);
	if (gone >= 1) return null;
	const from = g.from ?? {};
	const [cx, cy, w] = g.to;
	const s = lerp(from.s ?? 1, w / W, e);
	const x = lerp(W / 2 + (from.x ?? 0), cx, e);
	const y = lerp(H / 2 + (from.y ?? 0), cy, e);
	const border = ease(t, t0 + dur * 0.4, dur * 0.6);
	return (
		<AbsoluteFill style={{opacity: 1 - gone}}>
			<div
				style={{
					position: 'absolute',
					left: 0,
					top: 0,
					width: W,
					height: H,
					overflow: 'hidden',
					transformOrigin: '50% 50%',
					transform: `translate(${x - W / 2}px, ${y - H / 2}px) scale(${s})`,
					// Border and shadow are drawn at the inset's size, so divide by the scale.
					outline: `${(3 / s) * border}px solid ${palette.parchment}`,
					boxShadow: `0 0 ${(40 / s) * border}px ${(10 / s) * border}px rgba(0,0,0,${0.55 * border})`,
				}}
			>
				<Img src={staticFile(g.src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
			</div>
		</AbsoluteFill>
	);
};

export const SCALE: Record<string, React.FC<GraphicProps>> = {
	pullBack: PullBack,
};
