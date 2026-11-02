"""ButterSkin brand builder · Botanical Luxury (approved Option 1).
Writes design tokens (JSON + CSS, with a WCAG contrast table), the lotus emblem, logo lockups and app icon (all type outlined).
Product images are 3D renders made separately by tools/render/ (Blender Cycles).
Run from the butterskin folder:  python3 tools/brand.py
Needs: fontTools, brotli, uharfbuzz. Fonts are read from prototype/assets/fonts (Playfair Display and Inter, SIL OFL 1.1)."""
import io, json, os, shutil
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = f"{ROOT}/prototype/assets/fonts"

# ------------------------------------------------------------------ tokens
# Core Option 1 colours: Deep Emerald #0E4A38, Sage #7F9F86, Ivory #FAF8F4, Champagne #C9AA6B, Charcoal #1F2A24.
PALETTE = {
    "ivory": {"0": "#FFFFFF", "50": "#FAF8F4", "100": "#F3EFE7", "200": "#E6DFD2"},
    "charcoal": {"900": "#1F2A24", "700": "#38433D", "600": "#56605A", "400": "#8A928D"},
    "emerald": {"900": "#0A3729", "800": "#0E4A38", "700": "#155C46", "100": "#E2ECE6"},
    "sage": {"100": "#EDF2EC", "200": "#D9E3D9", "300": "#B7CBBB", "500": "#7F9F86"},
    "champagne": {"200": "#EFE3C8", "400": "#C9AA6B", "700": "#7A5E28"},
    "stone": {"200": "#ECE6DB", "300": "#D8CFC0"},
    "status": {"error-fg": "#A3261C", "error-bg": "#FBE3DF", "success-fg": "#0E4A38", "success-bg": "#E2ECE6"},
}
CORE = [("Deep Emerald", "emerald.800", "Primary · actions, headlines, glass"), ("Sage Green", "sage.500", "Secondary · surfaces and illustration"),
        ("Ivory", "ivory.50", "Background"), ("Champagne", "champagne.400", "Accent · caps, rules, emblem"), ("Charcoal", "charcoal.900", "Text")]
CATEGORY = {"cleanse": ("sage", "100"), "treat": ("emerald", "100"), "moisturise": ("ivory", "100"), "protect": ("champagne", "200")}
SEMANTIC = {
    "bg-canvas": "ivory.50", "bg-surface": "ivory.0", "bg-sunken": "ivory.100", "border": "ivory.200", "border-strong": "charcoal.400",
    "text-primary": "charcoal.900", "text-secondary": "charcoal.700", "text-muted": "charcoal.600",
    "action": "emerald.800", "action-hover": "emerald.700", "action-pressed": "emerald.900", "on-action": "ivory.0",
    "link": "emerald.800", "focus": "champagne.700", "accent": "champagne.400", "accent-text": "champagne.700",
    "surface-secondary": "sage.200", "surface-tint": "sage.100", "surface-photo": "stone.200",
}
TYPE = {
    "display": ("Playfair Display", 400, 46, 52, -0.01), "h1": ("Playfair Display", 400, 34, 40, -0.01), "h2": ("Playfair Display", 400, 26, 32, 0),
    "h3": ("Playfair Display", 500, 20, 26, 0), "body": ("Inter", 400, 16, 25, 0), "body-sm": ("Inter", 400, 14, 21, 0),
    "label": ("Inter", 500, 14, 18, 0), "button": ("Inter", 600, 13, 16, 0.1), "caption": ("Inter", 400, 13, 18, 0),
    "eyebrow": ("Inter", 500, 12, 16, 0.16),
}
SPACE = [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64]
RADIUS = {"control": 2, "card": 4, "media": 4, "sheet": 12}


def hexval(ref):
    g, k = ref.split(".")
    return PALETTE[g][k]


def lum(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + 0.05) / (y + 0.05)


PAIRS = [("Body text on ivory", "charcoal.900", "ivory.50", 4.5), ("Secondary text on ivory", "charcoal.700", "ivory.50", 4.5),
         ("Muted text on ivory", "charcoal.600", "ivory.50", 4.5), ("Muted text on sunken ivory", "charcoal.600", "ivory.100", 4.5),
         ("Muted text on sage tint", "charcoal.600", "sage.100", 4.5), ("Muted text on sage 200", "charcoal.600", "sage.200", 4.5),
         ("Muted text on champagne tint", "charcoal.600", "champagne.200", 4.5), ("Muted text on photo stone", "charcoal.600", "stone.200", 4.5),
         ("Button label on emerald", "ivory.0", "emerald.800", 4.5), ("Button label on emerald hover", "ivory.0", "emerald.700", 4.5),
         ("Ivory text on emerald 900", "ivory.50", "emerald.900", 4.5), ("Emerald link on white", "emerald.800", "ivory.0", 4.5),
         ("Emerald on sage 200", "emerald.800", "sage.200", 4.5), ("Champagne text on white", "champagne.700", "ivory.0", 4.5),
         ("Champagne text on ivory", "champagne.700", "ivory.50", 4.5), ("Error text", "status.error-fg", "status.error-bg", 4.5),
         ("Success text", "status.success-fg", "status.success-bg", 4.5), ("Champagne 400 on emerald (large text, emblem)", "champagne.400", "emerald.800", 3.0),
         ("Focus ring on ivory (3:1)", "champagne.700", "ivory.50", 3.0), ("Control border on white (3:1)", "charcoal.400", "ivory.0", 3.0)]
DECORATIVE = [("Sage 500 on ivory", "sage.500", "ivory.50"), ("Champagne 400 on ivory", "champagne.400", "ivory.50")]


def contrast_rows():
    return [(n, hexval(f), hexval(b), round(contrast(hexval(f), hexval(b)), 2), m) for n, f, b, m in PAIRS]


def write_tokens():
    os.makedirs(f"{ROOT}/design/tokens", exist_ok=True)
    data = {"$description": "ButterSkin design tokens, Botanical Luxury (fictional concept). px unless noted.",
            "color": {"palette": PALETTE, "core": [{"name": n, "ref": r, "value": hexval(r), "role": u} for n, r, u in CORE],
                      "semantic": {k: {"ref": v, "value": hexval(v)} for k, v in SEMANTIC.items()},
                      "category": {k: hexval(".".join(v)) for k, v in CATEGORY.items()}},
            "typography": {k: {"family": f, "weight": w, "size": s, "lineHeight": lh, "trackingEm": t} for k, (f, w, s, lh, t) in TYPE.items()},
            "space": SPACE, "radius": RADIUS,
            "contrast": [{"pair": n, "fg": f, "bg": b, "ratio": r, "min": m, "pass": r >= m} for n, f, b, r, m in contrast_rows()],
            "decorative_only": [{"pair": n, "ratio": round(contrast(hexval(a), hexval(b)), 2)} for n, a, b in DECORATIVE]}
    json.dump(data, open(f"{ROOT}/design/tokens/tokens.json", "w"), indent=2)
    css = ["/* ButterSkin tokens (Botanical Luxury). Generated by tools/brand.py. */"]
    faces = [("Playfair Display", 400, "normal", "playfair-display-latin-400-normal"), ("Playfair Display", 500, "normal", "playfair-display-latin-500-normal"),
             ("Playfair Display", 600, "normal", "playfair-display-latin-600-normal"), ("Playfair Display", 400, "italic", "playfair-display-latin-400-italic"),
             ("Inter", 400, "normal", "inter-latin-400-normal"), ("Inter", 500, "normal", "inter-latin-500-normal"), ("Inter", 600, "normal", "inter-latin-600-normal")]
    for fam, w, st, f in faces:
        css.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};font-display:swap;src:url('fonts/{f}.woff2') format('woff2')}}")
    for w in (400, 500, 600):  # latin-ext subset supplies the rupee sign and accented letters
        css.append(f"@font-face{{font-family:'Inter';font-style:normal;font-weight:{w};font-display:swap;src:url('fonts/inter-latin-ext-{w}-normal.woff2') format('woff2');unicode-range:U+0100-024F,U+20A0-20C0}}")
    css.append(":root{")
    for g, sh in PALETTE.items():
        for k, v in sh.items():
            css.append(f"  --bs-{g}-{k}:{v};")
    for k, v in SEMANTIC.items():
        css.append(f"  --bs-{k}:var(--bs-{v.replace('.', '-')});")
    for k, v in CATEGORY.items():
        css.append(f"  --bs-cat-{k}:var(--bs-{v[0]}-{v[1]});")
    for i, v in enumerate(SPACE):
        css.append(f"  --bs-space-{i}:{v}px;")
    for k, v in RADIUS.items():
        css.append(f"  --bs-radius-{k}:{v}px;")
    css += ["  --bs-font-display:'Playfair Display',Didot,Georgia,serif;", "  --bs-font-text:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;", "}"]
    for k, (f, w, s, lh, t) in TYPE.items():
        fam = "var(--bs-font-display)" if f.startswith("Playfair") else "var(--bs-font-text)"
        up = "text-transform:uppercase;" if k in ("eyebrow", "button") else ""
        css.append(f".bs-{k}{{font-family:{fam};font-weight:{w};font-size:{s}px;line-height:{lh}px;letter-spacing:{t}em;{up}}}")
    open(f"{ROOT}/design/tokens/tokens.css", "w").write("\n".join(css).replace("url('fonts/", "url('../../prototype/assets/fonts/") + "\n")
    open(f"{ROOT}/prototype/assets/tokens.css", "w").write("\n".join(css) + "\n")


# ------------------------------------------------------------------ outlined type
_c = {}


def _font(name):
    if name not in _c:
        tt = TTFont(f"{FONTS}/{name}.woff2"); tt.flavor = None
        b = io.BytesIO(); tt.save(b)
        f = hb.Font(hb.Face(b.getvalue())); _c[name] = (f, tt, tt.getGlyphSet(), tt["head"].unitsPerEm)
    return _c[name]


def text_path(text, fname, size, x=0, y=0, track=0.0):
    font, tt, gs, upem = _font(fname)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf, {"kern": True})
    order = tt.getGlyphOrder(); s = size / upem; pen = SVGPathPen(gs); cx = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gs[order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + cx * s, y)))
        cx += pos.x_advance + track * upem
    return pen.getCommands(), (cx - track * upem) * s


def centered(text, fname, size, cx, y, fill, track=0.0):
    _, w = text_path(text, fname, size, 0, 0, track)
    d, _ = text_path(text, fname, size, cx - w / 2, y, track)
    return f'<path d="{d}" fill="{fill}"/>', w


PF, IN5 = "playfair-display-latin-400-normal", "inter-latin-500-normal"


# ------------------------------------------------------------------ emblem: an original line-drawn lotus
def petal(L, w, ang, cx, cy, tip=0.30):
    p = (f"M0 0 C{w * .95:.2f} {-L * .18:.2f} {w:.2f} {-L * .62:.2f} {w * tip:.2f} {-L * .93:.2f} "
         f"Q0 {-L * 1.02:.2f} {-w * tip:.2f} {-L * .93:.2f} C{-w:.2f} {-L * .62:.2f} {-w * .95:.2f} {-L * .18:.2f} 0 0Z")
    return p, f"translate({cx} {cy}) rotate({ang})"


def emblem(stroke, size=100, sw=2.7):
    """Centre petal, two side petals, two low leaves and a water line, drawn in a 100 x 100 box."""
    parts = [(30, 10.5, -78, .22), (30, 10.5, 78, .22), (45, 13.5, -38, .26), (45, 13.5, 38, .26), (60, 15.5, 0, .26)]
    shapes = "".join(f'<path d="{p}" transform="{t}"/>' for p, t in (petal(L, w, a, 50, 82, tp) for L, w, a, tp in parts))
    return (f'<g transform="scale({size / 100})" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">'
            f'{shapes}<path d="M50 78 L50 38"/><path d="M26 91 Q50 97 74 91"/></g>')


def svg(vb, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>'


EM, CH, CH7, IV, INK = PALETTE["emerald"]["800"], PALETTE["champagne"]["400"], PALETTE["champagne"]["700"], PALETTE["ivory"]["50"], PALETTE["charcoal"]["900"]


def lockup(mark, word, tag, bg=None, stacked=True, tagline=True):
    if stacked:
        W = 560; wm, _ = centered("BUTTERSKIN", PF, 58, W / 2, 196, word, .2)
        tg = centered("BOTANICAL SKINCARE", IN5, 15.5, W / 2, 236, tag, .34)[0] if tagline else ""
        body = f'<g transform="translate({W / 2 - 52} 6)">{emblem(mark, 104)}</g>{wm}{tg}'; vb = [0, 0, W, 256 if tagline else 214]
    else:
        _, ww = text_path("BUTTERSKIN", PF, 50, 0, 0, .2); x0 = 104
        wd, _ = text_path("BUTTERSKIN", PF, 50, x0, 62 if tagline else 70, .2)
        body = f'<g transform="translate(0 4)">{emblem(mark, 92)}</g><path d="{wd}" fill="{word}"/>'
        if tagline:
            _, tw = text_path("BOTANICAL SKINCARE", IN5, 13, 0, 0, .34)
            td, _ = text_path("BOTANICAL SKINCARE", IN5, 13, x0 + (ww - tw) / 2, 94, .34); body += f'<path d="{td}" fill="{tag}"/>'
        vb = [0, 0, round(x0 + ww + 4, 1), 104]
    if bg:
        x, y, w, h = vb; body = f'<rect x="{x - 32}" y="{y - 28}" width="{w + 64}" height="{h + 56}" fill="{bg}"/>' + body; vb = [x - 32, y - 28, w + 64, h + 56]
    return svg(" ".join(map(str, vb)), body, "ButterSkin logo")


def write_logos():
    L, A = f"{ROOT}/design/brand/logo", f"{ROOT}/design/brand/app-icon"
    for d in (L, A):
        if os.path.isdir(d): shutil.rmtree(d)
        os.makedirs(d)
    files = {
        f"{L}/butterskin-emblem.svg": svg("0 0 100 100", emblem(EM), "ButterSkin emblem"),
        f"{L}/butterskin-emblem-champagne.svg": svg("0 0 100 100", emblem(CH), "ButterSkin emblem"),
        f"{L}/butterskin-emblem-ivory.svg": svg("0 0 100 100", emblem(IV), "ButterSkin emblem"),
        f"{L}/butterskin-lockup-stacked.svg": lockup(EM, INK, CH7),
        f"{L}/butterskin-lockup-stacked-dark.svg": lockup(CH, IV, CH, bg=EM),
        f"{L}/butterskin-lockup-stacked-reverse.svg": lockup(CH, IV, CH),
        f"{L}/butterskin-lockup-horizontal.svg": lockup(EM, INK, CH7, stacked=False),
        f"{L}/butterskin-lockup-horizontal-dark.svg": lockup(CH, IV, CH, bg=EM, stacked=False),
        f"{L}/butterskin-lockup-compact.svg": lockup(EM, INK, CH7, stacked=False, tagline=False),
        f"{L}/butterskin-wordmark.svg": svg("0 0 600 96", centered("BUTTERSKIN", PF, 58, 300, 70, INK, .2)[0], "ButterSkin wordmark"),
        f"{A}/app-icon-1024.svg": svg("0 0 1024 1024", f'<rect width="1024" height="1024" fill="{EM}"/><g transform="translate(262 236)">{emblem(CH, 500)}</g>', "ButterSkin app icon"),
        f"{A}/app-icon-rounded-preview.svg": svg("0 0 1024 1024", f'<rect width="1024" height="1024" rx="230" fill="{EM}"/><g transform="translate(262 236)">{emblem(CH, 500)}</g>', "ButterSkin app icon"),
    }
    for p, s in files.items():
        open(p, "w").write(s)
    PA = f"{ROOT}/prototype/assets"
    for old in os.listdir(PA):
        if old.startswith("logo-") and old.endswith(".svg"): os.remove(f"{PA}/{old}")
    shutil.copy(f"{L}/butterskin-lockup-stacked.svg", f"{PA}/logo-lockup.svg")
    shutil.copy(f"{L}/butterskin-lockup-compact.svg", f"{PA}/logo-header.svg")
    shutil.copy(f"{L}/butterskin-emblem.svg", f"{PA}/logo-mark.svg")
    shutil.copy(f"{L}/butterskin-lockup-stacked-reverse.svg", f"{PA}/logo-lockup-reverse.svg")
    return len(files)


if __name__ == "__main__":
    write_tokens()
    n = write_logos()
    rows = contrast_rows()
    print(f"tokens written; {sum(r >= m for *_, r, m in rows)}/{len(rows)} contrast pairs pass; {n} logo files")
