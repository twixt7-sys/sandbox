import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {rng} from '../lib/random';
import {H, W} from '../theme';
import type {SceneProps} from './registry';

const BOKEH = (() => {
	const r = rng(321);
	return Array.from({length: 26}, () => ({x: r() * W, y: 500 + r() * 1500, rad: 30 + r() ** 2 * 140, speed: 8 + r() * 22, o: 0.15 + r() * 0.35}));
})();

/** Lantern bokeh behind the series lockup (the lockup itself is a graphic). */
export const EndCard: React.FC<SceneProps> = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	return (
		<AbsoluteFill style={{background: 'linear-gradient(180deg, #070c14 0%, #0d1824 55%, #1a2230 100%)'}}>
			<svg width={W} height={H}>
				<defs>
					<radialGradient id="eb">
						<stop offset="0%" stopColor="#f4c46e" stopOpacity={0.55} />
						<stop offset="65%" stopColor="#e9a94b" stopOpacity={0.18} />
						<stop offset="100%" stopColor="#e9a94b" stopOpacity={0} />
					</radialGradient>
				</defs>
				{BOKEH.map((b, i) => (
					<circle key={i} cx={b.x + Math.sin(t * 0.5 + i) * 12} cy={b.y - t * b.speed} r={b.rad} fill="url(#eb)" opacity={b.o} />
				))}
			</svg>
		</AbsoluteFill>
	);
};
