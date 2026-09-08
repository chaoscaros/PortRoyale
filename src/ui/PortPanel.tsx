import type { DebugSnapshot } from "../app/GameApplication";
import type { Command } from "../simulation/Simulation";
import { Icon } from "./Icon";
export function PortPanel({
  debug,
  onClose,
  onCommand,
}: {
  debug: DebugSnapshot | null;
  onClose: () => void;
  onCommand: (command: Command) => void;
}) {
  const port = debug?.world.ports.find(
    (p) => p.id === debug.selection.selectedPortId,
  );
  if (!port || !debug) return null;
  const fleet = debug.world.fleets.find(
      (f) => f.id === debug.selection.selectedFleetId,
    ),
    same =
      fleet &&
      (fleet.currentPortId === port.id || fleet.destinationPortId === port.id);
  return (
    <section className="port-panel object-panel" aria-label="港口信息">
      <div className="port-card-art">
        <Icon name="port" size={44} />
        <div>
          <p className="eyebrow">加勒比海 · 港口</p>
          <h2>{port.displayName}</h2>
        </div>
        <button
          className="icon-button"
          aria-label="关闭港口面板"
          onClick={onClose}
        >
          <Icon name="close" size={16} />
        </button>
      </div>
      <div className="port-card-content">
        <p>
          {port.id === "port-havana"
            ? "红瓦、钟楼与棕榈环绕的海湾。扬帆的旅程，从这座温暖的港口开始。"
            : "海风掠过码头，一处等待舰队抵达的热带港湾。"}
        </p>
        <button
          className="primary-button"
          disabled={!fleet || !!same}
          onClick={() =>
            fleet &&
            onCommand({
              type: "move-fleet",
              fleetId: fleet.id,
              destinationPortId: port.id,
            })
          }
        >
          <Icon name="ship" size={17} />
          {same
            ? fleet?.status === "docked"
              ? "已停泊于此"
              : "正前往此港"
            : `前往${port.displayName}`}
          <Icon name="arrow" size={16} />
        </button>
        {!fleet && <small>先选择舰队，再下达航行指令。</small>}
      </div>
    </section>
  );
}
