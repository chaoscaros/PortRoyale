# 当前架构 · Phase 1

```text
Data/portDefinitions → PortRegistry → PortSnapshot ───→ PortRenderer
                                   ↘ WorldSnapshot
Canvas picking / HTML 港口标签 → SelectionState（客户端）
                                 ↓ 确认前往
                            MoveFleetCommand
                                 ↓ 校验
Simulation → Map<FleetId,FleetState> ← FleetNavigationSystem.tick(dt)
                                 ↓ 深只读快照
                          FleetSnapshot → FleetRenderer → GLB transform
```

src/data/ports/portDefinitions.ts 是港口唯一数据来源。Simulation 的 PortRegistry 复制并冻结定义，投影到快照；Renderer 不另存港口定义。src/data/worldDefinition.ts 定义初始港、舰队 ID 与 speed=8。

Simulation 持有 Fleet collection 和 Clock，Command 仅修改模拟意图。固定 tick 调用集中 FleetNavigationSystem，直线每步 min(speed*dt, remaining)，到港精确 snap 并更新 docked/currentPort/destination。航行中改道保留当前位置，同目的地为 no-op。世界位置为纯 x/z，不含 Babylon Vector3。

快照 ports、fleets、position 均只读并冻结；不泄露内部可变舰队。heading 航行时按当前位置到目标派生，停泊默认 0（+Z）。ETA 和 remainingDistance 为 UI 派生，不保存冗余权威状态。

GameApplication 持有客户端 SelectionState（不进入 WorldSnapshot）。点击船/港只更新选择，确认“前往”才发送 move-fleet。Renderer picking metadata 只携带稳定英文 ID，不以 mesh name 或 index 为身份。

GameRenderer 消费 Snapshot 与独立 SelectionState。PortRenderer 创建程序岛、码头、金色标记和 HTML 名称标签，远距离固定小字号；标签每帧投影，不随模型无限缩放。FleetRenderer 维护 FleetId → GLB root，选中显示圆环及当前目标航线；没有第二艘静态假船，也不读取 Mesh 反写模拟。

宿主 requestAnimationFrame 与 10 TPS 分离；模拟倍率 1/2/4，自然对应 10/20/40 tick/真实秒。UI 最多约 10Hz 更新，性能数值每秒采样。长帧截断 250ms，隐藏页不补算；纯 Clock 不截断传入时间。ResizeObserver、pointer observer、标签、场景和引擎随应用 dispose 清理。

## 已知边界

只有 4 港/1 Fleet；直线可能穿视觉岛，无海路/避障/碰撞/风/加速度。无经济、货物、完整 ShipState、存档或联机。正式模型保持 Blender→GLB、米制、Babylon 右手 +Y 上/+Z 船首。相机只调初始距离、最大距离和平移边界以覆盖四港，没有重构。
