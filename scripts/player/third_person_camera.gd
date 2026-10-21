extends SpringArm3D

@export var sensitivity := 0.003
var pitch := -0.18

func _ready() -> void:
	add_excluded_object(get_parent().get_rid())
	rotation.x = pitch
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotation.y -= event.relative.x * sensitivity
		pitch = clampf(pitch - event.relative.y * sensitivity, -0.8, 0.35)
		rotation.x = pitch
