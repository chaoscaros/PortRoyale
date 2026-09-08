# 性能策略

渲染目标 60 FPS，时钟默认每模拟秒 10 tick；2×/4× 正常对应每真实秒 20/40 tick。HUD 一秒更新一次。实际 FPS 随设备、窗口和负载变化，不承诺固定值。

宿主长帧最多计入 250ms，隐藏页不补算。海面是单平面 procedural shader，不开发 FFT/流体/浮力。未来大量环境使用 Instances / Thin Instances / LOD；当前不做大规模 benchmark。

引擎初始打包体积仍较大，后续可评估按需导入、资源懒加载和构建拆分；不要为消除警告改变游戏行为。

## Phase 1

当前仅4Ports/1Fleet。导航集中在FleetNavigationSystem，未来hundreds of fleets仍走集中tick，不为每舰队建立interval。舰队信息最多约10Hz更新，性能统计1Hz；标签每帧投影、航线复用mesh。未做大规模benchmark，当前不宣称性能达标。
