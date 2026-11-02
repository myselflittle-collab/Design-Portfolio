"""ButterSkin 3D packaging models and materials (Blender/Cycles via the bpy module).
Units: metres. Helper C converts centimetres."""
import bpy, bmesh, math, os, sys, json
from mathutils import Vector

C = 0.01
HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ basics
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 16
    sc.cycles.transmission_bounces = 16
    sc.cycles.glossy_bounces = 8
    sc.cycles.transparent_max_bounces = 16
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.blur_glossy = 1.0
    sc.view_settings.view_transform = "AgX"
    try:
        sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.9, 0.88, 0.84, 1); bg.inputs[1].default_value = 0.08
    return sc


def fillet(pts, rad, steps=8):
    """Round the interior corners of a 2D polyline (r,z). rad may be a list per point."""
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        r = rad[i] if isinstance(rad, (list, tuple)) else rad
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[i + 1])
        if r <= 0:
            out.append(tuple(p1)); continue
        a, b = (p0 - p1), (p2 - p1)
        la, lb = a.length, b.length
        r = min(r, la * .49, lb * .49)
        a.normalize(); b.normalize()
        s, e = p1 + a * r, p1 + b * r
        for k in range(steps + 1):
            t = k / steps  # quadratic bezier through corner
            q = (1 - t) ** 2 * s + 2 * (1 - t) * t * p1 + t * t * e
            out.append((q.x, q.y))
    out.append(pts[-1])
    return out


def lathe(name, prof, seg=128, mat=None, smooth=True, closed=False):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    rings = []
    for r, z in prof:
        ring = [bm.verts.new((r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)]
        rings.append(ring)
    uv = bm.loops.layers.uv.new()
    n = len(rings)
    for j in range(n - 1 + (1 if closed else 0)):
        A, B = rings[j], rings[(j + 1) % n]
        for i in range(seg):
            f = bm.faces.new((A[i], A[(i + 1) % seg], B[(i + 1) % seg], B[i]))
            for lp, (uu, vv) in zip(f.loops, ((i / seg, j / n), ((i + 1) / seg, j / n), ((i + 1) / seg, (j + 1) / n), (i / seg, (j + 1) / n))):
                lp[uv].uv = (uu, vv)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    if smooth:
        for p in me.polygons: p.use_smooth = True
    if mat: me.materials.append(mat)
    return ob


def decal(name, radius, z0, z1, ang, img, ink_mat_fn, deform=None, seg=96, rows=40, face=-math.pi / 2):
    """Cylindrical decal facing -Y. ang = arc in radians."""
    me = bpy.data.meshes.new(name); bm = bmesh.new(); uv = bm.loops.layers.uv.new()
    grid = []
    for j in range(rows + 1):
        z = z0 + (z1 - z0) * j / rows; row = []
        for i in range(seg + 1):
            th = face - ang / 2 + ang * i / seg
            x, y = radius * math.cos(th), radius * math.sin(th)
            if deform: x, y = deform(x, y, z)
            row.append(bm.verts.new((x, y, z)))
        grid.append(row)
    for j in range(rows):
        for i in range(seg):
            f = bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
            for lp, (uu, vv) in zip(f.loops, ((i / seg, j / rows), ((i + 1) / seg, j / rows), ((i + 1) / seg, (j + 1) / rows), (i / seg, (j + 1) / rows))):
                lp[uv].uv = (uu, vv)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    me.materials.append(ink_mat_fn(img))
    return ob


# ------------------------------------------------------------------ materials
def P(name, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    keys = {"base": "Base Color", "metal": "Metallic", "rough": "Roughness", "ior": "IOR", "trans": "Transmission Weight",
            "coat": "Coat Weight", "coat_rough": "Coat Roughness", "sss": "Subsurface Weight", "sss_r": "Subsurface Radius",
            "aniso": "Anisotropic", "spec": "Specular IOR Level", "sheen": "Sheen Weight"}
    for k, v in kw.items():
        if k == "base" and len(v) == 3: v = (*v, 1)
        b.inputs[keys[k]].default_value = v
    return m, b


def glass(name, tint=(1, 1, 1), rough=0.0, ior=1.5):
    m, _ = P(name, base=tint, trans=1.0, rough=rough, ior=ior); return m


def frosted(name, tint=(0.97, 0.98, 0.97)):
    m, b = P(name, base=tint, trans=1.0, rough=0.42, ior=1.5)
    return m


def liquid(name, col, ior=1.36, dens=0.0, vol_col=None):
    m, b = P(name, base=col, trans=1.0, rough=0.0, ior=ior)
    if dens:
        nt = m.node_tree; va = nt.nodes.new("ShaderNodeVolumeAbsorption")
        va.inputs["Color"].default_value = (*vol_col, 1); va.inputs["Density"].default_value = dens
        nt.links.new(va.outputs[0], nt.nodes["Material Output"].inputs["Volume"])
    return m


def brushed_metal(name, col=(0.80, 0.66, 0.45), rough=0.22):
    m, b = P(name, base=col, metal=1.0, rough=rough)
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord"); nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 900; nz.inputs["Detail"].default_value = 2
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1, 1, 0.02)  # streaks along circumference
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.05; bp.inputs["Distance"].default_value = 0.0002
    nt.links.new(tc.outputs["Object"], mp.inputs[0]); nt.links.new(mp.outputs[0], nz.inputs[0])
    nt.links.new(nz.outputs[0], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    try: b.inputs["Anisotropic"].default_value = 0.6
    except Exception: pass
    return m


def plastic(name, col, rough=0.45, coat=0.15):
    m, _ = P(name, base=col, rough=rough, coat=coat, coat_rough=0.3); return m


def ceramic(name, col):
    m, _ = P(name, base=col, rough=0.16, coat=0.6, coat_rough=0.08, sss=0.15, sss_r=(0.002, 0.002, 0.002)); return m


def rubber(name, col):
    m, b = P(name, base=col, rough=0.55, sheen=0.2); return m


def ink(img_path, rough=0.35, metal=0.0, emboss=0.0):
    def make(_):
        m = bpy.data.materials.new("ink_" + os.path.basename(img_path)); m.use_nodes = True
        nt = m.node_tree; b = nt.nodes["Principled BSDF"]; out = nt.nodes["Material Output"]
        b.inputs["Roughness"].default_value = max(rough, 0.75); b.inputs["Metallic"].default_value = metal; b.inputs["Specular IOR Level"].default_value = 0.2
        tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = bpy.data.images.load(img_path); tx.interpolation = "Cubic"
        tx.image.alpha_mode = "STRAIGHT"
        nt.links.new(tx.outputs["Color"], b.inputs["Base Color"])
        tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
        pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 0.42
        nt.links.new(tx.outputs["Alpha"], pw.inputs[0]); nt.links.new(pw.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(b.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs[0])
        m.blend_method = "HASHED" if hasattr(m, "blend_method") else None
        return m
    return make


# ------------------------------------------------------------------ products
def place(objs, x, y, rotz=0.0):
    e = bpy.data.objects.new("grp", None); bpy.context.collection.objects.link(e)
    for o in objs: o.parent = e
    e.location = (x, y, 0); e.rotation_euler = (0, 0, rotz)
    return e


def dropper_bottle(M, label_img, R=1.65, H=7.2, glass_mat=None, liq=None, fill=0.78):
    t, tb, rn, nz = 0.17, 0.45, 0.78, 8.3  # wall, bottom, neck radius, neck top
    out = [(0, 0), (R, 0), (R, H), (rn, H + 0.75), (rn, nz)]
    inn = [(rn - t, nz), (rn - t, H + 0.75), (R - t, H - 0.05), (R - t, tb), (0, tb)]
    prof = fillet(out, [0, .35, .5, .25, 0], 10) + fillet(inn, [0, .2, .4, .25, 0], 10)
    prof = [(r * C, z * C) for r, z in prof]
    objs = [lathe("serum_glass", prof, mat=glass_mat)]
    lz = tb + (H - tb) * fill
    lp = fillet([(0, tb + .02), (R - t - .004, tb + .02), (R - t - .004, lz), (0, lz)], [0, .2, 0, 0], 8)
    objs.append(lathe("serum_liq", [(r * C, z * C) for r, z in lp], mat=liq))
    # pipette
    pp = fillet([(0, 1.3), (0.26, 1.3), (0.26, nz + .2), (0.33, nz + .2), (0.33, 1.25), (0, 1.0)], [0, .1, 0, 0, .12, 0], 6)
    objs.append(lathe("pipette", [(r * C, z * C) for r, z in pp], seg=48, mat=M["clear"]))
    # collar
    cp = fillet([(0, nz - 0.55), (rn + 0.2, nz - 0.55), (rn + 0.2, nz + 1.75), (0.62, nz + 1.75), (0.62, nz + 1.9), (0, nz + 1.9)], [0, .12, .14, .05, 0, 0], 8)
    objs.append(lathe("collar", [(r * C, z * C) for r, z in cp], mat=M["metal"]))
    # bulb
    b0 = nz + 1.75
    bp = fillet([(0, b0), (0.66, b0), (0.6, b0 + 0.5), (0.66, b0 + 2.1), (0.0, b0 + 2.75)], [0, .2, .25, .6, 0], 12)
    objs.append(lathe("bulb", [(r * C, z * C) for r, z in bp], mat=M["rubber"]))
    objs.append(decal("serum_label", (R + 0.004) * C, 1.15 * C, (H - 0.35) * C, 1.75, label_img, ink(label_img, 0.3)))
    return objs


def jar(M, label_img, R=3.3, H=4.0, body=None, lid=None):
    bp = fillet([(0, 0), (R - 0.15, 0), (R, 0.35), (R, H), (R - 0.35, H), (R - 0.35, H + 0.55), (0, H + 0.55)], [0, .1, .2, .25, 0.05, 0, 0], 10)
    objs = [lathe("jar_body", [(r * C, z * C) for r, z in bp], mat=body)]
    lp = fillet([(0, H + 0.08), (R + 0.04, H + 0.08), (R + 0.04, H + 2.0), (0, H + 2.0)], [0, .06, .32, 0], 12)
    objs.append(lathe("jar_lid", [(r * C, z * C) for r, z in lp], mat=lid))
    objs.append(decal("jar_label", (R + 0.004) * C, 0.55 * C, (H - 0.25) * C, 1.55, label_img, ink(label_img, 0.3)))
    return objs


def tube(M, label_img, R=1.9, L=13.0, body=None, cap=None):
    ch = 2.3  # cap height (tube stands on its cap)
    z0, z1 = ch + 0.6, ch + 0.6 + L

    def shape(z):
        t = max(0.0, min(1.0, (z - z0) / L))
        s = 0 if t < 0.12 else ((t - 0.12) / 0.88)
        s = s * s * (3 - 2 * s)
        return 1 + 0.30 * s, 1 - 0.93 * s

    def deform(x, y, z):
        sx, sy = shape(z); return x * sx, y * sy

    prof = [(1.0, ch - 0.05), (1.0, ch + 0.15)] + [(1.0 + (R - 1.0) * math.sin(math.pi / 2 * k / 10), ch + 0.15 + 0.45 * (1 - math.cos(math.pi / 2 * k / 10))) for k in range(1, 11)]
    prof += [(R, z0 + L * k / 60) for k in range(1, 61)]
    prof = [(r * C, z * C) for r, z in prof]
    ob = lathe("tube_body", prof, mat=body)
    for v in ob.data.vertices:
        x, y = deform(v.co.x / C, v.co.y / C, v.co.z / C); v.co.x, v.co.y = x * C, y * C
    objs = [ob]
    # crimp seal
    bpy.ops.mesh.primitive_cube_add(size=1)
    cr = bpy.context.active_object; cr.name = "crimp"
    cr.scale = (2 * R * 1.30 * C, 0.36 * C, 1.1 * C); cr.location = (0, 0, (z1 + 0.45) * C)
    bv = cr.modifiers.new("b", "BEVEL"); bv.width = 0.08 * C; bv.segments = 3
    cmat = body.copy(); nt = cmat.node_tree; bsdf = nt.nodes["Principled BSDF"]
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 18; wv.bands_direction = "Z"
    bpn = nt.nodes.new("ShaderNodeBump"); bpn.inputs["Strength"].default_value = 0.4
    nt.links.new(wv.outputs["Fac"], bpn.inputs["Height"]); nt.links.new(bpn.outputs[0], bsdf.inputs["Normal"])
    cr.data.materials.append(cmat)
    for p in cr.data.polygons: p.use_smooth = True
    cr.parent = None; objs.append(cr)
    # cap
    cp = fillet([(0, 0), (1.32, 0), (1.32, ch), (0, ch)], [0, .18, .12, 0], 10)
    objs.append(lathe("tube_cap", [(r * C, z * C) for r, z in cp], mat=cap))
    objs.append(decal("tube_label", (R + 0.006) * C, (z0 + 0.9) * C, (z0 + L * 0.80) * C, 1.7, label_img, ink(label_img, 0.4),
                      deform=lambda x, y, z: tuple(c * C for c in deform(x / C, y / C, z / C))))
    return objs


def cap_bottle(M, label_img, R=2.35, H=10.5, glass_mat=None, liq=None, fill=0.8):
    t, tb, rn = 0.2, 0.55, 1.0
    out = [(0, 0), (R, 0), (R, H), (rn, H + 1.0), (rn, H + 1.8)]
    inn = [(rn - t, H + 1.8), (rn - t, H + 1.0), (R - t, H - 0.05), (R - t, tb), (0, tb)]
    prof = fillet(out, [0, .4, .8, .3, 0], 10) + fillet(inn, [0, .25, .6, .3, 0], 10)
    objs = [lathe("bottle_glass", [(r * C, z * C) for r, z in prof], mat=glass_mat)]
    lz = tb + (H - tb) * fill
    lp = fillet([(0, tb + .02), (R - t - .005, tb + .02), (R - t - .005, lz), (0, lz)], [0, .3, 0, 0], 8)
    if liq: objs.append(lathe("bottle_liq", [(r * C, z * C) for r, z in lp], mat=liq))
    top = H + 1.8
    cp = fillet([(0, top - 0.95), (rn + 0.32, top - 0.95), (rn + 0.32, top + 2.1), (0, top + 2.1)], [0, .12, .3, 0], 10)
    objs.append(lathe("bottle_cap", [(r * C, z * C) for r, z in cp], mat=M["metal"]))
    objs.append(decal("bottle_label", (R + 0.004) * C, 1.4 * C, (H - 0.6) * C, 1.45, label_img, ink(label_img, 0.35)))
    return objs


def pump_bottle(M, label_img, R=2.55, H=11.5, glass_mat=None, liq=None, fill=0.72):
    t, tb, rn = 0.2, 0.55, 1.05
    out = [(0, 0), (R, 0), (R, H), (rn, H + 1.0), (rn, H + 1.8)]
    inn = [(rn - t, H + 1.8), (rn - t, H + 1.0), (R - t, H - 0.05), (R - t, tb), (0, tb)]
    prof = fillet(out, [0, .45, .9, .3, 0], 10) + fillet(inn, [0, .25, .7, .3, 0], 10)
    objs = [lathe("pump_glass", [(r * C, z * C) for r, z in prof], mat=glass_mat)]
    lz = tb + (H - tb) * fill
    lp = fillet([(0, tb + .02), (R - t - .005, tb + .02), (R - t - .005, lz), (0, lz)], [0, .3, 0, 0], 8)
    if liq: objs.append(lathe("pump_liq", [(r * C, z * C) for r, z in lp], mat=liq))
    if liq: objs.append(lathe("diptube", [(r * C, z * C) for r, z in [(0, 0.8), (0.18, 0.8), (0.18, H + 1.9), (0, H + 1.9)]], seg=32, mat=M["clear"]))
    top = H + 1.8
    cp = fillet([(0, top - 0.9), (rn + 0.28, top - 0.9), (rn + 0.28, top + 0.6), (0.5, top + 0.6), (0.5, top + 2.0), (0, top + 2.0)], [0, .12, .15, .05, 0, 0], 8)
    objs.append(lathe("pump_collar", [(r * C, z * C) for r, z in cp], mat=M["metal"]))
    a0 = top + 2.0
    ap = fillet([(0, a0), (1.25, a0), (1.25, a0 + 1.4), (0, a0 + 1.55)], [0, .25, .4, 0], 10)
    objs.append(lathe("actuator", [(r * C, z * C) for r, z in ap], mat=M["metal"]))
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.3 * C, depth=2.0 * C, location=(0, -1.6 * C, (a0 + 0.8) * C), rotation=(math.pi / 2, 0, 0))
    nz = bpy.context.active_object; nz.name = "nozzle"; nz.data.materials.append(M["metal"])
    bv = nz.modifiers.new("b", "BEVEL"); bv.width = 0.06 * C; bv.segments = 3
    for p in nz.data.polygons: p.use_smooth = True
    objs.append(nz)
    objs.append(decal("pump_label", (R + 0.004) * C, 1.4 * C, (H - 0.6) * C, 1.45, label_img, ink(label_img, 0.35)))
    return objs


# ------------------------------------------------------------------ sets
def area(name, loc, rot, size, power, col=(1, 1, 1), shape="RECTANGLE", sy=None, visible_glossy=True):
    d = bpy.data.lights.new(name, "AREA"); d.energy = power; d.color = col; d.shape = shape
    d.size = size; d.size_y = sy if sy else size
    o = bpy.data.objects.new(name, d); bpy.context.collection.objects.link(o)
    o.location = loc; o.rotation_euler = rot
    o.visible_camera = False
    return o


def look_at(o, target):
    d = Vector(target) - o.location; o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def sweep(col, rough=0.55):
    m, _ = P("sweep", base=col, rough=rough)
    prof = [(-1.5, -1.0, 0)]
    pts = [(y, z) for y, z in [(-1.2, 0), (0.25, 0)]] + [(0.25 + 0.35 * math.sin(k / 16 * math.pi / 2), 0.35 * (1 - math.cos(k / 16 * math.pi / 2))) for k in range(1, 17)] + [(0.6, 2.0)]
    me = bpy.data.meshes.new("sweep"); bm = bmesh.new()
    rows = []
    for y, z in pts:
        rows.append([bm.verts.new((x, y, z)) for x in (-2.0, 2.0)])
    for j in range(len(rows) - 1):
        bm.faces.new((rows[j][0], rows[j][1], rows[j + 1][1], rows[j + 1][0]))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("sweep", me); bpy.context.collection.objects.link(ob); me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    return ob


def plinth(w, d, h, x=0, y=0):
    m, b = P("stone", base=(0.83, 0.79, 0.72), rough=0.7)
    nt = m.node_tree; tc = nt.nodes.new("ShaderNodeNewGeometry"); tc.outputs["Position"].name
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 9; nz.inputs["Detail"].default_value = 10; nz.inputs["Roughness"].default_value = 0.65
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1, 6, 1)
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.60, 0.53, 0.44, 1); ramp.color_ramp.elements[1].color = (0.86, 0.81, 0.73, 1); ramp.color_ramp.elements[0].position = 0.35; ramp.color_ramp.elements[1].position = 0.62
    vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 260
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.0006
    nt.links.new(tc.outputs["Position"], mp.inputs[0]); nt.links.new(mp.outputs[0], nz.inputs[0]); nt.links.new(nz.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], b.inputs["Base Color"]); nt.links.new(tc.outputs["Position"], vor.inputs[0])
    nt.links.new(vor.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, -h / 2)); o = bpy.context.active_object
    o.scale = (w, d, h); bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.003; bv.segments = 3
    o.data.materials.append(m); return o


def leaves(n=14, seed=3, toward=(-0.5, -0.6, 0.62), dist=0.42):
    import random
    random.seed(seed)
    m, _ = P("leaf", base=(0.1, 0.12, 0.1), rough=0.8)
    obs = []
    for i in range(n):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1)
        o = bpy.context.active_object
        o.scale = (0.026 + random.random() * .018, 0.010 + random.random() * .006, 0.002)
        tv = Vector(toward).normalized() * dist; wp = Vector((random.uniform(-0.05, 0.42), 0.6, random.uniform(0.16, 0.42))); o.location = wp + tv
        o.rotation_euler = (random.uniform(-.4, .4), random.uniform(-.4, .4), random.uniform(0, 3.14))
        o.visible_camera = False; o.visible_glossy = False; o.visible_transmission = False
        o.data.materials.append(m); obs.append(o)
    return obs


def camera(loc, target, lens=90, fstop=8.0, focus=None):
    cd = bpy.data.cameras.new("cam"); cd.lens = lens
    o = bpy.data.objects.new("cam", cd); bpy.context.collection.objects.link(o)
    o.location = loc; look_at(o, target); bpy.context.scene.camera = o
    cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    cd.dof.focus_distance = focus if focus else (Vector(target) - Vector(loc)).length
    return o
