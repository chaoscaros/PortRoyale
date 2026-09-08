# 未来联机边界（未实现）

Browser Input → Command → WebSocket → Server Authoritative Simulation → Snapshot / Event → Browser Renderer / UI。

服务器控制 tick、命令校验和权威状态；客户端只发意图。重放、排序、重连、增量快照、鉴权和同步策略未来单独设计。当前不创建服务器、协议或多人功能。
