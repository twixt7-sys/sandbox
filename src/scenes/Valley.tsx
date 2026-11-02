import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {FogBank} from '../fx/Fx';
import {lerp} from '../lib/timing';
import {ridgePath, ridgeYAt} from '../lib/random';
import {H, W} from '../theme';
import type {SceneProps} from './registry';

/** Wraps a depth layer: nearer layers (depth→1) move more under the same camera move. */
export const Depth: React.FC<{depth: number; cam: {x: number; y: number; zoom: number}; children: React.ReactNode}> = ({depth, cam, children}) => {
	const z = 1 + (cam.zoom - 1) * (0.35 + depth * 0.65);
	return (
		<AbsoluteFill style={{transform: `translate(${cam.x * depth}px, ${cam.y * depth}px) scale(${z})`, transformOrigin: '50% 48%'}}>
			{children}
		</AbsoluteFill>
	);
};

const Svg: React.FC<{children: React.ReactNode}> = ({children}) => (
	<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
		{children}
	</svg>
);

export const Sky: React.FC<{stops: [number, string][]; sun?: {x: number; y: number; r: number; color: string; opacity: number}}> = ({stops, sun}) => (
	<Svg>
		<defs>
			<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
				{stops.map(([o, c]) => (
					<stop key={o} offset={o} stopColor={c} />
				))}
			</linearGradient>
			{sun && (
				<radialGradient id="sun">
					<stop offset="0%" stopColor={sun.color} stopOpacity={sun.opacity} />
					<stop offset="35%" stopColor={sun.color} stopOpacity={sun.opacity * 0.35} />
					<stop offset="100%" stopColor={sun.color} stopOpacity={0} />
				</radialGradient>
			)}
		</defs>
		<rect width={W} height={H} fill="url(#sky)" />
		{sun && <ellipse cx={sun.x} cy={sun.y} rx={sun.r * 1.4} ry={sun.r} fill="url(#sun)" />}
	</Svg>
);

/** A ridge with a soft lit rim along its crest. */
export const Ridge: React.FC<{seed: number; baseY: number; amp: number; fill: string; rim?: string; rimOpacity?: number; rough?: number; ridged?: boolean}> = ({
	seed,
	baseY,
	amp,
	fill,
	rim,
	rimOpacity = 0.35,
	rough,
	ridged,
}) => {
	const d = ridgePath(seed, {baseY, amp, rough, ridged});
	return (
		<Svg>
			<path d={d} fill={fill} />
			{rim && <path d={d} fill="none" stroke={rim} strokeOpacity={rimOpacity} strokeWidth={2} />}
		</Svg>
	);
};

const riverPolygon = (from: [number, number], to: [number, number], w0: number, w1: number, wiggle: number) => {
	const left: string[] = [];
	const right: string[] = [];
	const N = 60;
	for (let i = 0; i <= N; i++) {
		const s = i / N;
		const y = lerp(from[1], to[1], 1 - (1 - s) ** 1.6);
		const x = lerp(from[0], to[0], s) + Math.sin(s * 5.2 + 0.4) * wiggle * (1 - s) ** 0.8;
		const w = lerp(w0, w1, 1 - (1 - s) ** 2.2) / 2;
		left.push(`${(x - w).toFixed(1)},${y.toFixed(1)}`);
		right.unshift(`${(x + w).toFixed(1)},${y.toFixed(1)}`);
	}
	return `M${left.join(' L')} L${right.join(' L')} Z`;
};

const Tower: React.FC<{x: number; y: number; s?: number; fill: string; rim: string}> = ({x, y, s = 1, fill, rim}) => {
	const w = 34 * s;
	const h = 120 * s;
	const top = y - h;
	const d = `M${x - w / 2},${y + 6} L${x - w / 2},${top + 14 * s} L${x - w / 2 + 6 * s},${top + 6 * s} L${x - 4 * s},${top + 18 * s} L${x + 3 * s},${top} L${x + w / 2 - 4 * s},${top + 22 * s} L${x + w / 2},${top + 30 * s} L${x + w / 2},${y + 6} Z`;
	return (
		<g>
			<path d={d} fill={fill} />
			<path d={d} fill="none" stroke={rim} strokeOpacity={0.4} strokeWidth={1.5} />
			<rect x={x - 3 * s} y={top + 45 * s} width={6 * s} height={14 * s} fill="#05080a" opacity={0.7} />
		</g>
	);
};

const Pines: React.FC<{seed: number; ridge: {baseY: number; amp: number}; x0: number; x1: number; fill: string; scale?: number}> = ({seed, ridge, x0, x1, fill, scale = 1}) => {
	const trees: React.ReactNode[] = [];
	let k = 0;
	for (let x = x0; x < x1; x += 22 + ((k * 37) % 19)) {
		const y = ridgeYAt(seed, ridge, x) + 6;
		const h = (70 + ((k * 53) % 70)) * scale;
		const w = h * 0.32;
		trees.push(<path key={k} d={`M${x},${y - h} L${x + w / 2},${y} L${x - w / 2},${y} Z M${x - 2},${y} L${x + 2},${y} L${x + 2},${y + 10} L${x - 2},${y + 10} Z`} fill={fill} />);
		k++;
	}
	return (
		<Svg>
			<g>{trees}</g>
		</Svg>
	);
};

export const BLUE_HOUR = {
	sky: [
		[0, '#101d27'],
		[0.25, '#22394a'],
		[0.4, '#5a7480'],
		[0.47, '#a9a693'],
		[0.52, '#d8b98b'],
	] as [number, string][],
	far: '#8697a0',
	mid: '#5b717b',
	near: '#384c56',
	floor: '#222f35',
	fore: '#0c1317',
	rim: '#f0c888',
};

/** Hook: aerial over an immense, empty valley. Also rendered as the loop target at the end. */
export const Valley: React.FC<SceneProps> = ({progress}) => {
	const frame = useCurrentFrame();
	const p = progress;
	const cam = {x: lerp(0, -30, p), y: lerp(0, 40, p), zoom: lerp(1.0, 1.09, p)};
	const C = BLUE_HOUR;
	const towerRidge = {baseY: 1010, amp: 230};
	return (
		<AbsoluteFill style={{backgroundColor: '#101d27'}}>
			<Depth depth={0} cam={cam}>
				<Sky stops={C.sky} sun={{x: 660, y: 830, r: 520, color: '#f4c78a', opacity: 0.55}} />
			</Depth>
			<Depth depth={0.08} cam={cam}>
				<Ridge seed={11} baseY={790} amp={210} fill={C.far} rim={C.rim} rimOpacity={0.45} rough={0.58} ridged />
				<FogBank y={860} opacity={0.35} seed={2} drift={0.25} />
			</Depth>
			<Depth depth={0.18} cam={cam}>
				<Ridge seed={23} baseY={900} amp={240} fill={C.mid} rim={C.rim} rimOpacity={0.25} rough={0.6} ridged />
				<FogBank y={975} opacity={0.4} seed={3} drift={0.35} />
			</Depth>
			<Depth depth={0.3} cam={cam}>
				<Ridge seed={37} {...towerRidge} fill={C.near} rim={C.rim} rimOpacity={0.18} />
				<Svg>
					<Tower x={300} y={ridgeYAt(37, towerRidge, 300)} s={0.9} fill={C.near} rim={C.rim} />
				</Svg>
				<FogBank y={1110} opacity={0.42} seed={4} drift={0.45} height={300} />
			</Depth>
			<Depth depth={0.45} cam={cam}>
				<Svg>
					<defs>
						<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
							<stop offset="0" stopColor="#62737a" />
							<stop offset="0.35" stopColor="#36474e" />
							<stop offset="1" stopColor="#141d22" />
						</linearGradient>
					</defs>
					<path d={ridgePath(41, {baseY: 1190, amp: 40, bottom: 2100})} fill="url(#floor)" transform="translate(0 0)" />
					<path d={ridgePath(43, {baseY: 1330, amp: 70})} fill="#26343a" opacity={0.85} />
					<path d={ridgePath(47, {baseY: 1470, amp: 90})} fill="#1b262b" opacity={0.9} />
				</Svg>
				<FogBank y={1260} opacity={0.22} seed={14} drift={0.4} height={140} />
				<Svg>
					<defs>
						<linearGradient id="river" x1="0" y1="1" x2="0" y2="0">
							<stop offset="0" stopColor="#2e434c" />
							<stop offset="0.55" stopColor="#7e949a" />
							<stop offset="1" stopColor="#e2cfa6" />
						</linearGradient>
					</defs>
					<path d={riverPolygon([880, 2000], [560, 1170], 520, 10, 260)} fill="url(#river)" />
					{Array.from({length: 14}, (_, i) => {
						const y = 1250 + i * 52 + ((frame * 0.6 + i * 17) % 40);
						const w = 30 + i * 9;
						const x = 700 + Math.sin(i * 1.3 + frame / 40) * (40 + i * 6);
						return <line key={i} x1={x - w} x2={x + w} y1={y} y2={y} stroke="#eadcbc" strokeOpacity={0.12 + (i % 3) * 0.04} strokeWidth={2} />;
					})}
				</Svg>
			</Depth>
			<Depth depth={0.8} cam={cam}>
				<Ridge seed={53} baseY={1680} amp={260} fill={C.fore} rough={0.6} />
				<Pines seed={53} ridge={{baseY: 1680, amp: 260}} x0={-120} x1={1200} fill={C.fore} scale={1.25} />
				<FogBank y={1840} opacity={0.18} seed={5} drift={0.7} height={200} />
			</Depth>
		</AbsoluteFill>
	);
};

/** Thesis: same valley from river level at early dawn; the empty sky carries the statement. */
export const ValleyLow: React.FC<SceneProps> = ({progress}) => {
	const frame = useCurrentFrame();
	const p = progress;
	const cam = {x: lerp(40, -60, p), y: lerp(20, -10, p), zoom: lerp(1.04, 1.0, p)};
	const sky: [number, string][] = [
		[0, '#14222c'],
		[0.3, '#2d4553'],
		[0.5, '#7d8e8f'],
		[0.6, '#d7b68a'],
	];
	const horizon = 1240;
	return (
		<AbsoluteFill style={{backgroundColor: '#14222c'}}>
			<Depth depth={0} cam={cam}>
				<Sky stops={sky} sun={{x: 380, y: 1150, r: 560, color: '#f6c582', opacity: 0.6}} />
			</Depth>
			<Depth depth={0.1} cam={cam}>
				<Ridge seed={11} baseY={1080} amp={300} fill="#7b8d94" rim="#f2c98c" rimOpacity={0.5} rough={0.58} ridged />
				<FogBank y={1120} opacity={0.35} seed={6} drift={0.3} />
			</Depth>
			<Depth depth={0.22} cam={cam}>
				<Ridge seed={23} baseY={1190} amp={230} fill="#4d636c" rim="#f2c98c" rimOpacity={0.3} />
				<FogBank y={1210} opacity={0.5} seed={7} drift={0.4} height={180} />
			</Depth>
			<Depth depth={0.4} cam={cam}>
				<Svg>
					<defs>
						<linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
							<stop offset="0" stopColor="#c9b28a" />
							<stop offset="0.25" stopColor="#6e8389" />
							<stop offset="1" stopColor="#141f25" />
						</linearGradient>
					</defs>
					<rect x={-200} y={horizon} width={W + 400} height={H - horizon + 200} fill="url(#water)" />
					<clipPath id="below">
						<rect x={-200} y={horizon} width={W + 400} height={H} />
					</clipPath>
					{/* Mirror of the mid ridge about the waterline. */}
					<path d={ridgePath(23, {baseY: 2 * horizon - 1190, amp: -230, bottom: horizon})} fill="#3f545c" opacity={0.16} clipPath="url(#below)" />
					{Array.from({length: 22}, (_, i) => {
						const y = horizon + 12 + i * i * 1.45;
						const w = 40 + i * 14;
						const x = 380 + Math.sin(i * 2.1 + frame / 35) * (30 + i * 5);
						return <line key={i} x1={x - w} x2={x + w} y1={y} y2={y} stroke="#f0d8a8" strokeOpacity={0.22 - i * 0.007} strokeWidth={1.5 + i * 0.12} />;
					})}
				</Svg>
			</Depth>
			<Depth depth={0.85} cam={cam}>
				<Svg>
					{Array.from({length: 46}, (_, i) => {
						const side = i % 2 === 0 ? -1 : 1;
						const x = side < 0 ? -40 + (i * 11) % 230 : 860 + (i * 13) % 260;
						const h = 160 + ((i * 47) % 220);
						const bend = Math.sin(frame / 30 + i) * 6;
						return <path key={i} d={`M${x},1960 Q${x + bend},${1960 - h * 0.6} ${x + bend * 2 + side * 8},${1960 - h}`} stroke="#0a1013" strokeWidth={4 + (i % 3)} fill="none" />;
					})}
				</Svg>
			</Depth>
		</AbsoluteFill>
	);
};
