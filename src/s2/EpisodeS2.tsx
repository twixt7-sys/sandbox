// Season 2 episode composition ("the World Engine"). One continuous 3D diorama renders under the whole episode;
// shots only group narration lines and carry overlays. EP01–EP25 keep using src/Episode.tsx unchanged: this
// component is selected only when episode.json has "season": 2.
import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {BrandContext, LogoBug} from '../brand/Logo';
import {Vignette} from '../fx/Fx';
import {cueTime, TimingContext} from '../lib/timing';
import type {EpisodeProps, Graphic, Shot} from '../types';
import {CaptionsS2} from './CaptionsS2';
import {S2_OVERLAYS} from './overlays/Overlays';
import {resolveWorld, WorldRaw} from './world/timeline';
import {S2Context, useWorldState, WorldScene} from './world/WorldScene';

const withDefaults = (g: Graphic, shot: Shot, next?: Shot): Graphic => ({
	...g,
	start: g.start ?? {shot: shot.id},
	end: g.end ?? (next ? {shot: next.id} : undefined),
});

export const EpisodeS2: React.FC<EpisodeProps> = (props) => {
	const {episode, series, timing} = props;
	if (!episode || !series || !timing || !(episode as any).world) return null;
	return <EpisodeS2Inner {...props} />;
};

const EpisodeS2Inner: React.FC<EpisodeProps> = ({episodeId, episode: ep, series: se, timing: ti}) => {
	const episode = ep!;
	const series = se!;
	const timing = ti!;
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const raw = (episode as any).world as WorldRaw;
	const world = useMemo(() => resolveWorld(raw, timing), [raw, timing]);
	const centers = useMemo(() => (raw.herd?.centers ?? [[8, -2]]) as [number, number][], [raw]);
	const state = useWorldState(world, t, centers, raw.herd?.base ?? 120);
	const overlays = episode.shots.flatMap((shot, i) => shot.graphics.map((g, k) => ({g: withDefaults(g, shot, episode.shots[i + 1]), key: `${shot.id}-${k}`})));
	const hidden = episode.shots
		.filter((s) => s.hideLogoBug)
		.map((s) => {
			const span = timing.shots.find((x) => x.id === s.id)!;
			const until = (s as any).hideLogoBugUntil;
			const end = until ? cueTime(timing, until) : span.end + 1;
			return [span.start, end] as [number, number];
		});
	const layer = (front: boolean) =>
		overlays
			.filter(({g}) => Boolean(g.front) === front)
			.map(({g, key}) => {
				const O = S2_OVERLAYS[g.type];
				if (!O) throw new Error(`Unknown S2 overlay type ${g.type}`);
				return <O key={key} g={g} t={t} />;
			});
	return (
		<TimingContext.Provider value={timing}>
			<BrandContext.Provider value={series.brand}>
				<S2Context.Provider value={state}>
					<AbsoluteFill style={{backgroundColor: '#05080a'}}>
						<WorldScene state={state} />
						<Vignette strength={0.42} />
						{layer(false)}
						<CaptionsS2 timing={timing} episode={episode} t={t} centerY={(episode as any).captionY ?? 1238} />
						{series.brand && <LogoBug brand={series.brand} t={t} hidden={hidden} />}
						{layer(true)}
						<Audio src={staticFile(`${episodeId}/mix.wav`)} />
					</AbsoluteFill>
				</S2Context.Provider>
			</BrandContext.Provider>
		</TimingContext.Provider>
	);
};
