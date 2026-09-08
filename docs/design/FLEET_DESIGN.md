# 当前舰队 MVP · Phase 1

当前 1 Fleet（fleet-player-001）初始停泊哈瓦那，只有一个已有 GLB 船视觉。速度固定可配置，默认 8 世界单位/模拟秒。没有货物、船员、战斗或 ShipState[]。

选择船（或辅助“选择测试舰队”按钮）→ 点击港口标记/名称 → 确认“前往” → 直线航行 → 到港停泊。选中显示圈，航行时显示到目的港的线。HUD 显示状态、当前港/海上、目的港、速度、剩余距离、派生 ETA 和调试坐标。

航行开始 currentPortId=null；到港 position 精确等于港口位置，status=docked，currentPortId=目标，destination=null。航行中可改道，从实时当前位置转向，不瞬移；同目标重复命令 no-op。暂停停止模拟位移，倍率作用于 Clock；暂停中可发命令，恢复后才移动。

船首由目标方向 atan2(dx,dz) 派生；停泊使用稳定默认 +Z。最近港间约 10 模拟秒，哈瓦那到圣胡安约 26.3 秒，最远约 27 秒，便于测试，非最终平衡。

已知限制：只有直线，尚无海上航路/岛屿避障，也无船间碰撞、海浪物理或转弯半径。视图每 tick 更新位置，暂不加渲染插值。

未来：Multi-ship fleet、Cargo、Crew、Route、Trade、Combat，按阶段增加。长期 Fleet=1..N Ships，不在本轮提前实现。
