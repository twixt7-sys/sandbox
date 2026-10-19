import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {FogBank} from '../fx/Fx';
import {lerp} from '../lib/timing';
import {H, W} from '../theme';
import {Depth, Ridge, Sky} from './Valley';
import type {SceneProps} from './registry';

/** Bridge geometry (shared by the dawn and night shots so the structure stays identical). */
export const BRIDGE = {
	deckTop: 930,
	deckBottom: 985,
	water: 1165,
	gapL: 430,
	gapR: 650,
	piers: [-60, 170, 860, 1100],
};

const halfPath = (side: 'L' | 'R') => {
	const {deckTop, water, gapL, gapR} = BRIDGE;
	// Outer silhouette with a jagged broken end.
	if (side === 'L') {
		return `M-200,${deckTop - 26} L${gapL - 30},${deckTop - 26} L${gapL - 22},${deckTop - 8} L${gapL + 4},${deckTop + 6} L${gapL - 10},${deckTop + 34} L${gapL + 8},${deckTop + 58} L${gapL - 16},${deckTop + 92} L${gapL - 40},${deckTop + 110} L${gapL - 52},${water + 4} L-200,${water + 4} Z`;
	}
	return `M${W + 200},${deckTop - 26} L${gapR + 26},${deckTop - 26} L${gapR + 14},${deckTop - 2} L${gapR - 6},${deckTop + 18} L${gapR + 12},${deckTop + 46} L${gapR - 4},${deckTop + 70} L${gapR + 30},${deckTop + 104} L${gapR + 48},${water + 4} L${W + 200},${water + 4} Z`;
};

const arches = () => {
	const {deckBottom, water} = BRIDGE;
	// Arch openings between surviving piers (semi-ellipses) — punched out with evenodd.
	const spans: [number, number][] = [
		[-240, -60 - 24],
		[-60 + 24, 170 - 24],
		[170 + 24, 380],
		[700, 860 - 24],
		[860 + 24, 1100 - 24],
		[1100 + 24, 1300],
	];
	return spans
		.map(([a, b]) => {
			const r = (b - a) / 2;
			const crown = deckBottom + 30;
			return `M${a},${water + 6} L${a},${crown + r * 0.9} A${r},${r * 0.9} 0 0 1 ${b},${crown + r * 0.9} L${b},${water + 6} Z`;
		})
		.join(' ');
};

export const BridgeShape: React.FC<{fill: string; rim?: string; courses?: boolean; id: string}> = ({fill, rim, courses = true, id}) => {
	const {deckTop, water, gapL, gapR} = BRIDGE;
	const body = `${halfPath('L')} ${halfPath('R')} ${arches()}`;
	return (
		<g>
			<defs>
				<clipPath id={`${id}-clip`}>
					<path d={body} clipRule="evenodd" />
				</clipPath>
			</defs>
			<path d={body} fill={fill} fillRule="evenodd" />
			{courses && (
				<g clipPath={`url(#${id}-clip)`} opacity={0.18}>
					{Array.from({length: 16}, (_, i) => (
						<line key={i} x1={-200} x2={W + 200} y1={deckTop + 6 + i * 15} y2={deckTop + 6 + i * 15} stroke="#c8bba0" strokeWidth={1} />
					))}
					{Array.from({length: 60}, (_, i) => (
						<line key={`v${i}`} x1={-180 + i * 24 + (i % 2) * 12} x2={-180 + i * 24 + (i % 2) * 12} y1={deckTop + 6 + (i % 8) * 15} y2={deckTop + 21 + (i % 8) * 15} stroke="#c8bba0" strokeWidth={1} />
					))}
				</g>
			)}
			{/* Parapet blocks */}
			{Array.from({length: 26}, (_, i) => {
				const x = -180 + i * 52;
				if (x > gapL - 40 && x < gapR + 20) return null;
				return <rect key={i} x={x} y={deckTop - 46} width={30} height={22} fill={fill} />;
			})}
			{/* Broken pier stumps in the gap */}
			<path d={`M${gapL + 30},${water + 6} L${gapL + 30},${deckTop + 150} L${gapL + 46},${deckTop + 128} L${gapL + 60},${deckTop + 160} L${gapL + 74},${deckTop + 138} L${gapL + 78},${water + 6} Z`} fill={fill} />
			<path d={`M${gapR - 82},${water + 6} L${gapR - 80},${deckTop + 172} L${gapR - 66},${deckTop + 150} L${gapR - 52},${deckTop + 176} L${gapR - 36},${deckTop + 158} L${gapR - 34},${water + 6} Z`} fill={fill} />
			{rim && (
				<>
					<path d={halfPath('L')} fill="none" stroke={rim} strokeOpacity={0.55} strokeWidth={2} />
					<path d={halfPath('R')} fill="none" stroke={rim} strokeOpacity={0.55} strokeWidth={2} />
				</>
			)}
		</g>
	);
};

/** Lore: the broken bridge at cold dawn, pushing in toward the gap. */
export const Bridge: React.FC<SceneProps> = ({progress}) => {
	const frame = useCurrentFrame();
	const p = progress;
	const cam = {x: 0, y: lerp(0, -30, p), zoom: lerp(1.0, 1.16, p)};
	const {water, gapL, gapR} = BRIDGE;
	const sky: [number, string][] = [
		[0, '#121f29'],
		[0.3, '#2b4352'],
		[0.45, '#73868b'],
		[0.53, '#c9b08a'],
	];
	return (
		<AbsoluteFill style={{backgroundColor: '#121f29'}}>
			<Depth depth={0} cam={cam}>
				<Sky stops={sky} sun={{x: 540, y: 960, r: 460, color: '#f4c78a', opacity: 0.6}} />
			</Depth>
			<Depth depth={0.1} cam={cam}>
				<Ridge seed={11} baseY={890} amp={250} fill="#7c8e95" rim="#f2c98c" rimOpacity={0.4} rough={0.58} ridged />
				<FogBank y={930} opacity={0.4} seed={8} drift={0.3} />
			</Depth>
			<Depth depth={0.2} cam={cam}>
				<Ridge seed={29} baseY={1010} amp={120} fill="#4f646d" />
				<FogBank y={1060} opacity={0.5} seed={9} drift={0.4} height={200} />
			</Depth>
			<Depth depth={0.4} cam={cam}>
				<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					<defs>
						<linearGradient id="bwater" x1="0" y1="0" x2="0" y2="1">
							<stop offset="0" stopColor="#a49c86" />
							<stop offset="0.2" stopColor="#5f747b" />
							<stop offset="1" stopColor="#0e171b" />
						</linearGradient>
						<linearGradient id="reflFade" x1="0" y1="0" x2="0" y2="1">
							<stop offset="0" stopColor="#fff" stopOpacity={0.5} />
							<stop offset="0.5" stopColor="#fff" stopOpacity={0} />
						</linearGradient>
						<mask id="reflMask">
							<rect x={-200} y={water} width={W + 400} height={H} fill="url(#reflFade)" />
						</mask>
					</defs>
					<rect x={-200} y={water} width={W + 400} height={H - water + 200} fill="url(#bwater)" />
					<g mask="url(#reflMask)" transform={`translate(0 ${water * 2}) scale(1 -1)`}>
						<BridgeShape fill="#0d1519" courses={false} id="refl" />
					</g>
					<BridgeShape fill="#1d2a30" rim="#f3c98e" id="main" />
					{/* fallen masonry in the shallows */}
					{[
						[gapL + 10, 34, 18],
						[gapL + 95, 52, 24],
						[gapR - 120, 40, 20],
						[gapR - 20, 30, 14],
					].map(([x, w, h], i) => (
						<g key={i}>
							<path d={`M${x},${water + 14} L${x + 6},${water + 14 - h} L${x + w - 4},${water + 10 - h} L${x + w},${water + 14} Z`} fill="#141e22" />
							<line x1={x - 8} x2={x + w + 8} y1={water + 16 + ((frame + i * 9) % 12) * 0.3} y2={water + 16 + ((frame + i * 9) % 12) * 0.3} stroke="#d6dfe0" strokeOpacity={0.35} strokeWidth={2} />
						</g>
					))}
					{Array.from({length: 18}, (_, i) => {
						const y = water + 30 + i * i * 2.3;
						const w = 50 + i * 16;
						const x = 540 + Math.sin(i * 1.9 + frame / 30) * (40 + i * 8);
						return <line key={i} x1={x - w} x2={x + w} y1={y} y2={y} stroke="#e7d4aa" strokeOpacity={0.2 - i * 0.008} strokeWidth={1.5 + i * 0.15} />;
					})}
				</svg>
				<FogBank y={water - 10} opacity={0.38} seed={10} drift={0.5} height={160} />
			</Depth>
			<Depth depth={0.9} cam={cam}>
				<FogBank y={1750} opacity={0.16} seed={12} drift={0.8} height={260} />
			</Depth>
		</AbsoluteFill>
	);
};
