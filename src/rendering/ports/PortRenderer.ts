import {
  ArcRotateCamera,
  Matrix,
  TransformNode,
  Vector3,
  type Scene,
  type ShadowGenerator,
} from "@babylonjs/core";
import type { PortId, PortSnapshot } from "../../simulation/world/types";
import { createPortVisual } from "./createPortVisual";
import type { VisualAssetLibrary } from "../assets/VisualAssetLibrary";
import type { PickTarget, SelectionState } from "../../input/SelectionState";
export class PortRenderer {
  private readonly entries = new Map<
    PortId,
    {
      root: TransformNode;
      button: HTMLButtonElement;
    }
  >();
  constructor(
    private readonly scene: Scene,
    private readonly labels: HTMLElement,
    private readonly onPick: (target: PickTarget) => void,
    private readonly assets: VisualAssetLibrary,
    private readonly shadows: ShadowGenerator,
  ) {}
  update(ports: readonly PortSnapshot[], selection: SelectionState) {
    for (const port of ports) {
      if (this.entries.has(port.id)) continue;
      const root = new TransformNode(`port:${port.id}`, this.scene);
      root.position.set(port.position.x, 0, port.position.z);
      createPortVisual(this.scene, port, root, this.assets, this.shadows);
      for (const mesh of root.getChildMeshes()) {
        if (mesh.name.includes("pier") || mesh.name.includes("lighthouse")) {
          mesh.isPickable = true;
          mesh.metadata = {
            pickTarget: { kind: "port", id: port.id } satisfies PickTarget,
          };
        }
      }
      const button = document.createElement("button");
      button.className = "port-label";
      const emblem = document.createElement("span");
      emblem.className = "port-emblem";
      emblem.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M6 20h12M8 20l2-11h4l2 11M9 9h6V5H9zM12 2v3M7 13l-3 2m13-2 3 2"/></svg>';
      const name = document.createElement("span");
      name.textContent = port.displayName;
      button.append(emblem, name);
      button.setAttribute("aria-label", `选择港口 ${port.displayName}`);
      button.onclick = () => this.onPick({ kind: "port", id: port.id });
      this.labels.append(button);
      this.entries.set(port.id, { root, button });
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
      const showPort =
        port.id === "port-havana" ||
        !(camera instanceof ArcRotateCamera) ||
        camera.radius > 330 ||
        Vector3.Distance(camera.target, entry.root.position) < 80;
      entry.root.setEnabled(showPort);
      const anchor = new Vector3(port.position.x + 17, 4, port.position.z + 14);
      const screen = Vector3.Project(
        anchor,
        Matrix.Identity(),
        this.scene.getTransformMatrix(),
        viewport,
      );
      const x = (screen.x / engine.getRenderWidth()) * this.labels.clientWidth,
        y = (screen.y / engine.getRenderHeight()) * this.labels.clientHeight;
      entry.button.style.display =
        !showPort ||
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
