# 技术架构

- `scenes/world/Courtyard_Blockout.tscn`：世界、线索、门、终点与 HUD。
- `scenes/character/Qinglan_TEMP.tscn`：CharacterBody3D 胶囊代理、SpringArm3D 与 Camera3D。
- `scripts/gameplay/game_state.gd`：线索集合、解锁信号、重开。
- `scripts/player/player_controller.gd`：移动、转向、近距离交互焦点。
- `scripts/player/third_person_camera.gd`：鼠标 yaw/pitch 与 SpringArm。
- `scripts/interactables/`：线索、门、终点。
- `scripts/ui/hud.gd`：线索计数和通关提示。

当前状态仍是 M1 初稿；暂停菜单、交互提示、焦点方向/遮挡校验和完整行为验收未完成。
