"""Measured composition proposal for review. No runtime export or game replacement."""
import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source/ENV_Courtyard_Composition_DRAFT_v001.blend"
OUT = ROOT / "handoff/reference/environments"
random.seed(2201)


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    mat.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (*color, 1)
    mat.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 0.9
    return mat


def box(name, position, dimensions, mat, bevel=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    if bevel:
        modifier = obj.modifiers.new("DRAFT_Edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 1
        obj.modifiers.new("DRAFT_Normals", "WEIGHTED_NORMAL")
    return obj


def main():
    if SOURCE.exists():
        raise FileExistsError("Preserve existing draft; create a new version")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    OUT.mkdir(parents=True, exist_ok=True)
    wood = material("DRAFT_Timber", (0.10, 0.055, 0.027))
    plaster = material("DRAFT_Plaster", (0.56, 0.53, 0.44))
    stone = material("DRAFT_Stone", (0.23, 0.25, 0.23))
    ground = material("DRAFT_Earth", (0.12, 0.14, 0.10))
    tile = material("DRAFT_Gray_Roof", (0.10, 0.125, 0.13))
    bamboo = material("DRAFT_Bamboo", (0.09, 0.15, 0.065))
    # Blender coordinates: (Godot X, -Godot Z, Godot Y).
    box("DRAFT_30m_Courtyard", (0, 0, -0.15), (30, 30, 0.30), ground)
    box("DRAFT_12x8m_Platform", (0, 9.3, 0.15), (12, 8, 0.30), stone)
    box("DRAFT_Lower_Step", (0, 4.7, 0.075), (3.8, 0.8, 0.15), stone)
    box("DRAFT_Upper_Step", (0, 5.1, 0.15), (3.8, 0.5, 0.30), stone)
    for x in [-14.8, 14.8]:
        box("DRAFT_Side_Wall", (x, 0, 0.9), (0.35, 30, 1.8), plaster)
    box("DRAFT_North_Wall", (0, 14.8, 0.9), (30, 0.35, 1.8), plaster)
    for x in [-5.4, -1.8, 1.8, 5.4]:
        for y in [6.8, 11.8]:
            box("DRAFT_Post_Base", (x, y, 0.38), (0.42, 0.42, 0.16), stone)
            box("DRAFT_Timber_Post", (x, y, 1.83), (0.24, 0.24, 3.06), wood)
    for y in [6.8, 11.8]:
        box("DRAFT_Tie_Beam", (0, y, 3.25), (11.4, 0.28, 0.26), wood)
    for x in [-5.4, -1.8, 1.8, 5.4]:
        box("DRAFT_Rafter_Tie", (x, 9.3, 3.35), (0.20, 5.6, 0.22), wood)
    for x in [-3.26, 3.26]:
        box("DRAFT_Front_Wall", (x, 8, 1.6), (4.28, 0.18, 2.6), plaster)
        box("DRAFT_Rear_Wall", (x, 11.6, 1.6), (4.28, 0.18, 2.6), plaster)
        # Framed lattice windows are massing guides, not finished modules.
        box("DRAFT_Window_Dark_Inset", (x, 7.89, 1.80), (1.75, 0.04, 1.20), wood)
        for offset in [-0.6, -0.3, 0, 0.3, 0.6]:
            box("DRAFT_Window_Bar", (x + offset, 7.85, 1.8), (0.035, 0.04, 1.15), plaster, 0.003)
        for height in [1.3, 1.8, 2.3]:
            box("DRAFT_Window_Bar", (x, 7.85, height), (1.7, 0.04, 0.035), plaster, 0.003)
    for x in [-5.5, 5.5]:
        box("DRAFT_End_Wall", (x, 9.8, 1.6), (0.18, 3.6, 2.6), plaster)
    # Reuse the approved-direction door without changing its source asset.
    bpy.ops.import_scene.gltf(filepath=str(ROOT / "assets/game/ARCH_003_DoorSong_v003_game.glb"))
    door_root = bpy.data.objects.get("DoorSong")
    door_root.location = (0, 8, 0.3)
    for side in [-1, 1]:
        front_y, ridge_y, back_y = 6.1, 9.3, 12.8
        end_y = front_y if side == -1 else back_y
        mesh = bpy.data.meshes.new("DRAFT_Roof_Surface")
        mesh.from_pydata([(-6.4, end_y, 3.35), (6.4, end_y, 3.35), (6.4, ridge_y, 4.85), (-6.4, ridge_y, 4.85)], [], [(0, 1, 2, 3)])
        mesh.update()
        obj = bpy.data.objects.new("DRAFT_Roof_Plane", mesh)
        bpy.context.collection.objects.link(obj)
        obj.data.materials.append(tile)
        solid = obj.modifiers.new("DRAFT_Roof_Thickness", "SOLIDIFY")
        solid.thickness = 0.10
        for row in range(18):
            t = row / 18
            y = end_y + (ridge_y - end_y) * t
            z = 3.35 + 1.5 * t + 0.025
            box("DRAFT_Tile_Row", (0, y, z), (12.85, 0.035, 0.035), tile, 0.005)
    box("DRAFT_Ridge", (0, 9.3, 4.90), (12.8, 0.14, 0.12), tile)
    for x in [-0.6, 0, 0.6]:
        for row in range(29):
            y = -12.5 + row * 0.60
            box("DRAFT_Central_Paving", (x, y, 0.015), (0.57, 0.57, 0.05), stone, 0.015)
    # Explicit natural-asset proxies; final rocks and bamboo are separate tasks.
    for x, y, radius in [(-8, 0, 1.0), (8, 6, 0.8), (-9, 10, 0.7)]:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=radius, location=(x, y, radius * 0.4))
        obj = bpy.context.object
        obj.name = "DRAFT_Rock_Proxy"
        obj.scale = (1.2, 0.9, 0.7)
        obj.data.materials.append(stone)
    for base_x, base_y in [(-11, 5), (11, 9), (-12, -2)]:
        for index in range(9):
            x, y = base_x + random.uniform(-1.4, 1.4), base_y + random.uniform(-1.4, 1.4)
            height = random.uniform(2.5, 4.2)
            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.035, depth=height, location=(x, y, height / 2))
            bpy.context.object.name = "DRAFT_Bamboo_Stem_Proxy"
            bpy.context.object.data.materials.append(bamboo)
    # Sun and neutral fill establish legible massing, not final environment lighting.
    light_data = bpy.data.lights.new("DRAFT_Morning_Sun", "SUN")
    light_data.energy = 2.0
    light_data.angle = math.radians(6)
    light_data.color = (1.0, 0.88, 0.72)
    sun = bpy.data.objects.new("DRAFT_Morning_Sun", light_data)
    bpy.context.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(30), math.radians(-25), math.radians(-35))
    scene = bpy.context.scene
    scene.world = bpy.data.worlds.new("DRAFT_Neutral_Fill")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value = (0.55, 0.65, 0.74, 1)
    scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.4
    bpy.ops.object.camera_add(location=(7, -9, 3.0))
    camera = bpy.context.object
    camera.rotation_euler = (Vector((0, 8.5, 2.0)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 38
    scene.camera = camera
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1440
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    scene.render.filepath = str(OUT / "ENV_Composition_DRAFT_v001_main.png")
    bpy.ops.render.render(write_still=True)
    camera.location = (0, -13, 1.6)
    camera.rotation_euler = (Vector((0, 8.5, 1.8)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = str(OUT / "ENV_Composition_DRAFT_v001_entrance.png")
    bpy.ops.render.render(write_still=True)
    print("COURTYARD_DRAFT: rendered proposal only; no game asset exported")


if __name__ == "__main__":
    main()
