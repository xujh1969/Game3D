"""Versioned garden dressing and irregular background ridges; existing gameplay geometry stays intact."""
import math
import random
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/game/ENV_CourtyardGarden_v003_game.glb'
random.seed(261026)



import struct

class Vector(tuple):
    def __add__(self,o): return Vector(a+b for a,b in zip(self,o))
    def __sub__(self,o): return Vector(a-b for a,b in zip(self,o))
    def __mul__(self,n): return Vector(a*n for a in self)
    def normalized(self):
        length=math.sqrt(sum(a*a for a in self))
        return self*(1/length) if length>1e-9 else Vector((1,0,0))
    def cross(self,o):
        a,b,c=self; x,y,z=o
        return Vector((b*z-c*y,c*x-a*z,a*y-b*x))

def material(name,color,roughness=.8): return {'name':name,'pbrMetallicRoughness':{'baseColorFactor':[*color,1],'metallicFactor':0,'roughnessFactor':roughness},'doubleSided':True}

class Batch:
    def __init__(self,name,materials): self.name=name; self.materials=materials; self.faces=[]
    def face(self,points,mat=0): self.faces.append((list(points),mat))
    def object(self): return self

def leaf(batch,base,direction,length,width,mat):
    direction=direction.normalized(); cross=direction.cross(Vector((0,0,1))).normalized()
    center=base+direction*(length*.48)+Vector((0,0,.025 if length>.15 else .003))
    tip=base+direction*length+Vector((0,0,-length*.25)); near=base+direction*(length*.25); far=base+direction*(length*.72)
    for sign in [-1,1]:
        e1=near+cross*(width*sign); e2=far+cross*(width*.55*sign)
        for points in [[base,e1,center],[e1,e2,center],[e2,tip,center]]:
            batch.face(points if sign==1 else list(reversed(points)),mat)

def export(objects,name):
    data=bytearray(); views=[]; accessors=[]; meshes=[]; materials=[]; nodes=[]
    def accessor(values,kind,count,shape,limits=None,target=34962):
        while len(data)%4: data.append(0)
        offset=len(data); data.extend(struct.pack('<'+str(len(values))+kind,*values))
        views.append({'buffer':0,'byteOffset':offset,'byteLength':len(data)-offset,'target':target})
        item={'bufferView':len(views)-1,'componentType':5126 if kind=='f' else 5125,'count':count,'type':shape}
        if limits: item.update(min=limits[0],max=limits[1])
        accessors.append(item); return len(accessors)-1
    for obj in objects:
        primitives=[]
        for mi,mat in enumerate(obj.materials):
            vertices=[]; normals=[]; indices=[]; lookup={}
            for face,index in obj.faces:
                if index!=mi: continue
                ids=[]
                for v in face:
                    # Blender Z-up to glTF/Godot Y-up, proper rotation.
                    p=(v[0],v[2],-v[1]); key=tuple(round(a,6) for a in p)
                    if key not in lookup: lookup[key]=len(vertices);vertices.append(Vector(p));normals.append(Vector((0,0,0)))
                    ids.append(lookup[key])
                for j in range(1,len(ids)-1):
                    tri=[ids[0],ids[j],ids[j+1]]
                    n=(vertices[tri[1]]-vertices[tri[0]]).cross(vertices[tri[2]]-vertices[tri[0]])
                    if sum(x*x for x in n)<1e-14: continue
                    indices.extend(tri)
                    for vi in tri: normals[vi]=normals[vi]+n
            if not indices: continue
            pos=[x for v in vertices for x in v]; norm=[x for n in normals for x in n.normalized()]
            pa=accessor(pos,'f',len(vertices),'VEC3',([min(v[k] for v in vertices) for k in range(3)],[max(v[k] for v in vertices) for k in range(3)]))
            na=accessor(norm,'f',len(vertices),'VEC3'); ia=accessor(indices,'I',len(indices),'SCALAR',target=34963)
            materials.append(mat); primitives.append({'attributes':{'POSITION':pa,'NORMAL':na},'indices':ia,'material':len(materials)-1})
        meshes.append({'name':obj.name,'primitives':primitives});nodes.append({'name':obj.name,'mesh':len(meshes)-1})
    doc={'asset':{'version':'2.0','generator':'MountainCourtyard authored mesh builder'},'scene':0,'scenes':[{'nodes':list(range(len(nodes)))}],'nodes':nodes,'meshes':meshes,'materials':materials,'buffers':[{'byteLength':len(data)}],'bufferViews':views,'accessors':accessors}
    text=json.dumps(doc,separators=(',',':')).encode()
    text+=b' '*((-len(text))%4);data+=b'\0'*((-len(data))%4)
    output=struct.pack('<III',0x46546c67,2,12+8+len(text)+8+len(data))+struct.pack('<II',len(text),0x4e4f534a)+text+struct.pack('<II',len(data),0x004e4942)+data
    (ROOT/'assets/game'/name).write_bytes(output)
    print('EXPORTED',name,len(output),'bytes',sum(len(m['primitives']) for m in meshes),'surfaces')


def sphere(batch, center, radius, stretch, mat):
    rings, sides = 4, 7
    def point(i, j):
        a, b = math.pi*i/rings, math.tau*(j % sides)/sides
        r = radius*(1+.09*math.sin((j % sides)*3.7+i*2.3)*math.sin(a))
        return center+Vector((math.sin(a)*math.cos(b)*r*stretch[0], math.sin(a)*math.sin(b)*r*stretch[1], math.cos(a)*r*stretch[2]))
    for i in range(rings):
        for j in range(sides):
            batch.face([point(i,j),point(i,j+1),point(i+1,j+1),point(i+1,j)],mat)




def main():
    if SOURCE.exists(): raise FileExistsError('Preserve garden v003; use a new version')
    greens=[material('Garden_Leaf_'+str(i),c) for i,c in enumerate([(.115,.18,.058),(.20,.26,.078),(.29,.30,.12)])]
    grass=Batch('Garden_Low_Grass',greens)
    ferns=Batch('Garden_Ferns',greens)
    dry=Batch('Garden_Fallen_Leaves',[material('Dry_Leaf_Ochre',(.21,.15,.075)),material('Dry_Leaf_Umber',(.125,.105,.055))])
    stones=Batch('Garden_Pebbles',[material('Pebble_Gray',(.22,.245,.205)),material('Pebble_Warm',(.32,.29,.225))])
    # Patches hug the path edge, walls and existing rock/plant groups; no decoration colliders.
    patches=[(-2.15,z,.32) for z in [-1,1.2,3.8,7.1,10.6,12.8]]+[(2.2,z,.30) for z in [-2.3,.2,4.6,8.3,11.8]]
    patches += [(-10,8,1.5),(10,9,1.7),(-11,3,1.3),(11,2,1.4),(-8,-.2,1.8),(8,-3,1.8),(-10,-6,1.2),(5.8,2.0,1.0),(-6.5,-4.7,1.0),(-13,12,1.2),(13,12,1.2)]
    grass_count=0
    for x,y,radius in patches:
        for _ in range(int(35+radius*65)):
            angle=random.random()*math.tau; r=radius*math.sqrt(random.random())
            center=Vector((x+math.cos(angle)*r, -(y+math.sin(angle)*r), .008))
            for blade in range(random.randint(4,8)):
                a=random.random()*math.tau; h=random.uniform(.08,.27)*(1 if radius>.5 else .65)
                direction=Vector((math.cos(a)*.35,math.sin(a)*.35,1))
                leaf(grass,center,direction,h,random.uniform(.006,.012),random.randrange(3))
                grass_count+=1
        for _ in range(int(radius*22+5)):
            a=random.random()*math.tau; r=radius*random.random()
            base=Vector((x+math.cos(a)*r,-y+math.sin(a)*r,.012))
            leaf(dry,base,Vector((math.cos(a),math.sin(a),.02)),random.uniform(.045,.13),random.uniform(.012,.022),random.randrange(2))
        for _ in range(int(radius*12+4)):
            a=random.random()*math.tau; r=radius*random.random()
            sphere(stones,Vector((x+math.cos(a)*r,-y+math.sin(a)*r,.012)),random.uniform(.012,.045),(1.3,.8,.55),random.randrange(2))
    fern_centers=[(-8.6,-.2),(-10.4,-5.4),(8.9,-2.6),(10.2,6),(-11,6.8),(5.6,2.3),(-6,-4.8),(-12,11.5),(12.4,11.8)]
    for x,y in fern_centers:
        for plant in range(3):
            base=Vector((x+random.uniform(-.28,.28),-y+random.uniform(-.28,.28),.02))
            for frond in range(7):
                a=frond*math.tau/7+plant*.7; length=random.uniform(.32,.62)
                forward=Vector((math.cos(a),math.sin(a),0))
                for section in range(1,11):
                    t=section/11
                    stem=base+forward*(length*t)+Vector((0,0,math.sin(t*math.pi*.85)*length*.65))
                    for sign in [-1,1]:
                        direction=Vector((math.cos(a+sign*1.02),math.sin(a+sign*1.02),.05))
                        leaf(ferns,stem,direction,length*.26*math.sin(t*math.pi),.012*math.sin(t*math.pi),random.randrange(3))
    shrubs=Batch('Garden_Shrubs',greens)
    for x,y in [(-10.5,7.8),(10.5,7.2),(-9.5,-.9),(9.0,-3.4),(-11,-5.0),(6.0,1.9)]:
        for branch in range(18):
            angle=random.random()*math.tau; radius=random.uniform(.1,.65)
            base=Vector((x+math.cos(angle)*radius,-y+math.sin(angle)*radius,random.uniform(.13,.60)))
            for k in range(6):
                a=angle+k*2.4
                leaf(shrubs,base+Vector((0,0,k*.038)),Vector((math.cos(a),math.sin(a),random.uniform(-.1,.4))),random.uniform(.12,.23),random.uniform(.025,.047),random.randrange(3))
    timber=Batch('Garden_Wooden_Bench',[material('Bench_Aged_Wood',(.19,.145,.083),.91)])
    def board(center,size):
        x,y,z=center; a,b,c=(v/2 for v in size)
        v=[Vector((x+sx*a,y+sy*b,z+sz*c)) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
        for ids in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: timber.face([v[i] for i in ids])
    # A small aged plank bench, grouped with the scroll table, outside the input route.
    for y in [5.52,5.69]: board((-5.8,-y,.40),(1.12,.15,.075))
    for x in [-6.17,-5.43]:
        for y in [5.53,5.69]: board((x,-y,.19),(.065,.07,.38))
    board((-5.8,-5.61,.16),(.92,.055,.06))
    jar=Batch('Garden_Earthen_Jar',[material('Jar_Unglazed_Clay',(.18,.125,.075),.9),material('Jar_Dark_Interior',(.045,.038,.025),.98)])
    profile=[(.12,0),(.18,.04),(.235,.19),(.24,.31),(.21,.43),(.145,.51),(.14,.55),(.115,.55),(.115,.49),(.14,.43),(.15,.34),(.04,.29)]
    for ring in range(len(profile)-1):
        for j in range(32):
            points=[]
            for ri,si in [(ring,j),(ring,j+1),(ring+1,j+1),(ring+1,j)]:
                r,z=profile[ri];a=si*math.tau/32
                r*=1+.015*math.sin(z*90)
                points.append(Vector((-5.35+r*math.cos(a),-4.45+r*math.sin(a),z)))
            jar.face(points,0 if ring<8 else 1)
    garden=[grass.object(),ferns.object(),dry.object(),stones.object(),shrubs.object(),timber.object(),jar.object()]
    # Background uses many overlapping narrow peaks and ridged slope detail, never a playable surface.
    ridges=[]
    for layer in range(4):
        color=[(.18,.235,.22),(.265,.335,.34),(.365,.425,.43),(.47,.52,.52)][layer]
        batch=Batch('Atmosphere_Ridge_'+str(layer+1),[material('Ridge_Stone_'+str(layer+1),color,.98)])
        nx,ny=220,36
        peaks=[(random.uniform(-190,190),random.uniform(16,40)*(1+layer*.22),random.uniform(11,27)) for _ in range(14)]
        def point(ix,iy):
            x=-230+460*ix/nx; y=62+layer*60+iy/ny*75
            profile=max(h*math.exp(-abs((x-p)/w)**1.8) for p,h,w in peaks)
            t=iy/ny; envelope=math.sin(math.pi*t)**.85
            ridge=abs(math.sin(x*.095+y*.054))*3.2+math.sin(x*.26-y*.19)*.7+math.sin(x*.57+y*.33)*.26
            z=-4+(profile+ridge)*envelope
            return Vector((x,y,z))
        for iy in range(ny):
            for ix in range(nx):
                batch.face([point(ix,iy),point(ix+1,iy),point(ix+1,iy+1),point(ix,iy+1)])
        ridges.append(batch.object())
    # Pack authored source including all details; export independent runtime groups.
    export(garden,'ENV_CourtyardGarden_v003_game.glb')
    if not (ROOT/'assets/game/ENV_DistantMountains_v004_game.glb').exists():
        export(ridges,'ENV_DistantMountains_v004_game.glb')
    report={'grass_blades':grass_count,'fern_plants':len(fern_centers)*3,'garden_meshes':len(garden),'ridge_layers':4,'collision':'none; decorative patches outside the original route','source':'tools/python/build_courtyard_garden.py; Blender executable unavailable this run'}
    (ROOT/'reports/validation/Courtyard_Garden_v003.json').write_text(json.dumps(report,indent=2)+'\n')
    print('GARDEN_BUILD:',json.dumps(report))


if __name__=='__main__': main()
