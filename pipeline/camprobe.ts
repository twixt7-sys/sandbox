// Camera probe for Season 2 poses: where named points land in the 1080×1920 frame, and whether the line of sight from
// the camera to its target clears the Isle's terrain and trees. Plan every pose with it before rendering a still: EP30
// and EP31 lost several rounds to cameras that looked into hills, trees, or older episodes' landmarks.
//
// Build once, then run with a JSON spec (the same az / el / dist / target / fov as a camera key in make_epNN.py):
//   npx esbuild pipeline/camprobe.ts --bundle --platform=node --log-level=warning --outfile=out/camprobe.cjs
//   node out/camprobe.cjs '{"cams": [{"name": "hook", "az": 0, "el": 9, "dist": 76, "target": [18, 8.6, 1.5], "fov": 15}],
//                           "points": [["statue", 18, 1.5, 3], ["dais", 9.4, -2.2], ["cairn", 8.95, -5.38]]}'
// Points are [name, x, z, height above the ground (default 1), "abs" (optional, EP34+: the height is world y, e.g. a
// point on the painted dome)]. Output per camera: its position and height above the
// ground, the tightest clearance along the line of sight (and what causes it), then each point as (x, y) in output
// pixels and its distance, marked "out" when it falls outside the frame.
import * as THREE from 'three';
import {isle} from '../src/s2/world/island';
import {camPose} from '../src/s2/world/Stage';

type Spec = {cams: {name?: string; az: number; el: number; dist: number; target: [number, number, number]; fov?: number}[]; points?: [string, number, number, number?, string?][]};

const I = isle();
const spec: Spec = JSON.parse(process.argv[2] ?? '{"cams": []}');
for (const c of spec.cams) {
	const target = c.target;
	const p = camPose({az: c.az, el: c.el, dist: c.dist, at: target, fov: c.fov ?? 24});
	// line of sight: sample the segment camera → target; clearance is height above the ground or above a tree's top
	let worst = {k: 0, clear: Infinity, what: 'ground'};
	for (let k = 0.02; k < 0.98; k += 0.01) {
		const x = p[0] + (target[0] - p[0]) * k;
		const y = p[1] + (target[1] - p[1]) * k;
		const z = p[2] + (target[2] - p[2]) * k;
		let clear = y - I.heightAt(x, z);
		let what = 'ground';
		for (const t of I.trees) {
			if (Math.hypot(t.x - x, t.z - z) < 1.3 && y - (t.y + t.h) < clear) {
				clear = y - (t.y + t.h);
				what = `tree (${t.x.toFixed(1)}, ${t.z.toFixed(1)})`;
			}
		}
		if (clear < worst.clear) worst = {k, clear, what};
	}
	const cam = new THREE.PerspectiveCamera(c.fov ?? 24, 1080 / 1920, 1, 400);
	cam.position.set(p[0], p[1], p[2]);
	cam.lookAt(target[0], target[1], target[2]);
	cam.updateMatrixWorld();
	cam.updateProjectionMatrix();
	const row = [
		`${c.name ?? 'cam'}: at (${p.map((v) => v.toFixed(1)).join(', ')}), ${(p[1] - I.heightAt(p[0], p[2])).toFixed(1)} above the ground;`,
		`line of sight clears by ${worst.clear.toFixed(1)} at ${Math.round(worst.k * 100)}% (${worst.what})${worst.clear < 0 ? ' BLOCKED' : ''}`,
	];
	for (const [name, x, z, hy, abs] of spec.points ?? []) {
		const y = abs === 'abs' ? (hy ?? 0) : I.heightAt(x, z) + (hy ?? 1);
		const v = new THREE.Vector3(x, y, z).project(cam);
		const inFrame = Math.abs(v.x) <= 1 && Math.abs(v.y) <= 1 && v.z < 1;
		row.push(`  ${name} (${Math.round((v.x + 1) * 540)}, ${Math.round((1 - v.y) * 960)}) d ${Math.hypot(x - p[0], y - p[1], z - p[2]).toFixed(0)}${inFrame ? '' : ' out'}`);
	}
	console.log(row.join('\n'));
}
