extends Node3D

var unlocked := false
var is_open := false
var is_opening := false

func _ready() -> void:
	var left_visual: Node3D = $Visual.find_child("LeafLeft", true, false)
	var right_visual: Node3D = $Visual.find_child("LeafRight", true, false)
	left_visual.reparent($LeftLeaf, false)
	left_visual.transform = Transform3D.IDENTITY
	right_visual.reparent($RightLeaf, false)
	right_visual.transform = Transform3D.IDENTITY
	add_to_group("interactable")
	get_parent().get_node("GameState").door_unlocked.connect(_on_unlocked)

func _on_unlocked() -> void:
	unlocked = true

func interact(_player: Node3D) -> void:
	if not unlocked:
		get_parent().get_node("UI").show_message("门被锁住了，还需要收集线索。")
		return
	if is_open or is_opening:
		return
	is_opening = true
	remove_from_group("interactable")
	var tween := create_tween()
	tween.set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)
	tween.set_parallel(true)
	tween.tween_property($LeftLeaf, "rotation:y", PI * 0.5, 0.8).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property($RightLeaf, "rotation:y", -PI * 0.5, 0.8).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.finished.connect(func():
		is_open = true
		is_opening = false
	)

func get_prompt() -> String:
	return "E 打开木门" if unlocked else "E 查看木门（线索不足）"
