extends SpringArm3D

@export var sensitivity := 0.003
var pitch := -0.18

func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotation.y -= event.relative.x * sensitivity
		pitch = clampf(pitch - event.relative.y * sensitivity, -0.8, 0.35)
		rotation.x = pitch
	if event.is_action_pressed("pause"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
