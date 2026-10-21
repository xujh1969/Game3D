# ASSET_ARCH_003 — 宋风双扇木门

- 状态：PASS_WITH_LIMITATIONS。
- 图像依据：用户已批准 `handoff/reference/generated/PROP_REF_001_ArchDoorSong_sheet_v001.png`，批准记录见 `handoff/approvals/USER_APPROVAL_2026-10-22_Qinglan_Door_v001.md`。
- 制作方式：本项目Blender参数化几何，非外部AI模型；木材地图来自已核验CC0的Poly Haven，来源与校验值已保存。
- 运行文件：`assets/game/ARCH_003_DoorSong_v003_game.glb`。
- 源文件：`assets/source/ARCH_003_DoorSong_v003.blend`，先前试制稿保留。
- 测量：框体2.24×2.66×0.186m；叶片总宽约2m、高2.5m。7,740 triangles，2材质，3张1024²内嵌PBR贴图，缺失贴图0。
- 交互：独立左右门轴，Godot两组碰撞随门扇向内反向打开；框体固定。集齐三线索才开门，动画完毕才允许终点胜利。
- 验收：GLB结构、Blender导入、AssetTest、Mobile双门检查、M1回归与无传送通关路线均通过。真人键鼠体验及最终照明未验收。
- 交付报告：`reports/validation/ARCH_003_DELIVERY_v003.md`；来源：`docs/ASSET_LICENSES.md`。
- 不再需要用户为本木门生成或上传额外模型。
