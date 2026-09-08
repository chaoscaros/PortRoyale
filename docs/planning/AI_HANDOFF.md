# AI 交接

## 当前阶段

Phase 1 - Port World + Fleet Navigation。Task 02 功能实现已完成，运行验收待用户服务恢复。长期目标依然是高度参考《海商王3》的 Web 航海贸易游戏；当前只有航行基础，没有经济。请与 GPT_PLANNING_BRIEF.md 一起上传给 ChatGPT 网页版制定下一轮提示词。

## 当前可运行状态

仓库 /Users/fenglian1/projects/AI/PortRoyale。npm ci 后由用户执行 npm run dev。默认 9999，占用自动顺延；Codex 不启动/重启服务，不新开 Playwright 或替代测试标签，只使用用户指定 Chrome http://localhost:9999/。本轮检查该页面显示 ERR_CONNECTION_REFUSED，Runtime Validation Pending。

进入页面预期看到四港和停泊哈瓦那的一艘船。点击船或“选择测试舰队”，点击港口名/金色标记，再确认“前往”；仅点击港口不会移动。HUD 保留 Clock 调试及派生舰队状态。运行不需要 Blender 或 private local-assets。

## 已实现

- React/TypeScript/Vite/Babylon WebGL/Vitest 基础保持；10TPS Clock、pause、1/2/4。
- Data 四港：哈瓦那(-90,-30)、圣胡安(120,-20)、圣多明各(35,-50)、拿骚(-60,45)。PortId branded，PortRegistry 校验并复制冻结。
- Map<FleetId,FleetState>，初始 fleet-player-001 停泊哈瓦那，speed=8 世界单位/模拟秒。
- MoveFleetCommand 校验 Fleet/Port/状态；同停泊港/同目标 no-op；中途改道从当前位置开始。
- 集中 FleetNavigationSystem fixed tick，直线 min(speed*dt,remaining)，精确到港无 overshoot，更新 currentPort/status/destination。
- WorldSnapshot 深冻结 ports/fleets/position；heading 派生，docked默认+Z；Simulation不依赖DOM或Babylon。
- SelectionState 属于客户端，不在世界快照。点击船高亮，点击港提示，确认前往才发送命令。
- FleetSnapshot → FleetRenderer → 现有 GLB，移除旧静态假船。PortSnapshot → PortRenderer → marker、程序岛/码头、HTML名称标签。
- 选中舰队的目的港航线；UI 状态、海上/港口、距离、speed、派生模拟秒 ETA、命令反馈。
- 相机只调整默认距离330、最大距离520、平移±180覆盖四港，保留原旋转/平移/缩放输入和俯角限制。

## 部分完成

Runtime Validation PENDING。本轮未在运行页面观察新功能，不把单元测试当作浏览器通过。Phase 0 历史已观测海面/船/GLB、暂停、1× TPS10和2× TPS20；4×及相机完整验收仍需补。

最终静态检查：2 个测试文件、30 项测试通过；typecheck（含无DOM核心编译）通过；build 通过，仍有大 chunk 警告。lint: Not configured。

## 尚未实现

Goods、Market、Inventory、Price、Trade、Automatic Trade、Cargo、Crew、Production、Combat、Nation、Mission、Save Game、Server、Multiplayer。没有 A*、NavMesh、海路/海岸避障、碰撞、风或浮力。没有正式港口模型和新增船型。

## 最近工作

2026-09-08 Task 02：实现数据四港、权威舰队、移动命令、导航系统、选择与快照渲染，新增20项导航/模型测试，更新架构、设计、接力文档。Git 提交推送以仓库日志和最终回复为准。

## 重要文件

- src/data/ports/portDefinitions.ts、src/data/worldDefinition.ts。
- src/simulation/world/types.ts、PortRegistry.ts、systems/FleetNavigationSystem.ts、Simulation.ts。
- src/input/SelectionState.ts、src/app/GameApplication.ts。
- src/rendering/ports/PortRenderer.ts、fleets/FleetRenderer.ts、GameRenderer.ts、assets/loadTestShip.ts。
- src/ui/FleetPanel.tsx、Game.tsx、game.css。
- tests/navigation.test.ts、tests/simulation.test.ts。
- docs/architecture/DATA_MODEL.md（Owner/Mutable/Snapshot/Save矩阵）、ARCHITECTURE.md、SYSTEMS.md。

## 已知问题

直线可能穿过视觉岛屿；尚无海上航路/岛屿避障。只有4港/1舰队，不能声称大规模性能。原有 Babylon 构建体积较大；没有触控专项验收。暂停只冻结模拟，镜头仍可操作。位置暂按10TPS直接投影，无渲染插值；停泊船使用默认+Z朝向。港口定义本轮静态，动态增删港口不在范围。

## 技术债

恢复用户服务后补运行验收。后续评估渲染插值、资源拆分、大量舰队加载与性能；FleetRenderer集中维护ID映射，但当前只实际配置一舰队。将来扩展深层数据需继续冻结快照并增加业务测试。

## 无明确理由不要修改

Simulation权威位置、Command/Snapshot边界、固定模拟时间、港口Data单一来源、右手+Y上/+Z船首、GLB米制、不任意缩放、npm、9999自动顺延、用户控制服务/指定Chrome验收、唯一当前状态文件AI_HANDOFF。

## 推荐下一任务

Goods + Market + Fleet Cargo + Buy/Sell Foundation
