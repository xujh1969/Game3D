extends SceneTree

var world: Node
var player: CharacterBody3D
var state: Node
var failed := false

func _initialize() -> void:
	run.call_deferred()

func frames(count: int) -> void:
	for index in count:
		await physics_frame
		await process_frame

func release_movement() -> void:
	for action in ["move_left", "move_right", "move_forward", "move_back"]:
		Input.action_release(action)

func walk_to(target: Vector2) -> void:
	for frame in 600:
		var offset := target - Vector2(player.position.x, player.position.z)
		if offset.length() < 0.15 or state.won:
			release_movement()
			return
		var direction := offset.normalized()
		release_movement()
		Input.action_press("move_right" if direction.x > 0 else "move_left", absf(direction.x))
		Input.action_press("move_back" if direction.y > 0 else "move_forward", absf(direction.y))
		await frames(1)
	failed = true
	release_movement()
	push_error("Route blocked at " + str(player.position) + " toward " + str(target))
	quit(1)

func interact() -> void:
	await frames(8)
	Input.action_press("interact")
	await frames(2)
	Input.action_release("interact")

func run() -> void:
	world = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	player = world.get_node("Player")
	state = world.get_node("GameState")
	# Prevent OS mouse motion from changing the deterministic route's camera basis.
	player.get_node("SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	await frames(10)
	# All travel uses the real CharacterBody3D controller; there are no teleports.
	for approach in [Vector2(-4, 8), Vector2(-4, 6.4)]:
		await walk_to(approach)
	await interact()
	print("ROUTE: scroll, count=", state.clues.size())
	for approach in [Vector2(4, 5.5), Vector2(4, 3.4)]:
		await walk_to(approach)
	await interact()
	print("ROUTE: tablet, count=", state.clues.size())
	for approach in [Vector2(-5, 0), Vector2(-5, -2.6)]:
		await walk_to(approach)
	await interact()
	print("ROUTE: incense, count=", state.clues.size())
	for approach in [Vector2(0, -4), Vector2(0, -6.4)]:
		await walk_to(approach)
	await interact()
	await frames(60)
	await walk_to(Vector2(0, -13))
	var passed: bool = not failed and state.clues.size() == 3 and state.won and world.get_node("Door").is_open
	print("PLAYTHROUGH_RESULT: ", "PASS" if passed else "FAIL", " position=", player.position)
	if DisplayServer.get_name() != "headless":
		var capture_name := "M1_Playthrough_Victory_TEMP"
		for argument in OS.get_cmdline_user_args():
			if argument.begins_with("--capture-name="):
				capture_name = argument.trim_prefix("--capture-name=")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://reports/screenshots/" + capture_name + ".png")
	quit(0 if passed else 1)
