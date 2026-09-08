import {
  SimulationClock,
  type ClockSnapshot,
  type TimeScale,
} from "./SimulationClock";
import { worldDefinition } from "../data/worldDefinition";
import { PortRegistry } from "./world/PortRegistry";
import { FleetNavigationSystem } from "./systems/FleetNavigationSystem";
import type {
  CommandResult,
  FleetId,
  FleetSnapshot,
  FleetState,
  MoveFleetCommand,
  PortDefinition,
  PortId,
  PortSnapshot,
} from "./world/types";
export type Command =
  | { type: "SetPaused"; paused: boolean }
  | { type: "SetTimeScale"; timeScale: TimeScale }
  | MoveFleetCommand;
export interface WorldSnapshot {
  readonly clock: ClockSnapshot;
  readonly ports: readonly PortSnapshot[];
  readonly fleets: readonly FleetSnapshot[];
}
export interface WorldDefinition {
  readonly ports: readonly PortDefinition[];
  readonly initialPortId: PortId;
  readonly fleetId: FleetId;
  readonly fleetSpeed: number;
}
export class Simulation {
  private readonly clock: SimulationClock;
  private readonly ports: PortRegistry;
  private readonly fleets = new Map<FleetId, FleetState>();
  private readonly navigation = new FleetNavigationSystem();
  constructor(
    ticksPerSecond = 10,
    definition: WorldDefinition = worldDefinition,
  ) {
    this.clock = new SimulationClock(ticksPerSecond);
    this.ports = new PortRegistry(definition.ports);
    const origin = this.ports.get(definition.initialPortId);
    if (
      !origin ||
      !definition.fleetId ||
      !Number.isFinite(definition.fleetSpeed) ||
      definition.fleetSpeed <= 0
    )
      throw new Error("Invalid initial fleet");
    this.fleets.set(definition.fleetId, {
      id: definition.fleetId,
      position: { ...origin.position },
      status: "docked",
      currentPortId: origin.id,
      destinationPortId: null,
      speed: definition.fleetSpeed,
    });
  }
  dispatch(command: Command): CommandResult {
    switch (command.type) {
      case "SetPaused":
        this.clock.setPaused(command.paused);
        return { outcome: "accepted" };
      case "SetTimeScale":
        this.clock.setTimeScale(command.timeScale);
        return { outcome: "accepted" };
      case "move-fleet": {
        const fleet = this.fleets.get(command.fleetId),
          port = this.ports.get(command.destinationPortId);
        if (!fleet) return { outcome: "rejected", reason: "fleet-not-found" };
        if (!port) return { outcome: "rejected", reason: "port-not-found" };
        if (!["docked", "sailing"].includes(fleet.status))
          return { outcome: "rejected", reason: "fleet-unavailable" };
        if (fleet.status === "docked" && fleet.currentPortId === port.id)
          return { outcome: "noop", reason: "already-docked" };
        if (fleet.status === "sailing" && fleet.destinationPortId === port.id)
          return { outcome: "noop", reason: "already-sailing" };
        fleet.status = "sailing";
        fleet.currentPortId = null;
        fleet.destinationPortId = port.id;
        return { outcome: "accepted" };
      }
    }
  }
  advance(seconds: number) {
    return this.clock.advance(seconds, (dt) =>
      this.navigation.tick(this.fleets.values(), this.ports, dt),
    );
  }
  snapshot(): WorldSnapshot {
    return Object.freeze({
      clock: this.clock.snapshot(),
      ports: this.ports.snapshots,
      fleets: Object.freeze(
        [...this.fleets.values()].map((fleet) => {
          const target = fleet.destinationPortId
            ? this.ports.get(fleet.destinationPortId)
            : undefined;
          // Docked vessels use a stable port heading (+Z); sailing heading is derived.
          const heading = target
            ? Math.atan2(
                target.position.x - fleet.position.x,
                target.position.z - fleet.position.z,
              )
            : 0;
          return Object.freeze({
            ...fleet,
            position: Object.freeze({ ...fleet.position }),
            heading,
          });
        }),
      ),
    });
  }
}
