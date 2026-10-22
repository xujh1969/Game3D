"""Confirm material upgrade did not alter editable construction geometry."""
import bpy
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]


def snapshot(version):
    bpy.ops.wm.open_mainfile(filepath=str(root/f"assets/source/ARCH_Courtyard_{version}.blend"))
    records={}
    for obj in bpy.context.scene.objects:
        if obj.type!="MESH":
            continue
        data={"vertices":[list(vertex.co) for vertex in obj.data.vertices],"faces":[list(face.vertices) for face in obj.data.polygons],"transform":[list(row) for row in obj.matrix_world]}
        records[obj.name]=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
    return records


before=snapshot("v002")
after=snapshot("v003")
used={mat.name for obj in bpy.context.scene.objects if obj.type=="MESH" for mat in obj.data.materials if mat}
checks={"identical_object_geometry_and_transforms":before==after,"photographic_ground": "PH_brown_mud_02_PBR" in used,"photographic_plaster":"PH_plastered_wall_02_PBR" in used}
report={"status":"PASS" if all(checks.values()) else "FAILED","mesh_objects":len(after),"checks":checks}
(root/"reports/validation/Surface_Upgrade_geometry.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print("SURFACE_GEOMETRY: "+json.dumps(report))
if not all(checks.values()):
    raise RuntimeError("Surface upgrade changed geometry or lacks materials")
