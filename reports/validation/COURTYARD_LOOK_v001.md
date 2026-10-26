# 庭院画面与空气感精修首轮 v001

2026-10-26 / PASS_WITH_LIMITATIONS。用户已批准本轮改善方向；当前是实际游戏美术首轮，不宣称达到最终写实质量。

## 改动与源

- 原ARCH_Courtyard_v003 GLB、角色v006和三线索位置不变。独立Atmosphere子节点对原地面/铺路材质做运行时覆盖，不改主通道碰撞。
- 地面使用保留照片BaseColor/Normal/Roughness：双尺度/旋转混合、大尺度土色及潮土苔色分区；石板按实际.60m间距做色差。不是仅换一张更大重复贴图。
- garden v003：112874三角面/7网格/16参数材质；11657草叶、27蕨株及灌木、枯叶碎石、木凳和陶罐。植被无碰撞，小物件另有简化实体碰撞，位于原路线外。
- ridges v004：63360三角面/4层，远近色差、普通雾与简化坡面着色。六组复用外竹根部在边界外，一组冠层自然越墙约.56m。叶片轻摆。
- 新几何由tools/python/build_courtyard_garden.py制作可复现GLB。本机未找到之前记录的Blender可执行文件，MCP也未连接，因此没有运行Blender或生成BLEND；未因此中断其他改善。源脚本及v001/v002/v003试制资产保留。新增植被/小物件没有照片纹理，不虚构贴图生产。
- 清晨侧光、天空冷色填光、低能量门廊补光；补光是近似，不是烘焙GI。Lightmap_Readiness报告显示原建筑7网格UV2全为0，本轮没有进行烘焙；UV2整理和编辑器GPU烘焙仍为后续独立阶段。
- 深度/高度薄雾；远景景深46m起、65m过渡、强度.055，BOX低采样。没有Mobile不支持的体积雾。
- 门廊/竹下局部浮尘、22粒香烟与泥地脚步尘。billboard保留尺度，避免首轮观察到的大块白斑。脚步尘以当前庭院坐标分区判断地面，不是通用材质射线系统。
- FXAA、60FPS上限用于集显预算；不启用高成本实时GI或2xMSAA。

## 实际画面对比

Before与After均为Godot Mobile/1280×720实际渲染，相同固定机位/FOV，隐藏HUD；不是生成概念图。After使用最终视觉设置，图片已查看。

| 机位 | 改前 | 改后 |
|---|---|---|
| 入口 | [Before](../screenshots/Courtyard_Look_v001_Before_Entrance.png) | [After](../screenshots/Courtyard_Look_v001_After_Entrance.png) |
| 主视角 | [Before](../screenshots/Courtyard_Look_v001_Before_Hero.png) | [After](../screenshots/Courtyard_Look_v001_After_Hero.png) |
| 地面 | [Before](../screenshots/Courtyard_Look_v001_Before_Ground.png) | [After](../screenshots/Courtyard_Look_v001_After_Ground.png) |
| 香炉 | [Before](../screenshots/Courtyard_Look_v001_Before_Incense.png) | [After](../screenshots/Courtyard_Look_v001_After_Incense.png) |
| 门廊 | [Before](../screenshots/Courtyard_Look_v001_Before_Porch.png) | [After](../screenshots/Courtyard_Look_v001_After_Porch.png) |

独立EXE实际帧：Courtyard_Look_v001_Release_Boot.png，已查看。

## 实际检查与打包

- Godot导入、18项美术/效果检查、24项玩法回归均通过；原始日志Courtyard_Look_v001_Structure/M1以及Packed_Look/Packed_M1保留。
- 最终同一PCK：Inventory missing=[]/forbidden=[]；Look18项、M1 24项、Mobile三线索→开门→步行终点通过，无传送。Validation JSON保存PCK SHA256及各项退出0。
- 首包选定场景导出漏掉4个Shader与2个新增GLB，真实PCK测试发现预载失败。现改resources模式并显式列出这6项及主场景，失败PCK保存在builds/Windows_Look_MissingDeps.pck，失败日志也保留。不能只凭源preload推断导出齐全。
- 独立Release EXE在builds/Windows自身目录运行，Radeon Mobile真实启动/渲染并自动退出0，日志Courtyard_Look_v001_Release_Boot.log。完整自动路线是编辑器加载同一PCK，不宣称独立EXE真人完整操作验收。
- 最新EXE/PCK位于builds/Windows，便携ZIP为builds/MountainCourtyard_Look_v001_Windows_2026-10-26.zip。旧有效包另存Windows_Before_Look_2026-10-26，旧ZIP保留。新构建清单与SHA256见Courtyard_Look_v001_Build_Files.json。builds不上传Git。

复现：

```text
BuildWindows.cmd
Python tools/python/validate_windows_export.py --report-prefix=Courtyard_Look_v001_Packed --profile-route
Godot --path . --script res://tools/godot/capture_courtyard_look.gd -- --phase=After
Godot --path . --script res://tools/godot/profile_graybox.gd -- --report-name=Courtyard_Look_v001_Profile_Final
Godot --headless --path . --script res://tools/godot/check_lightmap_readiness.gd
```

## 性能：区分首次运行和复测

本机AMD Radeon(TM) Graphics / Vulkan1.3.260 / Mobile /720p。移动测量从首次物理移动后2秒开始，到通关前停止，不把截图编码当作游戏帧时间；启动阶段另外记录。GPU测试拒绝headless，实际拒绝退出1日志保留。

| PCK完整移动路线 | 平均FPS | p95 ms | 最慢ms | >33.33ms帧 |
|---|---:|---:|---:|---:|
| 高开销初版 | 68.57 | 48.320 | 286.350 | 268 |
| 最终设置首次 | 50.33 | 40.131 | 298.840 | 198 |
| 最终设置复测 | 60.00 | 16.941 | 18.697 | 0 |

最终复测采样40.332秒/2420帧，p99 17.223ms，最多91draw calls。启动到首次移动1.836秒，启动阶段已记录间隔最大35.647ms。

最终静止样本平均60.00FPS，p95 16.939ms，最慢21.963ms，无>33.33ms帧。AB_Control/NoDOF/NoMSAA/NoOuterShadows/LowCostDOF/Cap60原始JSON与日志保留，说明单效果有开销；单轮受系统负载影响，不能当作全部卡顿根因证明。

早期源场景测量出现过1秒级启动长帧，首次最终配置PCK仍有298.84ms长帧。以上失败/慢帧没有删除，也没有用复测60FPS宣称冷启动或长期稳定性已解决。

## 剩余边界

建筑近景构件/石材边缘、植被和木凳陶罐细表面仍简化，远山仍为程序地形。没有烘焙间接光、复杂体积光或真实布料。角色原有衣摆/脚底贴合限制未在本轮解决。最终写实观感、真人完整流程、其他电脑与长期稳定性仍待体验和后续精修。独立只读审查未发现剩余Critical/Important，修复与说明见CodeReview报告。
