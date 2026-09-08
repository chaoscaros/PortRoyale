# 代码约定

TypeScript strict，React 函数组件。npm 与锁文件一起维护。职责按 simulation / rendering / app / input / ui 划分，不把逻辑堆到 main.tsx。

Simulation 无 Babylon、React、DOM、系统时间依赖，单位使用秒和米。Command 表达意图；Snapshot 不暴露可变状态，新增嵌套对象要复制并冻结。未来随机必须由种子驱动。

原型渲染夹具不提前变成业务实体。只为真实需求建模块，不创建几十个空文件。资源在正式目录登记，private local-assets 被忽略。

结束执行 typecheck/test/build，更新交接和 TODO，追加历史；中文 commit。当前未配置 lint，因此不宣称 lint 通过。


## 用户指定的运行与测试方式

开发服务的启动、重启由用户操作。Codex 不自行启动 dev/preview 服务；需要运行验收时告知用户所需命令并等待。只连接用户指定的现有 Chrome 标签，不自行启动 Playwright 浏览器或创建替代测试页面。默认 9999，占用顺延；若实际端口改变，请用户提供对应标签。
