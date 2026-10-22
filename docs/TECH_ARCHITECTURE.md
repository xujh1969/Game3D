# 技术架构

- `scenes/world/Courtyard_Blockout.tscn`：世界、碰撞边界、墙段/门、三项线索、终点、HUD。
- 当前世界保留入口名，实例化`CourtyardArchitecture.tscn`与`CourtyardNature.tscn`。前者使用ARCH_Courtyard_v002静态GLB和显式简化碰撞，后者为三种扫描岩石及简化盒体碰撞。原HallWallLeft/Right由实际立面与两侧横墙替代。
- `EnvironmentScenery.tscn`独立包含4组竹丛与3层远山；24根竹秆用窄柱碰撞，叶片无碰撞，远山无碰撞且全部位于可玩场界之外。生成脚本分别为`build_landscape.py`与`write_landscape_scene.py`。
- WorldEnvironment启用Mobile普通深度雾，密度.0035，高度贡献关闭；不使用体积雾。现有相机/输入/线索接口不变。
- 建筑石台基顶面Y=.3；双门根与终点随台基升高.3m。踏步采用宽3.8m的凸斜坡碰撞，避免为现有控制器增加跨阶系统；屋面凸形碰撞参与SpringArm遮挡。木门保持独立交互节点，未烘入静态建筑。
- `scenes/character/Qinglan_TEMP.tscn`：CharacterBody3D根节点、TEMP标签、SpringArm3D和Camera3D；Proxy实例为`QinglanProxy_TEMP.tscn`，包含几何身体、四肢支点和AnimationPlayer。
- `scripts/player/proxy_animation.gd`：运行时创建Idle/Walk/Run循环，按实际平面速度和奔跑输入选择，0.12秒混合；只改几何子节点，不移动物理根节点。无正式骨骼、脚底IK或服装。
- `scripts/player/player_controller.gd`：水平面相机相对移动；仅 Proxy 转向，相机与碰撞根节点不随人物朝向旋转。近距离/朝向筛选加物理射线遮挡检查得到焦点，E调用该焦点；可选InteractionPoint定义观察点，物理子节点被识别为同一交互对象。
- `scripts/player/third_person_camera.gd`：鼠标 yaw/pitch 和 SpringArm，排除玩家自身碰撞。Esc/鼠标模式由 HUD 统一管理。
- `scripts/gameplay/game_state.gd`：世界内状态节点，保存线索集合及解锁/胜利信号；重开解除暂停并重载当前场景。目前未设为 autoload，单场景闭环使用世界内节点。
- `scripts/interactables/clue.gd`：唯一拾取后退出交互组。
- clue增加`hide_on_collect`，默认true；石碑设false，读取后保留可见实体，仍移出交互组并关闭monitoring。卷轴InteractionPoint位于纸面，其木案是独立StaticBody，避免拾取后留下不可见碰撞。石碑Body为Area子节点，焦点射线可识别其归属。
- `scripts/interactables/door_controller.gd`：Door.tscn的Node3D根控制器，固定框体与左右StaticBody3D门扇。GLB中的LeafLeft/LeafRight在ready时挂到对应物理门轴；物理tween同步反向旋转±90°，保留碰撞，结束才标为打开。
- `scripts/interactables/finish_trigger.gd`：实际玩家/三线索/门已开且未胜利时触发一次；HUD 暂停并显示重开/退出。
- `scripts/ui/hud.gd`：计数、交互提示、暂时反馈、暂停/胜利菜单；always processing 允许暂停时响应按钮。
- `scenes/world/AssetTest.tscn`：模型尺度和材质审查，入口脚本 `scripts/debug/asset_test.gd`。
- `scripts/debug/debug_hud.gd`：开发版显示真实FPS、draw calls与渲染primitive计数；F3切换。release默认隐藏。primitive计数不等同于源模型三角形预算。
- `tools/godot/profile_graybox.gd`：图形后端静止出生点测量，预热2秒、采样10秒，输出原始JSON和截图；`-- --report-name=Courtyard_Rocks_Profile_v001`保留不同阶段记录，不覆盖原灰盒基线；不是最终场景性能验收。

测试入口：`tests/test_game_state.gd`（计数信号）、`tests/test_m1_runtime.gd`（实际场景行为）、`tests/test_playthrough.gd`（无传送输入路线）。详情与边界见 `reports/validation/M1_ACCEPTANCE_2026-10-22.md`。
