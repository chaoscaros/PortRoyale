# 系统状态

| 系统 | 状态 | 当前职责 |
|---|---|---|
| SimulationClock | Implemented | 10TPS 默认、pause、1/2/4、余数与模拟秒 |
| Port Definition / Projection | Implemented | Data 四港定义、PortRegistry 校验复制、冻结投影 |
| Simulation Command | Implemented | 时间命令、move-fleet 校验、拒绝/no-op/接受 |
| FleetNavigationSystem | Implemented | 集中 fixed tick、直线移动、精确抵达、改道 |
| Fleet Selection | Implemented | 客户端选船/港、确认前往、不污染世界 |
| Fleet Rendering | Implemented | ID→GLB、snapshot位置朝向、选中圈、目标线 |
| PortRenderer | Implemented | 金色 marker、程序占位物、标签投影、远距简化、点击 |
| GameApplication | Implemented | frame、snapshot桥、10Hz HUD、1Hz统计、生命周期 |
| 运行验收 | Partial | Phase 0 有历史观察；Phase 1 当前页面无法连接，待验 |
| 海路避障 | Planned | 当前直线可穿岛，不实施 |
| 经济/货舱/交易 | Planned | 下一阶段独立授权 |
| 存档/多人/战斗 | Planned | 未实现 |

执行顺序：宿主 elapsed → Clock fixed ticks → FleetNavigationSystem → Snapshot → Renderer/UI。新增系统需明确顺序，未来随机数必须种子化。
