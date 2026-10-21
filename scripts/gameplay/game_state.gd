extends Node

signal clue_collected(id: String)
signal door_unlocked
signal game_won

var clues: Dictionary = {}
var won := false

func collect_clue(id: String) -> bool:
	if clues.has(id):
		return false
	clues[id] = true
	clue_collected.emit(id)
	if clues.size() == 3:
		door_unlocked.emit()
	return true

func restart() -> void:
	clues.clear()
	won = false
	get_tree().reload_current_scene()
