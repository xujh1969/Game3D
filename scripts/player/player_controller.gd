extends CharacterBody3D

@export var walk_speed := 3.5
@export var run_speed := 5.5
@export var turn_speed := 10.0
var focus: Node3D
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

func _physics_process(delta: float) -> void:
	if get_tree().paused:
		return
	if not is_on_floor():
		velocity.y -= gravity * delta
	var input := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var camera_basis: Basis = $SpringArm3D/Camera3D.global_basis
	var forward: Vector3 = -camera_basis.z
	var right: Vector3 = camera_basis.x
	forward.y = 0
	right.y = 0
	var direction: Vector3 = (right.normalized() * input.x - forward.normalized() * input.y).normalized()
	var speed := run_speed if Input.is_action_pressed("run") else walk_speed
	velocity.x = direction.x * speed
	velocity.z = direction.z * speed
	if direction.length() > 0.1:
		$Proxy.rotation.y = lerp_angle($Proxy.rotation.y, atan2(-direction.x, -direction.z), minf(turn_speed * delta, 1.0))
	move_and_slide()
	_update_focus()
	if Input.is_action_just_pressed("interact") and is_instance_valid(focus):
		focus.interact(self)

func _update_focus() -> void:
	focus = null
	var best_distance := 2.5
	var player_forward: Vector3 = -$Proxy.global_basis.z
	for node in get_tree().get_nodes_in_group("interactable"):
		if not node is Node3D:
			continue
		var distance := global_position.distance_to(node.global_position)
		var toward: Vector3 = (node.global_position - global_position).normalized()
		if distance < best_distance and player_forward.dot(toward) > 0.2:
			var query := PhysicsRayQueryParameters3D.create(global_position + Vector3.UP * 1.2, node.global_position, 1, [get_rid()])
			var hit := get_world_3d().direct_space_state.intersect_ray(query)
			if not hit.is_empty() and hit.collider != node:
				continue
			best_distance = distance
			focus = node
	var hud := get_parent().get_node("UI")
	if is_instance_valid(focus):
		hud.set_interaction(focus.get_prompt())
	else:
		hud.set_interaction("")
