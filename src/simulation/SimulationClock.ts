export type TimeScale = 1 | 2 | 4;
export interface ClockSnapshot {
  readonly simulationTime: number;
  readonly tickCount: number;
  readonly timeScale: TimeScale;
  readonly paused: boolean;
}
/** Pure fixed-step clock. Seconds in/out; real time is supplied by the host. */
export class SimulationClock {
  readonly tickSeconds: number;
  private accumulator = 0;
  private tickCount = 0;
  private paused = false;
  private timeScale: TimeScale = 1;
  constructor(readonly ticksPerSecond = 10) {
    if (
      !Number.isInteger(ticksPerSecond) ||
      ticksPerSecond < 1 ||
      ticksPerSecond > 1000
    ) {
      throw new RangeError("ticksPerSecond must be an integer in [1, 1000]");
    }
    this.tickSeconds = 1 / ticksPerSecond;
  }
  setPaused(value: boolean) {
    this.paused = value;
  }
  setTimeScale(value: TimeScale) {
    if (![1, 2, 4].includes(value))
      throw new RangeError("Unsupported time scale");
    this.timeScale = value;
  }
  advance(elapsedSeconds: number, onTick: (dt: number) => void): number {
    if (!Number.isFinite(elapsedSeconds) || elapsedSeconds < 0)
      throw new RangeError("Invalid elapsed time");
    if (this.paused) return 0;
    this.accumulator += elapsedSeconds * this.timeScale;
    let ticks = 0;
    while (this.accumulator + 1e-10 >= this.tickSeconds) {
      this.accumulator = Math.max(0, this.accumulator - this.tickSeconds);
      this.tickCount++;
      onTick(this.tickSeconds);
      ticks++;
    }
    return ticks;
  }
  snapshot(): ClockSnapshot {
    return Object.freeze({
      simulationTime: this.tickCount * this.tickSeconds,
      tickCount: this.tickCount,
      paused: this.paused,
      timeScale: this.timeScale,
    });
  }
}
