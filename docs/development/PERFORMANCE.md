# 性能策略

渲染目标 60 FPS，时钟默认每模拟秒 10 tick；2×/4× 正常对应每真实秒 20/40 tick。HUD 一秒更新一次。实际 FPS 随设备、窗口和负载变化，不承诺固定值。

宿主长帧最多计入 250ms，隐藏页不补算。海面是单平面 procedural shader，不开发 FFT/流体/浮力。未来大量环境使用 Instances / Thin Instances / LOD；当前不做大规模 benchmark。

引擎初始打包体积仍较大，后续可评估按需导入、资源懒加载和构建拆分；不要为消除警告改变游戏行为。

## Phase 1

当前仅4Ports/1Fleet。导航集中在FleetNavigationSystem，未来hundreds of fleets仍走集中tick，不为每舰队建立interval。舰队信息最多约10Hz更新，性能统计1Hz；标签每帧投影、航线复用mesh。未做大规模benchmark，当前不宣称性能达标。

## Task 03 视觉切片

2048 PCF 主阴影，船只与主要建筑投影；植被不批量投影。同模块多实例复用，源网格统一 receiveShadows，避免在 InstancedMesh setter 上设置而失效。海面和尾流单平面 shader，FXAA + ACES，关闭 bloom/SSAO。15个正式GLB约24.6MiB，编辑源约85.7MiB；独立GLB嵌入图片有重复，尚未做LOD/资源压缩。

修复手动 RAF 渲染未 beginFrame/endFrame 导致 Engine deltaTime 不更新、平滑聚焦无法前进的问题。模拟仍由自己的固定步长驱动。航线复用网格并保持可见性，不每帧创建新对象。

指定 Chrome 实测多次稳定读数59～60 FPS，交互采样曾短暂51 FPS；1×/2×/4× 对应约10/20/40 TPS。三档桌面视口已检查。此为当前4港1船短时观察，非低配设备或长时压力基准，不能承诺所有设备60FPS。构建仍有 Babylon 大chunk警告。
