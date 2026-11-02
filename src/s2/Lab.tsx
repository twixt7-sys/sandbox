// Season 2 style lab: a standalone composition for testing the diorama look (not used by episodes).
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {isle} from './world/island';
import {IslandMesh} from './world/IslandMesh';
import {Lights, Stage} from './world/Stage';

export const S2Lab: React.FC<{pixel?: number}> = ({pixel = 3}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const island = isle();
	return (
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, #1b2b4a 0%, #0d1a33 45%, #070e1e 100%)'}}>
			<Stage pixel={pixel} cam={{az: 30 + t * 6, el: 32, dist: 150, at: [0, -3, 0], fov: 24}}>
				<Lights />
				<IslandMesh island={island} t={t} />
			</Stage>
		</AbsoluteFill>
	);
};
