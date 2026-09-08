# 未来存档格式（未实现）

正式存档必须有 saveVersion。仅序列化 Simulation State（包含时间、实体 ID、经济、航行和必要随机种子）。禁止 Mesh、Material、DOM、相机运行对象。加载先验证版本和数据，迁移失败不能覆盖原存档。

未来单机优先评估 IndexedDB；小型设置可用 localStorage。本轮不写入任何完整存档。
