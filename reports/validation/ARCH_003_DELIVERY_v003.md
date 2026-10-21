# ARCH_003 双扇木门 v003 交付与验收

日期：2026-10-22。状态：PASS_WITH_LIMITATIONS。依据用户已批准的 `PROP_REF_001_ArchDoorSong_sheet_v001.png` 制作，未修改该参考图。

## 文件与测量

- 源文件：`assets/source/ARCH_003_DoorSong_v003.blend`，包含可编辑模型、打包贴图和展示灯光/摄影机。
- 运行资产：`assets/game/ARCH_003_DoorSong_v003_game.glb`，约3.34MB；展示地面、摄影机和灯光未导出。Godot导入时自动提取的同前缀贴图也保留在game目录。
- 原点：门框中心地面；Godot Y-up；`LeafLeft` X=-1m、`LeafRight` X=+1m。
- 尺寸：框体整体 2.24m宽×2.66m高×0.186m深；门扇名义合计2m宽×2.5m高，实际门扇高度约2.48m。
- 3个网格组（框体、左扇、右扇），2个材质，7,740 triangles。
- 3张1024²内嵌PBR贴图：BaseColor、Roughness、OpenGL Normal；青铜使用金属度0.85、粗糙度0.48参数。缺失贴图0。
- v001和v002作为未采用试制稿保留在source/processed，未覆盖既有源文件。v001木纹偏平并有接合黑点，v002木纹规律性过强；v003修正接合并采用有许可的木材贴图。

## 来源

模型几何和制作脚本由本项目生成；木材地图使用Poly Haven的Fine Grained Wood，作者Rob Tuytel，CC0。来源 `https://polyhaven.com/a/fine_grained_wood`。未下载外部模型、未调用付费服务。

下载原文件、官方文件API返回的MD5校验和与来源保存在 `assets/source/third_party/fine_grained_wood/provenance.json`；复现下载用 `tools/python/fetch_door_textures.py`。整体资产来源另见 `docs/ASSET_LICENSES.md`。

## 已执行检查

1. `python tests/test_door_asset.py`：通过；确认GLB2、独立左右门轴、内嵌贴图、UV/法线、面数≤10k、没有展示摄影机、BLEND源文件存在。
2. Blender `validate_import.py`：报告 `ARCH_003_import_v003.json`，返回0，网格/贴图/尺寸检查通过。该通用脚本仍要求人工视觉/许可审查，本报告补充了实际来源及渲染审查。
3. Godot headless导入：通过，`ARCH_003_godot_import.log`。
4. `test_double_door.gd` 在Mobile/Vulkan/Radeon上运行：8项通过；确认左右视觉与物理轴一致、锁门不转、±90°向内开、门框不动、碰撞保留、重复触发不叠加。
5. `test_m1_runtime.gd`：24项引擎行为检查通过，`ARCH_003_M1_regression.log`，原线索/菜单/碰撞/通关功能未受破坏。
6. 无传送输入路线：headless与本机Mobile均通过，从出生点收三线索→E开门→穿过双门→到终点。日志 `ARCH_003_playthrough_v003.log`、`ARCH_003_playthrough_mobile_v003.log`。
7. AssetTest加载GLB并在Mobile下渲染，`ARCH_003_AssetTest.log`；尺度参照杆1m。调试信息改为屏幕叠层，避免高模型遮住文字；审查场景加少量环境补光，便于读取PBR材质。

以上各项成功执行的命令退出码均为0。最初的双门失败检查保存于 `ARCH_003_double_door_before.log`，当时仍是单扇灰盒。

## 实际画面

- `reports/screenshots/ARCH_003_DoorSong_v003_studio.png`：Blender展示渲染，正面3/4。
- `reports/screenshots/ARCH_003_DoorSong_v003_back.png`：Blender背面渲染。
- `reports/screenshots/ARCH_003_DoorSong_v003_game_closed.png` / `..._game_open.png`：Godot原关卡中的独立审查机位，关闭/打开，非合成效果图。
- `reports/screenshots/AssetTest_ARCH_003_DoorSong_v003_game.png`：标准资产场景实际帧。
- `reports/screenshots/ARCH_003_Playthrough_v003.png`：真实引擎输入路线完成后的通关帧。

已逐张查看正面、背面、Godot开/关门及AssetTest渲染。截图未加工。

## 限制与后续

木色会随灯光改变；当前展示图比参考图偏浅，灰盒关卡照明偏暗，整体写实场景照明留待M4/M6。青铜目前是基础PBR材质，没有专门氧化贴图；细节可在近景艺术迭代中加强。本模型为宋风创作，不宣称考古复建。

本轮确认了自动引擎流程，未补做真人键鼠通关和持续FPS采样；FPS_NOT_MEASURED。庭院、角色、其他道具仍为TEMP或尚未生产，不能据此宣称完成游戏或通过最终艺术验收。
