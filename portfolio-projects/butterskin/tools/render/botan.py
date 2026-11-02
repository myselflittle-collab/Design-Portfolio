"""Botanical set pieces: leaves, stones, moss, flowers, warm backdrop (Blender/Cycles)."""
import bpy, bmesh, math, random
from mathutils import Vector, Euler
from scene import P, look_at

rng = random.Random(7)


def leaf_mat(name, base=(0.07, 0.20, 0.07), tip=(0.16, 0.34, 0.11)):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; out = nt.nodes["Material Output"]
    b.inputs["Roughness"].default_value = 0.42; b.inputs["Coat Weight"].default_value = 0.25; b.inputs["Coat Roughness"].default_value = 0.25
    uv = nt.nodes.new("ShaderNodeUVMap"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(uv.outputs[0], sep.inputs[0])
    # midrib lighter + gradient along length
    ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"; nt.links.new(sep.outputs[0], ab.inputs[0])
    rib = nt.nodes.new("ShaderNodeMapRange"); rib.inputs[1].default_value = 0.0; rib.inputs[2].default_value = 0.035; rib.inputs[3].default_value = 1; rib.inputs[4].default_value = 0
    nt.links.new(ab.outputs[0], rib.inputs[0])
    grad = nt.nodes.new("ShaderNodeMix"); grad.data_type = "RGBA"; grad.inputs["A"].default_value = (*base, 1); grad.inputs["B"].default_value = (*tip, 1)
    nt.links.new(sep.outputs[1], grad.inputs["Factor"])
    rc = nt.nodes.new("ShaderNodeMix"); rc.data_type = "RGBA"; rc.inputs["B"].default_value = (0.42, 0.52, 0.25, 1)
    nt.links.new(grad.outputs["Result"], rc.inputs["A"]); nt.links.new(rib.outputs[0], rc.inputs["Factor"])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 30
    mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs["Factor"].default_value = 0.25
    nt.links.new(rc.outputs["Result"], mul.inputs["A"]); nt.links.new(nz.outputs["Color"], mul.inputs["B"])
    nt.links.new(mul.outputs["Result"], b.inputs["Base Color"])
    # lateral veins as bump
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 2.2; wv.inputs["Distortion"].default_value = 1.5
    comb = nt.nodes.new("ShaderNodeCombineXYZ"); add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"
    mlt = nt.nodes.new("ShaderNodeMath"); mlt.operation = "MULTIPLY"; mlt.inputs[1].default_value = 0.6
    nt.links.new(ab.outputs[0], mlt.inputs[0]); nt.links.new(mlt.outputs[0], add.inputs[0]); nt.links.new(sep.outputs[1], add.inputs[1])
    nt.links.new(add.outputs[0], comb.inputs[0]); nt.links.new(comb.outputs[0], wv.inputs[0])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.18; bp.inputs["Distance"].default_value = 0.0004
    nt.links.new(wv.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    tr = nt.nodes.new("ShaderNodeBsdfTranslucent"); nt.links.new(mul.outputs["Result"], tr.inputs["Color"])
    mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.35
    nt.links.new(b.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    return m


def leaf(L, W, mat, droop=0.25, fold=0.22, twist=0.0, nl=28, nw=10, pointy=1.0):
    me = bpy.data.meshes.new("leaf"); bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    grid = []
    for i in range(nl + 1):
        u = i / nl
        w = W * (math.sin(math.pi * min(1, u ** 0.85)) ** (0.75 * pointy)) * (1 - 0.1 * u)
        row = []
        for j in range(nw + 1):
            v = -1 + 2 * j / nw
            x = v * w; y = u * L
            z = fold * abs(v) * w + droop * L * u * u + twist * v * w * u
            row.append((bm.verts.new((x, y, z)), (v * 0.5, u)))
        grid.append(row)
    for i in range(nl):
        for j in range(nw):
            a, b, c, d = grid[i][j], grid[i][j + 1], grid[i + 1][j + 1], grid[i + 1][j]
            f = bm.faces.new((a[0], b[0], c[0], d[0]))
            for lp, (_, uv) in zip(f.loops, (a, b, c, d)): lp[uvl].uv = uv
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("leaf", me); bpy.context.collection.objects.link(o)
    for p in me.polygons: p.use_smooth = True
    me.materials.append(mat)
    sol = o.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.0004
    return o


def sprig(origin, yaw, mat, n=5, L=(0.07, 0.11), W=(0.022, 0.034), spread=70, pitch=(10, 55), droop=0.3, seed=0):
    r = random.Random(seed); obs = []
    for k in range(n):
        o = leaf(r.uniform(*L), r.uniform(*W), mat, droop=r.uniform(droop * .6, droop * 1.3), fold=r.uniform(.12, .3), twist=r.uniform(-.2, .2))
        o.location = origin
        o.rotation_euler = Euler((math.radians(r.uniform(*pitch)), 0, math.radians(yaw + r.uniform(-spread / 2, spread / 2))), "ZXY")
        # leaf grows along +Y; rotate so it points outward
        obs.append(o)
    return obs


def stone_mat(name="limestone", c1=(0.30, 0.27, 0.22), c2=(0.58, 0.53, 0.45)):
    m, b = P(name, base=(0.8, 0.76, 0.7), rough=0.82)
    nt = m.node_tree; geo = nt.nodes.new("ShaderNodeNewGeometry")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 30; nz.inputs["Detail"].default_value = 14; nz.inputs["Roughness"].default_value = 0.62
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (*c1, 1); ramp.color_ramp.elements[1].color = (*c2, 1)
    ramp.color_ramp.elements[0].position = .35; ramp.color_ramp.elements[1].position = .65
    nt.links.new(geo.outputs["Position"], nz.inputs[0]); nt.links.new(nz.outputs[0], ramp.inputs[0]); nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
    vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 60
    nz2 = nt.nodes.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 90; nz2.inputs["Detail"].default_value = 8
    add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"
    nt.links.new(geo.outputs["Position"], vor.inputs[0]); nt.links.new(geo.outputs["Position"], nz2.inputs[0])
    nt.links.new(vor.outputs["Distance"], add.inputs[0]); nt.links.new(nz2.outputs[0], add.inputs[1])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.0012
    nt.links.new(add.outputs[0], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    return m


def rock(loc, scale, mat, seed=1, flat_top=False):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=1, location=loc)
    o = bpy.context.active_object
    for v in o.data.vertices: v.co.x *= scale[0]; v.co.y *= scale[1]; v.co.z *= scale[2]
    m = max(scale)
    tex = bpy.data.textures.new(f"rk{seed}", "CLOUDS"); tex.noise_scale = m * 0.9; tex.noise_depth = 2
    d = o.modifiers.new("d", "DISPLACE"); d.texture = tex; d.strength = m * 0.45
    tex2 = bpy.data.textures.new(f"rn{seed}", "CLOUDS"); tex2.noise_scale = m * 0.22; tex2.noise_depth = 6
    d2 = o.modifiers.new("d2", "DISPLACE"); d2.texture = tex2; d2.strength = m * 0.07
    o.rotation_euler = (0, 0, seed * 1.3)
    for p in o.data.polygons: p.use_smooth = True
    o.data.materials.append(mat)
    return o


def slab(w, d, h, mat, loc=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1], loc[2] - h / 2)); o = bpy.context.active_object
    o.scale = (w, d, h); bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.004; bv.segments = 4; bv.use_clamp_overlap = True
    o.data.materials.append(mat); return o


def moss(loc, rx, ry, h=0.011, density=9000, seed=3):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=loc)
    o = bpy.context.active_object
    for v in o.data.vertices: v.co.x *= rx; v.co.y *= ry; v.co.z *= h
    tex = bpy.data.textures.new(f"ms{seed}", "CLOUDS"); tex.noise_scale = 0.012
    dm = o.modifiers.new("d", "DISPLACE"); dm.texture = tex; dm.strength = 0.004
    m, b = P(f"moss{seed}", base=(0.08, 0.14, 0.03), rough=0.9)
    o.data.materials.append(m)
    ps = o.modifiers.new("hair", "PARTICLE_SYSTEM"); st = ps.particle_system.settings
    st.type = "HAIR"; st.count = density; st.hair_length = 0.006; st.use_advanced_hair = False
    st.root_radius = 0.00018 / 0.0035 if False else 1.0
    try:
        st.radius_scale = 0.00025; st.root_radius = 1.0; st.tip_radius = 0.2
    except Exception: pass
    st.factor_random = 0.0; st.brownian_factor = 0.0; st.rendered_child_count = 0; st.length_random = 0.5 if hasattr(st, "length_random") else 0
    ps.particle_system.seed = seed
    hm, hb = P(f"mosshair{seed}", base=(0.13, 0.20, 0.045), rough=0.8)
    o.data.materials.append(hm); st.material = 2
    return o


def flower(loc, size=0.009, seed=0, tilt=(0, 0)):
    r = random.Random(seed)
    m, _ = P("petal", base=(0.96, 0.95, 0.9), rough=0.5, sss=0.4, sss_r=(0.003, 0.003, 0.003))
    c, _ = P("stamen", base=(0.85, 0.62, 0.12), rough=0.6)
    obs = []
    for k in range(5):
        o = leaf(size, size * .6, m, droop=0.08, fold=0.06, nl=10, nw=6, pointy=0.35)
        o.modifiers.clear()
        o.location = loc; o.rotation_euler = Euler((math.radians(tilt[0] + 14), math.radians(tilt[1]), math.radians(k * 72 + r.uniform(-8, 8))), "ZXY")
        obs.append(o)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=size * .2, location=(loc[0], loc[1], loc[2] + size * .1))
    s = bpy.context.active_object; s.scale.z = .6; s.data.materials.append(c); obs.append(s)
    return obs


def backdrop(col_top=(0.62, 0.58, 0.44), col_bot=(0.80, 0.74, 0.58), y=0.9, size=3):
    m = bpy.data.materials.new("bd"); m.use_nodes = True; nt = m.node_tree
    em = nt.nodes.new("ShaderNodeEmission"); tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (*col_bot, 1); ramp.color_ramp.elements[1].color = (*col_top, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs[1], ramp.inputs[0]); nt.links.new(ramp.outputs[0], em.inputs[0])
    em.inputs[1].default_value = 1.0
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, y, 0.4), rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object; o.data.materials.append(m)
    o.visible_shadow = False; o.visible_diffuse = True; o.visible_glossy = True
    return o


def bokeh(n=40, y=0.85, seed=5, col=(1.0, 0.86, 0.6), strength=6.0):
    r = random.Random(seed); m = bpy.data.materials.new("bok"); m.use_nodes = True; nt = m.node_tree
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*col, 1); em.inputs[1].default_value = strength
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs[0])
    for i in range(n):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=r.uniform(0.004, 0.012), location=(r.uniform(-0.6, 0.6), y + r.uniform(-0.1, 0.1), r.uniform(0.12, 0.6)))
        o = bpy.context.active_object; o.data.materials.append(m); o.visible_shadow = False; o.visible_diffuse = False


def foliage_bg(mat, n=40, y=0.7, seed=9):
    r = random.Random(seed)
    for i in range(n):
        o = leaf(r.uniform(0.10, 0.2), r.uniform(0.03, 0.06), mat, droop=r.uniform(.1, .4), fold=.2)
        o.location = (r.uniform(-0.7, 0.7), y + r.uniform(-0.15, 0.15), r.uniform(-0.05, 0.25))
        o.rotation_euler = Euler((math.radians(r.uniform(40, 85)), 0, math.radians(r.uniform(120, 240))), "ZXY")


def moss_clump(center, spread, n=9, seed=1, density=2500):
    r = random.Random(seed); obs = []
    for i in range(n):
        a = r.uniform(0, 6.28); d = r.uniform(0, 1) ** 0.7
        x = center[0] + math.cos(a) * d * spread[0]; y = center[1] + math.sin(a) * d * spread[1]
        rr = r.uniform(0.012, 0.024) * (1.2 - 0.5 * d)
        obs.append(moss((x, y, center[2]), rr * r.uniform(1, 1.4), rr, h=rr * r.uniform(0.35, 0.6), density=int(density * rr / 0.018), seed=seed * 100 + i))
    return obs
