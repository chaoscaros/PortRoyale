import { useEffect, useRef, useState } from "react";
import { GameApplication, type DebugSnapshot } from "../app/GameApplication";
import type { TimeScale } from "../simulation/SimulationClock";
import "./game.css";
export function Game() {
  const canvas = useRef<HTMLCanvasElement>(null),
    app = useRef<GameApplication | null>(null);
  const [debug, setDebug] = useState<DebugSnapshot | null>(null),
    [error, setError] = useState("");
  useEffect(() => {
    try {
      app.current = new GameApplication(canvas.current!, setDebug);
    } catch (e) {
      setError(`3D 场景启动失败，请检查 WebGL 支持。${String(e)}`);
    }
    return () => {
      app.current?.dispose();
      app.current = null;
    };
  }, []);
  const clock = debug?.world.clock;
  return (
    <main>
      <canvas
        ref={canvas}
        aria-label="航海测试海域，左键旋转，右键平移，滚轮缩放"
        onContextMenu={(e) => e.preventDefault()}
      />
      <header className="masthead">
        <span className="emblem">⚓</span>
        <div>
          <p>PORT ROYALE · WEB EXPERIMENT</p>
          <h1>
            远洋 <span>航海贸易原型</span>
          </h1>
        </div>
        <span className="edition">基础海域 / 01</span>
      </header>
      <aside className="location">
        <p>试航日志 · PROTOTYPE</p>
        <h2>一切，从海上开始。</h2>
        <div className="rule" />
        <span>测试岛屿 / 港口标记 / 自制帆船</span>
        <small>工程奠基阶段 · 尚未开放航行与贸易</small>
      </aside>
      <section className="hud" aria-label="模拟调试面板">
        <div className="hud-title">
          <span>航海时钟</span>
          <b>{clock?.paused ? "已暂停" : "运行中"}</b>
        </div>
        <div className="time" data-testid="simulation-time">
          {(clock?.simulationTime ?? 0).toFixed(1)}
          <small>模拟秒</small>
        </div>
        <div className="controls">
          <button
            disabled={!clock}
            aria-pressed={clock?.paused ?? false}
            onClick={() =>
              app.current?.dispatch({
                type: "SetPaused",
                paused: !clock?.paused,
              })
            }
          >
            {clock?.paused ? "▶ 继续" : "Ⅱ 暂停"}
          </button>
          {([1, 2, 4] as TimeScale[]).map((speed) => (
            <button
              key={speed}
              aria-pressed={clock?.timeScale === speed}
              onClick={() =>
                app.current?.dispatch({
                  type: "SetTimeScale",
                  timeScale: speed,
                })
              }
            >
              {speed}×
            </button>
          ))}
        </div>
        <div className="metrics">
          <span>
            FPS <b>{debug?.fps ?? "—"}</b>
          </span>
          <span>
            模拟 TPS <b>{debug?.tps ?? "—"}</b>
          </span>
          <span>
            Tick <b>{clock?.tickCount ?? 0}</b>
          </span>
        </div>
        <small className="asset-status">
          {debug?.assetStatus ?? "准备场景…"}
        </small>
      </section>
      <footer>
        <span>左键拖动 · 旋转　 /　 右键拖动 · 平移　 /　 滚轮 · 缩放</span>
        <span>WEBGL · 10 TICKS / SIM SECOND</span>
      </footer>
      {error && (
        <div className="error" role="alert">
          {error}
        </div>
      )}
    </main>
  );
}
