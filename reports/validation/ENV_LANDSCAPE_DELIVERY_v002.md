# 竹丛与远山环境首版

2026-10-22，PASS_WITH_LIMITATIONS。沿用ENV v002庭院方向；仍是制作中的可玩样板，未达到概念图最终写实质量。

## 资产与场景

- 源`assets/source/ENV_BambooLandscape_v002.blend`；脚本`tools/blender/build_landscape.py`。v001源、GLB和实际截图保留，v002焊接相邻顶点并提高山体采样，修正首版可见分面。
- `NAT_002_BambooClump_v002_game.glb`：一组6根竹，含竹节、细枝和弯曲披针形叶片；12,552三角面，1网格/5材质，3张512px竹秆PBR图。尺寸2.789×4.803×2.203m。
- `ENV_DistantMountains_v002_game.glb`：3层平滑背景山体，108,000三角面，3网格/3材质，9张512px PBR图。总尺寸310×57.375×160m，Godot Z=-34至-194m。尺寸表示背景外包围范围，可玩庭院仍30×30m；山体无碰撞、不可进入，不是新增可探索地图。
- 两类几何、纹理和参数材质均由项目制作，无外部模型/扫描输入。所有GLB贴图内嵌；Blender重新导入报告`NAT_002_v002_import.json`、`ENV_Mountains_v002_import.json`无缺失图。
- `EnvironmentScenery.tscn`布置4组竹丛：(-11,0,5)、(11,0,6)、(-11,0,-5)、(11.5,0,-5)。每组6个窄柱碰撞，叶片不挡人；碰撞为简化直柱，未逐段追踪竹秆细微倾斜。
- 竹叶为双面不透明几何，无透明混合卡片；当前没有风摆/LOD/季节变化。主光阴影距离仍限制45m，近景照明延续既有动态太阳。

## 雾与画面

主世界使用普通深度雾，fog_density=.0035，fog_height_density=0；高度贡献已关闭。没有使用Forward+专属体积雾，不宣称实现光束或局部体积云。依据[Godot渲染器说明](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)和[Environment API](https://docs.godotengine.org/en/4.6/classes/class_environment.html)，并在本机4.7.2 Mobile实际加载与渲染验证。

`reports/screenshots/ENV_Landscape_v002_Entrance.png`、Hero、Bamboo均实际Godot帧，已逐张查看。审查相机隐藏TEMP角色/HUD；不能称为默认玩家相机截图。`ENV_Landscape_v002_Victory.png`为实际通关帧。v001近景雾过浓，v002降低密度并关闭高度贡献。

## 实际验证

成功命令均实际执行、退出0：

```text
Blender --background --python-exit-code 1 --python tools/blender/build_landscape.py
python tools/python/write_landscape_scene.py
Blender --background --python-exit-code 1 --python tools/blender/validate_import.py -- INPUT.glb REPORT.json
Godot --headless --path . --editor --import
Godot --headless --path . --script res://tests/test_environment_scenery.gd
Godot --path . --script res://tests/test_environment_scenery.gd
Godot --headless --path . --script res://tests/test_m1_runtime.gd
Godot --path . --script res://tests/test_playthrough.gd -- --capture-name=ENV_Landscape_v002_Victory
Godot --path . --script res://tools/godot/profile_graybox.gd -- --report-name=ENV_Landscape_Profile_v002
```

环境6项检查通过，M1回归24项通过，Mobile无传送输入路线三线索→开门→终点PASS。日志前缀`ENV_Landscape_v002`；初始缺少环境实例的失败记录`ENV_Landscape_before.log`。独立只读审查未发现Critical/Important，指出不透明检查可能在没有网格时空通过，已补充非零surface条件并重新运行headless检查。

## 实机静止基线

AMD Radeon(TM) Graphics / Vulkan1.3.260 / Mobile，1280×720。预热2秒，采样10.005455秒，1441帧全部聚焦。平均144.021436FPS，最低瞬时115.553501FPS（最慢单帧8.654ms倒数）；最多70 draw calls、604942 rendered primitives。JSON/日志/截图为`ENV_Landscape_Profile_v002`。

方法为process_frame墙钟间隔，包含桌面和开发HUD开销；帧率可能受同步/刷新上限影响，未测GPU忙碌时间或性能余量。primitive包含渲染pass开销，不等于模型三角面总数。静止短样本不代表移动、长期稳定性或最终美术30FPS验收。

## 后续精修

竹叶层次/近景材质、山体自然轮廓与岩壁细节、地表苔藓混合、建筑接缝、烘焙照明仍需提高；没有声称山体已达照片级。主角与线索仍TEMP，正式香炉/卷轴/石碑和发布包未完成。
