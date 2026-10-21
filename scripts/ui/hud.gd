extends CanvasLayer

var label: Label
var message: Label

func _ready() -> void:
	label = Label.new()
	label.position = Vector2(24, 20)
	label.add_theme_font_size_override("font_size", 24)
	add_child(label)
	message = Label.new()
	message.position = Vector2(24, 58)
	message.add_theme_font_size_override("font_size", 20)
	add_child(message)
	var state := get_parent().get_node("GameState")
	state.clue_collected.connect(_on_clue_collected)
	state.game_won.connect(_on_game_won)
	_update_count()

func _on_clue_collected(_id: String) -> void:
	_update_count()

func _update_count() -> void:
	label.text = "线索：%d/3     WASD 移动  Shift 奔跑  E 互动  Esc 菜单" % get_parent().get_node("GameState").clues.size()

func _on_game_won() -> void:
	message.text = "你已抵达内院。按 Enter 重新开始。"
	set_process_input(true)

func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept") and message.text.begins_with("你已抵达"):
		get_parent().get_node("GameState").restart()
