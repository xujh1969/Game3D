# 资产来源与许可

## ARCH_003_DoorSong_v003

- 设计依据：用户已批准的项目生成木门参考图，批准记录 `handoff/approvals/USER_APPROVAL_2026-10-22_Qinglan_Door_v001.md`。
- 模型几何：本项目Blender脚本 `tools/blender/build_door.py` 制作；无外部模型输入。
- 木材BaseColor / Roughness / OpenGL Normal：Poly Haven **Fine Grained Wood**，作者 **Rob Tuytel**，资产页明确标注 **CC0**。来源：[资产页](https://polyhaven.com/a/fine_grained_wood)。
- 源贴图保留于 `assets/source/third_party/fine_grained_wood/`；`provenance.json` 记录原URL、日期与MD5；下载脚本核对MD5后才写入。
- 运行GLB嵌入贴图，Godot可能生成提取后的运行PNG。青铜为项目设置的基础PBR参数，未使用外部金属贴图。

## ARCH_Courtyard_v002（保留v001材质试制版）

- 柱梁、曲面搭接瓦、墙窗、石台基、路径和围墙：本项目Blender脚本`tools/blender/build_courtyard.py`制作。是简化屋架的宋风创作，不是历史建筑复建。
- 木材复用上述Poly Haven Fine Grained Wood CC0贴图；地面、石材、灰泥和灰瓦的BaseColor/Roughness/Normal由项目脚本生成，源PNG在`assets/source/materials/Courtyard_v002/`。
- BLEND源保留可编辑构件与打包纹理；GLB导出时按7组批处理。v001条纹材质问题已修正于v002，两版源文件均保留。

## NAT_001_MossRock_001–003_v001

- 原模型与PBR贴图：[Poly Haven Rock Moss Set 01](https://polyhaven.com/a/rock_moss_set_01)，作者Kless Gyzen，资产页明确标注CC0；[站点许可](https://polyhaven.com/license)允许商业使用与再分发。
- 原始glTF、BIN、3张1k贴图、API元数据与下载MD5记录在`assets/source/third_party/rock_moss_set_01/`。`tools/python/fetch_rock_source.py`逐文件验证校验值。
- `tools/blender/prepare_rocks.py`选前三个原网格，统一最长水平尺寸约1.8m、底部原点；BLEND保留减面前网格。运行GLB每个约3500三角面，贴图内嵌，无外部平台生成声明。
- Powered by Poly Haven — https://polyhaven.com 。公共API仅用于离线素材准备，游戏运行不联网；原模型/贴图按CC0使用，不把API服务器代码许可证套用到资产。

## NAT_002竹丛 / ENV_DistantMountains v002

- 模型、纹理及参数材质均由项目脚本`tools/blender/build_landscape.py`制作，无外部模型或扫描输入。依据项目既有庭院概念方向。
- 竹秆与山体使用项目生成的512px BaseColor/Roughness/Normal；源图位于`assets/source/materials/BambooLandscape_v002/`；竹叶为不透明参数材质，未使用外部照片或透明卡片。
- 源文件`assets/source/ENV_BambooLandscape_v002.blend`包含完整几何与打包贴图；v001试制源保留。运行输出`NAT_002_BambooClump_v002_game.glb`和`ENV_DistantMountains_v002_game.glb`。
- 山体是不可进入的背景艺术网格，不是地理扫描，也没有声称真实地貌复原。

## PROP_002卷轴 / 木案 / 石碑 v002

- 几何为项目脚本`tools/blender/build_clue_props.py`制作，纸/石/布PBR同样为项目生成；木材复用前述Poly Haven Fine Grained Wood CC0源图。
- 源`PROP_002_ClueSet_v002.blend`与`assets/source/materials/ClueProps_v002/`保留；v001法线试制源保留。三个运行GLB不包含字体文件。
- 场景贴面文字“山居记”“听竹 / 观石”为项目原创，通过Godot默认文字系统呈现，未宣称历史铭文或几何雕刻。
- 香炉`PROP_REF_002_IncenseBurner_sheet_v001.png`由内置image_gen生成，仅供外观审核；不是外部扫描/已批准3D模型。

## TEMP管线立方体原始说明

`tests/create_asset_fixture.py` 本项目生成，仅用于技术验证，不是正式艺术资产。
