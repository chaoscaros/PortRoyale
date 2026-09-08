import type { PortRegistry } from "../world/PortRegistry";
import { distance, type FleetState } from "../world/types";
/** One authoritative update for the entire collection, called only on fixed ticks. */
export class FleetNavigationSystem {
  tick(fleets: Iterable<FleetState>, ports: PortRegistry, dt: number) {
    for (const fleet of fleets) {
      if (fleet.status !== "sailing" || !fleet.destinationPortId) continue;
      const target = ports.get(fleet.destinationPortId);
      if (!target) throw new Error("World invariant: missing destination");
      const remaining = distance(fleet.position, target.position),
        step = fleet.speed * dt;
      if (remaining <= step) {
        fleet.position = { ...target.position };
        fleet.status = "docked";
        fleet.currentPortId = target.id;
        fleet.destinationPortId = null;
      } else {
        const ratio = step / remaining;
        fleet.position = {
          x: fleet.position.x + (target.position.x - fleet.position.x) * ratio,
          z: fleet.position.z + (target.position.z - fleet.position.z) * ratio,
        };
      }
    }
  }
}
