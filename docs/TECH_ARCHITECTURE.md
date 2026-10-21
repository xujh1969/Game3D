# 技术架构

- `scenes/world/Courtyard_Blockout.tscn`：世界、碰撞边界、墙段/门、三项线索、终点、HUD。
- `scenes/character/Qinglan_TEMP.tscn`：CharacterBody3D 根节点、Proxy 胶囊、TEMP 标签、SpringArm3D 和 Camera3D。
- `scripts/player/player_controller.gd`：水平面相机相对移动；仅 Proxy 转向，相机与碰撞根节点不随人物朝向旋转。近距离/朝向筛选加物理射线遮挡检查得到焦点，E调用该焦点；可选InteractionPoint定义观察点，物理子节点被识别为同一交互对象。
- `scripts/player/third_person_camera.gd`：鼠标 yaw/pitch 和 SpringArm，排除玩家自身碰撞。Esc/鼠标模式由 HUD 统一管理。
- `scripts/gameplay/game_state.gd`：世界内状态节点，保存线索集合及解锁/胜利信号；重开解除暂停并重载当前场景。目前未设为 autoload，单场景闭环使用世界内节点。
- `scripts/interactables/clue.gd`：唯一拾取后退出交互组。
- `scripts/interactables/door_controller.gd`：Door.tscn的Node3D根控制器，固定框体与左右StaticBody3D门扇。GLB中的LeafLeft/LeafRight在ready时挂到对应物理门轴；物理tween同步反向旋转±90°，保留碰撞，结束才标为打开。
- `scripts/interactables/finish_trigger.gd`：实际玩家/三线索/门已开且未胜利时触发一次；HUD 暂停并显示重开/退出。
- `scripts/ui/hud.gd`：计数、交互提示、暂时反馈、暂停/胜利菜单；always processing 允许暂停时响应按钮。
- `scenes/world/AssetTest.tscn`：模型尺度和材质审查，入口脚本 `scripts/debug/asset_test.gd`。

测试入口：`tests/test_game_state.gd`（计数信号）、`tests/test_m1_runtime.gd`（实际场景行为）、`tests/test_playthrough.gd`（无传送输入路线）。详情与边界见 `reports/validation/M1_ACCEPTANCE_2026-10-22.md`。
