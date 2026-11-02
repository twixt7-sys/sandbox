import React from 'react';
import {AbsoluteFill} from 'remotion';
import {rng} from '../lib/random';
import {ease} from '../lib/timing';
import {H, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Geography graphics (EP06 onward). Snowfall: wind-driven flakes in screen space, three depth layers
 * (near flakes are larger, faster and softer). Seeded and time-driven, so frames are deterministic.
 */

const FLAKES = (() => {
	const r = rng(606);
	return Array.from({length: 260}, () => {
		const z = r();
		return {x: r() * (W + 600) - 300, y: r() * (H + 200), z, ph: r() * 6.28, sway: 8 + r() * 22};
	});
})();

/** `wind` = horizontal px/s (default 260), `density` 0..1, `opacity`. */
export const Snowfall: React.FC<GraphicProps> = ({g, t, span}) => {
	const n = Math.round(FLAKES.length * (g.density ?? 0.7));
	const wind = g.wind ?? 260;
	const o = (g.opacity ?? 0.75) * ease(t, span.start - 0.6, 0.4);
	const loopY = H + 200;
	const loopX = W + 600;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				{FLAKES.slice(0, n).map((f, i) => {
					const speed = 120 + f.z * 260;
					const y = ((f.y + t * speed) % loopY) - 100;
					const x = ((((f.x + t * wind * (0.5 + f.z) + Math.sin(t * 1.3 + f.ph) * f.sway) % loopX) + loopX) % loopX) - 300;
					const r = 1.2 + f.z * 4.2;
					return <ellipse key={i} cx={x} cy={y} rx={r * 1.6} ry={r} fill="#eef3f5" opacity={o * (0.35 + 0.55 * f.z)} style={f.z > 0.8 ? {filter: 'blur(1.5px)'} : undefined} />;
				})}
			</svg>
		</AbsoluteFill>
	);
};

export const TERRAIN: Record<string, React.FC<GraphicProps>> = {
	snowfall: Snowfall,
};
