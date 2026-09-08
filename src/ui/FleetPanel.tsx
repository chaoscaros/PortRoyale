import type { DebugSnapshot } from "../app/GameApplication";
import { distance } from "../simulation/world/types";
import { VesselPortrait } from "./VesselPortrait";
import { Icon } from "./Icon";
export function FleetPanel({
  debug,
  onClose,
  onFocus,
}: {
  debug: DebugSnapshot | null;
  onClose: () => void;
  onFocus: () => void;
}) {
  const fleet = debug?.world.fleets.find(
    (f) => f.id === debug.selection.selectedFleetId,
  );
  if (!fleet || !debug) return null;
  const destination = debug.world.ports.find(
      (p) => p.id === fleet.destinationPortId,
    ),
    current = debug.world.ports.find((p) => p.id === fleet.currentPortId);
  const remaining = destination
    ? distance(fleet.position, destination.position)
    : 0;
  return (
    <section className="fleet-panel object-panel" aria-label="舰队信息">
      <div className="object-illustration">
        <VesselPortrait />
        <span>双桅横帆船</span>
      </div>
      <div className="object-content">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">你的舰队</p>
            <h2>
              晨曦号 <span>DAWN · BRIG</span>
            </h2>
          </div>
          <button
            className="icon-button"
            aria-label="关闭舰队面板"
            onClick={onClose}
          >
            <Icon name="close" size={16} />
          </button>
        </div>
        <div className="fleet-state">
          <span
            className={fleet.status === "sailing" ? "status sailing" : "status"}
          >
            {fleet.status === "sailing" ? "航行中" : "已停泊"}
          </span>
          <span>
            {current?.displayName ?? "海上"}
            {destination && (
              <>
                {" "}
                <Icon name="arrow" size={14} /> {destination.displayName}
              </>
            )}
          </span>
        </div>
        <dl className="fleet-stats">
          <div>
            <dt>航速</dt>
            <dd>
              {fleet.speed}
              <small>单位 / 模拟秒</small>
            </dd>
          </div>
          <div>
            <dt>距离</dt>
            <dd>
              {remaining.toFixed(1)}
              <small>世界单位</small>
            </dd>
          </div>
          <div>
            <dt>预计抵达</dt>
            <dd>
              {(remaining / fleet.speed).toFixed(1)}
              <small>模拟秒</small>
            </dd>
          </div>
        </dl>
        <button className="text-button" onClick={onFocus}>
          <Icon name="focus" size={14} />
          聚焦舰队
        </button>
      </div>
    </section>
  );
}
