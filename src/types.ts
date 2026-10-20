export type Cue = {line?: string; word?: string; shot?: string; offset?: number};

export type Word = {text: string; start: number; end: number};
export type TimedLine = {id: string; shot: string; text: string; start: number; end: number; words: Word[]; emphasis: string[]};
export type TimedShot = {id: string; start: number; end: number};
export type Timing = {episode: string; provider: string; duration: number; lines: TimedLine[]; shots: TimedShot[]};

export type Graphic = {type: string; start?: Cue; end?: Cue; [key: string]: any};

export type Transition = {type: 'cut' | 'dissolve' | 'fog' | 'flash'; duration?: number};

export type Shot = {
	id: string;
	scene: string;
	transitionIn?: Transition;
	captions?: boolean;
	/** Hide the corner logo for this shot (e.g. when the end card shows the full logo). */
	hideLogoBug?: boolean;
	graphics: Graphic[];
	[key: string]: any;
};

export type Episode = {
	id: string;
	number: number;
	title: string;
	captionReplace?: Record<string, string>;
	lines: {id: string; shot: string; text: string; emphasis?: string[]}[];
	shots: Shot[];
};

export type Brand = {
	logo: string;
	logoAspect: number;
	bug: {enabled: boolean; x: number; y: number; height: number; opacity: number};
};

export type Series = {
	name: string;
	tagline?: string;
	brand?: Brand;
	totalEpisodes: number;
	format: {width: number; height: number; fps: number};
	palette: Record<string, string>;
	safeArea: {top: number; bottom: number; left: number; right: number; captionCenterY: number};
};

/** Optional AI-generated plates: shot id -> file under public/<ep>/ */
export type Plates = Record<string, string>;

export type EpisodeProps = {
	episodeId: string;
	episode?: Episode;
	series?: Series;
	timing?: Timing;
	plates?: Plates;
};
