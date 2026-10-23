# 青岚用户骨骼动作接入 v006

2026-10-23 / PASS_WITH_LIMITATIONS。用户替换的新GLB包含Idle，Walking.fbx和Fast Run.fbx已合并进入实际庭院。没有重新制作程序步态。版权/来源/商用许可资料按用户实验范围不要求。

## 文件与处理

- 用户源：handoff/incoming/CHAR_001_Qinglan_v001_source.glb、Walking.fbx、Fast Run.fbx；原文件不改。旧高精源另有用户备份source-0.glb，历史源保留。
- 输出：assets/source/CHAR_001_Qinglan_v006_user_motion.blend、assets/game/CHAR_001_Qinglan_v006_game.glb。
- 41根骨骼，父子关系相同，rest矩阵最大误差0.0000398755；保留用户绑定/权重，独立检查权重差最大1.2e-7（浮点误差）。1网格、12899三角面、1材质、3张2048²内嵌PBR，重导入缺图0。
- 用户新GLB没有UV、材质或图像。从保留v002源对齐并投射BaseColor/Roughness/Normal，另建UV；不是用户新文件原有贴图。脸部/头发/衣物局部投射仍需精修。
- Idle原姿高1.48339m，均匀缩放1.14602278规范到约1.70m、脚底原点。模型视觉转Y轴180度适配既有控制器。
- Hips水平位移固定为Idle起始值，保留垂直重心运动；其他骨骼使用用户动作。Idle/Walk/Run源时长1.9/1.4/0.533333秒；GLB输出含末采样帧，实际为1.933333/1.433333/0.566667秒。Qinglan_UserMotion_v006.json的clips字段指源时长。
- 步行1.0m/s、奔跑4.9m/s近似匹配步幅；切换混合0.18秒，走跑切换保留归一化相位。不是精确步幅标定或地形脚底IK。

## 实际执行与证据

使用本机Godot4.7.2与Blender5.2；成功命令退出0：

```text
Blender --background --python tools/blender/merge_user_qinglan_motion.py
Godot --path . --script res://tests/test_qinglan_playable.gd
Godot --headless --path . --script res://tests/test_m1_runtime.gd
Godot --path . --script res://tests/test_playthrough.gd
Godot --path . --script res://tools/godot/profile_graybox.gd -- --report-name=Qinglan_Profile_v006
Godot --path . --write-movie builds/Qinglan_UserMotion_v006.avi --fixed-fps 30 --script res://tools/godot/capture_qinglan_motion.gd
```

- Qinglan_Playable_Mobile_v006.log：21项通过；41骨骼/三动作/实际键输入切换/暂停/站立微动作/膝肘弯曲/朝向及落地检查。每动作33姿态关节连续性最大间隙0，原始数值Qinglan_Playable_v006_Motion.json。
- Qinglan_M1_v006.log：24项通过。慢速步行的位移阈值与过门等待按实际速度计算，目标未缩减。
- Qinglan_Playthrough_Mobile_v006.log：三线索→开门→实际步行终点PASS，未传送；终点坐标约(-0.001445,0.300792,-11.68006)。
- Qinglan_Reimport_v006.json、Qinglan_UserMotion_Inspection_2026-10-23.json、Qinglan_UserMotion_v006.json保存导入、骨架与源SHA256，原日志保留。
- 已查看实际Godot Idle/Walk/Run/PlayerCamera截图，reports/screenshots/Qinglan_Playable_v006_*.png；通关图Qinglan_Playthrough_Victory_v006.png。
- 9秒实际引擎MovieMaker录制：builds/Qinglan_UserMotion_v006.avi（270帧/30fps；2秒Idle、3秒Walk、2秒Run、2秒Idle）。录制为离线固定帧率输出，实际耗时20秒，不能据视频帧率宣称运行性能。
- 实际Radeon Mobile/1280×720静止基线：预热2秒、采样10.003995秒/1441帧，平均144.042FPS、最慢9.197ms、p95 8.013ms、p99 8.483ms，0帧>33.33ms，最多67draw calls。Qinglan_Profile_v006.json/.log保留；静止短测不能替代长期稳定性/最终性能验收。

## 历史问题与当前边界

v004程序骨架曾误用父级相对向量作为世界方向，关节连续性失败最大0.56308m；v005修复并通过，但用户仍不认可步态。以上版本与失败日志保留，当前v006改用用户骨架及动作。TEMP代理也保留为回退，不作为当前角色。

本轮没有布料模拟、脚底地形IK、脸部表情或转向专用动作。衣摆穿插、脚底滑动和贴图局部仍待游戏体验精修。自动检查与截图不代表用户已认可动作自然程度，也不代表真人键鼠完整通关或长期稳定性验收。
