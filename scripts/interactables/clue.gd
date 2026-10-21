extends Area3D

@export var clue_id := "CLUE_001"
@export var title := "线索"
var collected := false

func _ready() -> void:
	add_to_group("interactable")

func interact(_player: Node3D) -> void:
	if collected:
		return
	var state := get_parent().get_node("GameState")
	if state.collect_clue(clue_id):
		collected = true
		visible = false
		set_deferred("monitoring", false)

func get_prompt() -> String:
	return "E 读取：" + title
