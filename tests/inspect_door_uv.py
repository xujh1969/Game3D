import bpy
from pathlib import Path

root = Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root / "assets/source/ARCH_003_DoorSong_v001.blend"))
for obj in bpy.data.objects:
    if obj.type == "MESH" and obj.name.endswith("Geometry"):
        uv = [tuple(loop.uv) for loop in obj.data.uv_layers.active.data]
        print("UV_PROBE", obj.name, len(set(uv)), "range", [(min(p[i] for p in uv), max(p[i] for p in uv)) for i in [0, 1]])
