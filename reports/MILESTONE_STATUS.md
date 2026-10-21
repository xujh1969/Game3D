# MountainCourtyard 开发状态

更新：2026-10-22（Asia/Shanghai）。

| 阶段 | 状态 | 当前结果 |
|---|---|---|
| M0 | PASS_WITH_LIMITATIONS | Godot4.7.2、Blender5.2.2 LTS和Python/Git可用；Mobile在AMD Radeon集显/Vulkan1.3.260实测运行；GitHub main与Git LFS同步。管理/源资产/报告目录排除Godot资源扫描。|
| M1 | PASS_WITH_LIMITATIONS | 原玩法闭环保持可运行；新增双门后24项引擎行为回归通过。headless/Mobile完整无传送输入路线均通过。真人键鼠体验、全部按钮实点、角色动画及长期稳定性未验收。|
| M2 | IN_PROGRESS | 青岚与木门v001参考设计已获用户批准；AssetTest和Blender导入/导出工具已实测。木门v003开始作为非TEMP资产使用。庭院图前次调用未返回，尚待重新制作和构图审批；其余试制资产未生产。|
| M3 | IN_PROGRESS | ARCH_003木门v003完成源文件、PBR、独立双门物理轴与关卡替换，状态PASS_WITH_LIMITATIONS；苔藓岩石/香炉尚未制作或提交。|
| M4–M7 | NOT_STARTED | 正式庭院/主建筑、正式青岚及动画、最终照明/性能与发布包尚未完成。|

## 本轮交付与证据

- 木门交付报告：`reports/validation/ARCH_003_DELIVERY_v003.md`，完整文件名、尺寸/面数、来源、验证命令与限制。
- 源BLEND：`assets/source/ARCH_003_DoorSong_v003.blend`；GLB：`assets/game/ARCH_003_DoorSong_v003_game.glb`。v001/v002试制稿保留。
- 实测：7,740 triangles，3网格组、2材质、3张1024²内嵌PBR贴图；框体2.24×2.66×0.186m，独立左右门轴X=-1/+1m；缺失贴图0。
- `tests/test_door_asset.py` 结构检查通过；`ARCH_003_import_v003.json` 为Blender导入测量报告。
- Godot导入日志 `ARCH_003_godot_import.log`；Mobile双门检查 `ARCH_003_double_door_mobile.log`（8项通过）。
- 回归 `ARCH_003_M1_regression.log`（24项通过）；完整路线 `ARCH_003_playthrough_v003.log` / `ARCH_003_playthrough_mobile_v003.log`，均PASS，成功命令退出码0。
- 实际图像：`reports/screenshots/ARCH_003_DoorSong_v003_*.png`、`AssetTest_ARCH_003_DoorSong_v003_game.png`、`ARCH_003_Playthrough_v003.png`。均实际渲染帧，已查看。
- 木材源贴图采用Poly Haven CC0，保留原文件、来源与校验值；来源文档 `docs/ASSET_LICENSES.md`。
- 原M1验收历史保留在 `reports/validation/M1_ACCEPTANCE_2026-10-22.md`；当时用户物理Esc停止Computer Use。本轮没有使用Windows界面自动按键，运行的是引擎输入脚本与渲染检查。

## 下一步

继续庭院入口/主视角参考图与构图确认，然后推进香炉、岩石和主建筑；青岚正式模型及动画另按M5生产。已批准的角色/木门设计无需重复征求视觉方向认可。任何重大外观变更保留新版本。

FPS_NOT_MEASURED：完成GPU渲染与玩法检查不等于最终720p 30fps达标；持续帧率、最终照明和Windows发布包尚未验收。
