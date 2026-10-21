"""Reproducible ARCH_003 v003. Run with Blender --background --python-exit-code 1 --python."""
import bpy
import math
import random
from pathlib import Path

from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source/ARCH_003_DoorSong_v003.blend"
GAME = ROOT / "assets/game/ARCH_003_DoorSong_v003_game.glb"
TEX = ROOT / "assets/source/third_party/fine_grained_wood"
RENDERS = ROOT / "reports/screenshots"
random.seed(31003)


def image_file(name, filename, color=True):
    image = bpy.data.images.load(str(TEX / filename))
    image.name = name
    image.colorspace_settings.name = "sRGB" if color else "Non-Color"
    image.pack()
    return image


def materials():
    # Unmodified CC0 source maps; provenance.json records original URLs and MD5.
    base_image = image_file("ARCH_003_Wood_BaseColor", "fine_grained_wood_col_1k.png")
    rough_image = image_file("ARCH_003_Wood_Roughness", "fine_grained_wood_rough_1k.png", False)
    normal_image = image_file("ARCH_003_Wood_Normal", "fine_grained_wood_nor_gl_1k.png", False)
    wood = bpy.data.materials.new("ARCH_003_Aged_Timber_PBR")
    wood.use_nodes = True
    nodes, links = wood.node_tree.nodes, wood.node_tree.links
    shader = nodes.get("Principled BSDF")
    for image, socket in [(base_image, "Base Color"), (rough_image, "Roughness")]:
        texture = nodes.new("ShaderNodeTexImage")
        texture.image = image
        links.new(texture.outputs["Color"], shader.inputs[socket])
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = normal_image
    converter = nodes.new("ShaderNodeNormalMap")
    converter.inputs["Strength"].default_value = 0.8
    links.new(texture.outputs["Color"], converter.inputs["Color"])
    links.new(converter.outputs["Normal"], shader.inputs["Normal"])
    bronze = bpy.data.materials.new("ARCH_003_Muted_Bronze")
    bronze.use_nodes = True
    shader = bronze.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (0.23, 0.135, 0.052, 1)
    shader.inputs["Metallic"].default_value = 0.85
    shader.inputs["Roughness"].default_value = 0.48
    return wood, bronze


def empty(name, position=(0, 0, 0)):
    obj = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(obj)
    obj.location = position
    return obj


def finish(obj, name, parent, material):
    obj.name = name
    position = obj.location.copy()
    obj.parent = parent
    obj.location = position - parent.location
    obj.data.materials.append(material)
    return obj


def box(name, position, dimensions, parent, material, grain="Z", bevel=0.002):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    obj = bpy.context.object
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    offset_u, offset_v = random.random(), random.random()
    for polygon in obj.data.polygons:
        for loop_index in polygon.loop_indices:
            point = obj.data.vertices[obj.data.loops[loop_index].vertex_index].co
            along = point.z if grain == "Z" else point.x
            across = (point.x if abs(polygon.normal.y) > 0.5 else point.y) if grain == "Z" else (point.z if abs(polygon.normal.y) > 0.5 else point.y)
            obj.data.uv_layers.active.data[loop_index].uv = (across / 0.20 + offset_u, along / 1.4 + offset_v)
    modifier = obj.modifiers.new("Small_Worn_Edges", "BEVEL")
    modifier.width = min(bevel, min(dimensions) * 0.15)
    modifier.segments = 2
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    modifier = obj.modifiers.new("Face_Normals", "WEIGHTED_NORMAL")
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    return finish(obj, name, parent, material)


def cylinder(name, position, radius, depth, parent, material, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=radius, depth=depth, location=position, rotation=rotation)
    obj = bpy.context.object
    for face in obj.data.polygons:
        face.use_smooth = len(face.vertices) == 4
    return finish(obj, name, parent, material)


def join_parts(parent):
    meshes = [obj for obj in parent.children if obj.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = parent.name + "_Geometry"


def build():
    if SOURCE.exists() or GAME.exists():
        raise FileExistsError("v003 already exists; preserve it and build a new version")
    TEX.mkdir(parents=True, exist_ok=True)
    GAME.parent.mkdir(parents=True, exist_ok=True)
    RENDERS.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    wood, bronze = materials()
    root = empty("DoorSong")
    frame = empty("DoorFrame")
    frame.parent = root
    for x in [-1.06, 1.06]:
        box("Jamb", (x, 0, 1.26), (0.12, 0.18, 2.52), frame, wood, bevel=0.004)
    box("Lintel", (0, 0, 2.59), (2.24, 0.186, 0.14), frame, wood, "X", 0.004)
    for name, pivot, sign in [("LeafLeft", -1, 1), ("LeafRight", 1, -1)]:
        leaf = empty(name, (pivot, 0, 0))
        leaf.parent = root

        def timber(label, t, z, width, height, depth=0.09, y=0, grain="Z"):
            return box(label, (pivot + sign * t, y, z), (width, depth, height), leaf, wood, grain)

        for t in [0.05, 0.95]:
            timber("Stile", t, 1.25, 0.075, 2.48)
        for z, height in [(0.06, 0.10), (1.06, 0.12), (2.44, 0.10)]:
            timber("Rail", 0.50, z, 0.83, height, 0.094, grain="X")
        for index in range(4):
            timber("Lower_Panel_Plank", 0.20 + index * 0.20, 0.55, 0.198, 0.88, 0.045)
        for t in [0.10, 0.90]:
            timber("Panel_Moulding", t, 0.55, 0.018, 0.87, 0.061)
        for z in [0.12, 0.98]:
            timber("Panel_Moulding", 0.50, z, 0.79, 0.018, 0.061, grain="X")
        for t in [0.16, 0.84]:
            timber("Grid_Side", t, 1.76, 0.026, 1.20, 0.035)
        for z in [1.17, 2.34]:
            timber("Grid_Border", 0.50, z, 0.70, 0.028, 0.041, grain="X")
        for t in [0.32, 0.68]:
            timber("Grid_Long_Vertical", t, 1.76, 0.025, 1.16, 0.035)
        for z in [1.30, 2.20]:
            timber("Grid_Crossbar", 0.50, z, 0.69, 0.025, 0.039, grain="X")
        for z in [1.40, 2.10]:
            timber("Grid_Center_Link", 0.50, z, 0.026, 0.20, 0.035)
        for z in [1.49, 2.01]:
            timber("Grid_Center_Bridge", 0.50, z, 0.36, 0.025, 0.039, grain="X")
        for z in [0.38, 1.27, 2.20]:
            box("Hinge_Plate", (pivot + sign * 0.025, -0.053, z), (0.05, 0.014, 0.15), leaf, bronze, bevel=0.001)
            cylinder("Hinge_Barrel", (pivot, -0.045, z), 0.016, 0.16, leaf, bronze)
        x = pivot + sign * 0.85
        cylinder("Knocker_Plate", (x, -0.057, 1.06), 0.035, 0.012, leaf, bronze, (math.pi / 2, 0, 0))
        cylinder("Knocker_Pivot", (x, -0.073, 1.06), 0.012, 0.025, leaf, bronze, (math.pi / 2, 0, 0))
        bpy.ops.mesh.primitive_torus_add(major_segments=24, minor_segments=8, location=(x, -0.085, 1.015), major_radius=0.045, minor_radius=0.006, rotation=(math.pi / 2, 0, 0))
        finish(bpy.context.object, "Ring_Knocker", leaf, bronze)
        join_parts(leaf)
    join_parts(frame)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in [root, *root.children_recursive]:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = root
    bpy.ops.export_scene.gltf(filepath=str(GAME), export_format="GLB", use_selection=True, export_yup=True, export_animations=False)
    # Presentation geometry is created after GLB export, never included in the game model.
    bpy.ops.mesh.primitive_plane_add(size=200)
    floor = bpy.context.object
    floor.name = "PRESENTATION_ONLY_Floor"
    floor.location.z = -0.015
    floor_material = bpy.data.materials.new("Studio_Warm_Gray")
    floor_material.diffuse_color = (0.18, 0.17, 0.15, 1)
    floor.data.materials.append(floor_material)
    for name, location, power, color, size in [
        ("Key", (2.5, -4, 5), 650, (1, 0.88, 0.75), 4),
        ("Fill", (-3, -2, 3), 350, (0.80, 0.88, 1), 3),
        ("Rim", (1, 2, 4), 700, (1, 0.92, 0.80), 3),
    ]:
        data = bpy.data.lights.new(name, "AREA")
        data.energy, data.color, data.shape, data.size = power, color, "DISK", size
        light = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(light)
        light.location = location
        light.rotation_euler = (Vector((0, 0, 1.3)) - light.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.camera_add(location=(3.0, -6.8, 3.1))
    camera = bpy.context.object
    camera.rotation_euler = (Vector((0, 0, 1.3)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 3.65
    scene = bpy.context.scene
    scene.camera = camera
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1400
    scene.render.resolution_percentage = 100
    scene.world = bpy.data.worlds.new("Neutral_Studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value = (0.22, 0.24, 0.27, 1)
    scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.35
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    scene.render.filepath = str(RENDERS / "ARCH_003_DoorSong_v003_studio.png")
    bpy.ops.render.render(write_still=True)
    print("DOOR_BUILD: " + str(GAME))


if __name__ == "__main__":
    build()
