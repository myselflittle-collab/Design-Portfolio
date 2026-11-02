"""Installs rendered PNGs as JPGs: prototype/assets/products, prototype/assets/photo and design/brand/packaging/renders.
python3 tools/render/install.py <folder with render PNGs>"""
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = sys.argv[1]
PR, PH, DS = f"{ROOT}/prototype/assets/products", f"{ROOT}/prototype/assets/photo", f"{ROOT}/design/brand/packaging/renders"
for d in (PR, PH, DS): os.makedirs(d, exist_ok=True)
n = 0
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".png"): continue
    im = Image.open(f"{SRC}/{f}").convert("RGB"); name = f[:-4]
    im.save(f"{DS}/{name}.jpg", quality=90, optimize=True)
    for pre, suf in (("pack-", ""), ("scene-", "-scene"), ("texture-", "-texture")):
        if name.startswith(pre):
            im.save(f"{PR}/{name[len(pre):]}{suf}.jpg", quality=84, optimize=True, progressive=True); break
    else:
        w = 1600 if name in ("hero", "range") else 1200
        if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(f"{PH}/{name}.jpg", quality=84, optimize=True, progressive=True)
    n += 1
print("installed", n, "renders")
