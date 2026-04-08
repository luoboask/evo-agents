# 定时任务配置指南

## 📋 说明

由于 Git 合并冲突，`install.sh` 已恢复到正常版本，但**定时任务需要手动配置**。

---

## 🔧 配置方法

### 方法 1：一键配置（推荐）

```bash
cd ~/.openclaw/workspace-<your-agent>
bash scripts/core/setup-recommended-cron.sh <agent-name> all
```

**示例**：
```bash
# main-agent
cd ~/.openclaw/workspace
bash scripts/core/setup-recommended-cron.sh main all

# claude-code-agent
cd ~/.openclaw/workspace-claude-code-agent
bash scripts/core/setup-recommended-cron.sh claude-code-agent all
```

---

### 方法 2：交互式配置

```bash
cd ~/.openclaw/workspace-<your-agent>
bash scripts/core/setup-recommended-cron.sh <agent-name>
```

会根据提示选择要配置的任务。

---

### 方法 3：单独配置每个任务

```bash
# 1. 会话扫描（每 30 分钟）
bash scripts/core/setup-cron.sh <agent-name> 30

# 2. 每日回顾（每天 09:00）
bash scripts/core/setup-daily-review.sh <agent-name> "09:00"

# 3. 夜间进化（每天 23:00）
CRON_CMD="0 23 * * * cd <workspace> && python3 skills/self-evolution/nightly_cycle.py >> logs/nightly_evolution.log 2>&1"
(crontab -l 2>/dev/null | grep -v "nightly_cycle"; echo "$CRON_CMD") | crontab -

# 4. 记忆压缩（每周日 03:00）
CRON_CMD="0 3 * * 0 cd <workspace> && python3 scripts/core/memory_compressor.py --weekly --monthly >> logs/memory_compress.log 2>&1"
(crontab -l 2>/dev/null | grep -v "memory_compressor"; echo "$CRON_CMD") | crontab -

# 5. 系统维护（每周日 02:00）
CRON_CMD="0 2 * * 0 cd <workspace> && bash skills/memory-search/maintenance.sh >> logs/system_maintenance.log 2>&1"
(crontab -l 2>/dev/null | grep -v "maintenance"; echo "$CRON_CMD") | crontab -
```

---

## ✅ 验证配置

```bash
# 查看 cron 任务
crontab -l

# 应该看到类似：
# */30 * * * * cd /Users/dhr/.openclaw/workspace && python3 scripts/core/scan_sessions.py --agent main >> logs/session_scan.log 2>&1
# 0 9 * * * cd /Users/dhr/.openclaw/workspace && python3 skills/memory-search/daily_review.py >> logs/daily_review.log 2>&1
# 0 23 * * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/nightly_cycle.py >> logs/nightly_evolution.log 2>&1
# 0 3 * * 0 cd /Users/dhr/.openclaw/workspace && python3 scripts/core/memory_compressor.py --weekly --monthly >> logs/memory_compress.log 2>&1
# 0 2 * * 0 cd /Users/dhr/.openclaw/workspace && bash skills/memory-search/maintenance.sh >> logs/system_maintenance.log 2>&1
```

---

## 📊 配置的任务

| 任务 | 频率 | 说明 |
|------|------|------|
| **会话扫描** | 每 30 分钟 | 自动同步 OpenClaw 会话到记忆系统 |
| **每日回顾** | 每天 09:00 | 创建今日记忆 + 显示昨天摘要 |
| **夜间进化** | 每天 23:00 | 记忆整合 + 自进化 + 上下文清理 |
| **记忆压缩** | 每周日 03:00 | 生成周摘要 + 月摘要 |
| **系统维护** | 每周日 02:00 | 清理旧记忆 + 压缩缓存 |

---

## 📚 相关文档

- [定时任务推荐配置](./CRON_RECOMMENDATIONS.md)
- [会话扫描使用指南](./SESSION_SCAN_CRON.md)
- [每日回顾集成](./DAILY_REVIEW_INTEGRATION.md)

---

**配置完成！** 🎉
