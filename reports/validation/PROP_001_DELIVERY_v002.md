# 青铜香炉首版交付 v002

2026-10-22，PASS_WITH_LIMITATIONS。采用用户明确批准的参考方向，尚不是最终近景艺术验收。

## 文件与实际数据

- 源`assets/source/PROP_001_IncenseBurner_v002.blend`；运行`assets/game/PROP_001_IncenseBurner_v002_game.glb`；生成脚本`tools/blender/build_incense.py`。
- 实测尺寸.45×.35×.45m，底部原点Y=0；3,672三角面、4网格（器身+三足）、1材质。无盖无耳，开口厚唇、实壁与内底。
- 源BaseColor/Roughness/Metallic/Normal各1024px，项目程序生成并打包；glTF将Metallic/Roughness合并，运行内嵌3张1k图。重新导入报告`PROP_001_v002_import.json`缺图0。无外部模型或材质输入。
- v001源/GLB/截图保留。实际内腔图发现足顶进入炉底，v002将足顶降至.103m，低于内底.113m，修正穿插，同时增加表面粗糙度/降低抛光感。当前铜锈仍为程序纹理，非扫描材质，近景精度可继续提高。

## 接入与检查

保留ClueIncense根坐标(-5,.5,-4)及CLUE_003；Visual下移.5m落地，旋转60°展示双前足。子Body用半径.22m/高.35m实心圆柱作为简化碰撞，覆盖整个小物件，不模拟玩家进入内腔。InteractionPoint在炉身前侧；读取射线可识别同一Area的子Body。hide_on_collect=false，激活后保留实体/碰撞，退出交互组，重复不计数。金色球与材质资源已移除，三项线索都有实际模型。

成功命令均实际退出0（本机Godot4.7.2、Blender5.2.2）：

```text
Blender --background --python-exit-code 1 --python tools/blender/build_incense.py
Blender --background --python-exit-code 1 --python tests/blender_check_incense.py -- v002
Blender --background --python-exit-code 1 --python tools/blender/validate_import.py -- INPUT.glb REPORT.json
Godot --headless --path . --editor --import
Godot --path . --script res://tests/test_incense.gd
Godot --headless --path . --script res://tests/test_m1_runtime.gd
Godot --headless --path . --script res://tests/test_clue_props.gd
Godot --path . --script res://tests/test_playthrough.gd -- --capture-name=PROP_001_Victory_v002
Godot --path . --script res://tools/godot/profile_graybox.gd -- --report-name=PROP_001_Profile_v002
Godot --path . res://scenes/world/AssetTest.tscn -- --asset=res://assets/game/PROP_001_IncenseBurner_v002_game.glb --capture
```

- 源几何19项检查通过，包含闭合/外法线/UV、三足、足底接地、内腔射线、足顶与内底间隙、尺寸。`PROP_001_geometry_v002.json`；v001升级后的间隙检查失败（退出1），`PROP_001_feet_before.log`与`PROP_001_geometry_v001.json`保留。
- `PROP_001_v002_mobile.log`6项检查、`PROP_001_v002_M1.log`24项回归、`PROP_001_prior_props.log`9项旧道具检查通过。
- `PROP_001_v002_playthrough_mobile.log`实际AMD Radeon/Mobile完整无传送输入路线PASS：三线索→开门→步行终点。
- `PROP_001_v002_Front.png`与Interior为实际Godot近景，已查看；审查相机隐藏TEMP角色和HUD，不是默认玩家机位。通关帧为`PROP_001_Victory_v002.png`。
- AssetTest标准灯光/1m标尺场景运行退出0，截图`AssetTest_PROP_001_IncenseBurner_v002_game.png`已查看。离线脚本`render_incense.py`实际执行退出0，`PROP_001_v002_Studio.png`已查看，明确为Blender离线材质审查，不能作为游戏帧或FPS证据。
- 独立只读代码审查无Critical/Important及本范围需改Minor，未额外运行GPU任务。

## 当前实机静止基线

AMD Radeon(TM) Graphics / Vulkan1.3.260 / Mobile / 1280×720，预热2秒，采样10.012626秒，共1442帧全部聚焦。平均144.018163FPS、最低瞬时117.426022FPS（最慢8.516ms倒数），最多80 draw calls和572086 rendered primitives。原始JSON/日志/截图`PROP_001_Profile_v002`。

这是process_frame墙钟间隔，可能受同步上限影响；未测GPU忙碌时间/余量。primitive含渲染pass，与资产源面数不同；前后不同可见物体/剔除结果不能直接按该计数解释模型复杂度。静止短样本不代替移动、长稳、最终画质30FPS或Windows包验收。

## 限制

已完成首批三类试制资产的接入基线，不声称整个游戏或最终写实画面完成。铜锈颗粒/近景细节、庭院材质/远山/照明仍需精修；无烟火特效，正式青岚骨骼/服装/动作及发布包未完成。
