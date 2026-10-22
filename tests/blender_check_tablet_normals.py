"""Verify closed tablet slab has outward winding using signed mesh volume."""
import bpy
import bmesh
import sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
version=sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.open_mainfile(filepath=str(root/f"assets/source/PROP_002_ClueSet_{version}.blend"))
obj=bpy.data.objects["Tablet_Slab"]
bm=bmesh.new()
bm.from_mesh(obj.data)
volume=bm.calc_volume(signed=True)
closed=all(edge.is_manifold for edge in bm.edges)
bm.free()
print(f"TABLET_NORMALS: {version} closed={closed} signed_volume={volume}")
if not closed or volume <= 0:
    raise RuntimeError("Tablet slab must be closed with outward normals")
