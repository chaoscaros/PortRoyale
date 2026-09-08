# ChatGPT 长期规划简报

## 使用方法

本文件与 AI_HANDOFF.md 可单独上传给 ChatGPT 网页版，作为制定后续 Codex 开发提示词的上下文。此文件保存长期方向，实际完成度和验证结果以 AI_HANDOFF 为准。请不要把“未来设计”误认为已实现功能。

## 愿景与定位

制作直接在浏览器运行的 3D 航海贸易经营游戏，玩法结构、低买高卖循环、港口交互、舰队管理、自动贸易、城市经营、大地图与后期海战体验高度参考《海商王3》。当前用于个人学习、自娱自乐和技术研究，没有商业发行计划。不为差异化刻意改变成熟玩法。

所有代码以 Web 原生方式重新实现；不依赖原作 EXE、DLL、反编译逻辑，不破解资源包或 DRM。资产优先自制，原作提取资源不进入公开仓库。个人实验资源只能放在 Git 忽略的 local-assets，不能成为启动依赖。

## 技术路线

React + TypeScript + Vite + Babylon.js + Vitest，npm。当前 WebGL，暂不做 WebGPU、服务器或多人。默认端口 9999，占用自动顺延。

Simulation 和 Rendering 严格分离：输入 → Command → Simulation → World State → 不可变 Snapshot / Event → UI 与 Renderer。Simulation 可在 Node/Vitest 独立运行，不能 import Babylon、React、DOM，不能读取 window/document 或现实系统时间。Mesh 只是表现映射，绝不是世界状态。

固定步长默认 10 tick/s，可配置。simulationTime、tickCount、timeScale、paused 属于模拟。渲染帧独立、目标 60 FPS；倍率改变模拟而非 requestAnimationFrame。未来 GameDate 由模拟秒转换，不取系统日期。

## 资产路线

Blender 是正式船只、建筑、码头、环境建模工具，流程 .blend → GLB → Babylon。1 Blender Unit = 1 米。经实际测试：Blender +Z 向上、-Y 船首；启用 +Y Up 导出后，在 Babylon 右手场景 +Y 向上、+Z 船首。船只 pivot 在水线中心，建筑在底面中心，应用旋转和缩放，禁止导入后用任意小数缩放补救。

运行时正式只支持 GLB。未来 PBR 纹理按需配置，LOD0/1/2 按近中远规划。自制源文件留在 assets-source/blender，运行资源放 public/assets，许可与作者记录在 ASSET_CATALOG。

## 玩法长期方向

经济：生产 → 库存 → 消费 → 供需 → 价格 → 玩家贸易。库存、供给、人口、消费、短缺共同影响价格，不使用永久固定买卖价。经济 MVP 10～12 种商品，可从粮食、木材、砖、工具、布料、糖、咖啡、可可、烟草、棉花、朗姆酒、肉类中选择。生产以后支持原料 → 建筑 → 产品 → 市场，例如甘蔗 → 朗姆酒厂 → 朗姆酒。

舰队：1..N 船只组成 Fleet，持有货物、船员、速度、位置、目的港、路线。先做点击舰队、点击港口、Move Command、模拟时间航行、抵达；航行先于经济。港口规模先 4，再 12、25、40+，不一次做完整加勒比海。未来自动贸易支持循环港口、买卖数量、最低库存、最大买价、最小卖价。

海战晚于经济与舰队：以后再评估操船、风、火炮、船体、船员、登船、投降和击沉。国家、任务、海盗和生产城市都不是工程奠基阶段内容。

## 阶段规划

Phase 0：工程、Clock、测试场景、策略相机、Blender 管线、接力文档。
Phase 1：World Map + Ports + Fleet Navigation Foundation 已实现四港、单舰队、选择确认、直线航行、抵达和改道；已在用户指定 Chrome 完成航行回归。没有贸易。
Phase 1.5 / Phase Visual AAA Slice：AAA Visual Vertical Slice First。用户认为Task03视觉不达标，要求向现代高规格PC策略经营游戏靠拢。Task04重制1个Hero Port、1艘Hero Ship、正式HUD、材质、气氛与构图；玩法冻结。后续优先Hero Port / Hero Ship second pass或Visual Polish 02，只有用户明确确认画面达标才讨论经济。
Phase 2 延后：Goods + Market + Fleet Cargo + Buy/Sell Foundation。后续细化 Inventory / Stock / Dynamic Price，先完成可验证的经济闭环，尚未实施。
之后：自动贸易 → 生产与城市 → 国家关系与任务 → 海战；每阶段单独细化、验收。

未来联机：Browser Command → WebSocket → Server Authoritative Simulation → Snapshot → Browser。当前只保留边界，不实现服务器、同步或预测。未来存档保存带 saveVersion 的 Simulation State，不保存 Mesh、Material、DOM 或相机运行对象。

## 制定下一轮提示词时

结合 AI_HANDOFF 的实际进度，指定目标、禁止范围、涉及模块、命令/数据边界、测试、浏览器验收和文档更新要求。要求提交与推送结果如实报告。不要一次启动多个阶段，不要求本轮完成完整游戏。

当前优先级：高级感 > 精致度 > 材质 > 构图 > HUD/UI > Hero Asset > 氛围 > 性能 > 新玩法。架构边界和已有航行正确性必须保持。经济、贸易、货舱暂缓，只有用户明确决定恢复后才制定对应开发任务。

视觉目标：Stylized Realism，17—18世纪加勒比殖民港口，向《纪元1800》这类现代桌面策略游戏的质感靠拢，不复制具体素材。否定低模小游戏、toy-like diorama和网页卡片工具感。集中英雄港、英雄船、HUD和气氛，不平均重制四港；真实美术验收以AI_HANDOFF及用户反馈为准，不能凭面数或功能PASS宣称3A达标。


## 用户指定的运行与测试方式

开发服务的启动、重启由用户操作。Codex 不自行启动 dev/preview 服务；需要运行验收时告知用户所需命令并等待。只连接用户指定的现有 Chrome 标签，不自行启动 Playwright 浏览器或创建替代测试页面。默认 9999，占用顺延；若实际端口改变，请用户提供对应标签。
