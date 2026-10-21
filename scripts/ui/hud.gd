extends CanvasLayer

var label: Label
var message: Label
var prompt: Label
var pause_panel: PanelContainer
var menu_title: Label
var resume_button: Button

func _ready() -> void:
	label = Label.new()
	label.position = Vector2(24, 20)
	label.add_theme_font_size_override("font_size", 24)
	add_child(label)
	message = Label.new()
	message.position = Vector2(24, 58)
	message.add_theme_font_size_override("font_size", 20)
	add_child(message)
	prompt = Label.new()
	prompt.anchor_left = 0.0
	prompt.anchor_top = 0.78
	prompt.anchor_right = 1.0
	prompt.anchor_bottom = 0.78
	prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt.add_theme_font_size_override("font_size", 22)
	add_child(prompt)
	_build_pause_panel()
	process_mode = Node.PROCESS_MODE_ALWAYS
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
	prompt.text = ""
	menu_title.text = "抵达内院 · 灰盒流程完成"
	resume_button.hide()
	pause_panel.show()
	set_process_input(true)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().paused = true

func set_interaction(text: String) -> void:
	prompt.text = text

func show_message(text: String) -> void:
	message.text = text
	get_tree().create_timer(2.5).timeout.connect(func():
		if message.text == text:
			message.text = ""
	)

func _build_pause_panel() -> void:
	pause_panel = PanelContainer.new()
	pause_panel.anchor_left = 0.5
	pause_panel.anchor_top = 0.5
	pause_panel.anchor_right = 0.5
	pause_panel.anchor_bottom = 0.5
	pause_panel.offset_left = -150
	pause_panel.offset_top = -110
	pause_panel.offset_right = 150
	pause_panel.offset_bottom = 110
	pause_panel.visible = false
	add_child(pause_panel)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 12)
	pause_panel.add_child(box)
	menu_title = Label.new()
	menu_title.text = "暂停"
	menu_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(menu_title)
	resume_button = Button.new()
	resume_button.text = "继续游戏"
	resume_button.pressed.connect(_toggle_pause)
	box.add_child(resume_button)
	var restart := Button.new()
	restart.text = "重新开始"
	restart.pressed.connect(func():
		get_tree().paused = false
		get_parent().get_node("GameState").restart()
	)
	box.add_child(restart)
	var quit := Button.new()
	quit.text = "退出游戏"
	quit.pressed.connect(func(): get_tree().quit())
	box.add_child(quit)

func _input(event: InputEvent) -> void:
	var won: bool = get_parent().get_node("GameState").won
	if event.is_echo():
		return
	if event.is_action_pressed("pause") and not won:
		_toggle_pause()
		get_viewport().set_input_as_handled()
	if event.is_action_pressed("ui_accept") and won:
		get_viewport().set_input_as_handled()
		get_parent().get_node("GameState").restart()

func _toggle_pause() -> void:
	var paused := not get_tree().paused
	get_tree().paused = paused
	pause_panel.visible = paused
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE if paused else Input.MOUSE_MODE_CAPTURED
