import { MeshBuilder, ShaderMaterial, type Scene } from "@babylonjs/core";
import type { FleetSnapshot } from "../../simulation/world/types";
export class ShipWake {
  private readonly mesh;
  private readonly material;
  constructor(scene: Scene) {
    this.mesh = MeshBuilder.CreateGround(
      "sloop-wake",
      { width: 15, height: 28 },
      scene,
    );
    this.mesh.isPickable = false;
    this.material = new ShaderMaterial(
      "wake-foam",
      scene,
      {
        vertexSource: `precision highp float;attribute vec3 position;attribute vec2 uv;uniform mat4 worldViewProjection;varying vec2 vUV;void main(){vUV=uv;gl_Position=worldViewProjection*vec4(position,1.);}`,
        fragmentSource: `precision highp float;varying vec2 vUV;uniform float time;void main(){float x=abs(vUV.x-.5)*2.;float trail=vUV.y;float width=.15+.78*(1.-trail);float edge=exp(-pow((x-width)*12.,2.));float ripple=.55+.45*sin(trail*80.+time*5.+x*12.);float alpha=edge*pow(trail,.4)*(1.-trail)*ripple*.48;gl_FragColor=vec4(.72,.85,.76,alpha);}`,
      },
      {
        attributes: ["position", "uv"],
        uniforms: ["worldViewProjection", "time"],
        needAlphaBlending: true,
      },
    );
    this.material.disableDepthWrite = true;
    this.material.backFaceCulling = false;
    this.mesh.material = this.material;
    this.mesh.setEnabled(false);
  }
  update(fleet: FleetSnapshot, time: number) {
    this.mesh.setEnabled(fleet.status === "sailing");
    this.mesh.position.set(
      fleet.position.x - Math.sin(fleet.heading) * 23,
      0.08,
      fleet.position.z - Math.cos(fleet.heading) * 23,
    );
    this.mesh.rotation.y = fleet.heading;
    this.material.setFloat("time", time);
  }
  dispose() {
    this.mesh.dispose(false, true);
  }
}
