"""Offline neutral studio material inspection; never a gameplay capture."""
import bpy
from pathlib import Path
from mathutils import Vector

root=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(root/"assets/source/PROP_001_IncenseBurner_v002.blend"))
bpy.ops.mesh.primitive_plane_add(size=200)
floor=bpy.context.object
floor.name="PRESENTATION_ONLY_Floor"
mat=bpy.data.materials.new("Studio_Gray")
mat.diffuse_color=(.14,.15,.16,1)
floor.data.materials.append(mat)
floor.location.z=-.001
for name,position,power,color,size in [("Key",(.6,-.8,1),90,(1,.91,.81),.8),("Fill",(-.7,-.3,.6),65,(.78,.86,1),.8),("Rim",(.3,.8,.8),100,(1,.96,.88),.6)]:
    data=bpy.data.lights.new(name,"AREA")
    data.energy=power
    data.color=color
    data.size=size
    obj=bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(obj)
    obj.location=position
    obj.rotation_euler=(Vector((0,0,.18))-obj.location).to_track_quat("-Z","Y").to_euler()
bpy.ops.object.camera_add(location=(.65,-1.0,.72))
camera=bpy.context.object
camera.rotation_euler=(Vector((0,0,.18))-camera.location).to_track_quat("-Z","Y").to_euler()
camera.data.type="ORTHO"
camera.data.ortho_scale=.70
scene=bpy.context.scene
scene.camera=camera
scene.world=bpy.data.worlds.new("Studio_Neutral")
scene.world.use_nodes=True
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.3
scene.render.engine="CYCLES"
scene.cycles.samples=24
scene.cycles.use_denoising=True
scene.render.resolution_x=1200
scene.render.resolution_y=1000
scene.render.resolution_percentage=100
scene.render.filepath=str(root/"reports/screenshots/PROP_001_v002_Studio.png")
bpy.ops.render.render(write_still=True)
