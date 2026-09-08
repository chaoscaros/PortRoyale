# 远洋 · 网页航海贸易原型

个人学习、自娱自乐与技术研究项目。高度参考《海商王3》的玩法结构与节奏，以 Web 原生代码重新实现。本仓库当前实现 Phase 1 四港世界与单舰队直线航行；不含贸易、经济或战斗，运行验收状态见 AI_HANDOFF。

## 运行

需要 Node.js 22.12+（或满足当前 Vite engines 的更新版本）、npm，以及支持 WebGL 的桌面浏览器。

```sh
npm ci
npm run dev
```

默认 http://127.0.0.1:9999 ，占用时自动尝试 10000、10001 等，以终端输出为准。预览也采用这一规则。不要结束占用端口的其他项目。

```sh
npm run typecheck
npm run test
npm run build
npm run preview
```

左键拖动旋转、右键拖动平移、滚轮缩放。HUD 提供暂停/继续及 1×/2×/4×。模型 GLB 已提交，正常启动不需要 Blender。

## 交给 ChatGPT 网页版

上传 [长期规划简报](docs/planning/GPT_PLANNING_BRIEF.md) 和 [当前交接](docs/planning/AI_HANDOFF.md)。请它基于两份文档制定下一轮 Codex 提示词；如果要详细约束，再上传 TODO、ARCHITECTURE、DATA_MODEL。

[完整文档导航](docs/README.md) · [Blender 管线](docs/art/BLENDER_PIPELINE.md)

开发服务由用户自行启动/重启；Codex 验收复用用户提供的 Chrome 标签，不另启自动化浏览器。

Phase 1：选择测试船 → 点击港口名称/标记 → 确认前往 → 航行 → 抵达。支持中途改道，无岛屿避障。
