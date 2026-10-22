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
	var scroll: Node3D = world.get_node("ClueScroll")
	var tablet: Node3D = world.get_node("ClueTablet")
	var state: Node = world.get_node("GameState")
	await frames(8)
	check(scroll.has_node("Visual") and tablet.has_node("Visual"), "scroll and tablet instance actual GLB visuals")
	check(world.has_node("ScrollStand/Visual"), "scroll stand has independent visible support")
	check(tablet.has_node("Body"), "stone tablet has physical body")
	if not world.has_node("ScrollStand") or not tablet.has_node("Body"):
		quit(1)
		return
	if DisplayServer.get_name() != "headless":
		player.visible = false
		world.get_node("UI").visible = false
		var camera := Camera3D.new()
		world.add_child(camera)
		camera.current = true
		camera.fov = 45
		for shot in [["Scroll",Vector3(-3.1,1.6,6.3),Vector3(-4,.65,5)],["Tablet",Vector3(5.1,1.4,3.6),Vector3(4,.75,2)]]:
			camera.position = shot[1]
			camera.look_at(shot[2])
			await frames(6)
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://reports/screenshots/PROP_002_v002_"+shot[0]+".png")
	tablet.interact(player)
	check(tablet.visible and tablet.collected, "reading stone tablet retains its physical visual")
	check(not tablet.is_in_group("interactable"), "read tablet leaves interaction focus group")
	tablet.interact(player)
	check(state.clues.size() == 1, "repeat tablet read does not increase count")
	scroll.interact(player)
	check(not scroll.visible and state.clues.size() == 2, "scroll pickup hides scroll and records second unique clue")
	check(world.get_node("ScrollStand").visible, "pickup keeps wooden stand visible")
	var query := PhysicsRayQueryParameters3D.create(Vector3(-4,1.5,5),Vector3(-4,.1,5))
	var hit := world.get_world_3d().direct_space_state.intersect_ray(query)
	check(not hit.is_empty() and hit.collider == world.get_node("ScrollStand"), "visible stand retains matching physical collision")
	print("CLUE_PROPS_RESULT: ",failures," failures")
	quit(0 if failures == 0 else 1)
