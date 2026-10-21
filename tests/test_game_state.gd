extends SceneTree

func _init() -> void:
	var state := Node.new()
	state.set_script(load("res://scripts/gameplay/game_state.gd"))
	root.add_child(state)
	var unlocks := [0]
	state.door_unlocked.connect(func(): unlocks[0] += 1)
	assert(state.collect_clue("CLUE_001"))
	assert(not state.collect_clue("CLUE_001"))
	assert(unlocks[0] == 0)
	assert(state.collect_clue("CLUE_002"))
	assert(unlocks[0] == 0)
	assert(state.collect_clue("CLUE_003"))
	assert(unlocks[0] == 1)
	assert(not state.collect_clue("CLUE_003"))
	print("PASS: unique clue counting and one-time unlock signal")
	quit()
