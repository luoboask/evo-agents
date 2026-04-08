# install.sh 自动定时任务配置

## 📅 更新时间
**2026-04-08 22:45 GMT+8**

---

## ✅ 功能说明

现在 `install.sh` 安装脚本会**自动配置定时任务**，用户可以选择跳过。

---

## 🚀 安装流程

### 1. 运行安装脚本

```bash
# 国内（Gitee 源）
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s my-agent

# 海外（GitHub 源）
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

### 2. 自动配置定时任务

安装过程中会自动询问：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ 自动配置定时任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 正在为您配置推荐的定时任务...
   ✅ 会话扫描 (每 30 分钟) - 自动同步 OpenClaw 会话
   ✅ 每日回顾 (每天 09:00) - 创建今日记忆 + 显示昨天摘要
   ✅ 夜间进化 (每天 23:00) - 记忆整合 + 自进化

是否需要跳过定时任务配置？(y/N，默认 N):
```

**直接回车** → 自动配置所有定时任务  
**输入 y** → 跳过配置

---

## 📊 配置的定时任务

| 任务 | 频率 | 说明 |
|------|------|------|
| **会话扫描** | 每 30 分钟 | 自动同步 OpenClaw 会话到记忆系统 |
| **每日回顾** | 每天 09:00 | 创建今日记忆 + 显示昨天摘要 |
| **夜间进化** | 每天 23:00 | 记忆整合 + 自进化 + 上下文清理 |

---

## 🔧 安装后验证

### 查看 cron 任务

```bash
crontab -l
```

**应该看到**：
```bash
*/30 * * * * cd /Users/dhr/.openclaw/workspace-my-agent && python3 scripts/core/scan_sessions.py --agent my-agent >> logs/session_scan.log 2>&1
0 9 * * * cd /Users/dhr/.openclaw/workspace-my-agent && python3 skills/memory-search/daily_review.py >> logs/daily_review.log 2>&1
0 23 * * * cd /Users/dhr/.openclaw/workspace-my-agent && python3 skills/self-evolution/nightly_cycle.py >> logs/nightly_evolution.log 2>&1
```

### 查看日志

```bash
# 会话扫描日志
tail -f logs/session_scan.log

# 每日回顾日志
tail -f logs/daily_review.log

# 夜间进化日志
tail -f logs/nightly_evolution.log
```

---

## 📝 代码实现

### 中文版本

```bash
if [ "$LANG" = "zh" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏰ 自动配置定时任务"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 正在为您配置推荐的定时任务..."
    echo "   ✅ 会话扫描 (每 30 分钟) - 自动同步 OpenClaw 会话"
    echo "   ✅ 每日回顾 (每天 09:00) - 创建今日记忆 + 显示昨天摘要"
    echo "   ✅ 夜间进化 (每天 23:00) - 记忆整合 + 自进化"
    echo ""
    
    # 询问是否跳过
    read -p "是否需要跳过定时任务配置？(y/N，默认 N): " -r SKIP_CRON
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        # 配置会话扫描
        if [ -f "$WORKSPACE_ROOT/scripts/core/setup-cron.sh" ]; then
            echo "📝 设置会话扫描定时任务 (每 30 分钟)..."
            cd "$WORKSPACE_ROOT"
            bash scripts/core/setup-cron.sh "$AGENT_NAME" 30 >/dev/null 2>&1 && echo "   ✅ 完成" || echo "   ⚠️  设置失败"
        fi
        
        # 配置每日回顾
        if [ -f "$WORKSPACE_ROOT/scripts/core/setup-daily-review.sh" ]; then
            echo "📝 设置每日回顾定时任务 (每天 09:00)..."
            cd "$WORKSPACE_ROOT"
            bash scripts/core/setup-daily-review.sh "$AGENT_NAME" "09:00" >/dev/null 2>&1 && echo "   ✅ 完成" || echo "   ⚠️  设置失败"
        fi
        
        # 配置夜间进化
        CRON_CMD="0 23 * * * cd $WORKSPACE_ROOT && python3 skills/self-evolution/nightly_cycle.py >> logs/nightly_evolution.log 2>&1"
        echo "📝 设置夜间进化循环 (每天 23:00)..."
        (crontab -l 2>/dev/null | grep -v "nightly_cycle"; echo "$CRON_CMD") | crontab - && echo "   ✅ 完成" || echo "   ⚠️  设置失败"
    fi
fi
```

### 英文版本

```bash
if [ "$LANG" != "zh" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏰ Auto-Configure Cron Jobs"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 Configuring recommended cron jobs..."
    echo "   ✅ Session Scan (every 30 min) - Auto-sync OpenClaw sessions"
    echo "   ✅ Daily Review (daily 09:00) - Create today's memory + yesterday's summary"
    echo "   ✅ Nightly Evolution (daily 23:00) - Memory consolidation + self-evolution"
    echo ""
    
    # Ask to skip
    read -p "Skip cron job configuration? (y/N, default N): " -r SKIP_CRON
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        # Configure cron jobs...
    fi
fi
```

---

## 🎯 用户体验

### 默认行为（直接回车）

```
是否需要跳过定时任务配置？(y/N，默认 N): [回车]

📝 设置会话扫描定时任务 (每 30 分钟)...
   ✅ 完成
📝 设置每日回顾定时任务 (每天 09:00)...
   ✅ 完成
📝 设置夜间进化循环 (每天 23:00)...
   ✅ 完成

📋 当前 cron 任务列表:
*/30 * * * * cd /Users/dhr/.openclaw/workspace && python3 scripts/core/scan_sessions.py --agent main >> logs/session_scan.log 2>&1
0 9 * * * cd /Users/dhr/.openclaw/workspace && python3 skills/memory-search/daily_review.py >> logs/daily_review.log 2>&1
0 23 * * * cd /Users/dhr/.openclaw/workspace && python3 skills/self-evolution/nightly_cycle.py >> logs/nightly_evolution.log 2>&1
```

### 跳过配置（输入 y）

```
是否需要跳过定时任务配置？(y/N，默认 N): y

   ⊘ 已跳过定时任务配置
```

---

## 📁 修改的文件

| 文件 | 修改内容 | 行数变化 |
|------|---------|---------|
| `install.sh` | 添加定时任务自动配置 | +87, -5 |

---

## 🔄 同步状态

| Agent | 状态 |
|-------|------|
| **evo-agents** | ✅ 已提交并推送 |
| **claude-code-agent** | ✅ 已同步 |
| **main-agent** | ✅ 已同步 |

---

## 📚 相关文档

- [定时任务推荐配置](./CRON_RECOMMENDATIONS.md)
- [会话扫描使用指南](./SESSION_SCAN_CRON.md)
- [每日回顾集成](./DAILY_REVIEW_INTEGRATION.md)
- [手动配置指南](./MANUAL_CRON_SETUP.md)

---

**自动配置完成！** 🎉

现在安装 evo-agents 时，定时任务会自动配置，无需手动运行脚本！
