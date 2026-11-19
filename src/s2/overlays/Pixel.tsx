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
	// EP31: the chronicles' facts (flame; `coin` for motive) and the next-run standard (EP32: a torn battle flag)
	flame: {rows: ['..X..', '.XX..', '.XXX.', 'XXOXX', 'XOOOX', '.XXX.'], colors: {X: 'currentColor', O: '#ffe9a8'}},
	coin: {rows: ['.XXX.', 'XXOXX', 'XOXOX', 'XXOXX', '.XXX.'], colors: {X: 'currentColor', O: '#050912'}},
	standard: {
		rows: ['P.......', 'PRRRRRR.', 'PRRWRRRR', 'PRRRRRR.', 'PRRRR...', 'P.RR....', 'P.......', 'P.......', 'P.......', 'P.......'],
		colors: {P: '#8a5a36', R: '#d0603f', W: '#efe6d2'},
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
	// EP32: the strata (grass, two centuries, the war layer with a bronze fleck, a vein rising through them)
	strata: {
		rows: ['GGGGGGGGGG', 'SSSSVSSSSS', 'ssssVsssss', 'SSSSVSSSSS', 'WWWWVWWBWW', 'WBWWWWWWWW'],
		colors: {G: '#86bb5c', S: '#8f6c46', s: '#7a5a3a', W: '#3a2a2e', B: '#46c2a0', V: '#46c2a0'},
	},
	// EP32's tease for EP33: the sun, eclipsed (a dark disc inside a ring of light)
	sun: {
		rows: ['...YYYY...', '.YYDDDDYY.', '.YDDDDDDY.', 'YDDDDDDDDY', 'YDDDDDDDDY', 'YDDDDDDDDY', 'YDDDDDDDDY', '.YDDDDDDY.', '.YYDDDDYY.', '...YYYY...'],
		colors: {Y: '#f4c46e', D: '#141d38'},
	},
	// EP33's tease for EP34: the ground split by a crack of light (what the gods buried)
	rift: {
		rows: ['GGGGLGGGGG', 'GGGGLLGGGG', 'SSSLLSSSSS', 'SSSSLLSSSS', 'sssssLssss', 'ssssLLssss', 'WWWWLWWWWW', 'WWWLLWWWWW'],
		colors: {G: '#86bb5c', S: '#8f6c46', s: '#7a5a3a', W: '#3a2a2e', L: '#fff6d2'},
	},
	// EP33's field card icon: a lamp (the belief that answers a fear)
	lantern: {rows: ['.KKK.', '..K..', 'KKKKK', 'KYYYK', 'KYOYK', 'KYYYK', 'KKKKK'], colors: {K: '#3a2a1e', Y: '#ffe45c', O: '#fff6d2'}},
	// EP34: the two skies' counters (a hole torn in painted lapis; a brush that paints it over) and the next-run card
	// for EP35 (broken pillars older than anyone, one fallen stone set back in fresh mortar)
	tear: {rows: ['UUUUUUU', 'UUC.CUU', 'UC...CU', 'U.....U', 'UC...CU', 'UUC.CUU', 'UUUUUUU'], colors: {U: '#4a68ff', C: '#efe3c2'}},
	brush: {rows: ['....HH', '...HH.', '..HH..', '.FF...', 'BBF...', 'BB....'], colors: {H: '#8a5a36', F: '#c9c2b4', B: '#4a68ff'}},
	// EP35: the finds tray (a gear, a great pot, a well full of sand, a child's handprint, last night's stone), a
	// question mark (the run-2 counter) and the next-run card for EP36 (three war banners on poles: more than two sides)
	gear: {rows: ['...X.X...', '..XXXXX..', '.XXX.XXX.', 'XXO...OXX', '.X..O..X.', 'XXO...OXX', '.XXX.XXX.', '..XXXXX..', '...X.X...'], colors: {X: '#c99a52', O: '#7a5a2c'}},
	pot: {rows: ['...S..S....', '....S..S...', '...S..S....', 'RRRRRRRRRRR', '.XXXXXXXXX.', 'XXXXXXXXXXX', 'XXXXXXXXXXX', '.XXXXXXXXX.', '..XXXXXXX..', 'FF.F.F.F.FF'], colors: {S: '#e8e0d0', R: '#8a8a94', X: '#55555c', F: '#f4c46e'}},
	well: {rows: ['...sssss...', '..sssssss..', '.sssssssss.', 'KKKKKKKKKKK', 'KLKKLKKLKKL', 'KKKKKKKKKKK', 'LKKLKKLKKLK', 'KKKKKKKKKKK'], colors: {s: '#e2cf98', K: '#9a9585', L: '#6d695c'}},
	handprint: {rows: ['..X.X.X..', '..X.X.X..', 'X.X.X.X..', 'X.X.X.X..', 'XXXXXXX..', 'XXXXXXX.X', 'XXXXXXXXX', 'XXXXXXXX.', '.XXXXXX..', '..XXXX...'], colors: {X: '#d08a5c'}},
	stone: {rows: ['..W....W..', 'W.QQQQQQ.W', '.QWWQQQQQ.', '.QWQQQQQQ.', '.QQQQQQQQ.', '.QQQQQQQQ.', 'W.QQQQQQ.W', '..W....W..'], colors: {Q: '#4fd6ff', W: '#c4f6ff'}},
	query: {rows: ['.XXX.', 'X...X', '....X', '..XX.', '..X..', '.....', '..X..'], colors: {X: '#f4c46e'}},
	// EP36: the war room (reasons pinned per side) and EP37's tease
	pin: {rows: ['.XXX.', 'XXWXX', 'XXXXX', '.XXX.', '..P..', '..P..', '..P..', '..P..'], colors: {X: 'currentColor', W: '#ffffff', P: '#8a8076'}},
	anchor: {rows: ['...X...', '..X.X..', '...X...', 'XXXXXXX', '...X...', '...X...', 'X..X..X', '.X.X.X.', '..XXX..'], colors: {X: 'currentColor'}},
	shield: {rows: ['XXXXXXX', 'X.....X', 'X..X..X', 'X.XXX.X', 'X..X..X', '.X...X.', '..X.X..', '...X...'], colors: {X: 'currentColor'}},
	clasp: {rows: ['XX....YY', 'XXX..YYY', '.XXXYYY.', '..XYXY..', '.XXXYYY.', 'XXX..YYY', 'XX....YY'], colors: {X: '#4f7fbf', Y: '#d4b23f'}},
	spark: {rows: ['...X...', 'X..X..X', '.X.X.X.', '..XXX..', 'XXXWXXX', '..XXX..', '.X.X.X.', 'X..X..X', '...X...'], colors: {X: 'currentColor', W: '#ffffff'}},
	fume: {rows: ['.X..X..X', 'X..X..X.', '.X..X..X', '........', '.XXXXXX.', 'XX.XX.XX', 'XXXXXXXX', 'X.XXXX.X', '.X....X.'], colors: {X: 'currentColor'}},
	host: {
		rows: ['FFF..FFF..FFF..FFF..', 'PFF..PFF..PFF..PFF..', 'P....P....P....P....', 'P.H.HP.H.HP.H.HP.H.H', 'PHHHHPHHHHPHHHHPHHHH', 'BBBBBBBBBBBBBBBBBBBB', 'BBBBBBBBBBBBBBBBBBBB', 'B.B.B.B.B.B.B.B.B.B.'],
		colors: {P: '#6b5a48', F: '#8f98a6', H: '#e0c8a8', B: '#5d6673'},
	},
	banners: {
		rows: ['P......P......P.....', 'PRRRR..PBBBB..PGGGG.', 'PRRRRR.PBBBBB.PGGGGG', 'PRRR...PBBB...PGGG..', 'PRR....PBB....PGG...', 'P......P......P.....', 'P......P......P.....', 'P......P......P.....', 'P......P......P.....', 'GGGGGGGGGGGGGGGGGGGG'],
		colors: {P: '#6b5a48', R: '#c0573c', B: '#4f7fbf', G: '#d4b23f'},
	},
	ruins: {
		rows: ['SSSS.......SSSS', '.SS.........SS.', '.SS...MM....SS.', '.SS...SS....SS.', '.SS...SS.....S.', '.SS...SS.......', '.SS.F.SS.......', '.SS.FFSS...SS..', 'GGGGGGGGGGGGGGG', 'ddddddddddddddd'],
		colors: {S: '#9a9b8e', M: '#5f7a4a', F: '#efe3c2', G: '#86bb5c', d: '#7a5a3a'},
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
