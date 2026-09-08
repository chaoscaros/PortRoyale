import {
  Color3,
  MeshBuilder,
  StandardMaterial,
  Vector3,
  type LinesMesh,
  type Scene,
  type TransformNode,
} from "@babylonjs/core";
import { loadTestShip } from "../assets/loadTestShip";
import type {
  FleetId,
  FleetSnapshot,
  PortSnapshot,
} from "../../simulation/world/types";
import type { PickTarget, SelectionState } from "../../input/SelectionState";
export class FleetRenderer {
  private readonly roots = new Map<FleetId, TransformNode>();
  private disposed = false;
  private readonly selectionRing;
  private route: LinesMesh;
  constructor(private readonly scene: Scene) {
    this.selectionRing = MeshBuilder.CreateTorus(
      "fleet-selection",
      { diameter: 25, thickness: 0.5, tessellation: 48 },
      scene,
    );
    const material = new StandardMaterial("fleet-selection-gold", scene);
    material.emissiveColor = Color3.FromHexString("#f1d18d");
    this.selectionRing.material = material;
    this.selectionRing.isPickable = false;
    this.selectionRing.setEnabled(false);
    this.route = MeshBuilder.CreateLines(
      "fleet-route",
      { points: [Vector3.Zero(), Vector3.Zero()], updatable: true },
      scene,
    );
    this.route.color = Color3.FromHexString("#e6c17b");
    this.route.isPickable = false;
    this.route.setEnabled(false);
  }
  async initialize(fleets: readonly FleetSnapshot[]) {
    for (const fleet of fleets) {
      const root = await loadTestShip(this.scene);
      if (this.disposed) {
        root.dispose();
        return;
      }
      root.name = `fleet:${fleet.id}`;
      for (const mesh of root.getChildMeshes())
        mesh.metadata = {
          pickTarget: { kind: "fleet", id: fleet.id } satisfies PickTarget,
        };
      this.roots.set(fleet.id, root);
      root.position.set(fleet.position.x, 0.6, fleet.position.z);
      root.rotation.y = fleet.heading;
    }
  }
  update(
    fleets: readonly FleetSnapshot[],
    ports: readonly PortSnapshot[],
    selection: SelectionState,
  ) {
    this.selectionRing.setEnabled(false);
    this.route.setEnabled(false);
    for (const fleet of fleets) {
      const root = this.roots.get(fleet.id);
      if (!root) continue;
      root.position.set(fleet.position.x, 0.6, fleet.position.z);
      root.rotation.y = fleet.heading;
      if (selection.selectedFleetId !== fleet.id) continue;
      this.selectionRing.setEnabled(true);
      this.selectionRing.position.set(fleet.position.x, 0.9, fleet.position.z);
      const target = ports.find((port) => port.id === fleet.destinationPortId);
      if (target) {
        this.route = MeshBuilder.CreateLines(
          "fleet-route",
          {
            points: [
              new Vector3(fleet.position.x, 1, fleet.position.z),
              new Vector3(target.position.x, 1, target.position.z),
            ],
            instance: this.route,
          },
          this.scene,
        );
        this.route.setEnabled(true);
      }
    }
  }
  dispose() {
    this.disposed = true;
    for (const root of this.roots.values()) root.dispose(false, true);
    this.roots.clear();
    this.route.dispose();
    this.selectionRing.dispose(false, true);
  }
}
