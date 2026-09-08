# AI 交接

## 当前阶段

Phase 1.5 — Visual Foundation。Task 03 视觉基础切片已实现并在用户指定 Chrome 验收。当前优先画面、港口、船只、UI；经济暂缓。与 GPT_PLANNING_BRIEF.md 一起交给 ChatGPT 网页版制定后续提示词，不默认恢复经济开发。

## 当前可运行状态

仓库 /Users/fenglian1/projects/AI/PortRoyale，分支 main。npm ci 后由用户运行 npm run dev，9999占用自动顺延。Codex不启动/重启服务、不另开Playwright或替代浏览器；只操作用户指定 http://localhost:9999/ Chrome。Task03期间页面可运行，已复用验收，窗口尺寸模拟已清除并刷新回初始状态。

默认展示哈瓦那、海面和新帆船；点击船→港口名称（或左上港口目录）→确认前往。顶部暂停/1×/2×/4×，底部舰队/哈瓦那/海图全览，F3隐藏/显示开发信息。面板可关闭，资金明确未启用。GLB随仓库交付，运行不需要Blender。

## 已实现

- 保留Phase1四港、一个权威Fleet、MoveFleetCommand、固定10TPS、精确抵达和改道、深冻结快照；Simulation本轮未改动。
- VisualAssetLibrary加载15个分类GLB，实例共享几何与材质；Blender4.5.13自制源文件及复现脚本齐备，3张1024纹理。
- 哈瓦那：两类民居、仓库、总督府、教堂、灯塔、两座码头、桶/箱/小艇、棕榈/树/灌木、沙滩草地丘陵及道路广场；模块独立编辑。其他三港仍是简化岛屿与少量共享建筑。
- 新sloop取代可见测试船，6222三角面、9材质；约6.89米宽、28.03米含艏斜桅长、24.02米总高，水下船底2米。船体/甲板/桅杆/曲面帆/索具/舵齐备，旧ship_test仅执行三轴校准后释放。
- 暖色方向光、冷天光、2048PCF阴影、渐变天空/雾、青蓝海面多频波纹/Fresnel/高光/浅水/泡沫、渲染尾流及轻摆动、FXAA/ACES。
- 正式中文HUD、统一SVG图标、舰队/港口独立面板、细选择圈与方向箭头、虚线航线、稳定港名标签、F3默认隐藏调试。
- 平滑镜头聚焦；修复手动RAF缺beginFrame/endFrame导致deltaTime不更新，以及实例receiveShadows设置位置、海图全览天空边界/过浓雾效。

## 部分完成

Runtime Validation：PASS（本轮4港1船桌面功能与画面加载）。半写实方向已建立，最终美术精修仍属PARTIAL：植被有几何块感、远海波纹重复、其他三港简化；低配和长期压力测试PENDING。不能把基础切片描述为最终高精度美术。

静态：typecheck通过（含无DOM核心编译）、3文件32测试通过、build通过；lint未配置。构建主chunk约6MB，存在体积警告。

## 尚未实现

Goods、Market、Inventory、Price、Trade、Cargo、Crew、Production、Combat、Nation、Mission、Save、Server、Multiplayer；无A*/NavMesh/海岸避障/碰撞/风力/浮力。无真实LOD1/2，未扩充到多艘可玩船或四座精修城市。

## 最近工作

2026-09-08 Task03：完成视觉资产、环境和UI重构，保持Command→Snapshot→Rendering。浏览器实测：选中3D船与港口后确认航行，1/2/4倍约10/20/40TPS；4倍抵达圣胡安(120,-20)，距离/ETA归零；暂停于(119.20,-20.04)、模拟293.2秒时改道拿骚，坐标不变；尾流/船首/虚线随新目标更新。三档1366×768、1440×900、1920×1080查看双面板，关闭/F3/聚焦/鼠标相机可用。详情见DEVLOG。

## 重要文件

- assets-source/blender/visual/build_visual_assets.py、manifest.json，分类.blend与public/assets/models分类GLB。
- src/rendering/assets/VisualAssetLibrary.ts、environment/createEnvironment.ts、ocean/createOcean.ts、effects/ShipWake.ts。
- src/rendering/ports/createPortVisual.ts、PortRenderer.ts、fleets/FleetRenderer.ts、GameRenderer.ts。
- src/ui/Game.tsx、FleetPanel.tsx、PortPanel.tsx、DeveloperHUD.tsx、Icon.tsx、game.css。
- src/app/GameApplication.ts、src/input/StrategyCamera.ts；Simulation、world、FleetNavigationSystem保持原边界。
- tests/assets.test.ts、navigation.test.ts、simulation.test.ts；docs/art三份规范及PERFORMANCE。

## 已知问题

直线航行可能穿视觉岛屿，缩放/平移相机没有地形碰撞。植被与背面墙细节简化，海面远处有程序纹理重复感。仅哈瓦那达到本轮港口切片范围。主chunk较大，独立GLB重复嵌入图片，首轮加载仍有优化空间。当前4港1船短时59～60FPS、交互曾51FPS，不代表所有设备60FPS。

## 技术债

下一轮评估材质/植被/海岸细节、图片去重与按需加载、LOD、低配测试。地形生成与海面浅水使用近似海岸轮廓，需未来美术pass统一。继续保留核心无DOM测试和不可变快照，严禁为视觉效果添加业务状态。

## 无明确理由不要修改

Simulation权威位置、Command/Snapshot边界、固定模拟时间、港口Data单一来源、右手+Y上/+Z船首、米制GLB与水线pivot、npm、9999自动顺延、用户控制服务/指定Chrome验收、唯一当前状态文件AI_HANDOFF。

## 推荐下一任务

Visual Polish 02。优先自然植被、海岸与材质细节、远海波纹和资源优化；或 More Ship / Port Asset Pass。只有用户明确认为画面足够后，才重新推荐 Goods + Market + Trade。
