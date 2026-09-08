import { describe, expect, it } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import manifest from "../assets-source/blender/visual/manifest.json";

describe("visual asset delivery", () => {
  it("ships every catalogued source and self-contained glTF 2 binary with matching geometry", () => {
    for (const asset of Object.values(manifest.assets)) {
      expect(existsSync(resolve(asset.source)), asset.source).toBe(true);
      const buffer = readFileSync(resolve("public", asset.url.slice(1)));
      expect(buffer.toString("ascii", 0, 4)).toBe("glTF");
      expect(buffer.readUInt32LE(4)).toBe(2);
      expect(buffer.readUInt32LE(8)).toBe(buffer.length);
      const gltf = JSON.parse(
        buffer.toString("utf8", 20, 20 + buffer.readUInt32LE(12)),
      );
      expect(gltf.buffers.every((b: { uri?: string }) => !b.uri)).toBe(true);
      expect(
        (gltf.images ?? []).every(
          (i: { bufferView?: number }) => i.bufferView !== undefined,
        ),
      ).toBe(true);
      const triangles = gltf.meshes
        .flatMap(
          (mesh: { primitives: { indices: number }[] }) => mesh.primitives,
        )
        .reduce(
          (sum: number, p: { indices: number }) =>
            sum + gltf.accessors[p.indices].count / 3,
          0,
        );
      expect(triangles, asset.url).toBe(asset.triangles);
      expect(asset.triangles).toBeLessThan(60000);
      expect(buffer.length).toBeLessThan(15 * 1024 * 1024);
    }
  });
  it("resolves every Havana module and preserves the ship waterline and forward extent", () => {
    for (const placement of manifest.havana) {
      expect(placement.asset in manifest.assets).toBe(true);
      expect(
        [placement.x, placement.y, placement.z, placement.heading].every(
          Number.isFinite,
        ),
      ).toBe(true);
    }
    expect(manifest.assets.sloop.bounds.min[1]).toBeLessThan(0);
    expect(manifest.assets.sloop.bounds.max[1]).toBeGreaterThan(0);
    expect(manifest.assets.sloop.bounds.max[2]).toBeGreaterThan(
      Math.abs(manifest.assets.sloop.bounds.min[2]),
    );
  });
});
