"""Offline source face reference to isolate review-decimation artifacts."""
import bpy
import sys
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
review = "--review" in sys.argv
if review:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(ROOT / "assets/review/CHAR_001_Qinglan_v001_review.glb"))
else:
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / "assets/source/CHAR_001_Qinglan_v001.blend"))
for name, position, power in [("Key", (2,-3,3), 350), ("Fill",(-2,-2,2),200)]:
    data=bpy.data.lights.new(name,"AREA")
    data.energy=power
    data.size=3
    obj=bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(obj)
    obj.location=position
    obj.rotation_euler=(Vector((0,0,1.5))-obj.location).to_track_quat("-Z","Y").to_euler()
bpy.ops.object.camera_add(location=(0,-3,1.5))
camera=bpy.context.object
camera.rotation_euler=(Vector((0,0,1.5))-camera.location).to_track_quat("-Z","Y").to_euler()
camera.data.type="ORTHO"
camera.data.ortho_scale=.62
scene=bpy.context.scene
scene.camera=camera
scene.world=bpy.data.worlds.new("Neutral")
scene.world.use_nodes=True
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.3
scene.render.engine="CYCLES"
scene.cycles.samples=12
scene.cycles.use_denoising=True
scene.render.resolution_x=640
scene.render.resolution_y=640
scene.render.resolution_percentage=100
scene.render.filepath=str(ROOT/ ("reports/screenshots/CHAR_001_Review_v001_Face_Studio.png" if review else "reports/screenshots/CHAR_001_Source_v001_Face_Studio.png"))
bpy.ops.render.render(write_still=True)
