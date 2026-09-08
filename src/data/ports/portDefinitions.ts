import type { PortDefinition, PortId } from "../../simulation/world/types";
export const PORT_IDS = {
  havana: "port-havana" as PortId,
  sanJuan: "port-san-juan" as PortId,
  santoDomingo: "port-santo-domingo" as PortId,
  nassau: "port-nassau" as PortId,
} as const;
export const portDefinitions: readonly PortDefinition[] = Object.freeze(
  [
    {
      id: PORT_IDS.havana,
      displayName: "哈瓦那",
      position: { x: -90, z: -30 },
    },
    {
      id: PORT_IDS.sanJuan,
      displayName: "圣胡安",
      position: { x: 240, z: -50 },
    },
    {
      id: PORT_IDS.santoDomingo,
      displayName: "圣多明各",
      position: { x: 85, z: -155 },
    },
    { id: PORT_IDS.nassau, displayName: "拿骚", position: { x: -160, z: 205 } },
  ].map((p) => Object.freeze({ ...p, position: Object.freeze(p.position) })),
);
