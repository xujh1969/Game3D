extends SceneTree

var failures := 0
var capture_prefix := "Qinglan_Playable_v006"

func _initialize() -> void:
	run.call_deferred()

func check(condition: bool, description: String) -> void:
	print(("PASS: " if condition else "FAIL: ") + description)
	if not condition:
		failures += 1

func frames(count: int) -> void:
	for index in count:
		await physics_frame
		await process_frame

func capture(name: String) -> void:
	if DisplayServer.get_name() != "headless":
		var debug_hud: Label = current_scene.get_node("UI/DebugHUD")
		var was_visible := debug_hud.visible
		debug_hud.visible = false
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://reports/screenshots/" + capture_prefix + "_" + name + ".png")
		debug_hud.visible = was_visible

func audit_motion(skeleton: Skeleton3D, animation: AnimationPlayer) -> void:
	var gap := 0.0
	var changes := {}
	for clip in ["Idle", "Walk", "Run"]:
		if not animation.has_animation(clip):
			continue
		animation.play(clip)
		var length := animation.get_animation(clip).length
		var first := {}
		var maximum := {"LeftLeg": 0.0, "LeftForeArm": 0.0, "Head": 0.0, "Spine2": 0.0}
		for sample in 33:
			animation.seek(length * float(sample) / 33.0, true)
			animation.advance(0)
			for side in ["Left", "Right"]:
				for pair in [["UpLeg", "Leg"], ["Leg", "Foot"], ["Arm", "ForeArm"], ["ForeArm", "Hand"]]:
					var parent := bone_index(skeleton, side + pair[0])
					var child := bone_index(skeleton, side + pair[1])
					var expected := skeleton.get_bone_global_pose(parent) * skeleton.get_bone_rest(child).origin
					gap = maxf(gap, expected.distance_to(skeleton.get_bone_global_pose(child).origin))
			for name: String in maximum:
				var pose := skeleton.get_bone_pose_rotation(bone_index(skeleton, name))
				if sample == 0:
					first[name] = pose
				maximum[name] = maxf(maximum[name], first[name].angle_to(pose))
		changes[clip] = maximum
	check(gap < .002, "user knees ankles elbows and wrists stay connected across three clips")
	check(changes["Walk"]["LeftLeg"] > .18 and changes["Run"]["LeftLeg"] > .18, "user knees flex in walk and run")
	check(changes["Walk"]["LeftForeArm"] > .04, "user elbow moves through walking cycle")
	check(changes["Idle"]["Head"] > .001 or changes["Idle"]["Spine2"] > .001, "user Idle retains living upper-body movement")
	var file := FileAccess.open("res://reports/validation/" + capture_prefix + "_Motion.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"maximum_joint_gap_m": gap, "bone_rotation_changes_rad": changes}, "\t") + "\n")
	animation.play("Idle")
	animation.seek(0, true)

func bone_index(skeleton: Skeleton3D, suffix: String) -> int:
	for index in skeleton.get_bone_count():
		if skeleton.get_bone_name(index).ends_with(suffix):
			return index
	return -1

func run() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture-prefix="):
			capture_prefix = argument.trim_prefix("--capture-prefix=")
	var world: Node3D = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	var player: CharacterBody3D = world.get_node("Player")
	var visual: Node3D = player.get_node("Proxy")
	var skeleton := visual.find_child("Skeleton3D", true, false) as Skeleton3D
	var animation := visual.find_child("AnimationPlayer", true, false) as AnimationPlayer
	check(skeleton != null, "world player uses the Qinglan skeletal model")
	check(not player.has_node("TEMPLabel"), "world no longer displays the geometric TEMP label")
	if skeleton == null or animation == null:
		print("QINGLAN_PLAYABLE_RESULT: ", failures, " failures")
		quit(1)
		return
	check(skeleton.get_bone_count() >= 20, "experimental humanoid skeleton is present")
	check(skeleton.get_bone_count() == 41, "user's 41-bone skeleton is retained")
	check(animation.has_animation("Idle") and animation.has_animation("Walk") and animation.has_animation("Run"), "three imported bone animation clips exist")
	audit_motion(skeleton, animation)
	var mesh := visual.find_child("Qinglan_Mesh", true, false) as MeshInstance3D
	check(mesh != null and mesh.skin != null, "Qinglan mesh uses skin bindings")
	player.get_node("SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	await frames(10)
	check(animation.current_animation == "Idle", "stationary Qinglan plays Idle")
	check(player.is_on_floor(), "character physics rests on courtyard ground")
	await capture("PlayerCamera")
	var camera := Camera3D.new()
	world.add_child(camera)
	camera.current = true
	camera.fov = 40
	camera.global_position = player.global_position + Vector3(2, 1.5, -3)
	camera.look_at(player.global_position + Vector3.UP * .9)
	await capture("Idle")
	Input.action_press("move_forward")
	await frames(12)
	check(animation.current_animation == "Walk", "W movement plays skeletal Walk")
	var thigh := bone_index(skeleton, "LeftUpLeg")
	var before := skeleton.get_bone_pose_rotation(thigh)
	var maximum_change := 0.0
	for sample in 8:
		await frames(1)
		maximum_change = maxf(maximum_change, before.angle_to(skeleton.get_bone_pose_rotation(thigh)))
	check(maximum_change > .03, "leg bone pose changes over sampled interval")
	camera.global_position = player.global_position + Vector3(2, 1.5, -3)
	camera.look_at(player.global_position + Vector3.UP * .9)
	await capture("Walk")
	var walk_speed := player.velocity.length()
	Input.action_press("run")
	await frames(12)
	check(animation.current_animation == "Run", "Shift movement plays skeletal Run")
	check(player.velocity.length() > walk_speed, "existing sprint remains faster than walk")
	camera.global_position = player.global_position + Vector3(2, 1.5, -3)
	camera.look_at(player.global_position + Vector3.UP * .9)
	await capture("Run")
	paused = true
	var paused_time := animation.current_animation_position
	await frames(6)
	check(is_equal_approx(paused_time, animation.current_animation_position), "pause freezes skeletal animation")
	paused = false
	Input.action_release("move_forward")
	Input.action_release("run")
	await frames(15)
	check(animation.current_animation == "Idle", "release movement returns to Idle")
	check(player.is_on_floor(), "animation does not move the physics capsule off ground")
	check(is_equal_approx(visual.get_node("Model").rotation.y, PI), "model facing is corrected to controller minus Z")
	await frames(120)
	check(animation.current_animation == "Idle", "user Idle continues looping while stationary")
	await capture("Idle_Loop")
	print("QINGLAN_PLAYABLE_RESULT: ", failures, " failures")
	quit(0 if failures == 0 else 1)
