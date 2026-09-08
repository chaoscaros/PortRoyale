import type { DebugSnapshot } from "../app/GameApplication";
import type { Command } from "../simulation/Simulation";
import { distance } from "../simulation/world/types";
import type { PickTarget } from "../input/SelectionState";
export function FleetPanel({
  debug,
  onSelect,
  onCommand,
}: {
  debug: DebugSnapshot | null;
  onSelect: (target: PickTarget) => void;
  onCommand: (command: Command) => void;
}) {
  const fleet = debug?.world.fleets.find(
    (f) => f.id === debug.selection.selectedFleetId,
  );
  const selectedPort = debug?.world.ports.find(
    (p) => p.id === debug.selection.selectedPortId,
  );
  const destination = debug?.world.ports.find(
    (p) => p.id === fleet?.destinationPortId,
  );
  const current = debug?.world.ports.find((p) => p.id === fleet?.currentPortId);
  const remaining =
    fleet && destination ? distance(fleet.position, destination.position) : 0;
  const same =
    fleet &&
    selectedPort &&
    (fleet.currentPortId === selectedPort.id ||
      fleet.destinationPortId === selectedPort.id);
  return (
    <aside className="fleet-panel" aria-label="舰队与目的港">
      <p className="eyebrow">试航日志 · 四港海域</p>
      <h2>测试舰队</h2>
      {!fleet ? (
        <>
          <p>点击海上的帆船，选择你的舰队。</p>
          <button
            className="fleet-select"
            disabled={!debug}
            onClick={() =>
              debug && onSelect({ kind: "fleet", id: debug.world.fleets[0].id })
            }
          >
            选择测试舰队
          </button>
        </>
      ) : (
        <>
          <div className="fleet-state">
            <b>{fleet.status === "sailing" ? "航行中" : "已停泊"}</b>
            <span>{current?.displayName ?? "海上"}</span>
          </div>
          <dl>
            <div>
              <dt>目的港</dt>
              <dd>{destination?.displayName ?? "—"}</dd>
            </div>
            <div>
              <dt>速度</dt>
              <dd>{fleet.speed} 世界单位/模拟秒</dd>
            </div>
            <div>
              <dt>剩余距离</dt>
              <dd>{remaining.toFixed(1)} 世界单位</dd>
            </div>
            <div>
              <dt>预计抵达</dt>
              <dd>{(remaining / fleet.speed).toFixed(1)} 模拟秒</dd>
            </div>
          </dl>
          <small>
            位置{" "}
            <span data-testid="fleet-position">
              {fleet.position.x.toFixed(2)}, {fleet.position.z.toFixed(2)}
            </span>
          </small>
        </>
      )}
      <div className="target-port">
        <span>目的港选择</span>
        {selectedPort ? (
          <>
            <h3>{selectedPort.displayName}</h3>
            <button
              className="sail-button"
              disabled={!fleet || !!same}
              onClick={() =>
                fleet &&
                onCommand({
                  type: "move-fleet",
                  fleetId: fleet.id,
                  destinationPortId: selectedPort.id,
                })
              }
            >
              {same
                ? fleet?.status === "docked"
                  ? "已停泊于此"
                  : "已前往此港"
                : `前往${selectedPort.displayName}`}
            </button>
            {!fleet && <small>先选择舰队，再下达航行指令。</small>}
          </>
        ) : (
          <p>点击海图上的港口名称或金色标记。</p>
        )}
      </div>
      <p className="command-message" role="status">
        {debug?.commandMessage}
      </p>
      <small>直线试航 · 尚无岛屿避障</small>
    </aside>
  );
}
