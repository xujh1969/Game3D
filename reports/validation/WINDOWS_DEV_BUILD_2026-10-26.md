# Windows 开发体验包 / 2026-10-26

状态：PASS_WITH_LIMITATIONS（开发包）。最终发布与真人独立包完整体验尚未验收。

## 交付

- builds/Windows/MountainCourtyard.exe：Windows x86_64 Release，109268480字节。
- builds/Windows/MountainCourtyard.pck：50252332字节；必须与EXE同目录。
- builds/Windows/README.md：操作与限制说明。
- builds/MountainCourtyard_Windows_dev_2026-10-26.zip：解压后双击EXE，无需安装Godot；体积与SHA256见Windows_Build_Files_2026-10-26.json。
- BuildWindows.cmd可重新导出；export_presets.cfg仅选择Courtyard_Blockout主场景及依赖，不打包历史源模型/交接图/测试/报告。
- builds按既有策略忽略，不将二进制开发包上传Git；代码、配置、说明与证据同步GitHub。

## 模板与实际导出

本机引擎4.7.2.stable.official.ed1daf0bf。原先无模板，现已从Godot官方发布包安装Windows x86_64 debug/release及console模板、version.txt至AppData Godot模板目录。按HTTP Range下载ZIP成员，核对解压长度与ZIP CRC32并保存SHA256；没有下载完整1.28GB跨平台包。

官方文件：https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_export_templates.tpz 。安装清单Windows_Templates_2026-10-26.json/.log。

实际运行BuildWindows.cmd退出0，日志Windows_Export_2026-10-26.log。导出未使用签名、自定义图标或外部rcedit；EXE与PCK分开，便于排查和后续迭代。

## 实际验证

1. 独立Release EXE：--headless --quit-after 5启动退出0；日志Windows_Standalone_Boot_2026-10-26.log。
2. 独立Release EXE：--quit-after 10 --write-movie PNG序列，在AMD Radeon(TM) Graphics / Vulkan1.3.260 / Mobile /1280×720运行并退出0。实际末帧保存为reports/screenshots/Windows_Release_Boot_2026-10-26.png，已查看：角色、庭院和中文HUD可见。日志Windows_Release_Graphics_2026-10-26.log。MovieMaker固定帧输出不用于性能声明。
3. 导出PCK文件清单：Windows_Packed_Inventory_2026-10-26.log，forbidden=[]，未包含源资产、交接、报告、测试、工具与v003-v005旧青岚资源。
4. 同一PCK实际引擎玩法回归24项通过；Windows_Packed_M1_2026-10-26.log，M1_RESULT:0 failures。
5. 同一PCK实际Mobile三线索→开门→步行终点通过，未传送；Windows_Packed_Route_2026-10-26.log，PLAYTHROUGH_RESULT:PASS，终点约(-0.001445,0.300792,-11.68006)。实际通关帧Windows_Package_Victory_2026-10-26.png。
6. 可复现第3–5项：Python tools/python/validate_windows_export.py。脚本在builds临时目录复制既有测试，只将截图输出路径换为包外绝对路径；不更改玩法断言/路线。使用编辑器--main-pack加载导出资源而非工程资源，脚本未打进游戏。

导出PCK SHA256：27dea4cbdf9f07023146fc11d7d383712d037f070f3ea6eac52074a1d79d8402。Release与Debug对照导出的PCK完全一致，后者保留于builds/WindowsQA供排查，不是用户启动包。

## 验证边界与诊断

官方导出模板禁用路径覆盖，--script外部脚本不会接管入口；Release/Debug Probe尝试均未出现PACKAGE_PROBE结果并被终止，相关Probe日志不作为通过证据。Godot --help说明该参数仅编辑器或编译时disable_path_overrides=false的模板可用。因此第4–5项是编辑器执行的同一PCK回归，不能称为独立EXE自动/真人输入通关。

独立EXE已验证启动、真实画面与自动退出；原生包真人键鼠移动/暂停/通关/重开/退出、其他电脑、长期稳定性仍待体验。当前衣摆穿插、投射贴图局部、地形脚底贴合与场景光照仍待精修；未宣称最终发布或最终性能达标。
