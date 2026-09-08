import { ArcRotateCamera, Vector3, type Scene } from "@babylonjs/core";
export function createStrategyCamera(scene: Scene, canvas: HTMLCanvasElement) {
  const camera = new ArcRotateCamera(
    "strategy",
    -1.12,
    1.02,
    205,
    new Vector3(-115, 0, 5),
    scene,
  );
  camera.lowerBetaLimit = 0.3;
  camera.upperBetaLimit = 1.12;
  camera.lowerRadiusLimit = 80;
  camera.upperRadiusLimit = 520;
  camera.panningSensibility = 35;
  camera.panningAxis = new Vector3(1, 0, 1);
  camera.wheelDeltaPercentage = 0.012;
  camera.minZ = 0.5;
  camera.maxZ = 6000;
  camera.attachControl(false, false, 2);
  scene.onBeforeRenderObservable.add(() => {
    camera.target.x = Math.max(-180, Math.min(180, camera.target.x));
    camera.target.z = Math.max(-180, Math.min(180, camera.target.z));
    camera.target.y = 0;
  });
  return camera;
}
