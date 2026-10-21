"""Known TEMP 1m cube for testing the import/export pipeline; never a formal asset."""
import bpy
from pathlib import Path

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
bpy.context.object.name = "TEMP_Pipeline_Cube_1m"
output = Path(__file__).resolve().parents[1] / "assets/temporary/TEMP_Pipeline_Cube_v001.glb"
bpy.ops.export_scene.gltf(filepath=str(output), export_format="GLB", export_yup=True)
print("TEMP_FIXTURE: " + str(output))
