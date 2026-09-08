# Blender → Hero Asset → GLB

## 可复现流程

Blender 4.5.13 LTS。新一轮唯一完整构建入口：

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python assets-source/blender/visual/build_high_end_assets.py
```

脚本复用build_visual_assets.py的基础建模函数，重制英雄船、建筑、码头、环境并输出35个资产。末尾调用scripts/optimize_visual_glb.py，把重复嵌入图片按内容散列合并到public/assets/textures/shared；请等待完整构建结束再刷新游戏，避免读取生成中的文件。此前build_visual_assets.py是Task03重现入口，会覆盖现行资产，不应用它单独更新Task05；build_hero_assets.py 仅用于重现 Task04。

## 坐标与命名

1 Blender单位=1米；Blender +Z上、-Y船首，export_yup=True后Babylon右手+Y上/+Z船首。运行时不任意缩放。船pivot为水线中心，建筑/道具以基底为参考。旧ship_test仍用于三轴10米校准，不作为可见船。当前sloop.blend/.glb保留稳定资产路径，但内部已升级为双桅横帆英雄船，UI标注BRIG，不新增第二支舰队。

source按ships/buildings/ports/props/environment分类，runtime按相同分类GLB；部件使用语义名称如barrel_roof_tiles、arcade、moulded_frame、ratline。source场景保留独立可编辑部件，保存场景依赖到压缩.blend；导出副本按材质合并，实例共享几何。

## Hero与模块流程

轮廓/尺度 → 部件结构 → 石基/厚檐/拱廊/门窗 → PBR分区 → UV → GLB → 实际镜头验收。港口以单栋模块与独立码头、石岸、街道、道具组合，不保存整城为单一不可编辑网格。地形提供城镇台地和码头开口，布局manifest只是Rendering数据。植被使用枝叶几何，不使用球形冠层。

## UV、材质和贴图

MetricUV 按部件投影轴和米制尺度展开，AtlasUV 为独立颜色图集坐标，TerrainUV 是整岛连续烘焙坐标。禁止 Smart Project 覆盖已烘焙坐标。七组自制1024 PBR图片：wood/deck/cloth/wall/roof/stone/ground，各Color、Normal、Roughness。Normal/Roughness是Non-Color；材质显式连接Principled BSDF。墙/瓦与树叶使用表面顶点色；地形烘焙后必须移除 BeachMask/RockMask，不能作为 COLOR_0 输出。源文件打包所用图片，普通运行不需Blender。

GLB保留几何二进制，图片URI使用../../textures/shared/内容散列.png。Babylon预处理器将其规范化，并限制为当前站点/assets目录；不放宽到任意远程地址。运行时必须同时交付public/assets/models与public/assets/textures/shared，不能只复制一个GLB。manifest列出每项实际textureUris与共享集合。独立原始贴图保留用于编辑，运行只请求所需共享图片。

## 预算与LOD

建议：Hero Ship LOD0 30k—80k tris，Hero Building 8k—25k，Secondary 3k—10k，Props 500—5k，Palm 2k—8k（实例化）。当前部分地标/棕榈高于参考，面数详见ASSET_CATALOG；需以性能观测判断，下一轮可制作LOD1/2，当前并未交付真实LOD。

1K 微表面图为默认，颜色图集为1254，连续地表为2K，确有近景收益才提高分辨率，不无差别4K。共享贴图去重，避免重复纹理造成网络/GPU浪费。首次生成图片和大规模UV会耗时，勿为减等待省略可编辑源。

## 验证与版本控制

资产测试校验源文件、GLB版本/长度/面数/缓冲区边界、图片路径、manifest模块引用、船体跨水线。浏览器另外检查材质加载、坐标校准、接地、阴影、帆装与默认构图。提交.blend、GLB、共享纹理、脚本和manifest；忽略.blend1、临时截图与工具缓存。禁止原作提取资源进入仓库。

## Task05 材质生产与可编辑源

完整入口调用 art05_surfaces.py（材质和双 UV）、art05_modules.py（商宅、港务所、设施）、art05_terrain.py（Blender Cycles 原生 EMIT 烘焙）、art05_layout.py（港区布局）。export_sources.py 可重新导出已经编辑的源文件，保留 ACTIVE 顶点色；最终自动运行共享贴图优化。源文件保留独立部件并打包引用图片，运行副本按材质合并、实例共享几何。

颜色材质命名 art05_wall/wood/deck/stone_atlas_PBR；老化屋面和帆布继续使用 hero_roof/cloth_PBR，地表为 art05_baked_terrain_PBR。共享原图 public/assets/textures/art05/surface_atlas.png 为 1254×1254 四区图集，每区约 627 像素，不能记作 2K。地表 terrain_color.png 为 2048×2048；微表面 Normal/Roughness 仍为 1K。当前图集为原创 AI 辅助颜色素材，法线/粗糙度另行制作，并非扫描级逐像素匹配 PBR。金属和绳索使用独立常量 PBR，植被使用几何叶片与顶点色，无叶片照片纹理。

生成记录：内置 image_gen，generate 模式，无参考图。保存到 public/assets/textures/art05/surface_atlas.png；不依赖 .codex 私有路径。提示词：Original single square 2x2 atlas, no labels, margins or text. Top left weathered warm ivory lime plaster with fine pores, ochre mottling, chips and gray rain stains. Top right aged honey oak vertical planks with dark caulk, grain, knots and worn edges. Bottom left warm gray limestone irregular rectangular cobbles with mortar and dirt. Bottom right tropical dry soil, olive grass, pale sand and tiny pebbles. Orthographic shadowless diffuse albedo, subdued earthy PBR source, no perspective, gloss, baked shadows, illustration or procedural-noise look.

图集仅作为材质输入；Blender 将整岛材质和高度遮罩烘焙成连续颜色图。临时遮罩使用 while 循环从源数据删除，避免删除属性后 Blender 引用失效。导出测试防止黑色遮罩乘到运行表面及图集错误 UV 通道回归。

所有 35 套源和 GLB、原始纹理、共享纹理、manifest、脚本同时提交。几何自制，AI 辅助颜色素材不声称纯手绘或原作授权资产；没有原作资源、私人素材和启动依赖。当前仅 LOD0，新增植物实例仍需真实低配评估。
