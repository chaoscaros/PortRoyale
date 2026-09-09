import { describe, expect, it } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import manifest from "../assets-source/blender/visual/manifest.json";

describe("visual asset delivery", () => {
  it("ships every catalogued source and glTF 2 binary with resolvable shared textures with matching geometry", () => {
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
      for (const image of gltf.images ?? []) {
        if (image.uri) {
          expect(image.uri.startsWith("../../textures/shared/")).toBe(true);
          expect(
            existsSync(resolve("public", asset.url.slice(1), "..", image.uri)),
          ).toBe(true);
        } else expect(image.bufferView).toBeDefined();
      }
      for (const view of gltf.bufferViews) {
        expect((view.byteOffset ?? 0) + view.byteLength).toBeLessThanOrEqual(
          gltf.buffers[0].byteLength,
        );
      }
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
      expect(asset.triangles).toBeLessThan(80001);
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
  it("preserves terrain bake UVs and never exports authoring masks as visible color", () => {
    const read = (path: string) => {
      const b = readFileSync(path);
      return JSON.parse(b.toString("utf8", 20, 20 + b.readUInt32LE(12)));
    };
    const terrain = read("public/assets/models/environment/island_visual_test.glb");
    for (const mesh of terrain.meshes) for (const primitive of mesh.primitives) {
      expect(primitive.attributes.COLOR_0).toBeUndefined();
      expect(primitive.attributes.TEXCOORD_0).toBeDefined();
      const material = terrain.materials[primitive.material];
      expect(material.name).toBe("art06_HarborTerrain");
      expect(material.pbrMetallicRoughness.baseColorTexture.texCoord ?? 0).toBe(0);
    }
    const house = read("public/assets/models/buildings/building_house_a.glb");
    const wall = house.materials.find((m: { name: string }) => m.name === "art06_Plaster");
    expect(wall.pbrMetallicRoughness.baseColorTexture.texCoord ?? 0).toBe(0);
    expect(wall.normalTexture.texCoord ?? 0).toBe(0);
    expect(wall.pbrMetallicRoughness.metallicRoughnessTexture.texCoord ?? 0).toBe(0);
    for (const mesh of house.meshes) for (const primitive of mesh.primitives) {
      if (house.materials[primitive.material] === wall) {
        expect(primitive.attributes.TEXCOORD_0).toBeDefined();
      }
    }
  });

  it("exports terrain at the surveyed building datums", () => {
    const b = readFileSync("public/assets/models/environment/island_visual_test.glb");
    const jsonLength = b.readUInt32LE(12);
    const gltf = JSON.parse(b.toString("utf8", 20, 20 + jsonLength));
    const primitive = gltf.meshes[0].primitives[0];
    const accessor = gltf.accessors[primitive.attributes.POSITION];
    const view = gltf.bufferViews[accessor.bufferView];
    expect(accessor.componentType).toBe(5126);
    const start = 28 + jsonLength + (view.byteOffset ?? 0) + (accessor.byteOffset ?? 0);
    for (const plot of manifest.site.plots) {
      let nearest = Infinity, height = 0;
      for (let v = 0; v < accessor.count; v++) {
        const offset = start + v * (view.byteStride ?? 12);
        const dx = b.readFloatLE(offset) - plot.x, dz = b.readFloatLE(offset + 8) - plot.z;
        if (dx * dx + dz * dz < nearest) {
          nearest = dx * dx + dz * dz;
          height = b.readFloatLE(offset + 4);
        }
      }
      expect(nearest, plot.asset).toBeLessThan(2);
      expect(Math.abs(height - plot.y), plot.asset).toBeLessThan(.2);
      const placement = manifest.havana.find(p => p.asset === plot.asset && p.x === plot.x && p.z === plot.z);
      expect(placement?.y).toBeCloseTo(plot.y + .11);
    }
  });
  it("ships conservative LOD1 geometry for the four designated modules", () => {
    for (const id of ["building_governor", "building_church", "prop_palm", "prop_palm_b"] as const) {
      const base = manifest.assets[id];
      const lod = manifest.assets[`${id}_lod1`];
      expect(lod.triangles).toBeLessThan(base.triangles * .75);
      expect(lod.triangles).toBeGreaterThan(base.triangles * .25);
    }
  });

});
