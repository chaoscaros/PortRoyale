import type { DebugSnapshot } from "../app/GameApplication";
export function DeveloperHUD({ debug }: { debug: DebugSnapshot | null }) {
  const clock = debug?.world.clock,
    fleet = debug?.world.fleets[0];
  return (
    <aside className="developer-hud" aria-label="开发者信息">
      <h2>
        开发者信息 <small>F3</small>
      </h2>
      <dl>
        <div>
          <dt>FPS / TPS</dt>
          <dd>
            {debug?.fps ?? 0} / {debug?.tps ?? 0}
          </dd>
        </div>
        <div>
          <dt>Simulation seconds</dt>
          <dd data-testid="simulation-time">
            {clock?.simulationTime.toFixed(1) ?? 0}
          </dd>
        </div>
        <div>
          <dt>Tick / 倍率</dt>
          <dd>
            {clock?.tickCount ?? 0} / {clock?.timeScale ?? 1}×
          </dd>
        </div>
        <div>
          <dt>状态</dt>
          <dd>{clock?.paused ? "已暂停" : "运行中"}</dd>
        </div>
        <div>
          <dt>Ports / Fleets</dt>
          <dd>
            {debug?.world.ports.length ?? 0} / {debug?.world.fleets.length ?? 0}
          </dd>
        </div>
        <div>
          <dt>Fleet position</dt>
          <dd data-testid="fleet-position">
            {fleet?.position.x.toFixed(2)}, {fleet?.position.z.toFixed(2)}
          </dd>
        </div>
      </dl>
      <p>{debug?.assetStatus}</p>
      <small>直线航行 · 无岛屿避障</small>
    </aside>
  );
}
