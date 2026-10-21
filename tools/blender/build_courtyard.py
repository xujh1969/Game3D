"""Build first production architecture; preserve modular source before joining export batches."""
import bpy
import math
import random
import sys
from pathlib import Path

import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_door as door

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source/ARCH_Courtyard_v002.blend"
GAME = ROOT / "assets/game/ARCH_Courtyard_v002_game.glb"
TEXTURES = ROOT / "assets/source/materials/Courtyard_v002"
random.seed(22004)


def pbr(name, color, seed, roughness):
    """Deterministic project-authored tileable mineral textures, no external inputs."""
    size = 512
    rng = np.random.default_rng(seed)
    noise = np.zeros((size, size), dtype=np.float32)
    # Periodic value noise has no preferred diagonal direction, unlike summed waves.
    for frequency, amplitude in [(2,.34),(4,.20),(8,.14),(16,.10),(32,.07),(64,.05),(128,.035)]:
        grid = rng.uniform(-1, 1, (frequency, frequency)).astype(np.float32)
        co = np.arange(size, dtype=np.float32) * frequency / size
        index = co.astype(int)
        t = co - index
        blend = t*t*(3-2*t)
        a = grid[index[:,None] % frequency, index[None,:] % frequency]
        b = grid[index[:,None] % frequency, (index[None,:]+1) % frequency]
        c = grid[(index[:,None]+1) % frequency, index[None,:] % frequency]
        d = grid[(index[:,None]+1) % frequency, (index[None,:]+1) % frequency]
        noise += amplitude * ((a*(1-blend[None,:])+b*blend[None,:])*(1-blend[:,None]) + (c*(1-blend[None,:])+d*blend[None,:])*blend[:,None])
    noise += rng.normal(0, .018, (size, size)).astype(np.float32)
    height = noise * .15
    dx = (np.roll(height, -1, 1) - np.roll(height, 1, 1)) * 2
    dy = (np.roll(height, -1, 0) - np.roll(height, 1, 0)) * 2
    normal = np.stack([-dx, -dy, np.ones_like(dx)], axis=-1)
    normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
    channels = {
        "BaseColor": np.clip(np.array(color)[None, None, :] * (1 + noise[:, :, None] * .30), .01, .95),
        "Roughness": np.repeat(np.clip(roughness + noise[:, :, None] * .10, .1, 1), 3, 2),
        "Normal": normal * .5 + .5,
    }
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    for channel, rgb in channels.items():
        img = bpy.data.images.new(name + "_" + channel, width=size, height=size)
        img.colorspace_settings.name = "sRGB" if channel == "BaseColor" else "Non-Color"
        rgba = np.concatenate([rgb, np.ones((size, size, 1))], axis=-1).astype(np.float32)
        img.pixels.foreach_set(rgba.ravel())
        img.filepath_raw = str(TEXTURES / (img.name + ".png"))
        img.file_format = "PNG"
        img.save()
        img.pack()
        tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex.image = img
        if channel == "Normal":
            convert = mat.node_tree.nodes.new("ShaderNodeNormalMap")
            convert.inputs["Strength"].default_value = .25
            mat.node_tree.links.new(tex.outputs["Color"], convert.inputs["Color"])
            mat.node_tree.links.new(convert.outputs["Normal"], shader.inputs["Normal"])
        else:
            mat.node_tree.links.new(tex.outputs["Color"], shader.inputs[channel if channel != "BaseColor" else "Base Color"])
    return mat


def mineral_uv(obj, scale=1.0):
    uv = obj.data.uv_layers.active or obj.data.uv_layers.new()
    for face in obj.data.polygons:
        axes = [i for i in range(3) if i != max(range(3), key=lambda i: abs(face.normal[i]))]
        for index in face.loop_indices:
            co = obj.data.vertices[obj.data.loops[index].vertex_index].co
            uv.data[index].uv = (co[axes[0]] / scale, co[axes[1]] / scale)


def main():
    if SOURCE.exists() or GAME.exists():
        raise FileExistsError("Preserve v002; use a new version for revisions")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    TEXTURES.mkdir(parents=True, exist_ok=True)
    wood, unused_bronze = door.materials()
    stone = pbr("Courtyard_Gray_Stone", (.28, .31, .29), 11, .87)
    plaster = pbr("Courtyard_Lime_Plaster", (.67, .63, .54), 12, .96)
    tile = pbr("Courtyard_Fired_Gray_Tile", (.14, .17, .18), 13, .82)
    earth = pbr("Courtyard_Earth", (.20, .22, .15), 14, .98)
    root = door.empty("CourtyardArchitecture")
    groups = {}
    for name in ["ARCH_001_Timber", "ARCH_002_Roof", "ARCH_004_Masonry", "ARCH_004_Windows", "Paving", "Ground", "Boundary"]:
        groups[name] = door.empty(name)
        groups[name].parent = root

    def box(label, pos, dims, group, mat, grain="Z", bevel=.01):
        obj = door.box(label, pos, dims, groups[group], mat, grain, bevel)
        if mat != wood:
            mineral_uv(obj)
        return obj

    # Coordinates (Godot X, -Godot Z, Godot Y); door at (0, 8, .3) is separate.
    box("Earth_30m", (0, 0, -.04), (30, 30, .08), "Ground", earth)
    box("Stone_Platform", (0, 9.3, .15), (12, 8, .30), "ARCH_004_Masonry", stone, bevel=.025)
    box("Step_Lower", (0, 4.8, .075), (3.8, .65, .15), "ARCH_004_Masonry", stone, bevel=.012)
    box("Step_Upper", (0, 5.15, .15), (3.8, .5, .30), "ARCH_004_Masonry", stone, bevel=.012)
    # Stone seams and the plinth upper lip are geometry, no painted illumination.
    for x in np.arange(-5.5, 5.6, 1.0):
        box("Plinth_Coping", (float(x), 5.30, .28), (.985, .22, .10), "ARCH_004_Masonry", stone)
    for x in [-5.4, -1.8, 1.8, 5.4]:
        for y in [6.8, 11.8]:
            box("Post_Foot", (x, y, .40), (.42, .42, .20), "ARCH_004_Masonry", stone, bevel=.02)
            # Rounded timber posts, capped by rectangular beam seats.
            obj = door.cylinder("Timber_Post", (x, y, 1.86), .15, 2.92, groups["ARCH_001_Timber"], wood)
            box("Post_Cap", (x, y, 3.28), (.38, .34, .16), "ARCH_001_Timber", wood)
        box("Cross_Tie", (x, 9.3, 3.40), (.22, 5.7, .24), "ARCH_001_Timber", wood, "X")
        for end in [6.6, 12.0]:
            box("Eave_Bearing_Block", (x, end, 3.43), (.44, .58, .16), "ARCH_001_Timber", wood)
    for y in [6.8, 11.8]:
        box("Longitudinal_Beam", (0, y, 3.22), (11.5, .28, .30), "ARCH_001_Timber", wood, "X")
    for y, z in [(6.35, 3.50), (7.8, 4.12), (9.3, 4.70), (10.8, 4.12), (12.35, 3.50)]:
        box("Roof_Purlin", (0, y, z), (12.25, .17, .17), "ARCH_001_Timber", wood, "X")
    for side in [-1, 1]:
        # Front wall panels leave real window holes and a clear 2.24m door opening.
        x = side * 3.31
        for z, height in [(.75, .90), (2.86, .52)]:
            box("Front_Plaster_Panel", (x, 8, z), (4.38, .20, height), "ARCH_004_Masonry", plaster)
        for offset in [-1.53, 1.53]:
            box("Window_Side_Panel", (x + offset, 8, 1.90), (1.32, .20, 1.40), "ARCH_004_Masonry", plaster)
        for offset in [-.94, .94]:
            box("Window_Jamb", (x + offset, 7.86, 1.90), (.10, .15, 1.50), "ARCH_004_Windows", wood)
        for z in [1.16, 2.64]:
            box("Window_Sill", (x, 7.84, z), (1.98, .22, .10), "ARCH_004_Windows", wood, "X")
        for offset in [-.72, -.48, -.24, 0, .24, .48, .72]:
            box("Window_Vertical_Lattice", (x + offset, 7.86, 1.90), (.026, .06, 1.40), "ARCH_004_Windows", wood, bevel=.003)
        for z in [1.42, 1.66, 1.90, 2.14, 2.38]:
            box("Window_Horizontal_Lattice", (x, 7.85, z), (1.80, .06, .026), "ARCH_004_Windows", wood, "X", .003)
        box("Rear_Plaster_Panel", (x, 11.6, 1.65), (4.38, .20, 2.70), "ARCH_004_Masonry", plaster)
        box("End_Plaster_Wall", (side * 5.5, 9.8, 1.65), (.20, 3.8, 2.70), "ARCH_004_Masonry", plaster)
        # Low wall closes the side route at the facade; it is also collidable in Godot.
        box("Cross_Courtyard_Wall", (side * 10.25, 8, .90), (9.5, .30, 1.80), "Boundary", plaster)
        box("Cross_Wall_Coping", (side * 10.25, 8, 1.83), (9.5, .46, .12), "Boundary", tile)
    box("Door_Head_Infill", (0, 8, 3.06), (2.24, .20, .20), "ARCH_004_Masonry", plaster)
    # Roof beds and actual overlapping concave pan / convex cover tiles.
    vertices, faces, uvs = [], [], []
    for side in [-1, 1]:
        end_y = 6.1 if side == -1 else 12.8
        delta_y = 9.3 - end_y
        slope = Vector((0, delta_y, 1.5)).normalized()
        normal = Vector((0, -slope.z * (1 if delta_y > 0 else -1), abs(slope.y)))
        length = math.hypot(delta_y, 1.5)
        for x in np.linspace(-5.9, 5.9, 30):
            obj = box("Exposed_Rafter", (float(x), (end_y + 9.3)/2, 4.04), (.075, length+.15, .10), "ARCH_001_Timber", wood)
            obj.rotation_euler.x = math.atan2(1.5, delta_y) if delta_y > 0 else -math.atan2(1.5, -delta_y)
        # Solid roof substrate supports the tiles and avoids light leaking.
        mesh = bpy.data.meshes.new("Roof_Bed")
        mesh.from_pydata([(-6.4, end_y, 3.39), (6.4, end_y, 3.39), (6.4, 9.3, 4.89), (-6.4, 9.3, 4.89)], [], [(0,1,2,3)] if side == -1 else [(3,2,1,0)])
        mesh.update()
        obj = bpy.data.objects.new("Roof_Bed", mesh)
        bpy.context.collection.objects.link(obj)
        obj.parent = groups["ARCH_002_Roof"]
        obj.data.materials.append(tile)
        mineral_uv(obj)
        thick = obj.modifiers.new("Roof_Bed_Thickness", "SOLIDIFY")
        thick.thickness = .07
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=thick.name)
        for col in range(53):
            for row in range(12):
                start = Vector((-6.36 + col*.24, end_y, 3.43)) + slope*(row*length/12)
                for cover in [False, True]:
                    width = .126 if not cover else .056
                    offset = 0 if not cover else .12
                    base = len(vertices)
                    for along in [0, length/12+.085]:
                        for sample in range(7):
                            theta = sample/6*math.pi
                            across = -math.cos(theta)*width
                            rise = (.025 - math.sin(theta)*.035) if not cover else math.sin(theta)*.065+.018
                            co = start + Vector((across+offset, 0, 0)) + slope*along + normal*rise
                            vertices.append(tuple(co))
                            uvs.append((float(col)*.19+sample/6*.22, row*.23+along))
                    for sample in range(6):
                        a=base+sample
                        face=(a,a+1,a+8,a+7)
                        faces.append(face if side == -1 else tuple(reversed(face)))
    mesh = bpy.data.meshes.new("Pan_And_Cover_Tiles")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Overlapping_Gray_Tiles", mesh)
    bpy.context.collection.objects.link(obj)
    obj.parent = groups["ARCH_002_Roof"]
    obj.data.materials.append(tile)
    uv = mesh.uv_layers.new()
    for face in mesh.polygons:
        face.use_smooth=True
        for loop in face.loop_indices:
            uv.data[loop].uv=uvs[mesh.loops[loop].vertex_index]
    box("Ridge_Bed", (0, 9.3, 4.95), (12.9, .28, .13), "ARCH_002_Roof", tile)
    for i in range(44):
        obj = door.cylinder("Ridge_Cap", (-6.45+i*.30, 9.3, 5.01), .14, .31, groups["ARCH_002_Roof"], tile, (0, math.pi/2, 0))
    for x in [-.6, 0, .6]:
        for row in range(29):
            # Flush top at floor level; paving is visible but does not need individual colliders.
            obj = box("Path_Stone", (x, -12.5+row*.60, -.012), (.575, .575, .055), "Paving", stone, bevel=.012)
            obj.rotation_euler.z = random.uniform(-.012, .012)
    for x, y, dims in [(-15.0, 0, (.35,30,1.8)), (15.0,0,(.35,30,1.8)), (0,15.0,(30,.35,1.8)), (0,-15.0,(30,.35,1.8))]:
        box("Boundary_Plaster", (x,y,.9), dims, "Boundary", plaster)
        box("Boundary_Base", (x,y,.15), (dims[0]+.05,dims[1]+.05,.30), "Boundary", stone)
        box("Boundary_Coping", (x,y,1.83), (dims[0]+.12,dims[1]+.12,.12), "Boundary", tile)
    # Preserve editable construction modules and packed source maps before batching.
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    for parent in groups.values():
        door.join_parts(parent)
    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active=root
    bpy.ops.export_scene.gltf(filepath=str(GAME), export_format="GLB", use_selection=True, export_yup=True, export_animations=False)
    print("COURTYARD_BUILD: " + str(GAME))


if __name__ == "__main__":
    main()
