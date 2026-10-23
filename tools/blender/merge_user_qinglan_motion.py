"""Merge the user's Mixamo clips, preserve skin, and recover a surface from retained Qinglan."""
import bpy
import hashlib
import json
import math
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"assets/source/CHAR_001_Qinglan_v006_user_motion.blend"
GAME=ROOT/"assets/game/CHAR_001_Qinglan_v006_game.glb"


def main():
    if SOURCE.exists() or GAME.exists():
        raise FileExistsError("Preserve user motion versions")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.render.fps=30
    incoming=ROOT/"handoff/incoming"
    bpy.ops.import_scene.gltf(filepath=str(incoming/"CHAR_001_Qinglan_v001_source.glb"))
    rig=next(o for o in scene.objects if o.type=="ARMATURE")
    mesh=next(o for o in scene.objects if o.type=="MESH" and o.parent==rig)
    mesh.name="Qinglan_Mesh"
    base_objects=set(scene.objects)
    names=set(rig.data.bones.keys())
    rest={b.name:b.matrix_local.copy() for b in rig.data.bones}
    sampled={}
    rest_errors={}
    for label,filename in [("Idle",None),("Walk","Walking.fbx"),("Run","Fast Run.fbx")]:
        if filename:
            before=set(scene.objects)
            bpy.ops.import_scene.fbx(filepath=str(incoming/filename))
            imported=set(scene.objects)-before
            actor=next(o for o in imported if o.type=="ARMATURE")
            if set(actor.data.bones.keys())!=names:
                raise ValueError("Different skeleton: "+filename)
            error=max(abs(rest[n][i][j]-actor.data.bones[n].matrix_local[i][j])
                      for n in names for i in range(4) for j in range(4))
            rest_errors[label]=error
            if error>.001:
                raise ValueError("Rest basis mismatch: "+filename)
        else:
            actor=rig
            imported=set()
        action=actor.animation_data.action
        first,last=action.frame_range
        fps=scene.render.fps/scene.render.fps_base
        duration=(last-first)/fps
        count=max(2,round(duration*30))
        poses=[]
        for sample in range(count+1):
            frame=first+(last-first)*sample/count
            scene.frame_set(int(frame),subframe=frame-int(frame))
            poses.append({p.name:p.matrix_basis.decompose() for p in actor.pose.bones})
        sampled[label]=(duration,poses)
        if imported:
            for obj in imported:
                bpy.data.objects.remove(obj,do_unlink=True)
    rig.animation_data_clear()
    scene.render.fps=30
    # Normalize to the user's first Idle frame; keep the original mesh and weights.
    for p in rig.pose.bones:
        loc,rot,scale=sampled["Idle"][1][0][p.name]
        p.rotation_mode="QUATERNION"
        p.location,p.rotation_quaternion,p.scale=loc,rot,scale
    bpy.context.view_layer.update()
    depsgraph=bpy.context.evaluated_depsgraph_get()
    evaluated=mesh.evaluated_get(depsgraph)
    points=[evaluated.matrix_world@v.co for v in evaluated.data.vertices]
    low=min(p.z for p in points)
    high=max(p.z for p in points)
    height=high-low
    # Surface recovery is baked in rest pose, not into an animated pose.
    rig.data.pose_position="REST"
    bpy.context.view_layer.update()
    with bpy.data.libraries.load(str(ROOT/"assets/source/CHAR_001_Qinglan_v002_review.blend"),link=False) as (available,loaded):
        loaded.objects=["Qinglan_Unrigged_Review"]
    reference=loaded.objects[0]
    bpy.context.collection.objects.link(reference)
    target_points=[mesh.matrix_world@v.co for v in mesh.data.vertices]
    ref_points=[reference.matrix_world@v.co for v in reference.data.vertices]
    target_low=Vector(tuple(min(p[i] for p in target_points) for i in range(3)))
    target_high=Vector(tuple(max(p[i] for p in target_points) for i in range(3)))
    ref_low=Vector(tuple(min(p[i] for p in ref_points) for i in range(3)))
    ref_high=Vector(tuple(max(p[i] for p in ref_points) for i in range(3)))
    scale=(target_high.z-target_low.z)/(ref_high.z-ref_low.z)
    target_origin=Vector(((target_low.x+target_high.x)/2,(target_low.y+target_high.y)/2,target_low.z))
    ref_origin=Vector(((ref_low.x+ref_high.x)/2,(ref_low.y+ref_high.y)/2,ref_low.z))
    reference.matrix_world=Matrix.Translation(target_origin)@Matrix.Scale(scale,4)@Matrix.Translation(-ref_origin)
    bpy.ops.object.select_all(action="DESELECT")
    mesh.select_set(True)
    bpy.context.view_layer.objects.active=mesh
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.015)
    bpy.ops.object.mode_set(mode="OBJECT")
    material=bpy.data.materials.new("Qinglan_Recovered_Surface")
    material.use_nodes=True
    shader=material.node_tree.nodes["Principled BSDF"]
    shader.inputs["Metallic"].default_value=0
    mesh.data.materials.clear()
    mesh.data.materials.append(material)
    scene.render.engine="CYCLES"
    scene.cycles.samples=8
    scene.render.bake.use_selected_to_active=True
    scene.render.bake.cage_extrusion=.055
    scene.render.bake.margin=12
    images={}
    for channel,bake_type in [("BaseColor","DIFFUSE"),("Roughness","ROUGHNESS"),("Normal","NORMAL")]:
        image=bpy.data.images.new("Qinglan_UserRig_"+channel,2048,2048,alpha=False)
        image.colorspace_settings.name="sRGB" if channel=="BaseColor" else "Non-Color"
        node=material.node_tree.nodes.new("ShaderNodeTexImage")
        node.image=image
        material.node_tree.nodes.active=node
        bpy.ops.object.select_all(action="DESELECT")
        reference.select_set(True)
        mesh.select_set(True)
        bpy.context.view_layer.objects.active=mesh
        if bake_type=="DIFFUSE":
            bpy.ops.object.bake(type=bake_type,pass_filter={"COLOR"})
        else:
            bpy.ops.object.bake(type=bake_type)
        image.pack()
        images[channel]=(image,node)
        print("RECOVERED_SURFACE:",channel,flush=True)
    material.node_tree.links.new(images["BaseColor"][1].outputs["Color"],shader.inputs["Base Color"])
    material.node_tree.links.new(images["Roughness"][1].outputs["Color"],shader.inputs["Roughness"])
    normal=material.node_tree.nodes.new("ShaderNodeNormalMap")
    normal.inputs["Strength"].default_value=.5
    material.node_tree.links.new(images["Normal"][1].outputs["Color"],normal.inputs["Color"])
    material.node_tree.links.new(normal.outputs["Normal"],shader.inputs["Normal"])
    bpy.data.objects.remove(reference,do_unlink=True)
    rig.data.pose_position="POSE"
    hip_name="mixamorig:Hips"
    hip_origin=sampled["Idle"][1][0][hip_name][0].copy()
    rig.animation_data_create()
    root_ranges={}
    for label,(duration,poses) in sampled.items():
        action=bpy.data.actions.new(label)
        rig.animation_data.action=action
        root_ranges[label]=max((p[hip_name][0]-poses[0][hip_name][0]).length for p in poses)
        for index,pose in enumerate(poses):
            for name,(loc,rot,scale_) in pose.items():
                bone=rig.pose.bones[name]
                bone.rotation_mode="QUATERNION"
                bone.location=loc
                if name==hip_name:
                    bone.location.x=hip_origin.x
                    bone.location.z=hip_origin.z
                bone.rotation_quaternion=rot
                bone.scale=scale_
                for path in ["location","rotation_quaternion","scale"]:
                    bone.keyframe_insert(path,frame=1+index,group=name)
        rig.animation_data.action=None
        track=rig.animation_data.nla_tracks.new()
        track.name=label
        track.strips.new(label,1,action)
        track.mute=True
    # A wrapper preserves the supplied skeleton's rest matrices and skin bindings.
    wrapper=bpy.data.objects.new("Qinglan_UserModel",None)
    scene.collection.objects.link(wrapper)
    for obj in list(base_objects):
        if obj.name in scene.objects and obj.parent is None:
            world=obj.matrix_world.copy()
            obj.parent=wrapper
            obj.matrix_world=world
    wrapper.scale=(1.70/height,)*3
    wrapper.location.z=-low*(1.70/height)
    rig.animation_data.nla_tracks[0].mute=False
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    for track in rig.animation_data.nla_tracks:
        track.mute=False
    bpy.ops.object.select_all(action="DESELECT")
    for obj in scene.objects:
        if obj.type in ["MESH","ARMATURE","EMPTY"] and obj not in {p.custom_shape for p in rig.pose.bones if p.custom_shape}:
            obj.select_set(True)
    bpy.context.view_layer.objects.active=rig
    bpy.ops.export_scene.gltf(filepath=str(GAME),export_format="GLB",export_yup=True,use_selection=True,
        export_animations=True,export_animation_mode="NLA_TRACKS",export_force_sampling=True)
    report={"status":"PASS_WITH_LIMITATIONS","bones":len(names),"clips":{k:v[0] for k,v in sampled.items()},
        "rest_matrix_errors":rest_errors,"original_idle_height_m":height,"uniform_scale":1.7/height,
        "original_root_travel_m":root_ranges,"surface":"Recovered by selected-to-active color/roughness/normal baking from retained v002 surface",
        "input_hashes":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [incoming/"CHAR_001_Qinglan_v001_source.glb",incoming/"Walking.fbx",incoming/"Fast Run.fbx"]},
        "limitations":"User skeleton and weights retained; no procedural gait. Surface projection needs visual review; no terrain foot IK."}
    (ROOT/"reports/validation/Qinglan_UserMotion_v006.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("USER_MOTION_MERGED",json.dumps(report))


if __name__=="__main__":
    main()
