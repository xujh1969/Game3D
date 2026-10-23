"""40-bone experimental rig; baked two-segment limb solving and varied standing motion."""
import bpy
import json
import math
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source/CHAR_001_Qinglan_v005_rigged.blend"
OUTPUT = ROOT / "assets/game/CHAR_001_Qinglan_v005_game.glb"


def main():
    if SOURCE.exists() or OUTPUT.exists():
        raise FileExistsError("Preserve Qinglan v005")
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / "assets/source/CHAR_001_Qinglan_v002_review.blend"))
    mesh = next(o for o in bpy.context.scene.objects if o.type == "MESH")
    mesh.name = "Qinglan_Mesh"
    bpy.ops.object.select_all(action="DESELECT")
    data = bpy.data.armatures.new("Qinglan_DetailedSkeleton")
    rig = bpy.data.objects.new("Qinglan_Rig", data)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    auxiliaries = []

    def bone(name, head, tail, parent=None, deform=True):
        result = data.edit_bones.new(name)
        result.head, result.tail = head, tail
        result.use_deform = deform
        if parent:
            result.parent = data.edit_bones[parent]
        return result

    bone("Root", (0,0,0), (0,0,.15), deform=False)
    bone("Hips", (0,0,.86), (0,0,.99), "Root")
    bone("Spine_Lower", (0,0,.99), (0,0,1.10), "Hips")
    bone("Spine_Upper", (0,0,1.10), (0,0,1.22), "Spine_Lower")
    bone("Chest", (0,0,1.22), (0,0,1.35), "Spine_Upper")
    bone("Neck_Lower", (0,0,1.35), (0,0,1.40), "Chest")
    bone("Neck_Upper", (0,0,1.40), (0,0,1.45), "Neck_Lower")
    bone("Head", (0,0,1.45), (0,0,1.70), "Neck_Upper")
    for side, sign in [("L",1),("R",-1)]:
        bone("Shoulder_"+side, (sign*.02,0,1.33), (sign*.17,0,1.33), "Chest")
        bone("UpperArm_"+side, (sign*.17,0,1.33), (sign*.28,0,1.12), "Shoulder_"+side)
        bone("Forearm_"+side, (sign*.28,0,1.12), (sign*.34,0,.95), "UpperArm_"+side)
        bone("Hand_"+side, (sign*.34,0,.95), (sign*.37,0,.87), "Forearm_"+side)
        bone("Thigh_"+side, (sign*.10,0,.86), (sign*.12,-.035,.48), "Hips")
        bone("Shin_"+side, (sign*.12,-.035,.48), (sign*.12,0,.10), "Thigh_"+side)
        bone("Foot_"+side, (sign*.12,0,.10), (sign*.12,-.14,.05), "Shin_"+side)
        bone("Toe_"+side, (sign*.12,-.14,.05), (sign*.12,-.20,.04), "Foot_"+side)
        for prefix in ["UpperArm", "Forearm", "Thigh", "Shin"]:
            parent = data.edit_bones[prefix+"_"+side]
            name = prefix+"Twist_"+side
            bone(name, parent.head.lerp(parent.tail,.45), parent.tail, parent.name, False)
            auxiliaries.append((parent.name,name,"twist"))
        name = "Scapula_"+side
        bone(name, (sign*.05,.03,1.30), (sign*.16,.03,1.33), "Chest", False)
        auxiliaries.append(("Shoulder_"+side,name,"scapula"))
        for label, y in [("Front",-.11),("Back",.11)]:
            name = "Coat_"+label+"_"+side
            bone(name,(sign*.09,y,.99),(sign*.09,y,.64),"Hips",False)
            auxiliaries.append(("Hips",name,label))
    bone("Breath", (0,-.07,1.22), (0,-.07,1.35), "Chest", False)
    auxiliaries.append(("Chest","Breath","breath"))
    bone("Satchel", (.23,.10,1.01), (.23,.10,.82), "Hips", False)
    auxiliaries.append(("Hips","Satchel","satchel"))
    bpy.ops.object.mode_set(mode="OBJECT")
    mesh.select_set(True)
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    # Secondary weights share existing influences rather than re-running heat on overlapping bones.
    for parent, name, kind in auxiliaries:
        data.bones[name].use_deform = True
        group = mesh.vertex_groups.new(name=name)
        original = mesh.vertex_groups[parent]
        for vertex in mesh.data.vertices:
            weight = next((g.weight for g in vertex.groups if g.group == original.index),0)
            if weight <= 0:
                continue
            x,y,z = vertex.co
            fraction = 0.0
            if kind == "twist":
                rest = data.bones[parent]
                t = (vertex.co-rest.head_local).dot((rest.tail_local-rest.head_local).normalized())/rest.length
                fraction = .30 * max(0,min(1,t))
            elif kind == "scapula":
                fraction = .18
            elif kind == "breath" and y < -.035 and 1.18 < z < 1.38:
                fraction = .22
            elif kind == "satchel" and x > .18 and y > .035 and .75 < z < 1.07:
                fraction = .6
            elif kind in ["Front","Back"] and .63 < z < 1.04 and abs(x) < .22:
                side_ok = x >= 0 if name.endswith("_L") else x < 0
                panel_ok = y < -.065 if kind == "Front" else y > .065
                if side_ok and panel_ok:
                    fraction = .35
            if fraction:
                group.add([vertex.index],weight*fraction,"REPLACE")
                original.add([vertex.index],weight*(1-fraction),"REPLACE")
    bpy.context.view_layer.objects.active = mesh
    rig.select_set(False)
    bpy.ops.object.vertex_group_limit_total(limit=4)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)
    if any(not v.groups or sum(g.weight for g in v.groups) < .999 for v in mesh.data.vertices):
        raise RuntimeError("Unnormalized weights")
    bpy.context.view_layer.objects.active = rig
    scene = bpy.context.scene
    scene.render.fps = 30
    rig.animation_data_create()
    rest = {b.name: b.matrix_local.copy() for b in data.bones}

    def orient(name, head, tail, extra=None):
        b = data.bones[name]
        # Bone.vector is parent-relative; all target points here are armature-space.
        direction = b.tail_local-b.head_local
        rotation = direction.rotation_difference(tail-head) @ rest[name].to_quaternion()
        if extra:
            rotation = extra @ rotation
        rig.pose.bones[name].matrix = Matrix.Translation(head) @ rotation.to_matrix().to_4x4()
        bpy.context.view_layer.update()

    def solve(a,b,start,end,pole):
        l1,l2 = data.bones[a].length,data.bones[b].length
        direction = end-start
        distance = min(direction.length,l1+l2-.0001)
        direction.normalize()
        endpoint = start+direction*distance
        along = (l1*l1-l2*l2+distance*distance)/(2*distance)
        bend = pole-direction*pole.dot(direction)
        bend.normalize()
        joint = start+direction*along+bend*math.sqrt(max(0,l1*l1-along*along))
        orient(a,start,joint)
        orient(b,joint,endpoint)
        return endpoint

    clips = [("Idle",12.0),("Idle_Look",8.0),("Idle_Shift",7.0),("Walk",.95),("Run",.65)]
    maximum_joint_gap = 0.0
    for clip,duration in clips:
        action = bpy.data.actions.new(clip)
        action.use_fake_user = True
        rig.animation_data.action = action
        samples = round(duration*30)
        for sample in range(samples+1):
            phase = sample/samples
            frame = 1+sample
            scene.frame_set(frame)
            for pose in rig.pose.bones:
                pose.rotation_mode = "XYZ"
                pose.rotation_euler = (0,0,0)
                pose.location = (0,0,0)
                pose.scale = (1,1,1)
            theta = phase*math.tau
            moving = clip in ["Walk","Run"]
            run = clip == "Run"
            breath = math.sin(theta*(3 if duration >= 10 else 2))
            shift = (.012 if moving else .020)*math.sin(theta)
            bob = -.0015+.001*breath
            if moving:
                stride = .34 if run else .27
                stance = .48 if run else .62
                support_heights = []
                for offset in [0,.5]:
                    p = (phase+offset)%1
                    if p < stance:
                        y = -stride+2*stride*p/stance
                        reach = data.bones["Thigh_L"].length+data.bones["Shin_L"].length-.003
                        support_heights.append(.10+math.sqrt(max(0,reach*reach-y*y-(.02+abs(shift))**2)))
                bob = min(support_heights)-.86 if support_heights else .008
            rig.pose.bones["Hips"].location = (shift,bob,0)
            rig.pose.bones["Hips"].rotation_euler.z = .025*math.sin(theta)
            rig.pose.bones["Spine_Lower"].rotation_euler.y = .025*math.sin(theta)
            rig.pose.bones["Spine_Upper"].rotation_euler.z = -.018*math.sin(theta)
            rig.pose.bones["Chest"].rotation_euler.x = (.07 if run else .015)+.010*breath
            rig.pose.bones["Chest"].rotation_euler.y = -.04*math.sin(theta) if moving else .02*math.sin(theta)
            rig.pose.bones["Breath"].scale.z = 1+.025*breath
            rig.pose.bones["Neck_Lower"].rotation_euler.x = -.025 if moving else .018*breath
            rig.pose.bones["Neck_Upper"].rotation_euler.z = .018*math.sin(theta)
            yaw = (.045 if moving else .08)*math.sin(theta)
            if clip == "Idle_Look":
                yaw = .22*math.sin(theta)*math.sin(math.pi*phase)**2
            elif clip == "Idle_Shift":
                rig.pose.bones["Hips"].location.x = .035*math.sin(theta)
                yaw = -.09*math.sin(theta)
            rig.pose.bones["Head"].rotation_euler = (.015*breath,yaw,-.02*math.sin(theta))
            bpy.context.view_layer.update()
            for side,sign,offset in [("L",1,0),("R",-1,.5)]:
                p = (phase+offset)%1
                stride = .34 if run else .27
                stance = .48 if run else .62
                pitch = 0.0
                if moving and p < stance:
                    y = -stride+2*stride*p/stance
                    lift = 0.0
                    pitch = -.10*math.cos(math.pi*p/stance)
                elif moving:
                    q = (p-stance)/(1-stance)
                    y = stride-2*stride*(q*q*(3-2*q))
                    lift = (.17 if run else .10)*math.sin(math.pi*q)
                    pitch = .10*math.cos(math.pi*q)
                else:
                    y,lift = 0.0,0.0
                hip = rig.pose.bones["Hips"].matrix @ (rest["Hips"].inverted() @ data.bones["Thigh_"+side].head_local)
                ankle = solve("Thigh_"+side,"Shin_"+side,hip,Vector((sign*.12,y,.10+lift)),Vector((0,-1,0)))
                foot_end = ankle+Vector((0,-.14,-.05))
                orient("Foot_"+side,ankle,foot_end,Quaternion((1,0,0),pitch))
                rig.pose.bones["Toe_"+side].rotation_euler.x = max(0,pitch)*.6
                shoulder = rig.pose.bones["Shoulder_"+side].tail.copy()
                swing = math.sin(theta+offset*math.tau)
                wrist = shoulder+Vector((sign*.025, (.23 if run else .16)*swing if moving else .015,
                    -.25 if run else (-.37 if moving else -.40)))
                solve("UpperArm_"+side,"Forearm_"+side,shoulder,wrist,Vector((sign*.08,.7,0)))
                rig.pose.bones["Hand_"+side].rotation_euler.y = .06*math.sin(theta+offset*math.tau)
                for prefix in ["UpperArm","Forearm","Thigh","Shin"]:
                    rig.pose.bones[prefix+"Twist_"+side].rotation_euler.y = .025*swing
                rig.pose.bones["Scapula_"+side].rotation_euler.y = .04*swing if moving else .012*breath
                for label in ["Front","Back"]:
                    rig.pose.bones["Coat_"+label+"_"+side].rotation_euler.x = .04*math.sin(theta+offset*math.tau+.4) if moving else .008*breath
            rig.pose.bones["Satchel"].rotation_euler.x = .035*math.sin(theta-.3) if moving else .008*breath
            bpy.context.view_layer.update()
            for side in ["L","R"]:
                for parent,child in [("Thigh","Shin"),("Shin","Foot"),("UpperArm","Forearm"),("Forearm","Hand")]:
                    gap = (rig.pose.bones[parent+"_"+side].tail-rig.pose.bones[child+"_"+side].head).length
                    maximum_joint_gap = max(maximum_joint_gap,gap)
                    if gap > .001:
                        raise RuntimeError(f"Disconnected joint {clip} {parent}/{child}: {gap}")
            for pose in rig.pose.bones:
                for path in ["location","rotation_euler","scale"]:
                    pose.keyframe_insert(path,frame=frame,group=pose.name)
        rig.animation_data.action = None
        track = rig.animation_data.nla_tracks.new()
        track.name = clip
        track.strips.new(clip,1,action)
        track.mute = True
    for track in rig.animation_data.nla_tracks:
        track.mute = True
    scene.frame_set(1)
    for pose in rig.pose.bones:
        pose.rotation_euler = (0,0,0)
        pose.location = (0,0,0)
        pose.scale = (1,1,1)
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    for track in rig.animation_data.nla_tracks:
        track.mute = False
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(OUTPUT),export_format="GLB",export_yup=True,
        export_animations=True,export_animation_mode="NLA_TRACKS",export_force_sampling=True)
    report = {"status":"PASS_WITH_LIMITATIONS","bones":len(data.bones),"clips":dict(clips),
        "vertices":len(mesh.data.vertices),"unweighted_vertices":0,"max_influences":4,
        "maximum_joint_gap_m":maximum_joint_gap,
        "method":"Baked analytic two-segment limbs; stance/swing ankle targets; auxiliary skin bones",
        "limitations":"Experimental procedural animation; no terrain-aware foot IK, mocap, finger articulation or cloth simulation"}
    (ROOT/"reports/validation/Qinglan_Rig_v005.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("QINGLAN_MOTION:",json.dumps(report))


if __name__ == "__main__":
    main()
