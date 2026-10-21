extends Label

var elapsed := 0.0

func _ready() -> void:
	visible = OS.is_debug_build()
	_update_counters()

func _process(delta: float) -> void:
	elapsed += delta
	if visible and elapsed >= 0.25:
		elapsed = 0
		_update_counters()

func _update_counters() -> void:
	text = "FPS %d · Draw %d · Primitives %d · F3" % [Engine.get_frames_per_second(), Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME), Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME)]

func _unhandled_input(event: InputEvent) -> void:
	if OS.is_debug_build() and event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F3:
		visible = not visible
