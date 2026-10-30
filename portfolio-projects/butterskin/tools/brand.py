"""ButterSkin brand builder (Direction B · Porcelain Garden).
Writes design tokens (JSON + CSS), logo SVGs, app icon and studio-lit packaging renders (all type outlined).
Run from the butterskin folder:  python3 tools/brand.py
Needs: fontTools, brotli, uharfbuzz. Fonts are read from prototype/assets/fonts (SIL OFL 1.1)."""
import io, json, os, shutil
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = f"{ROOT}/prototype/assets/fonts"
DATA = json.load(open(f"{ROOT}/data/products.json"))

# ------------------------------------------------------------------ tokens
PALETTE = {
    "porcelain": {"0": "#FFFFFF", "50": "#FCFBF8", "100": "#F4F2EC", "200": "#E6E1D6"},
    "charcoal": {"900": "#262A28", "700": "#3E4441", "600": "#5B605C", "400": "#878C88"},
    "emerald": {"900": "#0F3B2D", "800": "#1B5643", "700": "#23684F", "100": "#E3EDE8"},
    "sage": {"100": "#EEF3EC", "200": "#E5ECE3", "300": "#C7D5C6", "500": "#8FA88F"},
    "champagne": {"200": "#EFE4CC", "400": "#CDB68A", "700": "#7A5E2A"},
    "mist": {"200": "#E4EBEE"},
    "status": {"error-fg": "#A3261C", "error-bg": "#FBE3DF", "success-fg": "#1B5643", "success-bg": "#E3EDE8"},
}
CATEGORY = {"cleanse": ("sage", "200"), "treat": ("champagne", "200"), "moisturise": ("porcelain", "100"), "protect": ("mist", "200")}
SEMANTIC = {
    "bg-canvas": "porcelain.50", "bg-surface": "porcelain.0", "bg-sunken": "porcelain.100", "border": "porcelain.200", "border-strong": "charcoal.400",
    "text-primary": "charcoal.900", "text-secondary": "charcoal.700", "text-muted": "charcoal.600",
    "action": "emerald.800", "action-hover": "emerald.700", "action-pressed": "emerald.900", "on-action": "porcelain.0",
    "link": "emerald.800", "focus": "champagne.700", "accent": "champagne.400", "accent-text": "champagne.700",
    "surface-secondary": "sage.200", "surface-tint": "sage.100",
}
TYPE = {
    "display": ("Bodoni Moda", 400, 48, 54, -0.01), "h1": ("Bodoni Moda", 400, 34, 40, -0.01), "h2": ("Bodoni Moda", 400, 26, 32, 0),
    "h3": ("Bodoni Moda", 500, 20, 26, 0), "body": ("Jost", 400, 16, 25, 0), "body-sm": ("Jost", 400, 14, 21, 0),
    "label": ("Jost", 500, 14, 18, 0.02), "button": ("Jost", 500, 14, 16, 0.12), "caption": ("Jost", 400, 13, 18, 0),
    "eyebrow": ("Jost", 500, 12, 16, 0.18),
}
SPACE = [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64]
RADIUS = {"control": 2, "card": 4, "media": 6, "sheet": 12}


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


PAIRS = [("Primary text on canvas", "charcoal.900", "porcelain.50", 4.5), ("Secondary text on canvas", "charcoal.700", "porcelain.50", 4.5),
         ("Muted text on canvas", "charcoal.600", "porcelain.50", 4.5), ("Muted text on sunken", "charcoal.600", "porcelain.100", 4.5),
         ("Muted text on sage", "charcoal.600", "sage.200", 4.5), ("Muted text on champagne tint", "charcoal.600", "champagne.200", 4.5),
         ("Muted text on mist", "charcoal.600", "mist.200", 4.5), ("Button label on emerald", "porcelain.0", "emerald.800", 4.5),
         ("Button label on emerald hover", "porcelain.0", "emerald.700", 4.5), ("Emerald link on card", "emerald.800", "porcelain.0", 4.5),
         ("Emerald link on sage", "emerald.800", "sage.200", 4.5), ("Champagne text on card", "champagne.700", "porcelain.0", 4.5),
         ("Champagne text on canvas", "champagne.700", "porcelain.50", 4.5), ("Error text", "status.error-fg", "status.error-bg", 4.5),
         ("Success text", "status.success-fg", "status.success-bg", 4.5), ("Charcoal on emerald tint", "charcoal.900", "emerald.100", 4.5),
         ("Focus ring on canvas (3:1)", "champagne.700", "porcelain.50", 3.0), ("Control border on card (3:1)", "charcoal.400", "porcelain.0", 3.0)]


def contrast_rows():
    return [(n, hexval(f), hexval(b), round(contrast(hexval(f), hexval(b)), 2), m) for n, f, b, m in PAIRS]


def write_tokens():
    os.makedirs(f"{ROOT}/design/tokens", exist_ok=True)
    data = {"$description": "ButterSkin design tokens, Direction B · Porcelain Garden (fictional concept). px unless noted.",
            "color": {"palette": PALETTE, "semantic": {k: {"ref": v, "value": hexval(v)} for k, v in SEMANTIC.items()},
                      "category": {k: hexval(".".join(v)) for k, v in CATEGORY.items()}},
            "typography": {k: {"family": f, "weight": w, "size": s, "lineHeight": lh, "trackingEm": t} for k, (f, w, s, lh, t) in TYPE.items()},
            "space": SPACE, "radius": RADIUS,
            "contrast": [{"pair": n, "fg": f, "bg": b, "ratio": r, "min": m, "pass": r >= m} for n, f, b, r, m in contrast_rows()]}
    json.dump(data, open(f"{ROOT}/design/tokens/tokens.json", "w"), indent=2)
    css = ["/* ButterSkin tokens (Porcelain Garden). Generated by tools/brand.py. */", ":root{"]
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
    css += ["  --bs-font-display:'Bodoni Moda',Didot,Georgia,serif;", "  --bs-font-text:'Jost','Rupee',system-ui,sans-serif;", "}"]
    for k, (f, w, s, lh, t) in TYPE.items():
        fam = "var(--bs-font-display)" if f.startswith("Bodoni") else "var(--bs-font-text)"
        up = "text-transform:uppercase;" if k in ("eyebrow", "button") else ""
        css.append(f".bs-{k}{{font-family:{fam};font-weight:{w};font-size:{s}px;line-height:{lh}px;letter-spacing:{t}em;{up}}}")
    open(f"{ROOT}/design/tokens/tokens.css", "w").write("\n".join(css) + "\n")
    shutil.copy(f"{ROOT}/design/tokens/tokens.css", f"{ROOT}/prototype/assets/tokens.css")


# ------------------------------------------------------------------ outlined type
_fonts = {}
SERIF, SERIF_M, SANS, SANS_M = "bodoni-moda-latin-400-normal.woff2", "bodoni-moda-latin-500-normal.woff2", "jost-latin-400-normal.woff2", "jost-latin-500-normal.woff2"


def _font(fname):
    if fname not in _fonts:
        tt = TTFont(f"{FONTS}/{fname}"); tt.flavor = None
        buf = io.BytesIO(); tt.save(buf); data = buf.getvalue()
        font = hb.Font(hb.Face(hb.Blob(data))); tt2 = TTFont(io.BytesIO(data))
        _fonts[fname] = (font, tt2, tt2.getGlyphSet(), tt2["head"].unitsPerEm)
    return _fonts[fname]


def text_path(text, fname, size, x=0, y=0, tracking=0.0):
    font, tt, gs, upem = _font(fname)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    order = tt.getGlyphOrder(); s = size / upem; pen = SVGPathPen(gs); cx = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gs[order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + (cx + pos.x_offset) * s, y - pos.y_offset * s)))
        cx += pos.x_advance + tracking * upem
    return pen.getCommands(), (cx - tracking * upem) * s


def centered(text, fname, size, cx, y, color, tracking=0.0, maxw=None):
    d, w = text_path(text, fname, size, 0, 0, tracking)
    sc = min(1.0, maxw / w) if maxw and w > maxw else 1.0
    return f'<path d="{d}" fill="{color}" transform="translate({cx - w * sc / 2:.2f} {y:.2f}) scale({sc:.4f})"/>'


def glyph_box(ch, fname, size):
    font, tt, gs, upem = _font(fname)
    bp = BoundsPen(gs); gs[tt.getBestCmap()[ord(ch)]].draw(bp)
    s = size / upem; x0, y0, x1, y1 = bp.bounds
    return x0 * s, y0 * s, x1 * s, y1 * s


# ------------------------------------------------------------------ logo
EM, EM9, CH, CH7, INK, WHITE, SAGE = hexval("emerald.800"), hexval("emerald.900"), hexval("champagne.400"), hexval("champagne.700"), hexval("charcoal.900"), "#FFFFFF", hexval("sage.200")


def monogram(cx, cy, r, disc=EM, ring=CH, letter=CH):
    fs = r * 1.25
    x0, y0, x1, y1 = glyph_box("B", SERIF_M, fs)
    d, _ = text_path("B", SERIF_M, fs, cx - (x0 + x1) / 2, cy + (y0 + y1) / 2)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{disc}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.86:.2f}" fill="none" stroke="{ring}" stroke-width="{max(1, r * 0.035):.2f}"/>'
            f'<path d="{d}" fill="{letter}"/>')


def wordmark(x, baseline, size, color=INK):
    d, w = text_path("BUTTERSKIN", SERIF, size, x, baseline, tracking=0.24)
    return f'<path d="{d}" fill="{color}"/>', w


def svg(vb, body, title, w=None, h=None):
    dim = f' width="{w}" height="{h}"' if w else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{dim} role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'


def write_logos():
    L = f"{ROOT}/design/brand/logo"; os.makedirs(L, exist_ok=True)
    for f in os.listdir(L):
        os.remove(f"{L}/{f}")
    open(f"{L}/butterskin-monogram.svg", "w").write(svg("0 0 120 120", monogram(60, 60, 56), "ButterSkin monogram"))
    open(f"{L}/butterskin-monogram-reverse.svg", "w").write(svg("0 0 120 120", monogram(60, 60, 56, WHITE, CH7, EM), "ButterSkin monogram, reverse"))
    open(f"{L}/butterskin-monogram-mono.svg", "w").write(svg("0 0 120 120", monogram(60, 60, 56, INK, WHITE, WHITE), "ButterSkin monogram, one colour"))
    wm, w = wordmark(0, 60, 64)
    open(f"{L}/butterskin-wordmark.svg", "w").write(svg(f"-2 0 {w + 4} 78", wm, "ButterSkin wordmark"))
    wm_l, w = wordmark(130, 72, 56)
    tag = centered("BOTANICAL SKINCARE", SANS_M, 13, 130 + w / 2, 104, hexval("charcoal.600"), tracking=0.32)
    body = monogram(54, 60, 54) + wm_l + tag
    open(f"{L}/butterskin-lockup.svg", "w").write(svg(f"0 0 {130 + w + 6} 120", body, "ButterSkin logo"))
    wm_d, _ = wordmark(130, 72, 56, WHITE)
    tag_d = centered("BOTANICAL SKINCARE", SANS_M, 13, 130 + w / 2, 104, hexval("sage.300"), tracking=0.32)
    open(f"{L}/butterskin-lockup-dark.svg", "w").write(svg(f"-32 -24 {130 + w + 70} 168", f'<rect x="-32" y="-24" width="{130 + w + 70}" height="168" fill="{EM}"/>' + monogram(54, 60, 54, WHITE, CH7, EM) + wm_d + tag_d, "ButterSkin logo, dark"))
    # stacked
    wm_s, ws = wordmark(0, 0, 40)
    stacked = monogram(ws / 2, 52, 46) + f'<g transform="translate(0 150)">{wm_s}</g>' + centered("BOTANICAL SKINCARE", SANS_M, 10.5, ws / 2, 178, hexval("charcoal.600"), tracking=0.32)
    open(f"{L}/butterskin-lockup-stacked.svg", "w").write(svg(f"-4 0 {ws + 8} 190", stacked, "ButterSkin logo, stacked"))
    A = f"{ROOT}/design/brand/app-icon"; os.makedirs(A, exist_ok=True)
    icon = lambda rx: svg("0 0 1024 1024", f'<rect width="1024" height="1024"{rx} fill="{EM}"/>' + f'<circle cx="512" cy="512" r="330" fill="none" stroke="{CH}" stroke-width="10"/>' +
                          (lambda b: f'<path d="{text_path("B", SERIF_M, 520, 512 - (b[0] + b[2]) / 2, 512 + (b[1] + b[3]) / 2)[0]}" fill="{CH}"/>')(glyph_box("B", SERIF_M, 520)),
                          "ButterSkin app icon", 1024, 1024)
    open(f"{A}/app-icon-1024.svg", "w").write(icon(""))
    open(f"{A}/app-icon-rounded-preview.svg", "w").write(icon(' rx="230"'))
    shutil.copy(f"{L}/butterskin-lockup.svg", f"{ROOT}/prototype/assets/logo-lockup.svg")
    shutil.copy(f"{L}/butterskin-monogram.svg", f"{ROOT}/prototype/assets/logo-mark.svg")
    for old in ("logo-lockup-dark.svg",):
        pass
    shutil.copy(f"{L}/butterskin-wordmark.svg", f"{ROOT}/prototype/assets/logo-wordmark.svg")
    wm_c, wc = wordmark(116, 74, 60)
    open(f"{L}/butterskin-lockup-compact.svg", "w").write(svg(f"0 0 {116 + wc + 4} 104", monogram(50, 52, 48) + wm_c, "ButterSkin logo, compact"))
    shutil.copy(f"{L}/butterskin-lockup-compact.svg", f"{ROOT}/prototype/assets/logo-header.svg")


# ------------------------------------------------------------------ studio-lit packaging
SHADES = {  # (highlight, mid, edge)
    "porcelain": ("#FFFFFF", "#F1EEE8", "#D3CDC1"), "frost": ("#FAFBF8", "#E9EEE7", "#C2CDBF"),
    "emerald": ("#2F7A61", "#1B5643", "#0B2C21"), "sage": ("#E6EDE4", "#CCD9CB", "#A3B7A2"),
}
BODY = {"cleanse": "frost", "treat": "emerald", "moisturise": "porcelain", "protect": "porcelain"}
CAP = ("#B8996199", "#E4D3AE", "#9C7E48")  # unused alpha placeholder kept for clarity


def defs(uid, body):
    hi, mid, edge = SHADES[body]
    return f"""<defs>
<linearGradient id="b{uid}" x1="0" x2="1"><stop offset="0" stop-color="{edge}"/><stop offset=".2" stop-color="{mid}"/><stop offset=".42" stop-color="{hi}"/><stop offset=".64" stop-color="{mid}"/><stop offset="1" stop-color="{edge}"/></linearGradient>
<linearGradient id="c{uid}" x1="0" x2="1"><stop offset="0" stop-color="#94773F"/><stop offset=".28" stop-color="#D3BC8C"/><stop offset=".46" stop-color="#FBF3DE"/><stop offset=".62" stop-color="#CFB585"/><stop offset="1" stop-color="#8E7139"/></linearGradient>
<linearGradient id="v{uid}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".10"/></linearGradient>
<linearGradient id="h{uid}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="s{uid}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#262A28" stop-opacity=".30"/><stop offset="1" stop-color="#262A28" stop-opacity="0"/></radialGradient>
</defs>"""


def split_name(name):
    w = name.split()
    if len(w) <= 2: return w if len(" ".join(w)) > 12 else [name]
    best = min(((max(len(" ".join(w[:i])), len(" ".join(w[i:]))), [" ".join(w[:i]), " ".join(w[i:])]) for i in range(1, len(w))))
    return best[1]


def label(p, cx, y, w, h):
    cat = next(c["name"] for c in DATA["categories"] if c["id"] == p["category"]).upper()
    lines = split_name(p["name"])
    nfs = min(12.5, w * 0.16)
    out = [f'<rect x="{cx - w / 2:.1f}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF"/>',
           f'<rect x="{cx - w / 2 + 3:.1f}" y="{y + 3}" width="{w - 6}" height="{h - 6}" fill="none" stroke="#CDB68A" stroke-width=".6"/>',
           centered("BUTTERSKIN", SERIF, min(8.5, w * 0.105), cx, y + 15, INK, tracking=0.22, maxw=w - 14),
           f'<line x1="{cx - 10}" x2="{cx + 10}" y1="{y + 20}" y2="{y + 20}" stroke="#CDB68A" stroke-width=".8"/>']
    for i, ln in enumerate(lines):
        out.append(centered(ln, SERIF, nfs, cx, y + 33 + i * (nfs + 2), INK, maxw=w - 12))
    out.append(centered(cat, SANS_M, 5.6, cx, y + h - 17, EM, tracking=0.2, maxw=w - 12))
    out.append(centered(f"{p['size'].upper()} · CONCEPT", SANS, 5.2, cx, y + h - 8, hexval("charcoal.600"), tracking=0.12, maxw=w - 12))
    return "".join(out)


TOPS = {"tube": 30, "pump": 52, "dropper": 52, "jar": 140, "bottle": 60}


def package(p, uid):
    fmt, body = p["format"], BODY[p["category"]]
    if p["id"] == "soft-cloud-moisturiser": body = "sage"
    cx = 100; o = [defs(uid, body)]
    sh = lambda rx, ry=10: o.append(f'<ellipse cx="{cx}" cy="294" rx="{rx}" ry="{ry}" fill="url(#s{uid})"/>')
    if fmt == "tube":
        sh(54, 9)
        o.append(f'<path d="M{cx - 44} 40 H{cx + 44} L{cx + 36} 246 H{cx - 36} Z" fill="url(#b{uid})"/><path d="M{cx - 44} 40 H{cx + 44} L{cx + 36} 246 H{cx - 36} Z" fill="url(#v{uid})"/>')
        o.append(f'<rect x="{cx - 46}" y="32" width="92" height="10" rx="1.5" fill="{SHADES[body][2]}"/>')
        o.append(f'<rect x="{cx - 33}" y="50" width="7" height="188" rx="3.5" fill="url(#h{uid})"/>')
        o.append(f'<rect x="{cx - 34}" y="244" width="68" height="48" rx="5" fill="url(#c{uid})"/>')
        o.append(label(p, cx, 98, 70, 92))
    elif fmt == "pump":
        sh(64)
        o.append(f'<rect x="{cx - 48}" y="118" width="96" height="174" rx="18" fill="url(#b{uid})"/><rect x="{cx - 48}" y="118" width="96" height="174" rx="18" fill="url(#v{uid})"/>')
        o.append(f'<rect x="{cx - 38}" y="132" width="8" height="146" rx="4" fill="url(#h{uid})"/>')
        o.append(f'<rect x="{cx - 20}" y="94" width="40" height="28" rx="2" fill="url(#c{uid})"/>')
        o.append(f'<rect x="{cx - 5}" y="64" width="10" height="32" fill="url(#c{uid})"/>')
        o.append(f'<path d="M{cx - 22} 56 H{cx + 36} a5 5 0 0 1 0 10 H{cx - 22} Z" fill="url(#c{uid})"/>')
        o.append(label(p, cx, 164, 78, 92))
    elif fmt == "dropper":
        sh(60)
        o.append(f'<rect x="{cx - 44}" y="132" width="88" height="160" rx="12" fill="url(#b{uid})"/><rect x="{cx - 44}" y="132" width="88" height="160" rx="12" fill="url(#v{uid})"/>')
        o.append(f'<rect x="{cx - 36}" y="146" width="8" height="132" rx="4" fill="url(#h{uid})"/>')
        o.append(f'<rect x="{cx - 24}" y="98" width="48" height="38" rx="3" fill="url(#c{uid})"/>')
        o.append(f'<path d="M{cx - 15} 100 V70 a15 15 0 0 1 30 0 V100 Z" fill="{"#1F2421" if body == "emerald" else EM}"/>')
        o.append(f'<rect x="{cx - 9}" y="62" width="5" height="32" rx="2.5" fill="#fff" opacity=".22"/>')
        o.append(label(p, cx, 172, 76, 92))
    elif fmt == "jar":
        sh(92, 12)
        o.append(f'<rect x="{cx - 80}" y="196" width="160" height="96" rx="10" fill="url(#b{uid})"/><rect x="{cx - 80}" y="196" width="160" height="96" rx="10" fill="url(#v{uid})"/>')
        o.append(f'<rect x="{cx - 68}" y="204" width="10" height="80" rx="5" fill="url(#h{uid})"/>')
        o.append(f'<rect x="{cx - 84}" y="150" width="168" height="50" rx="6" fill="url(#c{uid})"/><rect x="{cx - 84}" y="150" width="168" height="4" rx="2" fill="#fff" opacity=".4"/>')
        o.append(label(p, cx, 205, 112, 80))
    else:  # bottle (essence)
        sh(58)
        path = f"M{cx - 44} 140 q0 -34 30 -40 h28 q30 6 30 40 V278 a14 14 0 0 1 -14 14 H{cx - 30} a14 14 0 0 1 -14 -14 Z"
        o.append(f'<path d="{path}" fill="url(#b{uid})"/><path d="{path}" fill="url(#v{uid})"/>')
        o.append(f'<rect x="{cx - 34}" y="140" width="8" height="132" rx="4" fill="url(#h{uid})"/>')
        o.append(f'<rect x="{cx - 22}" y="62" width="44" height="42" rx="3" fill="url(#c{uid})"/>')
        o.append(label(p, cx, 172, 76, 92))
    return "".join(o)


def texture(p, uid):
    """A product texture swatch (cream swirl / gel / oil drop / fluid), used as a second gallery image."""
    tone = {"cleanse": ("#FFFFFF", "#E8EFE6"), "treat": ("#F6EBD3", "#D9C08E"), "moisturise": ("#FFFDF8", "#EDE6D8"), "protect": ("#FFFFFF", "#E3EAEC")}[p["category"]]
    return (f'<defs><radialGradient id="t{uid}" cx=".42" cy=".38" r=".7"><stop offset="0" stop-color="{tone[0]}"/><stop offset="1" stop-color="{tone[1]}"/></radialGradient>'
            f'<radialGradient id="g{uid}" cx=".35" cy=".3" r=".35"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="100" cy="190" rx="80" ry="16" fill="#262A28" opacity=".08"/>'
            f'<path d="M40 170 C30 120 80 92 112 110 C150 92 178 132 160 168 C150 196 70 204 40 170 Z" fill="url(#t{uid})"/>'
            f'<path d="M70 140 C88 122 118 124 132 140 C118 134 92 134 78 150 Z" fill="#fff" opacity=".7"/>'
            f'<ellipse cx="88" cy="128" rx="34" ry="16" fill="url(#g{uid})"/>')


def write_packaging():
    P = f"{ROOT}/design/brand/packaging"; A = f"{ROOT}/prototype/assets/packaging"
    for d in (P, A):
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            os.remove(f"{d}/{f}")
    for i, p in enumerate(DATA["products"]):
        art = package(p, f"p{i}"); y0 = TOPS[p["format"]] - 10
        title = f"{p['name']}, fictional concept packaging"
        tight = svg(f"22 {y0} 156 {308 - y0}", art, title); scene = svg("0 20 200 290", art, title)
        tex = svg("20 80 160 130", texture(p, f"x{i}"), f"{p['name']} texture, illustrative")
        for d in (P, A):
            open(f"{d}/{p['id']}.svg", "w").write(tight); open(f"{d}/{p['id']}-scene.svg", "w").write(scene); open(f"{d}/{p['id']}-texture.svg", "w").write(tex)
    items = "".join(f'<g transform="translate({i * 175} 0)">{package(p, f"f{i}")}</g>' for i, p in enumerate(DATA["products"]))
    open(f"{P}/family-lineup.svg", "w").write(svg(f"0 20 {175 * 7 + 200} 290", items, "ButterSkin concept packaging family (fictional)"))


if __name__ == "__main__":
    write_tokens(); write_logos(); write_packaging()
    rows = contrast_rows(); bad = [r for r in rows if r[3] < r[4]]
    for r in rows:
        print(f"{'PASS' if r[3] >= r[4] else 'FAIL'} {r[3]:>5}:1  {r[0]}")
    print("brand built;", len(bad), "contrast failures")
