"""Keep explicit stem collisions aligned with build_landscape.py."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
stems=[(-.45,-.25,4.4),(.05,-.4,4.8),(.5,-.05,4.2),(-.25,.35,3.7),(.4,.4,4.5),(-.65,.2,4.0)]
text='''[gd_scene load_steps=9 format=3]

[ext_resource type="PackedScene" path="res://assets/game/NAT_002_BambooClump_v002_game.glb" id="1"]
[ext_resource type="PackedScene" path="res://assets/game/ENV_DistantMountains_v002_game.glb" id="2"]

'''
for i,(_,_,height) in enumerate(stems):
    text+=f'[sub_resource type="CylinderShape3D" id="Stem{i}"]\nradius = 0.06\nheight = {height}\n\n'
text+='[node name="EnvironmentScenery" type="Node3D"]\n\n[node name="Mountains" parent="." instance=ExtResource("2")]\n\n'
for name,x,z,yaw in [('BambooWest',-11,5,.2),('BambooEast',11,6,-.5),('BambooNorthwest',-11,-5,1.2),('BambooNortheast',11.5,-5,.8)]:
    text+=f'[node name="{name}" type="StaticBody3D" parent="."]\nposition = Vector3({x}, 0, {z})\nrotation = Vector3(0, {yaw}, 0)\n\n[node name="Visual" parent="{name}" instance=ExtResource("1")]\n\n'
    for i,(sx,sy,height) in enumerate(stems):
        text+=f'[node name="Stem{i}" type="CollisionShape3D" parent="{name}"]\nposition = Vector3({sx}, {height/2}, {-sy})\nshape = SubResource("Stem{i}")\n\n'
(ROOT/'scenes/world/EnvironmentScenery.tscn').write_text(text.rstrip()+'\n',encoding='utf-8')
print('LANDSCAPE_SCENE: 4 clumps / 24 stem shapes / background without collision')
