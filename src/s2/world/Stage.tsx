// The Season 2 stage: a low-resolution WebGL render of the diorama, upscaled with nearest-neighbour filtering so the
// 3D world reads as crisp pixel art (the "pixel diorama" look), with a camera rig driven by keyframes.
import {ThreeCanvas} from '@remotion/three';
import React from 'react';
import * as THREE from 'three';
import {useThree} from '@react-three/fiber';

export type Cam = {
	/** azimuth in degrees (0 = looking from +z towards -z) */
	az: number;
	/** elevation in degrees above the horizon */
	el: number;
	/** distance from the target */
	dist: number;
	/** look-at target [x, y, z] */
	at: [number, number, number];
	/** vertical field of view (narrow = miniature / diorama feel) */
	fov?: number;
};

export const camPose = (c: Cam) => {
	const az = (c.az * Math.PI) / 180;
	const el = (c.el * Math.PI) / 180;
	const x = c.at[0] + Math.sin(az) * Math.cos(el) * c.dist;
	const z = c.at[2] + Math.cos(az) * Math.cos(el) * c.dist;
	const y = c.at[1] + Math.sin(el) * c.dist;
	return [x, y, z] as [number, number, number];
};

const CameraRig: React.FC<{cam: Cam}> = ({cam}) => {
	const {camera} = useThree();
	const p = camPose(cam);
	camera.position.set(p[0], p[1], p[2]);
	camera.lookAt(cam.at[0], cam.at[1], cam.at[2]);
	const pc = camera as THREE.PerspectiveCamera;
	if (pc.fov !== (cam.fov ?? 24)) {
		pc.fov = cam.fov ?? 24;
	}
	pc.near = 1;
	pc.far = 400;
	pc.updateProjectionMatrix();
	return null;
};

/** Sun direction (unit vector from the scene towards the sun) for an azimuth / elevation in degrees. */
export const sunDir = (az: number, el: number): [number, number, number] => {
	const a = (az * Math.PI) / 180;
	const e = (el * Math.PI) / 180;
	return [Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e)];
};

export const Lights: React.FC<{sun?: number; warm?: number; az?: number; el?: number; hemi?: number}> = ({sun = 1, warm = 0.5, az = 35, el = 49, hemi = 0.95}) => {
	const key = new THREE.Color('#fff1d6').lerp(new THREE.Color('#ffb46e'), warm);
	const d = sunDir(az, el);
	const ref = React.useRef<THREE.DirectionalLight>(null);
	// R3F sets the shadow-camera bounds below but doesn't rebuild the camera's projection; without this the shadow map
	// keeps three.js's default ±5-unit box and nothing more than 5 units from the island's centre casts a shadow.
	React.useLayoutEffect(() => {
		ref.current?.shadow.camera.updateProjectionMatrix();
	});
	return (
		<>
			<hemisphereLight args={['#bcd6ff', '#3a3048', hemi * 0.8]} />
			<directionalLight
				ref={ref}
				color={key}
				intensity={2.5 * sun}
				position={[d[0] * 60, d[1] * 60, d[2] * 60]}
				castShadow
				shadow-mapSize-width={1024}
				shadow-mapSize-height={1024}
				shadow-camera-left={-38}
				shadow-camera-right={38}
				shadow-camera-top={38}
				shadow-camera-bottom={-38}
				shadow-camera-near={1}
				shadow-camera-far={170}
				shadow-bias={-0.0015}
			/>
		</>
	);
};

type StageProps = {
	cam: Cam;
	/** output pixels per rendered pixel (3 => 360x640 render for a 1080x1920 frame) */
	pixel?: number;
	width?: number;
	height?: number;
	children: React.ReactNode;
	background?: string;
	/** drawn behind the 3D canvas (e.g. the pixel starfield) */
	backdrop?: React.ReactNode;
};

export const Stage: React.FC<StageProps> = ({cam, pixel = 3, width = 1080, height = 1920, children, background, backdrop}) => {
	const w = Math.round(width / pixel);
	const h = Math.round(height / pixel);
	return (
		<div style={{position: 'absolute', inset: 0, background: background ?? 'transparent', overflow: 'hidden'}}>
			{backdrop}
			<div style={{position: 'absolute', left: 0, top: 0, width: w, height: h, transform: `scale(${pixel})`, transformOrigin: '0 0', imageRendering: 'pixelated'}}>
				<ThreeCanvas
					width={w}
					height={h}
					dpr={1}
					shadows="basic"
					gl={{antialias: false, alpha: true, preserveDrawingBuffer: true, powerPreference: 'high-performance'}}
					camera={{fov: cam.fov ?? 24, position: [0, 30, 60]}}
					style={{imageRendering: 'pixelated'}}
				>
					<CameraRig cam={cam} />
					{children}
				</ThreeCanvas>
			</div>
		</div>
	);
};
