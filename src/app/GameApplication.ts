import type { PickTarget, SelectionState } from "../input/SelectionState";
import {
  Simulation,
  type Command,
  type WorldSnapshot,
} from "../simulation/Simulation";
import { GameRenderer } from "../rendering/GameRenderer";
export interface DebugSnapshot {
  world: WorldSnapshot;
  fps: number;
  tps: number;
  assetStatus: string;
  selection: SelectionState;
  commandMessage: string;
}
export class GameApplication {
  private selection: SelectionState = {
    selectedFleetId: null,
    selectedPortId: null,
  };
  private commandMessage = "";
  private publishSeconds = 0;
  private readonly simulation = new Simulation(10);
  private readonly renderer: GameRenderer;
  private frame = 0;
  private previous = performance.now();
  private sampleSeconds = 0;
  private sampleFrames = 0;
  private sampleTicks = 0;
  private fps = 0;
  private tps = 0;
  private disposed = false;
  private assetStatus = "正在加载港口与帆船…";
  private readonly resizeObserver: ResizeObserver;
  constructor(
    canvas: HTMLCanvasElement,
    labels: HTMLElement,
    private readonly publish: (state: DebugSnapshot) => void,
  ) {
    this.renderer = new GameRenderer(
      canvas,
      labels,
      this.simulation.snapshot(),
      (target) => this.select(target),
    );
    this.resizeObserver = new ResizeObserver(() => this.renderer.resize());
    this.resizeObserver.observe(canvas);
    document.addEventListener("visibilitychange", this.visibilityChanged);
    this.renderer.ready
      .then(() => {
        if (!this.disposed) {
          this.assetStatus = "视觉资产就绪 · GLB 校准通过";
          this.emit();
        }
      })
      .catch((error: unknown) => {
        if (!this.disposed) {
          this.assetStatus = `资源错误：${String(error)}`;
          this.emit();
        }
      });
    this.emit();
    this.frame = requestAnimationFrame(this.update);
  }
  private visibilityChanged = () => {
    this.previous = performance.now();
  };
  private emit() {
    this.publish({
      world: this.simulation.snapshot(),
      fps: this.fps,
      tps: this.tps,
      assetStatus: this.assetStatus,
      selection: this.selection,
      commandMessage: this.commandMessage,
    });
  }
  select(target: PickTarget) {
    this.selection =
      target.kind === "fleet"
        ? { ...this.selection, selectedFleetId: target.id }
        : { ...this.selection, selectedPortId: target.id };
    this.commandMessage = "";
    this.emit();
  }
  clearSelection(kind: "fleet" | "port") {
    this.selection =
      kind === "fleet"
        ? { ...this.selection, selectedFleetId: null }
        : { ...this.selection, selectedPortId: null };
    this.commandMessage = "";
    this.emit();
  }
  focusView(mode: "fleet" | "havana" | "world") {
    const world = this.simulation.snapshot();
    if (mode === "world") this.renderer.focus({ x: 0, z: 15 }, 430);
    else if (mode === "fleet")
      this.renderer.focus(world.fleets[0].position, 100);
    else {
      const p = world.ports[0].position;
      this.renderer.focus({ x: p.x - 25, z: p.z + 35 }, 205);
    }
  }
  dispatch(command: Command) {
    const result = this.simulation.dispatch(command);
    if (command.type === "move-fleet")
      this.commandMessage =
        result.outcome === "accepted"
          ? "航行指令已下达"
          : result.outcome === "noop"
            ? "舰队已在此港或正前往此港"
            : "航行指令被拒绝，请重新选择舰队和港口";
    this.emit();
  }
  private update = (now: number) => {
    if (this.disposed) return;
    // Host policy: cap stalls to 250ms and don't simulate hidden-tab time.
    const elapsed = document.hidden
      ? 0
      : Math.min(0.25, Math.max(0, (now - this.previous) / 1000));
    this.previous = now;
    this.sampleTicks += this.simulation.advance(elapsed);
    this.renderer.render(this.simulation.snapshot(), this.selection);
    this.sampleSeconds += elapsed;
    this.sampleFrames++;
    if (this.sampleSeconds >= 1) {
      this.fps = Math.round(this.sampleFrames / this.sampleSeconds);
      this.tps = Math.round(this.sampleTicks / this.sampleSeconds);
      this.sampleSeconds = 0;
      this.sampleFrames = 0;
      this.sampleTicks = 0;
    }
    this.publishSeconds += elapsed;
    if (this.publishSeconds >= 0.1) {
      this.publishSeconds = 0;
      this.emit();
    }
    this.frame = requestAnimationFrame(this.update);
  };
  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.frame);
    this.resizeObserver.disconnect();
    document.removeEventListener("visibilitychange", this.visibilityChanged);
    this.renderer.dispose();
  }
}
