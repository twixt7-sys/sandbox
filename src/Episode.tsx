import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {BrandContext, LogoBug} from './brand/Logo';
import {Captions} from './captions/Captions';
import {Grade, Grain, Vignette} from './fx/Fx';
import {GRAPHICS} from './graphics/Graphics';
import {TimingContext} from './lib/timing';
import {AtlasContext} from './scenes/Atlas';
import {PlateScene, SCENES} from './scenes/registry';
import {Valley} from './scenes/Valley';
import type {EpisodeProps, Graphic, Plates, Shot, TimedShot} from './types';

const MAP_LOCAL = new Set(['mapBase', 'ferryRoute', 'power', 'accents']);

const renderGraphics = (list: Graphic[], t: number, shot: Shot, span: TimedShot) =>
	list.map((g, i) => {
		const G = GRAPHICS[g.type];
		if (!G) throw new Error(`Unknown graphic type ${g.type}`);
		return <G key={i} g={g} t={t} shot={shot} span={span} />;
	});

const ShotLayer: React.FC<{shot: Shot; span: TimedShot; from: number; dur: number; plate?: string; episodeId: string}> = ({shot, span, from, dur, plate, episodeId}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = (from + frame) / fps;
	const progress = Math.min(1, frame / Math.max(1, dur - 1));
	const tr = shot.transitionIn;
	const trFrames = tr && tr.type !== 'cut' ? Math.round((tr.duration ?? 0.5) * fps) : 0;
	const opacity = trFrames ? interpolate(frame, [0, trFrames], [0, 1], {extrapolateRight: 'clamp'}) : 1;
	const Scene = SCENES[shot.scene];
	if (!Scene && !plate) throw new Error(`No scene "${shot.scene}" and no plate for shot ${shot.id}`);
	const graphics = shot.graphics.filter((g) => !MAP_LOCAL.has(g.type));
	// `local` graphics are pinned to the plate and share its camera move.
	const local = plate ? graphics.filter((g) => g.local) : [];
	const overlay = plate ? graphics.filter((g) => !g.local) : graphics;
	return (
		<AbsoluteFill style={{opacity}}>
			{plate ? (
				<PlateScene progress={progress} t={t} shot={shot} src={`${episodeId}/${plate}`}>
					{renderGraphics(local, t, shot, span)}
				</PlateScene>
			) : (
				<Scene progress={progress} t={t} shot={shot} />
			)}
			{renderGraphics(overlay, t, shot, span)}
		</AbsoluteFill>
	);
};

/** Fog / flash overlays that sit on top of the incoming shot at a transition point. */
const TransitionFx: React.FC<{type: string; at: number; dur: number}> = ({type, at, dur}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	if (type === 'fog') {
		const o = interpolate(t, [at - dur, at - dur * 0.2, at + dur * 0.6], [0, 0.75, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
		return <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 55%, #dfe6e6 0%, #9fb1b8 70%)', opacity: o}} />;
	}
	if (type === 'flash') {
		const o = interpolate(t, [at - dur, at - 0.05, at + 0.25], [0, 0.6, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
		return <AbsoluteFill style={{background: '#e8eef0', opacity: o}} />;
	}
	return null;
};

/** Last 0.6 s cross-fades into the hook's first frame (incl. its plate-pinned graphics) so the Short loops seamlessly. */
const LoopTail: React.FC<{duration: number; hook: Shot; span: TimedShot; plate?: string; episodeId: string}> = ({duration, hook, span, plate, episodeId}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const o = interpolate(frame / fps, [duration - 0.65, duration - 0.05], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	if (o <= 0) return null;
	return (
		<AbsoluteFill style={{opacity: o}}>
			{plate ? (
				<PlateScene progress={0} t={0} shot={hook} src={`${episodeId}/${plate}`}>
					{renderGraphics(hook.graphics.filter((g) => g.local), 0, hook, span)}
				</PlateScene>
			) : (
				<Valley progress={0} t={0} shot={hook} />
			)}
		</AbsoluteFill>
	);
};

/** A shot can reuse another shot's plate (`"plateFrom": "hook"`), e.g. the same landscape by night. */
const plateFor = (plates: Plates, shot: Shot) => plates[shot.id] ?? (shot.plateFrom ? plates[shot.plateFrom] : undefined);

export const EpisodeComposition: React.FC<EpisodeProps> = ({episodeId, episode, series, timing, plates = {}}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	if (!episode || !series || !timing) return null;
	const t = frame / fps;
	return (
		<TimingContext.Provider value={timing}>
			<BrandContext.Provider value={series.brand}>
			<AtlasContext.Provider value={episode.atlas}>
			<AbsoluteFill style={{backgroundColor: '#05080a'}}>
				{episode.shots.map((shot) => {
					const span = timing.shots.find((s) => s.id === shot.id)!;
					const tr = shot.transitionIn;
					const lead = tr && tr.type !== 'cut' ? tr.duration ?? 0.5 : 0;
					const from = Math.max(0, Math.round((span.start - lead) * fps));
					const to = Math.round(span.end * fps);
					return (
						<Sequence key={shot.id} from={from} durationInFrames={to - from} name={shot.id}>
							<ShotLayer shot={shot} span={span} from={from} dur={to - from} plate={plateFor(plates, shot)} episodeId={episodeId} />
						</Sequence>
					);
				})}
				{episode.shots.map((shot) => {
					const span = timing.shots.find((s) => s.id === shot.id)!;
					const tr = shot.transitionIn;
					return tr && (tr.type === 'fog' || tr.type === 'flash') ? <TransitionFx key={shot.id} type={tr.type} at={span.start} dur={tr.duration ?? 0.5} /> : null;
				})}
				<Grade />
				<Vignette />
				<Captions timing={timing} episode={episode} t={t} centerY={series.safeArea.captionCenterY} />
				{series.brand && (
					<LogoBug
						brand={series.brand}
						t={t}
						hidden={episode.shots
							.filter((s) => s.hideLogoBug)
							.map((s) => {
								const span = timing.shots.find((x) => x.id === s.id)!;
								return [span.start, span.end + 1] as [number, number];
							})}
					/>
				)}
				<LoopTail duration={timing.duration} hook={episode.shots[0]} span={timing.shots[0]} plate={plates[episode.shots[0].id]} episodeId={episodeId} />
				<Grain />
				<Audio src={staticFile(`${episodeId}/mix.wav`)} />
			</AbsoluteFill>
			</AtlasContext.Provider>
			</BrandContext.Provider>
		</TimingContext.Provider>
	);
};
