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

func capture(name: String, player: Node3D, camera: Camera3D) -> void:
	if DisplayServer.get_name() == "headless":
		return
	camera.global_position = player.global_position + Vector3(2.2, 1.6, 2.8)
	camera.look_at(player.global_position + Vector3.UP * 0.9)
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://reports/screenshots/TEMP_Proxy_" + name + "_v001.png")

func run() -> void:
	var world: Node = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	var spawn: Transform3D = world.get_node("Player").transform
	world.get_node("Player").free()
	var temporary: Node3D = load("res://scenes/character/Qinglan_TEMP.tscn").instantiate()
	temporary.transform = spawn
	world.add_child(temporary)
	root.add_child(world)
	current_scene = world
	var player: CharacterBody3D = world.get_node("Player")
	player.get_node("SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	var animation: AnimationPlayer = player.get_node_or_null("Proxy/AnimationPlayer")
	check(animation != null, "TEMP proxy provides an AnimationPlayer")
	if animation == null:
		quit(1)
		return
	var camera := Camera3D.new()
	world.add_child(camera)
	camera.current = true
	camera.fov = 50
	await frames(8)
	check(animation.has_animation("Idle") and animation.has_animation("Walk") and animation.has_animation("Run"), "three named TEMP motion clips exist")
	check(animation.current_animation == "Idle", "stationary character plays Idle")
	await capture("Idle", player, camera)
	Input.action_press("move_forward")
	await frames(12)
	check(animation.current_animation == "Walk", "W movement plays Walk")
	var leg: Node3D = player.get_node("Proxy/LeftLeg")
	var before := leg.rotation.x
	await frames(8)
	check(absf(leg.rotation.x - before) > 0.05, "limb pose changes over time")
	await capture("Walk", player, camera)
	var walk_velocity := Vector2(player.velocity.x, player.velocity.z).length()
	Input.action_press("run")
	await frames(12)
	check(animation.current_animation == "Run", "Shift movement plays Run")
	check(Vector2(player.velocity.x, player.velocity.z).length() > walk_velocity, "sprint moves faster than walking")
	await capture("Run", player, camera)
	paused = true
	var paused_time := animation.current_animation_position
	await frames(6)
	check(is_equal_approx(animation.current_animation_position, paused_time), "pause freezes the motion clip")
	paused = false
	Input.action_release("move_forward")
	Input.action_release("run")
	await frames(15)
	check(animation.current_animation == "Idle", "release movement returns to Idle")
	check(player.is_on_floor(), "motion clips preserve player floor contact")
	print("PROXY_ANIMATION_RESULT: ", failures, " failures")
	quit(0 if failures == 0 else 1)
