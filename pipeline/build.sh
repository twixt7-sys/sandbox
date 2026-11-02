#!/usr/bin/env bash
# Audio + timing build for one episode. Usage: pipeline/build.sh ep01 [--provider elevenlabs]
set -euo pipefail
EP="$1"; shift || true
cd "$(dirname "$0")"
python tts.py "$EP" "$@"
python score.py "$EP"
python mix.py "$EP"
mkdir -p ../public/"$EP"
cp ../episodes/"$EP"/episode.json ../public/"$EP"/episode.json
cp ../series/series.json ../public/series.json
rm -rf ../public/"$EP"/plates
[ -d ../episodes/"$EP"/plates ] && cp -r ../episodes/"$EP"/plates ../public/"$EP"/plates
# Season 2 runtime assets (sprites etc.) are copied flat into public/<ep>/.
if [ -d ../episodes/"$EP"/assets ]; then cp -r ../episodes/"$EP"/assets/. ../public/"$EP"/; fi
if [ -f ../episodes/"$EP"/plates.json ]; then cp ../episodes/"$EP"/plates.json ../public/"$EP"/plates.json; else echo '{}' > ../public/"$EP"/plates.json; fi
echo "[build] $EP ready -> public/$EP"
