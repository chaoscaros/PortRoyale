# AI 交接

## 当前阶段

Phase 1.5 — Task06 Hero Port Second Pass。目标仍是High-End Stylized Realism；本轮聚焦城市与地形融合，不以新增资产数量作为成绩。Hero Port second pass：PARTIAL，尚未获得用户视觉认可，不能写成达到Anno117品质。所有新玩法继续冻结。

与GPT_PLANNING_BRIEF一起交给ChatGPT网页制定后续提示词；需要具体美术任务时再附ART_DIRECTION、BLENDER_PIPELINE、ASSET_CATALOG、PERFORMANCE。当前优先级：城市地形融合 > 材质一致性 > 地形道路 > 非重复植被 > 港口生活密度 > 船只近景 > UI小修 > 性能 > 新内容。

## 当前可运行状态

仓库 /Users/fenglian1/projects/AI/PortRoyale，main跟踪origin/main。npm；9999占用自动顺延。服务启动/重启由用户操作，Codex仅连接用户现有Chrome localhost:9999，不启动服务或Playwright浏览器。

默认哈瓦那港湾、停泊双桅横帆船与正式HUD。底部选舰队→左侧港口列表或3D铭牌→右侧确认前往；顶部暂停/1×/2×/4×。底部镜头聚焦/全览；F3默认隐藏。右侧唯一对象面板缩窄贴边，未重设计UI架构。资金仍明确显示经济未启用。

## 已实现

- Simulation、Navigation、Command、Snapshot及Data本轮无改动。保持固定10TPS、权威位置、精确抵达与原地改道，Mesh从不作为权威状态。
- 场地统一：art06_site.py定义15个建筑台地和13段有高程的路网；同一函数用于岛屿、土建、摆放与水深图。主码头→仓储门前→商业坡道→喷泉广场→地标前台阶→住宅坡地形成连续动线。
- 正式Blender土建模块保留独立台基、挡土边、入口踏步、道路边石、坡道与码头连接。既有护岸模块重做中央阶梯开口，三座主码头对齐开口；货堆/绞盘/仓库形成装卸链。
- 后山改为斜向石灰岩脊、鞍部、沟槽和岩层，建筑台地切入地形；岸线补稀疏岩群，移除整圈等距岩石。水深PNG由同一地形导出，图边缘平滑回到深海。
- 10族配对PBR：Plaster/Stone/RoofTile/WoodStructural/WoodDeck/SailCloth/TerrainGrass/TerrainDirt/TerrainRock/Sand；1K、4米MetricUV，颜色/法线/粗糙度共同生成。当前不再运行Task05颜色图集，旧图保留历史编辑来源。
- 墙脚克制湿痕/盐渍、灰泥细裂纹、部分立面色差，陶瓦轻微厚度/色差。地表2K匹配颜色/法线/粗糙度采用Blender原生烘焙；世界空间草地斑块减少铺贴重复，弱化远距离微法线混叠。
- Tall Palm/Wide Palm/Dense Tropical/Sparse Tropical四种植被结构；从树干、分叉、叶簇与冠幅区别，按核心城镇/住宅/背风坡/裸岩布置，不仅随机scale。实例共享几何。
- Hero Ship为67636三角面，接近原预算；艉窗与饰条略弯、补艉甲板栏杆/舵铰；帆脚松弛与不同张力，帆缘/布缝贴合曲面。深木船体、暖甲板、象牙帆、少量蓝漆/黄铜。停泊表现角度改为0.25弧度以兼顾帆面与船体；航行朝向仍来自Snapshot。
- 36套基础资产（原35套精修、1套必要土建）和4套LOD1。总督府、教堂、棕榈A/B使用Babylon原生LOD：地标240米、棕榈175米。远景瓦面使用连续屋顶包络和原材质，避免对独立瓦片直接减面产生孔洞。不是全场景LOD系统。
- 规范材质名共享并冻结、静态港区世界矩阵缓存；动态舰队不冻结。F3增加draw call、active mesh、GPU内部纹理计数。未启用重型AO、4096阴影或重海洋模拟。
- 港名屏幕候选位置避让帆装、地标及对象面板，无安全位置时隐藏该铭牌但保留左侧选择入口。右面板298/280px贴边；默认相机alpha=-1.05、beta=1.03、radius225、目标(-86,0,39)，港口中右、海湾留白。

## 部分完成

Hero Port second pass：PARTIAL。施工基础和城市主轴更可解释，材质通道一致性、植被结构和性能有改善，但部分坡面仍较规则，院落与边缘绿地过渡不够自然，重复立面和少量道具仍有模块感。船只近景继续需要更精细的艉廊与帆布手工美术调整。用户尚未确认达到目标审美，不能按测试通过自动变为PASS。

功能/静态/性能与主观美术验收分别记录，最终数值见末尾“Task06验证记录”。

## 尚未实现

Goods、Market、Inventory、Price、Trade、Cargo、Crew、Production、Nation、Mission、Combat、Save、Server、Multiplayer。无岸线避障、碰撞、物理风力或浮力；直线航行仍可能穿视觉岛屿。无全场景LOD、KTX2、几何压缩和真实低配/长时基准。

## 最近工作

完整重建基础资产与LOD1，并对实际截图发现的问题做针对性重导出：修复浅水图矩形边界、补密冠生态群落、提亮结构木材、护岸真正开出阶梯、远景屋顶改连续包络、减弱地表微法线重复。保留原始可编辑源，未用运行Mesh补造权威地形。

热更新期间曾因旧DebugSnapshot缺少新rendering字段报错；DeveloperHUD已用可选链兼容旧状态，最终刷新后的日志单独检查。基线纹理初版计数只覆盖scene对象，不可作为对比；最终改用Engine GPU内部纹理缓存，包含渲染目标与材质纹理。

## 重要文件

- assets-source/blender/visual/build_high_end_assets.py：当前完整入口；art06_site/materials/vegetation/civilworks/quay/terrain/layout.py为制作分层；build_lod1.py自动生成4套LOD1。
- assets-source/blender/visual/manifest.json：全部资产、实际纹理、场地台地/路网与摆放；scripts/optimize_visual_glb.py负责共享PNG去重。
- assets-source/blender/ports/port_civilworks.blend、port_quay.blend；environment/island_visual_test.blend；ships/sloop.blend；完整源/GLB路径见ASSET_CATALOG。
- src/rendering/assets/VisualAssetLibrary.ts：同源图片限制、规范材质共享、原生LOD。
- src/rendering/ports/labelPlacement.ts、PortRenderer.ts；ocean/createOcean.ts、environment/createEnvironment.ts、fleets/FleetRenderer.ts。
- src/ui/art-hud.css、DeveloperHUD.tsx；tests/assets.test.ts、labelPlacement.test.ts。

## 已知问题

部分坡面、院落边界仍规则，草地细节和重复立面需继续精修；地表2K宏观图不具备建筑铺贴图同等像素密度。程序材质虽通道一致，但不是扫描级PBR或手工高规格成品。小艇、单箱、棚架仍是次级简化模型。船尾与帆布仍有进一步美术空间。

铭牌是局部候选避让，不是全局标签布局；视角极端或空间不足时可能隐藏，港口列表仍可用。右面板仍覆盖少量海图。LOD只有四套，切换是直接切换而非渐变。水深256图为近岸视觉近似，不支持真实折射/水下物理。直线航行无避障。

## 技术债

继续按截图精修坡面/建筑平台过渡、院落小路与非重复立面，再完善近景艉廊/帆面。基于实际GPU数据推进更多LOD和KTX2，而非无依据降画质。构建主chunk约6MB仍有警告；自制环境为低频LDR立方体，非预过滤HDRI；跨系统字体有fallback差异。

## 无明确理由不要修改

Simulation权威位置、Command/Snapshot边界、固定模拟时间、Data单一来源、右手+Y上/+Z船首、米制与水线pivot、npm、9999顺延、用户控制服务/现有Chrome验收。场地高程保持一个制作来源，源/运行文件同步提交，不得覆盖成低模占位体。

## 推荐下一任务

优先Hero Port third pass，以剩余坡面/院落/立面重复为验收对象；另外只允许按用户选择Hero Ship third pass、Secondary Port Art Pass或Visual Performance Pass。不自动开始下一轮，不恢复经济。

## Task06 验证记录 · 2026-09-09

功能回归 PASS；Hero Port second pass: PARTIAL。用户视觉认可、低配和长时基准未完成，不能写成达到Anno117品质。

接续完成：六处空置庭院/背坡的小型非等距植被组（总摆放217）；铭牌增加远侧候选，保护灯塔、总督府、教堂、帆装及左侧说明/导航、右面板。没有新增玩法、资产种类或权威状态。

指定Chrome现有localhost:9999标签实测：默认英雄港、放大港口、船只聚焦及旋转后帆面、港船组合与海图全览已查看；1366×768、1440×900、1920×1080桌面布局均检查，scrollWidth等于对应宽度，面板按钮可用。海图全览可见4港与4套LOD1对应的远景；没有使用新浏览器或启动服务。

2×航行观察20TPS；暂停在(43.36,-38.08)，simulationTime=83.9、tick=839。暂停改道拿骚后位置/时间/tick不变，目的港更新，距离316.9、ETA39.6；暂停稳定0TPS。恢复4×精确抵达拿骚(-160,205)，已停泊、距离/ETA=0，40TPS。1×观察10TPS。此前最终资产4×抵达圣胡安亦通过。

今日1920×1080近港约48～52FPS，311 draw calls / 743 active meshes / 64 GPU内部纹理；选船会增加约2个绘制与网格。航行/暂停操作期间有42～57FPS样本；全览抵达后60FPS、308/838/64。短时观察并非稳定60FPS承诺。GPU纹理包含渲染目标，不等同于21张共享PNG。昨日64FPS样本是不同窗口/负载，不替代今日数据。

最终静态：typecheck通过；4文件39测试通过；build通过（主chunk约6.07MB/gzip1.31MB，保留体积警告）；git diff --check通过。lint：Not configured。Simulation/Data diff为空。最终刷新后的error/warn日志为空；验收后清除视口模拟，恢复原窗口、默认哈瓦那停泊/1×与F3隐藏。

本轮仍有规则坡面、院落硬边、立面与部分树冠重复，以及船尾/帆布程序造型感；上述问题不是测试通过即可关闭的美术验收。下一轮优先Hero Port third pass，聚焦这些实际截图问题；不自动开始，不恢复经济。
