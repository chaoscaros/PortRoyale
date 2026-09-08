# 数据模型 · Phase 1

| 模型 | Owner | Mutable? | Snapshot? | Future Save? | Source File |
|---|---|---|---|---|---|
| WorldPosition | Simulation | 坐标对象只读，内部整体替换 | 深冻结副本 | 是 | src/simulation/world/types.ts |
| PortId | Data | 否，branded string | 是 | 以 ID 引用 | 同上 |
| PortDefinition | Data | 否 | 注册表复制投影 | 定义版本/ID | 同上；src/data/ports/portDefinitions.ts |
| PortSnapshot | Simulation projection | 否 | 是，含 position 冻结 | 不重复保存定义 | types.ts；PortRegistry.ts |
| FleetId | Simulation | 否，branded string | 是 | 是 | types.ts |
| FleetStatus | Simulation | 内部可变 | docked/sailing | 是 | types.ts |
| FleetState | Simulation Map | 内部可变 | 不能外泄原对象 | 是 | types.ts；Simulation.ts |
| FleetSnapshot | Simulation projection | 否，深冻结 | 是 | heading 可重建 | types.ts；Simulation.ts |
| MoveFleetCommand | Input → Simulation | 只读意图 | 否 | 未来可重放 | types.ts |
| SelectionState | GameApplication client | 整体替换 | 不属于 WorldSnapshot | 否 | src/input/SelectionState.ts |

WorldPosition = {x,z}；WORLD_DISTANCE_UNIT = 1 simulation world unit = 1 Babylon horizontal world unit。资产维持 1 米，不代表地图严格对应真实海里或地理投影。

PortDefinition/PortSnapshot：id、displayName、position。四港：port-havana 哈瓦那(-90,-30)、port-san-juan 圣胡安(120,-20)、port-santo-domingo 圣多明各(35,-50)、port-nassau 拿骚(-60,45)。无 nation、market、stock、人口字段。

FleetState：id、position、status、currentPortId、destinationPortId、speed。初始 fleet-player-001 停泊哈瓦那，speed=8 世界单位/模拟秒，destination=null。内部 Map 支持多实体形态，当前配置只创建一个。

FleetSnapshot 增加派生 heading：atan2(dx,dz)；docked 用港口默认朝向 0。WorldSnapshot：clock、ports、fleets。不存在 selection、Mesh、相机和权威 ETA。

MoveFleetCommand = {type:'move-fleet',fleetId,destinationPortId}。返回 CommandResult outcome accepted/noop/rejected，原因可为 fleet-not-found、port-not-found、fleet-unavailable、already-docked、already-sailing。非法命令不改变世界；同当前停泊港、同正在前往目标 no-op；改道保留原实时位置。

未来 cargo、ships、crew、route、market、nation 只在对应阶段扩展，不提前留空业务字段。存档仍仅文档设计，必须 saveVersion。
