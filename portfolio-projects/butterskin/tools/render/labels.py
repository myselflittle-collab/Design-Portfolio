"""Botanical Luxury pack labels: transparent PNG decals that render.py prints onto each pack. Uses the lotus emblem from tools/brand.py."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from brand import emblem
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); F = f"file://{ROOT}/prototype/assets/fonts/"
CSS = f"""@font-face{{font-family:P;font-weight:400;src:url({F}playfair-display-latin-400-normal.woff2)}}
@font-face{{font-family:P;font-weight:500;src:url({F}playfair-display-latin-500-normal.woff2)}}@font-face{{font-family:P;font-weight:600;src:url({F}playfair-display-latin-600-normal.woff2)}}
@font-face{{font-family:I;font-weight:400;src:url({F}inter-latin-400-normal.woff2)}}@font-face{{font-family:I;font-weight:500;src:url({F}inter-latin-500-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{background:transparent}}
.l{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--ink)}}
.em{{width:calc(var(--s)*3.6px);height:calc(var(--s)*3.6px);margin-bottom:calc(var(--s)*1.0px)}}
.brand{{font:500 calc(var(--s)*1.18px)/1 P;letter-spacing:.26em;margin-right:-.26em}}
.name{{font:500 calc(var(--s)*2.4px)/1.08 P;margin-top:calc(var(--s)*1.5px)}}
.rule{{width:calc(var(--s)*2.6px);height:calc(var(--s)*.1px);background:var(--acc);margin:calc(var(--s)*1.25px) 0}}
.ing{{font:500 calc(var(--s)*.78px)/1.45 I;letter-spacing:.05em}}
.size{{font:500 calc(var(--s)*.7px)/1.5 I;letter-spacing:.2em;margin-right:-.2em;margin-top:calc(var(--s)*1.1px)}}
"""
def label(page, out, w, h, ink, acc, s, name, ing, size, emb=True):
    em = f'<svg class="em" viewBox="0 0 100 100">{emblem(acc, 100, 3.2)}</svg>' if emb else ""
    html = f"""<html><head><style>{CSS}</style></head><body><div class="l" style="width:{w}px;height:{h}px;--ink:{ink};--acc:{acc};--s:{s}">
    {em}<div class="brand">BUTTERSKIN</div><div class="name">{name}</div><div class="rule"></div><div class="ing">{ing}</div><div class="size">{size} · CONCEPT</div></div></body></html>"""
    tmp = os.path.abspath(out + ".html"); open(tmp, "w").write(html)
    page.set_viewport_size({"width": w, "height": h}); page.goto("file://" + tmp); page.evaluate("document.fonts.ready"); page.wait_for_timeout(120)
    page.screenshot(path=out, omit_background=True); os.remove(tmp)
if __name__ == "__main__":
    specs = json.load(open(sys.argv[1]))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for sp in specs: label(pg, **sp)
        b.close()
