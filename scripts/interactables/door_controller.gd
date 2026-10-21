extends StaticBody3D

var unlocked := false

func _ready() -> void:
	add_to_group("interactable")
	get_parent().get_node("GameState").door_unlocked.connect(_on_unlocked)

func _on_unlocked() -> void:
	unlocked = true
	$MeshInstance3D.material_override = StandardMaterial3D.new()
	$MeshInstance3D.material_override.albedo_color = Color(0.35, 0.42, 0.3)

func interact(_player: Node3D) -> void:
	if not unlocked:
		return
	var tween := create_tween()
	tween.tween_property(self, "rotation:y", rotation.y + PI * 0.5, 0.8)
	$CollisionShape3D.set_deferred("disabled", true)
