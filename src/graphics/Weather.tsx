import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile} from 'remotion';
import {rng} from '../lib/random';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {GraphicProps} from './Graphics';

/*
 * Everyday-life graphics (EP04 onward): drawn rain with ground splashes, soft steam over a plate,
 * a line-art diagram of an object flipping on a cue (the doorstep bowl), and a detail → implication chain.
 * Everything is seeded and time-driven, so frames are deterministic and the motion never jitters.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));

const STREAKS = (() => {
	const r = rng(404);
	return Array.from({length: 220}, () => ({x: r() * (W + 300) - 150, y: r() * (H + 300), len: 40 + r() * 60, speed: 1700 + r() * 900, w: 1 + r() * 1.4, o: 0.4 + r() * 0.6}));
})();
const DROPS = (() => {
	const r = rng(405);
	return Array.from({length: 40}, () => ({fx: r(), fy: r(), period: 0.55 + r() * 0.7, ph: r()}));
})();

/**
 * Rain: thin slanted streaks falling at a steady speed (screen space, so it carries across cuts),
 * plus optional ripple splashes in a ground band `splashes: [x0, y0, x1, y1]`.
 */
export const Rain: React.FC<GraphicProps> = ({g, t, span}) => {
	const density = g.density ?? 0.4;
	const n = Math.round(STREAKS.length * density);
	const slant = g.slant ?? 0.16;
	const o = (g.opacity ?? 0.22) * ease(t, span.start - 0.6, 0.4);
	const band = g.splashes as number[] | undefined;
	const loop = H + 300;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
				<g opacity={o} stroke="rgb(214,223,224)" strokeLinecap="round">
					{STREAKS.slice(0, n).map((s, i) => {
						const y = ((s.y + t * s.speed) % loop) - 150;
						const x = s.x + y * slant;
						return <line key={i} x1={x} y1={y} x2={x - s.len * slant} y2={y - s.len} strokeWidth={s.w} opacity={s.o} />;
					})}
				</g>
				{band && (
					<g fill="none" stroke="rgb(214,223,224)">
						{DROPS.slice(0, Math.round(DROPS.length * density)).map((d, i) => {
							const u = (t / d.period + d.ph) % 1;
							const rx = 4 + u * 22;
							return (
								<ellipse
									key={i}
									cx={lerp(band[0], band[2], d.fx)}
									cy={lerp(band[1], band[3], d.fy)}
									rx={rx}
									ry={rx * 0.32}
									strokeWidth={1.4}
									opacity={o * 1.6 * (1 - u) * (u < 0.08 ? u / 0.08 : 1)}
								/>
							);
						})}
					</g>
				)}
			</svg>
		</AbsoluteFill>
	);
};

/** Soft steam rising from a point in the plate (use with `local: true`): slow puffs that swell, sway and fade. */
export const Steam: React.FC<GraphicProps> = ({g, t}) => {
	const {x = 540, y = 1000, width = 260, height = 420} = g;
	const puffs = g.puffs ?? 7;
	const id = `steam-${x}-${y}`;
	return (
		<svg width={W} height={H} style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
			<defs>
				<radialGradient id={id}>
					<stop offset="0%" stopColor="rgb(236,232,224)" stopOpacity={0.55} />
					<stop offset="55%" stopColor="rgb(220,222,220)" stopOpacity={0.2} />
					<stop offset="100%" stopColor="rgb(220,222,220)" stopOpacity={0} />
				</radialGradient>
			</defs>
			{Array.from({length: puffs}, (_, i) => {
				const period = 3.2;
				const u = (t / period + i / puffs) % 1;
				const sway = Math.sin(t * 0.9 + i * 1.9) * width * 0.18 * u;
				const r = width * (0.25 + 0.55 * u);
				const a = Math.sin(Math.PI * u) * (g.opacity ?? 0.7);
				return <ellipse key={i} cx={x + sway} cy={y - height * u} rx={r} ry={r * 0.7} fill={`url(#${id})`} opacity={a} />;
			})}
		</svg>
	);
};

/**
 * Line-art badge of the doorstep bowl: drops fall into the open bowl, then on `flip` it turns
 * upside down and the rain glances off its back. Makes the custom readable at a glance.
 */
export const BowlFlip: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const t0 = cueTime(timing, g.start);
	const tf = cueTime(timing, g.flip);
	const size = g.size ?? 230;
	const show = ease(t, t0 - 0.1, 0.5) * out(t, span.end, 0.3);
	const f = ease(t, tf, 0.55, Easing.inOut(Easing.cubic));
	const flipped = f > 0.5;
	const water = (1 - ease(t, tf, 0.3)) * Math.min(1, Math.max(0, (t - t0) / 1.5));
	const drops = [-28, 6, 34].map((dx, i) => {
		const u = (t * 1.25 + i * 0.37) % 1;
		const hitY = flipped ? -8 : 6;
		if (u < 0.55) return {x: dx * 0.5, y: lerp(-95, hitY, u / 0.55), o: 1, k: i};
		if (!flipped) return {x: dx * 0.5, y: hitY, o: 0, k: i};
		const v = (u - 0.55) / 0.45;
		const side = dx * 0.5 >= 0 ? 1 : -1;
		return {x: dx * 0.5 + side * v * 62, y: hitY + v * v * 60, o: 1 - v, k: i};
	});
	return (
		<div style={{position: 'absolute', left: g.x - size / 2, top: g.y - size / 2, width: size, height: size, opacity: show, transform: `scale(${0.94 + 0.06 * show})`}}>
			<div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: 'rgba(11,18,22,0.62)', border: `1.5px solid ${palette.amber}`, boxShadow: '0 6px 30px rgba(0,0,0,0.45)'}} />
			<svg width={size} height={size} viewBox="-100 -100 200 200" style={{position: 'absolute', inset: 0}}>
				<line x1={-72} x2={72} y1={52} y2={52} stroke={palette.fog} strokeWidth={2} opacity={0.6} />
				{drops.map((d) => (
					<line key={d.k} x1={d.x} y1={d.y - 12} x2={d.x} y2={d.y} stroke={palette.mist} strokeWidth={3} strokeLinecap="round" opacity={d.o * 0.9} />
				))}
				<g transform={`rotate(${180 * f} 0 22)`}>
					<path d="M-58,-4 Q-56,46 0,46 Q56,46 58,-4" fill="rgba(233,169,75,0.12)" stroke={palette.parchment} strokeWidth={4} strokeLinejoin="round" />
					<ellipse cx={0} cy={-4} rx={58} ry={10} fill="none" stroke={palette.parchment} strokeWidth={4} />
					<ellipse cx={0} cy={4} rx={46 * Math.sqrt(water)} ry={7 * Math.sqrt(water)} fill="rgba(127,190,214,0.75)" opacity={water} />
				</g>
			</svg>
			<div style={{position: 'absolute', top: size + 12, left: -60, right: -60, textAlign: 'center', ...kicker, fontSize: 20, color: flipped ? palette.amber : palette.mist, textShadow: '0 2px 10px rgba(0,0,0,0.85)'}}>
				{flipped ? g.after ?? 'Upside down' : g.before ?? 'First rain'}
			</div>
		</div>
	);
};

/**
 * Detail → implication chain: rows of plate medallion + detail name, an arrow drawing to what it implies.
 * rows: [{detail, implies, img, focus: [fx, fy], zoom, at: cue, impliesAt: cue}]. Plate behind is dimmed by `dim`.
 */
export const DetailChain: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const rows: any[] = g.rows;
	const top = g.top ?? 470;
	const gap = g.gap ?? 260;
	const m = 190;
	const o = out(t, span.end + 0.1, 0.35);
	const bg = ease(t, span.start - 0.3, 0.6);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<AbsoluteFill style={{background: `rgba(6,10,13,${(g.dim ?? 0.6) * bg})`}} />
			<div style={{position: 'absolute', top: 336, width: '100%', textAlign: 'center', ...kicker, fontSize: 26, color: palette.amber, opacity: bg}}>{g.kicker}</div>
			{rows.map((r, i) => {
				const a = ease(t, cueTime(timing, r.at) - 0.1, 0.5);
				const b = ease(t, cueTime(timing, r.impliesAt) - 0.12, 0.55);
				const y = top + i * gap;
				const [fx, fy] = r.focus ?? [0.5, 0.5];
				const z = r.zoom ?? 1.8;
				const iw = m * z;
				const ih = iw * (H / W);
				const next = rows[i + 1] ? ease(t, cueTime(timing, rows[i + 1].at) - 0.3, 0.4) : 0;
				return (
					<React.Fragment key={i}>
						{rows[i + 1] && <div style={{position: 'absolute', left: 90 + m / 2 - 1, top: y + m + 8, width: 2, height: (gap - m - 16) * next, background: palette.amber, opacity: 0.55}} />}
						<div style={{position: 'absolute', left: 90, top: y, width: m, height: m, borderRadius: '50%', overflow: 'hidden', border: `2.5px solid ${b > 0.5 ? palette.ember : 'rgba(239,230,210,0.7)'}`, opacity: a, transform: `scale(${0.9 + 0.1 * a})`, boxShadow: '0 6px 30px rgba(0,0,0,0.5)'}}>
							<Img src={staticFile(r.img)} style={{position: 'absolute', width: iw, height: ih, left: m / 2 - fx * iw, top: m / 2 - fy * ih}} />
						</div>
						<div style={{position: 'absolute', left: 90 + m + 44, top: y + 18, opacity: a, transform: `translateX(${(1 - a) * -16}px)`}}>
							<div style={{...kicker, fontSize: 32, color: palette.parchment, textShadow: '0 2px 12px rgba(0,0,0,0.8)'}}>{r.detail}</div>
							<div style={{display: 'flex', alignItems: 'center', marginTop: 6, gap: 18}}>
								<svg width={84} height={30} viewBox="0 0 84 30" style={{opacity: a}}>
									<line x1={2} y1={15} x2={2 + 72 * b} y2={15} stroke={palette.amber} strokeWidth={3} />
									<path d="M66,5 L80,15 L66,25" fill="none" stroke={palette.amber} strokeWidth={3} opacity={b > 0.85 ? 1 : 0} />
								</svg>
								<div style={{fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 96, lineHeight: 1, color: palette.ember, opacity: b, transform: `translateY(${(1 - b) * 14}px)`, textShadow: '0 4px 30px rgba(0,0,0,0.75)'}}>
									{r.implies}
								</div>
							</div>
						</div>
					</React.Fragment>
				);
			})}
		</AbsoluteFill>
	);
};

export const WEATHER: Record<string, React.FC<GraphicProps>> = {
	rain: Rain,
	steam: Steam,
	bowlFlip: BowlFlip,
	detailChain: DetailChain,
};
