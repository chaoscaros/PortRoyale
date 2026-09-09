# AI 交接

## 当前阶段与验收边界

Phase 1.5 — Task07 Hero Port Third Pass。实现与静态检查完成，Hero Port third pass仍为PARTIAL，必须等待用户视觉认可。不能声称达到《纪元1800》《纪元117》商业成品质感。所有新玩法继续冻结；不自动开启Secondary Port、Economy或Trade。

把本文件与GPT_PLANNING_BRIEF.md上传ChatGPT网页版即可制定后续提示词。细化美术时再附ART_DIRECTION、BLENDER_PIPELINE、ASSET_CATALOG和PERFORMANCE。以前Task06的第三轮推荐已在本轮执行，下一轮应先依据用户截图反馈。

## 运行方式

仓库/Users/fenglian1/projects/AI/PortRoyale；main跟踪origin/main；npm；默认9999占用顺延。服务启动/重启由用户执行。Codex只连接用户原有Chrome localhost:9999标签，没有启动服务、Playwright浏览器或替代页面。

底部舰队按钮选船，港口列表/铭牌选港，对象面板确认前往；顶部暂停/1×/2×/4×，底部聚焦/全览，F3调试。宽屏对象面板根据投影换侧，窄屏沿用右侧。经济未启用。

## 本轮实现

- Simulation、Navigation、Command、Snapshot、Data无修改，固定模拟时间与权威位置保持。Mesh仅用于表现。
- art06_site.py仍是岛屿、土建、摆放、水深的唯一高程来源。15个建筑场地、13段路网保持；自然地形过渡宽度扰动，结构基础按实际建筑收紧，挡墙分段、不同高度并半埋。后山降低并加宽，减少鼓包。
- 港口装卸、商贸、住宅、公共地标、后山五区沿既有动线精修。主路石铺、次路土铺，侧路轻微弯曲变宽，零散路缘及门前踏步，四处小型工作货堆。
- 住宅A/B/C保留三种主体，两套可选长外廊/浅阳台加门棚；源对象facadeOption与导出节点facade_0/1对应，manifest逐实例选一套。墙色、百叶、屋顶新/旧/暗/混瓦、烟囱或小老虎窗组合变化，不复制20栋房屋。
- 密冠/疏冠树分枝角度、冠幅和高度扰动，树/灌/草组局部镜像旋转后按坡度过滤；核心商业区不填森林。223个模块摆放，基础资产仍36套。
- 船尾弧面舷窗、两侧艉廊、栏杆、甲板阳台及舵装；不同帆腹与帆脚松弛、帆角补强、实际帆角到甲板的缭绳。65,747三角面，低于Task06的67,636；停泊表现朝向0.95弧度，航行朝向仍来自Snapshot。
- 继续10族1K配对PBR、4米MetricUV；屋瓦/墙/帆变化通过顶点色。地面2K颜色/法线/粗糙度由Blender原生重新烘焙，交通磨损与草土混合连续变化，水深256。没有新增另一套材质方案。
- LOD1由4套扩大到11套：地标2、棕榈2、住宅3、仓库2、热带树2。棕榈175米、树155米、住宅175米、其他240米，8米迟滞。近远各自普通实例共享几何和材质，同步切换完整模块。
- 实际浏览器发现逐Mesh原生LOD会出现建筑主体缺失而附件可见，最终改为模块整体切换，近远景已检查主体完整。增加禁用层级/TransformNode的内存成本，未声称全场景LOD或零开销。
- 默认相机alpha=-1.85、beta=1.03、radius225、target(-86,0,39)，船左前/城中右。宽屏选哈瓦那时按城市中心投影换侧，次级远标签淡化；非全局UI布局系统。
- 保持2048PCF、ACES/FXAA及原微量Bloom，无SSAO、重海洋或运行时顶点修补。静态矩阵缓存、材质共享冻结保留。

## 资产与重现

assets-source/blender/visual/build_high_end_assets.py为完整入口；art06_*.py名称沿用历史，不是旧效果。自动生成基础资产、build_lod1.py层级及共享纹理优化；正式修改全部.blend→GLB。源/GLB/manifest同时提交。

47个正式GLB共30,303,940 bytes；27张当前共享PNG共44,056,875 bytes；47个可编辑源共479,046,576 bytes，源不下载到浏览器。清理无当前GLB引用的共享PNG。资产表见ASSET_CATALOG；住宅面数包含两个可选组，运行只启用一组。

## 验证

typecheck通过；4文件40项测试通过，包含实际导出高程、配对UV、11套LOD面数和住宅两组导出节点；build通过，主chunk6.08MB/gzip1.31MB，体积警告保留。lint：Not configured。浏览器结果与最终Git校验在下方单独记录；静态通过不代表美术通过。

## 已知限制与下一轮输入

坡面仍有规则台地感，土路边缘偏硬，院落空地较大；近景冠层仍有薄片与程序生成感。门窗尺度和立面语言仍容易识别重复。船艉与帆面虽更完整，仍需手工塑形/材质精修。程序PBR不是扫描级材质；小艇和部分棚货仍次级简化。地面2K宏观图不具备近景铺贴图同等像素密度。

LOD直接切换，无交叉渐变，近远两层级常驻；没有KTX2、全场景LOD、低配或长时基准。面板换侧仅用于宽屏，铭牌无安全位置时隐藏，列表可继续选港。直线航行没有岛屿避障、碰撞或物理风力，现存限制未改变。

没有Goods/Market/Inventory/Price/Trade/Cargo/Crew/Production/Nation/Mission/Combat/Save/Server/Multiplayer。不要为了消除构建警告或视觉问题改Simulation边界。下一步仅等待用户截图确认精修优先级，不自动开展新阶段。

## Task07 运行记录 · 2026-09-09

只使用原Chrome localhost:9999标签。实际查看Default Hero、Port Close、Ship Close、Hill/Residential、Pier/Warehouse Close、Full Map；近远切换后建筑主体和选定立面均完整，宽屏选港面板可移至左边。住宅175米阈值最终调整后再查看默认画面。

2×观察20TPS。暂停位置(183.10,-46.55)、simulationTime=635.9、tick=6359；暂停选择拿骚并下令后这些数值不变，0TPS。恢复4×后精确停泊拿骚(-160,205)，距离/ETA=0，40TPS。1×为10TPS。此回归发生在住宅LOD距离最终由205调至175米之前，模拟/交互代码没有后续变化。

1920×1080最终默认短时54～59FPS，333 draw calls / 762 active meshes / 70 GPU textures。此前同一轮默认出现32～51FPS，全览航行/暂停约42～48FPS、334～336/861～863/70。最终默认样本高于Task06近港48～52FPS，但绘制、纹理与资源常驻成本增加，全览也未复现Task06的60FPS，不能据此宣称全场景性能改善或稳定不退化。GPU textures包含渲染目标，不等于27张共享PNG。无低配、长时或同镜头A/B基准。

最终typecheck、4文件40测试、build通过，主chunk约6.08MB/gzip1.31MB，保留体积警告；lint未配置。git diff --check通过，Simulation/Data差异为空。美术验收仍为PARTIAL。

1366×768、1440×900、1920×1080均实际查看，窄桌面舰队面板内容和聚焦按钮完整；1366默认53FPS短时样本。浏览器error/warn日志为空。验收后清除尺寸模拟并刷新，恢复原窗口、默认哈瓦那停泊、1×及F3隐藏。没有启动或重启用户服务。
