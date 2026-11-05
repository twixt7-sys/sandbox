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
	// EP27: livestock, a roof, a trade cart, a speech bubble (the comment ask), stacked stones (the EP28 tease)
	sheep: {
		rows: ['..WWWWWW....', '.WWWWWWWW.HH', 'WWWWWWWWWHHH', 'WWWWWWWWW.HE', '.WWWWWWWW...', '..L.L..L.L..'],
		colors: {W: '#f3efe4', H: '#24201d', E: '#24201d', L: '#2b2622'},
	},
	house: {
		rows: ['.....RR.....', '...RRRRRR...', '.RRRRRRRRRR.', 'RRRRRRRRRRRR', '.WWWWWWWWWW.', '.WWWWDDWWWW.', '.WWWWDDWWWW.'],
		colors: {R: '#d8b25a', W: '#e3d4b3', D: '#6b4a30'},
	},
	cart: {
		rows: ['..CCCCC.....', '.CCCCCCC..PP', '.CCCCCCC.PPP', 'BBBBBBBBBPP.', 'BBBBBBBBB.P.', '.K....K..P.P'],
		colors: {C: '#efe3c4', B: '#8a5a36', K: '#2c2420', P: '#5a3c28'},
	},
	bubble: {
		rows: ['.XXXXXXXXX.', 'XXXXXXXXXXX', 'XX.X.X.X.XX', 'XXXXXXXXXXX', '.XXXXXXXXX.', '...XX......', '..XX.......', '.X.........'],
		colors: {X: 'currentColor'},
	},
	cairn: {
		rows: ['.......LLLL.......', '......LMMMML......', '.....LMMMMMML.....', '.....LLLLLLLL.....', '...LKKKKKKKKKL....', '..LKKKKKKKKKKKL...', '..LLLLLLLLLLLLL...', 'LGGGGGGGGGGGGGGGL.', 'LGGGGGGGGGGGGGGGGL', 'LGGGGGGGGGGGGGGGGL', '.LLLLLLLLLLLLLLLL.'],
		colors: {L: '#2a2d36', M: '#8c877f', K: '#b2ada3', G: '#9a968e'},
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
	plus: {rows: ['..XX..', '..XX..', 'XXXXXX', 'XXXXXX', '..XX..', '..XX..'], colors: {X: 'currentColor'}},
	// the classic pointer hand (the follow button's "tap")
	hand: {
		rows: ['....XX......', '...XWWX.....', '...XWWX.....', '...XWWX.....', '...XWWXXX...', '...XWWXWWXX.', '.XXXWWXWWXWX', 'XWWXWWWWWWWX', 'XWWXWWWWWWWX', '.XWWWWWWWWWX', '..XWWWWWWWWX', '..XWWWWWWWX.', '...XWWWWWWX.', '...XXXXXXXX.'],
		colors: {X: '#050912', W: '#efe6d2'},
	},
	// a dragon seen from above: the same silhouette as its shadow on the Isle (the EP27 tease)
	dragon: {
		rows: ['........H.H........', '.........H.........', '........HEH........', '.........B.........', 'WW.......B.......WW', '.WWW....BBB....WWW.', '..WWWW..BBB..WWWW..', '..WWWWWBBBBBWWWWW..', '...WWWWWBBBWWWWW...', '...WWWWWBBBWWWWW...', '....W.W.WBW.W.W....', '.........B.........', '.........B.........', '..........B........', '..........B........', '.........TT........'],
		colors: {H: '#c95a3c', E: '#f4c46e', B: '#b34a35', W: '#d0603f', T: '#8f3a2c'},
	},
};

/** `mono` paints every pixel one colour (a locked silhouette, e.g. the next episode's creature before its reveal). */
export const PixelSprite: React.FC<{name: string; px?: number; color?: string; mono?: string; style?: React.CSSProperties}> = ({name, px = 6, color, mono, style}) => {
	const sp = SPRITES[name];
	if (!sp) return null;
	const w = Math.max(...sp.rows.map((r) => r.length));
	const h = sp.rows.length;
	return (
		<svg width={w * px} height={h * px} viewBox={`0 0 ${w} ${h}`} shapeRendering="crispEdges" style={{display: 'block', color, ...style}}>
			{sp.rows.flatMap((row, y) =>
				row.split('').map((ch, x) => (ch === '.' || ch === ' ' ? null : <rect key={`${x}-${y}`} x={x} y={y} width={1} height={1} fill={mono ?? sp.colors[ch] ?? 'currentColor'} />)),
			)}
		</svg>
	);
};
