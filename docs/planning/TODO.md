# 待办

## Phase 0
- [x] React / TypeScript / Vite / Babylon / Vitest 工程。
- [x] Command、固定步长 Clock、不可变 Snapshot、暂停与倍率。
- [x] 海面、天空、岛屿、港口标记、自制 GLB 船和策略相机。
- [x] Blender 源文件、导出脚本、方向尺度校验和资产登记。
- [x] 长期规划与当前接力文档体系。
- [x] typecheck（包括无 DOM 核心编译）、10 项 test、build 通过并回填交接。
- [ ] 等用户启动服务，在指定 Chrome 页面补完 4× 稳定 TPS、相机平移/旋转/缩放和极限验收。

## 下一阶段候选（未授权实施）
- 先做 4 个港口定义与海域数据。
- Fleet 的纯模拟位置、Move Command、按模拟时间移动和抵达。
- Picking 仅产生 ID，UI/input 转成命令，Renderer 按快照映射 FleetId。
- 验证暂停、倍率、低帧率及不同 frame 分割下航行一致。
- 暂不引入贸易、市场、国家 AI 或自动贸易。
