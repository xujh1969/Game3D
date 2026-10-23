"""Experimental humanoid rig and procedural locomotion for early playable integration."""
import bpy
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source/CHAR_001_Qinglan_v003_rigged.blend"
OUTPUT = ROOT / "assets/game/CHAR_001_Qinglan_v003_game.glb"


def main():
    if SOURCE.exists() or OUTPUT.exists():
        raise FileExistsError("Preserve Qinglan v003")
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / "assets/source/CHAR_001_Qinglan_v002_review.blend"))
    mesh = next(obj for obj in bpy.context.scene.objects if obj.type == "MESH")
    mesh.name = "Qinglan_Mesh"
    bpy.ops.object.select_all(action="DESELECT")
    armature = bpy.data.armatures.new("Qinglan_Skeleton")
    rig = bpy.data.objects.new("Qinglan_Rig", armature)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    def bone(name, head, tail, parent=None, deform=True):
        result = armature.edit_bones.new(name)
        result.head, result.tail = head, tail
        result.use_deform = deform
        if parent:
            result.parent = armature.edit_bones[parent]

    bone("Root", (0,0,0), (0,0,.15), deform=False)
    bone("Hips", (0,0,.86), (0,0,.99), "Root")
    bone("Spine", (0,0,.99), (0,0,1.16), "Hips")
    bone("Chest", (0,0,1.16), (0,0,1.34), "Spine")
    bone("Neck", (0,0,1.34), (0,0,1.43), "Chest")
    bone("Head", (0,0,1.43), (0,0,1.70), "Neck")
    for side, sign in [("L", 1), ("R", -1)]:
        bone("Shoulder_"+side, (sign*.02,0,1.33), (sign*.17,0,1.33), "Chest")
        bone("UpperArm_"+side, (sign*.17,0,1.33), (sign*.28,0,1.12), "Shoulder_"+side)
        bone("Forearm_"+side, (sign*.28,0,1.12), (sign*.34,0,.95), "UpperArm_"+side)
        bone("Hand_"+side, (sign*.34,0,.95), (sign*.37,0,.87), "Forearm_"+side)
        bone("Thigh_"+side, (sign*.10,0,.86), (sign*.12,0,.48), "Hips")
        bone("Shin_"+side, (sign*.12,0,.48), (sign*.12,0,.10), "Thigh_"+side)
        bone("Foot_"+side, (sign*.12,0,.10), (sign*.12,-.14,.05), "Shin_"+side)
        bone("Toe_"+side, (sign*.12,-.14,.05), (sign*.12,-.20,.04), "Foot_"+side)
    bpy.ops.object.mode_set(mode="OBJECT")
    mesh.select_set(True)
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    weights = [sum(group.weight for group in vertex.groups) for vertex in mesh.data.vertices]
    if any(weight < .00001 for weight in weights):
        raise RuntimeError("Automatic weights left unbound vertices; do not export")
    # Normalize and limit to glTF's four weights per vertex explicitly.
    bpy.context.view_layer.objects.active = mesh
    rig.select_set(False)
    bpy.ops.object.vertex_group_limit_total(limit=4)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)
    bpy.context.view_layer.objects.active = rig
    scene = bpy.context.scene
    scene.render.fps = 30
    rig.animation_data_create()
    for clip, end, leg_swing, arm_swing in [("Idle",73,0,0), ("Walk",27,.43,.28), ("Run",18,.68,.48)]:
        action = bpy.data.actions.new(clip)
        action.use_fake_user = True
        rig.animation_data.action = action
        for sample in range(25):
            phase = sample / 24
            frame = 1 + (end - 1) * phase
            for pose in rig.pose.bones:
                pose.rotation_mode = "XYZ"
                pose.rotation_euler = (0,0,0)
                pose.location = (0,0,0)
            if clip == "Idle":
                rig.pose.bones["Chest"].rotation_euler.x = .012 * math.sin(phase * math.tau)
                rig.pose.bones["Head"].rotation_euler.z = .015 * math.sin(phase * math.tau)
            else:
                for side, offset in [("L",0), ("R",math.pi)]:
                    swing = math.sin(phase * math.tau + offset)
                    rig.pose.bones["Thigh_"+side].rotation_euler.x = leg_swing * swing
                    rig.pose.bones["Shin_"+side].rotation_euler.x = -max(0,swing) * leg_swing * .85
                    rig.pose.bones["Foot_"+side].rotation_euler.x = -swing * .10
                    rig.pose.bones["UpperArm_"+side].rotation_euler.x = -arm_swing * swing
                    rig.pose.bones["Forearm_"+side].rotation_euler.x = -.12 if clip == "Walk" else -.40
                rig.pose.bones["Chest"].rotation_euler.y = .025 * math.sin(phase * math.tau)
            for pose in rig.pose.bones:
                pose.keyframe_insert("rotation_euler", frame=frame, group=pose.name)
        rig.animation_data.action = None
        track = rig.animation_data.nla_tracks.new()
        track.name = clip
        track.strips.new(clip, 1, action)
    for track in rig.animation_data.nla_tracks:
        track.mute = True
    # Save editable rig with a clean rest preview; exporter evaluates each NLA track.
    scene.frame_set(1)
    for pose in rig.pose.bones:
        pose.rotation_euler = (0,0,0)
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    for track in rig.animation_data.nla_tracks:
        track.mute = False
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(OUTPUT), export_format="GLB", export_yup=True,
        export_animations=True, export_animation_mode="NLA_TRACKS", export_force_sampling=True)
    report = {"status": "PASS_WITH_LIMITATIONS", "bones": len(armature.bones),
        "vertices": len(mesh.data.vertices), "unweighted_vertices": 0,
        "clips": ["Idle","Walk","Run"], "max_influences": 4,
        "limitations": "Automatic heat weights; procedural experimental cycles; no foot IK or cloth simulation"}
    (ROOT / "reports/validation/Qinglan_Rig_v003.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("QINGLAN_RIG: " + json.dumps(report))


if __name__ == "__main__":
    main()
