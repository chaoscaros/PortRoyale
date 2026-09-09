# 系统状态

| 系统 | 状态 | 当前职责 |
|---|---|---|
| SimulationClock | Implemented | 10TPS 默认、pause、1/2/4、余数与模拟秒 |
| Port Definition / Projection | Implemented | Data 四港定义、PortRegistry 校验复制、冻结投影 |
| Simulation Command | Implemented | 时间命令、move-fleet 校验、拒绝/no-op/接受 |
| FleetNavigationSystem | Implemented | 集中 fixed tick、直线移动、精确抵达、改道 |
| Fleet Selection | Implemented | 客户端选船/港、确认前往、不污染世界 |
| Fleet Rendering | Implemented | ID→GLB、snapshot位置朝向、选中圈、目标线 |
| PortRenderer | Implemented | 模块化英雄港/次级港、铭牌投影、距离显隐、点击 |
| GameApplication | Implemented | frame、snapshot桥、10Hz HUD、1Hz统计、生命周期 |
| 运行验收 | 当前记录见AI_HANDOFF | 功能、视觉与性能分别记录 |
| 海路避障 | Planned | 当前直线可穿岛，不实施 |
| 经济/货舱/交易 | Planned | 延后，需用户确认画面达标并授权 |
| 存档/多人/战斗 | Planned | 未实现 |

执行顺序：宿主 elapsed → Clock fixed ticks → FleetNavigationSystem → Snapshot → Renderer/UI。新增系统需明确顺序，未来随机数必须种子化。

## Phase 1.5 Rendering

已接入英雄哈瓦那、双桅横帆船（历史资产键sloop）、阴影海面天空和尾流。VisualAssetLibrary管理36套基础GLB与4套LOD1容器、共享纹理及实例；舰队映射仍按ID读快照。F3调试默认隐藏，正式UI只派生可用状态。旧船保留加载校准后释放。岛屿/建筑/尾流不是Simulation系统，没有碰撞、风力或浮力计算。

## Task05 表现层增量（历史）

新增模块、材质图集、双 UV 和整岛烘焙均属于 Blender 资产层，manifest.havana 只描述视觉摆放。createPortVisual 在定位完成后缓存静态节点世界矩阵；舰队动态变换不冻结，仍严格来自 Snapshot。默认镜头与哈瓦那聚焦目标统一为 (-128, 0, 30)。art-hud.css 作为统一视觉主题覆盖，不增加游戏系统或权威状态。Simulation 与 Data 本轮没有改动。

## Task06 表现层边界

场地高程/台地/道路统一在art06_site.py，输出GLB、manifest.site和水深图，仅供Rendering。Simulation、Navigation、Command、Snapshot没有修改。VisualAssetLibrary按作者约定的规范材质名复用并冻结材质，静态港区缓存世界矩阵；动态Fleet继续读取Snapshot。

四套超预算模块接Babylon原生LOD1，不引入独立调度系统。PortRenderer根据投影后的帆船/地标包围区与HUD覆盖区选择铭牌位置；无可用位置时仅隐藏铭牌，港口列表保留操作入口。DeveloperHUD增加draw call、active mesh和GPU内部纹理计数，仅作为表现诊断，默认仍隐藏。
