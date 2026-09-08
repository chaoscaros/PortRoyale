import type { FleetId, PortId } from "../simulation/world/types";
export interface SelectionState {
  readonly selectedFleetId: FleetId | null;
  readonly selectedPortId: PortId | null;
}
export type PickTarget =
  { kind: "fleet"; id: FleetId } | { kind: "port"; id: PortId };
