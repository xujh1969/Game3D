"""Material-only v003 from editable v002 source, with continuous world-scale UVs."""
import bpy
import json
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_door as door

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"assets/source/ARCH_Courtyard_v003.blend"
GAME=ROOT/"assets/game/ARCH_Courtyard_v003_game.glb"


def material(asset):
    folder=ROOT/"assets/source/third_party"/asset
    records=json.loads((folder/"provenance.json").read_text(encoding="utf-8"))
    mat=bpy.data.materials.new("PH_"+asset+"_PBR")
    mat.use_nodes=True
    shader=mat.node_tree.nodes["Principled BSDF"]
    for record in records:
        channel=record["channel"]
        image=bpy.data.images.load(str(folder/record["file"]))
        image.colorspace_settings.name="sRGB" if channel=="Diffuse" else "Non-Color"
        image.pack()
        node=mat.node_tree.nodes.new("ShaderNodeTexImage")
        node.image=image
        if channel=="nor_gl":
            normal=mat.node_tree.nodes.new("ShaderNodeNormalMap")
            normal.inputs["Strength"].default_value=.65
            mat.node_tree.links.new(node.outputs["Color"],normal.inputs["Color"])
            mat.node_tree.links.new(normal.outputs["Normal"],shader.inputs["Normal"])
        else:
            mat.node_tree.links.new(node.outputs["Color"],shader.inputs["Base Color" if channel=="Diffuse" else "Roughness"])
    return mat


def main():
    if SOURCE.exists() or GAME.exists():
        raise FileExistsError("Preserve courtyard v003")
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/"assets/source/ARCH_Courtyard_v002.blend"))
    swaps={"Courtyard_Earth":(material("brown_mud_02"),1.3),"Courtyard_Lime_Plaster":(material("plastered_wall_02"),2.2)}
    updated=[]
    for obj in bpy.context.scene.objects:
        if obj.type!="MESH" or not obj.data.materials:
            continue
        current=obj.data.materials[0].name
        if current not in swaps:
            continue
        replacement,scale=swaps[current]
        obj.data.materials[0]=replacement
        uv=obj.data.uv_layers.active or obj.data.uv_layers.new()
        for face in obj.data.polygons:
            normal=obj.matrix_world.to_3x3()@face.normal
            axes=[i for i in range(3) if i!=max(range(3),key=lambda i:abs(normal[i]))]
            for loop in face.loop_indices:
                co=obj.matrix_world@obj.data.vertices[obj.data.loops[loop].vertex_index].co
                uv.data[loop].uv=(co[axes[0]]/scale,co[axes[1]]/scale)
        updated.append(obj.name)
    if not updated:
        raise RuntimeError("No matching surface objects")
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    root=bpy.data.objects["CourtyardArchitecture"]
    for group in list(root.children):
        door.join_parts(group)
    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active=root
    bpy.ops.export_scene.gltf(filepath=str(GAME),export_format="GLB",use_selection=True,export_yup=True,export_animations=False)
    print("SURFACE_UPGRADE: "+str(len(updated))+" objects; unchanged geometry")


if __name__=="__main__":
    main()
