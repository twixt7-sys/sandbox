import React from 'react';
import {AbsoluteFill, Easing} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, palette} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Gate graphics (EP24, Arc 5: magic vs technology). One teleport gate against one muddy road. The gate's surface is drawn
 * in code inside a stone ring on the plate (`gateRing`, pinned with `"local": true`): a faint shimmer when idle, a lilac
 * swirl when it opens, a flicker and collapse when a jump fails. The comparison is a merchant's counting board
 * (`countingBoard`): dark walnut, brass rods, one wooden bead per question that slides to whichever side wins it, GATE on
 * the left and CART on the right. `crystalPrice` puts a price on the crystal each jump burns.
 */

/** EP24's motif colour: gate crystal, a pale lilac. */
export const CRYSTAL = '#c4b5f7';
const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const at = (t: number, s: number, dur: number, e?: (x: number) => number) => (Number.isFinite(s) ? ease(t, s, dur, e) : 0);
const cue = (timing: ReturnType<typeof useTiming>, c?: Cue) => (c ? cueTime(timing, c) : Infinity);

/**
 * GateRing: the gate's surface inside the stone ring at plate point `at: [x, y]`, inner radii `rx`, `ry`. Idle it is a
 * faint lilac shimmer (`idle`, default 0.3). `openAt` fills it with a turning swirl and a bright rim; `closeAt` lets it
 * fade back to idle. `jumps` cues flash the surface white and send one ring out (a cart going through). `failAt` makes an
 * open gate stutter three times and collapse to a point, leaving a few rust sparks. `dark: true` starts with no shimmer.
 * `stone: true` draws the stone ring itself (for plates where SDXL painted none). `occlude: [[x, y, rx, ry], ...]` masks
 * ellipses out of the light, so a figure standing in the opening stays in front of it.
 */
export const GateRing: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [x, y] = g.at;
	const rx = g.rx ?? 120;
	const ry = g.ry ?? 150;
	const t0 = cueTime(timing, g.start, span.start);
	const tEnd = g.end ? cueTime(timing, g.end) : span.end + 0.2;
	const tOpen = cue(timing, g.openAt);
	const tClose = cue(timing, g.closeAt);
	const tFail = cue(timing, g.failAt);
	const jumps: number[] = (g.jumps ?? []).map((q: Cue) => cueTime(timing, q));
	const vis = ease(t, t0, 0.4) * out(t, tEnd, 0.3);
	const idle = g.dark ? 0 : (g.idle ?? 0.3) * (0.8 + 0.2 * Math.sin(t * 2.4));
	const open = (g.open ? 1 : at(t, tOpen, 0.6)) * (1 - at(t, tClose, 0.6));
	// Failure: three stutters over 0.5 s, then the surface collapses to a point over 0.35 s.
	const stut = t > tFail && t < tFail + 0.5 ? (Math.floor((t - tFail) * 12) % 2 ? 0.2 : 1) : 1;
	const collapse = at(t, tFail + 0.5, 0.35, Easing.in(Easing.cubic));
	const fade = 1 - collapse;
	const surf = Math.max(idle * (1 - at(t, tFail, 0.2)), open * stut * fade);
	const flash = jumps.reduce((m, p) => Math.max(m, t >= p ? Math.exp(-(t - p) * 4) : 0), 0) + (Number.isFinite(tFail) && t > tFail + 0.5 ? Math.exp(-(t - tFail - 0.5) * 5) * 0.8 : 0);
	const sx = lerp(1, 0.05, collapse);
	const id = `gate-${Math.round(x)}-${Math.round(y)}`;
	const spin = t * 50;
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			<svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<radialGradient id={`${id}-f`}>
						<stop offset="0%" stopColor="#fbf9ff" stopOpacity={0.95} />
						<stop offset="35%" stopColor={CRYSTAL} stopOpacity={0.7} />
						<stop offset="85%" stopColor="#6d5bb8" stopOpacity={0.45} />
						<stop offset="100%" stopColor={CRYSTAL} stopOpacity={0.9} />
					</radialGradient>
					<mask id={`${id}-m`} maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}>
						<rect x={-200} y={-200} width={1480} height={2320} fill="white" />
						{(g.occlude ?? []).map(([ox, oy, orx, ory]: number[], i: number) => (
							<ellipse key={i} cx={ox} cy={oy} rx={orx} ry={ory} fill="black" style={{filter: 'blur(3px)'}} />
						))}
					</mask>
					<clipPath id={`${id}-c`}>
						<ellipse cx={x} cy={y} rx={rx} ry={ry} />
					</clipPath>
				</defs>
				{g.stone && (
					// A code-drawn stone ring for plates where SDXL painted none (a small, distant object it ignores).
					<g>
						<ellipse cx={x} cy={y + ry * 0.12} rx={rx * 1.55} ry={ry * 0.18} fill="rgba(0,0,0,0.35)" style={{filter: 'blur(4px)'}} transform={`translate(0 ${ry * 1.05})`} />
						<ellipse cx={x} cy={y} rx={rx * 1.3} ry={ry * 1.3} fill="none" stroke={g.stoneColor ?? '#8d908a'} strokeWidth={Math.max(rx, ry) * 0.6} />
						<ellipse cx={x} cy={y} rx={rx * 1.3} ry={ry * 1.3} fill="none" stroke="#2c2f2e" strokeWidth={Math.max(rx, ry) * 0.6} strokeDasharray={`${Math.max(rx, ry) * 0.06} ${Math.max(rx, ry) * 0.62}`} opacity={0.55} />
						<ellipse cx={x} cy={y} rx={rx * 1.58} ry={ry * 1.58} fill="none" stroke="#2c2f2e" strokeWidth={1.5} opacity={0.7} />
						<ellipse cx={x} cy={y} rx={rx} ry={ry} fill="none" stroke="#2c2f2e" strokeWidth={1.5} opacity={0.7} />
						<path d={`M ${x - rx * 1.2} ${y - ry * 0.9} A ${rx * 1.3} ${ry * 1.3} 0 0 1 ${x + rx * 0.4} ${y - ry * 1.4}`} fill="none" stroke="#c9c9bf" strokeWidth={Math.max(2, rx * 0.12)} opacity={0.35} />
						<path d={`M ${x - 6} ${y - ry * 1.58 - 4} L ${x} ${y - ry * 1.58 - 18} L ${x + 6} ${y - ry * 1.58 - 4} Z`} fill={CRYSTAL} opacity={0.9} style={{filter: `drop-shadow(0 0 6px ${CRYSTAL})`}} />
					</g>
				)}
				<g mask={g.occlude ? `url(#${id}-m)` : undefined}>
				{surf > 0.001 && (
					<g style={{mixBlendMode: 'screen'}} opacity={Math.min(1, surf)}>
						<g transform={`translate(${x} ${y}) scale(${sx}) translate(${-x} ${-y})`}>
							<ellipse cx={x} cy={y} rx={rx} ry={ry} fill={`url(#${id}-f)`} opacity={0.85} />
							<g clipPath={`url(#${id}-c)`}>
								{[0.92, 0.72, 0.52, 0.32].map((k, i) => (
									<ellipse
										key={k}
										cx={x}
										cy={y}
										rx={rx * k}
										ry={ry * k}
										fill="none"
										stroke="#f3efff"
										strokeWidth={3 - i * 0.4}
										strokeDasharray={`${40 + i * 18} ${30 + i * 10}`}
										strokeDashoffset={(i % 2 ? 1 : -1) * spin * (1 + i * 0.4)}
										opacity={0.55}
									/>
								))}
							</g>
							<ellipse cx={x} cy={y} rx={rx} ry={ry} fill="none" stroke={CRYSTAL} strokeWidth={6} style={{filter: `drop-shadow(0 0 14px ${CRYSTAL})`}} />
						</g>
					</g>
				)}
				{flash > 0.01 && <ellipse cx={x} cy={y} rx={rx * (1 + 0.25 * (1 - flash))} ry={ry * (1 + 0.25 * (1 - flash))} fill="#fbf9ff" opacity={Math.min(0.85, flash * 0.8)} style={{mixBlendMode: 'screen', filter: 'blur(6px)'}} />}
				{jumps.map((p, i) => {
					const q = ease(t, p, 1.0, Easing.out(Easing.cubic));
					if (t < p || q >= 1) return null;
					return <ellipse key={i} cx={x} cy={y} rx={lerp(rx, rx * 2.4, q)} ry={lerp(ry, ry * 2.4, q)} fill="none" stroke={CRYSTAL} strokeWidth={lerp(5, 1, q)} opacity={(1 - q) * 0.8} />;
				})}
				</g>
				{Number.isFinite(tFail) &&
					t > tFail + 0.7 &&
					Array.from({length: 10}, (_, i) => {
						const q = Math.min(1, (t - tFail - 0.7) / 1.4);
						const a = i * 0.63 + 0.4;
						const d = q * (40 + (i % 4) * 26);
						return <circle key={i} cx={x + Math.cos(a) * d} cy={y + Math.sin(a) * d + q * q * 60} r={2.6} fill={i % 3 ? palette.rust : palette.ember} opacity={(1 - q) * 0.9} />;
					})}
			</svg>
		</AbsoluteFill>
	);
};

/** A faceted crystal glyph (the gate's fuel), drawn in `c`. */
export const CrystalGlyph: React.FC<{c: string; size?: number; glow?: number}> = ({c, size = 40, glow = 0}) => (
	<svg width={size} height={size * 1.4} viewBox="0 0 20 28" style={{overflow: 'visible', filter: glow ? `drop-shadow(0 0 ${6 * glow}px ${c})` : undefined}}>
		<path d="M10 1 L18 9 L10 27 L2 9 Z" fill={c} fillOpacity={0.28} stroke={c} strokeWidth={1.4} strokeLinejoin="round" />
		<path d="M2 9 L18 9 M10 1 L6.5 9 L10 27 L13.5 9 Z" fill="none" stroke={c} strokeWidth={0.9} strokeOpacity={0.8} strokeLinejoin="round" />
	</svg>
);

/** A cart wheel glyph (the road), drawn in `c`. */
export const WheelGlyph: React.FC<{c: string; size?: number}> = ({c, size = 40}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth={1.6}>
		<circle cx={12} cy={12} r={10} />
		<circle cx={12} cy={12} r={2.2} fill={c} />
		{[0, 45, 90, 135].map((a) => (
			<line key={a} x1={12 - 10 * Math.cos((a * Math.PI) / 180)} y1={12 - 10 * Math.sin((a * Math.PI) / 180)} x2={12 + 10 * Math.cos((a * Math.PI) / 180)} y2={12 + 10 * Math.sin((a * Math.PI) / 180)} strokeWidth={1.2} />
		))}
	</svg>
);

/**
 * CrystalPrice: a crystal floating at `at: [x, y]` with a price chip (`kicker`, `price`) beside it on `side` (default
 * left; `below` centres it under the crystal). At `burnAt` it flares, then crumbles into rising lilac dust and its chip turns rust ("burned"). Overlay or local.
 */
export const CrystalPrice: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const [x, y] = g.at;
	const t0 = cueTime(timing, g.start, span.start);
	const tBurn = cue(timing, g.burnAt);
	const vis = ease(t, t0, 0.45) * out(t, g.end ? cueTime(timing, g.end) : span.end, 0.3);
	const bob = Math.sin(t * 2) * 6;
	const flare = Number.isFinite(tBurn) && t >= tBurn ? Math.exp(-(t - tBurn) * 3) : 0;
	const gone = at(t, tBurn + 0.25, 0.5);
	const chip = ease(t, t0 + 0.2, 0.45);
	const left = (g.side ?? 'left') === 'left';
	const below = g.side === 'below';
	const size = g.size ?? 70;
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: x - size / 2, top: y - size * 0.7 + bob, opacity: 1 - gone, transform: `scale(${1 + 0.25 * flare - 0.4 * gone})`}}>
				<CrystalGlyph c={CRYSTAL} size={size} glow={1 + 2 * flare} />
			</div>
			<svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				{flare > 0.01 && <circle cx={x} cy={y + bob} r={size * (0.8 + flare)} fill="#fbf9ff" opacity={flare * 0.6} style={{filter: 'blur(14px)', mixBlendMode: 'screen'}} />}
				{Number.isFinite(tBurn) &&
					t > tBurn + 0.2 &&
					Array.from({length: 16}, (_, i) => {
						const q = Math.min(1, (t - tBurn - 0.2) / 1.6);
						return <circle key={i} cx={x + Math.sin(i * 2.1) * (10 + q * 50)} cy={y - q * (70 + (i % 5) * 22)} r={2 + (i % 3)} fill={CRYSTAL} opacity={(1 - q) * 0.85} />;
					})}
			</svg>
			<div
				style={{
					position: 'absolute',
					...(below
						? {top: y + size * 0.85, left: x - 300, width: 600, textAlign: 'center' as const}
						: {top: y - 50, ...(left ? {right: 1080 - x + size * 0.75} : {left: x + size * 0.75}), textAlign: (left ? 'right' : 'left') as 'right' | 'left'}),
					opacity: chip,
					transform: `translateY(${(1 - chip) * 10}px)`,
					whiteSpace: 'nowrap',
				}}
			>
				<div style={{...kicker, fontSize: 26, color: gone > 0.5 ? palette.rust : CRYSTAL, textShadow: '0 2px 10px rgba(0,0,0,0.95)'}}>{gone > 0.5 && g.burnedKicker ? g.burnedKicker : g.kicker}</div>
				<div style={{marginTop: 4, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 56, lineHeight: 1.05, color: palette.parchment, textShadow: '0 2px 16px rgba(0,0,0,0.95)'}}>{g.price}</div>
			</div>
		</AbsoluteFill>
	);
};

type BoardRow = {label: string; gate: string; cart: string; at: Cue; win: 'gate' | 'cart'};
type Box = {x: number; y: number; s: number};

const BOARD_W = 900;
const HEAD_H = 104;
const ROW_H = 112;
const FOOT_H = 92;
const WALNUT = 'linear-gradient(180deg, #2c1e14 0%, #22170f 55%, #1b120c 100%)';
const BRASS = '#c9a35e';

/**
 * CountingBoard: a merchant's counting board, GATE (left, lilac crystal) against CART (right, amber wheel). `box: {x, y, s}`
 * is its top-left and scale (900 px wide at s 1). Each of `rows: [{label, gate, cart, at, win}]` appears at `at` with its
 * bead in the middle of a brass rod; 0.35 s later the bead slides to the `win` side with a small bounce, the winner's note
 * brightens and the loser's dims. Rows not yet cued are hidden; the newest row glows for a beat. `score: {at}` adds the
 * footer tally (CART n · GATE n). `moveAt` + `move: {x, y, s}` glides the board to a new box (the lesson). `enter: false`
 * skips the fade-in (the board carried over from the previous shot). `lessonKicker` / `lessonText` (lines; *word* = ember
 * italic) land at `lessonTop` on `lessonAt`.
 */
export const CountingBoard: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const rows: BoardRow[] = g.rows;
	const t0 = cueTime(timing, g.start, span.start);
	const vis = (g.enter === false ? 1 : ease(t, t0, 0.45)) * out(t, g.end ? cueTime(timing, g.end) : span.end + 0.25, 0.3);
	const b0: Box = g.box ?? {x: 90, y: 336, s: 0.8};
	const tMove = cue(timing, g.moveAt);
	const mv = at(t, tMove, 0.8);
	const b1: Box = g.move ?? b0;
	const bx = lerp(b0.x, b1.x, mv);
	const by = lerp(b0.y, b1.y, mv);
	const bs = lerp(b0.s, b1.s, mv);
	const times = rows.map((r) => cueTime(timing, r.at));
	const shown = rows.filter((_, i) => t >= times[i] - 0.05 || g.all);
	const tScore = cue(timing, g.score?.at);
	const score = at(t, tScore, 0.5);
	const tally = (side: 'gate' | 'cart') => rows.filter((r, i) => r.win === side && t >= times[i] + 0.5).length;
	const n = Math.max(1, shown.length);
	const h = HEAD_H + n * ROW_H + (score > 0 ? FOOT_H * score : 0) + 18;
	const tLesson = cue(timing, g.lessonAt);
	const lk = at(t, tLesson, 0.5);
	const lessonLines: string[] = Array.isArray(g.lessonText) ? g.lessonText : g.lessonText ? [g.lessonText] : [];
	return (
		<AbsoluteFill style={{opacity: vis, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: bx, top: by, width: BOARD_W, transform: `scale(${bs})`, transformOrigin: '0 0'}}>
				<div
					style={{
						position: 'relative',
						width: BOARD_W,
						height: h,
						background: WALNUT,
						border: `2px solid ${BRASS}`,
						borderRadius: 14,
						boxShadow: '0 18px 60px rgba(0,0,0,0.65), inset 0 0 0 6px rgba(0,0,0,0.25), inset 0 2px 0 rgba(255,220,160,0.08)',
						overflow: 'hidden',
					}}
				>
					{/* wood grain */}
					<svg width={BOARD_W} height={h} style={{position: 'absolute', inset: 0, opacity: 0.18}}>
						{Array.from({length: 14}, (_, i) => (
							<path key={i} d={`M0 ${20 + i * 52} C 220 ${10 + i * 52 + (i % 3) * 8}, 620 ${34 + i * 52 - (i % 4) * 6}, ${BOARD_W} ${18 + i * 52}`} stroke="#8a6440" strokeWidth={1.2} fill="none" />
						))}
					</svg>
					{[
						[16, 16],
						[BOARD_W - 26, 16],
						[16, h - 26],
						[BOARD_W - 26, h - 26],
					].map(([rx, ry], i) => (
						<div key={i} style={{position: 'absolute', left: rx, top: ry, width: 10, height: 10, borderRadius: 5, background: `radial-gradient(circle at 35% 35%, #f1d79a, ${BRASS} 60%, #6d5428)`}} />
					))}
					{/* header */}
					<div style={{position: 'absolute', top: 22, left: 50, display: 'flex', alignItems: 'center', gap: 14}}>
						<CrystalGlyph c={CRYSTAL} size={30} />
						<span style={{...kicker, fontSize: 34, color: CRYSTAL}}>Gate</span>
					</div>
					<div style={{position: 'absolute', top: 22, right: 50, display: 'flex', alignItems: 'center', gap: 14}}>
						<span style={{...kicker, fontSize: 34, color: palette.amber}}>Cart</span>
						<WheelGlyph c={palette.amber} size={40} />
					</div>
					<div style={{position: 'absolute', top: 34, left: 0, right: 0, textAlign: 'center', ...kicker, fontSize: 20, color: palette.fog, opacity: 0.8}}>{g.title ?? 'Who wins?'}</div>
					<div style={{position: 'absolute', top: HEAD_H - 14, left: 36, right: 36, height: 1.5, background: BRASS, opacity: 0.5}} />
					<div style={{position: 'absolute', top: HEAD_H, bottom: 18 + FOOT_H * score, left: BOARD_W / 2 - 1, width: 2, background: 'rgba(0,0,0,0.45)', boxShadow: '1px 0 0 rgba(255,220,160,0.08)'}} />
					{shown.map((r, i) => {
						const ta = times[rows.indexOf(r)];
						const appear = g.all ? 1 : ease(t, ta - 0.05, 0.35);
						const slide = g.all ? 1 : ease(t, ta + 0.35, 0.55, Easing.out(Easing.back(1.4)));
						const fresh = g.all ? 0 : Math.exp(-Math.max(0, t - ta - 0.6) * 1.6) * (t >= ta + 0.35 ? 1 : 0);
						const gate = r.win === 'gate';
						const wc = gate ? CRYSTAL : palette.amber;
						const rodL = 70;
						const rodR = BOARD_W - 70;
						const bead = lerp(BOARD_W / 2, gate ? rodL + 30 : rodR - 30, slide);
						const top = HEAD_H + i * ROW_H;
						const winO = lerp(0.75, 1, slide);
						const loseO = lerp(0.75, 0.5, slide);
						return (
							<div key={r.label} style={{position: 'absolute', top, left: 0, width: BOARD_W, height: ROW_H, opacity: appear}}>
								{fresh > 0.01 && <div style={{position: 'absolute', inset: '4px 20px', borderRadius: 10, background: wc, opacity: 0.1 * fresh}} />}
								<div style={{position: 'absolute', top: 10, left: 0, right: 0, textAlign: 'center', ...kicker, fontSize: 24, color: slide > 0.5 ? wc : palette.mist}}>{r.label}</div>
								<div style={{position: 'absolute', top: 52, left: rodL, width: rodR - rodL, height: 5, borderRadius: 3, background: `linear-gradient(180deg, #f1d79a, ${BRASS} 50%, #6d5428)`, opacity: 0.85}} />
								<div
									style={{
										position: 'absolute',
										top: 54 - 21,
										left: bead - 30,
										width: 60,
										height: 42,
										borderRadius: 21,
										background: `radial-gradient(ellipse at 40% 30%, #e9c48d, #a86f3a 55%, #5b3517)`,
										boxShadow: `0 4px 10px rgba(0,0,0,0.6)${slide > 0.9 ? `, 0 0 ${16 * (0.4 + fresh)}px ${wc}` : ''}`,
										border: slide > 0.9 ? `2px solid ${wc}` : '2px solid rgba(0,0,0,0.3)',
									}}
								/>
								<div style={{position: 'absolute', top: 66, left: 50, width: BOARD_W / 2 - 80, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 36, color: gate ? palette.parchment : palette.fog, opacity: gate ? winO : loseO, whiteSpace: 'nowrap'}}>
									{r.gate}
								</div>
								<div style={{position: 'absolute', top: 66, right: 50, width: BOARD_W / 2 - 80, textAlign: 'right', fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 36, color: gate ? palette.fog : palette.parchment, opacity: gate ? loseO : winO, whiteSpace: 'nowrap'}}>
									{r.cart}
								</div>
							</div>
						);
					})}
					{score > 0 && (
						<div style={{position: 'absolute', top: HEAD_H + n * ROW_H + 8, left: 36, right: 36, height: FOOT_H - 10, borderTop: `1.5px solid ${BRASS}`, opacity: score, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 14px'}}>
							<span style={{fontFamily: fonts.display, fontWeight: 700, fontSize: 60, color: CRYSTAL}}>{tally('gate')}</span>
							<span style={{...kicker, fontSize: 22, color: palette.fog}}>{g.score?.label ?? 'Most days, the cart'}</span>
							<span style={{fontFamily: fonts.display, fontWeight: 700, fontSize: 60, color: palette.amber}}>{tally('cart')}</span>
						</div>
					)}
				</div>
			</div>
			{lessonLines.length > 0 && (
				<div style={{position: 'absolute', top: g.lessonTop ?? 980, left: 60, right: 60, textAlign: 'center', opacity: lk, transform: `translateY(${(1 - lk) * 16}px)`}}>
					{g.lessonKicker && <div style={{...kicker, fontSize: 30, color: palette.amber, textShadow: '0 2px 12px rgba(0,0,0,0.9)'}}>{g.lessonKicker}</div>}
					{lessonLines.map((ln, li) => {
						const lp = ease(t, tLesson + 0.15 + li * 0.3, 0.6);
						return (
							<div key={li} style={{marginTop: li ? 0 : 14, fontFamily: fonts.display, fontWeight: 600, fontSize: g.lessonSize ?? 84, lineHeight: 1.06, color: palette.parchment, opacity: lp, textShadow: '0 4px 30px rgba(0,0,0,0.8)'}}>
								{ln.split(' ').map((w, k) => (
									<span key={k} style={w.startsWith('*') ? {color: palette.ember, fontStyle: 'italic'} : undefined}>
										{w.replace(/\*/g, '')}{' '}
									</span>
								))}
							</div>
						);
					})}
				</div>
			)}
		</AbsoluteFill>
	);
};

export const GATE: Record<string, React.FC<GraphicProps>> = {
	gateRing: GateRing,
	crystalPrice: CrystalPrice,
	countingBoard: CountingBoard,
};
