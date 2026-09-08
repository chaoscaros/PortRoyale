export type PortId = string & { readonly __brand: "PortId" };
export type FleetId = string & { readonly __brand: "FleetId" };
export interface WorldPosition {
  readonly x: number;
  readonly z: number;
}
export interface PortDefinition {
  readonly id: PortId;
  readonly displayName: string;
  readonly position: WorldPosition;
}
export type PortSnapshot = PortDefinition;
export type FleetStatus = "docked" | "sailing";
export interface FleetState {
  readonly id: FleetId;
  position: WorldPosition;
  status: FleetStatus;
  currentPortId: PortId | null;
  destinationPortId: PortId | null;
  readonly speed: number;
}
export interface FleetSnapshot extends Readonly<FleetState> {
  readonly heading: number;
}
export interface MoveFleetCommand {
  readonly type: "move-fleet";
  readonly fleetId: FleetId;
  readonly destinationPortId: PortId;
}
export type CommandResult = {
  readonly outcome: "accepted" | "noop" | "rejected";
  readonly reason?:
    | "fleet-not-found"
    | "port-not-found"
    | "fleet-unavailable"
    | "already-docked"
    | "already-sailing";
};
export const WORLD_DISTANCE_UNIT =
  "1 simulation world unit = 1 Babylon horizontal world unit";
export function distance(a: WorldPosition, b: WorldPosition) {
  return Math.hypot(b.x - a.x, b.z - a.z);
}
