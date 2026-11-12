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
	eye: {rows: ['...XXXXX...', '.XX.....XX.', 'X...XXX...X', 'X..XXOXX..X', 'X...XXX...X', '.XX.....XX.', '...XXXXX...'], colors: {X: 'currentColor', O: '#050912'}},
	// EP28: a Fenn (the counter icon) and an hourglass (the EP29 tease)
	fenn: {
		rows: ['F..GG..F', 'FFGGGGFF', '.GEGGEG.', '.GGGGGG.', '..GGGG..', '.GGGGGG.', 'G.GSSG.G', '..G..G..', '.GG..GG.'],
		colors: {G: '#3fa08a', F: '#2b7a69', E: '#0c1014', S: '#b89a5a'},
	},
	hourglass: {
		rows: ['XXXXXXXXX', '.X.....X.', '.XSSSSSX.', '..XSSSX..', '...XSX...', '...XSX...', '..X.S.X..', '.X..S..X.', '.XSSSSSX.', 'XXXXXXXXX'],
		colors: {X: '#c9a26a', S: '#f4c46e'},
	},
	// EP29: the Undying Queen (a counter icon), a mortal and an elder (the lineage strip), a crown, a council seat,
	// a memory lamp, a book (the record), and a shrine with candles (the EP30 tease)
	queen: {
		rows: ['..GGGG..', '.SSSSSS.', 'SSFFFFSS', 'SSFEFEFS', 'SSFFFFSS', 'SSVVVVSS', '.VVLVVV.', 'VVVLVVVV', 'VVVLVVVV'],
		colors: {G: '#e9b85a', S: '#ece2e0', F: '#f1d6c4', E: '#2a1838', V: '#6a43a0', L: '#bba4c7'},
	},
	mortal: {rows: ['.HHH.', 'HSSSH', '.SSS.', 'XXXXX', 'XXXXX', '.XXX.', '.L.L.'], colors: {H: '#5a3a22', S: '#e2b48a', X: 'currentColor', L: '#3a2c20'}},
	elder: {rows: ['.HHH.', 'HSSSH', '.SSS.', 'XXXXX', 'XXXXX', '.XXX.', '.L.L.'], colors: {H: '#e4e0da', S: '#e2b48a', X: 'currentColor', L: '#3a2c20'}},
	crown: {rows: ['X.X.X', 'XXXXX', 'XXXXX'], colors: {X: 'currentColor'}},
	seat: {rows: ['XX...', 'XX...', 'XXXXX', 'X...X'], colors: {X: 'currentColor'}},
	lamp: {rows: ['.X.', 'XXX', 'XXX', '.X.'], colors: {X: 'currentColor'}},
	book: {rows: ['XXX.XXX', 'X.XXX.X', 'X..X..X', 'XXXXXXX'], colors: {X: 'currentColor'}},
	shrine: {
		rows: ['...F...F...F...', '...C...C...C...', '...C...C...C...', '.SSSSSSSSSSSSS.', '.SKKKKKKKKKKKS.', 'SSSSSSSSSSSSSSS', '.S...........S.', '.S...........S.'],
		colors: {F: '#ffc96a', C: '#efe3c4', S: '#8f8c86', K: '#a9a49a'},
	},
	// EP30: the ledger's weights (harvest, medicine; fear reuses `eye`) and the next-run stele (EP31: a painted standing stone)
	sheaf: {rows: ['G.G.G', '.GGG.', 'GGGGG', '.BBB.', '..G..', '.G.G.', 'G...G'], colors: {G: '#e6c357', B: '#b98a4e'}},
	vial: {rows: ['.CC.', '.KK.', 'K..K', 'KRRK', 'KRRK', '.KK.'], colors: {C: '#8a5a36', K: '#efe6d2', R: '#e0687f'}},
	stele: {
		rows: ['.SSSSS.', 'SSSSSSS', 'SSSGSSS', 'SGSGSGS', 'SSGGGSS', 'SSSGSSS', 'SSGSGSS', 'SSGSGSS', 'SSSSSSS', 'SSSSSSS', 'SSSSSSS', 'DDDDDDD'],
		colors: {S: '#9b968c', G: '#f4c46e', D: '#6b5a48'},
	},
	play: {rows: ['X....','XXX..', 'XXXXX', 'XXX..', 'X....'], colors: {X: 'currentColor'}},
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
