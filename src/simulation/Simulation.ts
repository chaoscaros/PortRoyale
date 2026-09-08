import {
  SimulationClock,
  type ClockSnapshot,
  type TimeScale,
} from "./SimulationClock";
export type Command =
  | { type: "SetPaused"; paused: boolean }
  | { type: "SetTimeScale"; timeScale: TimeScale };
export interface WorldSnapshot {
  readonly clock: ClockSnapshot;
}
export class Simulation {
  private readonly clock: SimulationClock;
  constructor(ticksPerSecond = 10) {
    this.clock = new SimulationClock(ticksPerSecond);
  }
  dispatch(command: Command) {
    switch (command.type) {
      case "SetPaused":
        this.clock.setPaused(command.paused);
        break;
      case "SetTimeScale":
        this.clock.setTimeScale(command.timeScale);
        break;
    }
  }
  advance(seconds: number) {
    return this.clock.advance(seconds, () => {
      /* Future authoritative world systems. */
    });
  }
  snapshot(): WorldSnapshot {
    return Object.freeze({ clock: this.clock.snapshot() });
  }
}
