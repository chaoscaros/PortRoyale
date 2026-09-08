# 测试与验收

```sh
npm run typecheck
npm run test
npm run build
```

typecheck 同时使用 tsconfig.simulation.json（只有 ES2022，无 DOM 或 Node 环境全局）独立编译核心。

Vitest 默认 Node。tests/simulation.test.ts 覆盖固定 dt 与余数、20 TPS 配置、暂停、1/2/4 倍率、不同帧分割确定性、历史快照不变、无效输入和核心依赖边界。核心测试不导入 Babylon。

运行验收：npm run dev（9999 起顺延），检查 Ocean / Sky / Island / Port Marker / Ship、GLB 状态、鼠标旋转平移缩放、暂停秒数固定、继续和倍率改变 tick 速率、缩放俯角极限不穿海面或模型。检查控制台资源/着色器错误，重新加载检查初始化。

GLB 资产加载时做三轴 10 米世界坐标校验；这是浏览器资产验收，与纯模拟单元测试分开。FPS/TPS 为真实采样，不是保证值。未来改动世界模型后增加业务行为测试，不以静态检查代替运行验收。


## 用户指定的运行与测试方式

开发服务的启动、重启由用户操作。Codex 不自行启动 dev/preview 服务；需要运行验收时告知用户所需命令并等待。只连接用户指定的现有 Chrome 标签，不自行启动 Playwright 浏览器或创建替代测试页面。默认 9999，占用顺延；若实际端口改变，请用户提供对应标签。
