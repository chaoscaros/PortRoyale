# AI 交接

## 当前阶段

Phase 1.5 — AAA Visual Overhaul。Task04英雄港口、英雄船和桌面HUD重制已交付；现代3A策略经营审美仍是目标，不能以面数或功能通过代替用户的美术验收。Task03画面被用户认为仍有玩具/沙盘感，本轮明显提高结构与材质规格，但最终画面质量仍需第二轮精修。经济及所有新玩法继续冻结。

与 GPT_PLANNING_BRIEF.md 一起交给 ChatGPT 网页版制定后续提示词；需要具体美术任务时再附 ART_DIRECTION、ASSET_CATALOG、BLENDER_PIPELINE。

## 当前可运行状态

仓库 /Users/fenglian1/projects/AI/PortRoyale，分支 main，远程 origin/main。用户运行 npm run dev；9999占用自动顺延。Codex不启动/重启服务，也不启动Playwright浏览器。Task04复用用户现有 Chrome localhost:9999，验收后清除视口模拟、刷新恢复初始哈瓦那。

默认展示哈瓦那英雄港、双桅横帆船和正式HUD。底部舰队选择→左侧海域港口或3D港名选择→右侧确认前往。顶部暂停/1×/2×/4×，底部舰队/哈瓦那/全览，主菜单可返回英雄视角、切F3、关闭菜单。右侧只显示一个对象面板；F3默认隐藏。资金明确显示经济未启用，不伪造资源。

## 已实现

- Simulation文件未修改；保留权威Fleet、集中导航、10TPS、Command→Simulation→Snapshot→Rendering、精确抵达和原地改道。
- 依用户允许调整Data次级港位置：哈瓦那(-90,-30)、圣胡安(240,-50)、圣多明各(85,-155)、拿骚(-160,205)。ID稳定，没有只挪Mesh制造假坐标。次级港仅全览或近距离焦点可见，为主港留出画面空间。
- 24套自制可编辑Blender资产和对应GLB：三类民居、两类仓库、总督府、教堂、灯塔、三座木码头、连续石砌港岸/台阶、铺装街道、石墙、市场棚/手推车/桶箱/小艇、两类棕榈/枝叶树/灌木/岩石、不规则海岸及背部高地。
- 英雄建筑实做屋檐、瓦片、窗框百叶、拱券、栏杆阳台、石基与转角石；仓储临海、住宅内街、地标后置。部分临街连续性和地表仍待精修。
- 晨曦号重制为双桅横帆船：66810三角面、9材质、9张运行纹理引用；曲面船体、甲板木缝、舷侧护条/栏杆、舱盖/绞盘、艉楼窗、舵、两桅多层帆和索梯。保留历史资产键与文件名sloop，不能据此误判现在是一桅船。
- 7套1K PBR纹理，共21张编辑PNG；GLB图片去重为20张共享运行PNG。木材/甲板/帆布/墙/瓦/石/地面使用颜色、法线、粗糙度；金属/绳/涂漆独立材质。
- 暖阳+冷天光+自制低频环境立方体、2048PCF、ACES/FXAA和微量Bloom；FBM多尺度海面法线/Fresnel/浅水/泡沫、雾、模拟时间驱动尾流轻摆。港岸水线对齐并柔化浅水硬边。
- 海军蓝/旧铜/象牙白HUD，统一SVG、衬线港名、正式船只线描画像、顶部时钟/倍率/菜单、左区说明、右对象信息、底部命令；选择细弧、方向箭头、细虚线脉动航线、悬停指针与平滑镜头。

## 部分完成

Runtime Validation：PASS（本轮桌面加载、航行和交互回归）；AAA美术目标：PARTIAL。地表较空、树冠规则、帆布和船尾仍有程序模型感，其他三港仍简化。用户最终审美验收、低配/长时基准：PENDING。不要将PASS扩展为“已经达到Anno1800/3A品质”。

最终静态：npm run typecheck通过（含无DOM核心）；npm test为3文件32项通过；npm run build通过；git diff --check通过。lint未配置。主chunk约6.03MB（gzip1.30MB），保留构建体积警告。

## 尚未实现

Goods、Market、Inventory、Price、Trade、Cargo、Crew、Production、Combat、Nation、Mission、Save、Server、Multiplayer。无A*/NavMesh/岸线避障/碰撞/物理风力/浮力。无LOD1/2、纹理KTX2或几何压缩。未做四座英雄城市或多船玩法。

## 最近工作

2026-09-08 Task04：完整执行 build_hero_assets.py 并导出24资产，再运行共享纹理优化；最终船66810三角面。修复码头被地形覆盖、帆层间隙过大、叶冠过稀、共享纹理URL被加载器拼接/拒绝、海岸浅水硬边；最终当前Chrome error日志为空。

实测4×从哈瓦那抵达圣胡安(240.00,-50.00)，停泊、距离/ETA均0；返航途中暂停于(-73.82,-30.98)、模拟322.0秒，再确认改道拿骚，位置和模拟时间保持不变，目标更新，距离251.2、ETA31.4。暂停后TPS0；1×/4×稳定约10/40TPS。观察尾流、船首朝向和航线。F3、面板关闭、菜单、聚焦、旋转/右拖平移/滚轮均实际操作。

1366×768、1440×900、1920×1080在同一Chrome标签模拟并截图检查，正式HUD没有溢出；1366宽DOM scrollWidth也为1366。最终清除模拟恢复原1920×878窗口。详情与限制见 PERFORMANCE/DEVLOG。

## 重要文件

- assets-source/blender/visual/build_hero_assets.py、manifest.json；scripts/optimize_visual_glb.py。旧build_visual_assets.py仅保留Task03基础助手，不是当前重建入口。
- assets-source/blender/ships/sloop.blend → public/assets/models/ships/sloop.glb；其余分类源与GLB路径见ASSET_CATALOG。
- src/rendering/assets/VisualAssetLibrary.ts：共享纹理预处理限定同源/assets/，允许GLB引用../../textures/shared/；修改导出路径须同步验证。
- src/rendering/environment/createEnvironment.ts、ocean/createOcean.ts、ports/createPortVisual.ts、PortRenderer.ts、fleets/FleetRenderer.ts。
- src/ui/Game.tsx、FleetPanel.tsx、PortPanel.tsx、VesselPortrait.tsx、game.css；src/app/GameApplication.ts、src/input/StrategyCamera.ts。
- tests/assets.test.ts、navigation.test.ts、simulation.test.ts；docs/art三份规范、PERFORMANCE。

## 已知问题

直线航行仍可能穿视觉岛屿。地形/浅水轮廓分别在Blender和Shader实现，仅近似一致；港岸端部、草地细节和地面道路需下一pass。背部树冠重复、部分建筑过于规整，船尾体块和帆布张力仍需雕琢。次级小箱/棚/小艇保持简化。较窄视口右面板会遮住主港右侧一部分，但操作可用。港名在部分角度遮住帆装。

当前无真实LOD：总督府32190、教堂26138、两棕榈13104/14112超出建议区间，作为本轮例外记录，不能无限扩展实例。共享GLB几何16.41MiB、共享PNG26.48MiB；源文件约254MiB。短时稳定59～60FPS，交互/焦点过渡样本52～61；并非低配承诺。

## 技术债

第二轮优先画面而不是加玩法：地表/街巷连续性、非重复树冠、帆装/艉楼、近景材质尺度、标签避让；再做LOD、KTX2和按需加载、真实低配测试。当前环境反射是自制低频LDR立方体，不是预过滤HDRI。字体有本机回退，外部字体不可用时字形可能不同。构建大chunk仍待拆分。

## 无明确理由不要修改

Simulation权威位置、Command/Snapshot边界、固定模拟时间、港口Data单一来源、右手+Y上/+Z船首、米制GLB与水线pivot、npm、9999自动顺延、用户控制服务/指定Chrome验收。资产必须源与运行文件同步，不能覆盖为低模占位体。

## 推荐下一任务

仅推荐 Hero Port / Hero Ship Second Pass（或 Visual Polish 02）。使用当前实际截图制定验收，以更自然的地表/城市密度/树冠和可信帆船近景消除沙盘感。用户明确认可视觉之后，才考虑恢复经济路线。不要自动执行下一阶段。
