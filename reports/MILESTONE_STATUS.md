# MountainCourtyard 开发状态

更新：2026-10-23（Asia/Shanghai）。

用户范围更新：当前为Codex三维技术实验，取消三维资产版权/来源/商用许可提交和审核门槛，相关历史待办不再适用，记录见USER_TECH_EXPERIMENT_SCOPE_2026-10-22.md。

| 阶段 | 状态 | 当前结果 |
|---|---|---|
| M0 | PASS_WITH_LIMITATIONS | Godot4.7.2、Blender5.2.2 LTS和Python/Git可用；Mobile在AMD Radeon集显/Vulkan1.3.260实测运行；GitHub main与Git LFS同步。管理/源资产/报告目录排除Godot资源扫描。|
| M1 | PASS_WITH_LIMITATIONS | 青岚v006用户Idle/Walk/Run的21项检查、24项回归与Mobile无传送完整路线通过，开发F3性能HUD可用。真人体验与长期稳定性未验收。|
| M2 | PASS_WITH_LIMITATIONS | 初期方向/任务单/资产检查管线齐备；青岚/门/庭院方向沿用，香炉参考已明确批准。最终美术与正式角色仍需生产/验收。|
| M3 | PASS_WITH_LIMITATIONS | 首批木门、三种岩石、青铜香炉及卷轴/石碑已接入；香炉v002经19项几何、6项运行检查，24项M1及Mobile完整通关通过。材质质量限制保留。|
| M4 | IN_PROGRESS | 建筑v003地面/灰泥接入CC0照片PBR，315构件几何/变换保持一致，空间8项/回归24项及Mobile完整通关通过。竹丛/远山保持v002；平铺/山形/最终照明仍待精修。|
| M5 | IN_PROGRESS | 青岚v006已接入可玩庭院：用户新GLB的41根骨骼及Idle，合并Walking.fbx与Fast Run.fbx为Walk/Run；12899三角面、3张2K恢复贴图，约1.70m。21项动作检查、24项玩法回归和Mobile无传送完整通关通过。外观、动作自然程度、地形脚底贴合仍待用户体验与精修。|
| M6 | IN_PROGRESS | v003前两轮静止平均102.90/126.37FPS，有约218–221ms长帧；后续新旧对照均约144FPS且无>33.33ms帧。根因未知，原始记录保留，稳定性未验收；烘焙/音效/设置尚未完成。|
| M7 | NOT_STARTED | Windows独立发布包及实机发布验收尚未完成。|

## 本轮交付与证据

- 青岚v006已接入可玩庭院：用户新GLB的41根骨骼及Idle，合并Walking.fbx与Fast Run.fbx为Walk/Run；12899三角面、3张2K恢复贴图，约1.70m。21项动作检查、24项玩法回归和Mobile无传送完整通关通过。详见`reports/validation/CHAR_001_PLAYABLE_v006.md`。
- 本机720p Mobile静止10.003995秒平均144.042FPS，最慢9.197ms，p95 8.013ms，无>33.33ms帧；仅短时静止基线，历史偶发长帧未据此宣称解决。
- 原始用户文件、旧版源与失败记录保留。v004关节坐标问题在v005修复；用户不认可旧程序步态后，v006全部改用用户动作。9秒游戏录制位于builds/Qinglan_UserMotion_v006.avi。

## 之前的静态接收阶段（历史记录）

- 青岚接收报告`reports/validation/CHAR_001_INTAKE_v002.md`：原件SHA256记录，1.17m源规范至约1.70m；第一版直接减面失败保留。导入重复点焊接924398→749772并重算法线后再减面，v002视觉改善，仍不等同动画拓扑。
- v002实际Front/Left/Right/Back/Face均已查看；重导入缺图0，8项Mobile技术检查退出0。仅静态审查，未替换可玩TEMP，无新角色性能/动画验收声明。
- 用户明确取消三维资产版权/来源/商用许可要求，已同步AGENTS/MASTER_PLAN/任务单，不再为此请求或等待材料。

## 之前的材质阶段（历史记录）

- `reports/validation/SURFACE_UPGRADE_v003.md`：六张1k原图MD5核验；20对象材质/UV升级，315构件几何/变换一致；GLB保持61752三角面/7网格/5材质/15图，缺图0，v002保留。
- 空间8项、M1回归24项与Mobile无传送完整输入通关通过；Entrance/Hero/Porch/Ground四张实际Godot审查图已查看。
- 保留四轮性能JSON/日志/截图。首次与复测有长帧，后续新旧对照未复现；新增p95/p99与慢帧采样时间，未声称定位根因或修复。独立只读审查无Critical/Important。
- 单人A姿技术参考CHAR_REF_002已生成/保存/查看，沿用已认可青岚。该阶段曾等待角色输入；当前模型与三段动作已接入，许可门槛已取消；允许未绑定源，不索取账户密钥、不发起购买。

## 之前的香炉阶段（历史记录）

- 用户明确批准香炉方向，记录`handoff/approvals/USER_APPROVAL_Incense_2026-10-22.md`。现已制作PROP_001香炉v002，模型非TEMP；角色仍TEMP。
- `reports/validation/PROP_001_DELIVERY_v002.md`：.45×.35×.45m，3672三角面/4网格/1材质/3张内嵌1k图。源v001/v002与原始程序PBR图保留，重新导入缺图0。
- 几何19项、香炉运行6项、先前道具9项与M1回归24项通过，Mobile完整无传送输入通关通过。足顶穿插由实际近景发现，v001间隙检查失败、v002修复通过；原始记录保留。
- 实际Godot近景/标准灯光与Blender离线Studio图均已查看，准确区分来源。独立只读审查无Critical/Important。
- 静止基线`PROP_001_Profile_v002.json`：10.012626秒平均144.018FPS、最低瞬时117.426FPS、最多80draw calls；不代表最终画面性能。

## 之前的卷轴与石碑阶段（历史记录）

- `reports/validation/PROP_002_DELIVERY_v002.md`：卷轴2392面/木案972面/石碑812面，源BLEND与内嵌PBR GLB保留，重新导入缺图0。碑身法线v001有向体积检查失败、v002通过，两版源与日志保留。
- 卷轴拾取后隐藏但木案保留；石碑读取后保留实体且退出焦点组。9项道具检查、24项M1回归与Mobile无传送输入通关通过，均退出0。实际卷轴/石碑近景已查看。
- 当前静止基线`PROP_002_Profile_v002.json`：10.003252秒平均143.953FPS，最低瞬时102.281FPS，最多75 draw calls。短时静止不是最终画面验收。
- 香炉同板参考已生成、保存、查看：`handoff/approvals/INCENSE_REFERENCE_v001.md`，WAITING_FOR_USER；没有香炉3D交付声明。独立只读代码审查无Critical/Important。

## 之前的竹丛与远山阶段（历史记录）

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

继续根据实际游戏体验精修青岚表面、走跑衔接、衣摆与脚底贴合；用户模型及Idle/Walk/Run已接入，无需补交相同素材。山体/材质平铺/照明及偶发长帧调查仍为后续工作。

FPS_NOT_MEASURED仅用于最终美术场景：灰盒、建筑/岩石及竹丛/远山阶段均已有真实GPU静止基线，最终庭院/照明负载、长期稳定性和Windows发布包尚未验收。
