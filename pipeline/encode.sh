#!/usr/bin/env bash
# Delivery encodes from the master, all with the master's audio copied (-c:a copy), each checked by qa.py.
# Usage: pipeline/encode.sh ep26 [download_kbps] [player_kbps]   (default 1600k: with the master's 256k AAC copied, a 60 s episode stays under the 15 MB page-file limit; 1900k would be ~16.3 MB)
set -euo pipefail
EP="$1"; KB="${2:-1600}"
cd "$(dirname "$0")/.."
M="out/$EP.mp4"
# compat: H.264 Main, CRF 20, faststart
ffmpeg -y -v error -i "$M" -c:v libx264 -profile:v main -pix_fmt yuv420p -crf 20 -preset slow -movflags +faststart -c:a copy "out/${EP}_compat.mp4"
# download: two-pass near-master, passlog before the output on both passes
ffmpeg -y -v error -i "$M" -c:v libx264 -pix_fmt yuv420p -b:v "${KB}k" -preset slow -pass 1 -passlogfile "out/${EP}_2pass" -an -f mp4 /dev/null
ffmpeg -y -v error -i "$M" -c:v libx264 -pix_fmt yuv420p -b:v "${KB}k" -preset slow -pass 2 -passlogfile "out/${EP}_2pass" -movflags +faststart -c:a copy "out/${EP}_download.mp4"
rm -f out/${EP}_2pass*
# player: lighter two-pass copy for the page's <video> (uploaded as an asset). At 60 s a CRF-26 pixel-art render is
# ~25 MB, over the asset cap, so Season 2 uses two-pass 1300k (~12 MB).
PK="${3:-1300}"
ffmpeg -y -v error -i "$M" -c:v libx264 -pix_fmt yuv420p -b:v "${PK}k" -preset slow -pass 1 -passlogfile "out/${EP}_2pass_player" -an -f mp4 /dev/null
ffmpeg -y -v error -i "$M" -c:v libx264 -pix_fmt yuv420p -b:v "${PK}k" -preset slow -pass 2 -passlogfile "out/${EP}_2pass_player" -movflags +faststart -c:a copy "out/${EP}_player.mp4"
rm -f out/${EP}_2pass_player*
ls -la out/${EP}.mp4 out/${EP}_compat.mp4 out/${EP}_download.mp4 out/${EP}_player.mp4
