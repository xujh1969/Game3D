"""Weld coincident import seam vertices before collapse; keep all source versions."""
import bpy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/review/CHAR_001_Qinglan_v002_review.glb"
if OUTPUT.exists():
    raise FileExistsError("Preserve review v002")
bpy.ops.wm.open_mainfile(filepath=str(ROOT / "assets/source/CHAR_001_Qinglan_v001.blend"))
obj = next(obj for obj in bpy.context.scene.objects if obj.type == "MESH")
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
before_vertices = len(obj.data.vertices)
bpy.ops.mesh.customdata_custom_splitnormals_clear()
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.remove_doubles(threshold=0.000001)
bpy.ops.object.mode_set(mode="OBJECT")
after_vertices = len(obj.data.vertices)
print("WELDED_VERTICES:", before_vertices, after_vertices, flush=True)
for face in obj.data.polygons:
    face.use_smooth = True
modifier = obj.modifiers.new("Review_30000_Welded", "DECIMATE")
modifier.ratio = 30000 / 1499720
bpy.ops.object.modifier_apply(modifier=modifier.name)
for face in obj.data.polygons:
    face.use_smooth = True
obj.data.calc_loop_triangles()
for image in bpy.data.images:
    if image.source == "FILE" and max(image.size) > 2048:
        image.scale(2048, 2048)
        image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "assets/source/CHAR_001_Qinglan_v002_review.blend"))
bpy.ops.export_scene.gltf(filepath=str(OUTPUT), export_format="GLB", export_yup=True, export_animations=False)
report = {"status": "PASS_WITH_LIMITATIONS", "before_weld_vertices": before_vertices,
          "after_weld_vertices": after_vertices, "weld_threshold_m": 0.000001,
          "review_triangles": len(obj.data.loop_triangles), "rigged": False,
          "changes": "Weld coincident imported seam vertices before collapse; regenerate smooth normals",
          "limitations": "Static review; global decimation is not animation retopology"}
(ROOT / "reports/validation/CHAR_001_preparation_v002.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print("QINGLAN_REPAIR:", json.dumps(report))
