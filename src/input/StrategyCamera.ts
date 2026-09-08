import { ArcRotateCamera, Vector3, type Scene } from "@babylonjs/core";
export function createStrategyCamera(scene: Scene, canvas: HTMLCanvasElement) {
  const camera = new ArcRotateCamera(
    "strategy",
    -1.32,
    1.01,
    215,
    new Vector3(-125, 0, 22),
    scene,
  );
  camera.lowerBetaLimit = 0.3;
  camera.upperBetaLimit = 1.12;
  camera.lowerRadiusLimit = 80;
  camera.upperRadiusLimit = 740;
  camera.panningSensibility = 35;
  camera.panningAxis = new Vector3(1, 0, 1);
  camera.wheelDeltaPercentage = 0.012;
  camera.minZ = 0.5;
  camera.maxZ = 6000;
  camera.attachControl(false, false, 2);
  scene.onBeforeRenderObservable.add(() => {
    camera.target.x = Math.max(-300, Math.min(300, camera.target.x));
    camera.target.z = Math.max(-300, Math.min(300, camera.target.z));
    camera.target.y = 0;
  });
  return camera;
}
