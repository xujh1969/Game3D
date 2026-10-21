# 庭院构图审核 v001

日期：2026-10-22。状态：WAITING_FOR_USER。对应MASTER_PLAN.md的HUMAN GATE #2；尚未收到批准。

## 审核内容

请确认三件事：单层三开间的主建筑体量；中轴石径、两级石阶和中央双门的布局；灰瓦旧木、竹石边景、清晨侧光的氛围方向。青岚和木门已有批准，不重复审核。

## 氛围概念

![入口概念](../reference/generated/ENV_REF_001_MainCourtyardHero_keyframe01_v002.png)

![主庭院概念](../reference/generated/ENV_REF_001_MainCourtyardHero_keyframe02_v002.png)

内置image_gen生成的两张视觉参考，均已实际查看。入口图以主视角作为编辑参考保持场景一致。它们不是Godot游戏截图，不保证尺寸或历史结构准确。主视角右侧附加侧翼、整院满铺石材和屋角曲率不自动进入本轮范围；正式构图以以下尺度草案为基础。已批准木门v003仍保留，不直接复制AI图中的门图案。

## 可执行尺度草案

![入口尺度草案](../reference/environments/ENV_Composition_DRAFT_v001_entrance.png)

![斜向尺度草案](../reference/environments/ENV_Composition_DRAFT_v001_main.png)

这两张是实际Blender离线渲染；源文件`assets/source/ENV_Courtyard_Composition_DRAFT_v001.blend`，复现脚本`tools/blender/build_courtyard_draft.py`，构建日志`reports/validation/ENV_Composition_DRAFT_v001_build.log`。均已查看。

庭院30×30m，建筑台基12×8m，单层三开间，约1.8m中轴石径，台基高0.3m、两级0.15m踏步。木门复用v003。屋面条带、窗格、竹竿和多面石块均为DRAFT体量，没有最终瓦片/苔藓/竹叶/PBR细节。草案未导出GLB、未替换运行关卡。

## 批准后

按该体量制作柱梁/墙窗/台基与屋面模块、真实材质和受控植被，接入Godot后再验证上阶、门后终点通道及实机性能。保持30×30m和现有解谜流程。

可直接回复“庭院方向认可，继续”，或指出要调整的建筑高度、路径布局、竹石分布或光照氛围。此回复只批准方向，不替代正式模型与游戏画面的后续验收。
