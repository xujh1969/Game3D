# 青岚GLB接收与静态审查 v002

日期：2026-10-22。状态：PASS_WITH_LIMITATIONS（静态导入）；M5仍IN_PROGRESS。

## 用户范围与原件

用户已明确将本项目限定为Codex三维技术实验，取消此前三维资产版权、来源和商业使用许可的资料提交及审核要求。已更新AGENTS/MASTER_PLAN/任务索引，相关历史待办不再适用，无需再补此类资料。

原件：handoff/incoming/CHAR_001_Qinglan_v001_source.glb，84,053,700字节。
SHA256：c4185db4655fd60d8440e67a580f4bffe94bab5c39119a9c50d1533e35c2e95a。
处理前后哈希一致，原始GLB未覆盖。用户说明为混元3D生成，此信息只作技术记录，不作为审核或开发门槛。

## 实测源数据

Blender5.2.2实际重导入：1网格、1材质、1,499,720三角面、924,398顶点；3张内嵌4096²贴图（BaseColor、Normal、Packed Metallic/Roughness），缺图0。原尺寸约0.520×1.166×0.243m（Godot XYZ）；无骨骼、无动作。源.blend保留完整网格/4K纹理并规范至1.70m、脚底原点。

## 版本和故障处理

- assets/source/CHAR_001_Qinglan_v001.blend：规范尺度后的高精度可编辑源，原细节保留。
- assets/review/CHAR_001_Qinglan_v001_review.glb：第一次直接减至30,000三角面、2K贴图。自动数据检查通过，但实际Godot面部/服装出现严重三角碎片；视觉失败，保留作前后对照，不用于接入。
- 诊断：关闭法线贴图后问题仍存在；无光照模式仍有碎片。原高精度源Blender Studio面部正常，v001在同一Blender灯光下也异常，因此不只是Godot照明问题。
- v002重新从高精度源出发，清除导入自定义法线，按0.000001m焊接重合顶点（924398→749772），重建平滑法线后再减面。该组合处理明显改善碎片；尚未逐项隔离焊接和法线的贡献，不能将全部问题单独归因于其中一项。
- assets/source/CHAR_001_Qinglan_v002_review.blend及assets/review/CHAR_001_Qinglan_v002_review.glb：30,000三角面、1网格/1材质/3张2048²图；缺图0。尺寸0.758483×1.699890×0.353951m，脚底Y=.000137m。
- 首次放assets/processed时受已有.gdignore排除，Godot检查失败退出1；移至独立assets/review并重新导入后通过。该目录是实验审查候选，不是已完成动作资产，原始失败日志保留。

## 实际验证

| 检查 | 日志/JSON | 结果 |
|---|---|---|
| 原件Blender导入 | CHAR_001_source_import_v001.json/.log | 退出0，缺图0 |
| v001处理 | CHAR_001_preparation_v001.json/.log | 退出0，但视觉失败 |
| 原件/首稿同灯光面部 | CHAR_001_source_face_render_v001.log、CHAR_001_review_face_render_v001.log | 退出0，实际图片已查看 |
| 重复点/法线数据 | CHAR_001_normals_diagnostic_v001.log | 退出0 |
| v002修整 | CHAR_001_preparation_v002.json/.log | 退出0 |
| v002 Blender重导入 | CHAR_001_review_import_v002.json/.log | 退出0，缺图0 |
| v002 Godot导入 | CHAR_001_godot_review_import_v002.log | 退出0 |
| v002 Mobile资产检查 | CHAR_001_godot_review_mobile_v002.log、CHAR_001_Review_v002.json | 8项PASS，退出0 |

Godot检查实际测量单角色网格、约1.70m身高、脚底原点、20k–31k面数、单材质、BaseColor、Normal/Roughness存在及确实未绑定。自动PASS只描述这些数据，不代表面部质量或动画完成。

实际Godot Mobile/Radeon/1280×720截图CHAR_001_Review_v002_Front/Left/Right/Back/Face.png均已查看。正背面服装/发髻/左胯行囊延续参考，手脚完整且没有额外摄影台。侧面审查时1m参考柱在Right视图遮挡部分人物，图中明确保留，并非人物模型的一部分。FaceNoNormal/FaceUnshaded仅诊断，不作为最终材质展示。Studio截图为Blender离线灯光，不冒充游戏帧。

## 当前限制与下一步

面部近景仍有低密度轮廓/阴影及UV细节误差，头发/手部也需进一步保真；3万面全局减面不是可变形重拓扑。没有骨骼/Idle/Walk/Run，不宣称动作融合、衣服穿模或脚底接地验收。当前世界仍使用已有TEMP动作代理，未把静态模型直接替换成“能走的正式角色”。

下一步由Codex继续面部保真、可变形拓扑、骨骼权重与基础动作实验；不要求用户重交已收到的模型或补交已取消的资料。本轮未修改游戏世界/控制器，没有重跑完整玩法回归或角色GPU性能采样，历史性能不能视为新角色负载。
