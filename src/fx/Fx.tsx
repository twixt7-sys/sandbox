import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {H, W} from '../theme';

/** Film grain from pre-baked noise tiles (an SVG turbulence filter per frame is ~10x slower to render). */
export const Grain: React.FC<{opacity?: number}> = ({opacity = 0.07}) => {
	const frame = useCurrentFrame();
	const i = frame % 6;
	const dx = ((frame * 37) % 7) - 3;
	const dy = ((frame * 53) % 7) - 3;
	return (
		<AbsoluteFill style={{opacity, pointerEvents: 'none'}}>
			<Img src={staticFile(`textures/grain${i}.png`)} style={{width: W + 8, height: H + 8, transform: `translate(${dx - 4}px, ${dy - 4}px)`}} />
		</AbsoluteFill>
	);
};

export const Vignette: React.FC<{strength?: number}> = ({strength = 0.6}) => (
	<AbsoluteFill
		style={{
			pointerEvents: 'none',
			background: `radial-gradient(ellipse 85% 70% at 50% 46%, rgba(0,0,0,0) 55%, rgba(4,8,10,${strength}) 100%)`,
		}}
	/>
);

/** Series grade: warm top, cool shadows, slightly lifted blacks (plain alpha layers: blend modes are slow to render). */
export const Grade: React.FC = () => (
	<>
		<AbsoluteFill style={{pointerEvents: 'none', background: 'linear-gradient(180deg, rgba(233,169,75,0.035) 0%, rgba(0,0,0,0) 45%, rgba(16,48,58,0.12) 100%)'}} />
		<AbsoluteFill style={{pointerEvents: 'none', background: 'rgba(14,22,26,0.06)'}} />
	</>
);

/** Soft fog made of radial-gradient ellipses (cheap to render, no blur filters). */
export const FogBank: React.FC<{
	y: number;
	color?: string;
	opacity?: number;
	count?: number;
	drift?: number;
	height?: number;
	seed?: number;
}> = ({y, color = '214,223,224', opacity = 0.45, count = 6, drift = 0.6, height = 260, seed = 1}) => {
	const frame = useCurrentFrame();
	return (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
			<defs>
				<radialGradient id={`fog-${seed}`}>
					<stop offset="0%" stopColor={`rgb(${color})`} stopOpacity={1} />
					<stop offset="60%" stopColor={`rgb(${color})`} stopOpacity={0.45} />
					<stop offset="100%" stopColor={`rgb(${color})`} stopOpacity={0} />
				</radialGradient>
			</defs>
			{Array.from({length: count}, (_, i) => {
				const span = W + 900;
				const x = ((i * span) / count + frame * drift * (1 + (i % 3) * 0.3) + seed * 137) % span - 450;
				const w = 520 + ((i * 97 + seed * 31) % 260);
				return (
					<ellipse
						key={i}
						cx={x}
						cy={y + Math.sin(i * 1.7 + seed) * height * 0.25}
						rx={w}
						ry={height * (0.55 + ((i * 13) % 5) * 0.08)}
						fill={`url(#fog-${seed})`}
						opacity={opacity}
					/>
				);
			})}
		</svg>
	);
};
