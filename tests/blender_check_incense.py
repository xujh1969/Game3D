"""Check source geometry, wall interior, positive volumes and three stable feet."""
import bpy
import bmesh
import json
import sys
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
version=sys.argv[sys.argv.index("--")+1] if "--" in sys.argv else "v002"
bpy.ops.wm.open_mainfile(filepath=str(ROOT/f"assets/source/PROP_001_IncenseBurner_{version}.blend"))
body=bpy.data.objects["Bowl_With_Interior"]
feet=[obj for obj in bpy.data.objects if obj.name.startswith("Foot_")]
checks={"three_feet":len(feet)==3}
for obj in [body,*feet]:
    bm=bmesh.new()
    bm.from_mesh(obj.data)
    checks[obj.name+"_closed"]=all(edge.is_manifold for edge in bm.edges)
    checks[obj.name+"_outward"]=bm.calc_volume(signed=True)>0
    bm.free()
    checks[obj.name+"_uv"]=bool(obj.data.uv_layers)
center=body.ray_cast(Vector((0,0,.5)),Vector((0,0,-1)))
rim=body.ray_cast(Vector((.214,0,.5)),Vector((0,0,-1)))
checks["open_inner_cavity"]=bool(center[0] and center[1].z<.15)
checks["rim_above_inner_floor"]=bool(rim[0] and rim[1].z>.31)
checks["feet_below_inner_floor"]=bool(center[0] and all(max(vertex.co.z for vertex in obj.data.vertices)<center[1].z-.005 for obj in feet))
checks["feet_touch_ground"]=all(abs(min(vertex.co.z for vertex in obj.data.vertices))<.0001 for obj in feet)
checks["diameter_45cm"]=abs(body.dimensions.x-.45)<.001
checks["height_35cm"]=abs(max(vertex.co.z for obj in [body,*feet] for vertex in obj.data.vertices)-.35)<.001
report={"status":"PASS" if all(checks.values()) else "FAILED","checks":checks}
(ROOT/f"reports/validation/PROP_001_geometry_{version}.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print("INCENSE_GEOMETRY: "+json.dumps(report))
if not all(checks.values()):
    raise RuntimeError("Incense geometry check failed")
