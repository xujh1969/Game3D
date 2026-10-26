# MountainCourtyard / 山中古院

Godot 4.7.2，Windows 单机第三人称宋风山居探索解谜。当前30×30m可玩样板含首版建筑、双门、石径、岩石、竹丛、远山/深度雾及卷轴/石碑/青铜香炉。青岚已使用用户提供的新骨骼模型与Idle/Walk/Run。

当前范围为Codex三维技术实验。按用户2026-10-22明确指示，取消此前三维资产版权/来源/商用许可资料提交与审核门槛，不再据此阻断开发。青岚v006已接入可玩庭院：用户新GLB的41根骨骼及Idle，合并Walking.fbx与Fast Run.fbx为Walk/Run；12899三角面、3张2K恢复贴图，约1.70m。21项动作检查、24项玩法回归和Mobile无传送完整通关通过。交付报告见`reports/validation/CHAR_001_PLAYABLE_v006.md`。

## Windows 开发包（2026-10-26）

本机已导出`builds/Windows/MountainCourtyard.exe`，双击运行，保持同目录PCK文件一起保存。便携包为`builds/MountainCourtyard_Windows_dev_2026-10-26.zip`，解压后运行；无需安装Godot。重新打包运行`BuildWindows.cmd`，详见`docs/WINDOWS_BUILD.md`。构建文件仅在本机builds目录，未上传Git。

独立Release EXE已在本机Mobile图形后端启动并实际截图，导出的同一PCK通过24项玩法回归及完整输入路线；后两者由编辑器加载PCK执行，不是独立EXE真人键鼠通关。报告：`reports/validation/WINDOWS_DEV_BUILD_2026-10-26.md`。

## 启动和操作

本机双击 `Play.cmd`，或在 Godot 中打开 `project.godot` 后 F6/F5 运行。启动脚本使用已检测的本机 Godot 安装路径；其他机器需修改路径或从编辑器运行。默认 Mobile 后端已在 AMD Radeon(TM) Graphics / Vulkan 1.3.260 实际启动。

- WASD：相机相对移动；Shift：奔跑；鼠标：绕角色旋转镜头。
- 靠近并朝向木案上的卷轴、东侧石碑和西侧青铜香炉，出现提示后按E。卷轴拾取后消失，石碑和香炉互动后保留。
- 集齐三项后靠近主殿中间木门按 E，等待门打开，穿门走向内院终点。
- Esc：暂停/继续；菜单提供重开和退出。通关后可点击重开或退出，Enter 也可重开。
- F3：开发版切换性能计数。

## 已验证和限制

实际 Godot 物理场景检查通过，headless 和本机 Mobile 图形后端的无传送自动输入路线均通过（0→3→开门→步行到终点）。日志、截图与验证边界见 `reports/validation/M1_ACCEPTANCE_2026-10-22.md`。

完整真人键鼠通关、菜单按钮实点和长期镜头体验仍待验收。角色已使用用户骨骼动作；贴图投射局部、衣摆穿插与斜坡脚底贴合仍待精修。建筑/岩石阶段的台阶/碰撞及历史基线见`reports/validation/COURTYARD_DELIVERY_v002.md`。

竹丛/远山历史阶段见`reports/validation/ENV_LANDSCAPE_DELIVERY_v002.md`。当前建筑v003接入有来源/校验记录的1k地面与灰泥PBR；315构件几何不变，8项空间/24项回归及Mobile完整通关通过，见`reports/validation/SURFACE_UPGRADE_v003.md`。性能前两轮出现约218–221ms长帧，后续新旧对照均约144FPS且无长帧；根因仍待调查，未完成稳定性验收。

卷轴/石碑阶段记录见`reports/validation/PROP_002_DELIVERY_v002.md`。香炉v002已接入，19项几何、6项香炉、24项回归及Mobile通关通过；历史性能见`reports/validation/PROP_001_DELIVERY_v002.md`。三个金色占位物均已替换，材质与场景仍待精修。

青岚新模型与两个FBX均已接入，无需重复导出。步行1.0m/s，Shift奔跑4.9m/s，动作切换混合0.18秒；打开`Play.cmd`即可体验。角色设计沿用已认可版本。

## 视觉方向审核

生成的待审角色、门和庭院初稿位于 `handoff/reference/generated/`。批准和修改要求见 `handoff/approvals/ART_DIRECTION_v001.md`，图像与资产索引见 `handoff/REQUESTS.md`。模型制作受艺术审核门槛约束。

## 开发工具

```text
Godot --headless --path . --script res://tests/test_m1_runtime.gd
Godot --headless --path . --script res://tests/test_playthrough.gd
Godot --path . res://scenes/world/AssetTest.tscn -- --asset=res://assets/game/FILE.glb
```

Blender 检查/导出工具用法见 `docs/ASSET_PIPELINE.md`。资产清单和性能日志位于 `project_admin/`；管理文件夹带 `.gdignore`，不会被 Godot 当作翻译表或运行资产导入。Git LFS 保存GLB、BLEND、FBX和图像，克隆后需要安装Git LFS并拉取对应文件。

木门制作与实测报告：reports/validation/ARCH_003_DELIVERY_v003.md；材质来源与许可：docs/ASSET_LICENSES.md。
