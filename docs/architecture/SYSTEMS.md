# 系统边界

| 系统 | 当前职责 | 以后 |
|---|---|---|
| SimulationClock | fixed dt、pause、scale、tick | GameDate 映射 |
| Simulation | 命令分发、快照 | 世界状态与确定性系统 |
| GameApplication | frame、统计、resize、dispose | UI 输入桥 |
| GameRenderer | 静态夹具、海水时间、GLB | Fleet ID 与表现映射 |
| StrategyCamera | 平移、旋转、距离俯角限制 | 地图约束 |
| React HUD | 时间、性能、资产状态、命令 | 选择和信息面板 |

模拟 Tick 与帧数独立。未来 systems 执行顺序需明确记录，随机数需种子化，不用 Math.random 或系统日期决定结果。
