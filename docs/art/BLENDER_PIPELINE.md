# Blender → GLB → Babylon 管线

## 可复现的本轮资产

Blender 4.5.13 LTS 已执行 scripts/create_test_ship.py，保存 assets-source/blender/ships/ship_test.blend 并导出 public/assets/models/ship_test.glb。普通运行不依赖本地 Blender；重新制作资产才需要它。

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/create_test_ship.py
```

脚本在独立后台 Blender 场景生成一个测试船，不操作用户正在编辑的场景。

## 已实测的坐标和尺寸

- Blender：+Z 向上，-Y 船首，+X 横向；1 Blender Unit = 1 米。
- GLB：export_yup=True（+Y Up）。转换为 (x, z, -y)。
- Babylon：导入前 scene.useRightHandedSystem = true；+Y 向上、+Z 船首。
- axis_forward 在 Blender (0,-10,0)，导入世界坐标应为 (0,0,10)。
- axis_up (0,0,10) → (0,10,0)，axis_right (10,0,0) 保持不变。
- loadTestShip 在资产放置前以 0.001 米容差验证这三个点；通过才显示 HUD 验证完成。此为真实 GLB/Babylon 导入检查，不只依据说明书。

测试船船体长 20 米、宽 8 米，origin 位于船体水线中心。场景对船只仅平移、旋转，不缩放。不要为了改朝向切换 Babylon 左右手系。

## 正式规范

船 pivot 在水线中心；建筑 pivot 在地面底部中心。建模完成应用 Rotation / Scale，检查单位与尺寸。禁止用 scale=0.00437 一类导入补丁修资产。

命名：ship_sloop、ship_brig、ship_frigate、building_warehouse、building_shipyard、port_pier、prop_barrel、prop_crate。已增加 ships/buildings/ports/props/environment 分类；ship_test 保留为技术校准资产。

正式运行格式只用 GLB，不混用 OBJ/FBX/外置 glTF。PBR 根据需要使用 Base Color、Normal、Metallic/Roughness，不强求每物体全套贴图。LOD0/1/2 近中远规划，当前没有实际三套 LOD。

每个新资产：登记作者/来源/许可 → 检查 pivot/尺度/方向 → 导出 GLB → Babylon 导入检查 → 真实策略视角截图 → 检查远距离辨识。私人资源放被忽略的 local-assets/，不得成为正常启动依赖。

参考：[Blender glTF 导出](https://docs.blender.org/manual/en/4.0/addons/import_export/scene_gltf2.html)、[Babylon glTF 坐标转换](https://doc.babylonjs.com/features/featuresDeepDive/mesh/copies/instances)。规范以本仓库实际导入校验结果为准。

## Task 03 正式视觉资产

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python assets-source/blender/visual/build_visual_assets.py
```

脚本重新生成15个独立 .blend 和对应分类 GLB、三张1024纹理及 visual/manifest.json。每个源场景保存独立可编辑部件；导出副本按材质合并，运行实例共享网格/材质。修改脚本可完整复现，生成 .blend1 备份已忽略。源文件打包纹理；UV 使用 Smart Project，GLB 嵌入图片，运行不依赖外部工具。

纹理为自制 timber、sail_canvas、lime_plaster；其他材质以 PBR base color/roughness/metallic 区分，未提供完整烘焙 normal/ORM 套件。海面法线由 shader 程序生成。所有新资产目前只有 LOD0，实例复用不等于已经实现 LOD。

sloop 包围盒（Babylon 米制）约 X[-3.445,3.445]、Y[-2,22.020]、Z[-12,16.025]；含艏斜桅长28.025米、宽6.89米，6222三角面、9材质。水面Y=0，船底在水下2米；实例不额外缩放。运行先执行旧船三轴校准，再隐藏/释放旧船并创建正式船。

交付检查：tests/assets.test.ts 校验所有源文件和GLB存在、二进制长度/glTF版本、图片嵌入、实际索引三角数与清单相符、模块引用和船体跨水线。浏览器另验轮廓、接地、阴影和航向，不能用这些静态检查替代画面验收。
