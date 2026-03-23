# 夜间进化循环系统

## 🌙 系统概述

基于 TinkerClaw 的夜间进化循环设计，实现 4 个核心任务：

| 任务 | 功能 | 参考 |
|------|------|------|
| 🍷 Wind Down | 每日复盘，生成洞察和建议 | TinkerClaw |
| 😴 Memory Consolidation | 记忆整合，49% 压缩率 | ENGRAM 论文 |
| 🧹 Cleaning Lady | 上下文清理，释放空间 | TinkerClaw |
| 🔍 Auto-Evolution | 扫描改进机会 | TinkerClaw |

## 📁 文件位置

- **核心代码**: `nightly_cycle.py`
- **记忆流**: `memory_stream.py`
- **数据库**: `<workspace-root>/data/demo-agent/memory/memory_stream.db`

## 🚀 使用方法

### 手动运行

```bash
cd <workspace-root>/skills/self-evolution
python3 nightly_cycle.py
```

### 定时运行 (Cron)

建议每天凌晨 2 点运行：

```bash
# 编辑 crontab
crontab -e

# 添加任务（每天 02:00）
0 2 * * * cd <workspace-root>/skills/self-evolution && python3 nightly_cycle.py >> /tmp/nightly_cycle.log 2>&1
```

### OpenClaw Cron (推荐)

使用 OpenClaw 的 cron 系统：

```python
# 在 OpenClaw 中配置
openclaw cron add --schedule "0 2 * * *" --command "python3 nightly_cycle.py"
```

## 📊 输出示例

```
======================================================================
🌙 夜间进化循环
   开始时间：2026-03-17 10:41:47
======================================================================

======================================================================
🍷 Wind Down - 每日复盘
======================================================================
   今日事件：50 个
   ✅ 生成复盘：3 个洞察，1 个建议

======================================================================
😴 Memory Consolidation - 记忆整合
======================================================================
   压缩率：0.0% (目标：49%)

======================================================================
🧹 Cleaning Lady - 上下文清理
======================================================================
   清理文件：3 个
   释放空间：0.18MB

======================================================================
🔍 Auto-Evolution - 自动进化
======================================================================
   发现 0 个改进机会

======================================================================
📊 夜间循环总结
======================================================================
   🍷 Wind Down: ✅ (50 个事件)
   😴 Memory Consolidation: ✅ (压缩率 0.0%)
   🧹 Cleaning Lady: ✅ (清理 3 个文件)
   🔍 Auto-Evolution: ✅ (0 个改进机会)

======================================================================
✅ 夜间循环完成：2026-03-17 10:42:00
======================================================================
```

## 🔧 配置选项

在 `nightly_cycle.py` 中修改配置：

```python
self.config = {
    'memory_consolidation': {
        'compress_after_days': 7,      # 7 天后的记忆压缩
        'keep_high_importance': 7.0,   # 保留重要性 >= 7 的记忆
        'target_compression_rate': 0.49  # 49% 压缩率
    },
    'cleaning': {
        'max_learning_files': 30,      # 保留最近 30 天的学习文件
        'max_log_size_mb': 100,        # 日志文件最大 100MB
        'clean_temp_files': True       # 清理临时文件
    }
}
```

## 📈 效果指标

### Wind Down
- 每日事件回顾
- 洞察生成数量
- 建议生成数量

### Memory Consolidation
- 压缩率（目标 49%）
- 保留记忆数量
- 生成摘要数量

### Cleaning Lady
- 清理文件数量
- 释放空间大小

### Auto-Evolution
- 发现改进机会数量
- 高优先级问题数量

## 🔗 相关论文和项目

1. **Generative Agents** - 记忆流架构
   - https://github.com/joonspk-research/generative_agents
   - 论文：https://arxiv.org/abs/2304.03442

2. **TinkerClaw** - 夜间循环设计
   - https://github.com/globalcaos/tinkerclaw

3. **ENGRAM 论文** - 记忆压缩
   - 目标：49% 压缩率

## 🎯 下一步优化

1. **增强 Memory Consolidation**
   - 添加语义相似度分析
   - 更智能的聚类算法

2. **改进 Auto-Evolution**
   - 集成 GitHub 扫描
   - 自动搜索 AI 新工具

3. **添加晨间简报**
   - 整合日历/邮件/任务
   - 生成每日行动计划
