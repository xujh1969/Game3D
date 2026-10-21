# REQUESTS

更新：2026-10-22。青岚与木门视觉方向已获用户认可，庭院参考尚未取得输出；审核证据，见 `handoff/approvals/ART_DIRECTION_v001.md`。不用重新生成已有角色/木门图。

## 图像任务
- IMAGE_CHAR_REF_001_Qinglan_Turnaround — PASS：2026-10-22用户已认可转面同板 `handoff/reference/generated/CHAR_REF_001_Qinglan_Turnaround_sheet_v001.png`。
- IMAGE_PROP_REF_001_ArchDoorSong — PASS：2026-10-22用户已认可正/侧/背/局部同板 `handoff/reference/generated/PROP_REF_001_ArchDoorSong_sheet_v001.png`。
- IMAGE_ENV_REF_001_MainCourtyardHero — BLOCKED_TOOL：图像调用长时间未返回，本轮已停止等待；没有获得庭院图文件。提示词已保留，后续重试；已有角色与门视觉方向已批准。

## 后续三维资产（先确认图像，暂不请用户同时生成模型）
- ASSET_ARCH_003 — PASS_WITH_LIMITATIONS：v003已由Blender制作并接入Godot；独立双门开合、碰撞与通关检查通过。报告 reports/validation/ARCH_003_DELIVERY_v003.md。
- ASSET_NAT_001 — NOT_STARTED：任务单已备好，待庭院视觉方向统一。
- ASSET_PROP_001 — NOT_STARTED：任务单已备好，待庭院视觉方向统一及物件参考。

生成提示词原文：`handoff/reference/generated/PROMPTS_v001.md`。对应 IMAGE/ASSET 任务单原路径不变；本索引的状态优先于任务单里的初始待办状态。
