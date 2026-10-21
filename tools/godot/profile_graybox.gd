extends SceneTree

var started := 0
var previous := 0
var intervals: Array[float] = []
var draw_calls: Array[float] = []
var primitives: Array[float] = []
var focused_frames := 0
var finishing := false
var world: Node
var report_name := "Graybox_Profile_v001"

func _initialize() -> void:
	run.call_deferred()

func run() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--report-name="):
			report_name = argument.trim_prefix("--report-name=")
	if DisplayServer.get_name() == "headless":
		push_error("GPU baseline requires a graphical backend; headless cannot measure it")
		quit(1)
		return
	world = load("res://scenes/world/Courtyard_Blockout.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	world.get_node("Player/SpringArm3D").set_process_unhandled_input(false)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	started = Time.get_ticks_usec()
	process_frame.connect(sample_frame)

func sample_frame() -> void:
	if finishing:
		return
	var now := Time.get_ticks_usec()
	var elapsed := float(now - started) / 1000000.0
	if elapsed < 2.0:
		previous = now
		return
	if previous > 0:
		intervals.append(float(now - previous) / 1000000.0)
		draw_calls.append(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
		primitives.append(Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME))
		if DisplayServer.window_is_focused():
			focused_frames += 1
	previous = now
	if elapsed >= 12.0:
		finishing = true
		finish.call_deferred()

func finish() -> void:
	var measured_seconds := 0.0
	for interval in intervals:
		measured_seconds += interval
	var report := {
		"status": "PASS_WITH_LIMITATIONS",
		"date": "2026-10-22",
		"scene": "Courtyard_Blockout / static spawn / " + ("ENV_BambooLandscape_v002 + " if world.has_node("EnvironmentScenery") else "") + ("ARCH_Courtyard_v002 + NAT_001 v001 + " if world.has_node("Architecture") else "") + "TEMP articulated proxy + ARCH_003 v003",
		"device": RenderingServer.get_video_adapter_name(),
		"renderer": ProjectSettings.get_setting("rendering/renderer/rendering_method"),
		"viewport": [root.size.x, root.size.y],
		"warmup_seconds": 2,
		"measured_seconds": measured_seconds,
		"frames": intervals.size(),
		"average_fps": intervals.size() / measured_seconds,
		"minimum_instantaneous_fps": 1.0 / intervals.max(),
		"maximum_frame_ms": intervals.max() * 1000.0,
		"focused_frames": focused_frames,
		"draw_calls_max": draw_calls.max(),
		"rendered_primitives_max": primitives.max(),
		"limitations": "Static development scene only; process_frame wall-clock intervals after warmup. Minimum is reciprocal of the single slowest frame. Includes development HUD and desktop overhead. Not final art performance, not a 30fps acceptance result."
	}
	var hud: Label = world.get_node("UI/DebugHUD")
	var key := InputEventKey.new()
	key.keycode = KEY_F3
	key.pressed = true
	var visible_before := hud.visible
	hud._unhandled_input(key)
	report["debug_toggle_checked"] = hud.visible != visible_before
	hud._unhandled_input(key)
	var file := FileAccess.open("res://reports/validation/" + report_name + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t") + "\n")
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://reports/screenshots/" + report_name + ".png")
	print("GRAYBOX_PROFILE: ", JSON.stringify(report))
	quit()
