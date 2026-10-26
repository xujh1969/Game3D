extends SceneTree

var failures := 0
var checks := 0

func _initialize() -> void:
	run.call_deferred()

func check(condition: bool, label: String) -> void:
	checks += 1
	print("PASS: " if condition else "FAIL: ", label)
	if not condition:
		failures += 1

func frames(count: int) -> void:
	for frame in count:
		await physics_frame
		await process_frame

func run() -> void:
	var world: Node3D = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	await frames(10)
	var look: Node3D = world.get_node("Atmosphere")
	var player: CharacterBody3D = world.get_node("Player")
	player.get_node("SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	check(look.get_meta("look_version") == "v001", "atmosphere initialized")
	if not look.has_node("Garden"):
		print("COURTYARD_LOOK_RESULT: required runtime look resources missing")
		quit(1)
		return
	check(look.get_node("Garden").find_children("*", "MeshInstance3D", true, false).size() == 7, "seven authored garden mesh groups")
	check(look.get_node("Garden").find_children("*", "CollisionObject3D", true, false).is_empty(), "vegetation mesh asset adds no imported physics")
	check(look.get_node("BenchCollision") is StaticBody3D and look.get_node("JarCollision") is StaticBody3D, "solid bench and jar have simplified collision outside the route")
	check(look.get_node("LayeredMountains").find_children("*", "MeshInstance3D", true, false).size() == 4, "four atmospheric background layers")
	check(not world.get_node("EnvironmentScenery/Mountains").visible, "old mountain version retained but hidden")
	var earth: MeshInstance3D = world.get_node("Architecture/Visual").find_child("Ground_Geometry", true, false)
	check(earth.get_active_material(0) is ShaderMaterial, "earth uses nonrepeating world-scale blend")
	var paving: MeshInstance3D = world.get_node("Architecture/Visual").find_child("Paving_Geometry", true, false)
	check(paving.get_active_material(0) is ShaderMaterial, "paving has per-stone variation")
	check(world.get_node("Environment").environment.fog_enabled, "depth and height fog enabled")
	check(not world.get_node("Environment").environment.volumetric_fog_enabled, "no unsupported Mobile volumetric fog")
	var camera: Camera3D = player.get_node("SpringArm3D/Camera3D")
	check(camera.attributes is CameraAttributesPractical and camera.attributes.dof_blur_far_distance >= 40, "far blur keeps playable court in focus")
	for label in ["PorchDust", "BambooDust", "IncenseSmoke"]:
		var particles: GPUParticles3D = look.get_node(label)
		check(particles.emitting and particles.amount <= 44 and particles.draw_pass_1.material.billboard_keep_scale, label + " is bounded and preserves small particle scale")
	check(not look.foot_dust.emitting, "stationary player raises no dust")
	player.position = Vector3(3, .1, 9)
	await frames(5)
	Input.action_press("move_forward")
	await frames(15)
	check(look.foot_dust.emitting, "walking on soil emits foot dust")
	Input.action_release("move_forward")
	player.position = Vector3(0, .1, 9)
	await frames(5)
	Input.action_press("move_forward")
	await frames(15)
	check(not look.foot_dust.emitting, "walking on paving emits no soil dust")
	Input.action_release("move_forward")
	check(world.get_node("ClueScroll").position == Vector3(-4,.5,5) and world.get_node("ClueTablet").position == Vector3(4,.5,2) and world.get_node("ClueIncense").position == Vector3(-5,.5,-4), "all three interaction locations preserved")
	print("COURTYARD_LOOK_RESULT: ", checks, " checks; ", failures, " failures")
	quit(0 if failures == 0 else 1)
