"""Project-authored scroll, low reading stand and inscribed-stone geometry."""
import bpy
import math
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_courtyard as courtyard
import build_door as door

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"assets/source/PROP_002_ClueSet_v002.blend"


def main():
    if SOURCE.exists():
        raise FileExistsError("Preserve clue source v002")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    courtyard.TEXTURES=ROOT/"assets/source/materials/ClueProps_v002"
    courtyard.TEXTURES.mkdir(parents=True,exist_ok=True)
    wood,_=door.materials()
    paper=courtyard.pbr("Scroll_Fiber_Paper",(.64,.53,.35),221,.97)
    stone=courtyard.pbr("Tablet_Weathered_Stone",(.25,.28,.26),222,.92)
    cloth=courtyard.pbr("Scroll_Linen_End",(.18,.24,.20),223,.91)
    scroll=door.empty("Scroll")
    stand=door.empty("ReadingStand")
    tablet=door.empty("StoneTablet")

    def box(name,pos,size,parent,mat,bevel=.006,grain="Z"):
        obj=door.box(name,pos,size,parent,mat,grain,bevel)
        if mat != wood:
            courtyard.mineral_uv(obj,.30)
        return obj

    # Paper surface has a shallow undulation and rolled ends, not a flat sprite.
    vertices=[]
    faces=[]
    for row in range(17):
        y=-.18+.36*row/16
        for col in range(25):
            x=-.27+.54*col/24
            z=.016+.004*math.cos(x*12)+.002*math.sin(y*18)
            vertices.append((x,y,z))
    for row in range(16):
        for col in range(24):
            i=row*25+col
            faces.append((i,i+1,i+26,i+25))
    mesh=bpy.data.meshes.new("Fiber_Paper_Surface")
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    obj=bpy.data.objects.new("Unrolled_Paper",mesh)
    bpy.context.collection.objects.link(obj)
    obj.parent=scroll
    obj.data.materials.append(paper)
    courtyard.mineral_uv(obj,.30)
    modifier=obj.modifiers.new("Paper_Thickness","SOLIDIFY")
    modifier.thickness=.0015
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    for x in [-.29,.29]:
        door.cylinder("Wood_Scroll_Roller",(x,0,.025),.018,.43,scroll,wood,(math.pi/2,0,0))
        door.cylinder("Paper_Roll",(x,0,.025),.026,.36,scroll,paper,(math.pi/2,0,0))
        for y in [-.22,.22]:
            door.cylinder("Roller_End_Cap",(x,y,.025),.023,.025,scroll,wood,(math.pi/2,0,0))
    for x in [-.252,.252]:
        box("Fabric_Edge",(x,0,.023),(.026,.36,.002),scroll,cloth,bevel=.0002)

    box("Reading_Top",(0,0,.66),(.95,.62,.08),stand,wood,.008,"X")
    for x in [-.38,.38]:
        for y in [-.22,.22]:
            box("Stand_Leg",(x,y,.31),(.065,.065,.62),stand,wood,.004)
        box("Stand_Side_Tie",(x,0,.18),(.05,.48,.045),stand,wood,.004)
    for y in [-.22,.22]:
        box("Stand_Long_Tie",(0,y,.52),(.80,.045,.10),stand,wood,.004,"X")

    box("Tablet_Base",(0,0,.08),(.90,.46,.16),tablet,stone,.022)
    box("Tablet_Lower_Lip",(0,0,.18),(.76,.32,.07),tablet,stone,.012)
    # Slight shoulders soften the slab silhouette while preserving a legible front.
    profile=[(-.32,.20),(.32,.20),(.32,1.25),(.26,1.34),(-.26,1.34),(-.32,1.25)]
    verts=[(x,y,z) for y in [-.115,.115] for x,z in profile]
    n=len(profile)
    polygons=[tuple(range(n)),tuple(reversed(range(n,2*n)))]
    polygons += [(i+n,(i+1)%n+n,(i+1)%n,i) for i in range(n)]
    mesh=bpy.data.meshes.new("Stone_Slab")
    mesh.from_pydata(verts,[],polygons)
    mesh.update()
    obj=bpy.data.objects.new("Tablet_Slab",mesh)
    bpy.context.collection.objects.link(obj)
    obj.parent=tablet
    obj.data.materials.append(stone)
    courtyard.mineral_uv(obj,.55)
    modifier=obj.modifiers.new("Weathered_Edge","BEVEL")
    modifier.width=.012
    modifier.segments=2
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    for x in [-.27,.27]:
        box("Tablet_Border",(x,-.12,.77),(.018,.012,.91),tablet,stone,.003)
    for z in [.32,1.23]:
        box("Tablet_Border",(0,-.12,z),(.55,.012,.018),tablet,stone,.003)
    # Godot front is +Z, Blender front is -Y. Text is separate scene-local lettering.
    for image in bpy.data.images:
        if image.source=="FILE":
            image.pack()
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    for root,name in [(scroll,"Scroll"),(stand,"ScrollStand"),(tablet,"StoneTablet")]:
        door.join_parts(root)
        bpy.ops.object.select_all(action="DESELECT")
        for obj in [root,*root.children_recursive]:
            obj.select_set(True)
        bpy.context.view_layer.objects.active=root
        destination=ROOT/"assets/game"/f"PROP_002_{name}_v002_game.glb"
        if destination.exists():
            raise FileExistsError(str(destination))
        bpy.ops.export_scene.gltf(filepath=str(destination),export_format="GLB",use_selection=True,export_yup=True,export_animations=False)
    print("CLUE_BUILD: scroll / stand / stone geometry exported")


if __name__=="__main__":
    main()
