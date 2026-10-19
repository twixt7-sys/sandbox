import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import {FogBank} from '../fx/Fx';
import {lerp} from '../lib/timing';
import type {Shot} from '../types';
import {Bridge} from './Bridge';
import {EndCard} from './EndCard';
import {LanternRiver} from './Lanterns';
import {MapScene} from './MapScene';
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
};

/**
 * AI-generated still (or a frame-accurate clip) used as the background plate.
 * Camera motion is a restrained push/drift so generated detail never has to move.
 */
export const PlateScene: React.FC<SceneProps & {src: string; motion?: 'push' | 'pull' | 'driftL' | 'driftR'}> = ({progress, src, motion = 'push'}) => {
	const p = progress;
	const m = {
		push: {s: lerp(1.0, 1.08, p), x: 0, y: lerp(0, -20, p)},
		pull: {s: lerp(1.1, 1.0, p), x: 0, y: lerp(-20, 0, p)},
		driftL: {s: 1.06, x: lerp(30, -30, p), y: 0},
		driftR: {s: 1.06, x: lerp(-30, 30, p), y: 0},
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
			</AbsoluteFill>
			<FogBank y={1500} opacity={0.12} seed={40} drift={0.5} />
		</AbsoluteFill>
	);
};
