extends SceneTree

func _initialize() -> void:
	run.call_deferred()

func run() -> void:
	var world: Node3D = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	var player: CharacterBody3D = world.get_node("Player")
	player.get_node("SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	world.get_node("UI/DebugHUD").visible = false
	var camera := Camera3D.new()
	world.add_child(camera)
	camera.current = true
	camera.fov = 40
	for frame in 270:
		if frame == 60:
			Input.action_press("move_forward")
		if frame == 150:
			Input.action_press("run")
		if frame == 210:
			Input.action_release("move_forward")
			Input.action_release("run")
		camera.global_position = player.global_position + Vector3(2.2,1.35,-3)
		camera.look_at(player.global_position + Vector3.UP*.9)
		await process_frame
	print("QINGLAN_MOTION_CAPTURE: engine rendered 270 frames")
	quit()
