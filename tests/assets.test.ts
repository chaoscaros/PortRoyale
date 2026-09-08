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
      expect(material.name).toBe("art05_baked_terrain_PBR");
      expect(material.pbrMetallicRoughness.baseColorTexture.texCoord ?? 0).toBe(0);
    }
    const house = read("public/assets/models/buildings/building_house_a.glb");
    const wall = house.materials.find((m: { name: string }) => m.name === "art05_wall_atlas_PBR");
    expect(wall.pbrMetallicRoughness.baseColorTexture.texCoord).toBe(1);
    for (const mesh of house.meshes) for (const primitive of mesh.primitives) {
      if (house.materials[primitive.material] === wall) {
        expect(primitive.attributes.TEXCOORD_1).toBeDefined();
      }
    }
  });

});
