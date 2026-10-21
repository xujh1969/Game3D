# MountainCourtyard 开发状态

更新：2026-10-22（Asia/Shanghai）。

| 阶段 | 状态 | 当前结果 |
|---|---|---|
| M0 | PASS_WITH_LIMITATIONS | Godot4.7.2、Blender5.2.2 LTS和Python/Git可用；Mobile在AMD Radeon集显/Vulkan1.3.260实测运行；GitHub main与Git LFS同步。管理/源资产/报告目录排除Godot资源扫描。|
| M1 | PASS_WITH_LIMITATIONS | TEMP几何代理增加Idle/Walk/Run，headless/Mobile各10项检查通过；24项M1回归与本轮headless完整路线通过，前轮Mobile完整路线已通过。开发F3性能HUD可用。真人体验与长期稳定性未验收。|
| M2 | IN_PROGRESS | 青岚与木门v001参考已批准；庭院主视角v002和Blender入口/斜向尺度草案已制作、查看，等待HUMAN GATE #2方向批准。其余试制资产未生产。|
| M3 | IN_PROGRESS | ARCH_003木门v003完成源文件、PBR、独立双门物理轴与关卡替换，状态PASS_WITH_LIMITATIONS；苔藓岩石/香炉尚未制作或提交。|
| M4 | WAITING_FOR_USER | 庭院体量DRAFT源文件与两张实际离线渲染供审，尚未接入运行场景；正式建筑制作等待HUMAN GATE #2批准。|
| M5–M7 | NOT_STARTED | 正式青岚及动画、最终照明/性能与发布包尚未完成。|

## 本轮交付与证据

- 本轮新增报告`reports/validation/PROXY_AND_PROFILE_v001.md`：TEMP动作、回归与真实GPU静止灰盒测量。实际720p平均144.02FPS/最低瞬时100.07FPS，采样10.005424秒；不代表最终美术性能。原始JSON、日志和截图保留。
- 构图审核：`handoff/approvals/COURTYARD_COMPOSITION_DRAFT_v001.md`。入口/主视角两张概念图v002与Blender两张尺寸草案均已查看；草案不是正式模型或Godot画面。源BLEND和生成脚本保留。

## 上轮木门交付（保持有效）

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

请用户审核庭院建筑体量/中轴布局/清晨氛围方向，批准后推进模块化正式主建筑、香炉和岩石；青岚正式模型及动画另按M5生产。已批准的角色/木门无需重复方向审批。

FPS_NOT_MEASURED仅用于最终美术场景：当前静止灰盒已有真实GPU基线，最终庭院/照明负载、长期稳定性和Windows发布包尚未验收。
