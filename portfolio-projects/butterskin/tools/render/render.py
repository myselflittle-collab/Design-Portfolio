"""ButterSkin product renders (Blender Cycles through the bpy module, pip install bpy).
python3 tools/render/render.py SHOT out.png width samples
SHOT = hero | detail | range | pack:<id> | scene:<id> | texture:<id>.  tools/render/render_all.sh renders the full set."""
import sys, os, json, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
from scene import *
import botan as B

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
SHOT, OUT, W, SPP = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
LD = f"{ROOT}/design/brand/packaging/labels"; os.makedirs(LD, exist_ok=True)
EM, CHP, CH7, IV = "#0E4A38", "#C9AA6B", "#7A5E28", "#F6F1E6"


def dims(kind, g):
    if kind == "dropper": return (1.654) * 1.75, (7.2 - 0.35) - 1.15
    if kind == "jar": return 3.304 * 1.55, 3.2
    if kind == "tube": return (g["R"] + .006) * 1.7, g["L"] * 0.80 - 0.9
    return (g["R"] + .004) * 1.45, (g["H"] - 0.6) - 1.4


#            id: kind, geometry, label name, ingredient line, size, ink, type size (cm)
PROD = {
    "dewdrop-hydration-serum": ("dropper", {}, "Dewdrop<br>Hydration Serum", "Hyaluronic acid · Panthenol", "30 ML", "ivory", .232),
    "soft-gel-cleanser": ("pump", {"R": 2.45, "H": 11.0}, "Soft Gel<br>Cleanser", "Glycerin · Green tea", "150 ML", "emerald", .25),
    "butter-balm-cream": ("jar", {}, "Butter Balm Cream", "Shea butter · Ceramides", "50 ML", "emerald", .19),
    "daylight-spf-50": ("tube", {"R": 1.85, "L": 11.0}, "Daylight<br>SPF 50", "UV filters · Niacinamide", "50 ML", "emerald", .2),
    "still-water-essence": ("bottle", {"R": 1.95, "H": 10.0}, "Still Water<br>Essence", "Niacinamide · Rice ferment", "100 ML", "emerald", .21),
    "cloud-milk-cleanser": ("tube", {"R": 2.15, "L": 13.5}, "Cloud Milk<br>Cleanser", "Glycerin · Oat extract", "120 ML", "emerald", .22),
    "quiet-night-oil": ("dropper", {}, "Quiet<br>Night Oil", "Squalane · Jojoba oil", "30 ML", "emerald", .232),
    "soft-cloud-moisturiser": ("pump", {"R": 2.05, "H": 8.0}, "Soft Cloud<br>Moisturiser", "Glycerin · Squalane", "50 ML", "emerald", .19),
}
HEIGHT = {"dewdrop-hydration-serum": 13.0, "quiet-night-oil": 13.0, "soft-gel-cleanser": 16.4, "butter-balm-cream": 6.0, "daylight-spf-50": 15.4,
          "cloud-milk-cleanser": 18.1, "still-water-essence": 13.9, "soft-cloud-moisturiser": 13.3}

specs = []
for pid, (kind, g, name, ing, size, inkc, scm) in PROD.items():
    arc, h = dims(kind, g)
    w, hh = (int(2000 * arc / h), 2000) if arc < h else (2000, int(2000 * h / arc))
    iv = inkc == "ivory"
    specs.append(dict(out=f"{LD}/{pid}.png", w=w, h=hh, ink=IV if iv else EM, acc=CHP if iv else "#A88748", s=round(scm * hh / h, 1),
                      name=name, ing=ing, size=size, emb=kind != "jar"))
if not all(os.path.exists(x["out"]) for x in specs) or os.environ.get("RELABEL"):
    json.dump(specs, open(f"{LD}/specs.json", "w"))
    subprocess.run([sys.executable, f"{HERE}/labels.py", f"{LD}/specs.json"], check=True)
L = lambda p: f"{LD}/{p}.png"

sc = reset()
sc.render.resolution_x = W
sc.render.resolution_y = int(W * (1.25 if SHOT.split(":")[0] in ("pack", "scene", "texture") else 0.5625 if SHOT in ("hero",) else 0.5 if SHOT == "range" else 0.75))
sc.cycles.samples = SPP
M = {"metal": brushed_metal("champagne", col=(0.83, 0.68, 0.42), rough=0.2), "rubber": P("bulb", base=(0.006, 0.008, 0.007), rough=0.38)[0], "clear": glass("clear", (1, 1, 1))}
deep_em = glass("deep_emerald", (0.07, 0.29, 0.19))
frost = frosted("frost", (0.97, 0.975, 0.965))
porcelain = ceramic("porcelain", (0.92, 0.905, 0.87))
tube_white = plastic("tube_white", (0.93, 0.915, 0.88), rough=0.48)


def make(pid):
    k, g = PROD[pid][0], PROD[pid][1]
    if pid == "dewdrop-hydration-serum": return dropper_bottle(M, L(pid), glass_mat=deep_em, liq=liquid("serum_liq", (0.97, 0.96, 0.9)))
    if pid == "quiet-night-oil": return dropper_bottle(M, L(pid), glass_mat=frost, liq=liquid("oil_liq", (1.0, 0.70, 0.26), ior=1.47), fill=0.72)
    if pid == "butter-balm-cream": return jar(M, L(pid), body=porcelain, lid=M["metal"])
    if k == "tube": return tube(M, L(pid), R=g["R"], L=g["L"], body=tube_white, cap=M["metal"])
    if pid == "soft-gel-cleanser": return pump_bottle(M, L(pid), R=g["R"], H=g["H"], glass_mat=frost, liq=liquid("gel", (0.95, 0.97, 0.93), ior=1.34))
    if pid == "soft-cloud-moisturiser": return pump_bottle(M, L(pid), R=g["R"], H=g["H"], glass_mat=porcelain, liq=None)
    if pid == "still-water-essence": return cap_bottle(M, L(pid), R=g["R"], H=g["H"], glass_mat=frost, liq=liquid("ess", (0.98, 0.98, 0.96), ior=1.34))


def studio(sweep_col=(0.80, 0.765, 0.69)):
    sweep(sweep_col, 0.5)
    k = area("key", (-0.55, -0.55, 0.5), (0, 0, 0), 0.7, 22, col=(1.0, 0.95, 0.88)); look_at(k, (0, 0, 0.06))
    f = area("fill", (0.6, -0.6, 0.25), (0, 0, 0), 0.9, 4); look_at(f, (0, 0, 0.06))
    for nm, x in (("rimL", -0.35), ("rimR", 0.35)):
        r = area(nm, (x, 0.30, 0.18), (0, 0, 0), 0.06, 9, sy=0.9); look_at(r, (x / 7, 0, 0.08))
    tp = area("top", (0, 0, 0.75), (0, 0, 0), 0.8, 3); look_at(tp, (0, 0, 0))
    bg = area("bgwash", (0, 0.15, 0.05), (0, 0, 0), 0.5, 2.2, col=(1.0, 0.93, 0.82)); look_at(bg, (0, 0.55, 0.5))


def botanical(products, cam, tgt, lens, fstop, focus_pt):
    stone = B.stone_mat(); rk = B.stone_mat("rock", c1=(0.20, 0.18, 0.15), c2=(0.42, 0.38, 0.32))
    B.slab(0.8, 0.5, 0.06, stone, (0.03, 0.08, 0))
    B.rock((-0.14, 0.14, 0.02), (0.085, 0.06, 0.075), rk, 1)
    B.rock((0.13, 0.18, 0.03), (0.10, 0.07, 0.10), rk, 2)
    B.rock((0.24, 0.05, 0.0), (0.05, 0.04, 0.035), rk, 3)
    B.rock((-0.19, -0.05, 0.0), (0.04, 0.035, 0.022), rk, 4)
    for pid, x, y, rz in products: place(make(pid), x, y, rz)
    B.moss_clump((-0.085, -0.04, 0.0), (0.05, 0.03), n=11, seed=1)
    B.moss_clump((0.195, -0.035, 0.0), (0.05, 0.03), n=9, seed=2)
    B.moss_clump((-0.14, 0.10, 0.045), (0.04, 0.02), n=6, seed=3)
    for i, (x, y) in enumerate([(-0.115, -0.075), (-0.10, -0.088), (-0.03, -0.085), (0.16, -0.07), (0.18, -0.085)]):
        B.flower((x, y, 0.004), 0.011 + 0.003 * (i % 2), seed=i, tilt=(8 * (i % 3), -6 + 4 * i))
    lm = B.leaf_mat("leafA"); lm2 = B.leaf_mat("leafB", base=(0.05, 0.16, 0.06), tip=(0.12, 0.28, 0.09))
    B.sprig((-0.26, 0.20, 0.0), 160, lm, n=6, L=(0.14, 0.22), W=(0.04, 0.06), spread=60, pitch=(30, 62), droop=0.35, seed=1)
    B.sprig((0.30, 0.22, 0.0), 205, lm2, n=6, L=(0.14, 0.22), W=(0.04, 0.06), spread=60, pitch=(30, 62), droop=0.35, seed=2)
    B.sprig((-0.02, 0.32, 0.0), 180, lm2, n=7, L=(0.16, 0.26), W=(0.04, 0.07), spread=110, pitch=(55, 80), droop=0.25, seed=3)
    B.sprig((-0.30, 0.10, 0.0), 150, lm2, n=8, L=(0.09, 0.15), W=(0.025, 0.04), spread=80, pitch=(20, 55), droop=0.3, seed=6)
    B.sprig((0.33, 0.10, 0.0), 210, lm, n=8, L=(0.09, 0.15), W=(0.025, 0.04), spread=80, pitch=(20, 55), droop=0.3, seed=7)
    B.sprig((0.06, 0.30, 0.0), 170, lm, n=6, L=(0.12, 0.2), W=(0.02, 0.035), spread=120, pitch=(60, 85), droop=0.2, seed=8)
    B.foliage_bg(lm2, n=45, y=0.62); B.bokeh(46, y=0.9, col=(1.0, 0.78, 0.45), strength=9)
    B.sprig((-0.55, -0.05, 0.25), 100, lm2, n=9, L=(0.10, 0.16), W=(0.03, 0.05), spread=90, pitch=(-20, 20), droop=0.2, seed=11)
    B.sprig((-0.22, -0.02, 0.0), 125, lm, n=4, L=(0.06, 0.09), W=(0.02, 0.03), spread=60, pitch=(10, 30), droop=0.2, seed=4)
    B.sprig((0.27, -0.01, 0.0), 230, lm, n=4, L=(0.06, 0.09), W=(0.02, 0.03), spread=60, pitch=(10, 30), droop=0.2, seed=5)
    B.backdrop(col_top=(0.16, 0.21, 0.10), col_bot=(0.72, 0.56, 0.30), y=1.0, size=4)
    sd = bpy.data.lights.new("sun", "SUN"); sd.energy = 6.5; sd.angle = math.radians(1.5); sd.color = (1.0, 0.86, 0.66)
    so = bpy.data.objects.new("sun", sd); bpy.context.collection.objects.link(so); so.location = (-1.0, -0.25, 0.75); look_at(so, (0, 0, 0))
    f = area("fill", (0.2, -0.8, 0.35), (0, 0, 0), 1.0, 4.5, col=(1.0, 0.95, 0.88)); look_at(f, (0, 0, 0.06))
    r = area("rim", (0.4, 0.3, 0.2), (0, 0, 0), 0.06, 6, sy=0.8); look_at(r, (0.05, 0, 0.08))
    camera(cam, tgt, lens=lens, fstop=fstop, focus=(Vector(cam) - Vector(focus_pt)).length)


HERO = [("dewdrop-hydration-serum", -0.065, -0.035, 0.0), ("soft-gel-cleanser", -0.012, 0.05, -0.05), ("butter-balm-cream", 0.045, -0.03, 0.0),
        ("daylight-spf-50", 0.098, 0.05, 0.08), ("still-water-essence", 0.150, 0.0, 0.0)]

if SHOT.startswith("pack:"):
    pid = SHOT.split(":")[1]; place(make(pid), 0, 0, 0.0); studio()
    h = HEIGHT[pid] * 0.01; fr = max(h, {"butter-balm-cream": 0.095}.get(pid, 0)); d = fr * 3.15 + 0.06
    camera((0, -d, h * 0.55 + d * 0.06), (0, 0, h * 0.5), lens=85, fstop=16, focus=d - 0.02)
elif SHOT == "range":
    lay = [("cloud-milk-cleanser", -0.165), ("soft-gel-cleanser", -0.115), ("still-water-essence", -0.068), ("dewdrop-hydration-serum", -0.030),
           ("quiet-night-oil", 0.003), ("butter-balm-cream", 0.050), ("soft-cloud-moisturiser", 0.103), ("daylight-spf-50", 0.148)]
    for pid, x in lay: place(make(pid), x, 0.0, 0.0)
    studio()
    camera((-0.008, -1.15, 0.10), (-0.008, 0, 0.082), lens=95, fstop=13, focus=1.15)
elif SHOT == "hero":
    botanical(HERO, (0.035, -0.78, 0.125), (0.04, 0.02, 0.068), 58, 4.5, (-0.065, -0.05, 0.06))
elif SHOT.startswith("scene:"):
    pid = SHOT.split(":")[1]; h = HEIGHT[pid] * 0.01; d = max(h, 0.10) * 2.7 + 0.07
    botanical([(pid, 0.0, -0.035, 0.0)], (0.0, -0.035 - d, h * 0.52 + 0.035), (0.0, -0.035, h * 0.54), 70, 4.0, (0.0, -0.06, h * 0.5))
elif SHOT.startswith("texture:"):
    pid = SHOT.split(":")[1]
    stone = B.stone_mat(); B.slab(0.5, 0.4, 0.04, stone, (0, 0, 0))
    kind = {"butter-balm-cream": "cream", "soft-cloud-moisturiser": "lotion", "cloud-milk-cleanser": "lotion", "daylight-spf-50": "fluid",
            "soft-gel-cleanser": "gel", "dewdrop-hydration-serum": "drops", "still-water-essence": "drops", "quiet-night-oil": "oil"}[pid]
    mats = {"cream": P("cream", base=(0.95, 0.93, 0.88), rough=0.32, sss=0.6, sss_r=(0.004, 0.004, 0.003))[0],
            "lotion": P("lotion", base=(0.96, 0.95, 0.92), rough=0.22, sss=0.6, sss_r=(0.004, 0.004, 0.004), coat=0.4)[0],
            "fluid": P("fluid", base=(0.97, 0.96, 0.93), rough=0.18, sss=0.5, sss_r=(0.003, 0.003, 0.003), coat=0.6)[0],
            "gel": liquid("gelx", (0.93, 0.97, 0.92), ior=1.34), "drops": liquid("dropx", (0.99, 0.99, 0.97), ior=1.34), "oil": liquid("oilx", (1.0, 0.72, 0.28), ior=1.47)}
    import random as _r; rr = _r.Random(4)
    def blob(loc, sx, sy, sz, peak=0.0, mat=None):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, location=loc); o = bpy.context.active_object
        for v in o.data.vertices:
            x, y, z = v.co; z = max(z, -0.15)
            if peak and z > 0: z *= 1 + peak * math.exp(-(x * x + y * y) / 0.25)
            v.co = (x * sx, y * sy, (z + 0.15) * sz)
        o.location.z += 0.0003
        if mat.name.startswith(("cream", "lotion", "fluid")):
            tex = bpy.data.textures.new("bl" + str(len(bpy.data.textures)), "CLOUDS"); tex.noise_scale = 0.006
            dm = o.modifiers.new("d", "DISPLACE"); dm.texture = tex; dm.strength = sz * 0.25
        for p in o.data.polygons: p.use_smooth = True
        o.data.materials.append(mat); return o
    m = mats[kind]
    if kind == "cream": blob((0, 0, 0), 0.024, 0.02, 0.009, peak=0.8, mat=m); blob((0.045, 0.012, 0), 0.03, 0.008, 0.0018, mat=m)
    elif kind in ("lotion", "fluid"): blob((0, 0, 0), 0.022, 0.017, 0.0055, peak=0.6, mat=m); blob((0.04, 0.008, 0), 0.032, 0.009, 0.0016, mat=m)
    elif kind == "gel": blob((0, 0, 0), 0.022, 0.018, 0.0075, peak=0.4, mat=m); blob((0.042, 0.012, 0), 0.012, 0.01, 0.0035, mat=m)
    else:
        for i in range(7):
            s = rr.uniform(0.004, 0.011); blob((rr.uniform(-0.03, 0.04), rr.uniform(-0.02, 0.025), 0), s, s * rr.uniform(0.85, 1.1), s * 0.55, mat=m)
    lm = B.leaf_mat("leafT"); lf = B.leaf(0.12, 0.04, lm, droop=0.05, fold=0.15); lf.location = (-0.03, 0.05, 0.003); lf.rotation_euler = (0.08, 0, math.radians(140))
    B.backdrop(col_top=(0.30, 0.34, 0.20), col_bot=(0.80, 0.68, 0.45), y=0.8, size=3)
    sd = bpy.data.lights.new("sun", "SUN"); sd.energy = 5.0; sd.angle = math.radians(2.0); sd.color = (1.0, 0.88, 0.70)
    so = bpy.data.objects.new("sun", sd); bpy.context.collection.objects.link(so); so.location = (-1.0, -0.4, 0.9); look_at(so, (0, 0, 0))
    f = area("fill", (0.3, -0.6, 0.5), (0, 0, 0), 0.8, 5, col=(1.0, 0.96, 0.9)); look_at(f, (0, 0, 0))
    cam = (0.010, -0.19, 0.15); camera(cam, (0.008, 0.012, 0.0), lens=90, fstop=5.6, focus=(Vector(cam) - Vector((0.005, 0, 0.004))).length)
elif SHOT == "detail":
    botanical(HERO, (-0.115, -0.40, 0.10), (-0.060, -0.035, 0.072), 100, 4.0, (-0.065, -0.052, 0.07))
sc.render.filepath = OUT; sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
print("done", OUT)
