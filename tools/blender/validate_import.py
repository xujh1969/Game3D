"""Blender CLI: --background --python validate_import.py -- INPUT.glb REPORT.json."""
import bpy
import json
import sys
from pathlib import Path
from mathutils import Vector


def main():
    source, destination = map(Path, sys.argv[sys.argv.index("--") + 1:])
    if source.suffix.lower() != ".glb" or not source.is_file():
        raise ValueError("Expected an existing GLB")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    points = [obj.matrix_world @ Vector(point) for obj in meshes for point in obj.bound_box]
    bounds = [[min(p[i] for p in points), max(p[i] for p in points)] for i in range(3)] if points else []
    triangles = 0
    for obj in meshes:
        obj.data.calc_loop_triangles()
        triangles += len(obj.data.loop_triangles)
    missing = []
    images = []
    for image in bpy.data.images:
        if image.source != "FILE":
            continue
        exists = bool(image.packed_file) or Path(bpy.path.abspath(image.filepath)).is_file()
        images.append({"name": image.name, "size": list(image.size), "packed": bool(image.packed_file)})
        if not exists:
            missing.append(image.filepath)
    report = {
        "source": str(source.resolve()),
        "blender_version": bpy.app.version_string,
        "status": "PASS_WITH_LIMITATIONS" if meshes and not missing else "FAILED",
        "mesh_count": len(meshes), "triangles": triangles,
        "materials": [material.name for material in bpy.data.materials],
        "blender_bounds_xyz": bounds,
        "godot_dimensions_xyz_m": [bounds[0][1] - bounds[0][0], bounds[2][1] - bounds[2][0], bounds[1][1] - bounds[1][0]] if bounds else [],
        "armatures": [obj.name for obj in bpy.context.scene.objects if obj.type == "ARMATURE"],
        "actions": [action.name for action in bpy.data.actions],
        "images": images, "missing_files": missing,
        "requires_review": ["Source and license", "Expected real-world dimensions and pivot", "Normals, UV, PBR appearance, extra base geometry", "Rig and animation quality when applicable"],
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ASSET_VALIDATION: " + report["status"])
    if report["status"] == "FAILED":
        raise RuntimeError("Asset validation failed; see report")


if __name__ == "__main__":
    main()
