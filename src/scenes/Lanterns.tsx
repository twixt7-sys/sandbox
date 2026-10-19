import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {FogBank} from '../fx/Fx';
import {lerp} from '../lib/timing';
import {rng} from '../lib/random';
import {H, W} from '../theme';
import {BRIDGE, BridgeShape} from './Bridge';
import {Depth, Ridge, Sky} from './Valley';
import type {SceneProps} from './registry';

type Lantern = {x0: number; z0: number; speed: number; phase: number; hue: number};

const LANTERNS: Lantern[] = (() => {
	const r = rng(99);
	return Array.from({length: 230}, () => ({
		x0: (r() * 2 - 1) * 1.15,
		z0: 1.05 + r() ** 1.15 * 11,
		speed: 0.18 + r() * 0.14,
		phase: r() * Math.PI * 2,
		hue: r(),
	}));
})();

const FIGURES: [number, number][] = [
	[96, 1.0], [140, 0.9], [188, 1.05], [236, 0.95], [292, 1.0], [338, 0.85],
	[742, 0.9], [790, 1.0], [846, 0.95], [902, 1.05], [956, 0.9], [1004, 1.0],
];

/** Payoff: the same bridge at night, lanterns drifting toward the lost crossing. */
export const LanternRiver: React.FC<SceneProps & {soft?: boolean}> = ({progress, soft}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const p = progress;
	const cam = soft ? {x: 0, y: 0, zoom: 1.04} : {x: 0, y: lerp(-40, 30, p), zoom: lerp(1.14, 1.0, p)};
	const {water} = BRIDGE;
	const sky: [number, string][] = [
		[0, '#04080f'],
		[0.35, '#0b1626'],
		[0.5, '#16263a'],
		[0.6, '#22344a'],
	];
	const horizonY = water;
	const project = (x: number, z: number) => ({sx: 540 + (x * 980) / z, sy: horizonY + 880 / z, s: 1 / z});
	const stars = rng(5);
	return (
		<AbsoluteFill style={{backgroundColor: '#04080f'}}>
			<Depth depth={0} cam={cam}>
				<Sky stops={sky} sun={{x: 540, y: 1000, r: 520, color: '#e9a94b', opacity: 0.22}} />
				<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					{Array.from({length: 90}, (_, i) => {
						const x = stars() * W;
						const y = stars() * 760;
						const tw = 0.4 + 0.6 * Math.abs(Math.sin(t * (0.5 + stars()) + i));
						return <circle key={i} cx={x} cy={y} r={0.6 + stars() * 1.3} fill="#dfe8f0" opacity={0.25 + 0.5 * tw * (1 - y / 900)} />;
					})}
				</svg>
			</Depth>
			<Depth depth={0.1} cam={cam}>
				<Ridge seed={11} baseY={890} amp={250} fill="#101c29" rim="#7f95ad" rimOpacity={0.25} rough={0.58} ridged />
				<FogBank y={960} color="120,140,170" opacity={0.12} seed={20} drift={0.2} />
			</Depth>
			<Depth depth={0.2} cam={cam}>
				<Ridge seed={29} baseY={1010} amp={120} fill="#0a121b" />
			</Depth>
			<Depth depth={0.35} cam={cam}>
				<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					<defs>
						<linearGradient id="nwater" x1="0" y1="0" x2="0" y2="1">
							<stop offset="0" stopColor="#1d2c3c" />
							<stop offset="1" stopColor="#03060a" />
						</linearGradient>
						<radialGradient id="lglow">
							<stop offset="0%" stopColor="#ffd38a" stopOpacity={0.9} />
							<stop offset="30%" stopColor="#e9a94b" stopOpacity={0.35} />
							<stop offset="100%" stopColor="#e9a94b" stopOpacity={0} />
						</radialGradient>
						<linearGradient id="lrefl" x1="0" y1="0" x2="0" y2="1">
							<stop offset="0" stopColor="#f4c46e" stopOpacity={0.55} />
							<stop offset="1" stopColor="#f4c46e" stopOpacity={0} />
						</linearGradient>
					</defs>
					<rect x={-200} y={water} width={W + 400} height={H} fill="url(#nwater)" />
					<BridgeShape fill="#05090d" rim="#e9a94b" courses={false} id="night" />
					{/* figures on both banks, each holding a lantern */}
					{FIGURES.map(([x, s], i) => {
						const y = BRIDGE.deckTop - 26;
						const bob = Math.sin(t * 1.3 + i) * 1.2;
						return (
							<g key={i} transform={`translate(${x} ${y}) scale(${s * 1.7})`}>
								<circle cx={0} cy={-38} r={6} fill="#05090d" />
								<path d="M-7,-30 L7,-30 L10,0 L-10,0 Z" fill="#05090d" />
								<circle cx={11} cy={-18 + bob} r={9} fill="url(#lglow)" />
								<circle cx={11} cy={-18 + bob} r={2.4} fill="#ffe2a6" />
							</g>
						);
					})}
					{LANTERNS.map((l, i) => ({l, i, z: l.z0 + t * l.speed}))
						.sort((a, b) => b.z - a.z)
						.map(({l, i, z}) => {
							const converge = 1 - 0.4 * Math.min(1, (z - 1) / 11);
							const x = l.x0 * converge + Math.sin(t * 0.6 + l.phase) * 0.02;
							const {sx, sy, s} = project(x, z);
							if (sy < water + 4) return null;
							const size = 46 * s + 1.2;
							const bob = Math.sin(t * 2 + l.phase) * 3 * s;
							const flicker = 0.85 + 0.15 * Math.sin(t * 9 + l.phase * 3);
							return (
								<g key={i} opacity={Math.min(1, (z - 1) * 2)}>
									<ellipse cx={sx} cy={sy + size * 2.2} rx={size * 0.55} ry={size * 2.6} fill="url(#lrefl)" opacity={0.6 * flicker} />
									<circle cx={sx} cy={sy + bob} r={size * 2.4} fill="url(#lglow)" opacity={0.75 * flicker} />
									<rect x={sx - size / 2} y={sy - size * 0.6 + bob} width={size} height={size * 1.1} rx={size * 0.2} fill={l.hue > 0.8 ? '#ffd9a0' : '#f4b860'} />
								</g>
							);
						})}
				</svg>
				<FogBank y={water + 20} color="233,169,75" opacity={0.08} seed={21} drift={0.3} height={120} />
			</Depth>
			{/* foreground bokeh */}
			<Depth depth={1} cam={cam}>
				<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					<defs>
						<radialGradient id="bokeh">
							<stop offset="0%" stopColor="#f4c46e" stopOpacity={0.5} />
							<stop offset="70%" stopColor="#f4c46e" stopOpacity={0.25} />
							<stop offset="100%" stopColor="#f4c46e" stopOpacity={0} />
						</radialGradient>
					</defs>
					{[
						[120, 1800, 90],
						[930, 1700, 70],
						[780, 1880, 110],
						[300, 1620, 50],
					].map(([x, y, r], i) => (
						<circle key={i} cx={x + Math.sin(t * 0.4 + i) * 10} cy={y - t * 6} r={r} fill="url(#bokeh)" opacity={0.5} />
					))}
				</svg>
			</Depth>
		</AbsoluteFill>
	);
};
