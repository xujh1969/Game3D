"""Write explicit simplified architecture collisions; dimensions match build_courtyard.py."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
resources = []
nodes = []


def vector(point):
    return "Vector3(" + ", ".join(str(round(value, 5)) for value in point) + ")"


def shape(name, points=None, size=None):
    if size:
        resources.append(f'[sub_resource type="BoxShape3D" id="{name}"]\nsize = {vector(size)}\n')
    else:
        values = ", ".join(str(round(value, 5)) for point in points for value in point)
        resources.append(f'[sub_resource type="ConvexPolygonShape3D" id="{name}"]\npoints = PackedVector3Array({values})\n')


def box(name, position, size):
    shape(name, size=size)
    nodes.append(f'[node name="{name}" type="CollisionShape3D" parent="Collision"]\nposition = {vector(position)}\nshape = SubResource("{name}")\n')


def main():
    box("Platform", (0,.15,-9.3), (12,.30,8))
    # The wedge spans the visible steps. Top runs from y=0 at z=-4.4 to .3 at -5.4.
    shape("StepRamp", points=[(x,y,z) for x in [-1.9,1.9] for y,z in [(0,-4.4),(0,-5.4),(.30,-5.4)]])
    nodes.append('[node name="StepRamp" type="CollisionShape3D" parent="Collision"]\nshape = SubResource("StepRamp")\n')
    for side, label in [(-1,"Left"),(1,"Right")]:
        box(label+"Facade", (side*3.31,1.65,-8), (4.38,2.70,.20))
        box(label+"Rear", (side*3.31,1.65,-11.6), (4.38,2.70,.20))
        box(label+"End", (side*5.5,1.65,-9.8), (.20,2.70,3.8))
        box(label+"CrossWall", (side*10.25,.95,-8), (9.5,1.9,.35))
        for index,z in enumerate([-6.8,-11.8]):
            for column,x in enumerate([-5.4,-1.8,1.8,5.4]):
                if side == -1:
                    box(f"Post_{index}_{column}", (x,1.85,z), (.32,3.1,.32))
    box("DoorHead", (0,3.06,-8), (2.24,.20,.20))
    for label, end in [("FrontRoof",-6.1),("RearRoof",-12.8)]:
        shape(label, points=[(x,y,z) for x in [-6.5,6.5] for y,z in [(3.35,end),(3.58,end),(5.12,-9.3),(4.85,-9.3)]])
        nodes.append(f'[node name="{label}" type="CollisionShape3D" parent="Collision"]\nshape = SubResource("{label}")\n')
    content = f'''[gd_scene load_steps={len(resources)+2} format=3]

[ext_resource type="PackedScene" path="res://assets/game/ARCH_Courtyard_v002_game.glb" id="1"]

''' + "\n".join(resources) + '''
[node name="Architecture" type="Node3D"]

[node name="Visual" parent="." instance=ExtResource("1")]

[node name="Collision" type="StaticBody3D" parent="."]

''' + "\n".join(nodes)
    (ROOT / "scenes/world/CourtyardArchitecture.tscn").write_text(content, encoding="utf-8")
    print("ARCHITECTURE_SCENE: explicit simplified colliders written")


if __name__ == "__main__":
    main()
