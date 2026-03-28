# Uninstall Guide | 卸载指南

[English](#english) | [中文](#中文)

---

## English {#english}

### 🗑️ Uninstall Options

You have two uninstall options:

1. **Uninstall a sub-agent** - Remove one sub-agent, keep workspace
2. **Uninstall entire workspace** - Remove everything
3. **Self-check before uninstall** - Verify workspace health

---

### Option 0: Self-Check (Recommended Before Uninstall)

**Use case:** Check workspace health before uninstalling.

```bash
cd ~/.openclaw/workspace-my-agent
python3 scripts/core/self_check.py
```

**Auto-fix issues:**
```bash
# Preview fixes
python3 scripts/core/self_check.py --dry-run

# Apply fixes
python3 scripts/core/self_check.py --fix
```

**Why check first?**
- ✅ Ensures uninstall scripts are present
- ✅ Verifies OpenClaw registration
- ✅ Detects potential issues
- ✅ Can auto-fix common problems

---

### Option 1: Uninstall Sub-Agent

**Use case:** Remove a specific sub-agent, keep the workspace and other agents.

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/uninstall-agent.sh <agent-name>
```

**Example:**
```bash
./scripts/core/uninstall-agent.sh assistant-agent
```

**What it does:**
- ✅ Backs up agent data (optional)
- ✅ Unregisters from OpenClaw
- ✅ Deletes `agents/<agent-name>/`
- ✅ Updates `config/agents.yaml`
- ✅ Keeps workspace and other agents

**Safety:**
- ⚠️ Asks for confirmation
- ⚠️ Offers backup before delete
- ⚠️ Shows what will be deleted

---

### Option 2: Uninstall Entire Workspace

**Use case:** Remove the entire workspace and all agents.

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/uninstall-workspace.sh
```

**Or specify agent name:**
```bash
./scripts/core/uninstall-workspace.sh my-agent
```

**What it does:**
- ✅ Backs up entire workspace (optional)
- ✅ Unregisters main agent from OpenClaw
- ✅ Unregisters all sub-agents
- ✅ Deletes entire workspace directory
- ✅ Updates OpenClaw config

**Safety:**
- ⚠️ Requires typing agent name to confirm
- ⚠️ Requires typing "YES" for final confirmation
- ⚠️ Offers full backup before delete
- ⚠️ Shows what will be deleted

---

### 📋 Before Uninstalling

#### Backup Your Data

**Backup sub-agent:**
```bash
cp -r ~/.openclaw/workspace-my-agent/agents/assistant-agent \
      /tmp/backup-assistant-agent-$(date +%Y%m%d)
```

**Backup entire workspace:**
```bash
cp -r ~/.openclaw/workspace-my-agent \
      /tmp/backup-workspace-my-agent-$(date +%Y%m%d)
```

#### Check What Will Be Deleted

**List sub-agents:**
```bash
ls -la ~/.openclaw/workspace-my-agent/agents/
```

**Check workspace size:**
```bash
du -sh ~/.openclaw/workspace-my-agent/
```

---

### 🔄 After Uninstalling

#### Verify Uninstall

**Check remaining agents:**
```bash
openclaw agents list
```

**Check workspace:**
```bash
ls -la ~/.openclaw/workspace-my-agent/agents/  # Should be empty or missing uninstalled agent
```

#### Restore from Backup

**Restore sub-agent:**
```bash
cp -r /tmp/backup-assistant-agent-* \
      ~/.openclaw/workspace-my-agent/agents/assistant-agent
```

**Restore workspace:**
```bash
cp -r /tmp/backup-workspace-my-agent-* \
      ~/.openclaw/workspace-my-agent
```

---

### ❓ FAQ

#### Q: Can I undo an uninstall?

**A:** Only if you created a backup. The uninstall scripts offer backup option before deleting.

---

#### Q: What happens to memory data?

**A:** It's deleted with the agent/workspace. That's why backup is important!

---

#### Q: Do I need to manually unregister from OpenClaw?

**A:** No, the uninstall scripts automatically unregister agents from OpenClaw.

---

#### Q: Can I reinstall after uninstalling?

**A:** Yes! Just run the install script again:
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

---

## 中文 {#中文}

### 🗑️ 卸载选项

你有两个卸载选项：

1. **卸载子 Agent** - 删除一个子 Agent，保留 workspace
2. **卸载整个 workspace** - 删除所有内容

---

### 选项 1: 卸载子 Agent

**使用场景：** 删除特定子 Agent，保留 workspace 和其他 Agent。

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/uninstall-agent.sh <agent-name>
```

**示例：**
```bash
./scripts/core/uninstall-agent.sh assistant-agent
```

**做什么：**
- ✅ 备份 Agent 数据（可选）
- ✅ 从 OpenClaw 注销
- ✅ 删除 `agents/<agent-name>/`
- ✅ 更新 `config/agents.yaml`
- ✅ 保留 workspace 和其他 Agent

**安全：**
- ⚠️ 询问确认
- ⚠️ 删除前提供备份
- ⚠️ 显示将删除的内容

---

### 选项 2: 卸载整个 Workspace

**使用场景：** 删除整个 workspace 和所有 Agent。

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/uninstall-workspace.sh
```

**或指定 agent 名称：**
```bash
./scripts/core/uninstall-workspace.sh my-agent
```

**做什么：**
- ✅ 完整备份 workspace（可选）
- ✅ 从 OpenClaw 注销主 Agent
- ✅ 注销所有子 Agent
- ✅ 删除整个 workspace 目录
- ✅ 更新 OpenClaw 配置

**安全：**
- ⚠️ 需要输入 agent 名称确认
- ⚠️ 需要输入 "YES" 最终确认
- ⚠️ 删除前提供完整备份
- ⚠️ 显示将删除的内容

---

### 📋 卸载前

#### 备份数据

**备份子 Agent：**
```bash
cp -r ~/.openclaw/workspace-my-agent/agents/assistant-agent \
      /tmp/backup-assistant-agent-$(date +%Y%m%d)
```

**备份整个 workspace：**
```bash
cp -r ~/.openclaw/workspace-my-agent \
      /tmp/backup-workspace-my-agent-$(date +%Y%m%d)
```

#### 检查将删除的内容

**列出子 Agent：**
```bash
ls -la ~/.openclaw/workspace-my-agent/agents/
```

**检查 workspace 大小：**
```bash
du -sh ~/.openclaw/workspace-my-agent/
```

---

### 🔄 卸载后

#### 验证卸载

**检查剩余 Agent：**
```bash
openclaw agents list
```

**检查 workspace：**
```bash
ls -la ~/.openclaw/workspace-my-agent/agents/  # 应该为空或缺少已卸载的 Agent
```

#### 从备份恢复

**恢复子 Agent：**
```bash
cp -r /tmp/backup-assistant-agent-* \
      ~/.openclaw/workspace-my-agent/agents/assistant-agent
```

**恢复 workspace：**
```bash
cp -r /tmp/backup-workspace-my-agent-* \
      ~/.openclaw/workspace-my-agent
```

---

### ❓ 常见问题

#### Q: 卸载可以撤销吗？

**A:** 只有创建了备份才可以。卸载脚本会在删除前提供备份选项。

---

#### Q: 记忆数据会怎样？

**A:** 会随 Agent/workspace 一起删除。这就是为什么备份很重要！

---

#### Q: 需要手动从 OpenClaw 注销吗？

**A:** 不需要，卸载脚本会自动从 OpenClaw 注销 Agent。

---

#### Q: 卸载后可以重新安装吗？

**A:** 可以！只需重新运行安装脚本：
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

---

## 📋 Command Reference | 命令参考

| Command | Description |
|---------|-------------|
| `./scripts/core/uninstall-agent.sh <name>` | Uninstall sub-agent |
| `./scripts/core/uninstall-workspace.sh` | Uninstall entire workspace |
| `openclaw agents list` | List registered agents |
| `cp -r source backup` | Backup before uninstall |

---

**⚠️ Always backup before uninstalling!**  
**⚠️ 卸载前始终备份！**
