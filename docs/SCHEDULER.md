# 定时任务配置

_自动化技能执行_

---

## 推荐配置

### 每日任务

**夜间循环** - 凌晨 2:00
```bash
0 2 * * * python3 skills/self-evolution/main.py nightly
```
作用：回顾当天记忆、整合知识、清理过期数据

### 每周任务

**RAG 评估** - 周日上午 9:00
```bash
0 9 * * 0 python3 skills/rag/main.py evaluate --days 7 --report
```
作用：生成 RAG 性能评估报告

**分形思考** - 周日上午 10:00
```bash
0 10 * * 0 python3 skills/self-evolution/main.py fractal --limit 50
```
作用：深度分析记忆，生成认知模式

---

## OpenClaw Cron 配置

```json
{
  "jobs": [
    {
      "name": "nightly-cycle",
      "schedule": {
        "kind": "cron",
        "expr": "0 2 * * *",
        "tz": "Asia/Shanghai"
      },
      "payload": {
        "kind": "agentTurn",
        "message": "执行夜间循环",
        "timeoutSeconds": 300
      },
      "sessionTarget": "isolated",
      "enabled": true
    }
  ]
}
```

导入：`openclaw cron add --file cron_config.json`

---

_版本：1.0.0 | 2026-04-01_
