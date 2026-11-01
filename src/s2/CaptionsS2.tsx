// Season 2 captions: short bursts (1–3 words, ≤16 characters) that swap as they are spoken, each word popping
// on its own timestamp; emphasis words in ember. Heavy outline so they read over the bright diorama.
import React, {useMemo} from 'react';
import {AbsoluteFill} from 'remotion';
import {clamp} from './rng';
import {F2, outline, S2} from './style';
import type {Episode, Timing} from '../types';

type W = {text: string; start: number; end: number; em: boolean};
type G = {words: W[]; start: number; end: number};
const MAX = 13;
const norm = (w: string) => w.toLowerCase().replace(/[^a-z0-9']/g, '');

export const buildGroupsS2 = (timing: Timing, episode: Episode): G[] => {
	const off = new Set(episode.shots.filter((s) => s.captions === false).map((s) => s.id));
	const offLines = new Set((episode as any).captionsOffLines ?? []);
	// [{line, from}]: drop that line's captions from the word `from` on (a kinetic title says it instead)
	const offs: {line: string; from: string; to?: string}[] = (episode as any).captionsOff ?? [];
	const groups: G[] = [];
	for (const line of timing.lines) {
		if (off.has(line.shot) || offLines.has(line.id)) continue;
		const em = new Set(line.emphasis.map(norm));
		let cur: W[] = [];
		const flush = () => {
			if (cur.length) groups.push({words: cur, start: cur[0].start, end: cur[cur.length - 1].end});
			cur = [];
		};
		// [{line, from, to?}]: drop words from `from` up to (not including) `to` — a kinetic title says them instead
		const cuts = offs
			.filter((c) => c.line === line.id)
			.map((c) => {
				const a = line.words.findIndex((w) => norm(w.text) === norm(c.from));
				const b = c.to ? line.words.findIndex((w) => norm(w.text) === norm(c.to!)) : line.words.length;
				return [a, b < 0 ? line.words.length : b] as [number, number];
			});
		line.words.forEach((w, wi) => {
			if (cuts.some(([a, b]) => a >= 0 && wi >= a && wi < b)) {
				flush();
				return;
			}
			const text = w.text.replace(/[,;]+$/, '');
			const len = cur.reduce((n, c) => n + c.text.length + 1, 0);
			const gap = cur.length ? w.start - cur[cur.length - 1].end : 0;
			if (cur.length && (len + text.length > MAX || cur.length >= 3 || gap > 0.25)) flush();
			cur.push({text, start: w.start, end: w.end, em: em.has(norm(w.text))});
			if (/[.,;:!?]$/.test(w.text)) flush();
		});
		flush();
	}
	return groups.map((g, i) => {
		const next = groups[i + 1];
		const hold = next && next.start - g.end < 0.5 ? next.start - 0.02 : g.end + 0.3;
		return {...g, start: g.start - 0.06, end: hold};
	});
};

export const CaptionsS2: React.FC<{timing: Timing; episode: Episode; t: number; centerY: number}> = ({timing, episode, t, centerY}) => {
	const groups = useMemo(() => buildGroupsS2(timing, episode), [timing, episode]);
	const g = groups.find((x) => t >= x.start && t < x.end);
	if (!g) return null;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: 70, right: 140, top: centerY - 50, textAlign: 'center', fontFamily: F2.caption, fontWeight: 900, fontSize: 78, lineHeight: 1.05, letterSpacing: '-0.01em', textTransform: 'uppercase'}}>
				{g.words.map((w, i) => {
					const k = clamp((t - (w.start - 0.04)) / 0.1);
					const spoken = t >= w.start - 0.04;
					return (
						<span
							key={i}
							style={{
								display: 'inline-block',
								marginRight: i < g.words.length - 1 ? '0.24em' : 0,
								color: w.em ? S2.ember : S2.parchment,
								opacity: spoken ? 1 : 0.0,
								transform: `scale(${spoken ? 1 + (1 - k) * 0.22 : 0.9}) translateY(${(1 - k) * 6}px)`,
								textShadow: outline('#050912', 7),
							}}
						>
							{w.text}
						</span>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};
