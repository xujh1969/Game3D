# ASSET_<ID> — <中文资产名称>

- 状态：WAITING_FOR_USER
- 资产用途：
- 推荐工具：Tripo / 混元3D / Blender / 已授权现成资产
- 现实世界尺寸（米）：
- 游戏目标三角面：
- 贴图要求：BaseColor / Roughness / Normal / Metallic（适用时），优先 1024
- 参考图存放：`handoff/reference/<ID>_ref_front_v001.png`（侧面和背面按需）
- 参考图提示词 PROMPT_IMAGE（生成单物体、纯背景、正交/三视图、无遮挡、不带地台/文字/水印）：
  ```
  [在这里填可复制的中/英文提示词]
  ```
- Tripo/混元 3D 生成提示词 PROMPT_3D：
  ```
  [填写单一物件、材质、尺度、无背景等]
  ```
- 用户操作步骤：上传参考图 → 生成模型 → 预览检查 → 导出 GLB（如不支持则 FBX） → 以指定文件名保存
- 最终上传路径：`handoff/incoming/<ID>_<Name>_v001_source.glb`
- 有条件提交截图：`handoff/reference/<ID>_preview_v001.png`
- 验收标准：尺度、法线、材质、结构、拓扑、许可记录
- 如失败：换 Tripo/混元、再使用 Blender 拆分/修复；不要一次重做所有资产。
- 用户完成后回复：素材已放好，继续。
