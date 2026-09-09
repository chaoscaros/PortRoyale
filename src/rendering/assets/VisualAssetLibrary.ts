import {
  LoadAssetContainerAsync,
  TransformNode,
  Mesh,
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
    // Native mesh LOD is sufficient for the four prepared modules; no new simulation system.
    for (const [id, container] of this.containers) {
      const definition = manifest.assets[id];
      if (!("lodOf" in definition) || typeof definition.lodOf !== "string") continue;
      const source = this.containers.get(definition.lodOf as VisualAssetId);
      if (!source) continue;
      for (const mesh of source.meshes) {
        if (!(mesh instanceof Mesh) || !mesh.material) continue;
        const lod = container.meshes.find(m => m instanceof Mesh && m.material?.name === mesh.material?.name);
        if (lod instanceof Mesh) mesh.addLODLevel(id.includes("palm") ? 175 : 240, lod);
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
  ) {
    const container = this.containers.get(id);
    if (!container) throw new Error(`Asset not ready: ${id}`);
    const root = new TransformNode(`${id}:placement`, this.scene);
    root.parent = parent;
    root.position.set(x, y, z);
    root.rotation.y = heading;
    const entries = container.instantiateModelsToScene(
      (name) => `${id}:${name}`,
      false,
      { doNotInstantiate: false },
    );
    for (const node of entries.rootNodes) node.parent = root;
    for (const mesh of root.getChildMeshes()) {
      mesh.isPickable = false;
      if (shadows) shadows.addShadowCaster(mesh, false);
    }
    return root;
  }
  dispose() {
    this.disposed = true;
    for (const c of this.containers.values()) c.dispose();
    this.containers.clear();
  }
}
