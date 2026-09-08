import { useEffect, useRef, useState } from "react";
import { GameApplication, type DebugSnapshot } from "../app/GameApplication";
import type { TimeScale } from "../simulation/SimulationClock";
import { Icon } from "./Icon";
import { FleetPanel } from "./FleetPanel";
import { PortPanel } from "./PortPanel";
import { DeveloperHUD } from "./DeveloperHUD";
import "./game.css";
export function Game() {
  const canvas = useRef<HTMLCanvasElement>(null),
    labels = useRef<HTMLDivElement>(null),
    app = useRef<GameApplication | null>(null);
  const [debug, setDebug] = useState<DebugSnapshot | null>(null),
    [error, setError] = useState(""),
    [showDebug, setShowDebug] = useState(false),
    [showPorts, setShowPorts] = useState(false);
  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      if (e.key === "F3") {
        e.preventDefault();
        setShowDebug((v) => !v);
      }
    };
    window.addEventListener("keydown", key);
    try {
      app.current = new GameApplication(
        canvas.current!,
        labels.current!,
        setDebug,
      );
    } catch (e) {
      setError(`场景启动失败：${String(e)}`);
    }
    return () => {
      window.removeEventListener("keydown", key);
      app.current?.dispose();
      app.current = null;
    };
  }, []);
  const clock = debug?.world.clock,
    loading = !debug || debug.assetStatus.includes("正在加载"),
    assetError = debug?.assetStatus.startsWith("资源错误");
  return (
    <main>
      <canvas
        ref={canvas}
        aria-label="加勒比海图，左键旋转，右键平移，滚轮缩放"
        onContextMenu={(e) => e.preventDefault()}
      />
      <div ref={labels} className="map-labels" aria-label="海图港口" />
      <header className="game-header">
        <div className="brand">
          <Icon name="compass" size={34} />
          <div>
            <h1>远洋</h1>
            <span>PORT ROYALE</span>
          </div>
        </div>
        <div className="header-divider" />
        <div className="world-caption">
          <strong>加勒比海</strong>
          <span>航海原型 · 视觉切片</span>
        </div>
        <div className="funds">
          <Icon name="coins" size={18} />
          <span>
            资金 <b>—</b>
            <small>经济系统未启用</small>
          </span>
        </div>
        <div className="time-controls" aria-label="航海时间控制">
          <button
            className="pause-button"
            disabled={!clock}
            aria-label={clock?.paused ? "继续" : "暂停"}
            aria-pressed={clock?.paused ?? false}
            onClick={() =>
              app.current?.dispatch({
                type: "SetPaused",
                paused: !clock?.paused,
              })
            }
          >
            <Icon name={clock?.paused ? "play" : "pause"} size={17} />
            <span>{clock?.paused ? "继续" : "暂停"}</span>
          </button>
          <div className="speed-controls">
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
        </div>
      </header>
      <nav className="port-navigation" aria-label="港口导航">
        <button
          className="nav-toggle"
          aria-expanded={showPorts}
          onClick={() => setShowPorts((v) => !v)}
        >
          <Icon name="map" size={18} />
          海域港口<span>04</span>
        </button>
        {showPorts && (
          <div className="port-list">
            {debug?.world.ports.map((port) => (
              <button
                key={port.id}
                onClick={() => {
                  app.current?.select({ kind: "port", id: port.id });
                  setShowPorts(false);
                }}
              >
                <Icon name="port" size={16} />
                {port.displayName}
                <Icon name="arrow" size={14} />
              </button>
            ))}
          </div>
        )}
      </nav>
      <div className="scene-caption">
        <span>西印度群岛</span>
        <p>海风与远方</p>
        <div />
      </div>
      <div className="north-compass" aria-hidden="true">
        <span>北</span>
        <Icon name="compass" size={38} />
      </div>
      <FleetPanel
        debug={debug}
        onClose={() => app.current?.clearSelection("fleet")}
        onFocus={() => app.current?.focusView("fleet")}
      />
      <PortPanel
        debug={debug}
        onClose={() => app.current?.clearSelection("port")}
        onCommand={(command) => app.current?.dispatch(command)}
      />
      {showDebug && <DeveloperHUD debug={debug} />}
      <div className="notice" role="status">
        {debug?.commandMessage}
      </div>
      <footer className="game-footer">
        <div className="camera-help">
          拖动旋转 <i /> 右键平移 <i /> 滚轮缩放
        </div>
        <div className="quick-actions">
          <button
            onClick={() => {
              if (debug)
                app.current?.select({
                  kind: "fleet",
                  id: debug.world.fleets[0].id,
                });
            }}
          >
            <Icon name="ship" size={18} />
            舰队
          </button>
          <button onClick={() => app.current?.focusView("havana")}>
            <Icon name="port" size={18} />
            哈瓦那
          </button>
          <button onClick={() => app.current?.focusView("world")}>
            <Icon name="map" size={18} />
            海图全览
          </button>
          <button
            aria-pressed={showDebug}
            onClick={() => setShowDebug((v) => !v)}
          >
            <Icon name="settings" size={18} />
            开发者信息 <kbd>F3</kbd>
          </button>
        </div>
        <span className="build-caption">VISUAL FOUNDATION · 03</span>
      </footer>
      {loading && (
        <div className="loading-screen" role="status">
          <Icon name="compass" size={44} />
          <h2>海风将至</h2>
          <p>正在准备港口与帆船…</p>
        </div>
      )}
      {(error || assetError) && (
        <div className="error" role="alert">
          {error || debug?.assetStatus}
        </div>
      )}
    </main>
  );
}
