# MountainCourtyard 开发状态

更新时间：2026-10-21（Asia/Shanghai）

## 环境与基线
- Godot 绝对路径版本检查：`4.7.2.stable.official.ed1daf0bf`。
- Blender 绝对路径版本检查：Blender 5.2.2 LTS。
- Python：3.11.4；Git：2.54.0.windows.1。
- 初始目录未发现 `.git` 或 v1.1 Godot 工程；已初始化新 Git 仓库并建立项目文件。
- Godot/Blender 命令未加入 PATH，按已安装位置使用绝对路径执行。

## 里程碑

| 里程碑 | 状态 | 实际情况与验证 |
|---|---|---|
| M0 环境检测和工程基础 | PASS_WITH_LIMITATIONS | 建立 Godot 工程、目录、README/CHANGELOG、技术文档、manifest 和 Git 仓库。headless 导入/启动均退出码 0。Godot 仍会扫描 `project_admin/` 与 `templates/` 下 CSV，并把它们识别为翻译表，产生无翻译警告；不影响场景加载。|
| M1 第三人称可玩灰盒 | IN_PROGRESS | 有 30×30 地面、青岚 TEMP 胶囊、CharacterBody3D 移动、鼠标第三人称 SpringArm、三线索、解锁门、终点信号和计数/胜利 HUD。暂停菜单、交互提示/方向焦点、围界/建筑阻挡未完成；未验证真实键鼠、镜头遮挡、完整通关和重开。|
| M2 艺术规范与资产准备 | IN_PROGRESS | 建立艺术方向、关卡设计、技术架构、资产管线、验收、性能日志及 6 份 IMAGE/ASSET 任务单；未收到参考图或正式资产。AssetTest 与 Blender 校验/导出脚本尚未实现。|

## 验证记录
- Godot `--headless --path . --import`：最终退出码 0；导入完成，CSV 翻译资源有警告。
- Godot `--headless --path . --quit`：最终退出码 0，无脚本/场景错误。这是 headless 加载检查，不是图形运行验证。
- 首轮发现的 GDScript 类型推断与场景子资源解析错误已修复，后续 headless 检查通过。
- FPS_NOT_MEASURED：未运行目标 Radeon 实机图形性能测试。

## 下一步
- 请按 `handoff/REQUESTS.md` 任务单放入角色三视图、木门三视图和主庭院两张关键帧。正式资产在参考图齐备后继续。
- 完成暂停菜单、交互提示、关卡围界，再验证完整玩法与图形运行。
- 补 AssetTest 场景和 Blender 校验/导出工具。
