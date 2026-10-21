extends SceneTree

var failures: Array[String] = []

func _initialize() -> void:
	_run.call_deferred()

func check(condition: bool, description: String) -> void:
	print(("PASS: " if condition else "FAIL: ") + description)
	if not condition:
		failures.append(description)

func frames(count: int) -> void:
	for index in count:
		await physics_frame
		await process_frame

func capture(filename: String) -> void:
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://reports/screenshots/" + filename + ".png")

func _run() -> void:
	var world: Node = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	var player: CharacterBody3D = world.get_node("Player")
	var state: Node = world.get_node("GameState")
	var door: Node = world.get_node("Door")
	var hud: Node = world.get_node("UI")
	var wins := [0]
	state.game_won.connect(func(): wins[0] += 1)
	await frames(12)
	await capture("M1_Entrance_TEMP")
	check(player.is_on_floor(), "player settles on floor")
	var start := player.position
	Input.action_press("move_forward")
	await frames(20)
	Input.action_release("move_forward")
	check(player.position.z < start.z - 0.5, "W moves toward camera forward (-Z)")
	player.rotation.y = 0
	player.get_node("SpringArm3D").rotation.y = 0
	var camera: Camera3D = player.get_node("SpringArm3D/Camera3D")
	var camera_start := camera.global_basis.z
	Input.action_press("move_right")
	await frames(20)
	Input.action_release("move_right")
	check(camera.global_basis.z.dot(camera_start) > 0.99, "character turning does not rotate camera")
	world.get_node("Finish")._on_body_entered(player)
	check(wins[0] == 0, "finish refuses player before door opens")
	door.interact(player)
	check(not door.is_open, "door stays locked before three clues")
	player.position = Vector3(-2.2, 0, -7.2)
	player.get_node("Proxy").rotation.y = 0
	player._update_focus()
	check(player.focus != door, "wall blocks interaction focus")
	player.position = Vector3(0, 0, -6.7)
	var arm: SpringArm3D = player.get_node("SpringArm3D")
	arm.rotation.y = PI
	await frames(5)
	print("CAMERA_PROBE: hit=", arm.get_hit_length(), " camera=", camera.global_position, " player=", player.global_position)
	check(arm.get_hit_length() < 2.0 and camera.global_position.z > -7.925, "camera retracts before closed door")
	arm.rotation.y = 0
	player.position = Vector3(0, 0, -6)
	player.velocity = Vector3.ZERO
	player.get_node("SpringArm3D").rotation.y = 0
	Input.action_press("move_forward")
	await frames(40)
	Input.action_release("move_forward")
	check(player.position.z > -7.7, "closed door physically blocks passage")
	player.position = Vector3(-4, 0, 6.5)
	player.rotation.y = 0
	player.get_node("Proxy").rotation.y = 0
	player.velocity = Vector3.ZERO
	await frames(2)
	var first: Node = world.get_node("ClueScroll")
	Input.action_press("interact")
	await frames(2)
	Input.action_release("interact")
	check(state.clues.size() == 1, "E input collects focused clue")
	player._update_focus()
	check(player.focus != first, "collected clue cannot retain interaction focus")
	first.interact(player)
	check(state.clues.size() == 1, "repeat clue interaction does not increase count")
	world.get_node("ClueTablet").interact(player)
	world.get_node("ClueIncense").interact(player)
	check(door.unlocked and state.clues.size() == 3, "three clues unlock door")
	check(hud.label.text.begins_with("线索：3/3"), "HUD shows three clues")
	await capture("M1_Three_Clues_TEMP")
	door.interact(player)
	await frames(1)
	check(not door.is_open, "door is not marked open before animation completes")
	check(not door.get_node("CollisionShape3D").disabled, "opening door retains physical collision")
	await frames(60)
	check(door.is_open, "door opens after animation")
	player.position = Vector3(0, 0, -6)
	player.velocity = Vector3.ZERO
	Input.action_press("move_forward")
	await frames(110)
	Input.action_release("move_forward")
	check(player.position.z < -8.5, "player physically passes through opened doorway")
	world.get_node("Finish")._on_body_entered(player)
	world.get_node("Finish")._on_body_entered(player)
	check(state.won and wins[0] == 1, "victory is recorded exactly once after opening")
	check(hud.pause_panel.visible, "victory displays restart and exit menu")
	await capture("M1_Victory_TEMP")
	paused = false
	state.restart()
	await frames(3)
	check(current_scene.get_node("GameState").clues.is_empty(), "restart clears clues")
	check(not current_scene.get_node("Door").is_open, "restart restores locked door")
	var new_hud: Node = current_scene.get_node("UI")
	new_hud._toggle_pause()
	check(paused and new_hud.pause_panel.visible, "pause displays menu and stops game")
	await capture("M1_Pause_TEMP")
	new_hud._toggle_pause()
	check(not paused and not new_hud.pause_panel.visible, "resume returns to game")
	var new_player: CharacterBody3D = current_scene.get_node("Player")
	new_player.position = Vector3(0, 0, 14.4)
	new_player.velocity = Vector3.ZERO
	Input.action_press("move_back")
	await frames(20)
	Input.action_release("move_back")
	check(new_player.position.z < 14.8 and new_player.position.y > -0.1, "courtyard boundary prevents falling out")
	print("M1_RESULT: %d failures" % failures.size())
	quit(0 if failures.is_empty() else 1)
