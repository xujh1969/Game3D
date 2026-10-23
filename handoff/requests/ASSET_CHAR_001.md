# CHAR_001 — 正式青岚角色生产交接

状态：IN_PROGRESS。2026-10-23：青岚v006已接入可玩庭院：用户新GLB的41根骨骼及Idle，合并Walking.fbx与Fast Run.fbx为Walk/Run；12899三角面、3张2K恢复贴图，约1.70m。21项动作检查、24项玩法回归和Mobile无传送完整通关通过。无需重复提交。报告：`reports/validation/CHAR_001_PLAYABLE_v006.md`。

用户已明确将本项目限定为Codex三维技术实验，取消此前版权、来源及商用许可资料和审核要求。下列历史交接步骤中的此类要求不再适用；不再以此阻断开发。范围记录：`handoff/approvals/USER_TECH_EXPERIMENT_SCOPE_2026-10-22.md`。

## 已完成的原始模型交接（历史步骤）

请把模型放入项目：

`C:/Users/AYOU/Desktop/MountainCourtyard/handoff/incoming/CHAR_001_Qinglan_v001_source.glb`

若平台只能导出FBX，用同目录`CHAR_001_Qinglan_v001_source.fbx`，贴图放同名文件夹`CHAR_001_Qinglan_v001_textures/`。**当前GLB已收到，不需重交。** 第一阶段允许未绑定A姿模型，后续由Codex检查和安排绑定，不让用户反复生成已有外形。

## 可直接使用的参考

- 单人正面生产姿态：`handoff/reference/generated/CHAR_REF_002_Qinglan_ProductionFront_v001.png`。已按原设计生成、保存并查看；手臂与身体分开，便于建模。
- 新增独立左侧/右侧/背面参考：同目录`CHAR_REF_002_Qinglan_ProductionLeft_v001.png`、`CHAR_REF_002_Qinglan_ProductionRight_v001.png`、`CHAR_REF_002_Qinglan_ProductionBack_v002.png`。对应方向与可点选文件见`handoff/reference/generated/QINGLAN_PRODUCTION_VIEWS.md`。
- 已认可设计主依据：`handoff/reference/generated/CHAR_REF_001_Qinglan_Turnaround_sheet_v001.png`。旧同板包侧存在不一致，生产以正面和新增独立图为准：行囊在人物自身左胯，肩带从右肩到左胯；不要使用Back_DRAFT_v001。
- 新图是技术姿态辅助，不替代原设计，也不是已完成的3D模型。若单图输入，只上传Front；若工具支持多视图，分别指定Front/Left/Right/Back v002四张，不把同板当单人输入。独立AI图存在局部衣褶/轮廓差异，不宣称精确几何一致。

## 推荐操作

1. 打开[Tripo图片转3D](https://www.tripo3d.ai/zh/features/image-to-3d-model)，用你自己的账户；也可使用你已有且许可明确的同类平台。该官方页面目前列有图片生成、绑定与GLB/FBX导出，但实际按钮/额度以登录后的界面为准，不保证生成质量。
2. 上传单人正面参考，输入下方提示词；目标是一位完整青岚，而非场景、雕像或四个人物。
3. 检查脸部、发髻、衣层、包带、手指和双腿是否分开。优先保留原始高质量源，不必为了面数目标把脸部减坏；运行目标15k–30k三角面、1k/2k PBR，我收到后可整理优化。
4. 若现有功能可直接绑定人体骨骼，可导出绑定版；动作希望为Idle/Walk/Run且原地循环。不具备绑定时先导出未绑定A姿版本，不购买/升级套餐来满足本单；额度或导出受限就告知具体限制。
5. 导出GLB（优先，含贴图）或FBX+贴图，按上面文件名放好，回复“青岚素材已放好，继续”。本项已完成。

## 可复制提示词

One single photorealistic young East Asian woman traveler, match the supplied approved Qinglan reference exactly: same face and topknot, muted blue-gray linen Song-inspired layered tunic, pale undersleeves, brown wrapped belt and crossed satchel strap, brown side satchel, loose dark trousers, wrapped worn boots. Full body in relaxed symmetric A-pose, separate hands and fingers, legs separated naturally, believable anatomy, about1.70m tall. Game character with clean deformable topology, complete underside, PBR base color roughness normal, neutral textures without baked directional shadows. Preserve the side/back costume design from the approved sheet. One character only; no weapons, armor, fantasy ornaments, ground, pedestal, environment or extra bodies. Skeleton/rig when available; otherwise keep clean A-pose geometry for later rigging.

## 我收到后负责

保留原文件，Blender检查尺寸、网格、材质/缺图和骨骼；复核已认可外观；处理原点/朝向/减面与贴图；验证或补齐Idle/Walk/Run，再接入现有CharacterBody控制与相机。外观问题只提具体修正项；版权/来源/商用许可不再是实验门槛。

## 最低验收与替代

仅一个全身人物，无底座/摄影台，服装/五官与参考一致，手脚不粘连，脸部没有明显破面；贴图随文件保存。不要提交账号密码或API密钥。

如生成平台不能得到合格人物，可提供已有源模型/委托建模结果，继续沿用已认可设计；当前TEMP只用于玩法，不替代骨骼动画的技术检查。
