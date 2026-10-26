extends SceneTree

func _initialize() -> void:
	run.call_deferred()

func run() -> void:
	var phase := "Before"
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--phase="):
			phase = argument.trim_prefix("--phase=")
	var world: Node3D = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	world.get_node("Player/SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	world.get_node("UI").hide()
	var camera := Camera3D.new()
	world.add_child(camera)
	camera.current = true
	camera.fov = 58
	var shots := [
		["Entrance", Vector3(0, 2.0, 13.8), Vector3(0, 1.65, -6)],
		["Hero", Vector3(8, 3.0, 9), Vector3(-1, 1.3, -6)],
		["Ground", Vector3(3.0, 1.1, 6), Vector3(0, 0.1, 3)],
		["Incense", Vector3(-2.7, 1.2, -1), Vector3(-5, 0.65, -4)],
		["Porch", Vector3(3.5, 1.7, -3), Vector3(0, 1.7, -8)]
	]
	for shot in shots:
		camera.position = shot[1]
		camera.look_at(shot[2])
		for frame in 90:
			await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://reports/screenshots/Courtyard_Look_v001_" + phase + "_" + shot[0] + ".png")
		print("LOOK_CAPTURE: ", phase, " ", shot[0])
	quit()
