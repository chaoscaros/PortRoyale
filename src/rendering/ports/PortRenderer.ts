import {
  Color3,
  Matrix,
  MeshBuilder,
  StandardMaterial,
  TransformNode,
  Vector3,
  type Scene,
} from "@babylonjs/core";
import type { PortId, PortSnapshot } from "../../simulation/world/types";
import type { PickTarget, SelectionState } from "../../input/SelectionState";
export class PortRenderer {
  private readonly entries = new Map<
    PortId,
    {
      root: TransformNode;
      button: HTMLButtonElement;
      material: StandardMaterial;
    }
  >();
  constructor(
    private readonly scene: Scene,
    private readonly labels: HTMLElement,
    private readonly onPick: (target: PickTarget) => void,
  ) {}
  update(ports: readonly PortSnapshot[], selection: SelectionState) {
    for (const port of ports) {
      if (this.entries.has(port.id)) continue;
      const root = new TransformNode(`port:${port.id}`, this.scene);
      root.position.set(port.position.x, 0, port.position.z);
      const material = new StandardMaterial(
        `port-marker:${port.id}`,
        this.scene,
      );
      material.diffuseColor = Color3.FromHexString("#d8b574");
      material.emissiveColor = Color3.FromHexString("#58401d");
      const ring = MeshBuilder.CreateTorus(
        `port-ring:${port.id}`,
        { diameter: 14, thickness: 0.8, tessellation: 32 },
        this.scene,
      );
      ring.parent = root;
      ring.position.set(0, 1, 17);
      ring.material = material;
      const beacon = MeshBuilder.CreateCylinder(
        `port-beacon:${port.id}`,
        { height: 9, diameterBottom: 3, diameterTop: 1.8, tessellation: 6 },
        this.scene,
      );
      beacon.parent = root;
      beacon.position.set(0, 5, 20);
      beacon.material = material;
      for (const mesh of [ring, beacon])
        mesh.metadata = {
          pickTarget: { kind: "port", id: port.id } satisfies PickTarget,
        };
      const island = MeshBuilder.CreateSphere(
        `port-island:${port.id}`,
        { diameter: 2, segments: 8 },
        this.scene,
      );
      island.parent = root;
      island.position.set(0, -2, 39);
      island.scaling.set(22, 6, 15);
      island.isPickable = false;
      const land = new StandardMaterial(`land:${port.id}`, this.scene);
      land.diffuseColor = Color3.FromHexString("#8f9972");
      land.specularColor = Color3.Black();
      island.material = land;
      const pier = MeshBuilder.CreateBox(
        `pier:${port.id}`,
        { width: 6, height: 1, depth: 15 },
        this.scene,
      );
      pier.parent = root;
      pier.position.set(0, 1, 25);
      pier.material = material;
      pier.metadata = beacon.metadata;
      const button = document.createElement("button");
      button.className = "port-label";
      button.textContent = port.displayName;
      button.setAttribute("aria-label", `选择港口 ${port.displayName}`);
      button.onclick = () => this.onPick({ kind: "port", id: port.id });
      this.labels.append(button);
      this.entries.set(port.id, { root, button, material });
    }
    const camera = this.scene.activeCamera;
    if (!camera) return;
    const engine = this.scene.getEngine(),
      viewport = camera.viewport.toGlobal(
        engine.getRenderWidth(),
        engine.getRenderHeight(),
      );
    for (const port of ports) {
      const entry = this.entries.get(port.id)!;
      const anchor = new Vector3(port.position.x, 11, port.position.z + 20);
      const screen = Vector3.Project(
        anchor,
        Matrix.Identity(),
        this.scene.getTransformMatrix(),
        viewport,
      );
      const x = (screen.x / engine.getRenderWidth()) * this.labels.clientWidth,
        y = (screen.y / engine.getRenderHeight()) * this.labels.clientHeight;
      entry.button.style.display =
        screen.z < 0 ||
        screen.z > 1 ||
        x < 0 ||
        x > this.labels.clientWidth ||
        y < 0 ||
        y > this.labels.clientHeight
          ? "none"
          : "";
      entry.button.style.left = `${x}px`;
      entry.button.style.top = `${y}px`;
      entry.button.classList.toggle(
        "far",
        Vector3.Distance(camera.position, anchor) > 330,
      );
      const selected = selection.selectedPortId === port.id;
      entry.button.setAttribute("aria-pressed", String(selected));
      entry.material.emissiveColor = Color3.FromHexString(
        selected ? "#a98534" : "#58401d",
      );
    }
  }
  dispose() {
    for (const { button, root } of this.entries.values()) {
      button.remove();
      root.dispose(false, true);
    }
    this.entries.clear();
  }
}
