# 调试

黑屏：检查 WebGL 支持、控制台 shader/资源错误，确认 npm dev 的实际端口。页面有启动失败提示，GLB 错误会显示在 HUD。

船只方向/尺寸错误：先检查 BLENDER_PIPELINE 的三个校验节点和 Blender scale，不在 Renderer 随意缩放。素材缺失：确认 public/assets/models/ship_test.glb 存在；可用 Blender 脚本重建。

时间问题：先跑 Clock 测试，再检查宿主 visibility 和 250ms 截断。暂停时 TPS 应最终变 0，显示有一秒采样延迟；倍率控制不自动解除暂停。不要用 FPS 作为速度乘数。

端口占用：默认 9999 自动顺延，以 Vite 输出为准，不结束其他项目进程。

## 舰队不移动

确认已选择舰队和港口并点击前往；检查CommandResult、paused、timeScale、status=sailing、destination、speed>0以及NavigationSystem是否被fixed tick调用。同目标命令no-op是正常行为。

## 舰队视觉不跟随

先看WorldSnapshot位置是否变化，再查FleetRenderer的FleetId映射、GLB加载、root transform；不得把Mesh位置反写模拟。

## 点击不到港口

检查marker的pickTarget metadata、POINTERTAP、左键及相机拖动冲突。HTML名称按钮提供同一稳定PortId入口；检查投影可见性与遮挡。港口坐标是停泊水面点，marker偏向岛岸。

## 船首方向错误

检查Babylon右手+Z forward与atan2(dx,dz)，停泊采用0。不要重新缩放或改Blender规范。
