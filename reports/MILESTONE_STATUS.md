# MountainCourtyard 开发状态

更新：2026-10-22（Asia/Shanghai）。

| 阶段 | 状态 | 当前结果 |
|---|---|---|
| M0 | PASS_WITH_LIMITATIONS | Godot4.7.2、Blender5.2.2 LTS和Python/Git可用；Mobile在AMD Radeon集显/Vulkan1.3.260实测运行；GitHub main与Git LFS同步。管理/源资产/报告目录排除Godot资源扫描。|
| M1 | PASS_WITH_LIMITATIONS | TEMP几何代理增加Idle/Walk/Run，headless/Mobile各10项检查通过；24项M1回归与本轮headless完整路线通过，前轮Mobile完整路线已通过。开发F3性能HUD可用。真人体验与长期稳定性未验收。|
| M2 | IN_PROGRESS | 青岚与木门参考已批准；庭院概念/尺度草案提交后用户指示继续开发，沿用方向推进。岩石已采用许可核验的CC0扫描资产；香炉参考与资产待制作。|
| M3 | IN_PROGRESS | 木门v003与三种NAT_001岩石v001已接入、校验和查看，均PASS_WITH_LIMITATIONS；正式香炉未完成。|
| M4 | IN_PROGRESS | 建筑/岩石首版保持可玩；新增竹丛/三层远山v002，6项环境检查、24项回归及Mobile完整输入通关通过。v001源保留，v002修正远山分面。山体轮廓和近景材质未达最终目标。|
| M5 | NOT_STARTED | 正式青岚模型/骨骼/动画与许可尚未完成，现为TEMP几何动作。|
| M6 | IN_PROGRESS | Mobile普通深度雾与有限动态太阳可用；当前环境实机720p静止10秒平均144.02FPS，最终烘焙/音效/设置/稳定性尚未完成。|
| M7 | NOT_STARTED | Windows独立发布包及实机发布验收尚未完成。|

## 本轮交付与证据

- 竹丛/远山交付：`reports/validation/ENV_LANDSCAPE_DELIVERY_v002.md`。四组6秆竹丛，单组12,552三角面；背景3网格共108,000三角面，全部在可玩场界外且无碰撞。源BLEND、GLB与贴图保留，无外部模型输入。
- 6项环境检查headless/Mobile通过；24项M1回归、Mobile三线索→开门→步行终点通过。新截图`ENV_Landscape_v002_*.png`已查看，未覆盖旧阶段截图。
- 实机Mobile/Radeon/720p静止10.005455秒：平均144.021FPS，最低瞬时115.554FPS，最多70 draw calls。原始`ENV_Landscape_Profile_v002.json`保留，可能受同步上限影响，不能外推最终性能。
- 独立只读审查无Critical/Important；opacity测试的非零surface检查已补充并复跑。普通深度雾启用，高度/体积雾未启用。

## 之前的建筑与岩石阶段（历史记录）

- 当前建筑与岩石报告：`reports/validation/COURTYARD_DELIVERY_v002.md`，包含源BLEND/GLB、数据、实际命令、截图和边界。静态建筑61,752三角面/7网格组/5材质；岩石3499/3499/3500三角面，均无缺图。
- 门与终点随0.3m台基升高；可见踏步使用连续斜坡碰撞。`Courtyard_Rocks_mobile.log`8项检查、`Courtyard_Rocks_M1.log`24项、`Courtyard_Rocks_playthrough_mobile.log`完整无传送输入通关均通过，退出0。
- 当前实机720p静止10秒平均144.027FPS，最低瞬时111.757FPS；最多58 draw calls。原始`Courtyard_Rocks_Profile_v001.json`保留，不能代表最终美术负载。
- 独立只读代码审查未发现Critical/Important；资产来源、manifest、场景布局和状态已随交付更新。

## 之前的代理动作和构图准备（历史记录）

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

继续提高山体轮廓、竹叶/地表/建筑近景材质与照明，准备正式香炉统一参考并替换线索。青岚正式模型/骨骼及许可按M5生产；几何代理和金色线索仍TEMP。已认可的角色/木门和沿用的庭院方向无需重复索取。

FPS_NOT_MEASURED仅用于最终美术场景：灰盒、建筑/岩石及竹丛/远山阶段均已有真实GPU静止基线，最终庭院/照明负载、长期稳定性和Windows发布包尚未验收。
