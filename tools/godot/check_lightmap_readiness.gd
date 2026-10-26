extends SceneTree
func _initialize() -> void:
	var scene: Node = load("res://assets/game/ARCH_Courtyard_v003_game.glb").instantiate()
	var meshes: Array[Dictionary] = []
	for mesh in scene.find_children("*", "MeshInstance3D", true, false):
		var arrays: Array = mesh.mesh.surface_get_arrays(0)
		meshes.append({"mesh":mesh.name,"gi_mode":mesh.gi_mode,"uv2_vertices":arrays[Mesh.ARRAY_TEX_UV2].size() if arrays[Mesh.ARRAY_TEX_UV2]!=null else 0})
	var report := {"meshes":meshes,"bake_attempted":false,"reason":"Architecture has no UV2; lightmap atlas and editor GPU bake are a separate asset revision. Current porch fill is explicitly an approximation, not baked GI."}
	FileAccess.open("res://reports/validation/Courtyard_Look_v001_Lightmap_Readiness.json",FileAccess.WRITE).store_string(JSON.stringify(report,"\t")+"\n")
	print("LIGHTMAP_READINESS: ",JSON.stringify(report))
	scene.free()
	quit()
