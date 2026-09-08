import { describe, expect, it } from "vitest";
import { SimulationClock } from "../src/simulation/SimulationClock";
import { Simulation } from "../src/simulation/Simulation";
import { readFileSync, readdirSync } from "node:fs";
describe("fixed simulation clock", () => {
  it("retains remainder and emits exact fixed dt", () => {
    const c = new SimulationClock();
    const dt: number[] = [];
    expect(c.advance(0.09, (t) => dt.push(t))).toBe(0);
    expect(c.advance(0.21, (t) => dt.push(t))).toBe(3);
    expect(dt).toEqual([0.1, 0.1, 0.1]);
    expect(c.snapshot().simulationTime).toBeCloseTo(0.3);
  });
  it("supports configurable tick rate", () => {
    const c = new SimulationClock(20);
    expect(c.advance(1, () => {})).toBe(20);
  });
  it("pause discards elapsed real time and preserves fractional progress", () => {
    const c = new SimulationClock();
    c.advance(0.05, () => {});
    c.setPaused(true);
    expect(c.advance(100, () => {})).toBe(0);
    c.setPaused(false);
    expect(c.advance(0.05, () => {})).toBe(1);
  });
  it.each([1, 2, 4] as const)(
    "scale %i multiplies simulation ticks",
    (scale) => {
      const c = new SimulationClock();
      c.setTimeScale(scale);
      c.advance(1, () => {});
      expect(c.snapshot().tickCount).toBe(10 * scale);
    },
  );
  it("is deterministic across render frame partitions", () => {
    const a = new Simulation(),
      b = new Simulation();
    for (const s of [a, b]) s.dispatch({ type: "SetTimeScale", timeScale: 4 });
    for (let i = 0; i < 600; i++) a.advance(1 / 60);
    for (let i = 0; i < 240; i++) b.advance(1 / 24);
    expect(a.snapshot()).toEqual(b.snapshot());
    expect(a.snapshot().clock.tickCount).toBe(400);
  });
  it("old snapshots remain immutable after commands and advancement", () => {
    const s = new Simulation();
    const before = s.snapshot();
    s.advance(1);
    s.dispatch({ type: "SetPaused", paused: true });
    expect(before.clock.tickCount).toBe(0);
    expect(before.clock.paused).toBe(false);
    expect(Object.isFrozen(before.clock)).toBe(true);
    expect(Object.isFrozen(before)).toBe(true);
  });
  it("rejects invalid configuration and elapsed input", () => {
    for (const rate of [0, -1, 1.5, Infinity])
      expect(() => new SimulationClock(rate)).toThrow();
    const c = new SimulationClock();
    for (const dt of [-1, NaN, Infinity])
      expect(() => c.advance(dt, () => {})).toThrow();
  });
  it("has no rendering or browser dependencies", () => {
    for (const file of readdirSync("src/simulation", { recursive: true }).filter((f) =>
      typeof f === "string" && f.endsWith(".ts"),
    )) {
      expect(readFileSync(`src/simulation/${file}`, "utf8")).not.toMatch(
        /@babylonjs|from ['"]react|\bwindow\b|\bdocument\b|HTMLCanvasElement/,
      );
    }
  });
});
