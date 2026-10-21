extends Node3D

@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
	var library := AnimationLibrary.new()
	var idle := Animation.new()
	idle.length = 2.4
	idle.loop_mode = Animation.LOOP_LINEAR
	for joint in ["LeftLeg", "RightLeg", "LeftArm", "RightArm"]:
		var track := idle.add_track(Animation.TYPE_VALUE)
		idle.track_set_path(track, NodePath(joint + ":rotation"))
		idle.track_insert_key(track, 0, Vector3.ZERO)
	var breathing := idle.add_track(Animation.TYPE_VALUE)
	idle.track_set_path(breathing, NodePath("Torso:scale"))
	idle.track_insert_key(breathing, 0, Vector3.ONE)
	idle.track_insert_key(breathing, 1.2, Vector3(1, 1.025, 1))
	idle.track_insert_key(breathing, 2.4, Vector3.ONE)
	library.add_animation("Idle", idle)
	library.add_animation("Walk", _gait(0.85, 0.48, 0.30))
	library.add_animation("Run", _gait(0.55, 0.80, 0.65))
	animation_player.add_animation_library("", library)
	animation_player.play("Idle")

func _gait(duration: float, leg_swing: float, arm_swing: float) -> Animation:
	var clip := Animation.new()
	clip.length = duration
	clip.loop_mode = Animation.LOOP_LINEAR
	var joints := {"LeftLeg": leg_swing, "RightLeg": -leg_swing, "LeftArm": -arm_swing, "RightArm": arm_swing}
	for joint: String in joints:
		var track := clip.add_track(Animation.TYPE_VALUE)
		clip.track_set_path(track, NodePath(joint + ":rotation"))
		for sample in 9:
			var phase := float(sample) / 8.0
			clip.track_insert_key(track, duration * phase, Vector3(sin(phase * TAU) * joints[joint], 0, 0))
	var torso := clip.add_track(Animation.TYPE_VALUE)
	clip.track_set_path(torso, NodePath("Torso:scale"))
	clip.track_insert_key(torso, 0, Vector3.ONE)
	return clip

func update_movement(planar_speed: float, running: bool) -> void:
	var next := "Idle" if planar_speed < 0.1 else ("Run" if running else "Walk")
	if animation_player.current_animation != next:
		animation_player.play(next, 0.12)
