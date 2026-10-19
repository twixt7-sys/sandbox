import React, {useMemo} from 'react';
import {AbsoluteFill} from 'remotion';
import {ease} from '../lib/timing';
import {fonts, palette} from '../theme';
import type {Episode, Timing} from '../types';

type CapWord = {text: string; start: number; end: number; em: boolean};
type Group = {words: CapWord[]; start: number; end: number};

const MAX_CHARS = 20;
const norm = (w: string) => w.toLowerCase().replace(/[^a-z0-9']/g, '');

/** Phrase-chunk the verified word timings into short single-line caption groups. */
export const buildGroups = (timing: Timing, episode: Episode): Group[] => {
	const off = new Set(episode.shots.filter((s) => s.captions === false).map((s) => s.id));
	const replace = episode.captionReplace ?? {};
	const groups: Group[] = [];
	for (const line of timing.lines) {
		if (off.has(line.shot)) continue;
		const em = new Set(line.emphasis.map(norm));
		let cur: CapWord[] = [];
		const flush = () => {
			if (cur.length) groups.push({words: cur, start: cur[0].start, end: cur[cur.length - 1].end});
			cur = [];
		};
		line.words.forEach((w, i) => {
			const bare = w.text.replace(/[.,;:]+$/, '');
			const text = replace[bare.toLowerCase()] ?? bare;
			const len = cur.reduce((n, c) => n + c.text.length + 1, 0);
			const gap = cur.length ? w.start - cur[cur.length - 1].end : 0;
			if (cur.length && (len + text.length > MAX_CHARS || gap > 0.28)) flush();
			cur.push({text, start: w.start, end: w.end, em: em.has(norm(bare))});
			if (/[.,;:!?]$/.test(w.text) && i < line.words.length - 1) flush();
		});
		flush();
	}
	// Each group holds until the next begins (or briefly after its last word).
	return groups.map((g, i) => {
		const next = groups[i + 1];
		const hold = next && next.start - g.end < 0.6 ? next.start - 0.03 : g.end + 0.35;
		return {...g, start: g.start - 0.08, end: hold};
	});
};

export const Captions: React.FC<{timing: Timing; episode: Episode; t: number; centerY: number}> = ({timing, episode, t, centerY}) => {
	const groups = useMemo(() => buildGroups(timing, episode), [timing, episode]);
	const g = groups.find((x) => t >= x.start && t < x.end);
	const anyVisible = groups.some((x) => t >= x.start - 0.4 && t < x.end + 0.4);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div
				style={{
					position: 'absolute',
					left: 0,
					right: 0,
					top: centerY - 190,
					height: 380,
					background: 'linear-gradient(180deg, rgba(6,10,13,0) 0%, rgba(6,10,13,0.42) 50%, rgba(6,10,13,0) 100%)',
					opacity: anyVisible ? 1 : 0,
				}}
			/>
			{g && (
				<div
					style={{
						position: 'absolute',
						left: 90,
						right: 160,
						top: centerY - 44,
						textAlign: 'center',
						transform: `translateY(${(1 - ease(t, g.start, 0.18)) * 16}px)`,
						opacity: ease(t, g.start, 0.14),
						fontFamily: fonts.ui,
						fontWeight: 800,
						fontSize: 66,
						lineHeight: 1.12,
						letterSpacing: '-0.01em',
						textShadow: '0 2px 2px rgba(0,0,0,0.65), 0 4px 22px rgba(0,0,0,0.55)',
					}}
				>
					{g.words.map((w, i) => {
						const spoken = t >= w.start - 0.03;
						return (
							<span key={i} style={{color: w.em ? palette.amber : palette.parchment, opacity: spoken ? 1 : 0.5, marginRight: i < g.words.length - 1 ? '0.26em' : 0}}>
								{w.text}
							</span>
						);
					})}
				</div>
			)}
		</AbsoluteFill>
	);
};
