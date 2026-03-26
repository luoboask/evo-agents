# HEARTBEAT.md - 定期任务

## 每次 Heartbeat

```bash
# 双向同步记忆（markdown ↔ 知识系统）
python3 scripts/bridge/bridge_sync.py --agent demo-agent
```

## 每周一

```bash
# 可选：运行记忆压缩（如果文件太多）
# python3 scripts/memory_compressor.py --weekly
```

## 规则

- 没事不做多余的事
- 深夜 (23:00-08:00) 保持安静
- 有重要发现才打扰用户
