import type { PortDefinition, PortId, PortSnapshot } from "./types";
export class PortRegistry {
  private readonly ports = new Map<PortId, PortSnapshot>();
  readonly snapshots: readonly PortSnapshot[];
  constructor(definitions: readonly PortDefinition[]) {
    for (const port of definitions) {
      if (
        !port.id ||
        this.ports.has(port.id) ||
        !port.displayName.trim() ||
        !Number.isFinite(port.position.x) ||
        !Number.isFinite(port.position.z)
      )
        throw new Error("Invalid port definition");
      this.ports.set(
        port.id,
        Object.freeze({
          ...port,
          position: Object.freeze({ ...port.position }),
        }),
      );
    }
    this.snapshots = Object.freeze([...this.ports.values()]);
  }
  get(id: PortId) {
    return this.ports.get(id);
  }
}
