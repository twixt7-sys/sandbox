// Render selected frames of an episode as JPEG stills in one browser session (bundles once).
// Usage: node pipeline/stills.mjs ep26 out/ep26_beats 0.5 4.2 9.8 ...   (times in seconds)
// Season 2 episodes need WebGL: this uses the software 'swangle' renderer, which works in a GPU-less container.
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition, ensureBrowser} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';

const [, , ep, outDir, ...times] = process.argv;
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const browserExecutable = process.env.REMOTION_BROWSER ?? '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.join(root, 'src/index.ts'), publicDir: path.join(root, 'public')});
const inputProps = {episodeId: ep};
const chromiumOptions = {gl: 'swangle'};
const composition = await selectComposition({serveUrl, id: 'Episode', inputProps, browserExecutable, chromiumOptions});
for (const ts of times) {
	const frame = Math.min(composition.durationInFrames - 1, Math.round(parseFloat(ts) * composition.fps));
	const output = path.join(outDir, `${ep}_${String(frame).padStart(4, '0')}.jpg`);
	const t0 = Date.now();
	await renderStill({serveUrl, composition, frame, output, inputProps, browserExecutable, chromiumOptions, imageFormat: 'jpeg', jpegQuality: 90});
	console.log(`[stills] ${ts}s -> ${output} (${Date.now() - t0} ms)`);
}
