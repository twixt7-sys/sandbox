import React from 'react';
import {AbsoluteFill, Easing, random} from 'remotion';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {fonts, H, palette, W} from '../theme';
import type {Cue} from '../types';
import type {GraphicProps} from './Graphics';

/*
 * Spellbook graphics (EP21 onward, Arc 5: Magic and Its Rules). `spellPage`: a blank spell page drawn in code whose
 * three ruled lines (CAN / CAN'T / COSTS) are asked and written in ink on cues, with a three-point sigil that lights
 * one point per answer and only ignites once all three are written. `mendSeam`: a crack on the plate that magic
 * knits shut with light (or fails to). `storyQuestions`: the plot questions the answers raise, each tied to a row.
 */

const kicker: React.CSSProperties = {fontFamily: fonts.ui, fontWeight: 700, letterSpacing: '0.22em', textTransform: 'uppercase'};
const out = (t: number, end: number, dur = 0.35) => 1 - ease(t, end - dur, dur, Easing.in(Easing.quad));
const INK = '#2a2219';
const FADED = '#7d6d58';
const LIT = '#5b47a0';
const PAGE_W = 800;
const PAGE_H = 660;
const ROW_TOP = 200;
const ROW_H = 142;

type Row = {num: string; label: string; q: string; a: string; qAt?: Cue; aAt?: Cue};
type Box = {x: number; y: number; s: number};

/** Three-point sigil: a ring, an inscribed triangle and a node per question. `lit[i]` 0..1 per node, `ignite` 0..1. */
const Sigil: React.FC<{cx: number; cy: number; r: number; lit: number[]; ignite: number; motif: string; t: number}> = ({cx, cy, r, lit, ignite, motif, t}) => {
	const pts = [0, 1, 2].map((i) => {
		const a = -Math.PI / 2 + (i * 2 * Math.PI) / 3;
		return [cx + r * 0.78 * Math.cos(a), cy + r * 0.78 * Math.sin(a)] as const;
	});
	const breathe = 0.85 + 0.15 * Math.sin(t * 4.2);
	return (
		<g>
			{ignite > 0 && <circle cx={cx} cy={cy} r={r * (1.2 + 0.5 * ignite)} fill={motif} opacity={0.22 * ignite * breathe} style={{filter: 'blur(14px)'}} />}
			<circle cx={cx} cy={cy} r={r} fill="none" stroke={ignite > 0.5 ? LIT : INK} strokeOpacity={0.35 + 0.65 * ignite} strokeWidth={2.5 + 1.5 * ignite} />
			<circle cx={cx} cy={cy} r={r * 0.9} fill="none" stroke={INK} strokeOpacity={0.25} strokeWidth={1} strokeDasharray="3 6" />
			{pts.map(([x, y], i) => {
				const [nx, ny] = pts[(i + 1) % 3];
				const edge = Math.min(lit[i], lit[(i + 1) % 3]);
				return <line key={`e${i}`} x1={x} y1={y} x2={nx} y2={ny} stroke={edge > 0.5 ? LIT : INK} strokeOpacity={0.3 + 0.7 * Math.max(edge, ignite)} strokeWidth={2 + 1.5 * ignite} />;
			})}
			{pts.map(([x, y], i) => (
				<g key={`n${i}`}>
					{lit[i] > 0 && <circle cx={x} cy={y} r={12 + 6 * lit[i]} fill={motif} opacity={0.5 * lit[i]} style={{filter: 'blur(5px)'}} />}
					<circle cx={x} cy={y} r={7} fill={lit[i] > 0.5 ? motif : '#e9dfc6'} stroke={lit[i] > 0.5 ? '#6d5aa8' : INK} strokeWidth={2} />
				</g>
			))}
			<circle cx={cx} cy={cy} r={4 + 4 * ignite} fill={ignite > 0.3 ? LIT : INK} opacity={0.4 + 0.6 * ignite} />
		</g>
	);
};

/**
 * Spell page: a parchment page at `at: {x, y, s}` (top-left corner and scale; 800×660 at s 1), optionally gliding in
 * from `from` over 0.6 s. Header: rust caps `kicker`, then the `title` (written at `titleAt`, else blank ruled line).
 * `rows: [{num, label, q, a, qAt, aAt}]`: each row shows its numeral and an empty dashed line; at `qAt` the caps label
 * and the faded question appear, at `aAt` the answer is written in ink (left-to-right reveal). Cues are absolute, so a
 * copy of the page in a later shot shows earlier rows already written. `active` (row index) marks the row being
 * answered. The sigil lights node i at `aAt` (or `litAt[i]`) and ignites at `igniteAt` (motif-coloured glow).
 * `pulseAt` pulses the three numerals; `dim` lays a midnight wash behind the page; `lessonText` (lines, *word* = ember
 * italic) lands at `lessonAt` beneath it at `lessonTop`.
 */
export const SpellPage: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const rows: Row[] = g.rows ?? [];
	const motif: string = g.motif ?? palette.ember;
	const t0 = cueTime(timing, g.start, span.start);
	const vis = (g.instant ? 1 : ease(t, t0, 0.5)) * out(t, (g.end ? cueTime(timing, g.end) : span.end) + 0.25, 0.3);
	const to: Box = g.at ?? {x: 140, y: 380, s: 1};
	const from: Box = g.from ?? to;
	const mv = ease(t, t0, 0.6);
	const box = {x: lerp(from.x, to.x, mv), y: lerp(from.y, to.y, mv), s: lerp(from.s, to.s, mv)};
	const q = rows.map((r) => (r.qAt ? cueTime(timing, r.qAt) : -1e9));
	const a = rows.map((r) => (r.aAt ? cueTime(timing, r.aAt) : 1e9));
	const litT: number[] = g.litAt ? g.litAt.map((c: Cue) => cueTime(timing, c)) : a;
	const lit = litT.map((x) => ease(t, x + 0.5, 0.4));
	const ignite = g.igniteAt ? ease(t, cueTime(timing, g.igniteAt), 0.7) : 0;
	const pulseT = g.pulseAt ? cueTime(timing, g.pulseAt) : 1e9;
	const titleP = g.titleAt ? ease(t, cueTime(timing, g.titleAt), 0.6) : a[0] < 1e8 ? ease(t, a[0], 0.6) : 0;
	const lessonLines: string[] = g.lessonText ?? [];
	const tLesson = g.lessonAt ? cueTime(timing, g.lessonAt) : 1e9;
	return (
		<AbsoluteFill style={{opacity: vis}}>
			{g.dim ? <AbsoluteFill style={{background: `radial-gradient(ellipse 85% 60% at 50% 42%, rgba(7,14,30,${g.dim * 0.7}) 0%, rgba(7,14,30,${g.dim}) 100%)`}} /> : null}
			<div style={{position: 'absolute', left: box.x, top: box.y, width: PAGE_W, height: PAGE_H, transformOrigin: '0 0', transform: `scale(${box.s}) rotate(-1.2deg)`}}>
				{/* Ignition halo behind the page. */}
				{ignite > 0 && <div style={{position: 'absolute', inset: -40, borderRadius: 30, background: motif, opacity: 0.28 * ignite, filter: 'blur(40px)'}} />}
				<div
					style={{
						position: 'absolute',
						inset: 0,
						borderRadius: 6,
						background: 'radial-gradient(ellipse 90% 80% at 45% 40%, #efe5cc 0%, #e3d5b5 70%, #cdb98f 100%)',
						boxShadow: `0 18px 50px rgba(0,0,0,0.6), inset 0 0 60px rgba(120,90,50,0.35)${ignite > 0 ? `, 0 0 ${50 * ignite}px ${motif}` : ''}`,
					}}
				/>
				<div style={{position: 'absolute', left: 52, top: 40, ...kicker, fontSize: 22, color: palette.rust}}>{g.kicker ?? 'A new spell'}</div>
				{/* Title: a blank ruled line until the spell has a name. */}
				<div style={{position: 'absolute', left: 52, top: 82, width: 470, height: 80, borderBottom: `2px dashed rgba(42,34,25,${0.45 * (1 - titleP)})`}}>
					<div style={{fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: 76, lineHeight: '80px', color: INK, clipPath: `inset(-20px ${(1 - titleP) * 100}% -20px 0)`}}>{g.title}</div>
				</div>
				<svg width={PAGE_W} height={PAGE_H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					<Sigil cx={668} cy={110} r={74} lit={lit} ignite={ignite} motif={motif} t={t} />
					<line x1={52} y1={182} x2={PAGE_W - 52} y2={182} stroke={INK} strokeOpacity={0.35} strokeWidth={1.5} />
				</svg>
				{rows.map((r, i) => {
					const top = ROW_TOP + i * ROW_H;
					const qp = ease(t, q[i], 0.45);
					const wp = ease(t, a[i], 0.8, Easing.inOut(Easing.quad));
					const pulse = ease(t, pulseT + i * 0.15, 0.2) * (1 - ease(t, pulseT + i * 0.15 + 0.25, 0.5));
					const flash = ease(t, litT[i], 0.2) * (1 - ease(t, litT[i] + 0.2, 0.6));
					const on = g.active === i;
					return (
						<div key={i} style={{position: 'absolute', left: 0, top, width: PAGE_W, height: ROW_H}}>
							{on && <div style={{position: 'absolute', left: 22, top: 10, width: 6, height: ROW_H - 26, borderRadius: 3, background: palette.rust, opacity: 0.85}} />}
							{flash > 0 && <div style={{position: 'absolute', left: 30, right: 30, top: 6, bottom: 10, borderRadius: 8, background: motif, opacity: 0.35 * flash}} />}
							<div
								style={{
									position: 'absolute',
									left: 46,
									top: 14,
									width: 58,
									height: 58,
									borderRadius: 29,
									border: `2px solid ${INK}`,
									textAlign: 'center',
									lineHeight: '54px',
									fontFamily: fonts.display,
									fontWeight: 700,
									fontSize: 28,
									color: INK,
									transform: `scale(${1 + 0.25 * pulse})`,
									background: pulse > 0 ? `rgba(185,84,58,${0.35 * pulse})` : undefined,
								}}
							>
								{r.num}
							</div>
							<div style={{position: 'absolute', left: 124, top: 16, whiteSpace: 'nowrap', opacity: qp, transform: `translateY(${(1 - qp) * 8}px)`}}>
								<span style={{...kicker, fontWeight: 800, fontSize: 24, color: palette.rust}}>{r.label}</span>
								<span style={{marginLeft: 16, fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 500, fontSize: 32, color: FADED}}>{r.q}</span>
							</div>
							{/* The answer line: dashed and empty until written. */}
							<div style={{position: 'absolute', left: 124, right: 52, top: 60, height: 62, borderBottom: `2px dashed rgba(42,34,25,${0.5 - 0.3 * wp})`}}>
								<div style={{whiteSpace: 'nowrap', fontFamily: fonts.display, fontWeight: 600, fontSize: g.answerSize ?? 40, lineHeight: '62px', color: INK, clipPath: `inset(-20px ${(1 - wp) * 100}% -20px 0)`}}>{r.a}</div>
							</div>
						</div>
					);
				})}
			</div>
			{lessonLines.length > 0 && (
				<div style={{position: 'absolute', top: g.lessonTop ?? 1040, left: 60, right: 60, textAlign: 'center'}}>
					{lessonLines.map((ln, li) => {
						const lp = ease(t, tLesson + li * 0.25, 0.6);
						return (
							<div key={li} style={{fontFamily: fonts.display, fontWeight: 600, fontSize: g.lessonSize ?? 84, lineHeight: 1.06, color: palette.parchment, opacity: lp, transform: `translateY(${(1 - lp) * 16}px)`, textShadow: '0 4px 30px rgba(0,0,0,0.8)'}}>
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

/** Point at fraction `f` (0..1) along a polyline, plus the total length. */
const along = (pts: number[][], f: number) => {
	const seg = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
	const total = seg.reduce((s, x) => s + x, 0);
	let d = f * total;
	for (let i = 0; i < seg.length; i++) {
		if (d <= seg[i] || i === seg.length - 1) {
			const k = seg[i] ? Math.min(1, d / seg[i]) : 0;
			return {x: lerp(pts[i][0], pts[i + 1][0], k), y: lerp(pts[i][1], pts[i + 1][1], k), total};
		}
		d -= seg[i];
	}
	return {x: pts[0][0], y: pts[0][1], total};
};

const pathD = (pts: number[][]) => pts.map((p, i) => `${i ? 'L' : 'M'}${p[0]} ${p[1]}`).join(' ');

/**
 * Mend seam (`local`): a crack on the plate along `crack: [[x, y], …]` plus optional `branches` (polylines). It opens
 * at `crackAt`, growing over `crackDur` (0 = already there). At `mendAt` light runs along it over `mendDur` in the
 * `motif` colour and leaves a thin glowing seam where the crack was. `fail: true`: the light gets about 60 % (`reach`) of the
 * way, gutters to rust and dies, and the crack stays (the limit). `mended: true` shows the finished seam only.
 */
export const MendSeam: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const motif: string = g.motif ?? palette.ember;
	const pts: number[][] = g.crack;
	const branches: number[][][] = g.branches ?? [];
	const tc = cueTime(timing, g.crackAt, span.start);
	const grow = g.crackDur ? ease(t, tc, g.crackDur, Easing.out(Easing.cubic)) : t >= tc ? 1 : 0;
	const tm = g.mendAt ? cueTime(timing, g.mendAt) : 1e9;
	const dur = g.mendDur ?? 0.9;
	const reach = g.fail ? g.reach ?? 0.6 : 1;
	const m = g.mended ? 1 : ease(t, tm, dur, Easing.inOut(Easing.quad)) * reach;
	const done = g.mended ? 1 : g.fail ? 0 : ease(t, tm + dur, 0.6);
	const die = g.fail ? ease(t, tm + dur * 0.55, 0.7) : 0;
	const flicker = g.fail && t > tm + dur * 0.3 ? 0.45 + 0.55 * random(`f${Math.floor(t * 24)}`) : 1;
	const glowC = die > 0.2 ? palette.rust : motif;
	const head = along(pts, m);
	const crackO = (g.mended ? 0 : grow) * (1 - done);
	const branchGrow = g.crackDur ? ease(t, tc + g.crackDur * 0.4, g.crackDur, Easing.out(Easing.cubic)) : grow;
	const live = m > 0 && !(g.fail && die >= 1);
	const o = out(t, span.end + 0.3, 0.3);
	return (
		<AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				{/* The crack: a dark fissure with a pale lit edge. */}
				<g opacity={crackO}>
					<path d={pathD(pts)} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - grow} fill="none" stroke="#0b0806" strokeWidth={g.width ?? 6} strokeLinejoin="round" strokeLinecap="round" />
					<path d={pathD(pts.map(([x, y]) => [x + 2, y + 1]))} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - grow} fill="none" stroke="rgba(255,240,220,0.45)" strokeWidth={1.5} strokeLinejoin="round" />
					{branches.map((b, i) => (
						<path key={i} d={pathD(b)} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - branchGrow} fill="none" stroke="#0b0806" strokeWidth={(g.width ?? 6) * 0.6} strokeLinecap="round" />
					))}
				</g>
				{/* The mend: light running along the crack, settling into a seam. */}
				{live && (
					<g opacity={(1 - die) * flicker}>
						<path d={pathD(pts)} pathLength={1} strokeDasharray={`${m} 2`} fill="none" stroke={glowC} strokeWidth={18} strokeLinecap="round" strokeLinejoin="round" opacity={0.45 * (1 - 0.6 * done)} style={{filter: 'blur(8px)'}} />
						<path d={pathD(pts)} pathLength={1} strokeDasharray={`${m} 2`} fill="none" stroke={glowC} strokeWidth={3.5 - done} strokeLinecap="round" strokeLinejoin="round" />
						{m < reach - 0.001 || (g.fail && die < 1) ? (
							<>
								<circle cx={head.x} cy={head.y} r={22} fill={glowC} opacity={0.55} style={{filter: 'blur(8px)'}} />
								<circle cx={head.x} cy={head.y} r={6} fill="#fff" opacity={0.9} />
							</>
						) : null}
						{done > 0 &&
							branches.map((b, i) => <path key={i} d={pathD(b)} fill="none" stroke={motif} strokeWidth={2} strokeLinecap="round" opacity={0.8 * done} />)}
					</g>
				)}
			</svg>
		</AbsoluteFill>
	);
};

/**
 * Story questions: the plot the three answers raise. `items: [{num, text, at}]` stack down from `top` (default 560) at
 * x 90, each a row numeral badge (which answer raised it) and an ember italic question, rising in on its cue.
 */
export const StoryQuestions: React.FC<GraphicProps> = ({g, t, span}) => {
	const timing = useTiming();
	const items: {num: string; text: string; at: Cue}[] = g.items ?? [];
	const o = out(t, span.end + 0.2, 0.35);
	return (
		<AbsoluteFill style={{opacity: o}}>
			{items.map((it, i) => {
				const p = ease(t, cueTime(timing, it.at), 0.5);
				return (
					<div key={i} style={{position: 'absolute', left: 90, top: (g.top ?? 560) + i * (g.gap ?? 108), display: 'flex', alignItems: 'center', gap: 20, opacity: p, transform: `translateX(${(1 - p) * -24}px)`}}>
						<div style={{width: 54, height: 54, borderRadius: 27, border: `2px solid ${palette.amber}`, textAlign: 'center', lineHeight: '50px', fontFamily: fonts.display, fontWeight: 700, fontSize: 26, color: palette.amber, background: 'rgba(8,12,16,0.65)'}}>{it.num}</div>
						<div style={{fontFamily: fonts.display, fontStyle: 'italic', fontWeight: 600, fontSize: g.size ?? 58, color: palette.ember, padding: '4px 18px 8px', background: 'rgba(8,12,16,0.62)', borderRadius: 6, textShadow: '0 2px 14px rgba(0,0,0,0.9)', whiteSpace: 'nowrap'}}>
							{it.text}
						</div>
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

export const SPELLBOOK: Record<string, React.FC<GraphicProps>> = {
	spellPage: SpellPage,
	mendSeam: MendSeam,
	storyQuestions: StoryQuestions,
};
