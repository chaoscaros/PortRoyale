import {
  Color3,
  MeshBuilder,
  PBRMaterial,
  type Scene,
  type ShadowGenerator,
  type TransformNode,
} from "@babylonjs/core";
import { PORT_IDS } from "../../data/ports/portDefinitions";
import type { PortSnapshot } from "../../simulation/world/types";
import {
  VisualAssetLibrary,
  visualManifest,
  type VisualAssetId,
} from "../assets/VisualAssetLibrary";
export function createPortVisual(
  scene: Scene,
  port: PortSnapshot,
  root: TransformNode,
  assets: VisualAssetLibrary,
  shadows: ShadowGenerator,
) {
  const hero = port.id === PORT_IDS.havana;
  if (hero) {
    assets.place("island_visual_test", root);
    for (const p of visualManifest.havana)
      assets.place(
        p.asset as VisualAssetId,
        root,
        p.x,
        p.y,
        p.z,
        p.heading,
        p.shadow ? shadows : undefined,
      );
  } else {
    const island = MeshBuilder.CreateSphere(
      `island:${port.id}`,
      { diameter: 2, segments: 20 },
      scene,
    );
    island.parent = root;
    island.position.set(0, -1, 36);
    island.scaling.set(23, 4, 18);
    island.isPickable = false;
    island.receiveShadows = true;
    const sand = new PBRMaterial(`sand:${port.id}`, scene);
    sand.albedoColor = Color3.FromHexString("#c5b38a").toLinearSpace();
    sand.roughness = 1;
    sand.metallic = 0;
    island.material = sand;
    assets.place("port_pier", root, -15, 0, 14, 0, shadows);
    assets.place("building_house_a", root, -7, 2.6, 35, 0, shadows);
    assets.place("building_house_b", root, 6, 2.5, 39, 0.2, shadows);
    assets.place("prop_palm", root, -12, 2, 40);
    assets.place("prop_palm", root, 13, 1.7, 33);
  }
}
