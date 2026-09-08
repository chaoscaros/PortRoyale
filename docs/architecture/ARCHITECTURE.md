# 架构

```text
React HUD / Input
  → Command
  → GameApplication.dispatch
  → Simulation (authoritative)
  → frozen WorldSnapshot
  → React HUD + GameRenderer
```

GameApplication 持有 Simulation 与 GameRenderer，负责 requestAnimationFrame、ResizeObserver、visibilitychange、取消帧和 dispose。UI 每秒接收一次统计，按钮命令立即发布新快照。渲染每帧消费快照。

SimulationClock 只接收经过宿主处理的 elapsed seconds：累加 elapsed × timeScale，以固定 dt 触发 tick，保留余数。simulationTime = tickCount × tickSeconds。暂停期间不累计新时间，保留已有余数。核心无现实时间、随机、浏览器和渲染依赖。

宿主把长帧截断为最多 250ms，隐藏标签期间不推进，重新可见重置基准，防止追赶风暴。因此不是离线时间模拟。时钟本身不丢传入时间。TPS 是每真实秒执行的 tick，正常倍率对应 10/20/40；FPS 是实际 frame 数，不是硬编码目标。

WorldSnapshot 当前只有 clock。测试岛、测试船、港口标记都是静态渲染夹具，没有 Fleet 权威状态；下一阶段才增加位置和 ID。禁止从渲染 Mesh 反推模拟。

Renderer 使用 Babylon WebGL、右手坐标、ArcRotateCamera、简单天空、程序海面、primitive 岛屿。GLB loader 在放置前校验三个命名方向节点（10 米），不做任意缩放。

当前没有 persistence 模块、data 定义或事件总线的空架子；需要时再添加。SAVE_FORMAT 和 DATA_MODEL 是未来设计。
