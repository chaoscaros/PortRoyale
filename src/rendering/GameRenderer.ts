import {
  Engine,
  Scene,
  Vector3,
  PointerEventTypes,
  SceneInstrumentation,
  type ArcRotateCamera,
} from "@babylonjs/core";
import type { WorldSnapshot } from "../simulation/Simulation";
import type { WorldPosition } from "../simulation/world/types";
import { createStrategyCamera } from "../input/StrategyCamera";
import { createOcean } from "./ocean/createOcean";
import { createEnvironment } from "./environment/createEnvironment";
import { VisualAssetLibrary } from "./assets/VisualAssetLibrary";
import { PortRenderer } from "./ports/PortRenderer";
import { FleetRenderer } from "./fleets/FleetRenderer";
import type { PickTarget, SelectionState } from "../input/SelectionState";
export class GameRenderer {
  private readonly engine: Engine;
  private readonly scene: Scene;
  private readonly camera: ArcRotateCamera;
  private readonly ocean;
  private readonly environment;
  private readonly assets: VisualAssetLibrary;
  private readonly ports: PortRenderer;
  private readonly fleets: FleetRenderer;
  private readonly instrumentation: SceneInstrumentation;
  private assetsReady = false;
  private disposed = false;
  private focusTarget: { position: Vector3; radius: number } | null = null;
  readonly ready: Promise<void>;
  constructor(
    canvas: HTMLCanvasElement,
    labels: HTMLElement,
    initial: WorldSnapshot,
    onPick: (target: PickTarget) => void,
  ) {
    this.engine = new Engine(canvas, true, { preserveDrawingBuffer: false });
    this.engine.setHardwareScalingLevel(1);
    this.scene = new Scene(this.engine);
    this.scene.useRightHandedSystem = true;
    this.instrumentation = new SceneInstrumentation(this.scene);
    this.camera = createStrategyCamera(this.scene, canvas);
    this.environment = createEnvironment(this.scene, this.camera);
    this.ocean = createOcean(this.scene, initial.ports);
    this.assets = new VisualAssetLibrary(this.scene);
    this.ports = new PortRenderer(
      this.scene,
      labels,
      onPick,
      this.assets,
      this.environment.shadows,
    );
    this.fleets = new FleetRenderer(
      this.scene,
      this.assets,
      this.environment.shadows,
    );
    this.scene.onPointerObservable.add((info) => {
      if (info.type === PointerEventTypes.POINTERMOVE)
        canvas.style.cursor = info.pickInfo?.pickedMesh?.metadata?.pickTarget
          ? "pointer"
          : "grab";
      if (info.type === PointerEventTypes.POINTERDOWN) this.focusTarget = null;
      if (
        info.type === PointerEventTypes.POINTERTAP &&
        info.event.button === 0
      ) {
        const target = info.pickInfo?.pickedMesh?.metadata?.pickTarget as
          PickTarget | undefined;
        if (target) onPick(target);
      }
    });
    this.ready = this.assets
      .load()
      .then(async () => {
        if (this.disposed) return;
        await this.fleets.initialize(initial.fleets);
        if (!this.disposed) {
          this.assetsReady = true;
          this.ports.update(initial.ports, {
            selectedFleetId: null,
            selectedPortId: null,
          });
        }
      })
      .catch((error) => {
        if (!this.disposed) throw error;
      });
  }
  focus(position: WorldPosition, radius = 190) {
    this.focusTarget = {
      position: new Vector3(position.x, 0, position.z),
      radius,
    };
  }
  render(snapshot: WorldSnapshot, selection: SelectionState) {
    this.engine.beginFrame();
    if (this.focusTarget) {
      const a = Math.min(1, this.engine.getDeltaTime() / 180);
      this.camera.target = Vector3.Lerp(
        this.camera.target,
        this.focusTarget.position,
        a,
      );
      this.camera.radius += (this.focusTarget.radius - this.camera.radius) * a;
      if (
        Vector3.Distance(this.camera.target, this.focusTarget.position) <
          0.05 &&
        Math.abs(this.camera.radius - this.focusTarget.radius) < 0.05
      )
        this.focusTarget = null;
    }
    this.ocean.update(snapshot.clock.simulationTime);
    if (this.assetsReady)
      this.fleets.update(
        snapshot.fleets,
        snapshot.ports,
        selection,
        snapshot.clock.simulationTime,
      );
    this.assets.updateDetail(this.camera.position);
    this.scene.render();
    this.engine.endFrame();
    if (this.assetsReady) this.ports.update(snapshot.ports, selection, snapshot.fleets);
  }
  getStats() {
    return {
      drawCalls: this.instrumentation.drawCallsCounter.current,
      activeMeshes: this.scene.getActiveMeshes().length,
      textures: this.engine.getLoadedTexturesCache().length,
    };
  }
  resize() {
    this.engine.resize();
  }
  dispose() {
    this.disposed = true;
    this.ports.dispose();
    this.fleets.dispose();
    this.assets.dispose();
    this.environment.dispose();
    this.instrumentation.dispose();
    this.scene.dispose();
    this.engine.dispose();
  }
}
