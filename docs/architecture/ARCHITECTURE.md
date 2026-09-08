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

GameRenderer 消费 Snapshot 与独立 SelectionState。PortRenderer 创建模块化GLB港口、次级岛屿和 HTML 名称铭牌，远距离固定小字号；标签每帧投影，不随模型无限缩放。FleetRenderer 维护 FleetId → GLB root，选中显示圆环及当前目标航线；没有第二艘静态假船，也不读取 Mesh 反写模拟。

宿主 requestAnimationFrame 与 10 TPS 分离；模拟倍率 1/2/4，自然对应 10/20/40 tick/真实秒。UI 最多约 10Hz 更新，性能数值每秒采样。长帧截断 250ms，隐藏页不补算；纯 Clock 不截断传入时间。ResizeObserver、pointer observer、标签、场景和引擎随应用 dispose 清理。

## 已知边界

只有 4 港/1 Fleet；直线可能穿视觉岛，无海路/避障/碰撞/风/加速度。无经济、货物、完整 ShipState、存档或联机。正式模型保持 Blender→GLB、米制、Babylon 右手 +Y 上/+Z 船首。相机有英雄镜头、平滑聚焦与全览距离；表现层不反写世界。

## Phase 1.5 视觉资产边界

VisualAssetLibrary 读取静态 manifest、加载 GLB 容器和实例化模块；createPortVisual 只构造港口外观。createEnvironment 负责灯光/阴影/天空/后处理，createOcean 和 ShipWake 仅生成视觉效果。FleetRenderer 按 FleetSnapshot 更新位置；摆动和停泊视觉朝向不写回 Simulation。GameRenderer 是组合协调层，初始化资产、调度更新和相机聚焦。

UI 分为 Game、FleetPanel、PortPanel、DeveloperHUD、Icon；F3状态、选择、镜头目标属于客户端。正式HUD不虚构经济数据。Port/Fleet/Command/Clock/深冻结Snapshot保持不变，未添加贸易或城市业务状态。

## Task04 渲染边界

主港位置保持(-90,-30)，次级港口通过唯一Data定义移到圣胡安(240,-50)、圣多明各(85,-155)、拿骚(-160,205)，保留稳定ID。不是mesh偏移；导航与snapshot自动使用同一新坐标，核心算法不变。目的是给英雄港地形留空间，避免地块重叠。

源文件与manifest声明模块布局，Runtime加载GLB与共享PBR图片。VisualAssetLibrary规范化图片URL且只允许同源/assets；没有网络业务。地表高度近似在海面shader中复用以匹配岸边效果，不成为导航避障。PortRenderer在全览或目标附近展示次级港口；Ocean使用相同显示条件，避免留下独立浅水圆斑。

右侧只显示一个对象面板；选港后保留客户端舰队选择以确认前往。顶部时钟为simulationTime派生的分秒，不是存档日期。菜单只有已实现的相机/调试/返回操作，不虚构经济或任务入口。

## Task05 表现层增量

新增模块、材质图集、双 UV 和整岛烘焙均属于 Blender 资产层，manifest.havana 只描述视觉摆放。createPortVisual 在定位完成后缓存静态节点世界矩阵；舰队动态变换不冻结，仍严格来自 Snapshot。默认镜头与哈瓦那聚焦目标统一为 (-128, 0, 30)。art-hud.css 作为统一视觉主题覆盖，不增加游戏系统或权威状态。Simulation 与 Data 本轮没有改动。
