# 资产管线

运行资产使用 glTF 2.0 binary `.glb`。原始生成文件保留在 `handoff/incoming/`，修整前另存 `assets/source/`；每版递增文件名，正式验收后进入 `assets/game/`。参考图、源文件、处理文件、管理清单和报告通过 `.gdignore` 排除出 Godot 运行资源扫描，仍由 Git/LFS 保存。

## 已实测工具

使用本机 `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`，以下参数接在 `--background --python-exit-code 1 --python` 后：

```text
tools/blender/validate_import.py -- INPUT.glb REPORT.json
tools/blender/optimize_export.py -- INPUT.glb NEW_OUTPUT.glb [RATIO]
```

检查脚本报告网格数量、三角面、世界包围盒、转换至 Godot 的 XYZ 尺寸、材质、图像/缺失贴图、骨架和动作。报告最多为 PASS_WITH_LIMITATIONS；许可、模型尺度预期、门轴、法线/UV、额外地台和实际材质仍须审查。

导出默认 RATIO=1，不自动减面；显式 RATIO<1 才添加 Decimate。骨架模型拒绝自动减面。输出路径必须不存在，避免覆盖旧版本，源文件不变。

## 审查场景

```text
Godot --path . res://scenes/world/AssetTest.tscn -- --asset=res://assets/game/FILE.glb
```

固定相机、主/辅光、地面和一米参照杆。模型保留导入尺度，不自动居中或缩放。默认显示 `assets/temporary/TEMP_Pipeline_Cube_v001.glb`，只是管线测试立方体。`--capture` 仅用于默认立方体的截图检查。

已用该一米立方体完成 Blender 导出→检查→再次导出→Godot 导入及 Mobile 渲染；12 triangles，尺寸 [1,1,1] m，缺失文件 0。报告 `reports/validation/TEMP_cube_import.json`，图像 `reports/screenshots/AssetTest_TEMP_Cube.png`。没有正式角色、纹理资产或减面结果通过验收。

## 素材审核

先批准 `handoff/reference/generated/` 的图像方向，再创建正式模型。记录来源与许可，核对尺寸/Y-up/原点/网格/法线/UV/PBR；按模型特征调整 LOD、贴图和材质。清单 `project_admin/ASSET_MANIFEST.csv`；性能日志 `project_admin/PERFORMANCE_LOG.csv`。当前正式资产为零。
