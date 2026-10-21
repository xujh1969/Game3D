"""Project-authored bamboo and distant landscape, no external model inputs."""
import bpy
import bmesh
import math
import random
import sys
from pathlib import Path
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_courtyard as courtyard

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source/ENV_BambooLandscape_v002.blend"
random.seed(22110)


def material(name, color, roughness=.8):
    mat=bpy.data.materials.new(name)
    mat.use_nodes=True
    shader=mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value=(*color,1)
    shader.inputs["Roughness"].default_value=roughness
    mat.diffuse_color=(*color,1)
    mat.use_backface_culling=False
    return mat


class Batch:
    def __init__(self, name, materials):
        self.name=name
        self.materials=materials
        self.vertices=[]
        self.faces=[]
        self.indices=[]

    def face(self, points, mat=0):
        start=len(self.vertices)
        self.vertices.extend(tuple(p) for p in points)
        self.faces.append(tuple(range(start,start+len(points))))
        self.indices.append(mat)

    def tube(self, start, end, r0, r1, mat=0, sides=10):
        axis=(end-start).normalized()
        cross=axis.cross(Vector((0,1,0))).normalized()
        if cross.length < .1:
            cross=axis.cross(Vector((1,0,0))).normalized()
        other=axis.cross(cross).normalized()
        rings=[]
        for point,radius in [(start,r0),(end,r1)]:
            rings.append([point+radius*(math.cos(i*2*math.pi/sides)*cross+math.sin(i*2*math.pi/sides)*other) for i in range(sides)])
        for i in range(sides):
            j=(i+1)%sides
            self.face([rings[0][i],rings[0][j],rings[1][j],rings[1][i]],mat)
        self.face(list(reversed(rings[0])),mat)
        self.face(rings[1],mat)

    def object(self):
        mesh=bpy.data.meshes.new(self.name)
        mesh.from_pydata(self.vertices,[],self.faces)
        mesh.update()
        obj=bpy.data.objects.new(self.name,mesh)
        bpy.context.collection.objects.link(obj)
        for mat in self.materials:
            mesh.materials.append(mat)
        for face,index in zip(mesh.polygons,self.indices):
            face.material_index=index
            face.use_smooth=True
        # Shared vertices are required for continuous normals across adjacent faces.
        bm=bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        courtyard.mineral_uv(obj,.4)
        return obj


def leaf(batch, base, direction, length, width, mat):
    direction=direction.normalized()
    cross=direction.cross(Vector((0,0,1))).normalized()
    if cross.length < .1:
        cross=Vector((1,0,0))
    # Folded central vein and drooping tip form six triangles, no alpha cards.
    center=base+direction*length*.48+Vector((0,0,.025))
    tip=base+direction*length+Vector((0,0,-length*.25))
    near=base+direction*length*.25
    far=base+direction*length*.72
    for sign in [-1,1]:
        edge1=near+cross*width*sign
        edge2=far+cross*width*.55*sign
        faces=[[base,edge1,center],[edge1,edge2,center],[edge2,tip,center]]
        for points in faces:
            batch.face(points if sign==1 else list(reversed(points)),mat)


def main():
    if SOURCE.exists():
        raise FileExistsError("Preserve landscape v002; build a new version")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    courtyard.TEXTURES=ROOT/"assets/source/materials/BambooLandscape_v002"
    courtyard.TEXTURES.mkdir(parents=True,exist_ok=True)
    culm=courtyard.pbr("Bamboo_Culm_PBR",(.14,.20,.055),121,.72)
    node=material("Bamboo_Node",(.17,.21,.09),.9)
    leaves=[material("Bamboo_Leaf_"+str(i),color,.76) for i,color in enumerate([(.075,.15,.035),(.12,.21,.055),(.18,.25,.075)])]
    bamboo=Batch("Bamboo_Clump",[culm,node,*leaves])
    # Positions are reused by the Godot stem colliders.
    stems=[(-.45,-.25,4.4),(.05,-.4,4.8),(.5,-.05,4.2),(-.25,.35,3.7),(.4,.4,4.5),(-.65,.2,4.0)]
    for index,(x,y,height) in enumerate(stems):
        lean=Vector((random.uniform(-.25,.25),random.uniform(-.25,.25),height))
        base=Vector((x,y,0))
        for segment in range(13):
            t0,t1=segment/13,(segment+1)/13
            a,b=base+lean*t0,base+lean*t1
            radius=.043*(1-.55*t0)
            bamboo.tube(a,b,radius,radius*.97,0,12)
            if segment:
                bamboo.tube(a-Vector((0,0,.012)),a+Vector((0,0,.016)),radius*1.17,radius*1.12,1,12)
            if segment < 4 or segment > 11:
                continue
            for branch in range(2):
                angle=index*1.3+segment*2.4+branch*2.6
                direction=Vector((math.cos(angle),math.sin(angle),.3))
                branch_length=random.uniform(.50,.90)*(1-.28*t0)
                end=a+direction*branch_length
                bamboo.tube(a,end,.009,.003,0,6)
                for k in range(7):
                    phase=(k+1)/8
                    twig=a+(end-a)*phase
                    sign=1 if k%2 else -1
                    out=Vector((math.cos(angle+sign*.75),math.sin(angle+sign*.75),random.uniform(-.25,.20)))
                    leaf(bamboo,twig,out,random.uniform(.19,.34),random.uniform(.017,.027),2+random.randrange(3))
    bamboo_obj=bamboo.object()
    # Three smooth ridges beyond the northern courtyard boundary, not playable terrain.
    mountain_mats=[courtyard.pbr("Mountain_Rock_"+str(i),color,130+i,.97) for i,color in enumerate([(.16,.20,.17),(.22,.28,.28),(.32,.38,.39)])]
    mountain_objs=[]
    for layer in range(3):
        ridge=Batch("Distant_Ridge_"+str(layer+1),[mountain_mats[layer]])
        nx,ny=300,60
        peaks=[(-95,19,18),(-48,32,15),(-10,27,21),(30,40,19),(75,30,20),(110,22,15)]
        def point(ix,iy):
            x=-155+310*ix/nx
            y=34+layer*48+iy/ny*64
            profile=sum(h*math.exp(-((x-p-layer*7)/width)**2) for p,h,width in peaks)
            # Feather slope edges into the valley; detail remains smooth at viewing distance.
            envelope=math.sin(math.pi*iy/ny)**1.5
            detail=(math.sin(x*.29+y*.13)*1.2+math.cos(x*.7-y*.17)*.45+math.sin(x*.13-y*.08)*2.0)*envelope
            z=-3+max(0,profile+detail)*(1+layer*.22)*envelope
            return Vector((x,y,z))
        for iy in range(ny):
            for ix in range(nx):
                ridge.face([point(ix,iy),point(ix+1,iy),point(ix+1,iy+1),point(ix,iy+1)])
        mountain_objs.append(ridge.object())
    for image in bpy.data.images:
        if image.source=="FILE":
            image.pack()
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    for name,objects in [("NAT_002_BambooClump_v002_game",[bamboo_obj]),("ENV_DistantMountains_v002_game",mountain_objs)]:
        target=ROOT/"assets/game"/(name+".glb")
        if target.exists():
            raise FileExistsError(str(target))
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active=objects[0]
        bpy.ops.export_scene.gltf(filepath=str(target),export_format="GLB",use_selection=True,export_yup=True,export_animations=False)
    print("LANDSCAPE_BUILD: bamboo and background ridges exported")


if __name__=="__main__":
    main()
