// EP34+: the two skies. The Lamplight's creation myth is a painted dome over the Isle; what the ground shows tears
// holes in it. Everything here is drawn only when an episode sets `world.sky` (or uses the `bones` / `ruin` props), so
// every older episode renders exactly as before.
import React, {useMemo} from 'react';
import * as THREE from 'three';
import {hash2} from '../rng';
import type {Island} from './island';
import type {SkyNow} from './timeline';

// ---------------------------------------------------------------- the painting (code-drawn, deterministic)

const W = 2048;
const H = 1024;
const DEG = 360 / W; // one texel in degrees (both axes)

type RGB = [number, number, number];
const hex = (h: string): RGB => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];

// fresco ultramarine and gilt (the episode's motif colour is the paint itself)
const SKY_BANDS: [number, string][] = [
	[50, '#141c4e'],
	[32, '#1a2766'],
	[18, '#233686'],
	[8, '#2d45a4'],
	[0, '#3956bb'],
	[-4.2, '#1b2560'],
	[-22, '#141b52'],
	[-45, '#0e1442'],
];
const GILT = hex('#e6be5e');
const GILT_HI = hex('#fff1c2');
const GOLD = hex('#c99a3e');
const GOLD_DK = hex('#6a4a22');
const CREAM = hex('#efe3c2');
const CLOUD = hex('#e3d8bd');
const CLOUD_HI = hex('#f6efdc');
const CLOUD_LO = hex('#9c8a68');

/** The lantern of the myth, as a pixel grid (K bronze outline, G gold frame, Y / O / X its light, from rim to core). */
const LANTERN = [
	'.....KKKK.....',
	'....K....K....',
	'....K....K....',
	'.....KKKK.....',
	'......KK......',
	'...KKKKKKKK...',
	'..KGGGGGGGGK..',
	'..KGYYYYYYGK..',
	'..KGYOOOOYGK..',
	'..KGYOXXOYGK..',
	'..KGYOXXOYGK..',
	'..KGYOXXOYGK..',
	'..KGYOOOOYGK..',
	'..KGYYYYYYGK..',
	'..KGGGGGGGGK..',
	'...KKKKKKKK...',
	'....KGGGGK....',
	'.....KKKK.....',
];
const LANTERN_C: Record<string, RGB> = {K: hex('#3a2a1e'), G: hex('#d9a843'), Y: hex('#ffd977'), O: hex('#fff0b0'), X: hex('#fffbea')};

const bandColor = (el: number, x: number, y: number): RGB => {
	for (let i = 0; i < SKY_BANDS.length; i++) {
		const [lo, c] = SKY_BANDS[i];
		if (el >= lo) {
			// dither the last degree above each band edge (a painted, pixel-art gradient)
			if (i > 0 && el - lo < 1.0 && (x + y) % 2 === 0) return hex(SKY_BANDS[i - 1][1]);
			return hex(c);
		}
	}
	return hex(SKY_BANDS[SKY_BANDS.length - 1][1]);
};

/** Paint the inside of the dome as an equirectangular RGBA texture (alpha 255; 250 marks the lamp and its trail,
 * which stay longest when the paint thins). Row 0 is elevation −90°, column 0 is dome azimuth 0°. */
const paint = (lamp: {az: number; el: number}): Uint8Array => {
	const data = new Uint8Array(W * H * 4);
	const put = (x: number, y: number, c: RGB, a = 255) => {
		const xx = ((Math.round(x) % W) + W) % W;
		const yy = Math.round(y);
		if (yy < 0 || yy >= H) return;
		const k = (yy * W + xx) * 4;
		data[k] = c[0];
		data[k + 1] = c[1];
		data[k + 2] = c[2];
		data[k + 3] = a;
	};
	const tx = (az: number) => az / DEG;
	const ty = (el: number) => (el + 90) / DEG;
	// 1. the lapis ground, banded and dithered by elevation
	for (let y = 0; y < H; y++) {
		const el = (y + 0.5) * DEG - 90;
		for (let x = 0; x < W; x++) put(x, y, bandColor(el, x, y));
	}
	// 2. the gold horizon band with a running wave ornament (purely geometric)
	for (let x = 0; x < W; x++) {
		for (let y = Math.floor(ty(-4.2)); y <= Math.ceil(ty(-0.6)); y++) {
			const el = (y + 0.5) * DEG - 90;
			let c = GOLD;
			if (el > -1.0 || el < -3.8) c = el > -1.0 ? CREAM : GOLD_DK;
			else {
				const wave = -2.4 + 0.9 * Math.sin((x / W) * Math.PI * 2 * 90);
				if (Math.abs(el - wave) < 0.32) c = GOLD_DK;
				else if (Math.abs(el - wave) < 0.6) c = GILT;
			}
			put(x, y, c);
		}
	}
	// a shape drawn in the tangent plane at (az0, el0): f(dx, dy) in degrees returns a colour or null
	const stamp = (az0: number, el0: number, rx: number, ry: number, f: (dx: number, dy: number) => RGB | null, a = 255) => {
		const ce = Math.max(0.2, Math.cos((el0 * Math.PI) / 180));
		for (let y = Math.floor(ty(el0 - ry)); y <= Math.ceil(ty(el0 + ry)); y++) {
			const el = (y + 0.5) * DEG - 90;
			for (let x = Math.floor(tx(az0 - rx / ce)); x <= Math.ceil(tx(az0 + rx / ce)); x++) {
				const az = (x + 0.5) * DEG;
				const c = f((az - az0) * ce, el - el0);
				if (c) put(x, y, c, a);
			}
		}
	};
	// 3. gilt four-point stars, scattered evenly over the sphere (a few big ones)
	for (let i = 0; i < 1300; i++) {
		const u = hash2(i, 1, 341);
		const v = hash2(i, 2, 341);
		const az = u * 360;
		const el = (Math.asin(2 * v - 1) * 180) / Math.PI;
		if (el > -6 && el < 1.2) continue;
		if (el < -6 && hash2(i, 5, 341) > 0.45) continue;
		const big = hash2(i, 3, 341) > 0.88;
		const arm = big ? 3 : hash2(i, 4, 341) > 0.5 ? 2 : 1;
		stamp(az, el, (arm + 1) * DEG, (arm + 1) * DEG, (dx, dy) => {
			const ix = Math.round(dx / DEG);
			const iy = Math.round(dy / DEG);
			if (ix === 0 && iy === 0) return big ? GILT_HI : GILT;
			if ((ix === 0 && Math.abs(iy) <= arm) || (iy === 0 && Math.abs(ix) <= arm)) return GILT;
			if (big && Math.abs(ix) === 1 && Math.abs(iy) === 1) return GILT;
			return null;
		});
	}
	// 4. painted clouds along the horizon: lumps of cream with a lit top and a dark underline
	for (let i = 0; i < 22; i++) {
		const az = hash2(i, 1, 342) * 360;
		const el = 2.6 + hash2(i, 2, 342) * 9;
		const w = 5 + hash2(i, 3, 342) * 6;
		const lumps = Array.from({length: 4}, (_, k) => [(k - 1.5) * w * 0.32 + (hash2(i, 10 + k, 342) - 0.5) * 1.2, 0.6 + hash2(i, 20 + k, 342) * w * 0.18, w * (0.22 + hash2(i, 30 + k, 342) * 0.1)]);
		const inside = (dx: number, dy: number) => dy > -0.2 && lumps.some(([cx, cy, r]) => (dx - cx) ** 2 + ((dy - cy) * 1.25) ** 2 < r * r);
		stamp(az, el, w * 0.9, w * 0.6, (dx, dy) => {
			if (!inside(dx, dy)) return null;
			if (!inside(dx, dy - DEG * 2)) return CLOUD_LO;
			if (!inside(dx, dy + DEG * 2)) return CLOUD_HI;
			return CLOUD;
		});
	}
	// 5. the First Lamp, falling: rays around it, a trail of light behind it (up and to the left), drops below
	const tilt = (-24 * Math.PI) / 180;
	const cell = 0.62;
	const gw = LANTERN[0].length;
	const gh = LANTERN.length;
	const L = 250;
	stamp(lamp.az, lamp.el, 15, 15, (dx, dy) => {
		const d = Math.hypot(dx, dy);
		const a = Math.atan2(dy, dx);
		// twelve rays, alternating gilt and cream, broken into dashes
		if (d > 6.4 && d < 12.5) {
			const k = Math.round((a / (Math.PI * 2)) * 12);
			const off = Math.abs(a - (k / 12) * Math.PI * 2);
			if (off * d < 0.38 && Math.floor(d / 1.4) % 2 === 0) return k % 2 ? CREAM : GILT;
		}
		return null;
	}, L);
	// the trail: a band of light running up-left from the lamp, widening and breaking into gilt drops
	for (let k = 0; k < 26; k++) {
		const s = 4.5 + k * 1.05;
		const ang = Math.PI - 0.62;
		const cx = Math.cos(ang) * s;
		const cy = Math.sin(ang) * s;
		const r = Math.max(0.35, 2.2 - k * 0.07);
		const c = k < 6 ? GILT_HI : k % 3 === 0 ? CREAM : GILT;
		stamp(lamp.az + cx / Math.max(0.2, Math.cos((lamp.el * Math.PI) / 180)), lamp.el + cy, r, r, (dx, dy) => (Math.hypot(dx, dy) < r && (k < 12 || (Math.round(dx / DEG) + Math.round(dy / DEG)) % 3 !== 0) ? c : null), L);
	}
	// drops of light falling from it towards the horizon (the world it lit)
	for (let k = 0; k < 9; k++) {
		const dx = 1.5 + (hash2(k, 1, 343) - 0.5) * 7;
		const dy = -6 - k * 1.2 - hash2(k, 2, 343) * 1.5;
		stamp(lamp.az + dx / Math.max(0.2, Math.cos((lamp.el * Math.PI) / 180)), lamp.el + dy, 0.6, 0.9, (x, y) => (Math.abs(x) + Math.abs(y) * 0.7 < 0.55 ? (k % 2 ? GILT : GILT_HI) : null), L);
	}
	// the lantern itself, tilted as it falls
	stamp(lamp.az, lamp.el, gh * cell * 0.75, gh * cell * 0.75, (dx, dy) => {
		const rx = dx * Math.cos(-tilt) - dy * Math.sin(-tilt);
		const ry = dx * Math.sin(-tilt) + dy * Math.cos(-tilt);
		const gx = Math.floor(rx / cell + gw / 2);
		const gy = Math.floor(-ry / cell + gh / 2);
		if (gx < 0 || gy < 0 || gx >= gw || gy >= gh) return null;
		const ch = LANTERN[gy][gx];
		return ch === '.' ? null : LANTERN_C[ch];
	}, L);
	return data;
};

let TEX: {key: string; tex: THREE.DataTexture} | null = null;
const skyTexture = (lamp: {az: number; el: number}) => {
	const key = `${lamp.az},${lamp.el}`;
	if (TEX && TEX.key === key) return TEX.tex;
	const tex = new THREE.DataTexture(paint(lamp), W, H, THREE.RGBAFormat);
	tex.magFilter = THREE.NearestFilter;
	tex.minFilter = THREE.NearestFilter;
	tex.wrapS = THREE.RepeatWrapping;
	tex.generateMipmaps = false;
	tex.needsUpdate = true;
	TEX = {key, tex};
	return tex;
};

// ---------------------------------------------------------------- the dome

const MAX_TEARS = 16;
const VERT = `
varying vec3 vDir;
void main() {
	vDir = position;
	gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`;
const FRAG = `
uniform sampler2D uTex;
uniform vec4 uTear[${MAX_TEARS}];
uniform vec4 uTearK[${MAX_TEARS}];
uniform vec4 uSky;
uniform float uSun;
varying vec3 vDir;
void main() {
	vec3 d = normalize(vDir);
	float az = atan(d.x, d.z);
	float el = asin(clamp(d.y, -1.0, 1.0));
	vec2 uv = vec2(fract(az / 6.2831853), el / 3.14159265 + 0.5);
	vec4 tx = texture2D(uTex, uv);
	vec3 c = tx.rgb;
	float lampM = tx.a < 0.99 ? 1.0 : 0.0;
	float hole = 0.0;
	float rim = 0.0;
	float pat = 0.0;
	vec3 patchC = vec3(0.0);
	for (int i = 0; i < ${MAX_TEARS}; i++) {
		vec4 T = uTear[i];
		vec4 K = uTearK[i];
		if (K.x <= 0.001) continue;
		float cs = clamp(dot(d, T.xyz), -1.0, 1.0);
		if (cs < cos(T.w * 1.5 + 0.03)) continue;
		float ang = acos(cs);
		vec3 up = abs(T.y) > 0.95 ? vec3(1.0, 0.0, 0.0) : vec3(0.0, 1.0, 0.0);
		vec3 e1 = normalize(cross(up, T.xyz));
		vec3 e2 = cross(T.xyz, e1);
		vec3 q = d - T.xyz * cs;
		float lx = dot(q, e1);
		float ly = dot(q, e2);
		float a = atan(ly, lx);
		float s = K.z;
		float rag = 0.84 + 0.12 * sin(a * 5.0 + s) + 0.07 * sin(a * 11.0 + s * 2.3) + 0.05 * sin(a * 23.0 + s * 4.1);
		float R = T.w * K.x * rag;
		if (K.y > 0.001) {
			// a patch: fresher paint brushed across the hole (along e1), a little larger than it, with a dark seam
			float RP = T.w * 1.12 * (0.95 + 0.04 * sin(a * 3.0 + s));
			float u = lx / max(T.w, 1e-4);
			if (ang < RP && u < mix(-1.3, 1.3, K.y)) {
				pat = 1.0;
				float stripe = sin((lx * 0.8 + ly * 0.6) / max(T.w, 1e-4) * 9.0);
				patchC = ang > RP - T.w * 0.08 ? vec3(0.07, 0.1, 0.3) : vec3(0.33, 0.47, 0.9) * (stripe > 0.3 ? 1.0 : stripe > -0.3 ? 0.9 : 0.8);
				continue;
			}
		}
		if (ang < R) hole = 1.0;
		else if (ang < R + 0.012 + 0.005 * sin(a * 7.0 + s)) rim = max(rim, ang < R + 0.005 ? 2.0 : 1.0);
	}
	if (pat > 0.5) c = patchC;
	else if (hole > 0.5) discard;
	else if (rim > 1.5) c = vec3(0.17, 0.12, 0.08);
	else if (rim > 0.5) c = vec3(0.93, 0.87, 0.74);
	// the room's light falls on the painting (warm at golden hour, drained in gloom)
	c *= (0.8 + 0.2 * uSun) * mix(vec3(1.0), vec3(1.16, 0.98, 0.8), uSky.z * 0.55);
	float g = dot(c, vec3(0.299, 0.587, 0.114));
	c = mix(vec3(g), c, uSky.w);
	float alpha = uSky.x * max(1.0 - 0.9 * uSky.y, lampM * (1.0 - 0.4 * uSky.y));
	if (alpha < 0.01) discard;
	gl_FragColor = vec4(c, alpha);
}`;

const dirOf = (az: number, el: number) => {
	const a = (az * Math.PI) / 180;
	const e = (el * Math.PI) / 180;
	return new THREE.Vector3(Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e));
};

/** The painted dome: a sphere seen from outside through its back faces, so its far inner wall is the sky behind the
 * island wherever the camera stands. Holes are discarded (the true sky behind shows), patches are repainted. */
export const PaintedSky: React.FC<{sky: SkyNow; warm: number; sat: number; sun: number}> = ({sky, warm, sat, sun}) => {
	const geo = useMemo(() => new THREE.SphereGeometry(1, 96, 48), []);
	const mat = useMemo(
		() =>
			new THREE.ShaderMaterial({
				uniforms: {
					uTex: {value: null},
					uTear: {value: Array.from({length: MAX_TEARS}, () => new THREE.Vector4())},
					uTearK: {value: Array.from({length: MAX_TEARS}, () => new THREE.Vector4())},
					uSky: {value: new THREE.Vector4(1, 0, 0, 1)},
					uSun: {value: 1},
				},
				vertexShader: VERT,
				fragmentShader: FRAG,
				side: THREE.BackSide,
				transparent: true,
				depthWrite: false,
				fog: false,
			}),
		[],
	);
	mat.uniforms.uTex.value = skyTexture(sky.lamp);
	for (let i = 0; i < MAX_TEARS; i++) {
		const tr = sky.tears[i];
		if (tr && tr.open > 0.001) {
			const d = dirOf(tr.az, tr.el);
			(mat.uniforms.uTear.value[i] as THREE.Vector4).set(d.x, d.y, d.z, (tr.r * Math.PI) / 180);
			(mat.uniforms.uTearK.value[i] as THREE.Vector4).set(tr.open, tr.patch, tr.seed, 0);
		} else (mat.uniforms.uTearK.value[i] as THREE.Vector4).set(0, 0, 0, 0);
	}
	(mat.uniforms.uSky.value as THREE.Vector4).set(sky.paint, sky.sheer, warm, sat);
	mat.uniforms.uSun.value = sun;
	if (sky.paint <= 0.001) return null;
	return <mesh geometry={geo} material={mat} position={[0, sky.y, 0]} scale={sky.r} renderOrder={-1} frustumCulled={false} />;
};

// ---------------------------------------------------------------- the real falling star

const STAR_BOX = new THREE.BoxGeometry(1, 1, 1);
const STAR_M = [
	new THREE.MeshBasicMaterial({color: '#ffffff', fog: false}),
	new THREE.MeshBasicMaterial({color: '#fff3c4', fog: false}),
	new THREE.MeshBasicMaterial({color: '#ffd36a', fog: false}),
	new THREE.MeshBasicMaterial({color: '#ff9f4a', fog: false}),
];
const HALO_M = new THREE.MeshBasicMaterial({color: '#fff3c4', transparent: true, opacity: 0.35, depthWrite: false, fog: false});

/** A star falling from `from` to `to` as `fall` runs 0..1 (accelerating), trailing a tail of glowing voxels. */
export const FallingStar: React.FC<{star: NonNullable<SkyNow['star']>}> = ({star}) => {
	const p = star.fall;
	if (p <= 0.001 || p >= 0.999) return null;
	const at = (q: number) => {
		const e = Math.max(0, q) ** 1.5;
		return [0, 1, 2].map((i) => star.from[i] + (star.to[i] - star.from[i]) * e) as [number, number, number];
	};
	const head = at(p);
	return (
		<group>
			<mesh geometry={STAR_BOX} material={HALO_M} position={head} scale={5.5} />
			<mesh geometry={STAR_BOX} material={STAR_M[0]} position={head} scale={2.6} />
			{Array.from({length: 22}, (_, k) => {
				const q = p - (k + 1) * 0.016;
				if (q <= 0) return null;
				const s = Math.max(0.35, 2.1 - k * 0.08);
				return <mesh key={k} geometry={STAR_BOX} material={STAR_M[Math.min(3, Math.floor(k / 5) + (k > 2 ? 1 : 0))]} position={at(q)} scale={s} />;
			})}
		</group>
	);
};

// ---------------------------------------------------------------- the ground's proof: a giant's bones, a ruin

const BONE_BOX = new THREE.BoxGeometry(1, 1, 1);
const BONE_M = new THREE.MeshLambertMaterial({color: '#e8dec4'});
const BONE_M2 = new THREE.MeshLambertMaterial({color: '#cbbd9c'});
const SOCKET_M = new THREE.MeshLambertMaterial({color: '#2a2420'});
const TRENCH_M = new THREE.MeshLambertMaterial({color: '#3e2c1e'});
const TRENCH_RIM_M = new THREE.MeshLambertMaterial({color: '#6b4e32'});
type Part = [number, number, number, number, number, number, number?, THREE.Material?];

const SKELETON: Part[] = (() => {
	const out: Part[] = [];
	// the skull (a long-snouted beast, facing +x), its eye sockets and jaw
	out.push([4.3, 0.55, 0, 1.7, 1.05, 1.3], [5.6, 0.38, 0, 1.3, 0.62, 0.86], [4.7, 0.82, 0.48, 0.34, 0.32, 0.3, 0, SOCKET_M], [4.7, 0.82, -0.48, 0.34, 0.32, 0.3, 0, SOCKET_M]);
	out.push([5.1, 0.02, 0, 1.7, 0.26, 0.74, 0, BONE_M2], [3.5, 0.95, 0, 0.5, 0.4, 0.9, 0, BONE_M2]);
	// the spine, gently arched, and its ribs
	for (let k = 0; k < 11; k++) {
		const x = 3.0 - k * 0.62;
		out.push([x, 0.42 + Math.sin((k / 10) * Math.PI) * 0.22, 0, 0.44, 0.42, 0.52, 0, k % 2 ? BONE_M2 : BONE_M]);
	}
	for (let k = 0; k < 7; k++) {
		const x = 2.5 - k * 0.66;
		const L = 0.7 + Math.sin(((k + 0.5) / 7) * Math.PI) * 0.55;
		for (const sd of [1, -1]) {
			out.push([x, 0.62, sd * 0.5, 0.2, 0.2, 0.55], [x, 0.38, sd * (0.72 + L * 0.35), 0.2, 0.55, 0.2], [x, 0.02, sd * (0.85 + L * 0.42), 0.2, 0.4, 0.2, 0, BONE_M2]);
		}
	}
	// the pelvis, four splayed legs, the tail curling away
	out.push([-3.4, 0.36, 0, 0.9, 0.42, 1.5, 0, BONE_M2]);
	for (const [lx, sd] of [[2.1, 1], [2.1, -1], [-3.3, 1], [-3.3, -1]] as [number, number][]) {
		out.push([lx + 0.3, 0.12, sd * 1.5, 0.28, 0.28, 1.5, sd * 0.5], [lx + 1.1, 0.06, sd * 2.4, 0.9, 0.22, 0.24, sd * 0.3, BONE_M2]);
	}
	for (let k = 0; k < 8; k++) out.push([-4.1 - k * 0.55, 0.3 - k * 0.02, Math.sin(k * 0.55) * 0.9, 0.36 - k * 0.025, 0.3 - k * 0.02, 0.36 - k * 0.025, 0, k % 2 ? BONE_M2 : BONE_M]);
	return out;
})();

/** EP34: a giant's skeleton lying in the ground, older than anyone's gods: `rise` 0 buried .. 1 half out of the turf. */
export const Bones: React.FC<{x: number; z: number; face: number; scale?: number; island: Island; rise: number}> = ({x, z, face, scale = 1, island, rise}) => {
	if (rise <= 0.001) return null;
	const y = island.heightAt(x, z);
	const sink = -1.7 * (1 - rise) - 0.22;
	const dug = Math.min(1, rise * 1.6);
	return (
		<group>
			{/* the dig: a trench of dark soil opened along the skeleton, so bone and the crack's light read against it */}
			<group position={[x, y, z]} rotation={[0, (face * Math.PI) / 180, 0]}>
				<mesh geometry={BONE_BOX} material={TRENCH_M} position={[-0.6 * scale, 0.0, 0]} scale={[15.5 * scale * dug, 0.1, 4.6 * scale * dug]} receiveShadow />
				<mesh geometry={BONE_BOX} material={TRENCH_RIM_M} position={[-0.6 * scale, -0.01, 0]} scale={[16.6 * scale * dug, 0.1, 5.6 * scale * dug]} receiveShadow />
			</group>
		<group position={[x, y + sink * scale, z]} rotation={[0, (face * Math.PI) / 180, 0]} scale={scale}>
			{SKELETON.map(([px, py, pz, sx, sy, sz, ry, m], k) => (
				<mesh key={k} geometry={BONE_BOX} material={m ?? BONE_M} position={[px, py, pz]} rotation={[0, ry ?? 0, 0]} scale={[sx, sy, sz]} castShadow receiveShadow />
			))}
		</group>
		</group>
	);
};

const RUIN_M = new THREE.MeshLambertMaterial({color: '#9a9b8e'});
const RUIN_M2 = new THREE.MeshLambertMaterial({color: '#7b7d72'});
const MOSS_M = new THREE.MeshLambertMaterial({color: '#5f7a4a'});
const RUIN: Part[] = [
	[-1.7, 1.25, 0, 0.62, 2.5, 0.62], [-1.7, 2.55, 0, 0.86, 0.16, 0.86, 0, MOSS_M],
	[-0.55, 0.62, 0.25, 0.62, 1.25, 0.62, 0, RUIN_M2], [-0.55, 1.28, 0.25, 0.5, 0.1, 0.5, 0, MOSS_M],
	[0.65, 1.0, -0.15, 0.62, 2.0, 0.62], [0.65, 2.05, -0.15, 0.86, 0.16, 0.86, 0, RUIN_M2],
	[1.8, 0.35, 0.1, 0.62, 0.7, 0.62, 0, RUIN_M2],
	[0.3, 0.18, 1.3, 2.6, 0.36, 0.55, 0.25], [0.2, 0.38, 1.25, 1.2, 0.06, 0.4, 0.25, MOSS_M],
];
/** EP34 (EP35's tease): broken pillars older than anyone, rising out of the ground with `rise` (0 under .. 1 standing). */
export const Ruin: React.FC<{x: number; z: number; face: number; scale?: number; island: Island; rise: number}> = ({x, z, face, scale = 1, island, rise}) => {
	if (rise <= 0.001) return null;
	const y = island.heightAt(x, z) - 2.8 * (1 - rise) * scale;
	return (
		<group position={[x, y, z]} rotation={[0, (face * Math.PI) / 180, 0]} scale={scale}>
			{RUIN.map(([px, py, pz, sx, sy, sz, ry, m], k) => (
				<mesh key={k} geometry={BONE_BOX} material={m ?? RUIN_M} position={[px, py, pz]} rotation={[0, ry ?? 0, 0]} scale={[sx, sy, sz]} castShadow receiveShadow />
			))}
		</group>
	);
};
