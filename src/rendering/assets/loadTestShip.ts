import { ImportMeshAsync, TransformNode, type Scene } from "@babylonjs/core";
import "@babylonjs/loaders/glTF";
export async function loadTestShip(scene: Scene) {
  const result = await ImportMeshAsync("/assets/models/ship_test.glb", scene);
  const root = new TransformNode("test-ship-visual", scene);
  for (const mesh of result.meshes) if (!mesh.parent) mesh.parent = root;
  // Verify Blender export and Babylon world-space conventions before placement.
  for (const [name, expected] of [
    ["axis_forward", [0, 0, 10]],
    ["axis_up", [0, 10, 0]],
    ["axis_right", [10, 0, 0]],
  ] as const) {
    const node = scene.getTransformNodeByName(name);
    if (!node) throw new Error(`GLB 缺少校验节点：${name}`);
    node.computeWorldMatrix(true);
    const p = node.getAbsolutePosition();
    if ([p.x, p.y, p.z].some((n, i) => Math.abs(n - expected[i]) > 0.001))
      throw new Error(`GLB 方向校验失败：${name}`);
  }
  root.position.set(26, 0.6, -39);
  root.rotation.y = -0.5;
  return root;
}
