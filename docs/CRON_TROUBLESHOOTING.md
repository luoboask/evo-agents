# 定时任务配置问题排查指南

## 📋 问题现象

用户安装 evo-agents 后，发现只配置了 2 个定时任务（会话扫描、每日回顾），缺少后 3 个（夜间进化、记忆压缩、系统维护）。

---

## 🔍 可能的原因

### 1. 安装时手动跳过 ⭐ 最常见

**现象**: 前 2 个任务成功，后 3 个缺失

**原因**: 
```bash
# 安装时的提示
是否需要跳过定时任务配置？(y/N，默认 N):

# 用户可能:
# a) 输入了 'y' → 完全跳过
# b) 按 Ctrl+C → 中断安装
# c) 网络问题导致脚本执行不完整
```

**解决方案**:
```bash
# 手动补全
cd ~/.openclaw/workspace-<agent>
bash scripts/core/setup-recommended-cron.sh <agent> all
```

---

### 2. 脚本文件缺失

**检查**:
```bash
ls -la ~/.openclaw/workspace-<agent>/skills/self-evolution/nightly_cycle.py
ls -la ~/.openclaw/workspace-<agent>/scripts/core/memory_compressor.py
```

**解决方案**:
```bash
# 从 evo-agents 复制
cd /tmp
git clone https://github.com/luoboask/evo-agents.git
cp evo-agents/skills/self-evolution/nightly_cycle.py ~/.openclaw/workspace-<agent>/skills/self-evolution/
cp evo-agents/scripts/core/memory_compressor.py ~/.openclaw/workspace-<agent>/scripts/core/
```

---

### 3. OpenClaw 未安装或不可用

**检查**:
```bash
openclaw --version
```

**解决方案**:
```bash
# 安装 OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash
```

---

### 4. 权限问题（不太可能）

**检查**:
```bash
ls -l ~/.openclaw/workspace-<agent>/skills/self-evolution/nightly_cycle.py
# 应该是 -rw-r--r-- (使用 python3 调用，不需要执行权限)
```

**解决方案**:
```bash
chmod +x ~/.openclaw/workspace-<agent>/skills/self-evolution/nightly_cycle.py
```

---

## 🛠️ 诊断工具

使用诊断脚本快速排查：

```bash
cd /tmp/evo-agents
bash scripts/core/diagnose-cron.sh <agent-name>
```

**输出示例**:
```
╔════════════════════════════════════════════════════════╗
║  定时任务配置诊断                                       ║
╚════════════════════════════════════════════════════════╝

📦 Agent: claude-code-agent
📁 Workspace: /Users/dhr/.openclaw/workspace-claude-code-agent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 检查脚本文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ scripts/core/scan_sessions.py
   （已删除，功能由 unified_search 替代）
   ✅ skills/self-evolution/nightly_cycle.py
   ✅ scripts/core/memory_compressor.py
   ✅ skills/memory-search/maintenance.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. 检查脚本权限
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ⚠️  scripts/core/scan_sessions.py (无执行权限，但使用 python3 调用不影响)
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. 检查 OpenClaw cron
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ OpenClaw 已安装

📋 当前 cron 任务:
abc123... claude-code-session-scan     cron */30 * * * *
def456... claude-code-daily-review     cron 0 9 * * *
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. 测试运行脚本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ 夜间进化脚本可运行
   ✅ 记忆压缩脚本可运行

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
诊断完成！
```

---

## ✅ 解决方案汇总

### 方案 1：使用诊断脚本（推荐）

```bash
# 1. 下载诊断脚本
curl -sO https://raw.githubusercontent.com/luoboask/evo-agents/master/scripts/core/diagnose-cron.sh

# 2. 运行诊断
bash diagnose-cron.sh <agent-name>

# 3. 根据诊断结果修复
```

---

### 方案 2：手动补全任务

```bash
cd ~/.openclaw/workspace-<agent>

# 夜间进化
openclaw cron add \
    --cron "0 23 * * *" \
    --agent <agent> \
    --message "python3 skills/self-evolution/nightly_cycle.py" \
    --name "nightly-evolution-<agent>"

# 记忆压缩
openclaw cron add \
    --cron "0 3 * * 0" \
    --agent <agent> \
    --message "python3 scripts/core/memory_compressor.py --weekly --monthly" \
    --name "weekly-compress-<agent>"

# 系统维护
openclaw cron add \
    --cron "0 2 * * 0" \
    --agent <agent> \
    --message "bash skills/memory-search/maintenance.sh" \
    --name "weekly-maintenance-<agent>"
```

---

### 方案 3：使用配置脚本

```bash
cd ~/.openclaw/workspace-<agent>
bash scripts/core/setup-recommended-cron.sh <agent> all
```

---

## 📊 验证结果

```bash
# 查看完整的 5 个任务
openclaw cron list | grep <agent> | grep -E "(session-scan|daily-review|nightly-evolution|weekly-compress|weekly-maintenance)"
```

**应该看到 5 个任务**：
```
✅ session-scan-<agent>         每 30 分钟
✅ daily-review-<agent>         每天 09:00
✅ nightly-evolution-<agent>    每天 23:00
✅ weekly-compress-<agent>      每周日 03:00
✅ weekly-maintenance-<agent>   每周日 02:00
```

---

## 🎯 预防措施

### 改进 install.sh

1. **添加进度提示**
```bash
echo "配置 1/5: 会话扫描..."
echo "配置 2/5: 每日回顾..."
echo "配置 3/5: 夜间进化..."
echo "配置 4/5: 记忆压缩..."
echo "配置 5/5: 系统维护..."
```

2. **添加错误处理**
```bash
if ! openclaw cron add ...; then
    echo "⚠️  任务配置失败，但继续安装..."
fi
```

3. **添加验证步骤**
```bash
# 配置完成后验证
count=$(openclaw cron list | grep "$AGENT_NAME" | wc -l)
if [ "$count" -lt 5 ]; then
    echo "⚠️  只配置了 $count/5 个任务，建议手动补全"
fi
```

---

## 📚 相关文档

- [定时任务推荐配置](./CRON_RECOMMENDATIONS.md)
- [自动配置指南](./AUTO_CRON_SETUP.md)
- [手动配置指南](./MANUAL_CRON_SETUP.md)

---

**更新日期**: 2026-04-09  
**版本**: 1.0.0
