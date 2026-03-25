# HEARTBEAT.md - 定期任务

## 每次 Heartbeat

```bash
# 增量索引（快速，几秒钟）
python3 scripts/memory_indexer.py --incremental
```

## 每周一

```bash
# 生成上周摘要
python3 scripts/memory_compressor.py --weekly
```

## 每月 1 号

```bash
# 生成上月摘要 + 归档旧 daily 文件
python3 scripts/memory_compressor.py --monthly --archive
```

## 日常检查

```bash
# 查看记忆状态
python3 scripts/memory_stats.py
```

## 规则

- 没事不做多余的事
- 深夜 (23:00-08:00) 保持安静
- 有重要发现才打扰用户
