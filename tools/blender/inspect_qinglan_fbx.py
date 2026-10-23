"""Read-only FBX/GLB comparison for user-provided Mixamo clips."""
import bpy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
records=[]
for filename in ["CHAR_001_Qinglan_v001_source.glb","Walking.fbx","Fast Run.fbx"]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    path=ROOT/"handoff/incoming"/filename
    if path.suffix==".glb":
        bpy.ops.import_scene.gltf(filepath=str(path))
    else:
        bpy.ops.import_scene.fbx(filepath=str(path))
    rigs=[o for o in bpy.context.scene.objects if o.type=="ARMATURE"]
    record={"file":filename,"actions":[{"name":a.name,"frames":list(a.frame_range)} for a in bpy.data.actions],
            "rigs":[{"name":r.name,"scale":list(r.scale),"rotation":list(r.rotation_euler),"world_matrix":[list(row) for row in r.matrix_world],
                     "bones":{b.name:{"head":list(b.head_local),"tail":list(b.tail_local),"matrix":[list(row) for row in b.matrix_local],"parent":b.parent.name if b.parent else None} for b in r.data.bones}}
                    for r in rigs],
            "meshes":[{"name":o.name,"vertices":len(o.data.vertices),"uv":len(o.data.uv_layers),"materials":[m.name if m else None for m in o.data.materials]} for o in bpy.context.scene.objects if o.type=="MESH"]}
    records.append(record)
(ROOT/"reports/validation/Qinglan_UserMotion_Inspection_2026-10-23.json").write_text(json.dumps(records,indent=2)+"\n",encoding="utf-8")
print("USER_MOTION_INSPECTED")
