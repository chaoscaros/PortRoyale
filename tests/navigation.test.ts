import { describe, it, expect } from "vitest";
import { Simulation } from "../src/simulation/Simulation";
import { PortRegistry } from "../src/simulation/world/PortRegistry";
import {
  distance,
  type FleetId,
  type PortId,
} from "../src/simulation/world/types";
import {
  portDefinitions,
  PORT_IDS as P,
} from "../src/data/ports/portDefinitions";
import {
  worldDefinition,
  PLAYER_FLEET_ID as F,
} from "../src/data/worldDefinition";
const move = (s: Simulation, id = P.sanJuan) =>
  s.dispatch({ type: "move-fleet", fleetId: F, destinationPortId: id });
const fleet = (s: Simulation) => s.snapshot().fleets[0];
describe("port world", () => {
  it("has four unique valid ports with Chinese names and stable lookup", () => {
    const registry = new PortRegistry(portDefinitions);
    expect(registry.snapshots).toHaveLength(4);
    expect(new Set(portDefinitions.map((p) => p.id)).size).toBe(4);
    for (const p of portDefinitions) {
      expect(registry.get(p.id)).toEqual(p);
      expect(p.displayName).toMatch(/[\u4e00-\u9fff]/);
      expect(
        Number.isFinite(p.position.x) && Number.isFinite(p.position.z),
      ).toBe(true);
    }
  });
  it("rejects duplicate IDs and invalid positions", () => {
    expect(
      () => new PortRegistry([portDefinitions[0], portDefinitions[0]]),
    ).toThrow();
    expect(
      () =>
        new PortRegistry([
          { ...portDefinitions[0], position: { x: NaN, z: 0 } },
        ]),
    ).toThrow();
  });
  it("starts one fleet docked exactly in Havana", () => {
    const s = new Simulation();
    expect(s.snapshot().fleets).toHaveLength(1);
    expect(fleet(s)).toMatchObject({
      id: F,
      status: "docked",
      currentPortId: P.havana,
      destinationPortId: null,
      position: portDefinitions[0].position,
    });
  });
});
describe("fleet commands and navigation", () => {
  it("starts sailing without teleporting", () => {
    const s = new Simulation(),
      before = fleet(s).position;
    expect(move(s).outcome).toBe("accepted");
    expect(fleet(s)).toMatchObject({
      status: "sailing",
      currentPortId: null,
      destinationPortId: P.sanJuan,
      position: before,
    });
  });
  it.each(["fleet", "port"])(
    "rejects missing %s without world mutation",
    (kind) => {
      const s = new Simulation(),
        before = s.snapshot();
      expect(
        s.dispatch({
          type: "move-fleet",
          fleetId: kind === "fleet" ? ("missing" as FleetId) : F,
          destinationPortId:
            kind === "port" ? ("missing" as PortId) : P.sanJuan,
        }).outcome,
      ).toBe("rejected");
      expect(s.snapshot()).toEqual(before);
    },
  );
  it("same docked port is a no-op", () => {
    const s = new Simulation(),
      before = s.snapshot();
    expect(move(s, P.havana)).toEqual({
      outcome: "noop",
      reason: "already-docked",
    });
    expect(s.snapshot()).toEqual(before);
  });
  it("moves speed * dt along a straight line", () => {
    const s = new Simulation(),
      before = fleet(s).position;
    move(s);
    s.advance(1);
    expect(distance(before, fleet(s).position)).toBeCloseTo(8, 10);
    const target = portDefinitions[1].position;
    expect(distance(fleet(s).position, target)).toBeCloseTo(
      distance(before, target) - 8,
      10,
    );
  });
  it.each([1, 2, 4] as const)(
    "scales displacement by %i from the clock",
    (scale) => {
      const s = new Simulation(),
        before = fleet(s).position;
      move(s);
      s.dispatch({ type: "SetTimeScale", timeScale: scale });
      s.advance(1);
      expect(distance(before, fleet(s).position)).toBeCloseTo(8 * scale, 10);
    },
  );
  it("pause freezes position and resume continues", () => {
    const s = new Simulation();
    move(s);
    s.advance(1);
    s.dispatch({ type: "SetPaused", paused: true });
    const before = fleet(s);
    s.advance(20);
    expect(fleet(s)).toEqual(before);
    s.dispatch({ type: "SetPaused", paused: false });
    s.advance(1);
    expect(distance(before.position, fleet(s).position)).toBeCloseTo(8);
  });
  it("arrival snaps exactly and cannot overshoot at high speed", () => {
    const s = new Simulation(10, { ...worldDefinition, fleetSpeed: 10000 });
    move(s);
    s.advance(0.1);
    expect(fleet(s)).toMatchObject({
      position: portDefinitions[1].position,
      status: "docked",
      currentPortId: P.sanJuan,
      destinationPortId: null,
    });
    s.advance(100);
    expect(fleet(s).position).toEqual(portDefinitions[1].position);
  });
  it("reroutes from current position without teleporting", () => {
    const s = new Simulation();
    move(s);
    s.advance(10);
    const before = fleet(s).position;
    move(s, P.nassau);
    expect(fleet(s).position).toEqual(before);
    s.advance(0.1);
    expect(distance(before, fleet(s).position)).toBeCloseTo(0.8);
    expect(fleet(s).destinationPortId).toBe(P.nassau);
  });
  it("repeated destination is no-op and preserves progress", () => {
    const s = new Simulation();
    move(s);
    s.advance(5);
    const before = s.snapshot();
    expect(move(s)).toEqual({ outcome: "noop", reason: "already-sailing" });
    expect(s.snapshot()).toEqual(before);
  });
  it("can return to its origin while sailing", () => {
    const s = new Simulation();
    move(s);
    s.advance(1);
    move(s, P.havana);
    s.advance(2);
    expect(fleet(s)).toMatchObject({
      status: "docked",
      currentPortId: P.havana,
      position: portDefinitions[0].position,
    });
  });
  it("remains deterministic across frame partitions and command boundaries", () => {
    const a = new Simulation(),
      b = new Simulation();
    for (const s of [a, b]) move(s);
    for (let i = 0; i < 300; i++) a.advance(1 / 60);
    for (let i = 0; i < 120; i++) b.advance(1 / 24);
    for (const s of [a, b]) {
      move(s, P.nassau);
      s.dispatch({ type: "SetTimeScale", timeScale: 4 });
    }
    for (let i = 0; i < 300; i++) a.advance(1 / 60);
    for (let i = 0; i < 120; i++) b.advance(1 / 24);
    expect(a.snapshot()).toEqual(b.snapshot());
  });
  it("deep snapshots cannot mutate world or prior snapshots", () => {
    const s = new Simulation(),
      old = s.snapshot();
    expect(() => Object.assign(old.fleets[0].position, { x: 99 })).toThrow();
    expect(() => Object.assign(old.fleets[0], { status: "sailing" })).toThrow();
    expect(() => Object.assign(old.ports[0].position, { z: 99 })).toThrow();
    expect(Object.isFrozen(old.fleets)).toBe(true);
    move(s);
    s.advance(1);
    expect(old.fleets[0].position).toEqual(portDefinitions[0].position);
  });
  it("copies input definitions so caller mutations cannot change the world", () => {
    const ports = portDefinitions.map((p) => ({
      ...p,
      position: { ...p.position },
    }));
    const s = new Simulation(10, { ...worldDefinition, ports });
    ports[0].position.x = 999;
    expect(s.snapshot().ports[0].position).toEqual(portDefinitions[0].position);
  });
  it("validates positive finite speed", () => {
    for (const speed of [0, -1, NaN, Infinity])
      expect(
        () => new Simulation(10, { ...worldDefinition, fleetSpeed: speed }),
      ).toThrow();
  });
});
