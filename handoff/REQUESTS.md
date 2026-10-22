# REQUESTS

更新：2026-10-22。青岚与木门视觉方向已获用户认可；庭院概念提交后用户指示继续，已接入建筑v002和岩石首版。方向记录见`handoff/approvals/COURTYARD_DIRECTION_CONTINUE_2026-10-22.md`，实际交付见`reports/validation/COURTYARD_DELIVERY_v002.md`。不用重新生成已有参考与岩石。

## 图像任务
- IMAGE_PROP_REF_002_IncenseBurner — PASS：用户明确回复“香炉方向认可，继续”；批准记录USER_APPROVAL_Incense_2026-10-22.md，已有图像无需重复生成/审核。
- IMAGE_CHAR_REF_001_Qinglan_Turnaround — PASS：2026-10-22用户已认可转面同板 `handoff/reference/generated/CHAR_REF_001_Qinglan_Turnaround_sheet_v001.png`。
- IMAGE_PROP_REF_001_ArchDoorSong — PASS：2026-10-22用户已认可正/侧/背/局部同板 `handoff/reference/generated/PROP_REF_001_ArchDoorSong_sheet_v001.png`。
- IMAGE_ENV_REF_001_MainCourtyardHero — PASS_WITH_LIMITATIONS：两张v002概念与尺度草案提交后，用户回复“继续开发”，沿用方向推进，记录见COURTYARD_DIRECTION_CONTINUE_2026-10-22.md；最终场景外观尚未验收。

- CHAR_REF_002_Qinglan_ProductionFront — PASS_WITH_LIMITATIONS：从已认可转面图生成并查看单人A姿技术辅助图，提示词保留；非3D交付，不替代原设计、不重复索取认可。

## 后续三维资产
- ASSET_CHAR_001 — WAITING_FOR_USER：按MASTER_PLAN M5/HUMAN GATE #1交接正式角色源；步骤见`handoff/requests/ASSET_CHAR_001.md`。请放入`handoff/incoming/CHAR_001_Qinglan_v001_source.glb`及`CHAR_001_LICENSE.md`；FBX+贴图可替代，允许先交未绑定A姿，收到后再检查/安排绑定。不购买或升级套餐。
- ASSET_ARCH_003 — PASS_WITH_LIMITATIONS：v003已由Blender制作并接入Godot；独立双门开合、碰撞与通关检查通过。报告 reports/validation/ARCH_003_DELIVERY_v003.md。
- ASSET_NAT_001 — PASS_WITH_LIMITATIONS：三种CC0扫描岩石已整理并接入；来源、减面数据和真实场景检查见COURTYARD_DELIVERY_v002.md，无需用户另行生成。
- ASSET_NAT_002 / ENV_MOUNTAINS — PASS_WITH_LIMITATIONS：项目制作的竹丛/远山v002已接入，来源/验证/不足见ENV_LANDSCAPE_DELIVERY_v002.md；无需用户提供同类占位资产。
- ASSET_PROP_001 — PASS_WITH_LIMITATIONS：源BLEND与PBR GLB v002已接入，19项几何/6项运行检查及Mobile通关通过；见PROP_001_DELIVERY_v002.md。
- ASSET_PROP_002 — PASS_WITH_LIMITATIONS：卷轴/低木案/石碑v002已接入；9项道具检查、M1回归与Mobile通关通过，见PROP_002_DELIVERY_v002.md。
- ARCH_COURTYARD_SURFACES — PASS_WITH_LIMITATIONS：v003仅替换地面/灰泥为CC0 PBR，源315构件几何不变；交付/未解释长帧记录见SURFACE_UPGRADE_v003.md。

生成提示词原文：`handoff/reference/generated/PROMPTS_v001.md`。对应 IMAGE/ASSET 任务单原路径不变；本索引的状态优先于任务单里的初始待办状态。
