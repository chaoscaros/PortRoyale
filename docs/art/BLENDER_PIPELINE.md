# Blender → Hero Asset → GLB

## 可复现流程

Blender 4.5.13 LTS。Task07 当前完整构建入口：

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python assets-source/blender/visual/build_high_end_assets.py
```

脚本复用build_visual_assets.py的基础建模函数，重制英雄船、建筑、码头、环境并输出36套基础资产并制作11套LOD1。末尾调用scripts/optimize_visual_glb.py，把重复嵌入图片按内容散列合并到public/assets/textures/shared；请等待完整构建结束再刷新游戏，避免读取生成中的文件。此前build_visual_assets.py是Task03重现入口，会覆盖现行资产，不应用它单独更新Task05；build_hero_assets.py 仅用于重现 Task04。

## 坐标与命名

1 Blender单位=1米；Blender +Z上、-Y船首，export_yup=True后Babylon右手+Y上/+Z船首。运行时不任意缩放。船pivot为水线中心，建筑/道具以基底为参考。旧ship_test仍用于三轴10米校准，不作为可见船。当前sloop.blend/.glb保留稳定资产路径，但内部已升级为双桅横帆英雄船，UI标注BRIG，不新增第二支舰队。

source按ships/buildings/ports/props/environment分类，runtime按相同分类GLB；部件使用语义名称如barrel_roof_tiles、arcade、moulded_frame、ratline。source场景保留独立可编辑部件，保存场景依赖到压缩.blend；导出副本按材质合并，实例共享几何。

## Hero与模块流程

轮廓/尺度 → 部件结构 → 石基/厚檐/拱廊/门窗 → PBR分区 → UV → GLB → 实际镜头验收。港口以单栋模块与独立码头、石岸、街道、道具组合，不保存整城为单一不可编辑网格。地形提供城镇台地和码头开口，布局manifest只是Rendering数据。植被使用枝叶几何，不使用球形冠层。

## UV、材质和贴图

当前所有普通材质使用MetricUV：按部件主轴、模块坐标和4米铺贴尺度展开，BaseColor/Normal/Roughness共用同一通道。地形使用整岛TerrainUV，三通道共同烘焙；禁止重展开覆盖。Normal/Roughness为Non-Color；PBR材质显式连接Principled BSDF。墙/瓦与叶片保留BYTE_COLOR表面颜色，地形临时遮罩在烘焙后删除。源文件打包所用图片，运行无需Blender。

GLB保留几何二进制，图片URI使用../../textures/shared/内容散列.png。Babylon预处理器将其规范化，并限制为当前站点/assets目录；不放宽到任意远程地址。运行时必须同时交付public/assets/models与public/assets/textures/shared，不能只复制一个GLB。manifest列出每项实际textureUris与共享集合。独立原始贴图保留用于编辑，运行只请求所需共享图片。

## 预算与LOD

建议：Hero Ship LOD0 30k—80k tris，Hero Building 8k—25k，Secondary 3k—10k，Props 500—5k，Palm 2k—8k（实例化）。部分地标高于参考，面数详见ASSET_CATALOG；需以性能观测判断。Task07交付11套LOD1，其余资产仍仅LOD0。下文Task05/06为历史流程，当前切换规则以Task07段落为准。

当前颜色/法线/粗糙度配对族均为1K，连续地表为2K；1254颜色图集仅属于Task05历史输入，确有近景收益才提高分辨率，不无差别4K。共享贴图去重，避免重复纹理造成网络/GPU浪费。首次生成图片和大规模UV会耗时，勿为减等待省略可编辑源。

## 验证与版本控制

资产测试校验源文件、GLB版本/长度/面数/缓冲区边界、图片路径、manifest模块引用、船体跨水线。浏览器另外检查材质加载、坐标校准、接地、阴影、帆装与默认构图。提交.blend、GLB、共享纹理、脚本和manifest；忽略.blend1、临时截图与工具缓存。禁止原作提取资源进入仓库。

## Task05 材质生产记录（历史，当前由Task06替代）

完整入口调用 art05_surfaces.py（材质和双 UV）、art05_modules.py（商宅、港务所、设施）、art05_terrain.py（Blender Cycles 原生 EMIT 烘焙）、art05_layout.py（港区布局）。export_sources.py 可重新导出已经编辑的源文件，保留 ACTIVE 顶点色；最终自动运行共享贴图优化。源文件保留独立部件并打包引用图片，运行副本按材质合并、实例共享几何。

颜色材质命名 art05_wall/wood/deck/stone_atlas_PBR；老化屋面和帆布继续使用 hero_roof/cloth_PBR，地表为 art05_baked_terrain_PBR。共享原图 public/assets/textures/art05/surface_atlas.png 为 1254×1254 四区图集，每区约 627 像素，不能记作 2K。地表 terrain_color.png 为 2048×2048；微表面 Normal/Roughness 仍为 1K。当前图集为原创 AI 辅助颜色素材，法线/粗糙度另行制作，并非扫描级逐像素匹配 PBR。金属和绳索使用独立常量 PBR，植被使用几何叶片与顶点色，无叶片照片纹理。

生成记录：内置 image_gen，generate 模式，无参考图。保存到 public/assets/textures/art05/surface_atlas.png；不依赖 .codex 私有路径。提示词：Original single square 2x2 atlas, no labels, margins or text. Top left weathered warm ivory lime plaster with fine pores, ochre mottling, chips and gray rain stains. Top right aged honey oak vertical planks with dark caulk, grain, knots and worn edges. Bottom left warm gray limestone irregular rectangular cobbles with mortar and dirt. Bottom right tropical dry soil, olive grass, pale sand and tiny pebbles. Orthographic shadowless diffuse albedo, subdued earthy PBR source, no perspective, gloss, baked shadows, illustration or procedural-noise look.

图集仅作为材质输入；Blender 将整岛材质和高度遮罩烘焙成连续颜色图。临时遮罩使用 while 循环从源数据删除，避免删除属性后 Blender 引用失效。导出测试防止黑色遮罩乘到运行表面及图集错误 UV 通道回归。

所有 35 套源和 GLB、原始纹理、共享纹理、manifest、脚本同时提交。几何自制，AI 辅助颜色素材不声称纯手绘或原作授权资产；没有原作资源、私人素材和启动依赖。当前仅 LOD0，新增植物实例仍需真实低配评估。

## Task06 [historical] · 当前生产规范

build_high_end_assets.py 调用 art06_materials.py、art06_vegetation.py、art06_site.py、art06_civilworks.py、art06_quay.py、art06_terrain.py、art06_layout.py，最后自动执行 build_lod1.py 和共享纹理优化。只新增一个必要的场地土建模块 port_civilworks；其余为既有资产的第二轮精修。LOD1属于同资产层级，不是新增城市内容。

材质命名 art06_<Family>；10个材质族每族1K配对颜色/法线/粗糙度，统一4米铺贴；所有通道使用MetricUV，不再单独截取颜色图集。颜色、法线、粗糙度由同一确定性高度/磨损场生成，不声称扫描级PBR。SurfaceTint以BYTE_COLOR保存墙脚老化、少量立面与瓦片色差，减少原FLOAT_COLOR属性开销。

HarborTerrain的2K颜色/法线/粗糙度均由Blender Cycles EMIT烘焙到同一TerrainUV；Normal和Roughness为Non-Color。烘焙后删除全部临时高度/材质遮罩，禁止导出COLOR_0遮罩乘色。256水深图HarborDepth.png由同一场地高程生成，线性编码(height+8)/48；海面在图边缘平滑过渡到深海，避免出现矩形浅水区。

台地和路网数据记录在manifest.site：plots的尺寸/标高供复核，roads包含起终点标高和宽度。运行只读取资产与摆放，不导入Python美术逻辑；水深图同样是外部资源。building source保留可编辑部件，土建模块保留台基、边石、阶梯与坡道，绝不以单张贴图替代施工结构。

build_lod1.py为总督府、教堂、棕榈A/B删除非轮廓细节并保守简化，保存独立*_lod1.blend/GLB，保留原LOD0。Babylon用原生mesh LOD，棕榈175米、地标240米；其他模块不声称已有LOD。Hero Ship不优先压缩。源、运行、shared PNG、manifest和脚本一起交付；旧材质图保留历史编辑来源，但运行仅请求当前实际引用文件。

资产测试增加地形导出顶点与台地标高一致性、配对材质UV、LOD面数和标签保护区；浏览器仍必须检查真实接地、帆装、冠层与LOD切换，静态检查不证明美术达标。

## Task07 · 立面组合、群落与自然场地

继续维护既有art06_*制作模块，文件名是历史来源，不另复制整套生成器。36个基础资产不增加；11个LOD1包含地标/棕榈4套和住宅A/B/C、仓库A/B、热带树A/B新增7套。所有几何修改保存.blend并重导GLB。

住宅主体和两组可选外廊/浅阳台遮棚同存一个源文件。源对象facadeOption=0/1；导出按(材质,可选组)合并，节点命名base__材质与facade_0/1__材质。manifest.havana.facade确定实例启用哪组，运行只启用/隐藏正式导出部件，不修改顶点。LOD必须保留同名可选组。Runtime按整个模块切换LOD0/1，阈值含8米迟滞；近远两个层级仍用普通实例共享几何。实际验收发现逐Mesh原生LOD路径出现主体缺失，最终采用同步切换，避免主体和立面各自切换。三种住宅主体、百叶不对称、墙色、新/旧/暗/混瓦四档顶点色和选择性烟囱/小老虎窗组合变化，不复制材质图片。

群落由三棵高低不同的树与林下灌草构成，平面布局交替镜像、旋转，再按坡度/道路/海拔排除不合理成员；镜像的是群落位置，不对模型施加负缩放。树枝朝向、冠幅与枝高也从源头打散。山脊保留露岩，住宅与道路不种满。

场地保留结构基底标高，外围回填宽度随位置变化；只在下坡侧做有缺口的半埋挡墙，嵌岩与道路来自同一高程。主轴保留石路；次路弯曲、变宽，住宅小路采用泥土地面和间断边石。连续DirtMask由离路距离与侵蚀方向混合，不以矩形in_town布尔值画硬色块。地表三通道重新烘焙，同一水深图同步输出。

船尾使用弧形艉板、收分侧廊、弯曲阳台与舵连杆；帆鼓度偏向一侧、帆脚随高度变化，补角片与主受力索连接帆角。继续共享既有PBR族；不新增帆布图片。最终材质尺度、接地与可见索具以浏览器多角度核查为准。
