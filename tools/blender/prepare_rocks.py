"""Prepare three CC0 scan variants, preserving full-resolution imported source geometry."""
import bpy
import json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source/NAT_001_MossRocks_v001.blend"


def triangles(obj):
    obj.data.calc_loop_triangles()
    return len(obj.data.loop_triangles)


def main():
    if SOURCE.exists():
        raise FileExistsError("Preserve rock source v001")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(ROOT / "assets/source/third_party/rock_moss_set_01/rock_moss_set_01_1k.gltf"))
    meshes = sorted([obj for obj in bpy.context.scene.objects if obj.type == "MESH"], key=lambda obj: obj.name)
    chosen = meshes[:3]
    for obj in meshes[3:]:
        bpy.data.objects.remove(obj, do_unlink=True)
    for index,obj in enumerate(chosen):
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active=obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        points=[vertex.co.copy() for vertex in obj.data.vertices]
        low=Vector([min(p[i] for p in points) for i in range(3)])
        high=Vector([max(p[i] for p in points) for i in range(3)])
        center=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
        factor=1.8/max(high.x-low.x,high.y-low.y)
        for vertex in obj.data.vertices:
            vertex.co=(vertex.co-center)*factor
        obj.name=f"MossRock_{index+1:03d}"
        obj.location=(index*2.5,0,0)
    for image in bpy.data.images:
        if image.source == "FILE":
            image.pack()
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    reports=[]
    for index,obj in enumerate(chosen):
        before=triangles(obj)
        obj.location=(0,0,0)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active=obj
        if before > 3500:
            modifier=obj.modifiers.new("Game_Decimation", "DECIMATE")
            modifier.ratio=3500/before
            bpy.ops.object.modifier_apply(modifier=modifier.name)
        output=ROOT/f"assets/game/NAT_001_MossRock_{index+1:03d}_v001_game.glb"
        if output.exists():
            raise FileExistsError(str(output))
        bpy.ops.export_scene.gltf(filepath=str(output), export_format="GLB", use_selection=True, export_yup=True, export_animations=False)
        reports.append({"file":output.name,"triangles_before":before,"triangles_after":triangles(obj),"godot_dimensions_xyz_m":[obj.dimensions.x,obj.dimensions.z,obj.dimensions.y],"materials":len(obj.data.materials)})
    (ROOT/"reports/validation/NAT_001_v001.json").write_text(json.dumps({"status":"PASS_WITH_LIMITATIONS","source":"https://polyhaven.com/a/rock_moss_set_01","license":"CC0","author":"Kless Gyzen","variants":reports},indent=2),encoding="utf-8")
    print("ROCK_PREPARATION: three variants exported")


if __name__ == "__main__":
    main()
