# CHAR_001 — 正式青岚角色生产交接

状态：WAITING_FOR_USER。MASTER_PLAN.md的M5及素材HUMAN GATE #1：当前没有正式角色文件，也没有已连接的角色生成/绑定服务或用户平台账户。已认可的人物设计不重新审批；TEMP几何人偶仍保留可玩。

## 本次只需提供一份原始角色模型

请把模型放入项目：

`C:/Users/AYOU/Desktop/MountainCourtyard/handoff/incoming/CHAR_001_Qinglan_v001_source.glb`

若平台只能导出FBX，用同目录`CHAR_001_Qinglan_v001_source.fbx`，贴图放同名文件夹`CHAR_001_Qinglan_v001_textures/`。同时填写同目录`CHAR_001_LICENSE.md`，记录来源/套餐/当前许可。已有骨骼或动画可以一并提供；**第一步允许先交未绑定A姿模型**，我会检查后再安排绑定，不让你反复生成已合格的外形。

## 可直接使用的参考

- 单人正面生产姿态：`handoff/reference/generated/CHAR_REF_002_Qinglan_ProductionFront_v001.png`。已按原设计生成、保存并查看；手臂与身体分开，便于建模。
- 已认可设计主依据：`handoff/reference/generated/CHAR_REF_001_Qinglan_Turnaround_sheet_v001.png`，提供侧面/背面/服装与包袱一致性。
- 新图是技术姿态辅助，不替代原设计，也不是已完成的3D模型。若单图输入，只上传单人正面图，避免将四视图同板误生成为四个人；支持附加视图时再补充原转面图。

## 推荐操作

1. 打开[Tripo图片转3D](https://www.tripo3d.ai/zh/features/image-to-3d-model)，用你自己的账户；也可使用你已有且许可明确的同类平台。该官方页面目前列有图片生成、绑定与GLB/FBX导出，但实际按钮/额度以登录后的界面为准，不保证生成质量。
2. 上传单人正面参考，输入下方提示词；目标是一位完整青岚，而非场景、雕像或四个人物。
3. 检查脸部、发髻、衣层、包带、手指和双腿是否分开。优先保留原始高质量源，不必为了面数目标把脸部减坏；运行目标15k–30k三角面、1k/2k PBR，我收到后可整理优化。
4. 若现有功能可直接绑定人体骨骼，可导出绑定版；动作希望为Idle/Walk/Run且原地循环。不具备绑定时先导出未绑定A姿版本，不购买/升级套餐来满足本单；额度或导出受限就告知具体限制。
5. 导出GLB（优先，含贴图）或FBX+贴图，按上面文件名放好，并附许可说明，回复“青岚素材已放好，继续”。

## 可复制提示词

One single photorealistic young East Asian woman traveler, match the supplied approved Qinglan reference exactly: same face and topknot, muted blue-gray linen Song-inspired layered tunic, pale undersleeves, brown wrapped belt and crossed satchel strap, brown side satchel, loose dark trousers, wrapped worn boots. Full body in relaxed symmetric A-pose, separate hands and fingers, legs separated naturally, believable anatomy, about1.70m tall. Game character with clean deformable topology, complete underside, PBR base color roughness normal, neutral textures without baked directional shadows. Preserve the side/back costume design from the approved sheet. One character only; no weapons, armor, fantasy ornaments, ground, pedestal, environment or extra bodies. Skeleton/rig when available; otherwise keep clean A-pose geometry for later rigging.

## 我收到后负责

保留原文件/许可，Blender检查尺寸、网格、材质/缺图和骨骼；复核已认可外观；处理原点/朝向/减面与贴图；验证或补齐Idle/Walk/Run，再接入现有CharacterBody控制与相机。正式模型外观及授权按HUMAN GATE #3记录；不合格只提具体修正项，不让你重做整套参考。

## 最低验收与替代

仅一个全身人物，无底座/摄影台，服装/五官与参考一致，手脚不粘连，脸部没有明显破面；贴图随文件保存。提供平台来源和允许本项目使用/商用/随游戏分发的当前许可依据，不预设免费套餐许可。不要提交账号密码或API密钥。

如生成平台不能得到合格人物，可提供你已有的合法授权源模型/委托建模结果及许可，继续沿用已认可设计；当前TEMP只用于玩法，不替代正式验收。
