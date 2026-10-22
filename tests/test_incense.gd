extends SceneTree

var failures := 0

func _initialize() -> void:
	run.call_deferred()

func check(ok: bool, message: String) -> void:
	print(("PASS: " if ok else "FAIL: ") + message)
	if not ok:
		failures += 1

func frames(count: int) -> void:
	for index in count:
		await physics_frame
		await process_frame

func run() -> void:
	var world: Node3D = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	var player: CharacterBody3D = world.get_node("Player")
	player.get_node("SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	var incense: Node3D = world.get_node("ClueIncense")
	check(incense.has_node("Visual") and incense.has_node("Body"), "incense instances actual asset and physical body")
	if not incense.has_node("Body"):
		quit(1)
		return
	await frames(8)
	player.position = Vector3(-5,0,-2.6)
	player.velocity = Vector3.ZERO
	player.get_node("Proxy").rotation.y = 0
	await frames(8)
	player._update_focus()
	check(player.focus == incense, "approach can focus incense through its own physical body")
	if DisplayServer.get_name() != "headless":
		player.visible = false
		world.get_node("UI").visible = false
		var camera := Camera3D.new()
		world.add_child(camera)
		camera.current = true
		camera.fov = 40
		for shot in [["Front",Vector3(-4.45,.60,-3.1),Vector3(-5,.18,-4)],["Interior",Vector3(-4.5,1.0,-3.4),Vector3(-5,.19,-4)]]:
			camera.position = shot[1]
			camera.look_at(shot[2])
			await frames(6)
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://reports/screenshots/PROP_001_v002_"+shot[0]+".png")
	incense.interact(player)
	var state: Node = world.get_node("GameState")
	check(incense.visible and incense.collected, "activated incense stays visible")
	check(not incense.is_in_group("interactable"), "activated incense leaves focus group")
	incense.interact(player)
	check(state.clues.size() == 1, "incense clue records once")
	var query := PhysicsRayQueryParameters3D.create(Vector3(-5,1,-4),Vector3(-5,-.1,-4))
	var hit := world.get_world_3d().direct_space_state.intersect_ray(query)
	check(not hit.is_empty() and hit.collider == incense.get_node("Body"), "visible incense retains physical collision")
	print("INCENSE_RESULT: ",failures," failures")
	quit(0 if failures == 0 else 1)
