import { PORT_IDS, portDefinitions } from "./ports/portDefinitions";
import type { FleetId } from "../simulation/world/types";
export const PLAYER_FLEET_ID = "fleet-player-001" as FleetId;
export const worldDefinition = Object.freeze({
  ports: portDefinitions,
  initialPortId: PORT_IDS.havana,
  fleetId: PLAYER_FLEET_ID,
  fleetSpeed: 8,
});
