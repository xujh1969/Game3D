# REQUESTS

更新：2026-10-22。青岚与木门视觉方向已获用户认可；庭院概念提交后用户指示继续，已接入建筑v002和岩石首版。方向记录见`handoff/approvals/COURTYARD_DIRECTION_CONTINUE_2026-10-22.md`，实际交付见`reports/validation/COURTYARD_DELIVERY_v002.md`。不用重新生成已有参考与岩石。

## 图像任务
- IMAGE_PROP_REF_002_IncenseBurner — WAITING_FOR_USER：同板三视图/3/4参考已生成并查看；仅请审核造型/锈色，见`handoff/approvals/INCENSE_REFERENCE_v001.md`。无需重新生成图片。
- IMAGE_CHAR_REF_001_Qinglan_Turnaround — PASS：2026-10-22用户已认可转面同板 `handoff/reference/generated/CHAR_REF_001_Qinglan_Turnaround_sheet_v001.png`。
- IMAGE_PROP_REF_001_ArchDoorSong — PASS：2026-10-22用户已认可正/侧/背/局部同板 `handoff/reference/generated/PROP_REF_001_ArchDoorSong_sheet_v001.png`。
- IMAGE_ENV_REF_001_MainCourtyardHero — PASS_WITH_LIMITATIONS：两张v002概念与尺度草案提交后，用户回复“继续开发”，沿用方向推进，记录见COURTYARD_DIRECTION_CONTINUE_2026-10-22.md；最终场景外观尚未验收。

## 后续三维资产（先确认图像，暂不请用户同时生成模型）
- ASSET_ARCH_003 — PASS_WITH_LIMITATIONS：v003已由Blender制作并接入Godot；独立双门开合、碰撞与通关检查通过。报告 reports/validation/ARCH_003_DELIVERY_v003.md。
- ASSET_NAT_001 — PASS_WITH_LIMITATIONS：三种CC0扫描岩石已整理并接入；来源、减面数据和真实场景检查见COURTYARD_DELIVERY_v002.md，无需用户另行生成。
- ASSET_NAT_002 / ENV_MOUNTAINS — PASS_WITH_LIMITATIONS：项目制作的竹丛/远山v002已接入，来源/验证/不足见ENV_LANDSCAPE_DELIVERY_v002.md；无需用户提供同类占位资产。
- ASSET_PROP_001 — WAITING_FOR_USER：参考图已就绪，外观确认后制作模型；当前游戏香炉仍TEMP。
- ASSET_PROP_002 — PASS_WITH_LIMITATIONS：卷轴/低木案/石碑v002已接入；9项道具检查、M1回归与Mobile通关通过，见PROP_002_DELIVERY_v002.md。

生成提示词原文：`handoff/reference/generated/PROMPTS_v001.md`。对应 IMAGE/ASSET 任务单原路径不变；本索引的状态优先于任务单里的初始待办状态。
