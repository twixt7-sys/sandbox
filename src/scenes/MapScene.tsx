import React from 'react';
import {AbsoluteFill, Easing, interpolate, staticFile} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {Graphic} from '../types';
import type {SceneProps} from './registry';

type Pt = [number, number];

const RIVER: Pt[] = [
	[660, 250], [600, 420], [500, 600], [560, 770], [660, 920], [610, 1070], [520, 1220], [540, 1500],
];

/** Catmull-Rom through points -> cubic Bézier path. */
const smooth = (pts: Pt[]) => {
	let d = `M${pts[0][0]},${pts[0][1]}`;
	for (let i = 0; i < pts.length - 1; i++) {
		const p0 = pts[Math.max(0, i - 1)];
		const [p1, p2] = [pts[i], pts[i + 1]];
		const p3 = pts[Math.min(pts.length - 1, i + 2)];
		const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
		const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
		d += ` C${c1[0]},${c1[1]} ${c2[0]},${c2[1]} ${p2[0]},${p2[1]}`;
	}
	return d;
};

const RIVER_D = smooth(RIVER);
const WEST_D = `M-100,-100 L${RIVER[0][0]},-100 L${RIVER[0][0]},${RIVER[0][1]} ${RIVER_D.replace(/^M[^C]+/, '')} L${RIVER[RIVER.length - 1][0]},${H + 100} L-100,${H + 100} Z`;
const EAST_D = `M${W + 100},-100 L${RIVER[0][0]},-100 L${RIVER[0][0]},${RIVER[0][1]} ${RIVER_D.replace(/^M[^C]+/, '')} L${RIVER[RIVER.length - 1][0]},${H + 100} L${W + 100},${H + 100} Z`;

const WEST_TOWN: Pt = [210, 690];
const EAST_TOWN: Pt = [880, 600];
const BRIDGE_PT: Pt = [548, 745];
const W_LAND: Pt = [585, 985];
const E_LAND: Pt = [730, 925];

const OLD_ROAD = `M${WEST_TOWN[0]},${WEST_TOWN[1]} C330,700 440,760 ${BRIDGE_PT[0] - 34},${BRIDGE_PT[1] + 4} M${BRIDGE_PT[0] + 40},${BRIDGE_PT[1] - 8} C680,720 780,640 ${EAST_TOWN[0]},${EAST_TOWN[1]}`;
const NEW_ROAD = `M${WEST_TOWN[0]},${WEST_TOWN[1] + 10} C260,860 420,1000 ${W_LAND[0]},${W_LAND[1]} M${E_LAND[0]},${E_LAND[1]} C820,880 900,760 ${EAST_TOWN[0]},${EAST_TOWN[1] + 12}`;
const FERRY = `M${W_LAND[0]},${W_LAND[1]} Q${(W_LAND[0] + E_LAND[0]) / 2},${(W_LAND[1] + E_LAND[1]) / 2 + 40} ${E_LAND[0]},${E_LAND[1]}`;

const Label: React.FC<{x: number; y: number; text: string; o: number; color?: string; size?: number; anchor?: 'start' | 'middle' | 'end'}> = ({
	x,
	y,
	text,
	o,
	color = palette.parchment,
	size = 34,
	anchor = 'middle',
}) => (
	<text
		x={x}
		y={y + (1 - o) * 10}
		textAnchor={anchor}
		fill={color}
		opacity={o}
		style={{fontFamily: fonts.ui, fontWeight: 700, fontSize: size, letterSpacing: '0.16em', textTransform: 'uppercase'}}
	>
		{text}
	</text>
);

const Town: React.FC<{at: Pt; o: number}> = ({at, o}) => (
	<g opacity={o} fill={palette.parchment}>
		{[
			[-18, -6, 14], [0, -14, 18], [18, -4, 12], [-4, 8, 12], [12, 10, 10],
		].map(([dx, dy, s], i) => (
			<rect key={i} x={at[0] + dx - s / 2} y={at[1] + dy - s / 2} width={s} height={s} opacity={0.85} />
		))}
		<circle cx={at[0]} cy={at[1]} r={48} fill="none" stroke={palette.parchment} strokeOpacity={0.35} strokeWidth={1.5} strokeDasharray="3 6" />
	</g>
);

const Hills: React.FC = () => (
	<g fill="none" stroke={palette.parchment} strokeOpacity={0.12} strokeWidth={1.4}>
		{[
			[250, 470, 150], [860, 1110, 130], [880, 390, 110], [230, 1120, 120],
		].flatMap(([x, y, r], k) =>
			Array.from({length: 5}, (_, i) => <ellipse key={`${k}-${i}`} cx={x + i * 6} cy={y + i * 3} rx={r - i * 24} ry={(r - i * 24) * 0.55} />),
		)}
	</g>
);

const find = (graphics: Graphic[], type: string) => graphics.find((g) => g.type === type);

/** Core insight: one lost bridge -> trade, power and culture, each drawn as it is spoken. */
export const MapScene: React.FC<SceneProps> = ({progress, t, shot}) => {
	const timing = useTiming();
	const g = shot.graphics;
	const tBase = cueTime(timing, find(g, 'mapBase')?.start, timing.shots.find((s) => s.id === shot.id)!.start);
	const ferry = find(g, 'ferryRoute');
	const power = find(g, 'power');
	const accents = find(g, 'accents');
	const tFerry = cueTime(timing, ferry?.start, 1e9);
	const tToll = cueTime(timing, ferry?.icon, 1e9);
	const tPower = cueTime(timing, power?.start, 1e9);
	const tAccent = cueTime(timing, accents?.start, 1e9);

	const draw = ease(t, tBase, 1.1, Easing.inOut(Easing.cubic));
	const base = ease(t, tBase + 0.2, 0.6);
	const ferryP = ease(t, tFerry, 1.2, Easing.inOut(Easing.cubic));
	const tollP = ease(t, tToll - 0.1, 0.5);
	const powerP = ease(t, tPower, 1.3);
	const accentP = ease(t, tAccent, 0.8);
	const zoom = lerp(1.08, 1.0, interpolate(progress, [0, 1], [0, 1], {easing: Easing.out(Easing.quad)}));
	const boat = (Math.sin((t - tFerry) * 1.2 - Math.PI / 2) + 1) / 2;
	const wave = (t - tAccent) * 60;

	return (
		<AbsoluteFill style={{backgroundColor: '#0d1519'}}>
			<AbsoluteFill style={{transform: `scale(${zoom})`, transformOrigin: '55% 45%'}}>
				<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
					<defs>
						<radialGradient id="influence">
							<stop offset="0%" stopColor={palette.amber} stopOpacity={0.32} />
							<stop offset="70%" stopColor={palette.amber} stopOpacity={0.1} />
							<stop offset="100%" stopColor={palette.amber} stopOpacity={0} />
						</radialGradient>
					</defs>
					<rect width={W} height={H} fill="#111b20" />
					<image href={staticFile('textures/paper.png')} width={W} height={H} preserveAspectRatio="none" />
					{/* frame */}
					<rect x={64} y={200} width={W - 128} height={1200} fill="none" stroke={palette.parchment} strokeOpacity={0.25 * base} strokeWidth={1.5} />
					<rect x={76} y={212} width={W - 152} height={1176} fill="none" stroke={palette.parchment} strokeOpacity={0.12 * base} strokeWidth={1} />
					<g opacity={base}>
						<Hills />
					</g>
					{/* culture: banks tinted differently */}
					<path d={WEST_D} fill="#6fa3c0" opacity={0.1 * accentP} />
					<path d={EAST_D} fill={palette.amber} opacity={0.09 * accentP} />
					{/* river */}
					<path d={RIVER_D} fill="none" stroke="#284652" strokeWidth={34} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - draw} />
					<path d={RIVER_D} fill="none" stroke={palette.fog} strokeOpacity={0.55 + 0.35 * accentP} strokeWidth={accentP > 0 ? 3 + 2 * accentP : 3} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - draw} />
					{/* old road + broken bridge */}
					<path d={OLD_ROAD} fill="none" stroke={palette.parchment} strokeOpacity={0.35 * base * (1 - 0.5 * ferryP)} strokeWidth={3} strokeDasharray="10 9" />
					<g opacity={base}>
						<line x1={BRIDGE_PT[0] - 40} y1={BRIDGE_PT[1] + 6} x2={BRIDGE_PT[0] - 14} y2={BRIDGE_PT[1]} stroke={palette.parchment} strokeWidth={8} />
						<line x1={BRIDGE_PT[0] + 18} y1={BRIDGE_PT[1] - 4} x2={BRIDGE_PT[0] + 44} y2={BRIDGE_PT[1] - 10} stroke={palette.parchment} strokeWidth={8} />
						<g stroke={palette.rust} strokeWidth={5} strokeLinecap="round">
							<line x1={BRIDGE_PT[0] - 12} y1={BRIDGE_PT[1] - 30} x2={BRIDGE_PT[0] + 16} y2={BRIDGE_PT[1] - 2} />
							<line x1={BRIDGE_PT[0] + 16} y1={BRIDGE_PT[1] - 30} x2={BRIDGE_PT[0] - 12} y2={BRIDGE_PT[1] - 2} />
						</g>
					</g>
					<Label x={BRIDGE_PT[0] - 70} y={BRIDGE_PT[1] - 44} text="Old bridge" o={base * 0.8} size={24} anchor="end" color={palette.rust} />
					<Town at={WEST_TOWN} o={base} />
					<Town at={EAST_TOWN} o={base} />
					{/* trade: new road to the ferry */}
					<path d={NEW_ROAD} fill="none" stroke={palette.amber} strokeWidth={4} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - ferryP} opacity={0.9} />
					<path d={FERRY} fill="none" stroke={palette.amber} strokeWidth={4} strokeDasharray="6 10" opacity={ferryP} />
					{ferryP > 0.6 && (
						<g transform={`translate(${lerp(W_LAND[0], E_LAND[0], boat)} ${lerp(W_LAND[1], E_LAND[1], boat) + Math.sin(boat * Math.PI) * 20})`}>
							<path d="M-16,-2 L16,-2 L10,8 L-10,8 Z" fill={palette.ember} />
							<line x1={0} y1={-2} x2={0} y2={-20} stroke={palette.ember} strokeWidth={2.5} />
						</g>
					)}
					{/* toll coin */}
					<g opacity={tollP} transform={`translate(${(W_LAND[0] + E_LAND[0]) / 2 + 10} ${(W_LAND[1] + E_LAND[1]) / 2 + 92}) scale(${0.7 + 0.3 * tollP})`}>
						<circle r={30} fill={palette.amber} />
						<circle r={23} fill="none" stroke="#7a5418" strokeWidth={3} />
						<path d="M-6,-12 L6,-12 L6,12 L-6,12 Z" fill="#7a5418" opacity={0.75} />
					</g>
					<Label x={(W_LAND[0] + E_LAND[0]) / 2 + 60} y={(W_LAND[1] + E_LAND[1]) / 2 + 102} text={ferry?.label ?? 'Ferry toll'} o={tollP} color={palette.ember} anchor="start" />
					{/* power: the ferry family's reach */}
					<circle cx={W_LAND[0]} cy={W_LAND[1]} r={40 + 360 * powerP} fill="url(#influence)" opacity={powerP} />
					{[0, 1, 2].map((k) => {
						const rr = 60 + 330 * ease(t, tPower + k * 0.18, 1.2);
						return <circle key={k} cx={W_LAND[0]} cy={W_LAND[1]} r={rr} fill="none" stroke={palette.amber} strokeOpacity={0.35 * powerP * (1 - k * 0.25)} strokeWidth={1.5} />;
					})}
					<g opacity={powerP} transform={`translate(${W_LAND[0] - 70} ${W_LAND[1] + 14}) scale(${0.8 + 0.2 * powerP})`}>
						<path d="M-26,-34 L26,-34 L26,0 C26,22 0,36 0,36 C0,36 -26,22 -26,0 Z" fill="#1b2328" stroke={palette.amber} strokeWidth={3} />
						<path d="M-14,4 L14,4 L9,14 L-9,14 Z" fill={palette.amber} />
						<line x1={0} y1={4} x2={0} y2={-20} stroke={palette.amber} strokeWidth={3} />
					</g>
					<Label x={W_LAND[0] - 112} y={W_LAND[1] + 30} text={power?.label ?? 'Ferry family'} o={powerP} color={palette.ember} anchor="end" />
					{/* culture: two accents */}
					<g opacity={accentP}>
						<Label x={250} y={460} text={accents?.labels?.[0] ?? 'West bank'} o={accentP} color="#b9d3e0" />
						<path
							d={Array.from({length: 40}, (_, i) => `${i ? 'L' : 'M'}${160 + i * 4.5},${500 + Math.sin((i * 4.5 + wave) / 14) * 12}`).join(' ')}
							fill="none"
							stroke="#b9d3e0"
							strokeWidth={3}
						/>
						<Label x={850} y={460} text={accents?.labels?.[1] ?? 'East bank'} o={accentP} color={palette.ember} />
						<path
							d={Array.from({length: 22}, (_, i) => `${i ? 'L' : 'M'}${760 + i * 8.5},${500 + ((i + Math.floor(wave / 8)) % 2 ? -12 : 12)}`).join(' ')}
							fill="none"
							stroke={palette.ember}
							strokeWidth={3}
							strokeLinejoin="miter"
						/>
					</g>
					{/* north mark */}
					<g opacity={base * 0.6} transform="translate(950 1290)">
						<path d="M0,-30 L9,8 L0,0 L-9,8 Z" fill={palette.parchment} />
						<text y={36} textAnchor="middle" fill={palette.parchment} style={{fontFamily: fonts.display, fontSize: 26, fontWeight: 600}}>
							N
						</text>
					</g>
				</svg>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
