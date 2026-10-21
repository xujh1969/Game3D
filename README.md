# MountainCourtyard / 山中古院

Godot 4.7.2，Windows 单机第三人称宋风山居探索解谜。当前是30×30m可玩灰盒，青岚胶囊、金色线索标记和墙段均为 TEMP。正式写实美术尚未进入游戏。

## 启动和操作

本机双击 `Play.cmd`，或在 Godot 中打开 `project.godot` 后 F6/F5 运行。启动脚本使用已检测的本机 Godot 安装路径；其他机器需修改路径或从编辑器运行。默认 Mobile 后端已在 AMD Radeon(TM) Graphics / Vulkan 1.3.260 实际启动。

- WASD：相机相对移动；Shift：奔跑；鼠标：绕角色旋转镜头。
- 靠近并朝向三个金色 TEMP 线索，出现提示后按 E 收集。
- 集齐三项后靠近主殿中间木门按 E，等待门打开，穿门走向内院终点。
- Esc：暂停/继续；菜单提供重开和退出。通关后可点击重开或退出，Enter 也可重开。

## 已验证和限制

实际 Godot 物理场景检查通过，headless 和本机 Mobile 图形后端的无传送自动输入路线均通过（0→3→开门→步行到终点）。日志、截图与验证边界见 `reports/validation/M1_ACCEPTANCE_2026-10-22.md`。

完整真人键鼠通关、菜单按钮实点和长期镜头体验仍待验收。角色没有正式模型或动画，正式资产为零。未做持续 FPS 测量，不能宣称最终画质或720p 30fps达标。

## 视觉方向审核

生成的待审角色、门和庭院初稿位于 `handoff/reference/generated/`。批准和修改要求见 `handoff/approvals/ART_DIRECTION_v001.md`，图像与资产索引见 `handoff/REQUESTS.md`。模型制作受艺术审核门槛约束。

## 开发工具

```text
Godot --headless --path . --script res://tests/test_m1_runtime.gd
Godot --headless --path . --script res://tests/test_playthrough.gd
Godot --path . res://scenes/world/AssetTest.tscn -- --asset=res://assets/game/FILE.glb
```

Blender 检查/导出工具用法见 `docs/ASSET_PIPELINE.md`。资产清单和性能日志位于 `project_admin/`；管理文件夹带 `.gdignore`，不会被 Godot 当作翻译表或运行资产导入。Git LFS 保存GLB、BLEND、FBX和图像，克隆后需要安装Git LFS并拉取对应文件。
