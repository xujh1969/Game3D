《山中古院》Codex 一次性交付开发包 v2.0

1. 在 Windows 创建 D:\GameProjects\MountainCourtyard
2. 解压本 ZIP 的所有文件到该文件夹。若已经有 Codex 开发中的 v1.1 项目，请先备份，然后将本包内 MASTER_PLAN.md、AGENTS.md、templates 等合并进原项目；不要直接覆盖原项目的脚本和场景。
3. 在 Codex 中将这个文件夹作为工作区。把 CODEX_START_HERE.txt 内容粘贴一次给 Codex。
4. Codex 会创建 handoff/requests/ASSET_*.md；你只需按照任务单，在 Tripo 或混元生成资产并放入指定路径。
5. 放好后对 Codex 说：素材已放好，继续。

这里是开发规格包，并非已经完成的 Godot 游戏。


新增（v2.1）：如果 Codex 需要你先生成 2D 参考图，它会在 handoff/requests/ 下创建 IMAGE_*.md 任务单，并要求你把人物三视图、物件三视图、场景情绪图或材质参考图放到 handoff/reference/ 对应子目录。