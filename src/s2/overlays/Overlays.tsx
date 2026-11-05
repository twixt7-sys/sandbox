// Season 2 overlays ("graphics" with S2 types). Each reads the narration timing for its cues and the world state
// (useS2) for numbers and 3D positions, so every on-screen number matches what the diorama shows.
import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile} from 'remotion';
import {Logo, useBrand} from '../../brand/Logo';
import {cueTime, ease, useTiming} from '../../lib/timing';
import type {Cue, Graphic} from '../../types';
import {sample} from '../keys';
import {clamp, hash2} from '../rng';
import {F2, outline, panel, pixelShadow, PX, S2} from '../style';
import {grimmawPose, project, useS2} from '../world/WorldScene';
import {clockAt, dragonAt, herdCount, seriesAt, simTime, World} from '../world/timeline';
import {dragonTargets, roofsIntact, Target} from '../world/Settlement';

/** A HUD value by key: herd, pred, roofs (EP27: standing, unburnt roofs, read from the village itself) or a world series. */
const hudValue = (w: World, key: string, t: number) => (key === 'roofs' ? roofsIntact(w, t) : seriesAt(w, key, t));
import {PixelSprite} from './Pixel';

type OP = {g: Graphic; t: number};

const useWin = (g: Graphic, t: number, fadeIn = 0.25, fadeOut = 0.25) => {
	const timing = useTiming();
	const a = cueTime(timing, g.start, 0);
	const b = g.end ? cueTime(timing, g.end) : Infinity;
	// A graphic that starts at 0 is fully visible on frame 0 (the first frame is the thumbnail / the loop target).
	const o = Math.min(a <= 0.001 ? 1 : clamp((t - a) / fadeIn), b === Infinity ? 1 : 1 - clamp((t - b) / fadeOut));
	return {a, b, o, timing};
};

const col = (c?: string) => (c ? ((S2 as Record<string, string>)[c] ?? c) : S2.parchment);

// ---------------------------------------------------------------- kinetic type

/** Big headline words that pop in on their cues: parts [{text, at, color, size}] stacked from y. */
export const Kinetic: React.FC<OP> = ({g, t}) => {
	const {o, timing} = useWin(g, t, g.fadeIn ?? 0.12, g.fadeOut ?? 0.2);
	if (o <= 0) return null;
	const font = g.font === 'serif' ? F2.serif : g.font === 'caption' ? F2.caption : F2.pixel;
	let y = g.y ?? 470;
	return (
		<AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
			{(g.parts as {text: string; at?: Cue; color?: string; size?: number; italic?: boolean}[]).map((p, i) => {
				const at = p.at ? cueTime(timing, p.at) : cueTime(timing, g.start, 0);
				const size = p.size ?? g.size ?? 96;
				const top = y;
				y += size * (g.font === 'serif' ? 1.05 : 1.12);
				const k = at <= 0.001 || g.preShow ? 1 : clamp((t - at) / 0.16);
				if (t < at - 0.001 && !g.preShow) return null;
				const pop = g.preShow ? 1 : 1 + (1 - k) * 0.35 + Math.max(0, Math.sin(clamp((t - at) / 0.3) * Math.PI)) * 0.04;
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: 70,
							right: 140,
							top,
							textAlign: g.align ?? 'center',
							fontFamily: font,
							fontWeight: g.font === 'serif' ? 600 : g.font === 'caption' ? 900 : 700,
							fontStyle: p.italic ? 'italic' : 'normal',
							fontSize: size,
							lineHeight: 1,
							letterSpacing: g.font === 'pixel' || !g.font ? '0.02em' : '-0.01em',
							color: col(p.color),
							transform: `scale(${pop})`,
							transformOrigin: '50% 60%',
							opacity: k,
							textShadow: g.font === 'serif' ? `0 4px 18px rgba(0,0,0,0.6), ${outline('#050912', 3)}` : outline('#050912', 7),
						}}
					>
						{p.text}
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- HUD: the sim bar

const Counter: React.FC<{icon: string; label: string; value: number; color: string; flash: number; compact?: boolean; digits?: number}> = ({icon, label, value, color, flash, compact, digits = 3}) => (
	<div style={{display: 'flex', alignItems: 'center', gap: compact ? 10 : 14}}>
		<PixelSprite name={icon} px={compact ? 4 : 6} />
		<div style={{display: 'flex', flexDirection: 'column', lineHeight: 1}}>
			<span style={{fontFamily: F2.pixel, fontSize: compact ? 18 : 21, color: 'rgba(239,230,210,0.75)', letterSpacing: '0.06em'}}>{label}</span>
			<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: compact ? 40 : 46, color: value === 0 ? S2.rust : color, textShadow: flash > 0 ? `0 0 ${12 * flash}px ${color}` : undefined}}>
				{String(Math.round(value)).padStart(digits, '0')}
			</span>
		</div>
	</div>
);

export const SimBar: React.FC<OP> = ({g, t}) => {
	const {o, timing} = useWin(g, t, 0.3, 0.3);
	const {world} = useS2();
	if (o <= 0) return null;
	const runs: number[] = (g.runAt ?? []).map((c: Cue) => cueTime(timing, c));
	const lastRun = runs.filter((r) => r <= t).pop();
	const speed = sample(world.speed, t, 1);
	const running = speed > 1.6;
	const pressed = lastRun !== undefined && t - lastRun < 0.22;
	const year = clockAt(world, t);
	const herd = herdCount(world, t);
	const pred = sample(world.pred, t, 0);
	const herdPrev = herdCount(world, t - 0.15);
	const rise = interpolate(o, [0, 1], [-30, 0]);
	// EP27+: `compact` fits three counters and the clock in the same 804 px bar
	const cp: boolean = Boolean(g.compact);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 90 + 6, top: 340 + rise, width: 804, height: 92, display: 'flex', alignItems: 'center', gap: cp ? 14 : 22, padding: cp ? '0 16px' : '0 22px', boxSizing: 'border-box', ...panel()}}>
				<div
					style={{
						display: 'flex',
						alignItems: 'center',
						gap: 10,
						padding: cp ? '0 12px' : '0 16px',
						height: 58,
						background: running || pressed ? S2.ember : 'rgba(239,230,210,0.12)',
						color: running || pressed ? S2.ink : S2.ember,
						boxShadow: pressed ? 'none' : `0 6px 0 ${running ? '#a8762b' : 'rgba(239,230,210,0.25)'}`,
						transform: `translateY(${pressed ? 6 : 0}px)`,
						fontFamily: F2.pixel,
						fontWeight: 700,
						fontSize: cp ? 24 : 30,
					}}
				>
					<PixelSprite name={running ? 'ffwd' : 'play'} px={cp ? 5 : 6} style={{opacity: running ? (Math.floor(t * 6) % 2 ? 1 : 0.45) : 1}} />
					<span>{running ? 'RUNNING' : 'RUN'}</span>
				</div>
				<div style={{display: 'flex', flexDirection: 'column', lineHeight: 1, minWidth: cp ? 76 : 128}}>
					<span style={{fontFamily: F2.pixel, fontSize: cp ? 18 : 21, color: 'rgba(239,230,210,0.75)', letterSpacing: '0.06em'}}>{world.clockLabel}</span>
					<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: cp ? 40 : 46, color: S2.parchment}}>{String(Math.floor(year + 1e-6)).padStart(2, '0')}</span>
				</div>
				<div style={{flex: 1}} />
				{g.counters ? (
					(g.counters as {icon: string; label: string; key: string; color?: string; digits?: number}[]).map((c) => {
						const v = hudValue(world, c.key, t);
						const vp = hudValue(world, c.key, t - 0.15);
						return <Counter key={c.key} icon={c.icon} label={c.label} value={v} color={col(c.color ?? 'prey')} flash={Math.abs(v - vp) > 0.5 ? 1 : 0} compact={cp} digits={c.digits} />;
					})
				) : (
					<>
						<Counter icon="mossback" label={g.preyLabel ?? 'MOSSBACKS'} value={herd} color={S2.prey} flash={Math.abs(herd - herdPrev) > 0.5 ? 1 : 0} />
						<Counter icon="grimmaw" label={g.predLabel ?? 'GRIMMAW'} value={pred} color={S2.pred} flash={0} />
					</>
				)}
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- population graph

export const SimGraph: React.FC<OP> = ({g, t}) => {
	const {o, timing} = useWin(g, t, 0.3, 0.3);
	const {world} = useS2();
	if (o <= 0) return null;
	const from = cueTime(timing, g.from);
	const to = cueTime(timing, g.to);
	const W = 804;
	const H = g.h ?? 200;
	const y0 = g.y ?? 456;
	const N = 67;
	const step = W / N;
	const now = clamp((t - from) / (to - from));
	const series: {key: string; color: string; max: number; label: string}[] = g.series ?? [
		{key: 'herd', color: S2.prey, max: 400, label: 'MOSSBACKS'},
		{key: 'pred', color: S2.pred, max: 4, label: 'GRIMMAW'},
	];
	const val = (key: string, tt: number) => (key === 'herd' ? herdCount(world, tt) : key === 'pred' ? sample(world.pred, tt, 0) : hudValue(world, key, tt));
	const plotH = H - 66;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 96, top: y0, width: W, height: H, ...panel({bg: 'rgba(5, 10, 26, 0.86)'})}}>
				<div style={{position: 'absolute', left: 18, top: 12, display: 'flex', gap: 26, fontFamily: F2.pixel, fontSize: 21, letterSpacing: '0.05em'}}>
					{series.map((s) => (
						<span key={s.key} style={{color: s.color}}>
							■ {s.label}
						</span>
					))}
					<span style={{color: 'rgba(239,230,210,0.55)'}}>{g.caption ?? 'POPULATION'}</span>
				</div>
				<svg width={W} height={plotH} style={{position: 'absolute', left: 0, top: 50}} shapeRendering="crispEdges">
					{[0.25, 0.5, 0.75].map((f) => (
						<rect key={f} x={0} y={Math.round(plotH * f)} width={W} height={2} fill="rgba(239,230,210,0.08)" />
					))}
					{series.map((s) => {
						const pts: React.ReactNode[] = [];
						let prevY: number | null = null;
						for (let i = 0; i <= N; i++) {
							const f = i / N;
							if (f > now + 1e-6) break;
							const v = val(s.key, from + f * (to - from));
							const yy = Math.round((plotH - 12) * (1 - clamp(v / s.max)) / PX) * PX + 2;
							const xx = Math.round((i * step) / PX) * PX;
							if (prevY !== null) {
								const lo = Math.min(prevY, yy);
								pts.push(<rect key={`v${i}`} x={xx} y={lo} width={PX * 2} height={Math.abs(prevY - yy) + PX * 2} fill={s.color} />);
							}
							pts.push(<rect key={`h${i}`} x={xx} y={yy} width={Math.ceil(step / PX) * PX + PX} height={PX * 2} fill={s.color} />);
							prevY = yy;
						}
						return <g key={s.key}>{pts}</g>;
					})}
				</svg>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- stamp

export const Stamp: React.FC<OP> = ({g, t}) => {
	const {a, o} = useWin(g, t, 0.01, 0.3);
	if (o <= 0 || t < a) return null;
	const k = clamp((t - a) / 0.14);
	const scale = 1.9 - 0.9 * k;
	const shake = t - a < 0.3 ? (hash2(Math.floor(t * 30), 3) - 0.5) * 10 * (1 - (t - a) / 0.3) : 0;
	const c = col(g.color ?? 'rust');
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: g.y ?? 700, display: 'flex', justifyContent: 'center'}}>
				<div
					style={{
						transform: `translate(${shake}px, ${shake * 0.6}px) rotate(${g.rotate ?? -6}deg) scale(${scale})`,
						opacity: k,
						border: `${PX * 3}px solid ${c}`,
						padding: '14px 34px 10px',
						fontFamily: F2.pixel,
						fontWeight: 700,
						fontSize: g.size ?? 104,
						color: c,
						letterSpacing: '0.06em',
						background: 'rgba(5, 9, 18, 0.55)',
						textShadow: pixelShadow('#050912', 2),
						boxShadow: `${PX * 3}px ${PX * 3}px 0 rgba(5,9,18,0.8)`,
					}}
				>
					{g.text}
					{g.sub && <div style={{fontSize: 30, letterSpacing: '0.12em', textAlign: 'center', marginTop: 6}}>{g.sub}</div>}
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the field card (creature checklist)

type Row = {n: number; label: string; text: string; at: Cue; locked?: boolean; unlockAt?: Cue};

export const FieldCard: React.FC<OP> = ({g, t}) => {
	const {o, timing} = useWin(g, t, 0.28, 0.28);
	if (o <= 0) return null;
	const mode: 'intro' | 'checklist' | 'full' = g.mode ?? 'checklist';
	const rows: Row[] = g.rows ?? [];
	const times = rows.map((r) => (r.at ? cueTime(timing, r.at) : Infinity));
	const unlocks = rows.map((r) => (r.unlockAt ? cueTime(timing, r.unlockAt) : Infinity));
	const slide = (1 - ease(t, cueTime(timing, g.start, 0), 0.35)) * -60;
	const y = g.y ?? 440;
	const W = 804;
	const active = times.reduce((acc, at, i) => (t >= at ? i : acc), -1);
	const sprite = staticFile(g.sprite ?? 'ep26/grimmaw_sprite.png');
	// sprite size in sprite pixels (EP26's Grimmaw is 168x108); a taller sprite pushes the intro card's text down
	const spW: number = g.spriteW ?? 168;
	const spH: number = g.spriteH ?? 108;
	const dy = (spH - 108) * 3;
	if (mode === 'intro') {
		const dietAt = g.dietAt ? cueTime(timing, g.dietAt) : Infinity;
		const dk = clamp((t - dietAt) / 0.2);
		return (
			<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
				<div style={{position: 'absolute', left: 96, top: y + slide, width: W, height: 530 + dy, ...panel()}}>
					<div style={{position: 'absolute', left: 24, top: 18, fontFamily: F2.pixel, fontSize: 24, color: S2.amber, letterSpacing: '0.08em'}}>{g.kicker ?? 'FIELD CARD · NO. 001'}</div>
					<div style={{position: 'absolute', right: 24, top: 18, fontFamily: F2.pixel, fontSize: 24, color: 'rgba(239,230,210,0.6)', letterSpacing: '0.08em'}}>{g.kind ?? 'APEX PREDATOR'}</div>
					<Img src={sprite} style={{position: 'absolute', left: (W - spW * 3) / 2, top: 58, width: spW * 3, height: spH * 3, imageRendering: 'pixelated'}} />
					<div style={{position: 'absolute', left: 24, top: 398 + dy, fontFamily: F2.pixel, fontWeight: 700, fontSize: 64, color: S2.parchment, textShadow: pixelShadow('#050912', 2)}}>{g.name ?? 'GRIMMAW'}</div>
					<div style={{position: 'absolute', left: 24, right: 24, top: 470 + dy, display: 'flex', alignItems: 'center', gap: 16, opacity: dk, transform: `translateX(${(1 - dk) * 30}px)`}}>
						<span style={{fontFamily: F2.pixel, fontSize: 26, color: 'rgba(239,230,210,0.7)', letterSpacing: '0.08em'}}>{g.dietLabel ?? 'DIET'}</span>
						<span style={{fontFamily: F2.pixelSans, fontWeight: 600, fontSize: 36, color: S2.rust}}>{g.diet ?? 'anything that moves'}</span>
					</div>
				</div>
			</AbsoluteFill>
		);
	}
	const big = mode === 'full';
	const rowH = big ? 92 : 56;
	const headH = big ? 168 : 84;
	// `collapse` keys fold the checklist to its header (e.g. while a run's graph needs the space).
	const fold = sample((g.collapse ?? []).map((k: [Cue, number]) => ({t: cueTime(timing, k[0]), v: k[1], e: 'smooth'})), t, 0);
	const H = headH + (rows.length * rowH + 22) * (1 - fold) + (fold > 0 ? 6 : 0);
	const done = rows.filter((r, i) => t >= times[i] && (!r.locked || t >= unlocks[i])).length;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 96, top: y + slide, width: W, height: H, overflow: 'hidden', ...panel()}}>
				<Img
					src={sprite}
					style={{position: 'absolute', left: 16, top: big ? 14 : 8, width: spW * (big ? 0.9 : 0.5) * (108 / spH), height: 108 * (big ? 0.9 : 0.5), imageRendering: 'pixelated', transform: big ? 'scale(1)' : undefined}}
				/>
				<div style={{position: 'absolute', left: big ? 186 : 112, top: big ? 22 : 16, fontFamily: F2.pixel, fontSize: big ? 26 : 21, color: S2.amber, letterSpacing: '0.08em'}}>{g.kicker ?? 'DESIGN CHECK'}</div>
				<div style={{position: 'absolute', left: big ? 186 : 112, top: big ? 56 : 42, fontFamily: F2.pixel, fontWeight: 700, fontSize: big ? 50 : 36, color: S2.parchment}}>{g.title ?? 'GRIMMAW'}</div>
				<div style={{position: 'absolute', right: 22, top: big ? 30 : 22, fontFamily: F2.pixel, fontWeight: 700, fontSize: big ? 52 : 40, color: done === rows.length ? S2.stable : S2.ember}}>
					{done}/{rows.length}
				</div>
				{big && g.subtitle && (
					<div style={{position: 'absolute', left: 186, top: 112, fontFamily: F2.serif, fontStyle: 'italic', fontWeight: 600, fontSize: 40, color: S2.ember, opacity: g.subtitleAt ? clamp((t - cueTime(timing, g.subtitleAt)) / 0.3) : 1}}>
						{g.subtitle}
					</div>
				)}
				{rows.map((r, i) => {
					const shown = t >= times[i];
					const locked = r.locked && t < unlocks[i];
					const reveal = r.locked ? clamp((t - unlocks[i]) / 0.25) : clamp((t - times[i]) / 0.25);
					const isActive = i === active && !big && (!r.locked || t >= unlocks[i] || true);
					const top = headH + i * rowH;
					const blink = locked && g.blinkAt && t > cueTime(timing, g.blinkAt) ? (Math.floor(t * 4) % 2 ? 1 : 0.4) : 1;
					return (
						<div key={i} style={{position: 'absolute', left: 16, right: 16, top, height: rowH - 10, display: 'flex', alignItems: 'center', gap: 16, padding: '0 14px', background: isActive ? 'rgba(244,196,110,0.16)' : 'rgba(239,230,210,0.05)', boxShadow: isActive ? `inset 0 0 0 ${PX}px ${S2.ember}` : undefined}}>
							<div style={{width: big ? 48 : 40, height: big ? 48 : 40, flex: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', background: shown && !locked ? (r.locked ? S2.ember : S2.stable) : 'rgba(239,230,210,0.1)', color: S2.ink}}>
								{locked ? <PixelSprite name="lock" px={5} color={S2.ember} style={{opacity: blink}} /> : shown ? <PixelSprite name="check" px={5} style={{opacity: reveal}} /> : null}
							</div>
							<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: big ? 25 : 22, color: locked ? S2.ember : shown ? S2.parchment : 'rgba(239,230,210,0.35)', width: big ? 222 : 196, flex: 'none', letterSpacing: '0.02em', whiteSpace: 'nowrap', opacity: locked ? blink : 1}}>
								{r.n} {locked ? '???' : r.label}
							</span>
							<span style={{fontFamily: F2.pixelSans, fontWeight: 500, fontSize: big ? 29 : 26, color: locked ? 'rgba(244,196,110,0.75)' : 'rgba(239,230,210,0.92)', opacity: locked ? blink : reveal, transform: `translateX(${(1 - reveal) * 20}px)`, whiteSpace: 'nowrap'}}>
								{locked ? (g.lockedText ?? 'the twist') : shown ? r.text : ''}
							</span>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- labels pinned to the world

const pinTarget = (g: Graphic, s: ReturnType<typeof useS2>): [number, number, number] | null => {
	if (g.dragon) {
		const d = s.world.dragons.find((dd) => dd.id === g.dragon);
		const dp = d ? dragonAt(d.keys, s.t, (x, z) => Math.max(s.island.waterLevel, s.island.heightAt(x, z))) : null;
		if (!d || !dp) return null;
		return [dp.x, dp.y + (g.dy ?? 3.6) * d.scale, dp.z];
	}
	if (g.pred) {
		const idx = s.world.predators.findIndex((p) => p.id === g.pred);
		if (idx < 0) return null;
		const pose = grimmawPose(s.island, s.world.predators[idx], s.t, simTime(s.world, s.t), idx);
		if (!pose) return null;
		return [pose.x, pose.y + (g.dy ?? 3.2) * pose.scale - pose.rest * 0.8, pose.z];
	}
	const [x, y, z] = g.at as [number, number, number];
	return [x, y ?? s.island.heightAt(x, z) + 1, z];
};

export const Pin: React.FC<OP> = ({g, t}) => {
	const {o} = useWin(g, t, 0.2, 0.2);
	const s = useS2();
	if (o <= 0) return null;
	const p = pinTarget(g, s);
	if (!p) return null;
	const sc = project(s.cam, p);
	if (sc.behind) return null;
	const lift = g.lift ?? 110;
	const c = col(g.color ?? 'ember');
	const x = Math.max(160, Math.min(860, sc.x));
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: sc.x - PX, top: sc.y - lift, width: PX * 2, height: lift - 8, background: c, opacity: 0.85}} />
			<div style={{position: 'absolute', left: sc.x - 9, top: sc.y - 9, width: 18, height: 18, background: c, boxShadow: `0 0 0 ${PX}px #050912`}} />
			<div style={{position: 'absolute', left: x, top: sc.y - lift - 70, transform: 'translateX(-50%)', padding: '10px 18px 8px', whiteSpace: 'nowrap', textAlign: 'center', ...panel({edge: c})}}>
				{g.kicker && <div style={{fontFamily: F2.pixel, fontSize: 20, color: c, letterSpacing: '0.08em'}}>{g.kicker}</div>}
				<div style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: g.size ?? 34, color: S2.parchment}}>{g.text}</div>
			</div>
		</AbsoluteFill>
	);
};

/** Floating pixel Zs over a sleeping predator. */
export const Zzz: React.FC<OP> = ({g, t}) => {
	const {o, a} = useWin(g, t, 0.3, 0.3);
	const s = useS2();
	if (o <= 0) return null;
	const p = pinTarget({...g, dy: 1.6}, s);
	if (!p) return null;
	const sc = project(s.cam, p);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{[0, 1, 2].map((k) => {
				const ph = ((t - a) * 0.7 + k / 3) % 1;
				return (
					<div key={k} style={{position: 'absolute', left: sc.x + 30 + ph * 70, top: sc.y - 40 - ph * 150, opacity: Math.sin(ph * Math.PI)}}>
						<PixelSprite name="z" px={6 + k * 3} color={S2.sky} />
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

/** Selection brackets + DEL key over predators being deleted. */
export const DeleteFx: React.FC<OP> = ({g, t}) => {
	const {o, a} = useWin(g, t, 0.12, 0.25);
	const s = useS2();
	if (o <= 0) return null;
	const ids: string[] = g.preds ?? [];
	const press = t >= a && t < a + 0.2;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{ids.map((id, k) => {
				const idx = s.world.predators.findIndex((p) => p.id === id);
				const keys = s.world.predators[idx];
				const pose = keys ? grimmawPose(s.island, keys, s.t, 0, idx) : null;
				const base = keys?.keys.find((kk) => kk.state === 'dissolve' && kk.t >= a - 0.5);
				const pos = pose ? [pose.x, pose.y + 1.4 * pose.scale, pose.z] : base ? [base.x, s.island.heightAt(base.x, base.z) + 1.4, base.z] : null;
				if (!pos) return null;
				const sc = project(s.cam, pos as [number, number, number]);
				const size = 120 * (keys?.scale ?? 1) * (g.size ?? 1);
				const flick = Math.floor((t + k * 0.13) * 14) % 2 ? 1 : 0.55;
				return (
					<div key={id} style={{position: 'absolute', left: sc.x - size, top: sc.y - size * 0.75, width: size * 2, height: size * 1.5, opacity: flick}}>
						{[
							{left: 0, top: 0, bl: 1, bt: 1},
							{right: 0, top: 0, br: 1, bt: 1},
							{left: 0, bottom: 0, bl: 1, bb: 1},
							{right: 0, bottom: 0, br: 1, bb: 1},
						].map((c, j) => (
							<div
								key={j}
								style={{
									position: 'absolute',
									width: 30,
									height: 30,
									...c,
									borderLeft: c.bl ? `${PX * 2}px solid ${S2.rust}` : undefined,
									borderRight: c.br ? `${PX * 2}px solid ${S2.rust}` : undefined,
									borderTop: c.bt ? `${PX * 2}px solid ${S2.rust}` : undefined,
									borderBottom: c.bb ? `${PX * 2}px solid ${S2.rust}` : undefined,
								}}
							/>
						))}
					</div>
				);
			})}
			<div style={{position: 'absolute', left: 0, right: 0, top: g.y ?? 600, display: 'flex', justifyContent: 'center'}}>
				<div style={{padding: '14px 30px 10px', fontFamily: F2.pixel, fontWeight: 700, fontSize: 64, color: press ? S2.ink : S2.rust, background: press ? S2.rust : 'rgba(5,9,18,0.8)', boxShadow: press ? 'none' : `0 ${PX * 3}px 0 ${S2.rust}, 0 0 0 ${PX * 2}px ${S2.rust}`, transform: `translateY(${press ? PX * 3 : 0}px)`}}>
					{g.label ?? 'DEL'}
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- full-frame effects

/** Rewind: scanlines, a sliding tear, a REWIND chip. */
export const Rewind: React.FC<OP> = ({g, t}) => {
	const {o, a} = useWin(g, t, 0.08, 0.2);
	if (o <= 0) return null;
	const tear = ((t - a) * 2.6) % 1;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(5,9,18,0.28) 0px, rgba(5,9,18,0.28) 3px, rgba(255,255,255,0.03) 3px, rgba(255,255,255,0.03) 9px)', mixBlendMode: 'multiply'}} />
			<div style={{position: 'absolute', left: 0, right: 0, top: `${tear * 100}%`, height: 36, background: 'rgba(143, 200, 255, 0.18)'}} />
			<div style={{position: 'absolute', left: 0, right: 0, top: g.y ?? 600, display: 'flex', justifyContent: 'center'}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 18, padding: '14px 28px 10px', fontFamily: F2.pixel, fontWeight: 700, fontSize: 60, color: S2.sky, ...panel({edge: S2.sky})}}>
					<PixelSprite name="rewind" px={9} color={S2.sky} />
					{g.label ?? 'REWIND'}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** The Season 2 transition: a diagonal sweep of pixel blocks (in, then out) around a cue. */
export const BlockWipe: React.FC<OP> = ({g, t}) => {
	const timing = useTiming();
	const at = cueTime(timing, g.at ?? g.start);
	const dur = g.dur ?? 0.36;
	const p = (t - (at - dur / 2)) / dur;
	if (p <= 0 || p >= 1) return null;
	const B = 90;
	const cols = 12;
	const rows = 22;
	const cells: React.ReactNode[] = [];
	for (let j = 0; j < rows; j++) {
		for (let i = 0; i < cols; i++) {
			const d = (i + j * 0.55) / (cols + rows * 0.55);
			const k = p < 0.5 ? clamp((p * 2 - d * 0.6) / 0.4) : 1 - clamp(((p - 0.5) * 2 - d * 0.6) / 0.4);
			if (k <= 0.01) continue;
			const sz = B * k;
			cells.push(<div key={`${i}-${j}`} style={{position: 'absolute', left: i * B + (B - sz) / 2, top: j * B + (B - sz) / 2, width: sz, height: sz, background: g.color ? col(g.color) : '#0a1430'}} />);
		}
	}
	return <AbsoluteFill style={{pointerEvents: 'none'}}>{cells}</AbsoluteFill>;
};

/** Series intro sting (≤1.5 s): the World Engine boots in the top-right while the hook is already playing. */
export const Sting: React.FC<OP> = ({g, t}) => {
	const dur = g.dur ?? 1.4;
	if (t > dur + 0.3) return null;
	const o = t < dur ? 1 : 1 - (t - dur) / 0.3;
	const label = g.label ?? 'WORLD ENGINE';
	const n = Math.floor(clamp(t / 0.55) * label.length);
	const run = g.run ?? 'RUN 26';
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', right: 160, top: 246, textAlign: 'right'}}>
				<div style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: 34, color: S2.ember, letterSpacing: '0.08em', textShadow: pixelShadow('#050912', 2)}}>
					{label.slice(0, n)}
					<span style={{opacity: Math.floor(t * 8) % 2 ? 1 : 0}}>█</span>
				</div>
				<div style={{fontFamily: F2.pixel, fontSize: 22, color: S2.parchment, letterSpacing: '0.14em', opacity: clamp((t - 0.55) / 0.2), textShadow: pixelShadow('#050912', 2)}}>{run}</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- end card

export const EndCardS2: React.FC<OP> = ({g, t}) => {
	const {o, a} = useWin(g, t, 0.4, g.fadeOut ?? 0.55);
	const brand = useBrand();
	if (o <= 0) return null;
	const k = (d: number) => ease(t, a + d, 0.4);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(7,14,30,0.9) 0%, rgba(9,18,40,0.78) 50%, rgba(5,9,18,0.55) 100%)'}} />
			<AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(255,255,255,0.025) 0px, rgba(255,255,255,0.025) 3px, transparent 3px, transparent 9px)'}} />
			{brand && (
				<div style={{position: 'absolute', left: 0, right: 0, top: 268, display: 'flex', justifyContent: 'center', opacity: k(0)}}>
					<Logo brand={brand} height={150} />
				</div>
			)}
			<div style={{position: 'absolute', left: 90, right: 160, top: 470, textAlign: 'center', opacity: k(0.1), fontFamily: F2.pixel, fontSize: 30, color: S2.amber, letterSpacing: '0.12em'}}>
				{g.kicker ?? 'EPISODE 26 / 50'}
			</div>
			<div style={{position: 'absolute', left: 90, right: 160, top: 528, textAlign: 'center', opacity: k(0.2), fontFamily: F2.serif, fontStyle: 'italic', fontWeight: 600, fontSize: 64, lineHeight: 1.08, color: S2.parchment}}>
				{g.title}
			</div>
			<div style={{position: 'absolute', left: 96, width: 804, top: 800, height: 330, opacity: k(0.35), transform: `translateY(${(1 - k(0.35)) * 24}px)`, ...panel({edge: S2.ember})}}>
				<div style={{position: 'absolute', left: 0, right: 0, top: 44, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22}}>
					<PixelSprite name={g.icon ?? 'share'} px={9} color={S2.ember} />
					<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: 78, color: S2.ember, textShadow: pixelShadow('#050912', 2)}}>{g.cta ?? 'SHARE THIS'}</span>
				</div>
				<div style={{position: 'absolute', left: 30, right: 30, top: 160, textAlign: 'center', fontFamily: F2.caption, fontWeight: 800, fontSize: 46, lineHeight: 1.15, color: S2.parchment}}>{g.with}</div>
			</div>
			<div style={{position: 'absolute', left: 90, right: 160, top: 1176, textAlign: 'center', whiteSpace: 'nowrap', opacity: k(0.5), fontFamily: F2.pixel, fontSize: 19, color: 'rgba(239,230,210,0.6)', letterSpacing: '0.06em'}}>
				{g.footer ?? 'WORLDCRAFT SHORTS · WORLDBUILDING, FROM THE GROUND UP'}
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the Season 2 ending (part number, follow, next run)

const GLYPHS = '#%@$&?*';

/** The episode number, spoken and shown: PART nn / 50 and a season bar of `of` segments that fills to the part on its cue. */
export const SeasonBar: React.FC<OP> = ({g, t}) => {
	const {o, a, timing} = useWin(g, t, 0.2, g.fadeOut ?? 0.3);
	if (o <= 0) return null;
	const part: number = g.part ?? 26;
	const of: number = g.of ?? 50;
	const fillAt = g.fillAt ? cueTime(timing, g.fillAt) : a;
	const ofAt = g.ofAt ? cueTime(timing, g.ofAt) : fillAt + 0.6;
	const lit = Math.round(clamp((t - fillAt) / (g.fillDur ?? 0.6)) * part);
	const full = lit >= part;
	const blink = full && Math.floor((t - fillAt) * 5) % 2 === 0;
	const seg = 12;
	const gap = 3;
	const barW = of * seg + (of - 1) * gap;
	const W = 804;
	const y = g.y ?? 372;
	const rise = (1 - ease(t, a, 0.25)) * 26;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 96, top: y + rise, width: W, height: 158, ...panel({edge: S2.ember})}}>
				<div style={{position: 'absolute', left: 30, top: 18, display: 'flex', alignItems: 'baseline', gap: 16, fontFamily: F2.pixel}}>
					<span style={{fontSize: 34, color: S2.amber, letterSpacing: '0.1em'}}>{g.label ?? 'PART'}</span>
					<span style={{fontWeight: 700, fontSize: 72, lineHeight: 1, color: full ? S2.ember : S2.parchment}}>{String(lit).padStart(2, '0')}</span>
					<span style={{fontSize: 34, color: 'rgba(239,230,210,0.75)', opacity: clamp((t - ofAt) / 0.15)}}>/ {of}</span>
				</div>
				<div style={{position: 'absolute', right: 30, top: 24, textAlign: 'right', fontFamily: F2.pixel, fontSize: 21, lineHeight: 1.3, color: S2.sky, letterSpacing: '0.08em'}}>
					{g.season ?? 'SEASON 2'}
					<br />
					{g.seasonName ?? 'THE WORLD ENGINE'}
				</div>
				<div style={{position: 'absolute', left: (W - barW) / 2, top: 112, width: barW, height: 24, display: 'flex', gap}}>
					{Array.from({length: of}, (_, i) => {
						const cur = i === part - 1 && full;
						const on = i < lit;
						return <div key={i} style={{width: seg, height: 24, flex: 'none', background: cur ? (blink ? S2.parchment : S2.ember) : on ? S2.ember : 'rgba(239,230,210,0.14)'}} />;
					})}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/**
 * The follow ask as a pixel button ("+ FOLLOW / FOR PART 27"). A pointer glides in and taps it on its cue: the
 * button presses, flashes, throws sparks and flips to FOLLOWING, the platform's own follow animation in pixels.
 */
export const FollowButton: React.FC<OP> = ({g, t}) => {
	const {o, a, timing} = useWin(g, t, 0.2, g.fadeOut ?? 0.3);
	if (o <= 0) return null;
	const at = cueTime(timing, g.pressAt);
	const dp = t - at;
	const down = dp >= -0.04 && dp < 0.16;
	const done = dp >= 0.08;
	const flash = dp >= 0 ? Math.max(0, 1 - dp / 0.3) : 0;
	const inK = ease(t, a, 0.28);
	const bounce = done ? Math.sin(clamp((dp - 0.08) / 0.32) * Math.PI) * 0.07 : 0;
	const scale = (0.72 + 0.28 * inK) * (1 + bounce);
	const y: number = g.y ?? 588;
	const cx0 = 498;
	const cy0 = y + 82;
	// the pointer: glides in over 0.45 s, taps, then drifts away
	const cin = ease(t, at - 0.55, 0.45);
	const cout = clamp((dp - 0.45) / 0.3);
	const handX = 650 + (1 - cin) * 240 + cout * 120;
	const handY = cy0 + 8 + (1 - cin) * 300 + (down ? 10 : 0) + cout * 90;
	const sparks =
		dp >= 0 && dp < 0.6
			? Array.from({length: 14}, (_, i) => {
					const q = dp / 0.6;
					const ang = (i / 14) * Math.PI * 2 + 0.25;
					const r = 150 + 300 * (1 - (1 - q) ** 2);
					const sz = Math.round((15 * (1 - q) + 3) / 3) * 3;
					return (
						<div key={i} style={{position: 'absolute', left: cx0 + Math.cos(ang) * r * 1.25 - sz / 2, top: cy0 + Math.sin(ang) * r * 0.5 - sz / 2, width: sz, height: sz, background: i % 2 ? S2.ember : S2.parchment}} />
					);
				})
			: null;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 96, width: 804, top: y, display: 'flex', justifyContent: 'center'}}>
				<div
					style={{
						position: 'relative',
						width: 640,
						height: 164,
						boxSizing: 'border-box',
						transform: `translateY(${down ? 10 : 0}px) scale(${scale})`,
						transformOrigin: '50% 50%',
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						gap: 30,
						background: done ? 'rgba(10,20,48,0.94)' : S2.ember,
						color: done ? S2.ember : S2.ink,
						boxShadow: `0 0 0 6px ${done ? S2.ember : S2.ink}, 0 ${down ? 4 : 14}px 0 6px ${done ? 'rgba(3,6,14,0.8)' : '#7d5218'}`,
					}}
				>
					<PixelSprite name={done ? 'check' : 'plus'} px={done ? 10 : 12} />
					<div style={{display: 'flex', flexDirection: 'column', lineHeight: 1, gap: 10}}>
						<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: done ? 62 : 80, letterSpacing: '0.02em'}}>{done ? (g.doneText ?? 'FOLLOWING') : (g.text ?? 'FOLLOW')}</span>
						<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: 34, letterSpacing: '0.1em', color: done ? S2.parchment : S2.ink}}>{g.sub ?? 'FOR PART 27'}</span>
					</div>
					{flash > 0 && <div style={{position: 'absolute', left: -6, top: -6, right: -6, bottom: -6, background: `rgba(255,248,232,${(flash * 0.85).toFixed(3)})`}} />}
				</div>
			</div>
			{sparks}
			{cin > 0.01 && cout < 1 && (
				<div style={{position: 'absolute', left: handX, top: handY, opacity: 1 - cout, transform: `scale(${down ? 0.88 : 1})`, transformOrigin: '30% 0%'}}>
					<PixelSprite name="hand" px={9} />
				</div>
			)}
		</AbsoluteFill>
	);
};

/** The next episode as a locked run that decodes on its cue: NEXT RUN · 27 / ??? → DRAGONS, silhouette → sprite. */
export const NextRun: React.FC<OP> = ({g, t}) => {
	const {o, a, timing} = useWin(g, t, 0.2, g.fadeOut ?? 0.3);
	if (o <= 0) return null;
	const at = cueTime(timing, g.revealAt);
	const k = clamp((t - at) / 0.42);
	const title: string = g.title ?? 'DRAGONS';
	const fr = Math.floor(t * 30);
	const n = Math.floor(k * title.length + 1e-6);
	const shown = t < at ? '???' : title.split('').map((c, i) => (i < n ? c : GLYPHS[(fr + i * 3) % GLYPHS.length])).join('');
	const flash = t >= at ? Math.max(0, 1 - (t - at) / 0.35) : 0;
	const sub = clamp((t - at - 0.35) / 0.2);
	const y: number = g.y ?? 772;
	const rise = (1 - ease(t, a, 0.25)) * 30;
	const locked = t < at;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 96, top: y + rise, width: 804, height: 186, ...panel({edge: locked ? 'rgba(239,230,210,0.9)' : S2.rust})}}>
				<div style={{position: 'absolute', left: 20, top: 18, width: 150, height: 150, background: locked ? 'rgba(239,230,210,0.08)' : 'rgba(208,96,63,0.18)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
					<PixelSprite name={g.sprite ?? 'dragon'} px={g.spritePx ?? 7} mono={locked ? '#46507a' : undefined} />
					{locked && <div style={{position: 'absolute', fontFamily: F2.pixel, fontWeight: 700, fontSize: 60, color: S2.parchment, opacity: Math.floor(t * 3) % 2 ? 1 : 0.55, textShadow: pixelShadow('#050912', 2)}}>?</div>}
					{flash > 0 && <div style={{position: 'absolute', left: 0, top: 0, right: 0, bottom: 0, background: `rgba(255,248,232,${(flash * 0.9).toFixed(3)})`}} />}
				</div>
				<div style={{position: 'absolute', left: 196, top: 22, fontFamily: F2.pixel, fontSize: 26, color: S2.sky, letterSpacing: '0.1em'}}>{g.kicker ?? 'NEXT RUN · 27'}</div>
				<div style={{position: 'absolute', left: 192, top: 58, fontFamily: F2.pixel, fontWeight: 700, fontSize: 80, lineHeight: 1, color: locked ? 'rgba(239,230,210,0.55)' : S2.rust, textShadow: pixelShadow('#050912', 2)}}>{shown}</div>
				<div style={{position: 'absolute', left: 196, top: 144, fontFamily: F2.pixel, fontSize: 22, color: S2.parchment, letterSpacing: '0.06em', opacity: sub}}>{g.sub ?? 'A DRAGON LANDS HERE.'}</div>
			</div>
		</AbsoluteFill>
	);
};

/** A light mid-video follow nudge in the top-right (where the sting booted): "+ FOLLOW · PART 26/50". */
export const FollowChip: React.FC<OP> = ({g, t}) => {
	const {o, a} = useWin(g, t, 0.2, g.fadeOut ?? 0.3);
	if (o <= 0) return null;
	const k = ease(t, a, 0.3);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', right: 166, top: 246, transform: `translateX(${Math.round((1 - k) * 60)}px)`, display: 'flex', alignItems: 'center', gap: 12, padding: '10px 16px 8px', ...panel({edge: S2.ember})}}>
				<PixelSprite name="plus" px={5} color={S2.ember} />
				<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: 30, color: S2.ember}}>{g.text ?? 'FOLLOW'}</span>
				<span style={{fontFamily: F2.pixel, fontSize: 22, color: S2.parchment, letterSpacing: '0.06em'}}>{g.sub ?? 'PART 26/50'}</span>
			</div>
		</AbsoluteFill>
	);
};


// ---------------------------------------------------------------- EP27: the dragon's-eye view

const EYE = {dragon: '#ff5a4e', tower: '#8fc8ff'};

/** Screen size (px) of a world radius r at p: projects p and a point r units above it. */
const screenSize = (cam: ReturnType<typeof useS2>['cam'], p: [number, number, number], r: number) => {
	const a = project(cam, p);
	const b = project(cam, [p[0], p[1] + r, p[2]]);
	return {a, px: Math.abs(a.y - b.y)};
};

const Bracket: React.FC<{x: number; y: number; size: number; color: string; k: number; label?: string; blink?: boolean; t: number}> = ({x, y, size, color, k, label, blink, t}) => {
	const sz = Math.round((size * (1 + (1 - k) * 1.2)) / PX) * PX;
	const arm = Math.max(PX * 3, Math.round(sz / 3 / PX) * PX);
	const on = blink ? Math.floor(t * 12) % 2 === 0 : true;
	const corners = [
		{left: 0, top: 0, bl: 1, bt: 1},
		{right: 0, top: 0, br: 1, bt: 1},
		{left: 0, bottom: 0, bl: 1, bb: 1},
		{right: 0, bottom: 0, br: 1, bb: 1},
	];
	return (
		<div style={{position: 'absolute', left: x - sz / 2, top: y - sz / 2, width: sz, height: sz, opacity: (0.35 + 0.65 * k) * (on ? 1 : 0.4)}}>
			{corners.map((c, j) => (
				<div
					key={j}
					style={{
						position: 'absolute',
						width: arm,
						height: arm,
						...c,
						borderLeft: c.bl ? `${PX}px solid ${color}` : undefined,
						borderRight: c.br ? `${PX}px solid ${color}` : undefined,
						borderTop: c.bt ? `${PX}px solid ${color}` : undefined,
						borderBottom: c.bb ? `${PX}px solid ${color}` : undefined,
						filter: 'drop-shadow(0 0 0 #050912)',
					}}
				/>
			))}
			{label && k > 0.6 && (
				<div style={{position: 'absolute', left: '50%', bottom: sz + 6, transform: 'translateX(-50%)', whiteSpace: 'nowrap', fontFamily: F2.pixel, fontWeight: 700, fontSize: 20, color, letterSpacing: '0.08em', textShadow: pixelShadow('#050912', 1)}}>
					{label}
				</div>
			)}
		</div>
	);
};

const TARGET_LABEL: Record<Target['kind'], string> = {roof: 'ROOF', flock: 'FLOCK', village: 'VILLAGE', cart: 'CART'};

/**
 * The dragon's-eye view (EP27): the world as a flying predator scans it. `mode: "dragon"` tints the frame and locks
 * red brackets onto every target it can see (read from the world: thatch roofs, flocks in open pens, the open village,
 * carts on the open road by day), staggered from `lockAt`; a TARGETS readout counts them. `mode: "light"` keeps only
 * the brackets and the readout (a target that disappears flashes green, HIDDEN). `mode: "tower"` is the village
 * looking back: a sky-blue tint and one bracket on the dragon, DRAGON · SPOTTED.
 */
export const DragonEye: React.FC<OP> = ({g, t}) => {
	const {o, a, timing} = useWin(g, t, g.fadeIn ?? 0.2, g.fadeOut ?? 0.25);
	const S = useS2();
	if (o <= 0) return null;
	const mode: 'dragon' | 'light' | 'tower' = g.mode ?? 'dragon';
	const color = mode === 'tower' ? EYE.tower : EYE.dragon;
	const lockAt = g.lockAt ? cueTime(timing, g.lockAt) : a;
	const stagger: number = g.stagger ?? 0.06;
	const s = simTime(S.world, t);
	const nodes: React.ReactNode[] = [];
	let count = 0;
	if (mode === 'tower') {
		const d = S.world.dragons.find((dd) => dd.id === (g.dragon ?? 'dragon'));
		const dp = d ? dragonAt(d.keys, t, (x, z) => Math.max(S.island.waterLevel, S.island.heightAt(x, z))) : null;
		if (dp && d) {
			const {a: sc, px} = screenSize(S.cam, [dp.x, dp.y + 1.6 * d.scale, dp.z], 3.2 * d.scale);
			if (!sc.behind) {
				const k = clamp((t - lockAt) / 0.22);
				if (k > 0) nodes.push(<Bracket key="d" x={sc.x} y={sc.y} size={Math.max(72, px * 2)} color={color} k={k} label={g.label ?? 'DRAGON · SPOTTED'} blink={t - lockAt < 0.4} t={t} />);
			}
		}
	} else {
		const now = dragonTargets(S.world, S.island, t, s);
		const before = [0.15, 0.3, 0.45, 0.6].map((dt) => dragonTargets(S.world, S.island, t - dt, simTime(S.world, t - dt)));
		const shownLabels = new Set<string>();
		now.forEach((tg, i) => {
			const lt = lockAt + i * stagger;
			const {a: sc, px} = screenSize(S.cam, tg.p, tg.r);
			if (tg.on) {
				if (t < lt) return;
				count++;
				if (sc.behind || sc.x < -60 || sc.x > 1140 || sc.y < (g.minY ?? 200) || sc.y > 1900) return;
				const k = clamp((t - lt) / 0.2);
				const label = !shownLabels.has(tg.kind) && tg.kind !== 'cart' ? TARGET_LABEL[tg.kind] : undefined;
				if (label) shownLabels.add(tg.kind);
				nodes.push(<Bracket key={i} x={sc.x} y={sc.y} size={Math.max(30, px * 2)} color={color} k={k} label={label} blink={t - lt < 0.35} t={t} />);
			} else if (!sc.behind && t >= lt && sc.y >= (g.minY ?? 200)) {
				// recently hidden: a green bracket that fades over 0.6 s
				const j = before.findIndex((b) => b[i]?.on);
				if (j >= 0) {
					const age = (j + 1) * 0.15;
					nodes.push(<Bracket key={`h${i}`} x={sc.x} y={sc.y} size={Math.max(30, px * 2)} color={S2.prey} k={1 - age / 0.75} label={tg.kind === 'village' || tg.kind === 'flock' ? 'HIDDEN' : undefined} t={t} />);
				}
			}
		});
	}
	const tint = mode === 'light' ? null : (
		<>
			<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 55%, transparent 38%, ${mode === 'tower' ? 'rgba(20,70,140,0.42)' : 'rgba(150,18,12,0.5)'} 100%)`}} />
			<AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(5,9,18,0.16) 0px, rgba(5,9,18,0.16) 3px, transparent 3px, transparent 9px)'}} />
		</>
	);
	const chip = mode === 'light' ? null : (
		<div style={{position: 'absolute', right: 166, top: 246, display: 'flex', alignItems: 'center', gap: 12, padding: '10px 16px 8px', ...panel({edge: color})}}>
			<PixelSprite name="eye" px={5} color={color} />
			<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: 26, color, letterSpacing: '0.06em'}}>{g.title ?? (mode === 'tower' ? "WATCHTOWER VIEW" : "DRAGON'S-EYE VIEW")}</span>
		</div>
	);
	const zero = count === 0;
	const readout =
		mode === 'tower' || g.readout === false || t < lockAt ? null : (
			<div style={{position: 'absolute', left: 96, top: g.readoutY ?? 1420, display: 'flex', alignItems: 'baseline', gap: 16, padding: '12px 20px 8px', ...panel({edge: zero ? S2.prey : color})}}>
				<span style={{fontFamily: F2.pixel, fontSize: 24, color: 'rgba(239,230,210,0.8)', letterSpacing: '0.1em'}}>TARGETS</span>
				<span style={{fontFamily: F2.pixel, fontWeight: 700, fontSize: 60, lineHeight: 1, color: zero ? S2.prey : color}}>{String(count).padStart(2, '0')}</span>
				{zero && g.zeroText && <span style={{fontFamily: F2.pixel, fontSize: 22, color: S2.prey, letterSpacing: '0.06em'}}>{g.zeroText}</span>}
			</div>
		);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{tint}
			{nodes}
			{chip}
			{readout}
		</AbsoluteFill>
	);
};

export const S2_OVERLAYS: Record<string, React.FC<OP>> = {
	dragonEye: DragonEye,
	kinetic: Kinetic,
	simBar: SimBar,
	simGraph: SimGraph,
	stamp: Stamp,
	fieldCard: FieldCard,
	pin: Pin,
	zzz: Zzz,
	deleteFx: DeleteFx,
	rewind: Rewind,
	blockWipe: BlockWipe,
	sting: Sting,
	endCardS2: EndCardS2,
	seasonBar: SeasonBar,
	followButton: FollowButton,
	nextRun: NextRun,
	followChip: FollowChip,
};
