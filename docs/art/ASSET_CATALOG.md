# 资产登记

| 名称 | 路径 | 来源 | 作者 | License / 权利状态 | 自制 |
|---|---|---|---|---|---|
| ship_test 源模型 | assets-source/blender/ships/ship_test.blend | scripts/create_test_ship.py | 本项目（Codex 辅助生成） | 项目自制，未另授第三方许可 | 是 |
| ship_test 运行模型 | public/assets/models/ship_test.glb | 上述 Blender 导出 | 本项目 | 同上 | 是 |
| 岛屿/港口占位物 | src/rendering/ports/PortRenderer.ts | 程序几何 | 本项目 | 同上 | 是 |
| 海面/天空 | src/rendering/ocean/createOcean.ts、GameRenderer.ts | 程序材质与基础网格 | 本项目 | 同上 | 是 |

未使用原作模型、音频、贴图或 UI 图片。仓库尚未指定整体开源许可证。新增外部资源必须记录精确来源与许可，不能假设“免费”等于可再分发。

## Phase 1 程序资源

PortRenderer.ts 替代已删除的 createTestWorld.ts：四港程序岛/码头/金色marker、HTML名称标签；FleetRenderer.ts新增选中圈/航线。来源与作者均为本项目（Codex辅助），自制、未另授第三方许可。复用原ship_test.glb/.blend，本轮未新建或重制模型。
