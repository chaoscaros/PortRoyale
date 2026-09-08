import {
  RawCubeTexture,
  Constants,
  Color3,
  Color4,
  DefaultRenderingPipeline,
  DirectionalLight,
  HemisphericLight,
  ImageProcessingConfiguration,
  Mesh,
  MeshBuilder,
  Scene,
  ShaderMaterial,
  ShadowGenerator,
  Vector3,
  type Camera,
} from "@babylonjs/core";
export function createEnvironment(scene: Scene, camera: Camera) {
  scene.clearColor = new Color4(0.55, 0.75, 0.79, 1);
  scene.fogMode = Scene.FOGMODE_LINEAR;
  scene.fogStart = 550;
  scene.fogEnd = 1500;
  scene.fogColor = new Color3(0.53, 0.72, 0.75);
  // Authored low-frequency sky/ground IBL: reusable faces, mipmapped reflections.
  const size = 32;
  const faces = Array.from({ length: 6 }, (_, face) => {
    const pixels = new Uint8Array(size * size * 4);
    for (let y = 0; y < size; y++)
      for (let x = 0; x < size; x++) {
        const h = face === 2 ? 1 : face === 3 ? 0 : 1 - y / (size - 1);
        const sky = [0.46, 0.57, 0.64],
          ground = [0.19, 0.18, 0.13];
        const i = (y * size + x) * 4;
        for (let c = 0; c < 3; c++)
          pixels[i + c] = Math.round(255 * (ground[c] * (1 - h) + sky[c] * h));
        pixels[i + 3] = 255;
      }
    return pixels;
  });
  const reflection = new RawCubeTexture(
    scene,
    faces,
    size,
    Constants.TEXTUREFORMAT_RGBA,
    Constants.TEXTURETYPE_UNSIGNED_BYTE,
    true,
  );
  reflection.gammaSpace = false;
  scene.environmentTexture = reflection;
  scene.environmentIntensity = 0.55;
  const ambient = new HemisphericLight(
    "tropical-skylight",
    new Vector3(0, 1, 0),
    scene,
  );
  ambient.intensity = 0.28;
  ambient.diffuse = new Color3(0.81, 0.91, 1);
  ambient.groundColor = new Color3(0.32, 0.3, 0.22);
  const sun = new DirectionalLight(
    "afternoon-sun",
    new Vector3(-0.65, -1, 0.35).normalize(),
    scene,
  );
  sun.position.set(120, 250, -180);
  sun.diffuse = new Color3(1, 0.94, 0.82);
  sun.intensity = 3.2;
  sun.shadowMinZ = 1;
  sun.shadowMaxZ = 800;
  const shadows = new ShadowGenerator(2048, sun);
  shadows.usePercentageCloserFiltering = true;
  shadows.filteringQuality = ShadowGenerator.QUALITY_MEDIUM;
  shadows.bias = 0.0003;
  shadows.normalBias = 0.025;
  shadows.setDarkness(0.2);
  const sky = MeshBuilder.CreateSphere(
    "tropical-sky",
    { diameter: 6000, segments: 24, sideOrientation: Mesh.BACKSIDE },
    scene,
  );
  sky.infiniteDistance = true;
  sky.isPickable = false;
  sky.applyFog = false;
  sky.material = new ShaderMaterial(
    "sky-gradient",
    scene,
    {
      vertexSource: `precision highp float;attribute vec3 position;uniform mat4 worldViewProjection;varying vec3 dir;void main(){dir=normalize(position);gl_Position=worldViewProjection*vec4(position,1.);}`,
      fragmentSource: `precision highp float;varying vec3 dir;
    float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1)),f.x),f.y);}
    void main(){float h=max(0.,dir.y);vec3 c=mix(vec3(.53,.72,.75),vec3(.17,.48,.68),pow(h,.55));vec2 p=dir.xz/max(.1,h)*2.;float cloud=noise(p)*.65+noise(p*2.)*.25+noise(p*4.)*.1;float mask=smoothstep(.59,.78,cloud)*smoothstep(.03,.25,h);c=mix(c,vec3(.95,.93,.85),mask*.7);gl_FragColor=vec4(c,1.);}`,
    },
    { attributes: ["position"], uniforms: ["worldViewProjection"] },
  );
  sky.material.disableDepthWrite = true;
  const pipeline = new DefaultRenderingPipeline("visual-post", true, scene, [
    camera,
  ]);
  pipeline.fxaaEnabled = true;
  pipeline.samples = 1;
  pipeline.bloomEnabled = true;
  pipeline.bloomThreshold = 1.15;
  pipeline.bloomWeight = 0.06;
  pipeline.bloomKernel = 32;
  pipeline.bloomScale = 0.35;
  scene.imageProcessingConfiguration.toneMappingEnabled = true;
  scene.imageProcessingConfiguration.toneMappingType =
    ImageProcessingConfiguration.TONEMAPPING_ACES;
  scene.imageProcessingConfiguration.exposure = 1.13;
  scene.imageProcessingConfiguration.contrast = 1.12;
  return {
    shadows,
    dispose() {
      pipeline.dispose();
      shadows.dispose();
      reflection.dispose();
    },
  };
}
