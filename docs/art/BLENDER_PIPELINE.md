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

命名：ship_sloop、ship_brig、ship_frigate、building_warehouse、building_shipyard、port_pier、prop_barrel、prop_crate。当前只有 ship_test；以后按类型增加 assets-source/blender 下目录，避免空资产堆积。

正式运行格式只用 GLB，不混用 OBJ/FBX/外置 glTF。PBR 根据需要使用 Base Color、Normal、Metallic/Roughness，不强求每物体全套贴图。LOD0/1/2 近中远规划，当前没有实际三套 LOD。

每个新资产：登记作者/来源/许可 → 检查 pivot/尺度/方向 → 导出 GLB → Babylon 导入检查 → 真实策略视角截图 → 检查远距离辨识。私人资源放被忽略的 local-assets/，不得成为正常启动依赖。

参考：[Blender glTF 导出](https://docs.blender.org/manual/en/4.0/addons/import_export/scene_gltf2.html)、[Babylon glTF 坐标转换](https://doc.babylonjs.com/features/featuresDeepDive/mesh/copies/instances)。规范以本仓库实际导入校验结果为准。
