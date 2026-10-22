extends SceneTree

var failures := 0
var capture_prefix := "CHAR_001_Review_v002"

func _initialize() -> void:
	run.call_deferred()

func check(condition: bool, label: String) -> void:
	print(("PASS: " if condition else "FAIL: ") + label)
	if not condition:
		failures += 1

func run() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture-prefix="):
			capture_prefix = argument.trim_prefix("--capture-prefix=")
	var stage: Node3D = load("res://scenes/world/AssetTest.tscn").instantiate()
	root.add_child(stage)
	current_scene = stage
	var holder := stage.get_node("Asset")
	var meshes := holder.find_children("*", "MeshInstance3D", true, false)
	check(meshes.size() == 1, "one character mesh in review stage")
	if meshes.size() != 1:
		quit(1)
		return
	var character: MeshInstance3D = meshes[0]
	var bounds := character.get_aabb()
	var triangles := 0
	for surface in character.mesh.get_surface_count():
		triangles += character.mesh.surface_get_array_index_len(surface) / 3
	check(absf(bounds.size.y - 1.70) < 0.005, "normalized 1.70m height")
	check(absf(bounds.position.y) < 0.005, "feet base at ground zero")
	check(triangles > 20000 and triangles <= 31000, "review mesh within 20k-31k triangle budget")
	check(character.mesh.get_surface_count() == 1, "one shared material surface")
	var material := character.mesh.surface_get_material(0) as StandardMaterial3D
	check(material != null and material.albedo_texture != null, "base color available")
	check(material != null and material.normal_texture != null and material.roughness_texture != null, "normal and packed roughness available")
	check(holder.find_children("*", "Skeleton3D", true, false).is_empty(), "source honestly identified as unrigged")
	var summary := {"status": "PASS_WITH_LIMITATIONS" if failures == 0 else "FAILED",
		"failures": failures, "triangles": triangles, "size_m": [bounds.size.x, bounds.size.y, bounds.size.z],
		"limitations": "Independent static review only; no rig/animations or production approval"}
	var file := FileAccess.open("res://reports/validation/"+capture_prefix+".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(summary, "\t") + "\n")
	if DisplayServer.get_name() != "headless":
		stage.get_node("Overlay/Label").text = "QINGLAN | TECHNICAL EXPERIMENT | UNRIGGED"
		var camera: Camera3D = stage.get_node("Camera3D")
		camera.projection = Camera3D.PROJECTION_ORTHOGONAL
		for shot in [["Front", Vector3(0,.85,3), Vector3(0,.85,0), 2.1],
			["Left", Vector3(3,.85,0), Vector3(0,.85,0), 2.1],
			["Right", Vector3(-3,.85,0), Vector3(0,.85,0), 2.1],
			["Back", Vector3(0,.85,-3), Vector3(0,.85,0), 2.1],
			["Face", Vector3(0,1.50,2), Vector3(0,1.50,0), .55]]:
			camera.size = shot[3]
			camera.position = shot[1]
			camera.look_at(shot[2])
			for frame in 10:
				await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://reports/screenshots/"+capture_prefix+"_"+shot[0]+".png")
		material.normal_enabled = false
		for frame in 10:
			await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://reports/screenshots/"+capture_prefix+"_FaceNoNormal.png")
		material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		for frame in 10:
			await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://reports/screenshots/"+capture_prefix+"_FaceUnshaded.png")
	print("QINGLAN_REVIEW_RESULT: ", failures, " failures")
	quit(0 if failures == 0 else 1)
