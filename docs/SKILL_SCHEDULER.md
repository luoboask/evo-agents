# 技能定时任务配置

_自动化技能执行配置示例_

---

## 📅 推荐配置

### 每天执行的任务

#### 1. 夜间循环（自进化系统）
**时间：** 凌晨 2:00  
**作用：** 回顾当天记忆、整合知识、清理过期数据

```bash
# crontab -e
0 2 * * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py nightly >> logs/nightly.log 2>&1
```

#### 2. 记忆备份
**时间：** 凌晨 3:00  
**作用：** 备份记忆数据库

```bash
0 3 * * * cd /Users/dhr/.openclaw/workspace && python3 scripts/backup_memory.py >> logs/backup.log 2>&1
```

---

### 每周执行的任务

#### 1. RAG 评估报告
**时间：** 周日上午 9:00  
**作用：** 生成 RAG 性能评估报告

```bash
0 9 * * 0 cd /Users/dhr/.openclaw/workspace && python3 skills/rag/main.py evaluate --days 7 --report >> logs/rag-eval.log 2>&1
```

#### 2. 分形思考
**时间：** 周日上午 10:00  
**作用：** 深度分析本周记忆，生成认知模式

```bash
0 10 * * 0 cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py fractal --limit 50 >> logs/fractal.log 2>&1
```

#### 3. 记忆整理
**时间：** 周日下午 5:00  
**作用：** 清理低质量记忆，合并重复内容

```bash
0 17 * * 0 cd /Users/dhr/.openclaw/workspace && python3 skills/memory-search/cleanup.py >> logs/cleanup.log 2>&1
```

---

### 每月执行的任务

#### 1. 系统健康检查
**时间：** 每月 1 日上午 9:00  
**作用：** 检查记忆系统、RAG、自进化系统状态

```bash
0 9 1 * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py status >> logs/monthly-status.log 2>&1
```

#### 2. 知识库审查
**时间：** 每月 1 日下午 3:00  
**作用：** 审查知识库条目，删除过时内容

```bash
0 15 1 * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py review_knowledge >> logs/knowledge-review.log 2>&1
```

---

## 🔧 OpenClaw Cron 配置

如果使用 OpenClaw 的内置 cron 系统，可以这样配置：

### 示例：每日夜间循环

```json
{
  "name": "nightly-cycle",
  "schedule": {
    "kind": "cron",
    "expr": "0 2 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "执行夜间循环：回顾今天的所有记忆，整合知识到知识库，生成反思总结。",
    "timeoutSeconds": 300
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### 示例：每周 RAG 评估

```json
{
  "name": "weekly-rag-eval",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 0",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "执行 RAG 评估：分析过去 7 天的检索性能，生成 HTML 报告，推荐最优配置。",
    "timeoutSeconds": 600
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce"
  },
  "enabled": true
}
```

---

## 📊 完整 crontab 示例

```bash
# === 每日任务 ===
# 夜间循环（凌晨 2 点）
0 2 * * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py nightly

# 记忆备份（凌晨 3 点）
0 3 * * * cd /Users/dhr/.openclaw/workspace && python3 scripts/backup_memory.py

# === 每周任务 ===
# RAG 评估（周日上午 9 点）
0 9 * * 0 cd /Users/dhr/.openclaw/workspace && python3 skills/rag/main.py evaluate --days 7 --report

# 分形思考（周日上午 10 点）
0 10 * * 0 cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py fractal --limit 50

# 记忆整理（周日下午 5 点）
0 17 * * 0 cd /Users/dhr/.openclaw/workspace && python3 skills/memory-search/cleanup.py

# === 每月任务 ===
# 系统健康检查（每月 1 日上午 9 点）
0 9 1 * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py status

# 知识库审查（每月 1 日下午 3 点）
0 15 1 * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py review_knowledge
```

---

## 🎯 最小化配置（推荐新手）

如果只想配置最核心的任务：

```bash
# 仅夜间循环（每天凌晨 2 点）
0 2 * * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/main.py nightly
```

这一个任务就够了！其他可以后续添加。

---

## 📝 验证配置

### 检查 crontab
```bash
crontab -l
```

### 查看日志
```bash
# 夜间循环日志
tail -f /Users/dhr/.openclaw/workspace/logs/nightly.log

# RAG 评估日志
tail -f /Users/dhr/.openclaw/workspace/logs/rag-eval.log
```

### 手动测试
```bash
# 测试夜间循环
python3 skills/self-evolution/main.py nightly

# 测试 RAG 评估
python3 skills/rag/main.py evaluate --days 7 --report
```

---

## ⚠️ 注意事项

1. **时区**：所有时间都是 Asia/Shanghai (GMT+8)
2. **日志**：建议所有任务都输出日志，便于排查问题
3. **超时**：长时间任务设置合理的 timeout
4. **并发**：避免多个任务同时执行（错开时间）
5. **权限**：确保 cron 有执行 Python 脚本的权限

---

## 🔍 故障排查

### 任务没有执行
```bash
# 检查 cron 服务
sudo systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog | tail -20
```

### 脚本执行失败
```bash
# 手动执行脚本
cd /Users/dhr/.openclaw/workspace
python3 skills/self-evolution/main.py nightly

# 检查 Python 路径
which python3
```

### 权限问题
```bash
# 确保脚本可执行
chmod +x skills/self-evolution/main.py

# 检查文件权限
ls -la skills/self-evolution/main.py
```

---

_版本：1.0.0 | 创建：2026-04-01_
