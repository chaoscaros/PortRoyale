import { MeshBuilder, ShaderMaterial, type Scene } from "@babylonjs/core";
export function createOcean(scene: Scene) {
  const ocean = MeshBuilder.CreateGround(
    "ocean",
    { width: 1800, height: 1800, subdivisions: 1 },
    scene,
  );
  const material = new ShaderMaterial(
    "ocean-material",
    scene,
    {
      vertexSource: `precision highp float; attribute vec3 position; uniform mat4 worldViewProjection; varying vec3 p;
      void main(){p=position;gl_Position=worldViewProjection*vec4(position,1.);}`,
      fragmentSource: `precision highp float; varying vec3 p; uniform float time;
      void main(){float wave=sin(p.x*.35+p.z*.2+time)*sin(p.z*.46-time*.7);
      float gleam=pow(max(0.,wave),18.);float shoal=exp(-length(p.xz-vec2(-15.,12.))*.012);
      vec3 c=mix(vec3(.025,.20,.27),vec3(.05,.46,.48),shoal);
      c+=vec3(.05,.10,.09)*wave*.24+vec3(.20,.29,.25)*gleam*.5;
      gl_FragColor=vec4(c,1.);}`,
    },
    { attributes: ["position"], uniforms: ["worldViewProjection", "time"] },
  );
  ocean.material = material;
  ocean.isPickable = false;
  return material;
}
