extends Area3D

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node3D) -> void:
	var state := get_parent().get_node("GameState")
	if body == get_parent().get_node("Player") and state.clues.size() == 3 and get_parent().get_node("Door").is_open and not state.won:
		state.won = true
		state.game_won.emit()
