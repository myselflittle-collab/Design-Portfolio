#!/bin/sh
# Renders every ButterSkin product image, then installs them as JPGs. About 75 minutes on 2 CPU cores.
# Run from the butterskin folder:  sh tools/render/render_all.sh   (needs: pip install bpy==5.2.3, playwright)
set -e
OUT=${OUT:-/tmp/butterskin-renders}; mkdir -p "$OUT"
R="python3 tools/render/render.py"
IDS="dewdrop-hydration-serum soft-gel-cleanser butter-balm-cream daylight-spf-50 still-water-essence cloud-milk-cleanser quiet-night-oil soft-cloud-moisturiser"
RELABEL=1 $R range "$OUT/range.png" 1600 32
$R hero "$OUT/hero.png" 1440 32
$R detail "$OUT/detail.png" 1200 32
for p in $IDS; do $R pack:$p "$OUT/pack-$p.png" 720 32; $R scene:$p "$OUT/scene-$p.png" 720 32; $R texture:$p "$OUT/texture-$p.png" 720 32; done
python3 tools/render/install.py "$OUT"
