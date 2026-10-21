"""Blender CLI: --background --python optimize_export.py -- INPUT.glb NEW_OUTPUT.glb [RATIO]."""
import bpy
import sys
from pathlib import Path


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    source, destination = map(Path, args[:2])
    ratio = float(args[2]) if len(args) == 3 else 1.0
    if not source.is_file() or source.suffix.lower() != ".glb":
        raise ValueError("Expected an existing GLB")
    if destination.exists() or destination.suffix.lower() != ".glb":
        raise ValueError("Output must be a new GLB path; existing versions are preserved")
    if not 0 < ratio <= 1:
        raise ValueError("Ratio must be within (0, 1]")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    if ratio < 1:
        if any(obj.type == "ARMATURE" for obj in bpy.context.scene.objects):
            raise ValueError("Automatic decimation of rigged characters requires separate review")
        for obj in bpy.context.scene.objects:
            if obj.type == "MESH":
                modifier = obj.modifiers.new("Requested_Decimation", "DECIMATE")
                modifier.ratio = ratio
    destination.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(destination.resolve()), export_format="GLB", export_apply=ratio < 1, export_yup=True, export_animations=True)
    print("EXPORTED_FOR_REVIEW: " + str(destination))


if __name__ == "__main__":
    main()
