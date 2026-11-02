// Season 2 design tokens ("the World Engine"). See docs/STYLE_S2.md.
import {loadFont} from '@remotion/fonts';
import type React from 'react';
import {staticFile} from 'remotion';

const faces: [string, string, string][] = [
	['Silkscreen', 'silkscreen-latin-400-normal', '400'],
	['Silkscreen', 'silkscreen-latin-700-normal', '700'],
	['Pixelify Sans', 'pixelify-sans-latin-500-normal', '500'],
	['Pixelify Sans', 'pixelify-sans-latin-600-normal', '600'],
	['Pixelify Sans', 'pixelify-sans-latin-700-normal', '700'],
	['Inter', 'inter-latin-900-normal', '900'],
];
for (const [family, file, weight] of faces) {
	loadFont({family, url: staticFile(`fonts/${file}.woff2`), weight, style: 'normal'});
}

export const S2 = {
	// series palette, kept
	night: '#0b1216',
	parchment: '#efe6d2',
	amber: '#e9a94b',
	ember: '#f4c46e',
	rust: '#d0603f',
	// Season 2 additions: the diorama's own colours, used by the HUD so numbers match the world
	panel: '#0a1430',
	panelEdge: '#efe6d2',
	ink: '#050912',
	prey: '#9bd16a',
	pred: '#f08a4b',
	sky: '#8fc8ff',
	stable: '#9bd16a',
};

export const F2 = {
	pixel: 'Silkscreen, "Pixelify Sans", monospace',
	pixelSans: '"Pixelify Sans", Silkscreen, monospace',
	caption: 'Inter, system-ui, sans-serif',
	serif: '"Cormorant Garamond", Georgia, serif',
};

/** One "pixel" of the S2 grid in output px (the diorama renders at 1/3 scale). */
export const PX = 3;

/** A pixel panel: flat dark fill, hard 2-px (6 px) light border, notched corners, hard offset shadow. */
export const panel = (opts: {bg?: string; edge?: string; px?: number} = {}): React.CSSProperties => {
	const p = opts.px ?? PX * 2;
	return {
		background: opts.bg ?? 'rgba(10, 20, 48, 0.9)',
		boxShadow: `0 0 0 ${p}px ${opts.edge ?? 'rgba(239, 230, 210, 0.9)'}, ${p * 2}px ${p * 2}px 0 ${p}px rgba(3, 6, 14, 0.75)`,
		clipPath: 'none',
	};
};

/** Hard pixel text shadow (no blur), for type sitting on the world. */
export const pixelShadow = (c = '#050912', n = 2, step = PX) =>
	Array.from({length: n}, (_, i) => `${(i + 1) * step}px ${(i + 1) * step}px 0 ${c}`).join(', ');

/** Outline via text-shadow in 8 directions + a drop. */
export const outline = (c = '#050912', w = 6) => {
	const d: string[] = [];
	for (let a = 0; a < 16; a++) {
		const r = (a / 16) * Math.PI * 2;
		d.push(`${(Math.cos(r) * w).toFixed(1)}px ${(Math.sin(r) * w).toFixed(1)}px 0 ${c}`);
	}
	d.push(`0 ${w + 4}px 0 ${c}`);
	return d.join(', ');
};
