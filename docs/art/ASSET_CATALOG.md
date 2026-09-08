# 资产清单

本轮全部为项目自制（Self-created），无第三方模型或原作提取资源。作者：本项目开发过程；使用范围：随本项目源文件交付，未引入额外第三方许可。15个正式视觉资产均为 LOD0 only；数据源 assets-source/blender/visual/manifest.json，包含材质名、包围盒和哈瓦那布局。所有 .blend 可独立编辑，运行仅加载 GLB。

| 资产 | Blender源文件 | 运行资源 | 三角面 | 材质数 | GLB KiB |
|---|---|---|---:|---:|---:|
| sloop | assets-source/blender/ships/sloop.blend | public/assets/models/ships/sloop.glb | 6222 | 9 | 3379.5 |
| building_house_a | assets-source/blender/buildings/building_house_a.blend | public/assets/models/buildings/building_house_a.glb | 714 | 7 | 1699.2 |
| building_house_b | assets-source/blender/buildings/building_house_b.blend | public/assets/models/buildings/building_house_b.glb | 1206 | 8 | 1624.8 |
| building_warehouse | assets-source/blender/buildings/building_warehouse.blend | public/assets/models/buildings/building_warehouse.glb | 978 | 7 | 1712.3 |
| building_governor | assets-source/blender/buildings/building_governor.blend | public/assets/models/buildings/building_governor.glb | 1630 | 8 | 3303.6 |
| building_church | assets-source/blender/buildings/building_church.blend | public/assets/models/buildings/building_church.glb | 502 | 7 | 1685.3 |
| port_lighthouse | assets-source/blender/ports/port_lighthouse.blend | public/assets/models/ports/port_lighthouse.glb | 676 | 5 | 1696.8 |
| port_pier | assets-source/blender/ports/port_pier.blend | public/assets/models/ports/port_pier.glb | 4704 | 2 | 1808.5 |
| prop_barrel | assets-source/blender/props/prop_barrel.blend | public/assets/models/props/prop_barrel.glb | 1692 | 2 | 1617.9 |
| prop_crate | assets-source/blender/props/prop_crate.blend | public/assets/models/props/prop_crate.glb | 156 | 2 | 1560.6 |
| prop_skiff | assets-source/blender/props/prop_skiff.blend | public/assets/models/props/prop_skiff.glb | 308 | 3 | 1565.2 |
| prop_palm | assets-source/blender/environment/prop_palm.blend | public/assets/models/environment/prop_palm.glb | 356 | 3 | 1576.8 |
| prop_tropical_tree | assets-source/blender/environment/prop_tropical_tree.blend | public/assets/models/environment/prop_tropical_tree.glb | 708 | 3 | 1575.8 |
| prop_bush | assets-source/blender/environment/prop_bush.blend | public/assets/models/environment/prop_bush.glb | 360 | 1 | 13.1 |
| island_visual_test | assets-source/blender/environment/island_visual_test.blend | public/assets/models/environment/island_visual_test.glb | 13110 | 1 | 411.0 |

## 共享纹理

public/assets/textures/timber.png、sail_canvas.png、lime_plaster.png：各1024×1024，自制程序纹理，生成方法见 build_visual_assets.py。同一资产实例共享材质/贴图；GLB 为独立交付而嵌入图片，不同资产之间仍存在图片重复，后续可优化资源去重。

## 技术基线

assets-source/blender/ships/ship_test.blend → public/assets/models/ship_test.glb，由 scripts/create_test_ship.py 自制。仅用于三轴/尺寸导入校验，校验后释放，不与正式 sloop 重复显示。旧测试海面纹理若保留，只作历史实验资源，正式海面使用 shader。

## 后续预算

本轮实际面数如上；后续hero船可按20k～60k三角面、常规建筑2k～10k、小道具0.2k～3k的量级评估，必须结合视距与实例数量实测，不要求低于预算的资产无意义加面。1K纹理优先，确有近景收益再用2K；当前没有4K纹理。LOD0已交付，LOD1/2只是未来方案。
