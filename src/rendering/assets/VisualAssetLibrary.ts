import {
  LoadAssetContainerAsync,
  TransformNode,
  Vector3,
  type Material,
  type AssetContainer,
  type Scene,
  type ShadowGenerator,
} from "@babylonjs/core";
import "@babylonjs/loaders/glTF";
import manifest from "../../../assets-source/blender/visual/manifest.json";
export { manifest as visualManifest };
export type VisualAssetId = keyof typeof manifest.assets;
/** One container per reusable module; repeated props/buildings share GPU geometry. */
export class VisualAssetLibrary {
  private readonly containers = new Map<VisualAssetId, AssetContainer>();
  private disposed = false;
  private readonly detailLevels: { root: TransformNode; near: TransformNode; far: TransformNode; distance: number; high: boolean }[] = [];
  constructor(private readonly scene: Scene) {}
  async load() {
    await Promise.all(
      (Object.keys(manifest.assets) as VisualAssetId[]).map(async (id) => {
        const container = await LoadAssetContainerAsync(
          manifest.assets[id].url,
          this.scene,
          {
            pluginOptions: {
              gltf: {
                preprocessUrlAsync: async (url: string) => {
                  // Our authored GLBs share local textures above the model category folder.
                  const resolved = new URL(url, window.location.href);
                  if (
                    resolved.origin !== window.location.origin ||
                    !resolved.pathname.startsWith("/assets/")
                  )
                    throw new Error(
                      "Asset URL outside the local asset library",
                    );
                  return resolved.href;
                },
              },
            },
          },
        );
        if (this.disposed) {
          container.dispose();
          return;
        }
        for (const mesh of container.meshes) mesh.receiveShadows = true;
        this.containers.set(id, container);
      }),
    );
    // Authored family names are canonical; identical materials across modules share a draw state.
    const shared = new Map<string, Material>();
    for (const container of this.containers.values()) {
      for (const mesh of container.meshes) {
        const material = mesh.material;
        if (!material) continue;
        const existing = shared.get(material.name);
        if (existing) mesh.material = existing;
        else { shared.set(material.name, material); material.freeze(); }
      }
    }
  }

  place(
    id: VisualAssetId,
    parent: TransformNode,
    x = 0,
    y = 0,
    z = 0,
    heading = 0,
    shadows?: ShadowGenerator,
    facade = 0,
  ) {
    const container = this.containers.get(id);
    if (!container) throw new Error(`Asset not ready: ${id}`);
    const root = new TransformNode(`${id}:placement`, this.scene);
    root.parent = parent;
    root.position.set(x, y, z);
    root.rotation.y = heading;
    const instantiate = (asset: VisualAssetId, level: TransformNode) => {
      const entries = this.containers.get(asset)!.instantiateModelsToScene(
        (name) => `${asset}:${name}`, false, { doNotInstantiate: false },
      );
      for (const node of entries.rootNodes) node.parent = level;
      for (const mesh of level.getChildMeshes()) {
        const option = mesh.name.match(/facade_(\d+)__/);
        if (option && Number(option[1]) !== facade) mesh.setEnabled(false);
        mesh.isPickable = false;
        if (shadows) shadows.addShadowCaster(mesh, false);
      }
    };
    const lodId = `${id}_lod1` as VisualAssetId;
    if (this.containers.has(lodId)) {
      // Switch the whole authored module together. Per-mesh native LOD can leave
      // optional facade groups at a different level from the building body.
      const near = new TransformNode(`${id}:near`, this.scene);
      const far = new TransformNode(`${id}:far`, this.scene);
      near.parent = far.parent = root;
      instantiate(id, near); instantiate(lodId, far); far.setEnabled(false);
      const distance = id.includes("palm") ? 175 : id.includes("tree") ? 155 : id.includes("house") ? 175 : 240;
      this.detailLevels.push({ root, near, far, distance, high: true });
    } else instantiate(id, root);
    return root;
  }
  updateDetail(cameraPosition: Vector3) {
    for (const level of this.detailLevels) {
      const distance = Vector3.Distance(cameraPosition, level.root.getAbsolutePosition());
      const high = distance < level.distance + (level.high ? 8 : -8);
      if (high === level.high) continue;
      level.near.setEnabled(high); level.far.setEnabled(!high); level.high = high;
    }
  }
  dispose() {
    this.detailLevels.length = 0;
    this.disposed = true;
    for (const c of this.containers.values()) c.dispose();
    this.containers.clear();
  }
}
