"""Preserve imported high-resolution source; export an unrigged review copy only."""
import bpy
import hashlib
import json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "handoff/incoming/CHAR_001_Qinglan_v001_source.glb"
SOURCE = ROOT / "assets/source/CHAR_001_Qinglan_v001.blend"
OUTPUT = ROOT / "assets/review/CHAR_001_Qinglan_v001_review.glb"


def main():
    if SOURCE.exists() or OUTPUT.exists():
        raise FileExistsError("Preserve existing Qinglan versions")
    digest = hashlib.sha256(INPUT.read_bytes()).hexdigest()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(INPUT))
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if len(meshes) != 1 or any(obj.type == "ARMATURE" for obj in bpy.context.scene.objects):
        raise ValueError("This intake is for the inspected single unrigged source only")
    obj = meshes[0]
    obj.name = "Qinglan_Unrigged_Review"
    points = [obj.matrix_world @ Vector(co) for co in obj.bound_box]
    bottom = min(p.z for p in points)
    height = max(p.z for p in points) - bottom
    center = Vector(((min(p.x for p in points)+max(p.x for p in points))/2,
                     (min(p.y for p in points)+max(p.y for p in points))/2, bottom))
    transform = obj.matrix_world.copy()
    for vertex in obj.data.vertices:
        vertex.co = (transform @ vertex.co - center) * (1.70 / height)
    obj.matrix_world.identity()
    for image in bpy.data.images:
        if image.source == "FILE":
            image.pack()
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    obj.data.calc_loop_triangles()
    before = len(obj.data.loop_triangles)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    modifier = obj.modifiers.new("Review_30000_Triangles", "DECIMATE")
    modifier.ratio = min(1.0, 30000 / before)
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    obj.data.calc_loop_triangles()
    after = len(obj.data.loop_triangles)
    for image in bpy.data.images:
        if image.source == "FILE" and max(image.size) > 2048:
            image.scale(2048, 2048)
            image.pack()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(OUTPUT), export_format="GLB",
                              export_yup=True, export_animations=False)
    report = {"status": "PASS_WITH_LIMITATIONS", "source_sha256": digest,
              "source_triangles": before, "review_triangles": after,
              "height_m": 1.70, "texture_max_px": 2048,
              "source_blend": str(SOURCE.relative_to(ROOT)),
              "review_glb": str(OUTPUT.relative_to(ROOT)),
              "limitations": ["Unrigged; no animations", "Source/license and appearance gate pending",
                              "Global decimation is not deformation-ready retopology; inspect face and hands"]}
    (ROOT / "reports/validation/CHAR_001_preparation_v001.json").write_text(
        json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print("QINGLAN_PREPARATION: " + json.dumps(report))


if __name__ == "__main__":
    main()
