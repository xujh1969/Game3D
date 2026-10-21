extends Node3D

func _ready() -> void:
	var path := "res://assets/temporary/TEMP_Pipeline_Cube_v001.glb"
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--asset="):
			path = argument.trim_prefix("--asset=")
	if not ResourceLoader.exists(path):
		push_error("Asset missing: " + path)
		return
	var packed := load(path) as PackedScene
	if packed == null:
		push_error("Expected an imported GLB scene: " + path)
		return
	$Asset.add_child(packed.instantiate())
	$Label3D.text = "Asset review · 1m reference\n" + path.get_file()
	if "--capture" in OS.get_cmdline_user_args():
		await get_tree().process_frame
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("res://reports/screenshots/AssetTest_TEMP_Cube.png")
		get_tree().quit()
