# 舰队方向（未实现）

Fleet = 1..N Ships。未来包含 cargo、crew、speed、position、destination、route。第一步只建立测试船舰队与按模拟秒航行。

点击 Fleet → 点击目标港口 → Move Command → 纯模拟移动 → 抵达港口。帧率不能影响航程，暂停和倍率应自然影响移动。

当前 GLB 是静态测试资产，不是可操控舰队。下一阶段应明确航线/陆地规避和抵达判定，不从 Mesh 位置读权威状态。
