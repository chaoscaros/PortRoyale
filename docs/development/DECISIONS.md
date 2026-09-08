# 决策记录

- 2026-09-08：采用用户指定的 React/TypeScript/Vite/Babylon/Vitest/npm。
- 默认 10 TPS，以整数 tick 派生模拟秒，支持配置与 1/2/4 倍率。
- Babylon 使用右手坐标，避免 GLB 根节点左右手转换；Blender -Y 船首经导出变 +Z。
- 原型使用自制一个 GLB 船和程序几何，不做正式资产批量制作。
- GameApplication 对宿主卡顿截断 250ms，隐藏标签不补算；纯 Clock 不截断输入。
- 用户指定开发/预览端口从 9999 起，自动顺延。
- 当前不配置 lint、不做完整存档、航行、贸易、网络；未来文档不是已实现功能。
