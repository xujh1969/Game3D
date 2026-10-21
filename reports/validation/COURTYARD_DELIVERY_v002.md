# 建筑与岩石首版交付

日期：2026-10-22。状态：PASS_WITH_LIMITATIONS。此处的“首版”是可继续精修的实际3D资产，尚未达到概念图最终视觉目标。

## 交付

- `assets/source/ARCH_Courtyard_v002.blend`：柱梁、搭接曲面瓦、墙窗、石台基、路径与围墙的可编辑构件及打包纹理。v001试制源保留，其斜向纹理问题已修正于v002。
- `assets/game/ARCH_Courtyard_v002_game.glb`：61,752三角面、7网格组、5材质；Godot外包围尺寸30.47×5.23×30.47m，含围墙外沿，庭院可玩范围仍30×30m。主建筑台基12×8m，Y=.3m，屋脊约5.15m。木门未包含在静态建筑里。
- 15张内嵌贴图：CC0木材3张1k图；项目生成的灰泥/瓦/石/地面各3张512图。Blender重新导入报告`ARCH_Courtyard_v002_import.json`确认缺失文件0。
- 三种`NAT_001_MossRock_00[1-3]_v001_game.glb`，分别3499/3499/3500三角面，每个1材质，3张1k PBR贴图。统一最长水平尺寸约1.8m，高约.785/.696/.938m。
- 岩石原始模型、贴图、API元数据与MD5在`assets/source/third_party/rock_moss_set_01/`；减面前BLEND在`assets/source/NAT_001_MossRocks_v001.blend`。来源为Poly Haven Rock Moss Set 01 / Kless Gyzen / CC0，见`docs/ASSET_LICENSES.md`。三份Blender重新导入报告`NAT_001_00[1-3]_import.json`均无缺图。

## 关卡接入

`CourtyardArchitecture.tscn`实例化静态建筑和显式碰撞；`CourtyardNature.tscn`布置三种岩石。原两堵整段灰盒墙替换为实际立面/端墙/横墙，双门根从Y=0升至.3m，终点升至1.3m。线索XZ位置不变。

可见两级踏步各.15m，使用宽3.8m连续斜坡碰撞，角色无需新跨阶系统。岩石采用贴近主体的简化盒体，屋面为两段凸碰撞，参与SpringArm遮挡。边界仍有防跌落。外观不含门的重复静态副本，门扇继续独立开合并保留碰撞。

## 实际验证

Godot路径使用本机4.7.2 console，Blender5.2.2 LTS。成功命令均实际运行并退出0：

```text
Blender --background --python-exit-code 1 --python tools/blender/build_courtyard.py
Blender --background --python-exit-code 1 --python tools/blender/prepare_rocks.py
Blender --background --python-exit-code 1 --python tools/blender/validate_import.py -- INPUT.glb REPORT.json
Godot --headless --path . --editor --import
Godot --path . --script res://tests/test_courtyard_architecture.gd
Godot --headless --path . --script res://tests/test_m1_runtime.gd
Godot --path . --script res://tests/test_playthrough.gd -- --capture-name=Courtyard_Rocks_Victory_v001
Godot --path . --script res://tools/godot/profile_graybox.gd -- --report-name=Courtyard_Rocks_Profile_v001
```

- `Courtyard_Rocks_mobile.log`：8项通过——实际建筑实例、门槛高度、上下阶、禁止侧绕、屋面遮挡、三种岩石实例、岩石独立物理碰撞。添加建筑前失败记录为`ARCH_Courtyard_before.log`。
- `Courtyard_Rocks_M1.log`：24项实际引擎行为检查通过。
- `Courtyard_Rocks_double_door.log`双门8项、`Courtyard_Rocks_proxy.log`代理动作10项headless追加回归均通过。
- `Courtyard_Rocks_playthrough_mobile.log`：AMD Radeon / Vulkan1.3.260 / Mobile，完整输入路线无传送，三线索→开门→步行终点PASS。先前建筑单独阶段headless/Mobile通关日志亦保留。
- `reports/screenshots/ARCH_Courtyard_v002_Entrance.png`、Hero、Porch为实际Godot场景渲染，已查看；审查相机暂时隐藏TEMP角色和HUD，场景中的金色线索仍可见。`Courtyard_Rocks_Victory_v001.png`是实际玩法通关帧，保留HUD，不能把审查机位称为默认玩家镜头。
- 三个岩石分别在`AssetTest.tscn`标准光照/1m标尺场景执行并截图，`NAT_001_AssetTest_00[1-3].log`退出0，`reports/screenshots/AssetTest_NAT_001_MossRock_00[1-3]_v001_game.png`已逐张查看。

## 实机性能

真实显卡AMD Radeon(TM) Graphics，Mobile，1280×720。静止出生点预热2秒、采样10.005068秒，共1441帧，全部聚焦。平均144.027007 FPS；最低瞬时111.756817 FPS（最慢单帧8.948ms的倒数）。最多58 draw calls、403438 rendered primitives。原始JSON/日志/截图均为`Courtyard_Rocks_Profile_v001`。

primitive计数包含引擎渲染与阴影等开销，不能作为资产源三角形总数。该读数使用process_frame墙钟间隔，不是GPU专用计时器；仅静止短样本。不能从它外推移动、长时稳定性或最终竹林/远山/雾/烘焙场景的30FPS验收。

## 审查与限制

独立只读代码审查未发现Critical/Important问题；提示的资产清单与阶段状态更新纳入本次交付。

当前PBR矿物材质仍为程序制作，近看细节、墙片接缝、屋面边缘和照明仍需精修；屋架为简化宋风创作，没有宣称按史料完成榫卯或斗拱复建。竹林、远山、薄雾、苔藓地表混合、正式香炉/卷轴/石碑、正式青岚及烘焙照明未完成。岩石是扫描资产的优化版本，非自制扫描。真人完整键鼠体验、脚底IK、服装和发布包未验收。
