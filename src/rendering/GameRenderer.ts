import {
  Color3,
  Color4,
  Engine,
  HemisphericLight,
  Mesh,
  MeshBuilder,
  Scene,
  StandardMaterial,
  Vector3,
  PointerEventTypes,
} from "@babylonjs/core";
import type { WorldSnapshot } from "../simulation/Simulation";
import { createStrategyCamera } from "../input/StrategyCamera";
import { createOcean } from "./ocean/createOcean";
import { PortRenderer } from "./ports/PortRenderer";
import { FleetRenderer } from "./fleets/FleetRenderer";
import type { PickTarget, SelectionState } from "../input/SelectionState";
export class GameRenderer {
  private readonly engine: Engine;
  private readonly scene: Scene;
  private readonly ocean;
  readonly ready: Promise<void>;
  private readonly ports: PortRenderer;
  private readonly fleets: FleetRenderer;
  private disposed = false;
  constructor(
    canvas: HTMLCanvasElement,
    labels: HTMLElement,
    initial: WorldSnapshot,
    onPick: (target: PickTarget) => void,
  ) {
    this.engine = new Engine(canvas, true, { preserveDrawingBuffer: false });
    this.engine.setHardwareScalingLevel(
      Math.max(1, window.devicePixelRatio / 1.5),
    );
    this.scene = new Scene(this.engine);
    this.scene.useRightHandedSystem = true;
    this.scene.clearColor = new Color4(0.46, 0.68, 0.71, 1);
    createStrategyCamera(this.scene, canvas);
    const light = new HemisphericLight(
      "sunlight",
      new Vector3(-0.5, 1, -0.3),
      this.scene,
    );
    light.intensity = 1.5;
    light.groundColor = new Color3(0.22, 0.29, 0.3);
    const sky = MeshBuilder.CreateSphere(
      "sky",
      { diameter: 1900, segments: 16, sideOrientation: Mesh.BACKSIDE },
      this.scene,
    );
    const skyMat = new StandardMaterial("sky-material", this.scene);
    skyMat.disableLighting = true;
    skyMat.emissiveColor = new Color3(0.46, 0.68, 0.71);
    sky.material = skyMat;
    sky.isPickable = false;
    this.ocean = createOcean(this.scene);
    this.ports = new PortRenderer(this.scene, labels, onPick);
    this.fleets = new FleetRenderer(this.scene);
    this.scene.onPointerObservable.add((info) => {
      if (
        info.type === PointerEventTypes.POINTERTAP &&
        info.event.button === 0
      ) {
        const target = info.pickInfo?.pickedMesh?.metadata?.pickTarget as
          PickTarget | undefined;
        if (target) onPick(target);
      }
    });
    this.ready = this.fleets
      .initialize(initial.fleets)
      .then(() => undefined)
      .catch((error) => {
        if (!this.disposed) throw error;
      });
  }
  render(snapshot: WorldSnapshot, selection: SelectionState) {
    this.ocean.setFloat("time", snapshot.clock.simulationTime);
    this.fleets.update(snapshot.fleets, snapshot.ports, selection);
    this.scene.render();
    this.ports.update(snapshot.ports, selection);
  }
  resize() {
    this.engine.resize();
  }
  dispose() {
    this.disposed = true;
    this.ports.dispose();
    this.fleets.dispose();
    this.scene.dispose();
    this.engine.dispose();
  }
}
