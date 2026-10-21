# MountainCourtyard 开发状态

更新时间：2026-10-21（Asia/Shanghai）

## 环境与基线
- Godot：4.7.2 stable（绝对路径调用）；Blender：5.2.2 LTS；Python 3.11.4；Git 2.54.0.windows.1。
- 项目已配置并跟踪 GitHub `origin/main`。

## 里程碑

| 里程碑 | 状态 | 实际情况与验证 |
|---|---|---|
| M0 环境检测和工程基础 | PASS_WITH_LIMITATIONS | Godot 工程、目录、基础文档、manifest 和 GitHub 同步基线已建立。CSV 仍被 Godot 识别为翻译表并发出无翻译警告，不阻断场景加载。|
| M1 第三人称可玩灰盒 | IN_PROGRESS | 30×30 地面及四周碰撞边界、主殿墙段/门洞、青岚 TEMP 胶囊、CharacterBody3D WASD/Shift 移动、鼠标 SpringArm 相机、三项可见测试标记、面向焦点的 E 交互、线索计数、锁门反馈、三线索解锁、开门动画、终点提示、Esc 菜单（继续/重开/退出）已实现。真实图形键鼠流程、相机遮挡/手感、完整开门过门和重开体验尚未验收。|
| M2 艺术规范与资产准备 | IN_PROGRESS | 艺术方向、关卡设计、技术架构、资产管线、验收文档及三份图像/三份模型任务单就绪。尚未收到图像/正式资产；AssetTest 和 Blender 自动检查工具待做。|

## 验证记录
- `Godot --headless --path . --editor --quit`：退出码 0，脚本扫描无解析错误。
- `Godot --headless --path . --script res://tests/test_game_state.gd`：退出码 0；通过“重复收集不计数”和“三线索后仅触发一次解锁”断言。
- `Godot --headless --path . --quit`：退出码 0；主场景 headless 加载检查通过。
- 未运行图形窗口的键鼠流程；FPS_NOT_MEASURED，未在 Radeon 实机测量。

## 下一步
- 完成并验收实际图形运行：玩家移动/跳跃落地、焦点与交互提示、线索收集、锁门/开门/通门、通关、暂停/继续/重开、边界与镜头遮挡。
- 继续 M2 的 AssetTest 和 Blender 检查/导出工具。
- 用户参考图任务见 `handoff/REQUESTS.md`；收到后按图像/资产验收流程继续。
