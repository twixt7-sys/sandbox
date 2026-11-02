import React from 'react';
import {AbsoluteFill} from 'remotion';
import {cueTime, ease, useTiming} from '../lib/timing';
import type {GraphicProps} from './Graphics';

/*
 * Rite graphics (EP11 onward). `shroud`: a linen-wrapped body lying on a bier or table, drawn over a plate when the
 * image model will not paint one (SDXL avoids bodies). Pin with `local: true`.
 */

/**
 * Shroud: `at: [x, y]` = centre of the body's base line, `length` (default 260), `height` (default 44), head end on the
 * `head: "left" | "right"` side, optional `sprigs` (herb count, default 5), `start` cue (else visible from the shot start).
 */
export const Shroud: React.FC<GraphicProps> = ({g, t}) => {
	const timing = useTiming();
	const [cx, cy] = g.at;
	const L = g.length ?? 260;
	const h = g.height ?? 44;
	const dir = g.head === 'right' ? -1 : 1;
	const o = g.start ? ease(t, cueTime(timing, g.start), 0.5) : 1;
	const x0 = cx - L / 2;
	// Smooth profile (u 0..1 along the body, head at u=0): round head, neck dip, chest, long body, raised feet.
	const bump = (u: number, c: number, w: number) => Math.exp(-(((u - c) / w) ** 2));
	const prof = (u: number) => Math.min(1, Math.sin((Math.PI / 2) * Math.min(1, u / 0.04, (1 - u) / 0.03)) ** 0.5) *
		(0.8 * bump(u, 0.08, 0.075) + 0.6 * bump(u, 0.3, 0.17) + 0.5 * bump(u, 0.56, 0.24) + 0.4 * bump(u, 0.8, 0.13) + 0.5 * bump(u, 0.94, 0.055));
	const X = (u: number) => (dir > 0 ? x0 + u * L : x0 + (1 - u) * L);
	const N = 80;
	const top = Array.from({length: N + 1}, (_, i) => [X(i / N), cy - Math.min(1, prof(i / N)) * h] as const);
	const d = `M${X(0)},${cy} ` + top.map(([x, y]) => `L${x.toFixed(1)},${y.toFixed(1)}`).join(' ') + ` L${X(1)},${cy} Z`;
	const n = g.sprigs ?? 5;
	return (
		<AbsoluteFill style={{opacity: o * (g.opacity ?? 1)}}>
			<svg width={1080} height={1920} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<linearGradient id="shroud-linen" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor="#fbf5e8" />
						<stop offset="0.45" stopColor="#e6dbc4" />
						<stop offset="1" stopColor="#9c8c70" />
					</linearGradient>
				</defs>
				<ellipse cx={cx} cy={cy + 3} rx={L * 0.55} ry={h * 0.3} fill="rgba(40,26,12,0.5)" style={{filter: 'blur(7px)'}} />
				<path d={d} fill="url(#shroud-linen)" opacity={0.94} style={{filter: 'blur(1.3px)'}} />
				{/* Wrapping bands: soft arcs over the body at intervals. */}
				{[0.16, 0.28, 0.4, 0.52, 0.64, 0.76, 0.86].map((u, i) => {
					const x = X(u);
					const y = cy - Math.min(1, prof(u)) * h;
					return <path key={i} d={`M${x - 3 * dir},${cy - 1} Q${x + 7 * dir},${(cy + y) / 2} ${x + 2 * dir},${y + 1}`} stroke="rgba(130,110,80,0.4)" strokeWidth={1.6} style={{filter: 'blur(0.6px)'}} fill="none" />;
				})}
				{Array.from({length: n}, (_, i) => {
					const u = 0.2 + (0.62 * i) / Math.max(1, n - 1);
					const x = X(u);
					const y = cy - Math.min(1, prof(u)) * h + 1;
					return (
						<g key={i} stroke="#5d7a3a" strokeWidth={2.2} strokeLinecap="round" fill="none" opacity={0.9}>
							<path d={`M${x - 14},${y + 3} Q${x},${y - 6} ${x + 14},${y - 2}`} />
							<path d={`M${x - 4},${y - 1} l-5,-8 M${x + 4},${y - 3} l4,-8`} />
						</g>
					);
				})}
			</svg>
		</AbsoluteFill>
	);
};

export const RITES: Record<string, React.FC<GraphicProps>> = {
	shroud: Shroud,
};
