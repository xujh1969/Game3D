# 资产来源与许可

## ARCH_003_DoorSong_v003

- 设计依据：用户已批准的项目生成木门参考图，批准记录 `handoff/approvals/USER_APPROVAL_2026-10-22_Qinglan_Door_v001.md`。
- 模型几何：本项目Blender脚本 `tools/blender/build_door.py` 制作；无外部模型输入。
- 木材BaseColor / Roughness / OpenGL Normal：Poly Haven **Fine Grained Wood**，作者 **Rob Tuytel**，资产页明确标注 **CC0**。来源：[资产页](https://polyhaven.com/a/fine_grained_wood)。
- 源贴图保留于 `assets/source/third_party/fine_grained_wood/`；`provenance.json` 记录原URL、日期与MD5；下载脚本核对MD5后才写入。
- 运行GLB嵌入贴图，Godot可能生成提取后的运行PNG。青铜为项目设置的基础PBR参数，未使用外部金属贴图。

## TEMP管线立方体

`tests/create_asset_fixture.py` 本项目生成，仅用于技术验证，不是正式艺术资产。
