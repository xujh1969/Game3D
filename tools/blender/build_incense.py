"""Approved-direction bronze burner: closed thick-walled vessel and three stable feet."""
import bpy
import bmesh
import math
import numpy as np
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"assets/source/PROP_001_IncenseBurner_v002.blend"
GAME=ROOT/"assets/game/PROP_001_IncenseBurner_v002_game.glb"
TEX=ROOT/"assets/source/materials/Incense_v002"


def bronze():
    n=1024
    rng=np.random.default_rng(22131)
    field=np.zeros((n,n),dtype=np.float32)
    for frequency,amount in [(4,.45),(12,.27),(40,.16),(120,.08)]:
        grid=rng.uniform(-1,1,(frequency,frequency))
        co=np.arange(n)*frequency/n
        index=co.astype(int)
        t=co-index
        t=t*t*(3-2*t)
        a=grid[index[:,None]%frequency,index[None,:]%frequency]
        b=grid[index[:,None]%frequency,(index[None,:]+1)%frequency]
        c=grid[(index[:,None]+1)%frequency,index[None,:]%frequency]
        d=grid[(index[:,None]+1)%frequency,(index[None,:]+1)%frequency]
        field+=amount*((a*(1-t[None,:])+b*t[None,:])*(1-t[:,None])+(c*(1-t[None,:])+d*t[None,:])*t[:,None])
    grain=rng.normal(0,.035,(n,n)).astype(np.float32)
    patina=np.clip((field-.025)*4,0,1)
    base=np.array([.22,.14,.075])[None,None,:]*(1+field[:,:,None]*.7+grain[:,:,None]*2)
    base=base*(1-patina[:,:,None])+np.array([.038,.092,.068])[None,None,:]*patina[:,:,None]
    rough=np.clip(.62+patina*.24+field*.1+grain,.48,.95)
    metallic=.75-patina*.65
    height=field*.17+grain*.70
    dx=(np.roll(height,-1,1)-np.roll(height,1,1))*2
    dy=(np.roll(height,-1,0)-np.roll(height,1,0))*2
    normals=np.stack([-dx,-dy,np.ones_like(dx)],axis=-1)
    normals/=np.linalg.norm(normals,axis=-1,keepdims=True)
    channels={"BaseColor":np.clip(base,.005,.9),"Roughness":np.repeat(rough[:,:,None],3,2),"Metallic":np.repeat(metallic[:,:,None],3,2),"Normal":normals*.5+.5}
    mat=bpy.data.materials.new("Aged_Bronze_Patina_PBR")
    mat.use_nodes=True
    shader=mat.node_tree.nodes.get("Principled BSDF")
    for channel,rgb in channels.items():
        image=bpy.data.images.new("Incense_"+channel,width=n,height=n)
        image.colorspace_settings.name="sRGB" if channel=="BaseColor" else "Non-Color"
        pixels=np.concatenate([rgb,np.ones((n,n,1))],axis=-1).astype(np.float32)
        image.pixels.foreach_set(pixels.ravel())
        image.filepath_raw=str(TEX/(image.name+".png"))
        image.file_format="PNG"
        image.save()
        image.pack()
        node=mat.node_tree.nodes.new("ShaderNodeTexImage")
        node.image=image
        if channel=="Normal":
            normal=mat.node_tree.nodes.new("ShaderNodeNormalMap")
            normal.inputs["Strength"].default_value=.45
            mat.node_tree.links.new(node.outputs["Color"],normal.inputs["Color"])
            mat.node_tree.links.new(normal.outputs["Normal"],shader.inputs["Normal"])
        else:
            mat.node_tree.links.new(node.outputs["Color"],shader.inputs["Base Color" if channel=="BaseColor" else channel])
    return mat


def lathe(name,profile,segments,material,center=(0,0,0)):
    vertices=[]
    rings=[]
    faces=[]
    for radius,z in profile:
        ring=[]
        for i in range(1 if radius==0 else segments):
            theta=i/segments*math.tau
            ring.append(len(vertices))
            vertices.append((center[0]+radius*math.cos(theta),center[1]+radius*math.sin(theta),center[2]+z))
        rings.append(ring)
    for index in range(len(rings)-1):
        a,b=rings[index:index+2]
        for i in range(segments):
            j=(i+1)%segments
            if len(a)==1:
                faces.append((a[0],b[j],b[i]))
            elif len(b)==1:
                faces.append((a[i],a[j],b[0]))
            else:
                faces.append((a[i],a[j],b[j],b[i]))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    bm=bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    mesh.materials.append(material)
    uv=mesh.uv_layers.new()
    for face in mesh.polygons:
        face.use_smooth=True
        coords=[]
        for loop in face.loop_indices:
            co=mesh.vertices[mesh.loops[loop].vertex_index].co
            u=(math.atan2(co.y-center[1],co.x-center[0])/math.tau)%1
            coords.append((loop,u,(co.z-center[2])/.35))
        seam=max(c[1] for c in coords)-min(c[1] for c in coords)>.5
        for loop,u,v in coords:
            uv.data[loop].uv=(u+1 if seam and u<.5 else u,v)
    return obj


def main():
    if SOURCE.exists() or GAME.exists():
        raise FileExistsError("Preserve incense v002")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    TEX.mkdir(parents=True,exist_ok=True)
    mat=bronze()
    profile=[(0,.09),(.12,.09),(.17,.095),(.202,.13),(.216,.18),(.214,.215),(.205,.255),(.194,.275),(.198,.29),(.222,.312),(.225,.326),(.222,.34),(.214,.35),(.200,.349),(.193,.338),(.194,.326),(.202,.318),(.196,.313),(.185,.29),(.183,.27),(.193,.24),(.201,.20),(.20,.17),(.182,.13),(.145,.113),(0,.113)]
    body=lathe("Bowl_With_Interior",profile,64,mat)
    feet=[]
    for i in range(3):
        angle=-math.pi/2+i*math.tau/3
        center=(.155*math.cos(angle),.155*math.sin(angle),0)
        feet.append(lathe("Foot_"+str(i+1),[(0,0),(.029,0),(.032,.008),(.030,.045),(.035,.080),(.040,.103),(0,.103)],20,mat,center))
    root=bpy.data.objects.new("IncenseBurner",None)
    bpy.context.collection.objects.link(root)
    for obj in [body,*feet]:
        obj.parent=root
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active=root
    bpy.ops.export_scene.gltf(filepath=str(GAME),export_format="GLB",use_selection=True,export_yup=True,export_animations=False)
    print("INCENSE_BUILD: thick-walled open vessel with three feet exported")


if __name__=="__main__":
    main()
