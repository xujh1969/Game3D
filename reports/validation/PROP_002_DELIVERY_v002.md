# 卷轴、低木案与石碑首版交付

2026-10-22，PASS_WITH_LIMITATIONS。不是最终近景美术验收；香炉仍为TEMP。

## 实际资产

源文件`assets/source/PROP_002_ClueSet_v002.blend`，脚本`tools/blender/build_clue_props.py`；v001源与GLB保留，v002修正石碑碑身朝内法线。

| GLB（assets/game/） | 三角面 | 材质/贴图 | Godot尺寸XYZ m |
|---|---:|---|---|
| PROP_002_Scroll_v002_game.glb | 2392 | 3材质/9图，木材1k及纸/布512 | .632×.052×.465 |
| PROP_002_ScrollStand_v002_game.glb | 972 | 1材质/3张1k图 | .95×.70×.62 |
| PROP_002_StoneTablet_v002_game.glb | 812 | 1材质/3张512图 | .90×1.34×.46 |

均为1网格，贴图内嵌，Blender重新导入报告`PROP_002_{Scroll,Stand,Tablet}_v002_import.json`缺失文件0。木材复用已核验Poly Haven Fine Grained Wood CC0；其余几何/纸/石/布PBR由项目脚本制作。源PNG在`assets/source/materials/ClueProps_v002/`。

卷轴有实体纸面起伏、厚度、卷端与轴杆；木案有案面、腿和横枨。石碑含基座、碑身与边框，文字由Godot贴面Label3D呈现，当前不是几何刻字或材质烘焙。原创短句“山居记”“听竹 / 观石”不作为历史文献引用，未复制或分发外部字体文件。

## 互动接入

ClueScroll/ClueTablet的既有坐标、clue_id不变。卷轴Visual放在独立木案上，InteractionPoint抬至纸面，避免读取射线被案面挡住；拾取后卷轴/文字隐藏，木案视觉与碰撞均保留。石碑Body为其Area的子节点，读取射线命中可被识别为同一交互对象；hide_on_collect=false使读取后保留实体，移出交互组并关闭monitoring，重复读取不计数。默认拾取行为不变，重启重载世界恢复初始状态。

## 真实验证

本机Godot4.7.2、Blender5.2.2。成功命令实际退出0：

```text
Blender --background --python-exit-code 1 --python tools/blender/build_clue_props.py
Blender --background --python-exit-code 1 --python tests/blender_check_tablet_normals.py -- v002
Blender --background --python-exit-code 1 --python tools/blender/validate_import.py -- INPUT.glb REPORT.json
Godot --headless --path . --editor --import
Godot --path . --script res://tests/test_clue_props.gd
Godot --headless --path . --script res://tests/test_m1_runtime.gd
Godot --path . --script res://tests/test_playthrough.gd -- --capture-name=PROP_002_v002_Victory
Godot --path . --script res://tools/godot/profile_graybox.gd -- --report-name=PROP_002_Profile_v002
```

- `PROP_002_v002_mobile.log`9项道具检查、`PROP_002_v002_M1.log`24项回归、`PROP_002_v002_playthrough_mobile.log`真实AMD Radeon/Mobile无传送输入通关均通过。
- 修改前缺少模型的失败日志`PROP_002_before.log`。闭合碑身有向体积检查v001=-.166229595（退出1）、v002=+.166229595（退出0），日志`PROP_002_normals_before/after.log`真实保留。
- 实际近景`reports/screenshots/PROP_002_v002_Scroll.png`与Tablet已查看；审查相机隐藏TEMP主角和HUD，不能作为默认玩家相机截图。通关帧`PROP_002_v002_Victory.png`保留HUD。
- 独立只读审查未发现Critical/Important或本范围需改的Minor问题，未运行额外GPU任务。

## 实机静止基线与限制

AMD Radeon(TM) Graphics / Vulkan1.3.260 / Mobile / 1280×720。预热2秒、采样10.003252秒，1440帧全部聚焦；平均143.953186FPS，最低瞬时102.280863FPS（最慢9.777ms倒数），最多75 draw calls、635607 rendered primitives。原始JSON/日志/截图为`PROP_002_Profile_v002`，含明确clue_visuals字段。

这是process_frame墙钟间隔，含开发HUD/桌面开销，可能受同步上限影响，不测GPU余量；primitive含渲染pass，非资产源面数。短时静止样本不能替代移动/长期/最终画面30FPS验收。

石碑文字字体/边框、纸张纤维和近景磨损仍需精修；石碑/木案使用简化盒体碰撞。香炉只有新生成2D参考，尚无正式模型，待`handoff/approvals/INCENSE_REFERENCE_v001.md`外观审核；正式青岚、烘焙/音效和发布包未完成。
