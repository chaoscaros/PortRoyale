# AI 开发约定

开始工作前依次阅读：
1. docs/planning/GPT_PLANNING_BRIEF.md
2. docs/planning/AI_HANDOFF.md
3. docs/planning/TODO.md
4. docs/architecture/ARCHITECTURE.md
5. docs/architecture/SYSTEMS.md
6. docs/development/CODE_CONVENTIONS.md

严格遵守当前阶段边界。Simulation 不得依赖 React、Babylon、DOM 或现实系统时间；以 Command → Simulation → Snapshot 驱动表现。禁止用 Mesh 作为权威状态。

npm 是包管理器。开发与预览默认 9999，占用自动顺延，不抢占其他项目端口。正式资产 Blender → GLB；私人资源只放被忽略的 local-assets/。

结束前执行 npm run typecheck、npm run test、npm run build；如果配置 lint 还须运行 lint。如实区分静态检查和浏览器实际验收。
更新 AI_HANDOFF、TODO、架构文档，追加 DEVLOG 和 CHANGELOG；不要另建重复进度文件。按用户授权进行中文提交和推送，不自动开启下一阶段。


## 用户指定的运行与测试方式

开发服务的启动、重启由用户操作。Codex 不自行启动 dev/preview 服务；需要运行验收时告知用户所需命令并等待。只连接用户指定的现有 Chrome 标签，不自行启动 Playwright 浏览器或创建替代测试页面。默认 9999，占用顺延；若实际端口改变，请用户提供对应标签。
