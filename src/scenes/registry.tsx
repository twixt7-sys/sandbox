import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import {FogBank} from '../fx/Fx';
import {lerp} from '../lib/timing';
import type {Shot} from '../types';
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
	lanterns: LanternRiver,
	endcard: EndCard,
	nightSky: NightSky,
};

/**
 * AI-generated still (or a frame-accurate clip) used as the background plate.
 * Camera motion is a restrained push/drift so generated detail never has to move.
 */
export const PlateScene: React.FC<SceneProps & {src: string; children?: React.ReactNode}> = ({progress, src, shot, children}) => {
	const p = progress;
	const motion: 'push' | 'pull' | 'driftL' | 'driftR' | 'descend' | 'still' = shot.plateMotion ?? 'push';
	// Generated skies are often bright: darken the top so parchment type stays legible.
	const scrim = shot.plateScrim ?? 0.5;
	const m = {
		push: {s: lerp(1.0, 1.08, p), x: 0, y: lerp(0, -20, p)},
		pull: {s: lerp(1.1, 1.0, p), x: 0, y: lerp(-20, 0, p)},
		driftL: {s: 1.06, x: lerp(30, -30, p), y: 0},
		driftR: {s: 1.06, x: lerp(-30, 30, p), y: 0},
		// Camera sinks into the scene: the picture rises past a slightly enlarged frame.
		descend: {s: lerp(1.2, 1.16, p), x: 0, y: lerp(150, -150, p)},
		still: {s: 1.0, x: 0, y: 0},
	}[motion];
	return (
		<AbsoluteFill style={{backgroundColor: '#0b1216'}}>
			<AbsoluteFill style={{transform: `translate(${m.x}px, ${m.y}px) scale(${m.s})`}}>
				{/\.mp4$/i.test(src) ? (
					// plates.py requests clips at least as long as the shot (from timing.json), so no freeze/hold is needed.
					<OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				) : (
					<Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				)}
				{/* Plate-pinned graphics (sun in the sky, glow on a carving) move with the camera. */}
				{children}
			</AbsoluteFill>
			<FogBank y={1500} opacity={0.12} seed={40} drift={0.5} />
			<AbsoluteFill style={{background: `linear-gradient(180deg, rgba(8,13,16,${scrim}) 0%, rgba(8,13,16,${scrim * 0.75}) 30%, rgba(8,13,16,0) 52%)`}} />
		</AbsoluteFill>
	);
};
