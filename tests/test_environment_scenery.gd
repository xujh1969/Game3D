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
	check(world.has_node("EnvironmentScenery"), "world instances bamboo and mountain scenery")
	if not world.has_node("EnvironmentScenery"):
		quit(1)
		return
	var scenery: Node3D = world.get_node("EnvironmentScenery")
	var stems := 0
	for child in scenery.get_children():
		if child is StaticBody3D:
			for shape in child.get_children():
				if shape is CollisionShape3D:
					stems += 1
	check(stems == 24, "four clumps provide 24 narrow stem colliders")
	var opaque := true
	var surface_count := 0
	for mesh_node in scenery.get_node("BambooWest/Visual").find_children("*", "MeshInstance3D", true, false):
		for index in mesh_node.mesh.get_surface_count():
			surface_count += 1
			var mat: Material = mesh_node.mesh.surface_get_material(index)
			opaque = opaque and mat is BaseMaterial3D and mat.transparency == BaseMaterial3D.TRANSPARENCY_DISABLED
	check(opaque and surface_count > 0, "bamboo has rendered surfaces using opaque geometry materials")
	check(scenery.get_node("Mountains").find_children("*", "CollisionObject3D", true, false).is_empty(), "distant mountains do not add playable terrain or collision")
	var environment: Environment = world.get_node("Environment").environment
	check(environment.fog_enabled and not environment.volumetric_fog_enabled, "regular fog enabled without Forward+ volumetrics")
	var player: CharacterBody3D = world.get_node("Player")
	player.get_node("SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	await frames(8)
	var bamboo: Node3D = scenery.get_node("BambooWest")
	var stem_position: Vector3 = bamboo.get_node("Stem0").global_position
	var query := PhysicsRayQueryParameters3D.create(stem_position + Vector3(0,0,1), stem_position - Vector3(0,0,1))
	var hit := world.get_world_3d().direct_space_state.intersect_ray(query)
	check(not hit.is_empty() and hit.collider == bamboo, "stem is included in scene physics queries")
	if DisplayServer.get_name() != "headless":
		player.visible = false
		world.get_node("UI").visible = false
		var camera := Camera3D.new()
		world.add_child(camera)
		camera.current = true
		camera.fov = 60
		for shot in [["Entrance",Vector3(0,1.6,12),Vector3(0,2.2,-8)],["Hero",Vector3(8,3.2,3),Vector3(0,2.2,-8)],["Bamboo",Vector3(-7,2.8,9),Vector3(-11,2.2,5)]]:
			camera.position = shot[1]
			camera.look_at(shot[2])
			await frames(6)
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://reports/screenshots/ENV_Landscape_v002_" + shot[0] + ".png")
	print("ENVIRONMENT_RESULT: ",failures," failures")
	quit(0 if failures == 0 else 1)
