import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Self-hosted (SIL OFL) so cloud renders never depend on a font CDN.
const faces: [string, string, string, 'normal' | 'italic'][] = [
	['Cormorant Garamond', 'cormorant-garamond-latin-500-normal', '500', 'normal'],
	['Cormorant Garamond', 'cormorant-garamond-latin-600-normal', '600', 'normal'],
	['Cormorant Garamond', 'cormorant-garamond-latin-700-normal', '700', 'normal'],
	['Cormorant Garamond', 'cormorant-garamond-latin-500-italic', '500', 'italic'],
	['Cormorant Garamond', 'cormorant-garamond-latin-600-italic', '600', 'italic'],
	['Inter', 'inter-latin-500-normal', '500', 'normal'],
	['Inter', 'inter-latin-600-normal', '600', 'normal'],
	['Inter', 'inter-latin-700-normal', '700', 'normal'],
	['Inter', 'inter-latin-800-normal', '800', 'normal'],
];
for (const [family, file, weight, style] of faces) {
	loadFont({family, url: staticFile(`fonts/${file}.woff2`), weight, style});
}

export const fonts = {
	display: '"Cormorant Garamond", Georgia, serif',
	ui: 'Inter, system-ui, sans-serif',
};

// Mirrors series/series.json so components can be used without props drilling.
export const palette = {
	night: '#0b1216',
	slate: '#16222a',
	fog: '#9fb1b8',
	mist: '#d6dfe0',
	parchment: '#efe6d2',
	ink: '#1c1a17',
	amber: '#e9a94b',
	ember: '#f4c46e',
	rust: '#b9543a',
};

export const W = 1080;
export const H = 1920;
