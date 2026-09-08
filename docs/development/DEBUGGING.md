# 调试

黑屏：检查 WebGL 支持、控制台 shader/资源错误，确认 npm dev 的实际端口。页面有启动失败提示，GLB 错误会显示在 HUD。

船只方向/尺寸错误：先检查 BLENDER_PIPELINE 的三个校验节点和 Blender scale，不在 Renderer 随意缩放。素材缺失：确认 public/assets/models/ship_test.glb 存在；可用 Blender 脚本重建。

时间问题：先跑 Clock 测试，再检查宿主 visibility 和 250ms 截断。暂停时 TPS 应最终变 0，显示有一秒采样延迟；倍率控制不自动解除暂停。不要用 FPS 作为速度乘数。

端口占用：默认 9999 自动顺延，以 Vite 输出为准，不结束其他项目进程。
