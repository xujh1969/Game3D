extends "res://tests/test_playthrough.gd"

var frame_intervals: Array[float] = []
var previous_tick := 0
var started_tick := 0
var peak_draws := 0.0
var slow_samples: Array[Dictionary] = []
var movement_started_tick := 0
var startup_max_frame_ms := 0.0

func run() -> void:
	if DisplayServer.get_name() == "headless":
		push_error("Moving GPU profile requires a graphical backend")
		quit(1)
		return
	started_tick = Time.get_ticks_usec()
	process_frame.connect(sample_frame)
	await super.run()
	var ordered := frame_intervals.duplicate()
	ordered.sort()
	var duration := 0.0
	var slow_frames := 0
	for interval in frame_intervals:
		duration += interval
		if interval > 1.0 / 30.0:
			slow_frames += 1
	var report := {
		"date": "2026-10-26", "look": "v001 / garden v003 / ridges v004",
		"device": RenderingServer.get_video_adapter_name(),
		"renderer": ProjectSettings.get_setting("rendering/renderer/rendering_method"),
		"viewport": [root.size.x, root.size.y], "warmup_seconds": 2,
		"warmup_reference": "first observed physical movement; startup excluded from movement statistics",
		"startup_seconds_before_movement": float(movement_started_tick-started_tick)/1000000.0,
		"startup_max_frame_ms": startup_max_frame_ms,
		"route_passed": not failed and state.won and state.clues.size() == 3,
		"frames": ordered.size(), "measured_seconds": duration,
		"average_fps": ordered.size() / duration,
		"maximum_frame_ms": ordered[-1] * 1000,
		"minimum_instantaneous_fps": 1.0 / ordered[-1],
		"p95_frame_ms": ordered[ceili(ordered.size()*.95)-1] * 1000,
		"p99_frame_ms": ordered[ceili(ordered.size()*.99)-1] * 1000,
		"frames_over_33_33_ms": slow_frames, "slow_samples": slow_samples, "peak_draw_calls": peak_draws,
		"limitations": "Actual scripted input route on graphical backend; wall-clock frame intervals. No native human input or long stability acceptance."
	}
	FileAccess.open("res://reports/validation/Courtyard_Look_v001_Route_Profile.json", FileAccess.WRITE).store_string(JSON.stringify(report,"\t")+"\n")
	print("LOOK_ROUTE_PROFILE: ", JSON.stringify(report))

func sample_frame() -> void:
	var now := Time.get_ticks_usec()
	# Stop before victory screenshot readback/PNG encoding; that is not gameplay frame time.
	if is_instance_valid(state) and state.won:
		return
	if movement_started_tick == 0:
		if previous_tick > 0:
			startup_max_frame_ms = maxf(startup_max_frame_ms, float(now-previous_tick)/1000)
		if is_instance_valid(player) and Vector2(player.position.x, player.position.z-10).length() > .05:
			movement_started_tick = now
	if previous_tick > 0 and movement_started_tick > 0 and now - movement_started_tick > 2000000:
		var interval := float(now - previous_tick) / 1000000.0
		frame_intervals.append(interval)
		if interval > 1.0 / 30.0:
			slow_samples.append({"sample_seconds":float(now-started_tick)/1000000.0,"frame_ms":interval*1000,"player_position":str(player.position),"clues":state.clues.size()})
		peak_draws = maxf(peak_draws, Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
	previous_tick = now
