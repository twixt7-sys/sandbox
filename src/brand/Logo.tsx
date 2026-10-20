import React, {createContext, useContext} from 'react';
import {AbsoluteFill, Img, interpolate, staticFile} from 'remotion';
import type {Brand} from '../types';

/** Series brand, provided once by the episode composition. */
export const BrandContext = createContext<Brand | undefined>(undefined);
export const useBrand = () => useContext(BrandContext);

/** The series logo, unaltered (designed for dark backgrounds). */
export const Logo: React.FC<{brand: Brand; height: number; style?: React.CSSProperties}> = ({brand, height, style}) => (
	<Img
		src={staticFile(brand.logo)}
		style={{height, width: height * brand.logoAspect, filter: 'drop-shadow(0 2px 10px rgba(0,0,0,0.55))', ...style}}
	/>
);

/**
 * Persistent corner logo, inside the top-left safe area. Series default for every episode;
 * shots can opt out with `hideLogoBug` (the end card shows the full logo instead).
 */
export const LogoBug: React.FC<{brand: Brand; t: number; hidden: [number, number][]}> = ({brand, t, hidden}) => {
	if (!brand.bug.enabled) return null;
	const o = hidden.reduce(
		(acc, [a, b]) => Math.min(acc, interpolate(t, [a - 0.3, a, b, b + 0.3], [1, 0, 0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})),
		1,
	);
	if (o <= 0) return null;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: brand.bug.x, top: brand.bug.y, opacity: brand.bug.opacity * o}}>
				<Logo brand={brand} height={brand.bug.height} />
			</div>
		</AbsoluteFill>
	);
};
