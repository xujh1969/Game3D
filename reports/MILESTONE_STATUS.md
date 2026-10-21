# MountainCourtyard 开发状态

更新：2026-10-22（Asia/Shanghai）。

| 阶段 | 状态 | 当前结果 |
|---|---|---|
| M0 | PASS_WITH_LIMITATIONS | Godot 4.7.2、Blender 5.2.2 LTS、Python/Git可用；GitHub main 同步；Git LFS仓库级启用。Godot Mobile在本机AMD Radeon集显/Vulkan1.3.260实际运行。管理目录使用.gdignore消除CSV误导入。工程以脚本构建的灰盒为主，部分场景组织将在美术阶段整理。|
| M1 | PASS_WITH_LIMITATIONS | 修复移动方向、角色与相机反馈、线索焦点、隔墙交互、门轴/碰撞、通关幂等/菜单；实际引擎回归检查通过；headless与Mobile无传送输入路线均完成0→3→开门→通关。完整真人操作、按钮实点和镜头体验未验收；角色动画仍缺。|
| M2 | IN_PROGRESS | AssetTest、Blender检查/不覆盖版本导出工具已用TEMP立方体实测；正式资产为零。角色/门概念图已由用户于2026-10-22认可，视觉方向确认；庭院图调用长时间未返回，已中止本轮等待，没有图像交付（BLOCKED_TOOL）。|
| M3–M7 | NOT_STARTED | 未开始正式模型集成、正式建筑/角色、最终性能与发布。|

## 证据

- 详细M1记录：`reports/validation/M1_ACCEPTANCE_2026-10-22.md`。
- 回归：`m1_runtime.log`；图形回归：`m1_mobile_runtime.log`。
- 无传送路线：`m1_playthrough_headless.log`、`m1_playthrough_mobile_fixed.log`；退出码均0，PLAYTHROUGH_RESULT=PASS。
- 首轮失败日志保留：`m1_before.log`、`m1_door_before.log`、`m1_playthrough_mobile.log`。
- GPU真实画面：`reports/screenshots/M1_*.png`；非美术效果图。
- Blender报告：`reports/validation/TEMP_cube_import.json`，12 triangles、[1,1,1]m、缺失文件0；导出同版保护，不代表正式资产验收。
- AssetTest实拍帧：`reports/screenshots/AssetTest_TEMP_Cube.png`。
- 最终导入日志：`reports/validation/final_import.log`；资源扫描退出0。
- Computer Use被用户物理Esc停止；已停止后续界面自动操作。未把自动输入路线当作真人验收。

## 当前门槛

青岚与木门参考图方向已确认，批准证据见 `handoff/approvals/USER_APPROVAL_2026-10-22_Qinglan_Door_v001.md`。这两项不再重复索取视觉认可。庭院构图及正式3D/角色骨架动画/生产资产许可仍待后续审核。审核文件 `handoff/approvals/ART_DIRECTION_v001.md`，索引 `handoff/REQUESTS.md`。后续木门制作按已批准参考推进；本次仅记录用户审批，未生成新模型。

FPS_NOT_MEASURED：GPU后端可运行，不等于已经达到最终720p 30fps。未测最终画质、导出包或长时间稳定性。
