extends Node3D

const EARTH = preload("res://assets/game/courtyard_earth_v001.gdshader")
const STONE = preload("res://assets/game/courtyard_stone_v001.gdshader")
const FOLIAGE = preload("res://assets/game/courtyard_foliage_v001.gdshader")
const RIDGE_SURFACE = preload("res://assets/game/courtyard_ridge_v001.gdshader")
const GARDEN = preload("res://assets/game/ENV_CourtyardGarden_v003_game.glb")
const RIDGES = preload("res://assets/game/ENV_DistantMountains_v004_game.glb")
const BAMBOO = preload("res://assets/game/NAT_002_BambooClump_v002_game.glb")

var foot_dust: GPUParticles3D
var player: CharacterBody3D

func _ready() -> void:
	var world := get_parent()
	_apply_surfaces(world.get_node("Architecture/Visual"))
	var garden := GARDEN.instantiate()
	garden.name = "Garden"
	add_child(garden)
	_apply_leaves(garden, true)
	var bench_shape := BoxShape3D.new()
	bench_shape.size = Vector3(1.15, .43, .37)
	_add_prop_collision("BenchCollision", Vector3(-5.8, .21, 5.61), bench_shape)
	var jar_shape := CylinderShape3D.new()
	jar_shape.radius = .24
	jar_shape.height = .55
	_add_prop_collision("JarCollision", Vector3(-5.35, .275, 4.45), jar_shape)
	_apply_leaves(world.get_node("EnvironmentScenery"), false)
	var grove := Node3D.new()
	grove.name = "OuterBamboo"
	add_child(grove)
	var locations := [Vector3(-16.5,0,7), Vector3(16.5,0,8), Vector3(-16.5,0,-2), Vector3(16.5,0,-3), Vector3(-9,0,-17), Vector3(8,0,-17)]
	for index in locations.size():
		var clump := BAMBOO.instantiate()
		clump.position = locations[index]
		clump.rotation.y = index * 1.73
		clump.scale = Vector3.ONE * (1.18 + .10 * (index % 3))
		grove.add_child(clump)
	_apply_leaves(grove, false)
	world.get_node("EnvironmentScenery/Mountains").hide()
	var ridges := RIDGES.instantiate()
	ridges.name = "LayeredMountains"
	add_child(ridges)
	var ridge_colors := [Color(.32,.40,.36), Color(.39,.46,.44), Color(.46,.52,.52), Color(.54,.59,.61)]
	var layer := 0
	for mesh in ridges.find_children("*", "MeshInstance3D", true, false):
		var material := ShaderMaterial.new()
		material.shader = RIDGE_SURFACE
		material.set_shader_parameter("tint", ridge_colors[layer])
		mesh.material_override = material
		layer += 1
	var environment: Environment = world.get_node("Environment").environment.duplicate()
	world.get_node("Environment").environment = environment
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	environment.ambient_light_energy = .48
	environment.reflected_light_source = Environment.REFLECTION_SOURCE_SKY
	environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	environment.fog_light_color = Color(.66, .73, .75)
	environment.fog_light_energy = .85
	environment.fog_density = .0057
	environment.fog_height = .1
	environment.fog_height_density = .015
	environment.fog_sky_affect = .18
	var sun: DirectionalLight3D = world.get_node("MorningLight")
	sun.rotation = Vector3(-.46, -1.22, 0)
	sun.light_color = Color(1, .88, .71)
	sun.light_energy = 1.5
	sun.light_angular_distance = .7
	sun.shadow_bias = .035
	sun.directional_shadow_max_distance = 48
	# Broad low-energy fill represents sky/bounce under the porch; this is not baked GI.
	var fill := OmniLight3D.new()
	fill.name = "PorchBounce"
	fill.position = Vector3(0, 2.4, -6.5)
	fill.light_color = Color(.70, .77, .86)
	fill.light_energy = .26
	fill.omni_range = 8
	fill.shadow_enabled = false
	add_child(fill)
	var camera: Camera3D = world.get_node("Player/SpringArm3D/Camera3D")
	var attributes := CameraAttributesPractical.new()
	attributes.dof_blur_far_enabled = true
	attributes.dof_blur_far_distance = 46
	attributes.dof_blur_far_transition = 65
	attributes.dof_blur_amount = .055
	camera.attributes = attributes
	world.get_node("Environment").camera_attributes = attributes
	_particles("PorchDust", Vector3(1, 1.8, -5), Vector3(4.5, 1.5, 1.0), false)
	_particles("BambooDust", Vector3(-10, 1.4, 5), Vector3(1.5, 1.2, 1.5), false)
	_particles("IncenseSmoke", Vector3(-5, .36, -4), Vector3(.025, .01, .025), true)
	player = world.get_node("Player")
	foot_dust = _particles("FootDust", Vector3.ZERO, Vector3(.09, .015, .09), false)
	foot_dust.amount = 12
	foot_dust.lifetime = .65
	foot_dust.preprocess = 0
	foot_dust.local_coords = false
	foot_dust.emitting = false
	var foot_process: ParticleProcessMaterial = foot_dust.process_material.duplicate()
	foot_dust.process_material = foot_process
	foot_process.direction = Vector3.UP
	foot_process.initial_velocity_min = .07
	foot_process.initial_velocity_max = .18
	foot_process.gravity = Vector3(.03, -.10, 0)
	foot_process.scale_min = .035
	foot_process.scale_max = .07
	var foot_fade := Gradient.new()
	foot_fade.offsets = PackedFloat32Array([0, .2, 1])
	foot_fade.colors = PackedColorArray([Color(.42,.34,.23,0), Color(.42,.34,.23,.16), Color(.42,.34,.23,0)])
	var foot_ramp := GradientTexture1D.new()
	foot_ramp.gradient = foot_fade
	foot_process.color_ramp = foot_ramp
	set_meta("look_version", "v001")

func _process(_delta: float) -> void:
	foot_dust.global_position = player.global_position + Vector3(0, .045, 0)
	var on_earth := absf(player.global_position.x) > 1.85 and player.global_position.z > -5.1
	foot_dust.emitting = on_earth and player.is_on_floor() and Vector2(player.velocity.x, player.velocity.z).length() > .6

func _add_prop_collision(label: String, center: Vector3, shape: Shape3D) -> void:
	var body := StaticBody3D.new()
	body.name = label
	body.position = center
	var collision := CollisionShape3D.new()
	collision.shape = shape
	body.add_child(collision)
	add_child(body)

func _apply_surfaces(node: Node) -> void:
	if node is MeshInstance3D:
		for surface in node.mesh.get_surface_count():
			var original: Material = node.get_active_material(surface)
			if not original is StandardMaterial3D:
				continue
			if original.resource_name.contains("brown_mud"):
				var material := ShaderMaterial.new()
				material.shader = EARTH
				material.set_shader_parameter("earth_color", original.albedo_texture)
				material.set_shader_parameter("earth_normal", original.normal_texture)
				material.set_shader_parameter("earth_roughness", original.roughness_texture)
				node.set_surface_override_material(surface, material)
			elif node.name == "Paving_Geometry":
				var material := ShaderMaterial.new()
				material.shader = STONE
				material.set_shader_parameter("stone_color", original.albedo_texture)
				material.set_shader_parameter("stone_normal", original.normal_texture)
				node.set_surface_override_material(surface, material)
	for child in node.get_children():
		_apply_surfaces(child)

func _apply_leaves(node: Node, garden: bool) -> void:
	if node is MeshInstance3D:
		for surface in node.mesh.get_surface_count():
			var original: Material = node.get_active_material(surface)
			if original is StandardMaterial3D and ((garden and (node.name.contains("Grass") or node.name.contains("Fern") or node.name.contains("Shrub"))) or original.resource_name.contains("Bamboo_Leaf")):
				var material := ShaderMaterial.new()
				material.shader = FOLIAGE
				material.set_shader_parameter("tint", original.albedo_color)
				material.set_shader_parameter("wind_strength", .025 if garden else .045)
				node.set_surface_override_material(surface, material)
	for child in node.get_children():
		_apply_leaves(child, garden)

func _particles(label: String, center: Vector3, extent: Vector3, smoke: bool) -> GPUParticles3D:
	var particles := GPUParticles3D.new()
	particles.name = label
	particles.position = center
	particles.amount = 22 if smoke else 44
	particles.lifetime = 5.5 if smoke else 9
	particles.preprocess = 5.5 if smoke else 9
	particles.fixed_fps = 30
	particles.visibility_aabb = AABB(-extent - Vector3.ONE, extent * 2 + Vector3(2, 4, 2))
	var process := ParticleProcessMaterial.new()
	process.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	process.emission_box_extents = extent
	process.direction = Vector3.UP if smoke else Vector3(1, .2, -.3)
	process.spread = 14 if smoke else 60
	process.initial_velocity_min = .09 if smoke else .015
	process.initial_velocity_max = .17 if smoke else .04
	process.gravity = Vector3(.007, .012, 0) if smoke else Vector3(.002, -.001, .001)
	process.scale_min = .09 if smoke else .009
	process.scale_max = .23 if smoke else .019
	var fade := Gradient.new()
	fade.offsets = PackedFloat32Array([0, .16, .65, 1])
	var tint := Color(.66, .69, .67, .13) if smoke else Color(.92, .83, .61, .38)
	fade.colors = PackedColorArray([Color(tint, 0), tint, Color(tint, tint.a*.5), Color(tint, 0)])
	var ramp := GradientTexture1D.new()
	ramp.gradient = fade
	process.color_ramp = ramp
	particles.process_material = process
	var radial := Gradient.new()
	radial.offsets = PackedFloat32Array([0, .25, 1])
	radial.colors = PackedColorArray([Color.WHITE, Color(1, 1, 1, .6), Color(1, 1, 1, 0)])
	var texture := GradientTexture2D.new()
	texture.gradient = radial
	texture.width = 32
	texture.height = 32
	texture.fill = GradientTexture2D.FILL_RADIAL
	texture.fill_from = Vector2(.5, .5)
	texture.fill_to = Vector2(1, .5)
	var material := StandardMaterial3D.new()
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
	material.billboard_keep_scale = true
	material.vertex_color_use_as_albedo = true
	material.albedo_texture = texture
	var quad := QuadMesh.new()
	quad.size = Vector2.ONE
	quad.material = material
	particles.draw_pass_1 = quad
	particles.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(particles)
	return particles
