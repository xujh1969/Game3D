extends SceneTree

var failures := 0

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

func run() -> void:
	var world: Node = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	var door: Node3D = world.get_node("Door")
	world.get_node("Player/SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	var review_camera := Camera3D.new()
	world.add_child(review_camera)
	review_camera.position = Vector3(2.4, 2.05, -3.6)
	review_camera.look_at(Vector3(0, 1.3, -8))
	review_camera.fov = 45
	review_camera.current = true
	var left := door.get_node_or_null("LeftLeaf") as StaticBody3D
	var right := door.get_node_or_null("RightLeaf") as StaticBody3D
	check(left != null and right != null, "two separate physical door leaves exist")
	if left == null or right == null:
		quit(1)
		return
	check(left.find_child("LeafLeft", true, false) != null, "left visual is attached to left physical pivot")
	check(right.find_child("LeafRight", true, false) != null, "right visual is attached to right physical pivot")
	var fixed_frame: Node3D = door.get_node("Visual").find_child("DoorFrame", true, false)
	var frame_start := fixed_frame.global_transform
	var player: CharacterBody3D = world.get_node("Player")
	door.interact(player)
	await frames(3)
	check(is_zero_approx(left.rotation.y) and is_zero_approx(right.rotation.y), "locked leaves do not rotate")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://reports/screenshots/ARCH_003_DoorSong_v003_game_closed.png")
	for clue in ["ClueScroll", "ClueTablet", "ClueIncense"]:
		world.get_node(clue).interact(player)
	door.interact(player)
	door.interact(player)
	await frames(65)
	check(is_equal_approx(left.rotation.y, PI / 2) and is_equal_approx(right.rotation.y, -PI / 2), "two leaves open inward at opposite 90 degree angles")
	check(fixed_frame.global_transform.is_equal_approx(frame_start), "door frame stays fixed")
	check(not left.get_node("CollisionShape3D").disabled and not right.get_node("CollisionShape3D").disabled, "both open leaves retain collision")
	check(door.is_open and not door.is_opening, "animation completion updates opening state")
	if DisplayServer.get_name() != "headless":
		await frames(3)
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://reports/screenshots/ARCH_003_DoorSong_v003_game_open.png")
	print("DOUBLE_DOOR_RESULT: ", failures, " failures")
	quit(0 if failures == 0 else 1)
