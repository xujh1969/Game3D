extends Node3D

@onready var animation_player: AnimationPlayer = find_child("AnimationPlayer", true, false)

func _ready() -> void:
	for name in ["Idle", "Walk", "Run"]:
		animation_player.get_animation(name).loop_mode = Animation.LOOP_LINEAR
	animation_player.play("Idle")

func update_movement(planar_speed: float, running: bool) -> void:
	var next := "Idle" if planar_speed < 0.1 else ("Run" if running else "Walk")
	if animation_player.current_animation != next:
		var previous := animation_player.current_animation
		var phase := animation_player.current_animation_position / maxf(animation_player.current_animation_length, .001)
		animation_player.play(next, 0.18)
		if previous in ["Walk", "Run"] and next in ["Walk", "Run"]:
			animation_player.seek(phase * animation_player.get_animation(next).length)
