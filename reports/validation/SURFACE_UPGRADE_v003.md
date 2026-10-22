# 地面与灰泥材质升级 v003

日期：2026-10-22。状态：PASS_WITH_LIMITATIONS；画面稳定性仍有未解释长帧，正式角色仍待素材。

## 本次变更

- 保留可编辑315构件源文件ARCH_Courtyard_v002.blend，另存assets/source/ARCH_Courtyard_v003.blend。
- 仅20个地面/灰泥对象替换材质与UV。源码比较全部315网格的顶点、面索引和世界变换一致；场景碰撞、交互位置、控制器未改。
- GLB为assets/game/ARCH_Courtyard_v003_game.glb，61,752三角面、7网格组、5材质、15张内嵌图，重新导入缺图0，边界30.47×5.23×30.47m不变。
- 地面使用[Poly Haven Brown Mud 02](https://polyhaven.com/a/brown_mud_02)，作者Rob Tuytel；灰泥使用[Plastered Wall 02](https://polyhaven.com/a/plastered_wall_02)，作者Charlotte Baglioni。资产页和[许可页](https://polyhaven.com/license)标记CC0。Diffuse/Roughness/OpenGL Normal各3张1k原图，下载均核对公共API给出的MD5，保存元数据/provenance和原始文件。
- UV按世界坐标连续投影，地面1.3m、灰泥2.2m周期；不将方向日照烘进贴图。旧木材保持1k、石/瓦保持512px项目程序贴图。当前仍不是最终写实场景。

## 实际执行与证据

所有成功命令退出0；日志均位于本目录，截图在../screenshots/。

| 检查 | 证据 | 结果 |
|---|---|---|
| 六张下载校验 | Surface_Textures_download.log | VERIFIED |
| Blender源几何对比 | Surface_Upgrade_geometry.json/.log | 315对象一致，3项PASS |
| Blender重导入 | ARCH_Courtyard_v003_import.json、_validate.log | 7网格/61752三角面/5材质/15图/缺图0 |
| Godot实际导入 | ARCH_Courtyard_v003_godot_import.log | 退出0 |
| Mobile空间 | ARCH_Courtyard_v003_mobile.log | 8项PASS |
| M1回归 | ARCH_Courtyard_v003_M1.log | 24项PASS |
| Mobile无传送输入路线 | ARCH_Courtyard_v003_playthrough_mobile.log | 三线索→开门→步行终点PASS |

已逐张查看ARCH_Courtyard_v003_Entrance/Hero/Porch/Ground.png，均为实际Godot Mobile渲染；审查相机隐藏TEMP角色与HUD，不代表玩家镜头。Victory.png来自实际输入路线。地面颗粒与灰泥表面可见；地面重复平铺、墙面接缝/竖向痕迹仍可见，石径/山体/屋瓦精修和最终光照未完成。

## Radeon实际性能与长帧调查

AMD Radeon(TM) Graphics，Mobile/Vulkan1.3.260，1280×720；每轮预热2秒后静止采样约10秒。process_frame墙钟间隔包含桌面/调度开销，不是纯GPU计时。未改运行材质来掩盖长帧；所有原始样本保留。

| JSON名称前缀 | 场景 | 平均FPS | 最长帧ms | p95/p99 ms | >33.33ms帧 |
|---|---|---:|---:|---|---|
| Surface_Upgrade_Profile_v003 | 新材质首轮 | 102.902 | 220.885 | 未采集 | 数量未采集，至少1 |
| Surface_Upgrade_Profile_v003_repeat | 新材质复测 | 126.367 | 217.891 | 未采集 | 数量未采集，至少1 |
| Surface_Upgrade_Profile_v002_control | 仅视觉替换回旧材质 | 144.019 | 9.391 | 7.787/8.224 | 0 |
| Surface_Upgrade_Profile_v003_diagnostic | 新材质顺序对照 | 144.048 | 9.452 | 7.732/8.379 | 0 |

四轮均80 draw calls / 572086渲染primitives上限，focused_frames等于总帧数。新旧对照不支持“新材质必然产生固定开销”的解释，但不能排除偶发材质/驱动/资源/系统调度问题；**两次长帧根因尚未定位，未宣称已修复**。不凭最后一轮宣称稳定30fps验收通过，长期和移动路线性能尚待测量。约144FPS可能受同步上限影响。

为后续调查，profile_graybox.gd新增p95/p99与所有>33.33ms帧的采样时间；--previous-surfaces只在诊断进程内替换旧视觉，不写世界场景/碰撞。第一次诊断因Node类型推断错误退出1，原始Surface_Upgrade_Profile_diagnostic_parse_failed.log保留；显式声明Node3D后两轮实际通过。

## 青岚生产准备

从已认可转面图生成并查看单人A姿辅助图CHAR_REF_002_Qinglan_ProductionFront_v001.png，精确提示词保存在同目录CHAR_REF_002_PROMPT_v001.md。它是技术参考图片，不是3D人物，不替代原认可设计。

当前无正式模型文件或已连接的角色生成/绑定服务。依MASTER_PLAN M5及HUMAN GATE #1，handoff/requests/ASSET_CHAR_001.md给出单一原始GLB交接、参考/提示词/步骤与许可模板；允许先交未绑定A姿源模型，不发起购买或升级。正式外观与授权另按HUMAN GATE #3确认，TEMP代理继续保持可玩。

## 边界

没有宣称最终材质、宋代考据复原、正式人物、烘焙照明、真人通关、长期稳定性或Windows发布包验收完成。独立只读审查记录见Surface_Upgrade_CodeReview_2026-10-22.md。
