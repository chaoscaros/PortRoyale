# AI 交接

## 当前阶段

Phase 1.5 — Task05 High-End Visual Art Pass。正式目标 High-End Stylized Realism，向《纪元1800》《纪元117》的材质层次、资产结构、场景密度和 HUD 质感靠拢。当前交付是进一步升级的美术 pass，不能宣称已经达到商业高规格成品品质。玩法继续冻结。

本文件与 GPT_PLANNING_BRIEF.md 一起交给 ChatGPT 网页制定后续提示词；具体美术任务再附 ART_DIRECTION、ASSET_CATALOG、BLENDER_PIPELINE。优先级：材质 > 模型 > 港口空间 > HUD > 环境 > 植被地形 > 性能 > 新玩法。

## 当前可运行状态

仓库 /Users/fenglian1/projects/AI/PortRoyale，main 跟踪 origin/main。用户运行 npm run dev，9999 占用自动顺延。Codex 不启动/重启服务，也不启动 Playwright 浏览器；只使用用户现有 localhost:9999 Chrome 标签。无需因本轮资产/CSS 修改另启服务。

默认哈瓦那英雄港、双桅横帆船、正式 HUD。底部选舰队→左侧港口或 3D 港名→右侧确认前往；顶部暂停/1×/2×/4×；底部舰队/哈瓦那/全览聚焦。右侧只显示一个对象，F3 默认隐藏，菜单只提供现有操作，资金标注经济未启用。

## 已实现

- Simulation、Data 本轮不变。保持 Command → Simulation → Snapshot、固定10TPS、权威位置、精确抵达及航行中改道，不以 Mesh 反写世界。
- 35 套可编辑 Blender 与 GLB。原 24 套升级表面/结构；新增商宅 A/B、港务所、热带树 B、货堆、货包、系船柱绳缆、起重机、喷泉广场、草丛、小码头共 11 套。墙体厚檐、凹窗、阳台外廊、石基、瓦片和船体曲面来自正式源模型。
- 哈瓦那港湾口保留泊船水域；石砌护岸/台阶接三座大码头，小泊位补边侧。装卸货物聚集仓库门和码头设施，商宅补沿街面，广场及教堂/总督府组织中心，住宅过渡到后方高地。
- 1254×1254 原创 AI 辅助灰泥/木材/石材/草土四区颜色图集。MetricUV 控微表面尺度、AtlasUV 独立取颜色；墙/木/瓦顶点色减少单一底色。2K 连续地表烘焙解决逐三角重复，沙/草/裸岩按高度渐变。原有 1K Normal/Roughness 保留，法线不是扫描级匹配数据。
- Hero Ship：67880 三角面、9 材质；艉楼改为收分曲面、侧窗廊与黄铜柱、较窄艉甲板，补艏部栏饰，强化木板纹理。两桅帆装、索梯、舵、舷侧结构保留。历史键 sloop 实际显示 BRIG，不新增船队。
- 植被含棕榈 A/B、枝叶热带树 A/B、灌木、草丛；冠簇非对称分布，模块实例共享几何。树冠轮廓仍有重复，未获得高规格自然度验收。
- 调整海面近岸灰青色、噪声振幅和高光；暖下午太阳与冷环境光。2048 PCF、ACES、FXAA、微量 Bloom、距离雾。AO 实验性能不佳，最终未启用。
- art-hud.css 统一海军蓝细纹基底、黄铜边缘光/内阴影、标题数值色阶、对象面板和按钮状态；沿用统一线性 SVG、衬线标题/清晰正文字体，F3 保持默认隐藏。
- 哈瓦那默认/聚焦目标统一 (-128,0,30)，radius215。港名移向港岸减少挡帆；静态港区定位后缓存世界矩阵，动态舰队不冻结。

## 部分完成

高规格视觉目标：PARTIAL。材质信息、港口设施、商街密度和 HUD 统一性有升级，但后方山脊仍偏光滑、部分建筑地基缺少自然台地/切坡、树冠仍偏团簇、近景帆布和船体尚有程序制作痕迹。小艇、单箱、桶、市场棚仍为次级简化资产。不能用 35 资产或测试通过代替用户视觉认可。

最终静态与当前浏览器实测结果见本文末尾“Task05 验证记录”；不要沿用 Task04 的 60FPS 作为本轮成绩。

## 尚未实现

Goods、Market、Inventory、Price、Buy/Sell、Cargo、Crew、Production、Combat、Nation、Mission、Save、Server、Multiplayer。无 A*/NavMesh/岸线避障/碰撞/物理风力或浮力。无 LOD1/2、KTX2 或几何压缩。没有把四港全部做成英雄城市。

## 最近工作

完整执行 build_high_end_assets.py，输出源、GLB、布局和共享纹理。修复两类实际画面问题：地表逐三角图集重复造成棋盘感；删除 Blender 属性时引用失效，RockMask 意外成为可见 COLOR_0 导致地面发黑。采用整岛 TerrainUV 烘焙、逐项删除遮罩和导出回归测试。曾试半分辨率 AO/4096 阴影，约34FPS，撤回 AO/恢复2048，再缓存静态变换。

## 重要文件

- assets-source/blender/visual/build_high_end_assets.py：当前完整入口；art05_surfaces/modules/terrain/layout.py 为分层助手；export_sources.py 用于已有源重导出。旧 build_hero_assets.py 仅 Task04 历史重现。
- assets-source/blender/visual/manifest.json、scripts/optimize_visual_glb.py：面数、布局、实际共享纹理、角色和状态。
- assets-source/blender/ships/sloop.blend → public/assets/models/ships/sloop.glb；全部35套对应路径见 ASSET_CATALOG。
- src/rendering/assets/VisualAssetLibrary.ts：共享图片 URI 规范化，限制同源 /assets；需同时交付 models 与 textures/shared。
- src/rendering/environment/createEnvironment.ts、ocean/createOcean.ts、ports/createPortVisual.ts、PortRenderer.ts、fleets/FleetRenderer.ts。
- src/ui/Game.tsx、game.css、art-hud.css；src/app/GameApplication.ts、src/input/StrategyCamera.ts；tests/assets.test.ts。

## 已知问题

直线航行可能穿视觉岛；海面浅水与 Blender 轮廓仅近似一致。港岸端部、后方裸岩山脊、建筑台地/道路切坡、树冠变化和船只近景仍需精修。港名并无通用避让算法。右面板会遮住主港右侧一部分。颜色图集与微表面图并非逐像素一致的扫描 PBR，图集每象限约627像素，不能当2K单材质。

仍仅 LOD0；总督府32586、教堂26446、两棕榈13104/14112超参考预算，不能无限复制。资源传输/显存成本上升，未做低配与长时基准。自制环境立方体为低频 LDR，不是预过滤 HDRI。构建大 chunk 警告仍在。

## 技术债

优先以真实默认/近景截图驱动 Hero Port second pass：山脊和建筑平台可信度、街巷连续性、非重复树冠与材质尺度；然后按实测做 LOD、KTX2、按需加载。需要对图集颜色与法线/粗糙度进行更一致的材质制作。字体使用系统回退，跨系统字形可能不同。

## 无明确理由不要修改

Simulation 权威位置、Command/Snapshot 边界、固定模拟时间、港口 Data 单一来源、右手 +Y 上/+Z 船首、米制与水线 pivot、npm、9999 自动顺延、用户控制服务/指定 Chrome 验收。源与运行文件必须同步。不要将正式模型覆盖为低模占位体。

## 推荐下一任务

Hero Port second pass。以当前默认截图与近景暴露的问题制定验收；不自动实施。仅用户明确认可视觉达标后，才重新建议 Goods + Market + Trade。

## Task05 验证记录 · 2026-09-08

静态：npm run typecheck 通过（含无DOM Simulation项目）；npm run test 3文件33项通过；npm run build 通过；git diff --check 通过。lint：Not configured。生产主chunk 6.05MB / gzip1.31MB，保留大chunk警告。

Runtime：功能回归 PASS，高规格美术目标 PARTIAL，用户审美认可和低配/长时基准 PENDING。本轮复用用户现有 localhost:9999 Chrome，未启动服务/新浏览器。实际查看默认港、船只聚焦近景、对象面板、港口切换和菜单；F3 默认隐藏且可切换。

4×精确抵达圣胡安(240.00,-50.00)，面板为已停泊，40TPS；暂停稳定0TPS。最终2×航行中暂停在(177.51,-46.21)，simulationTime67.9、tick679；改道拿骚后这些值保持不变，目的港更新，距离420.7、ETA52.6。2×运行观察20TPS，初始1×约10TPS。静态港区缓存没有冻结舰队。

同一标签模拟1366×768、1440×900、1920×1080并查看截图；DOM scrollWidth 分别等于1366/1440/1920，无横向溢出，右侧对象面板按钮可用。1920最终开场F3隐藏，Chrome当前 error/warn 日志为空。完成后清除视口模拟并刷新恢复默认哈瓦那、停泊和1×。

最终资产短时近港/全览观察约44～52FPS；视口切换/加载期间有33～38FPS样本，恢复后44～49，不能承诺稳定60FPS。此前半分辨率AO方案约34FPS，最终撤回；当前为2048PCF和静态变换缓存。
