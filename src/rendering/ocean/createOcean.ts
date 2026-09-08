import {
  ArcRotateCamera,
  MeshBuilder,
  ShaderMaterial,
  type Scene,
} from "@babylonjs/core";
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
    float fbm(vec2 q){float f=0.;float a=.5;for(int i=0;i<4;i++){f+=noise(q)*a;q=mat2(.8,-.6,.6,.8)*q*2.07+vec2(17.3,8.7);a*=.5;}return f;}
    float waves(vec2 q){vec2 drift=vec2(time*.045,-time*.035);float swell=sin(q.x*.095+q.y*.061+time*.31)*.10+sin(q.y*.131-q.x*.077-time*.27)*.07;return swell+fbm(q*.43+drift)*.34+fbm(q*1.2-drift*1.3)*.09;}
    float heroHeight(vec2 p){float x=p.x,z=p.y;float r=length(vec2((x+38.)/94.,(z-78.)/77.))+.035*sin(x*.12)+.025*sin(z*.17+x*.055);float coast=clamp((1.-r)*30.,-5.,4.2)-exp(-pow((x-14.)/31.,2.)-pow((z-20.)/27.,2.))*7.;float ridge=27.*exp(-pow((x+75.)/28.,2.)-pow((z-119.)/22.,2.))+18.*exp(-pow((x+8.)/24.,2.)-pow((z-128.)/21.,2.));float h=coast+max(0.,1.-r)*ridge*2.;float terrace=min(min(x+108.,34.-x),min(z-38.,98.-z));h=mix(h,4.2,clamp(terrace/7.,0.,1.));float quayBlend=smoothstep(-120.,-108.,x)*(1.-smoothstep(-1.,12.,x))*(1.-smoothstep(32.,45.,z));h=mix(h,min(h,(z-32.)*.75),quayBlend);if(r>1.15)h=min(h,(1.-r)*40.);return h;}
    void main(){vec2 q=p.xz;float depth=-heroHeight(q-(shores[0].xy+vec2(38.,-78.)));for(int i=1;i<4;i++){if(shores[i].z>0.){float v=length((q-shores[i].xy)/shores[i].zw);depth=min(depth,(v-1.)*20.);}}float shallow=exp(-max(0.,depth)*.38);float distanceToEye=length(eye-p);float detail=1.-smoothstep(170.,850.,distanceToEye);
    vec3 n=normalize(vec3((waves(q-vec2(.18,0))-waves(q+vec2(.18,0)))*2.2*detail,1.,(waves(q-vec2(0,.18))-waves(q+vec2(0,.18)))*2.2*detail));vec3 v=normalize(eye-p),l=normalize(vec3(.65,1.,-.35));float f=.035+.62*pow(1.-max(0.,dot(n,v)),5.);
    float sandbar=fbm(q*.025);vec3 water=mix(vec3(.028,.165,.205),vec3(.11,.36,.32),shallow*(.82+sandbar*.18));water+=vec3(.012,.026,.025)*(fbm(q*.017)-.5);
    vec3 reflected=mix(vec3(.27,.43,.50),vec3(.55,.65,.66),pow(1.-v.y,3.));vec3 c=mix(water,reflected,f);float spec=pow(max(0.,dot(n,normalize(l+v))),95.);c+=vec3(1.,.91,.74)*spec*.43;
    float edge=abs(depth-(sin(time*.34+fbm(q*.08)*5.)*.20));float foam=(1.-smoothstep(.05,.55,edge))*(.4+.6*noise(q*.9-time*.04));c=mix(c,vec3(.55,.62,.54),foam*.16);
    float fog=smoothstep(480.,1450.,distanceToEye);c=mix(c,vec3(.53,.72,.75),fog);gl_FragColor=vec4(c,1.);}`,
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
        ? [port.position.x - 38, port.position.z + 78, 94, 77]
        : [port.position.x, port.position.z + 36, 23, 18],
    ),
  );
  ocean.material = material;
  return {
    update(time: number) {
      const camera = scene.activeCamera;
      material.setArray4(
        "shores",
        ports.flatMap((port) => {
          if (port.id === PORT_IDS.havana)
            return [port.position.x - 38, port.position.z + 78, 94, 77];
          const visible =
            !(camera instanceof ArcRotateCamera) ||
            camera.radius > 330 ||
            Math.hypot(
              camera.target.x - port.position.x,
              camera.target.z - port.position.z,
            ) < 80;
          return [port.position.x, port.position.z + 36, visible ? 23 : -1, 18];
        }),
      );
      material.setFloat("time", time);
      if (scene.activeCamera)
        material.setVector3("eye", scene.activeCamera.position);
    },
  };
}
