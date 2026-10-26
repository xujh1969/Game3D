# Windows 开发包

当前版本：2026-10-26 庭院画面精修首轮，60FPS上限，FXAA与低采样远景景深。最新便携包：builds/MountainCourtyard_Look_v001_Windows_2026-10-26.zip。

## 体验

双击同目录的MountainCourtyard.exe，不需要安装Godot。
MountainCourtyard.exe和MountainCourtyard.pck必须放在一起；传给其他电脑时将整个Windows目录压缩后发送。

- WASD移动，Shift奔跑，鼠标旋转镜头。
- 靠近并朝向卷轴、石碑、香炉时按E；集齐三项后在主殿木门前按E，穿门到内院结束。
- Esc暂停，菜单可继续、重开或退出；通关后可重开或退出。

当前是开发体验版本。青岚衣摆穿插、贴图局部、斜坡脚底贴合，以及庭院材质/光照仍需精修。首次启动可能有着色器准备等待。

## 重新打包

在项目根目录运行BuildWindows.cmd，输出builds/Windows/MountainCourtyard.exe及同名PCK。
脚本使用本机Godot4.7.2路径；其他电脑可编辑脚本的GODOT_EXE变量。
需安装4.7.2.stable的Windows x86_64导出模板；本机现已安装Windows所需模板。

export_presets.cfg显式选择主场景、四个Shader和两个新增GLB及依赖；历史源模型、参考图、文档、报告和测试代码不进入游戏包。
未设置代码签名或自定义图标，此包用于当前技术实验。

## 验证与边界

运行Python tools/python/validate_windows_export.py可用编辑器加载导出的同一PCK，检查文件清单、24项玩法回归及Mobile完整路线。
独立EXE启动/渲染另行验证；官方模板禁用外部脚本路径覆盖，不能把编辑器执行的PCK回归称为EXE键鼠通关验收。
本轮实际结果见reports/validation/COURTYARD_LOOK_v001.md；早期开发包记录见WINDOWS_DEV_BUILD_2026-10-26.md。

本轮可复现包内18项美术检查、24项玩法与移动测量：

```text
Python tools/python/validate_windows_export.py --report-prefix=Courtyard_Look_v001_Packed --profile-route
```

初次运行曾测得长帧，复测路线约60FPS；冷启动/长期稳定性未宣称验收通过。
