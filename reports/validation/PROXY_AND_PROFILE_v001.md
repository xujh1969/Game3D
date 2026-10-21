# TEMP动作与灰盒性能记录

日期：2026-10-22。状态：PASS_WITH_LIMITATIONS。

## 改动及检查

`QinglanProxy_TEMP.tscn`提供几何躯干、头部、四肢和AnimationPlayer。Idle呼吸、Walk/Run摆动按实际水平速度切换，混合0.12秒；CharacterBody、相机和交互接口保留。

实际执行Godot 4.7.2 console，`--path . --script res://tests/test_proxy_animation.gd`，分别带/不带`--headless`。两次均退出0，10项检查通过（命名动作、静止、行走、肢体变化、奔跑、速度、暂停、恢复、物理接地）。原始日志：`TEMP_proxy_animation_headless.log`、`TEMP_proxy_animation_mobile.log`；修改前缺少AnimationPlayer的失败记录保存在`TEMP_proxy_animation_before.log`。

回归：`--headless --path . --script res://tests/test_m1_runtime.gd`，24项通过；`--headless --path . --script res://tests/test_playthrough.gd`，三线索→开门→步行终点PASS。对应`TEMP_proxy_M1_regression.log`、`TEMP_proxy_playthrough.log`，均退出0。本轮动作图形检查使用实际AMD Radeon / Mobile后端；完整路线本轮为headless，前轮木门Mobile通关证据仍保留。

图像：`reports/screenshots/TEMP_Proxy_Idle_v001.png`、Walk、Run，均实际Godot帧并已查看。它们是TEMP几何代理，无正式青岚身体/骨骼/衣服/脚底IK；物理胶囊接地不代表逐帧脚掌贴地或衣服穿模验收。

## 性能基线

实际运行`--path . --script res://tools/godot/profile_graybox.gd`，退出0；显卡AMD Radeon(TM) Graphics，Mobile/Vulkan1.3.260，1280×720。2秒预热后静止采样10.005424秒，共1441帧，全部窗口聚焦。

平均144.021883 FPS；最低瞬时100.070049 FPS（最慢单帧9.993ms的倒数）；最多28 draw calls、40904 rendered primitives。原始JSON为`Graybox_Profile_v001.json`，另存日志和截图。计数来自实际引擎Performance monitor，primitive不是离线源资产三角形总数。

开发HUD的F3显示切换由探针直接传入InputEventKey检查通过，未宣称真人实按。`debug_hud_before.log`是添加HUD前的失败探针，临时探针脚本已移除。

测量包含开发HUD和桌面环境开销，仅静止出生点与TEMP角色/已接入木门。没有移动场景统计、长时稳定性或最终建筑/植被/雾/照明负载；不能据此判定最终720p 30FPS目标已通过。发布版隐藏HUD的代码条件已实现，尚未导出release实测。
