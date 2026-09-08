# Blender → Hero Asset → GLB

## 可复现流程

Blender 4.5.13 LTS。新一轮唯一完整构建入口：

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python assets-source/blender/visual/build_hero_assets.py
```

脚本复用build_visual_assets.py的基础建模函数，重制英雄船、建筑、码头、环境并输出24个资产。末尾调用scripts/optimize_visual_glb.py，把重复嵌入图片按内容散列合并到public/assets/textures/shared；请等待完整构建结束再刷新游戏，避免读取生成中的文件。此前build_visual_assets.py是Task03重现入口，会覆盖现行资产，不应用它单独更新Task04。

## 坐标与命名

1 Blender单位=1米；Blender +Z上、-Y船首，export_yup=True后Babylon右手+Y上/+Z船首。运行时不任意缩放。船pivot为水线中心，建筑/道具以基底为参考。旧ship_test仍用于三轴10米校准，不作为可见船。当前sloop.blend/.glb保留稳定资产路径，但内部已升级为双桅横帆英雄船，UI标注BRIG，不新增第二支舰队。

source按ships/buildings/ports/props/environment分类，runtime按相同分类GLB；部件使用语义名称如barrel_roof_tiles、arcade、moulded_frame、ratline。source场景保留独立可编辑部件，保存场景依赖到压缩.blend；导出副本按材质合并，实例共享几何。

## Hero与模块流程

轮廓/尺度 → 部件结构 → 石基/厚檐/拱廊/门窗 → PBR分区 → UV → GLB → 实际镜头验收。港口以单栋模块与独立码头、石岸、街道、道具组合，不保存整城为单一不可编辑网格。地形提供城镇台地和码头开口，布局manifest只是Rendering数据。植被使用枝叶几何，不使用球形冠层。

## UV、材质和贴图

Smart Project用于当前部件；七组自制1024 PBR图片：wood/deck/cloth/wall/roof/stone/ground，各Color、Normal、Roughness。Normal/Roughness是Non-Color；材质显式连接Principled BSDF。地形与树叶有顶点颜色。源文件打包所用图片，普通运行不需Blender。

GLB保留几何二进制，图片URI使用../../textures/shared/内容散列.png。Babylon预处理器将其规范化，并限制为当前站点/assets目录；不放宽到任意远程地址。运行时必须同时交付public/assets/models与public/assets/textures/shared，不能只复制一个GLB。manifest列出每项实际textureUris与共享集合。独立原始贴图保留用于编辑，运行只请求所需共享图片。

## 预算与LOD

建议：Hero Ship LOD0 30k—80k tris，Hero Building 8k—25k，Secondary 3k—10k，Props 500—5k，Palm 2k—8k（实例化）。当前部分地标/棕榈高于参考，面数详见ASSET_CATALOG；需以性能观测判断，下一轮可制作LOD1/2，当前并未交付真实LOD。

1K为默认，确有近景收益才升2K，不无差别4K。共享贴图去重，避免重复纹理造成网络/GPU浪费。首次生成图片和大规模UV会耗时，勿为减等待省略可编辑源。

## 验证与版本控制

资产测试校验源文件、GLB版本/长度/面数/缓冲区边界、图片路径与PNG签名、manifest模块引用、船体跨水线。浏览器另外检查材质加载、坐标校准、接地、阴影、帆装与默认构图。提交.blend、GLB、共享纹理、脚本和manifest；忽略.blend1、临时截图与工具缓存。禁止原作提取资源进入仓库。
