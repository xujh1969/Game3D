# 验收状态

2026-10-26 Windows开发包：独立Release EXE在Radeon Mobile启动并实际渲染，正常自动退出；同一导出PCK的24项玩法与无传送通关通过，执行环境为编辑器加载PCK。未宣称独立EXE真人完整键鼠流程或最终发布验收。证据见`reports/validation/WINDOWS_DEV_BUILD_2026-10-26.md`。

2026-10-22用户范围更新：仅作Codex三维技术实验，取消三维资产版权/来源/商用许可提交与审核要求；下文历史记录中的相关门槛不再适用。技术检查与真实结果报告继续执行。

当前角色证据：`reports/validation/CHAR_001_PLAYABLE_v006.md`。青岚v006已接入可玩庭院：用户新GLB的41根骨骼及Idle，合并Walking.fbx与Fast Run.fbx为Walk/Run；12899三角面、3张2K恢复贴图，约1.70m。21项动作检查、24项玩法回归和Mobile无传送完整通关通过。实际截图与9秒录制已保存；不等同真人键鼠验收或动作自然程度获用户认可。输入动作时长Idle/Walk/Run为1.9/1.4/0.5333秒，导出后含一采样帧为1.9333/1.4333/0.5667秒；移动速度为近似匹配。

详见 `reports/MILESTONE_STATUS.md`。headless 导入/启动只检查项目资源和脚本加载，不替代图形运行与实际键鼠流程。M1 必须通过重复拾取、未集齐锁门、集齐解锁、通门、通关、重开清空、玩家碰撞与相机遮挡检查。正式美术需经过用户参考图/艺术门槛。GPU 性能必须在 Radeon 实机测量。

建筑/岩石阶段实际证据：`reports/validation/COURTYARD_DELIVERY_v002.md`。8项空间检查、24项M1回归、Mobile无传送自动通关与真实GPU静止基线通过；不替代真人完整体验、最终视觉验收或发布包检查。

竹丛/远山阶段实际证据：`reports/validation/ENV_LANDSCAPE_DELIVERY_v002.md`。6项环境检查、24项回归与Mobile通关通过；已查看三张实际场景审查图，最终自然景观质量仍待精修。

卷轴/石碑阶段实际证据：`reports/validation/PROP_002_DELIVERY_v002.md`。9项道具检查、24项回归和Mobile完整输入通关通过，保留法线RED/GREEN检查与当时实机静止基线；该阶段后香炉已完成下述制作。

香炉阶段最新证据：`reports/validation/PROP_001_DELIVERY_v002.md`。参考已明确批准，v002实际模型经19项几何、6项运行、24项回归与Mobile通关通过，三个线索均已替换；最终外观未宣称验收完成。

地面/灰泥当前证据：`reports/validation/SURFACE_UPGRADE_v003.md`。六张1k图MD5核验、315构件几何一致、GLB缺图0、8项空间/24项回归及Mobile完整通关通过；四张实际审查图已查看。前两轮性能出现约218–221ms长帧，后续新旧对照未复现，根因未知；不据短时平均FPS宣称稳定性验收。青岚已更新为用户骨骼模型与三段动作，许可资料不再要求。
