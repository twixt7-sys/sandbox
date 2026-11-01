// Tiny pixel sprites drawn in code (HUD icons), on the same 3-px grid as the diorama.
import React from 'react';

export const SPRITES: Record<string, {rows: string[]; colors: Record<string, string>}> = {
	mossback: {
		rows: ['...MMMM.....', '..MMWMMM....', '.WWWWWWWW.HH', '.WWWWWWWWHHH', '.WWWWWWWW.H.', '..L.L..L.L..'],
		colors: {W: '#ece2c6', M: '#41763a', H: '#6a5038', L: '#3a2c20'},
	},
	grimmaw: {
		rows: ['....R.R.R.....', '..RRRRRRRR.W..', '.DDDDDDDDDWWW.', 'DDSDDSDDDDWWWW', '.DDDDDDDDDDW..', '.DD.D...DD.D..'],
		colors: {D: '#686c78', S: '#3a3d46', R: '#cf7038', W: '#d6c6a5'},
	},
	play: {rows: ['X....', 'XXX..', 'XXXXX', 'XXX..', 'X....'], colors: {X: 'currentColor'}},
	ffwd: {rows: ['X...X...', 'XX..XX..', 'XXX.XXX.', 'XX..XX..', 'X...X...'], colors: {X: 'currentColor'}},
	rewind: {rows: ['...X...X', '..XX..XX', '.XXX.XXX', '..XX..XX', '...X...X'], colors: {X: 'currentColor'}},
	lock: {rows: ['.XXX.', 'X...X', 'X...X', 'XXXXX', 'XX.XX', 'XXXXX'], colors: {X: 'currentColor'}},
	check: {rows: ['......X', '.....XX', 'X...XX.', 'XX.XX..', '.XXX...', '..X....'], colors: {X: 'currentColor'}},
	cross: {rows: ['X...X', '.X.X.', '..X..', '.X.X.', 'X...X'], colors: {X: 'currentColor'}},
	share: {
		rows: ['.....XX..', '....XXXX.', '...XXXXXX', '.....XX..', '..XXXXX..', '.XXXX....', 'XXX......', 'XX.......'],
		colors: {X: 'currentColor'},
	},
	heart: {rows: ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...'], colors: {X: 'currentColor'}},
	z: {rows: ['XXXX', '..X.', '.X..', 'XXXX'], colors: {X: 'currentColor'}},
};

export const PixelSprite: React.FC<{name: string; px?: number; color?: string; style?: React.CSSProperties}> = ({name, px = 6, color, style}) => {
	const sp = SPRITES[name];
	if (!sp) return null;
	const w = Math.max(...sp.rows.map((r) => r.length));
	const h = sp.rows.length;
	return (
		<svg width={w * px} height={h * px} viewBox={`0 0 ${w} ${h}`} shapeRendering="crispEdges" style={{display: 'block', color, ...style}}>
			{sp.rows.flatMap((row, y) =>
				row.split('').map((ch, x) => (ch === '.' || ch === ' ' ? null : <rect key={`${x}-${y}`} x={x} y={y} width={1} height={1} fill={sp.colors[ch] ?? 'currentColor'} />)),
			)}
		</svg>
	);
};
