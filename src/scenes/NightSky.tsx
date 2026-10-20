import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {rng} from '../lib/random';
import {H, palette, W} from '../theme';
import type {SceneProps} from './registry';

const STARS = (() => {
	const r = rng(909);
	return Array.from({length: 140}, () => ({x: r() * W, y: r() * H, s: 0.6 + r() * 1.8, ph: r() * 6.28, o: 0.25 + r() * 0.6}));
})();

/** Clean midnight backdrop for diagrams: star field, stone grain and a slowly turning astrolabe. */
export const NightSky: React.FC<SceneProps> = ({t}) => {
	const cx = 540;
	const cy = 820;
	return (
		<AbsoluteFill style={{background: 'radial-gradient(ellipse 120% 80% at 50% 40%, #0d1a33 0%, #070e1e 55%, #03060e 100%)'}}>
			<Img src={staticFile('textures/paper.png')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', opacity: 0.07}} />
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				{STARS.map((s, i) => (
					<circle key={i} cx={s.x} cy={s.y} r={s.s} fill="#e3e9f7" opacity={s.o * (0.6 + 0.4 * Math.sin(t * 1.7 + s.ph))} />
				))}
				<g transform={`rotate(${t * 2.2} ${cx} ${cy})`} fill="none" stroke={palette.amber} opacity={0.13}>
					<circle cx={cx} cy={cy} r={520} strokeWidth={1.5} />
					<circle cx={cx} cy={cy} r={470} strokeWidth={1} strokeDasharray="4 14" />
					<ellipse cx={cx} cy={cy} rx={520} ry={190} strokeWidth={1} />
					<ellipse cx={cx} cy={cy} rx={190} ry={520} strokeWidth={1} />
					{Array.from({length: 24}, (_, i) => {
						const a = (i / 24) * Math.PI * 2;
						return <line key={i} x1={cx + Math.cos(a) * 520} y1={cy + Math.sin(a) * 520} x2={cx + Math.cos(a) * 545} y2={cy + Math.sin(a) * 545} strokeWidth={2} />;
					})}
				</g>
			</svg>
		</AbsoluteFill>
	);
};
