# MountainCourtyard / 山中古院 — Codex 全流程开发总规范

版本 2.1｜2026-10-21｜唯一执行入口：本文件。**这是待实现的开发规范，不代表游戏已经完成。**

## 0. 给 Codex 的最高优先级指令

你是本项目的实际执行工程师、技术美术、集成测试负责人。读取本文件后，从项目目录自主推进，不要把本文件变成另一份建议书。你可以编写文件、GDScript、Blender Python、自动化工具、测试以及文档；可访问且已授权的工具才可调用。**不得声称已运行未执行的测试，不得伪造素材或截图，不得为了绕过外部素材而将占位几何称为完成资产。**

原则：一次读完规划，按里程碑逐步执行；每阶段自动继续，只有明确的人类决策门（HUMAN GATE）才暂停并提交一份结构化任务单；使用者提供素材后继续，不需要重复索取已给信息。用户明确喜欢：高写实 A、宋风建筑、第三人称可见主角「青岚」。禁止改回第一人称、低多边形外观或仙侠夸张风。

机器：Windows，AMD Ryzen 5 5600H with integrated Radeon Graphics，16GB RAM，独立 GPU 暂不假设存在。目标开发分辨率 1280×720，优先 30 fps；画面质量需通过烘焙、LOD 和场景克制实现，不能假设能本机实时运行 3A 级动态全局光照。

### 不要向用户反复发送开发指令

你自己管理阶段；所有外部素材需求集中写在 `handoff/REQUESTS.md` 与 `handoff/requests/`，一张任务单一个资产或一类参考图；一次最多请求 3 个有代表性的项目。任务单必须包含具体文件名、目录、至少一条可复制提示词、必要的参考图规范、可接受格式、尺寸、验收标准、推荐工具与失败时替代方案。若参考图可通过项目授权的图像工具生成，则先生成；没有该工具就写 `PROMPT_IMAGE` 或 `PROMPT_IMAGE_SET`，等待用户自行生成并存到指定目录。用户只需按任务单放置文件，然后对你说“素材已放好，继续”。

## 1. 固定技术基线

- Godot 4.7.2 stable，GDScript，3D Renderer=Mobile 优先（检测 Vulkan 驱动与运行情况）；不可用则 Compatibility，记录原因。无需升至 Godot 4.8 beta。不得使用不存在或未经验证的节点/API。通过 `godot --version` 检查，若 PATH 中找不到，记录 `BLOCKED_TOOL` 并指引用户安装，不可假装已测试。
- Blender：可选用于生成、校验、优化、拆分模块、贴图整理；CLI `blender -b --python ...`，仅在检测存在后运行。
- 主资产标准：glTF 2.0 binary `.glb`；源文件 `.blend`、平台生成物与参考图片保留到非运行目录。真实角色需 Rig/Skeleton 和 Idle/Walk/Run 动画；缺失时可用带清晰标志的代理角色验证玩法。
- 项目是 Windows 单机可打包游戏；先完成离线、不联网的可运行 vertical slice。外部 AI 生成服务是人类可参与的依赖，不得硬编码平台密钥。任何付费行为必须先由用户批准。
- 版本控制 Git；大文件 Git LFS（如系统未安装，保留文件并提示安装）。所有阶段完成时保留可回退检查点。忽略 `.godot/`, `builds/` 临时产物；大资产需跟踪或备份，不允许丢失源文件。

## 2. 目标体验与可交付范围

标题：山中古院 / MountainCourtyard。类型：单人第三人称宋风山居探索解谜。游戏总体验 5–10 分钟（首个可玩样板），最终地图约 100×100m 的设想不在此轮制作范围内；**第一轮只制作 30×30m 庭院 vertical slice**。

玩家：青岚，年轻东方旅者，写实身体比例，宋风旅装，青灰/褐中性色调、包袱或小行囊，不穿浮夸盔甲；历史启发式服装而非声称考古复原。移动：WASD，Shift 奔跑，鼠标绕人旋转，E 互动，Esc 菜单。相机第三人称跟随（可配置距离、俯仰、遮挡收缩）、平滑转向、镜头不穿墙。Idle/Walk/Run 基础动作必备，必要时用可测试代理动画（标明 TEMP）。

流程：山径入口 → 庭院前场 → 搜集三项线索（卷轴、石碑铭文、香炉机关）→ 解锁并打开木门 → 到达内院触发结束提示；在 HUD 展示 0/3–3/3；开门前条件不满足时给出提示；胜利后可重新开始。允许探索，禁止卡死。人物碰撞、交互检测、任务状态保存于内存；持久存档可留后续。

美术：高度写实的**宋风山居**，灰瓦、木构梁柱、石台基、格子门、竹林、苔藓、石径、薄雾、清晨斜光。参照《营造法式》与可核验的宋风建筑资料把握构造逻辑；不要宣称历史精确复建。主建筑优先模块化几何：柱、梁、檐、灰瓦、屋面、墙片、门扇、台阶；禁止要求文本生成 3D AI 一次产出结构精确且可扩展的整栋建筑。

画质分级：质量标杆使用高精度离线源资产；实际运行采用优化模型、PBR、烘焙照明、限制阴影和透明层。不得为了图像好看牺牲交互正确性；也不得因低配平台将高写实替换成卡通。

## 3. 目录结构（必须建立）

```text
MountainCourtyard/
  AGENTS.md                     # Codex 行为规则摘要
  MASTER_PLAN.md                # 本文件完整复制
  README.md                     # 启动和实际状态
  CHANGELOG.md
  project.godot
  .gitignore
  docs/
    ART_DIRECTION.md            # 色板、尺度、构图、摄影参考、禁用项
    LEVEL_DESIGN.md             # 30x30 布局/坐标/路径/交互
    TECH_ARCHITECTURE.md        # 节点、信号、脚本职责
    ASSET_PIPELINE.md           # 导入检查、贴图/面数约束
    ACCEPTANCE.md               # 各阶段测试证据
    PERFORMANCE_LOG.csv         # 帧率、驱动、GPU、时间戳
  handoff/
    REQUESTS.md                 # 所有人工待办的索引
    requests/                   # ASSET_xxx.md 单项素材任务
    incoming/                   # 用户按指定命名放原始生成文件
    reference/                  # 用户提供或许可生成的参考图
      characters/               # 角色三视图、服装、表情、材质参考
      props/                    # 单物件三视图、局部特写、结构参考
      environments/             # 场景氛围图、构图图、关键画面
      materials/                # 木材、石材、青铜、布料等材质参考板
      generated/                # 若 Codex 可调用图像工具，则将生成结果统一存这里
    approvals/                  # 用户批准记录
  assets/
    source/                     # .blend 等高精度源文件（不放 res 游戏运行路径以外也可）
    processed/                  # 优化完的中间文件
    game/                       # 已验收、可供 Godot 加载的 .glb 和贴图
    temporary/                  # 标示占位资产
  scenes/
    world/                      # Courtyard.tscn / AssetTest.tscn
    character/                  # Qinglan.tscn / ThirdPersonCamera.tscn
    interactables/              # Door / Clue / InteractionPrompt
    ui/                         # HUD / PauseMenu / WinScreen
  scripts/
    player/ gameplay/ interactables/ ui/ debug/
  tools/
    blender/                    # validate_import.py / optimize_export.py
    godot/                      # tests & validations
    python/                     # manifest / path validation (stdlib)
  tests/
  builds/
  reports/
    MILESTONE_STATUS.md
    validation/
    screenshots/
  ASSET_MANIFEST.csv
```

Codex 可调整细小目录，但须同步文档、保持路径唯一；角色/场景用明确命名，避免 `NewScene2`。所有 `.tscn`、`.gd` 路径不得断链。项目根目录使用英文 ASCII 路径，避免部分 CLI 工具编码兼容问题。

## 4. 可交互完整架构（实现细则）

1. `GameState.gd`（autoload）保存线索集合、胜利状态、可发信号 `clue_collected(id)`, `door_unlocked`, `game_won`，重启清空。
2. `PlayerController.gd` 基于 `CharacterBody3D`；使用 `_physics_process`、地面检测/重力、相机相对 WASD、可配置速度、合理转向。碰撞 CapsuleShape3D；若第三人称角色美术未就绪，用代理 Mesh+颜色标识 TEMP，不因缺资产阻断 M1。
3. `ThirdPersonCamera` 使用 `SpringArm3D` 与 `Camera3D`，可配置 yaw/pitch/distance/灵敏度与窗口鼠标捕获；验证墙体遮挡回缩（如引擎 API 不合适需采用 raycast 并说明）。
4. `Interactable` 通用接口（基类或 group + 方法 `interact(player)`）；交互基于玩家相机方向或角色前方 ShapeCast/RayCast；靠近才提示，按 E 时只触发当前焦点物体。
5. 线索 `CLUE_001` 卷轴、`CLUE_002` 石碑、`CLUE_003` 香炉；每项仅可收集一次，UI 实时更新；对话与物件视觉独立。
6. `DoorController.gd` 被锁时显示中文提示；3/3 时解锁，按 E 平滑旋转开门，物理碰撞协调更新；玩家可以通过而不穿模。
7. `FinishTrigger` 到达内院显示通关界面，提供重新开始与退出按钮。`PauseMenu` 使用 Esc。
8. Debug HUD 显示 fps、draw calls 如可用、场景内三角形统计如可获取，不虚构引擎 API。非开发版可以隐藏。

## 5. 坐标、比例与场景布局

- 统一 1 Godot unit = 1m；Y 向上；建筑主门朝向庭院入口；角色约 1.65–1.75m，门净高建议 >=2.2m、主要通道净宽 >=1.4m（初版体验尺寸，艺术调整须记录）。
- 测试庭院 X,Z 在 -15 到 +15m，入口大致 (0,0,+13)，中轴石径向 -Z 到主建筑门，主建筑占后侧约 12×8m，庭院边界需防跌落，线索分布入口侧、东侧石碑、西侧香炉，内院终点门后。
- 首先建立灰盒 `Courtyard_Blockout.tscn`，并独立建美术层节点，保证替换资产不影响关卡交互坐标。角色和相机必须可移动。将场景组织为 Ground / Architecture / Nature / Props / Interaction / Lighting / Navigation / PlayerSpawn。
- 建筑只能以真实参考、合理尺度、模块复用为目标；屋顶斗拱先用可解释的参数化 Blender 模块，正式精修需人工审查。避免伪历史装饰。

## 6. 资产规范、外部 AI 分工、命名规则

*场景逻辑由 Codex 负责，外观源资产由最合适的工具负责*。

| Asset ID | 类型 | 首选来源 | 注意 |
|---|---|---|---|
| ARCH_001 | 柱/梁与架构模块 | Blender 脚本 | 精确尺度与拼接 |
| ARCH_002 | 屋面与灰瓦模块 | Blender 脚本或授权资产 | 重复实例、贴图重复 |
| ARCH_003 | 宋风雕花木门 | Tripo 或混元 + Blender | 独立生成，拆门轴做可动 |
| ARCH_004 | 格子窗/墙/台基 | Blender 脚本 | 模块化 |
| NAT_001 | 苔藓岩石 | Tripo/混元或授权扫描资产 | 可复用 3 个变体 |
| NAT_002 | 竹子/树 | 授权植被或 Blender | 不首选 AI 生成毛茸茸网格 |
| PROP_001 | 青铜香炉 | Tripo/混元 | 检查浮雕/纹理 |
| PROP_002 | 卷轴/石碑 | Blender + AI 纹理参考 | 可交互 |
| CHAR_001 | 青岚 | 人物工作流，先参考多视图 | 必须 Rig / Anim，版权及商用许可 |

源资产推荐命名：`ARCH_003_DoorSong_v001_source.glb`（生成结果），`ARCH_003_DoorSong_v001.blend`（修整源），`ARCH_003_DoorSong_v001_game.glb`（优化的可运行文件），参考图片 `ARCH_003_DoorSong_ref_front_v001.png`、`..._ref_side_v001.png`、`..._ref_back_v001.png`。所有 ID 文件名一律 ASCII、下划线，不使用空格或中文。每次更新 +1 版本，不覆盖已批准版本。对应目录分别为 `handoff/incoming/`, `assets/source/`, `assets/game/`, `handoff/reference/`。

GLB 导入前验证：完整网格/材质；实际尺寸正确，Y 向上；模型摆放和原点正确（门的门轴必须经过整理）；无额外地板/摄影台；没有烧进 BaseColor 的明显光照/阴影；检查法线/UV；纹理许可；必要时 LOD/网格减面/材质合并；不存在明显破面、内翻、悬空配件。对有 PBR 光泽材质至少保留 BaseColor, Roughness, Metallic（适用时）, Normal（适用时）。

初始预算建议：小道具 1k–5k triangles，中型构件 2k–10k，角色 15k–30k，贴图通常 1024，重点 2048；整个测试庭院面数、draw calls 和显存按实机测量迭代，不能把这些当绝对上限。共享纹理与 MultiMesh/实例化优先。因老集显不做大量透明树叶及高代价后处理。

### 人工素材任务单协议（最关键）

每次需要素材时：

1. 首先查询 `assets/game/` 中是否已有已验收可复用资产；再检查 `handoff/incoming/` 是否已有用户提交的文件；不要反复请求。
2. 无资产时向 `handoff/requests/ASSET_<ID>.md` 写一份任务，使用模板 `templates/ASSET_REQUEST_TEMPLATE.md`；更新 `handoff/REQUESTS.md` 中状态为 `WAITING_FOR_USER`。
3. 报告给用户：资产 ID、用途、推荐 Tripo/混元/Blender、图像参考输入、必须保存到的**完整相对路径**、文件名、需要的视图、禁止事项、导出格式和质量检查。需要参考图片时给出图像提示词；若有经授权且可用的图像生成工具，应生成并保存图片；否则不要声称有图片。
4. 一批最多 3 项，避免一次请求 23 件。人类可上传 `.glb` 或 `.fbx`（如 GLB 不可导出）及参考 `.png`。优先 `.glb`；如果供应方输出 `.fbx`，先用 Blender 转 GLB。
5. 收到文件后自动重启导入校验、建立资产测试场景并记录审查结果，变更 manifest `IN_REVIEW` → `APPROVED` / `REVISION_REQUIRED`。若仍有问题只回报具体问题和修改要求，不让用户重新阅读整份文档。
6. 缺少正式美术资产时可以继续实现不依赖它的玩法、测试与工具，但不能跳过 `ART_APPROVAL_GATE` 进入最终视觉验收。

人工任务单质量要能让非开发者直接照做；明确 Tripo/混元 Web 页面流程：打开 → 上传参考图或文字描述 → 选择模型生成 → 检查预览 → 导出 GLB → 按指定文件名放进项目的指定目录。禁止假定平台按钮名永远不变；如果实际界面不同，只描述目标操作。

### 6.1 图像参考任务单协议（2D 概念图 / 三视图 / 场景图）

高质量 3D 项目经常先缺 2D 参考而不是直接缺模型。因此 Codex 必须在合适时机主动请求 **人物三视图、单物件三视图、场景情绪图 / keyframe、材质参考板**，而不是在没有统一视觉依据的情况下盲目组装 3D 资产。

图像请求分为四类：

1. **CHAR_REF**：角色相关，例如 `CHAR_REF_001_Qinglan_Turnaround`、`CHAR_REF_002_Qinglan_Costume_Closeup`。
2. **PROP_REF**：单物件或建筑构件相关，例如门、香炉、灯笼、窗格、斗拱、瓦片。
3. **ENV_REF**：场景相关，例如入口石径、主庭院构图、清晨薄雾气氛图、内院终点镜头。
4. **MAT_REF**：材质板，例如宋风旧木、青石、灰瓦、青铜氧化、粗麻布。

图像文件命名统一：

- 三视图：`<REF_ID>_front_v001.png`, `<REF_ID>_side_v001.png`, `<REF_ID>_back_v001.png`
- 透视概念图：`<REF_ID>_perspective_v001.png`
- 场景关键帧：`<REF_ID>_keyframe01_v001.png`、`...02...`
- 材质板：`<REF_ID>_sheet_v001.png`

默认存放位置：

- 角色：`handoff/reference/characters/`
- 物件：`handoff/reference/props/`
- 场景：`handoff/reference/environments/`
- 材质：`handoff/reference/materials/`

Codex 在需要 2D 参考图时必须：

1. 先检查上述目录中是否已有可用图像；不要重复请求。
2. 若没有，创建 `handoff/requests/IMAGE_<REF_ID>.md`，使用模板 `templates/IMAGE_REQUEST_TEMPLATE.md`。
3. 在任务单中给出：图像用途、建议外部工具、画幅与数量、是否需要纯白/纯灰背景、是否需要正交三视图、是否必须全身、必须避免的内容，以及至少一条可复制的图像生成提示词。
4. 指明用户应将生成后的 PNG / JPG 放到哪个精确相对路径。
5. 对角色三视图和单物件三视图，要求 **无背景干扰、无遮挡、无文字水印、尽量正交**；对场景情绪图，要求给出摄影机高度、镜头方向、时间天气、主构图元素。
6. 收到图像后，更新 `handoff/REQUESTS.md` 状态，必要时挑选其中一张作为后续 Tripo/混元 3D 输入参考，并在相关 `ASSET_<ID>.md` 里引用路径。

**角色三视图最低要求**：正面、背面、侧面；同一角色保持服装、发型、比例一致；建议再附 1 张 3/4 透视图。

**物件三视图最低要求**：正面、侧面、背面；若是门、窗、斗拱等结构件，允许补 1 张局部特写以说明雕花和连接方式。

**场景图最低要求**：至少 2 张关键画面——入口第一眼与主庭院英雄镜头；如涉及光照氛围，再补清晨雾气或斜阳版本。

**材质参考板最低要求**：单张图中展示该材料在清晰光照下的近景纹理，不混合太多无关物体。

如果项目授权的图像生成工具可直接调用，则 Codex 可先生成初稿并保存在 `handoff/reference/generated/`，再请求用户审查；若没有，必须只提供提示词与路径，不得谎称已生成。

## 7. Codex 自主执行计划（按顺序，只有门槛暂停）

### M0：环境检测和工程基础

检测 `godot --version`、`blender --version`、`git --version`、Python；检查 Windows 运行权限与项目目录；创建目录、初始文档、MANIFEST 和 Git 仓库。只在 Godot 工具存在时创建/验证 `project.godot`。输出 `reports/MILESTONE_STATUS.md` 实际状态，工具缺失标 `BLOCKED_TOOL` 且继续其他可做的文档/代码。验收：结构齐全、项目能被 Godot 打开、无无关报错；保存 checkpoint。

### M1：无需外部资产的第三人称可玩灰盒

创建 30x30 庭院灰盒、可见青岚 TEMP 代理、SpringArm 相机、移动奔跑、可互动的三线索、门锁和开门、胜利界面、Esc 菜单。交互和空间基于数据驱动；代码分模块；创建基础自动检测脚本。
验收：玩家可完成 0→3→开门→通关；相机不穿墙；不允许用静止 2D 图骗成 3D；使用键鼠；运行日志无阻断错误。

### M2：艺术规范与资产生产准备

完成 `ART_DIRECTION.md`：宋代山居建筑参考规则、写实 PBR、材料分类、颜色与光源、人物轮廓、摄影角度、需避免的年代混用。完成资产清单、AssetTest 场景、Blender 自动检验/导出脚本（环境有 Blender 才执行）；先准备必要的图像任务单，包括 `CHAR_REF_001_Qinglan_Turnaround`、`ENV_REF_001_EntranceMood`、`ENV_REF_002_MainCourtyardHero`，以及 3 个试制资产任务：`ARCH_003` 宋风木门、`NAT_001` 苔藓岩石、`PROP_001` 青铜香炉`。先分别生成/导入/验收三类参考图和这三个资产，不可批量索取其他内容。
**HUMAN GATE #1**：当需要用户提供生成资产时，输出完整任务单路径与步骤，等待用户放入文件并说继续。其余无阻断任务照常推进。

### M3：资产优化与首批场景替换

对每个用户提供的资产先备份原始文件，使用 Blender 整理或记录无法处理原因。产出 `assets/game/<id>_..._game.glb`；填写面数、材质数量和尺寸；通过 `AssetTest.tscn` 显示标准光源下的尺度，实际查看或截图证据（若工具能取得截图）。替换灰盒对应位置，保留交互 Collider。不合格则提交具体修改单。

### M4：宋风主建筑与写实庭院

使用模块化 Blender 建造木柱、梁架、屋檐、灰瓦、格子门、台阶。保持可信宋式结构并将缺乏史料的做法标识为“宋风创作”。重点打造主视角构图，铺地与苔藓材质，竹林少量摆放，静态照明 / lightmaps 在当前渲染后端支持下实测。按阶段截图检查美术一致性。对不能自动获得的高质量植被/角色素材新增小批次人工任务单。
**HUMAN GATE #2**：正式主建筑外形与场景构图需要用户批准；不批准只迭代相关资产，不扩展地图。

### M5：青岚写实角色生产及动画

先用临时可行角色保持交互可玩。人物三视图与服装概念必须先通过图像任务单与人类参考图确认；如果缺少角色转面一致的图像，不得直接进入正式角色建模。若 Tripo/混元导出的角色无可靠骨骼/动画，使用适用的绑定/动画平台（如 Mixamo，核对服务支持的模型格式与许可）或合法已绑定角色基础模型。不得假称已自动得到写实角色。至少 Idle, Walk, Run；可选 Pickup。角色替换须保留角色控制与摄像机，测试动作融合、转向、脚底接地、衣服穿模。
**HUMAN GATE #3**：正式青岚外观及授权确认。

### M6：画面/音效/性能/稳定性

加入清晨光线、远山薄雾、PBR、烘焙阴影（若支持）、有限动态灯、音效、交互提示；做图形设置“Performance”与“Quality”，起始默认 Performance。性能测试应在**用户的真实 Radeon 机器**运行；若 Codex 在远程无 GPU 环境，只做 headless 脚本/导入验证，标示 `FPS_NOT_MEASURED`，不能编造。将 FPS 测试日志填写 `docs/PERFORMANCE_LOG.csv`。低配版 720p 30fps 为目标（可能需要再调整）。

### M7：发布与交付

安装并检测 Godot Windows export templates（没有则给用户安装任务），导出 `builds/MountainCourtyard_Windows.exe`，在真实 Windows 上确认可以启动、退出、完成所有剧情，不依赖编辑器。创建 README 使用方法、已知问题、授权清单、素材来源及许可证、截图证据、最终检验报告。没有实际运行时标 `EXPORTED_UNVERIFIED`，不可标 `PASS`。

## 8. 自动测试与人工验收准则

必须在可用工具环境执行：

- CLI：`godot --headless --path . --import` 用于导入资源；`godot --headless --path . --quit` 用于启动校验（不是实际图形运行验证）；`godot --headless --path . --script <script>` 用于自有脚本测试（以已测试 CLI 为准）。记录退出码、日志、运行环境。
- 逻辑：重复收集不得重复计数；未集齐不可开门；集齐可开；HUD 状态正确；Restart 清空进度；线索所有状态无空引用。
- 玩家：有重力和碰撞；WASD、跑步、朝向、跟随相机；能靠近物件按 E；可通过开门；不掉出地图。
- 资产：大小合规、法线正确、贴图不缺、物件原点合理、无多余底座、授权明确、导入可见；表现有照片级材质方向而非 Cartoon。
- 性能：用户实机记录分辨率、画质、场景、平均/最低 FPS（如果使用的工具可测），同时标注观测方法；仅 headless 不能代表 GPU 性能。
- 交付：源代码、GLB 和素材声明、Windows 包、详细 README 与每阶段真实状态。

状态值只能用 `NOT_STARTED`, `IN_PROGRESS`, `WAITING_FOR_USER`, `BLOCKED_TOOL`, `FAILED`, `PASS`, `PASS_WITH_LIMITATIONS`。每次 Codex 工作更新 `reports/MILESTONE_STATUS.md`：实际完成、验证命令、结果证据、阻断项和下一步。不要在最后用空泛句子“已完成游戏”。

## 9. 失败恢复与权限

外部生成一次失败允许调整提示词或换平台，保留失败版本；模型尺度/贴图不合格先尝试 Blender 修复；3 次失败汇总错误发用户决策，不无限自动重试。CLI 错误先最小复现并修复，不清除用户文件，不覆盖已验收素材。不删除旧资源；数据迁移先备份。

不得：假称调用付费平台；未经用户允许购买素材或订阅；提交任何 API key；从网络下载不明许可证模型；在工程内暗藏外部追踪；利用渲染图代替可玩程序；擅自更换引擎或人物视角。

## 10. Codex 首次启动的最终动作

1. 阅读本文件和 `AGENTS.md`，建立本项目工程，检查仓库是否已有 v1.1 成果。若已有成果优先增量保留，不重建。
2. 生成阶段状态表和验收文档，立即开始 M0/M1；能测试就运行；不能测试就标注环境限制。
3. 同时准备 M2 三件试制资产的任务单（详细命名、参考图生成提示词），但不要等待用户才实现基本玩法。
4. 当需要手工素材时，给用户一段短报告：`请将 <文件名> 放入 <路径>，完成后回复“素材已放好，继续”`，并指向详细任务单。
5. 除上述 HUMAN GATE 外，你负责自主管理，不要每一步都征求许可。

### 参考资料
- Godot 4.7.2： https://godotengine.org/download/archive/4.7.2-stable/
- Godot CLI： https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Godot glTF： https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html
- Tripo Image-to-3D： https://www.tripo3d.ai/zh/features/image-to-3d-model
