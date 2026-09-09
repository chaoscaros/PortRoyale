import {
  Color3,
  MeshBuilder,
  Vector3,
  type LinesMesh,
  type Scene,
  type ShadowGenerator,
} from "@babylonjs/core";
import { loadTestShip } from "../assets/loadTestShip";
import { VisualAssetLibrary } from "../assets/VisualAssetLibrary";
import { ShipWake } from "../effects/ShipWake";
import { TransformNode } from "@babylonjs/core";
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
  private readonly wakes = new Map<FleetId, ShipWake>();
  private readonly direction;
  private route: LinesMesh;
  constructor(
    private readonly scene: Scene,
    private readonly assets: VisualAssetLibrary,
    private readonly shadows: ShadowGenerator,
  ) {
    const arcs = Array.from({ length: 3 }, (_, sector) =>
      Array.from({ length: 25 }, (_, i) => {
        const angle = (sector * Math.PI * 2) / 3 + (i / 24) * Math.PI * 0.49;
        return new Vector3(Math.cos(angle) * 20, 0, Math.sin(angle) * 20);
      }),
    );
    this.selectionRing = MeshBuilder.CreateLineSystem(
      "fleet-bearing-arcs",
      { lines: arcs },
      scene,
    );
    this.selectionRing.color = Color3.FromHexString("#ab9467");
    this.selectionRing.alpha = 0.72;
    this.selectionRing.isPickable = false;
    this.selectionRing.setEnabled(false);
    this.direction = MeshBuilder.CreateLines(
      "fleet-direction",
      {
        points: [
          new Vector3(-1.3, 0, 19),
          new Vector3(0, 0, 22),
          new Vector3(1.3, 0, 19),
        ],
      },
      scene,
    );
    this.direction.color = Color3.FromHexString("#c4b08b");
    this.direction.isPickable = false;
    this.direction.setEnabled(false);
    this.route = MeshBuilder.CreateDashedLines(
      "fleet-route",
      {
        points: [Vector3.Zero(), new Vector3(0, 0, 1)],
        dashSize: 2,
        gapSize: 3,
        dashNb: 60,
        updatable: true,
      },
      scene,
    );
    this.route.color = Color3.FromHexString("#b5b698");
    this.route.isPickable = false;
    this.route.alwaysSelectAsActiveMesh = true;
    this.route.setEnabled(false);
  }
  async initialize(fleets: readonly FleetSnapshot[]) {
    const calibration = await loadTestShip(this.scene);
    calibration.dispose(false, true);
    if (this.disposed) return;
    for (const fleet of fleets) {
      const parent = new TransformNode(`fleet-anchor:${fleet.id}`, this.scene);
      const root = this.assets.place("sloop", parent, 0, 0, 0, 0, this.shadows);
      this.wakes.set(fleet.id, new ShipWake(this.scene));
      if (this.disposed) {
        root.dispose();
        return;
      }
      root.name = `fleet:${fleet.id}`;
      for (const mesh of root.getChildMeshes()) {
        mesh.isPickable = true;
        mesh.metadata = {
          pickTarget: { kind: "fleet", id: fleet.id } satisfies PickTarget,
        };
      }
      this.roots.set(fleet.id, root);
      root.position.set(fleet.position.x, 0.02, fleet.position.z);
      root.rotation.y = fleet.status === "docked" ? 0.95 : fleet.heading;
    }
  }
  update(
    fleets: readonly FleetSnapshot[],
    ports: readonly PortSnapshot[],
    selection: SelectionState,
    time: number,
  ) {
    this.selectionRing.setEnabled(false);
    this.direction.setEnabled(false);
    this.route.setEnabled(false);
    for (const fleet of fleets) {
      const root = this.roots.get(fleet.id);
      if (!root) continue;
      root.position.set(fleet.position.x, 0.02, fleet.position.z);
      root.rotation.y = fleet.status === "docked" ? 0.95 : fleet.heading;
      root.position.y = 0.02 + Math.sin(time * 1.1) * 0.06;
      root.rotation.z = Math.sin(time * 0.8) * 0.012;
      root.rotation.x = Math.cos(time * 0.7) * 0.007;
      this.wakes.get(fleet.id)?.update(fleet, time);
      if (selection.selectedFleetId !== fleet.id) continue;
      this.selectionRing.setEnabled(true);
      this.selectionRing.position.set(fleet.position.x, 0.12, fleet.position.z);
      this.direction.setEnabled(true);
      this.direction.position.copyFrom(this.selectionRing.position);
      this.direction.rotation.y =
        fleet.status === "docked" ? 0.95 : fleet.heading;
      const target = ports.find((port) => port.id === fleet.destinationPortId);
      if (target) {
        this.route = MeshBuilder.CreateDashedLines(
          "fleet-route",
          {
            points: [
              new Vector3(fleet.position.x, 0.15, fleet.position.z),
              new Vector3(target.position.x, 0.15, target.position.z),
            ],
            instance: this.route,
          },
          this.scene,
        );
        this.route.alpha = 0.52 + Math.sin(time * 0.7) * 0.08;
        this.route.setEnabled(true);
      }
    }
  }
  dispose() {
    this.disposed = true;
    for (const root of this.roots.values()) root.dispose(false, true);
    this.roots.clear();
    for (const wake of this.wakes.values()) wake.dispose();
    this.wakes.clear();
    this.direction.dispose();
    this.route.dispose();
    this.selectionRing.dispose(false, true);
  }
}
