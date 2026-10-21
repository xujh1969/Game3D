# M1 验收记录

日期：2026-10-22（Asia/Shanghai）。本机 Godot 4.7.2 stable，AMD Radeon(TM) Graphics，Vulkan 1.3.260，Forward Mobile，窗口视口 1280×720。

## 已执行

- `--headless --script res://tests/test_m1_runtime.gd`：实际实例化主场景，驱动 CharacterBody3D 与物理帧，检查 W 方向、角色转向不带动相机、锁门与通门、隔墙遮挡焦点、E 拾取、去重、计数、门动画/碰撞、胜利幂等、重开、暂停恢复和边界。
- 同一脚本在 Mobile 图形后端运行通过，日志 `m1_mobile_runtime.log`；画面在 GPU 完成一帧后通过 Viewport 保存，没有另行合成。
- `--script res://tests/test_playthrough.gd`：从出生点沿路径步行，以 Input action 驱动真实玩家，依次按 E 拾取、开门、走入终点，没有传送角色或直接触发线索。headless 与 Mobile 图形后端均通过。Mobile 最终日志 `m1_playthrough_mobile_fixed.log`；截图 `../screenshots/M1_Playthrough_Victory_TEMP.png`。
- 首轮 Mobile 自动路线受系统鼠标输入改变相机方向，未通过；失败证据保留在 `m1_playthrough_mobile.log`。自动路线驱动固定相机并释放鼠标，隔离外部鼠标输入后重跑通过。正常游戏仍支持鼠标旋转。
- `--headless --import`：最终资源扫描通过，日志 `final_import.log`。管理/参考/报告目录加入 `.gdignore`，避免 CSV 被误导入为翻译和参考图进入运行资源。
- Windows Computer Use 已实际查看游戏窗口和中文 HUD；后续用户按物理 Esc 停止 Computer Use，本轮已停止该界面自动操作。

## 修复与证据

首次场景检查复现 W 方向相反、角色转身带动相机、未开门可触发胜利、已收集线索保留焦点、胜利状态未记录五项失败，见 `m1_before.log`。扩展门/遮挡检查又复现三项失败，见 `m1_door_before.log`。修复后自动场景检查通过。

SpringArm 实测门前回缩：玩家 Z=-6.7，相机 Z=-7.914432，门前表面 Z=-7.925，hit length=1.234375；镜头位置未进入门面。该样本不能穷尽所有相机角度。

## 验收边界

状态：PASS_WITH_LIMITATIONS。通过的是引擎输入与物理驱动的自动流程及渲染检查；完整真人键鼠通关、全部菜单按钮实点、长时间稳定性与镜头手感仍待体验。代理角色和金色球形线索均为 TEMP，角色动画尚未制作。未做有代表性的持续 FPS 测量，不能据此宣称达到 720p 30fps。
