import {
  Color3,
  MeshBuilder,
  StandardMaterial,
  Vector3,
  type Scene,
} from "@babylonjs/core";
export function createTestWorld(scene: Scene) {
  const mat = (name: string, hex: string) => {
    const m = new StandardMaterial(name, scene);
    m.diffuseColor = Color3.FromHexString(hex);
    m.specularColor = Color3.Black();
    return m;
  };
  const sand = mat("sand", "#c9b78a"),
    grass = mat("grass", "#72835b"),
    rock = mat("rock", "#65776b");
  const wood = mat("pier", "#775640"),
    plaster = mat("plaster", "#ded0aa"),
    roof = mat("roof", "#976347");
  const island = MeshBuilder.CreateSphere(
    "island-sand",
    { diameter: 2, segments: 12 },
    scene,
  );
  island.scaling.set(47, 9, 33);
  island.position.set(-18, -4, 12);
  island.material = sand;
  const inland = MeshBuilder.CreateSphere(
    "island-grass",
    { diameter: 2, segments: 10 },
    scene,
  );
  inland.scaling.set(40, 10, 27);
  inland.position.set(-19, -3, 13);
  inland.material = grass;
  for (let i = 0; i < 3; i++) {
    const hill = MeshBuilder.CreateCylinder(
      `hill-${i}`,
      {
        diameterBottom: 24 - i * 3,
        diameterTop: 2,
        height: 16 + i * 4,
        tessellation: 5,
      },
      scene,
    );
    hill.position.set(-34 + i * 12, 8, 20 + (i % 2) * 7);
    hill.material = rock;
  }
  const pier = MeshBuilder.CreateBox(
    "port-pier",
    { width: 8, height: 1.5, depth: 26 },
    scene,
  );
  pier.position.set(7, 1.3, -18);
  pier.material = wood;
  for (let i = 0; i < 3; i++) {
    const house = MeshBuilder.CreateBox(
      `port-placeholder-${i}`,
      { width: 7, height: 5, depth: 6 },
      scene,
    );
    house.position.set(-5 - i * 10, 6, -1);
    house.material = plaster;
    const top = MeshBuilder.CreateCylinder(
      `roof-${i}`,
      { diameter: 10, height: 8, tessellation: 3 },
      scene,
    );
    top.rotation.z = Math.PI / 2;
    top.position.copyFrom(house.position).addInPlace(new Vector3(0, 3, 0));
    top.material = roof;
  }
  const marker = MeshBuilder.CreateTorus(
    "port-marker",
    { diameter: 12, thickness: 0.5, tessellation: 40 },
    scene,
  );
  marker.position.set(7, 2.2, -29);
  marker.material = mat("marker-gold", "#edc77a");
  for (let i = 0; i < 10; i++) {
    const x = -48 + ((i * 19) % 62),
      z = 4 + ((i * 13) % 26);
    const trunk = MeshBuilder.CreateCylinder(
      `tree-trunk-${i}`,
      { height: 7, diameter: 0.65, tessellation: 5 },
      scene,
    );
    trunk.position.set(x, 7, z);
    trunk.material = wood;
    const crown = MeshBuilder.CreateSphere(
      `tree-crown-${i}`,
      { diameter: 7, segments: 4 },
      scene,
    );
    crown.scaling.y = 0.35;
    crown.position.set(x, 10.5, z);
    crown.material = grass;
  }
}
