import { MeshBuilder, ShaderMaterial, type Scene } from "@babylonjs/core";
import type { PortSnapshot } from "../../simulation/world/types";
import { PORT_IDS } from "../../data/ports/portDefinitions";
export function createOcean(scene: Scene, ports: readonly PortSnapshot[]) {
  const ocean = MeshBuilder.CreateGround(
    "caribbean-ocean",
    { width: 2200, height: 2200 },
    scene,
  );
  ocean.isPickable = false;
  const material = new ShaderMaterial(
    "caribbean-water",
    scene,
    {
      vertexSource: `precision highp float;attribute vec3 position;uniform mat4 worldViewProjection;varying vec3 p;void main(){p=position;gl_Position=worldViewProjection*vec4(position,1.);}`,
      fragmentSource: `precision highp float;varying vec3 p;uniform float time;uniform vec3 eye;uniform vec4 shores[4];
    float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1)),f.x),f.y);}
    float waves(vec2 q){return sin(q.x*.43+q.y*.21+time*.8)*.45+sin(q.y*.73-q.x*.26-time*.6)*.22+noise(q*.55+time*.07)*.33;}
    void main(){vec2 q=p.xz;float d=20.;for(int i=0;i<4;i++){float v=length((q-shores[i].xy)/shores[i].zw);d=min(d,v);}float shallow=exp(-max(0.,d-.85)*3.8);
    vec3 n=normalize(vec3((waves(q-vec2(.2,0))-waves(q+vec2(.2,0)))*.65,1.,(waves(q-vec2(0,.2))-waves(q+vec2(0,.2)))*.65));vec3 v=normalize(eye-p),l=normalize(vec3(-.45,1.,-.55));float f=.025+.6*pow(1.-max(0.,dot(n,v)),5.);vec3 water=mix(vec3(.018,.145,.205),vec3(.055,.48,.39),shallow);water+=noise(q*.05)*.023;
    vec3 c=mix(water,vec3(.49,.71,.75),f);c+=vec3(.10,.16,.15)*pow(max(0.,waves(q)),5.)*.28;float spec=pow(max(0.,dot(n,normalize(l+v))),180.);c+=vec3(1.,.86,.57)*spec*.65;
    float foam=(1.-smoothstep(.0,.026,abs(d-(1.0+sin(time*.65+noise(q*.09)*3.)*.018))))*shallow;
    c=mix(c,vec3(.68,.79,.65),foam*.22);float fog=smoothstep(550.,1500.,length(eye-p));c=mix(c,vec3(.53,.72,.75),fog);gl_FragColor=vec4(c,1.);}`,
    },
    {
      attributes: ["position"],
      uniforms: ["worldViewProjection", "time", "eye", "shores"],
    },
  );
  material.setArray4(
    "shores",
    ports.flatMap((port) =>
      port.id === PORT_IDS.havana
        ? [port.position.x - 40, port.position.z + 64, 70, 50]
        : [port.position.x, port.position.z + 36, 23, 18],
    ),
  );
  ocean.material = material;
  return {
    update(time: number) {
      material.setFloat("time", time);
      if (scene.activeCamera)
        material.setVector3("eye", scene.activeCamera.position);
    },
  };
}
