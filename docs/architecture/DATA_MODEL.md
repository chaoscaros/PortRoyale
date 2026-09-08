# 数据模型

## 当前实现

ClockSnapshot：simulationTime、tickCount、timeScale (1|2|4)、paused。WorldSnapshot：只读 clock。Command：SetPaused、SetTimeScale。快照与内层 clock 均 freeze；没有将内部可变对象泄露给 UI。

## 目标模型（仅设计，未实现）

```ts
type PortId = string;
type NationId = string;
type FleetId = string;
interface WorldPosition { x: number; z: number } // 米；地表平面
interface PortDefinition {
  id: PortId;
  displayName: string;
  position: WorldPosition;
  nationId: NationId;
}
interface WorldMapDefinition {
  id: string;
  bounds: { minX: number; maxX: number; minZ: number; maxZ: number };
  ports: PortDefinition[];
}
interface FleetState {
  id: FleetId;
  position: WorldPosition;
  destinationPortId: PortId | null;
  speed: number; // 米 / 模拟秒
  shipIds: string[]; // 1..N
}
```

Nation 仅 ID 边界，不实现完整国家。货物、船员、路线、航线避障和事件模型在对应阶段补充。渲染 FleetId → TransformNode，向量转换只发生在渲染层。
