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
}
export class GameApplication {
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
  private assetStatus = "正在加载测试船…";
  private readonly resizeObserver: ResizeObserver;
  constructor(
    canvas: HTMLCanvasElement,
    private readonly publish: (state: DebugSnapshot) => void,
  ) {
    this.renderer = new GameRenderer(canvas);
    this.resizeObserver = new ResizeObserver(() => this.renderer.resize());
    this.resizeObserver.observe(canvas);
    document.addEventListener("visibilitychange", this.visibilityChanged);
    this.renderer.ready
      .then(() => {
        if (!this.disposed) {
          this.assetStatus = "GLB 方向与尺度已验证";
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
    });
  }
  dispatch(command: Command) {
    this.simulation.dispatch(command);
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
    this.renderer.render(this.simulation.snapshot());
    this.sampleSeconds += elapsed;
    this.sampleFrames++;
    if (this.sampleSeconds >= 1) {
      this.fps = Math.round(this.sampleFrames / this.sampleSeconds);
      this.tps = Math.round(this.sampleTicks / this.sampleSeconds);
      this.sampleSeconds = 0;
      this.sampleFrames = 0;
      this.sampleTicks = 0;
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
