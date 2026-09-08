# 正式资产目录 · Task 04

全部由本项目自制，无第三方模型和原作提取内容。24项资产均保留可编辑.blend与运行GLB，当前LOD0 only。Hero/Secondary指本轮呈现职责，不代表商业品质认证。ship_test作为历史校准资产保留，不重复显示。

| Asset | Category / Role | Source .blend | Runtime .glb | tris | 材质数 | Status |
|---|---|---|---|---:|---:|---|
| building_house_a | buildings / Hero | assets-source/blender/buildings/building_house_a.blend | public/assets/models/buildings/building_house_a.glb | 12046 | 8 | 重制升级 |
| building_house_b | buildings / Hero | assets-source/blender/buildings/building_house_b.blend | public/assets/models/buildings/building_house_b.glb | 16342 | 8 | 重制升级 |
| building_house_c | buildings / Hero | assets-source/blender/buildings/building_house_c.blend | public/assets/models/buildings/building_house_c.glb | 11086 | 8 | 新增正式模块 |
| building_warehouse | buildings / Hero | assets-source/blender/buildings/building_warehouse.blend | public/assets/models/buildings/building_warehouse.glb | 19570 | 9 | 重制升级 |
| building_warehouse_b | buildings / Hero | assets-source/blender/buildings/building_warehouse_b.blend | public/assets/models/buildings/building_warehouse_b.glb | 17610 | 9 | 新增正式模块 |
| building_governor | buildings / Hero | assets-source/blender/buildings/building_governor.blend | public/assets/models/buildings/building_governor.glb | 32190 | 8 | 重制升级 |
| building_church | buildings / Hero | assets-source/blender/buildings/building_church.blend | public/assets/models/buildings/building_church.glb | 26138 | 9 | 重制升级 |
| sloop | ships / Hero | assets-source/blender/ships/sloop.blend | public/assets/models/ships/sloop.glb | 66810 | 9 | 重制升级 |
| port_pier | ports / Hero | assets-source/blender/ports/port_pier.blend | public/assets/models/ports/port_pier.glb | 5724 | 3 | 重制升级 |
| port_lighthouse | ports / Hero | assets-source/blender/ports/port_lighthouse.blend | public/assets/models/ports/port_lighthouse.glb | 4436 | 6 | 重制升级 |
| prop_stone_wall | props / Secondary | assets-source/blender/props/prop_stone_wall.blend | public/assets/models/props/prop_stone_wall.glb | 1804 | 1 | 新增正式模块 |
| port_quay | ports / Hero | assets-source/blender/ports/port_quay.blend | public/assets/models/ports/port_quay.glb | 5544 | 1 | 新增正式模块 |
| port_street | ports / Hero | assets-source/blender/ports/port_street.blend | public/assets/models/ports/port_street.glb | 13640 | 1 | 新增正式模块 |
| prop_barrel | props / Secondary | assets-source/blender/props/prop_barrel.blend | public/assets/models/props/prop_barrel.glb | 1692 | 2 | 沿用次级 |
| prop_crate | props / Secondary | assets-source/blender/props/prop_crate.blend | public/assets/models/props/prop_crate.glb | 92 | 2 | 沿用次级 |
| prop_skiff | props / Secondary | assets-source/blender/props/prop_skiff.blend | public/assets/models/props/prop_skiff.glb | 308 | 3 | 沿用次级 |
| prop_cart | props / Secondary | assets-source/blender/props/prop_cart.blend | public/assets/models/props/prop_cart.glb | 2012 | 2 | 新增正式模块 |
| prop_market_awning | props / Secondary | assets-source/blender/props/prop_market_awning.blend | public/assets/models/props/prop_market_awning.glb | 224 | 2 | 新增正式模块 |
| prop_palm | environment / Hero | assets-source/blender/environment/prop_palm.blend | public/assets/models/environment/prop_palm.glb | 13104 | 3 | 重制升级 |
| prop_palm_b | environment / Hero | assets-source/blender/environment/prop_palm_b.blend | public/assets/models/environment/prop_palm_b.glb | 14112 | 3 | 新增正式模块 |
| prop_tropical_tree | environment / Hero | assets-source/blender/environment/prop_tropical_tree.blend | public/assets/models/environment/prop_tropical_tree.glb | 7460 | 2 | 重制升级 |
| prop_bush | environment / Secondary | assets-source/blender/environment/prop_bush.blend | public/assets/models/environment/prop_bush.glb | 1244 | 2 | 重制升级 |
| prop_rock | environment / Secondary | assets-source/blender/environment/prop_rock.blend | public/assets/models/environment/prop_rock.glb | 960 | 1 | 新增正式模块 |
| island_visual_test | environment / Hero | assets-source/blender/environment/island_visual_test.blend | public/assets/models/environment/island_visual_test.glb | 42240 | 1 | 重制升级 |

## 材质与纹理使用

每项精确材质名和运行纹理URI见assets-source/blender/visual/manifest.json中的materials/textureUris。建筑主要使用石灰灰泥、陶瓦、石基、木材、涂装、窗玻璃；船使用船体木、甲板木、帆布、绳索、铁、黄铜与涂装；石岸街道使用石材；植被使用树干材质和叶片分色；地形为地表Normal/Roughness加顶点着色。

原始编辑贴图public/assets/textures/hero_{wood,deck,cloth,wall,roof,stone,ground}_{color,normal,roughness}.png，共21张1024×1024。运行GLB共享20张内容散列图片（地形color由顶点颜色代替）；均自制程序PBR贴图。原Task03 timber/sail_canvas/lime_plaster保留作历史资产，现行PBR以hero组为准。

英雄船sloop路径沿用，实际为双桅BRIG：66810三角面，包围盒X约±6.8米（含横桁）、Y[-2.40,31.02]、Z[-16.15,22.05]，pivot水线中心，未加运行缩放。部件包括曲面船体、船舷、甲板、艉楼、桅杆、横桁、主帆/前帆、索具/绳梯、舵、绞盘与舱口。

参考预算与例外：BLENDER_PIPELINE.md。总督府/教堂和棕榈高于建议，需后续专门LOD处理；小箱、小艇和遮棚仍为次级简化资产，不作为本轮Hero近景质量标杆。
