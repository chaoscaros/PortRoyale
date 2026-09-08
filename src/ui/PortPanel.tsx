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
        <div className="port-engraving" aria-hidden="true">
          <svg
            viewBox="0 0 320 100"
            fill="none"
            stroke="currentColor"
            strokeWidth="1"
          >
            <path d="M10 86h300M30 86V54l25-16 25 16v32M34 54h42M45 66v12m16-12v12M99 86V37h35v49M95 37l21-15 22 15M108 37V17h16v20M115 17V7m-5 5h10M109 54a7 7 0 0 1 14 0v15h-14zM152 86V52h60v34M145 52l37-20 37 20M162 61v15m14-15v15m14-15v15m14-15v15M243 86l8-51h20l8 51M246 35h30v-7h-30zM254 28V16h14v12M249 16h24l-12-11zM8 94q40-8 80 0t80 0 80 0 64 0" />
          </svg>
        </div>
        <p>
          {port.id === "port-havana"
            ? "红瓦、钟楼与棕榈环绕的海湾。扬帆的旅程，从这座温暖的港口开始。"
            : "海风掠过码头，一处等待舰队抵达的热带港湾。"}
        </p>
        {fleet && (
          <div className="selected-fleet">
            <Icon name="ship" size={18} />
            <div>
              <span>执行舰队</span>
              <strong>晨曦号</strong>
            </div>
            <small>{fleet.status === "docked" ? "已停泊" : "航行中"}</small>
          </div>
        )}
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
