import { describe, expect, it } from "vitest";
import { placePortLabel } from "../src/rendering/ports/labelPlacement";
describe("port label exclusion", () => {
  it("moves a label away from the sail silhouette", () => {
    const sail = {left:450,right:550,top:300,bottom:480};
    const result = placePortLabel({x:500,y:400},{width:1366,height:768},[sail]);
    expect(result).not.toBeNull();
    expect(result!.x + 58).toBeLessThan(sail.left);
  });
  it("keeps the whole label inside the HUD-safe viewport", () => {
    const p = placePortLabel({x:1350,y:740},{width:1366,height:768},[]);
    expect(p!.x + 58).toBeLessThan(1366);
    expect(p!.y + 19).toBeLessThan(700);
  });
  it("finds space beyond the quay when nearby candidates are occupied", () => {
    const subjects = { left: 720, right: 1430, top: 200, bottom: 650 };
    const p = placePortLabel({ x: 990, y: 400 }, { width: 1440, height: 900 }, [subjects]);
    expect(p).not.toBeNull();
    expect(p!.x + 58 + 8).toBeLessThanOrEqual(subjects.left);
  });
  it("hides when every candidate would cover a protected subject", () => {
    expect(placePortLabel({x:500,y:400},{width:1366,height:768},[{left:0,right:1366,top:0,bottom:768}])).toBeNull();
  });
});
