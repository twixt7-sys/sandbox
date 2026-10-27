import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import {FogBank} from '../fx/Fx';
import {cueTime, ease, lerp, useTiming} from '../lib/timing';
import {palette} from '../theme';
import type {Shot} from '../types';
import {AtlasScene} from './Atlas';
import {Bridge} from './Bridge';
import {EndCard} from './EndCard';
import {LanternRiver} from './Lanterns';
import {MapScene} from './MapScene';
import {NightSky} from './NightSky';
import {Valley, ValleyLow} from './Valley';

export type SceneProps = {
	/** 0..1 across the shot's sequence (including its transition-in). */
	progress: number;
	/** Absolute episode time in seconds (for cue-synced beats). */
	t: number;
	shot: Shot;
};

/** Procedural scenes: zero-cost fallback visuals in the series style. */
export const SCENES: Record<string, React.FC<SceneProps>> = {
	valley: Valley,
	valleyLow: ValleyLow,
	bridge: Bridge,
	map: MapScene,
	atlas: AtlasScene,
	lanterns: LanternRiver,
	endcard: EndCard,
	nightSky: NightSky,
};

/** Named plate grades for `plateLook` (EP11): how an outsider vs an insider sees the same scene. Any CSS filter string also works. */
const LOOKS: Record<string, string> = {
	cold: 'saturate(0.22) brightness(0.78) contrast(1.08) hue-rotate(-8deg)',
	warm: 'saturate(1.12) brightness(1.04) sepia(0.12)',
	none: 'none',
};
const look = (k?: string) => (k ? LOOKS[k] ?? k : 'none');

/**
 * AI-generated still (or a frame-accurate clip) used as the background plate.
 * Camera motion is a restrained push/drift so generated detail never has to move.
 */
export const PlateScene: React.FC<SceneProps & {src: string; children?: React.ReactNode}> = ({progress, t, src, shot, children}) => {
	const timing = useTiming();
	const p = progress;
	const motion: 'push' | 'pull' | 'driftL' | 'driftR' | 'descend' | 'still' = shot.plateMotion ?? 'push';
	// Generated skies are often bright: darken the top so parchment type stays legible.
	const scrim = shot.plateScrim ?? 0.5;
	let m = {
		push: {s: lerp(1.0, 1.08, p), x: 0, y: lerp(0, -20, p)},
		pull: {s: lerp(1.1, 1.0, p), x: 0, y: lerp(-20, 0, p)},
		driftL: {s: 1.06, x: lerp(30, -30, p), y: 0},
		driftR: {s: 1.06, x: lerp(-30, 30, p), y: 0},
		// Camera sinks into the scene: the picture rises past a slightly enlarged frame.
		descend: {s: lerp(1.2, 1.16, p), x: 0, y: lerp(150, -150, p)},
		still: {s: 1.0, x: 0, y: 0},
	}[motion];
	// `plateFrame` overrides the preset: {from: {s, x, y}, to: {s, x, y}} (e.g. keep faces clear of the caption band).
	const f = shot.plateFrame;
	if (f) {
		m.s = lerp(f.from.s ?? 1, f.to.s ?? 1, p);
		m.x = lerp(f.from.x ?? 0, f.to.x ?? 0, p);
		m.y = lerp(f.from.y ?? 0, f.to.y ?? 0, p);
	}
	return (
		<AbsoluteFill style={{backgroundColor: '#0b1216'}}>
			<AbsoluteFill style={{transform: `translate(${m.x}px, ${m.y}px) scale(${m.s})`}}>
				{/\.mp4$/i.test(src) ? (
					// plates.py requests clips at least as long as the shot (from timing.json), so no freeze/hold is needed.
					<OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				) : (
					<Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: look(shot.plateLook?.from)}} />
				)}
				{/* `plateLook: {from, to?, at?, dur?}`: grade the plate (`from`), then wipe a second grade (`to`) across it left to right on a cue (a "look again" re-read of the same scene). */}
				{shot.plateLook?.to && (() => {
					const w = ease(t, cueTime(timing, shot.plateLook.at, 0), shot.plateLook.dur ?? 1.1);
					if (w <= 0) return null;
					return (
						<>
							<Img src={staticFile(src)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', filter: look(shot.plateLook.to), clipPath: `inset(0 ${(1 - w) * 100}% 0 0)`}} />
							{w < 1 && <div style={{position: 'absolute', top: 0, bottom: 0, left: `${w * 100}%`, width: 3, marginLeft: -1.5, background: palette.amber, boxShadow: `0 0 24px 6px rgba(233,169,75,0.55)`, opacity: Math.min(1, (1 - w) * 6)}} />}
						</>
					);
				})()}
				{/* Plate-pinned graphics (sun in the sky, glow on a carving) move with the camera. */}
				{children}
			</AbsoluteFill>
			<FogBank y={1500} opacity={0.12} seed={40} drift={0.5} />
			<AbsoluteFill style={{background: `linear-gradient(180deg, rgba(8,13,16,${scrim}) 0%, rgba(8,13,16,${scrim * 0.75}) 30%, rgba(8,13,16,0) 52%)`}} />
		</AbsoluteFill>
	);
};
