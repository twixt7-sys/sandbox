import React from 'react';
import {Composition, staticFile} from 'remotion';
import {EpisodeComposition} from './Episode';
import type {EpisodeProps} from './types';

const getJson = async (path: string, optional = false) => {
	const res = await fetch(staticFile(path));
	if (!res.ok) {
		if (optional) return undefined;
		throw new Error(`Missing ${path} — run pipeline/build.sh <episode> first`);
	}
	return res.json();
};

export const Root: React.FC = () => (
	<Composition
		id="Episode"
		component={EpisodeComposition}
		width={1080}
		height={1920}
		fps={30}
		durationInFrames={900}
		defaultProps={{episodeId: 'ep01'} as EpisodeProps}
		calculateMetadata={async ({props}) => {
			const id = props.episodeId;
			const [episode, series, timing, plates] = await Promise.all([
				getJson(`${id}/episode.json`),
				getJson(`series.json`),
				getJson(`${id}/timing.json`),
				getJson(`${id}/plates.json`, true),
			]);
			return {
				durationInFrames: Math.ceil(timing.duration * series.format.fps),
				fps: series.format.fps,
				width: series.format.width,
				height: series.format.height,
				props: {...props, episode, series, timing, plates: plates ?? {}},
			};
		}}
	/>
);
