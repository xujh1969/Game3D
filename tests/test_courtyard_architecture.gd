extends SceneTree

var failures := 0
var player: CharacterBody3D
var world: Node3D
var capture_prefix := "ARCH_Courtyard_v003"

func _initialize() -> void:
	run.call_deferred()

func check(ok: bool, description: String) -> void:
	print(("PASS: " if ok else "FAIL: ") + description)
	if not ok:
		failures += 1

func frames(count: int) -> void:
	for index in count:
		await physics_frame
		await process_frame

func run() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture-prefix="):
			capture_prefix = argument.trim_prefix("--capture-prefix=")
	world = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	player = world.get_node("Player")
	player.get_node("SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	check(world.has_node("Architecture/Visual"), "runtime world instances the production architecture")
	if not world.has_node("Architecture/Visual"):
		quit(1)
		return
	check(is_equal_approx(world.get_node("Door").position.y, .3), "door threshold matches 0.3m platform")
	player.position = Vector3(0, .02, -3.8)
	player.velocity = Vector3.ZERO
	await frames(8)
	Input.action_press("move_forward")
	await frames(48)
	Input.action_release("move_forward")
	await frames(5)
	check(player.position.z < -6.0 and player.position.y > .28 and player.is_on_floor(), "walks up real physics ramp onto visible stone steps")
	Input.action_press("move_back")
	await frames(48)
	Input.action_release("move_back")
	await frames(8)
	check(player.position.z > -4.4 and absf(player.position.y) < .05 and player.is_on_floor(), "walks down to courtyard without falling or sticking")
	player.position = Vector3(7,0,-6.8)
	player.velocity = Vector3.ZERO
	Input.action_press("move_forward")
	await frames(40)
	Input.action_release("move_forward")
	check(player.position.z > -7.6, "cross wall prevents bypassing locked door at building side")
	var query := PhysicsRayQueryParameters3D.create(Vector3(0,6,-7), Vector3(0,2,-7))
	var hit := world.get_world_3d().direct_space_state.intersect_ray(query)
	check(not hit.is_empty() and hit.collider == world.get_node("Architecture/Collision"), "roof is included in camera obstruction physics")
	check(world.has_node("Nature/RockWest/Visual") and world.has_node("Nature/RockEast/Visual") and world.has_node("Nature/RockNorthwest/Visual"), "three prepared moss-rock variants are instantiated")
	var rock_query := PhysicsRayQueryParameters3D.create(Vector3(-8,2,0), Vector3(-8,-.2,0))
	var rock_hit := world.get_world_3d().direct_space_state.intersect_ray(rock_query)
	check(not rock_hit.is_empty() and rock_hit.collider == world.get_node("Nature/RockWest"), "rock has physical collision distinct from ground")
	if DisplayServer.get_name() != "headless":
		player.visible = false
		world.get_node("UI").visible = false
		var camera := Camera3D.new()
		world.add_child(camera)
		camera.current = true
		camera.fov = 60
		for shot in [["Entrance", Vector3(0,1.6,12), Vector3(0,2,-8)], ["Hero",Vector3(8,3.2,3),Vector3(0,2,-8)], ["Porch",Vector3(3.1,2.2,-4.5),Vector3(0,1.9,-8)], ["Ground",Vector3(2,1.2,6),Vector3(0,.05,4)]]:
			camera.position = shot[1]
			camera.look_at(shot[2])
			await frames(5)
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://reports/screenshots/" + capture_prefix + "_" + shot[0] + ".png")
	print("COURTYARD_RESULT: ", failures, " failures")
	quit(0 if failures == 0 else 1)
