# AI 交接

## 当前阶段

Task 01 / Phase 0：网页版 3D 航海贸易经营游戏工程地基。高度参考《海商王3》玩法，代码 Web 原生实现，个人学习与娱乐定位。没有开始 Phase 1。

本文件可与 GPT_PLANNING_BRIEF.md 一起上传 ChatGPT 网页版。请 ChatGPT 据此生成下一轮 Codex 提示词，明确范围、禁止项、测试与交接要求；不要把未来设计当作现有功能。

## 当前可运行状态

仓库 /Users/fenglian1/projects/AI/PortRoyale。npm ci 后由用户执行 npm run dev；默认端口 9999，占用自动顺延，以 Vite 输出为准。代码不依赖 Blender 安装或 local-assets 即可运行。

重要用户约定：开发服务启动/重启由用户操作。Codex 不自行启动服务或 Playwright 浏览器，只使用用户指定的现有 Chrome 页面进行验收。本轮已关闭之前自行启动的服务和测试标签。用户指定页面为 http://localhost:9999/。

## 已实现

- React + TypeScript strict + Vite + Babylon.js WebGL + Vitest + npm 锁文件。
- SimulationClock：10 tick/s 默认、可配置，fixed timestep、余数保留、tickCount、simulationTime、pause、1/2/4 timeScale。
- Command → Simulation → 不可变 WorldSnapshot；Simulation 无 React/Babylon/DOM 依赖。
- GameApplication：frame 协调、ResizeObserver、visibility、统计、dispose。长帧上限 250ms，隐藏页不补算，未来不应误认作离线推进。
- 基础程序海面、天空、低多边形岛屿、港口标记、自制测试船。测试船静态摆放，无权威 Fleet 实体。
- 策略相机：左键旋转、右键平移、滚轮缩放、距离/俯角/平移范围限制。
- 中文 HUD：真实 FPS/TPS、模拟秒、tick、暂停、倍率和 GLB 校验状态。
- Blender 4.5.13 自制船源文件、生成脚本、GLB，导入时校验三轴 10 米节点。右手 Babylon：+Y 上，+Z 船首；Blender：+Z 上、-Y 船首。
- planning/design/architecture/art/development/history 文档体系与 AGENTS 约定。

## 部分完成

静态验收：最终 typecheck（包含无 DOM 核心编译）、10 项 Vitest、build 通过；未配置 lint。build 仍有大 chunk 警告。

运行验收：已在用户指定 Chrome localhost:9999 标签看到 Ocean、Island、Port Marker、Ship、HUD 和 GLB 方向/尺度通过状态；FPS 观测 60，1× TPS 10、2× TPS 20。暂停后模拟秒 121.6 / Tick 1216 保持不变，TPS 变 0；暂停时切换 2× 不解除暂停，继续后按 2× 推进。

4× 控件已切换，但尚未读到稳定 TPS 40；相机旋转动作已执行但尚无动作后画面对照，右键平移、滚轮与极限未完成运行验收。用户页面后来显示连接被拒绝，服务由用户启动后再补这些检查。不声称运行验收全部通过。此前自建标签已关闭，服务进程已停止。

## 尚未实现

港口世界数据、舰队选择与航行、贸易、动态价格、库存与经济、自动贸易、生产、国家、任务、海盗、海战、完整地图、完整存档、服务器和多人。DATA_MODEL 等中的目标接口只是设计。

## 最近工作

2026-09-08 从空 main 仓库创建工程和自制资产，完善长期规划；按用户要求默认端口改为 9999，明确服务由用户管理、验收使用指定 Chrome 标签。最终静态检查已通过，Git 交付以仓库日志和本轮最终回复为准。

## 重要文件

- src/simulation/SimulationClock.ts、Simulation.ts：纯模拟边界。
- src/app/GameApplication.ts：宿主生命周期和 UI 桥。
- src/rendering/GameRenderer.ts、ocean/createOcean.ts、scene/createTestWorld.ts。
- src/input/StrategyCamera.ts、src/ui/Game.tsx。
- scripts/create_test_ship.py、assets-source/blender/ships/ship_test.blend。
- src/rendering/assets/loadTestShip.ts、public/assets/models/ship_test.glb。
- tests/simulation.test.ts。
- GPT_PLANNING_BRIEF.md、TODO.md、../architecture/ARCHITECTURE.md、DATA_MODEL.md、../art/BLENDER_PIPELINE.md。

## 已知问题

正式构建有大 chunk 提示（Babylon 主包体积较大）；构建成功，未做体积优化和大型场景 benchmark。场景美术为工程占位质量，无天气和海水物理。触控操作未专项验收，桌面鼠标是当前目标。

## 技术债

未来按需拆分 Babylon 导入与加载；扩展数据模型时确保深层快照不可变并增加行为测试；需进一步覆盖销毁/重建、资源加载失败、隐藏标签和设备兼容性。依赖边界测试递归扫描 simulation，另有无 DOM 类型的核心编译检查。

## 无明确理由不要修改

Simulation/Rendering 分离、固定步长与模拟秒、Command/Snapshot 入口、右手坐标和米制 GLB、npm 锁文件、9999 顺延策略、用户控制服务/现有标签验收约定，以及以此文件作为唯一当前进度记录。

## 推荐下一任务

World Map + Ports + Fleet Navigation Foundation
