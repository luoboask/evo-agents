# Agent Migration Guide | Agent 迁移指南

[English](#english) | [中文](#中文)

---

## English {#english}

### 🚨 Important: Read Before Installing

**Already have a workspace for this agent?**

If you've previously installed evo-agents (or test-agents) for this agent, this guide explains what will happen.

---

### 🔄 What Happens During Re-installation

When you run the install script and a workspace already exists:

**✅ Preserved (Won't be deleted):**
- Personal configs: `USER.md`, `SOUL.md`, `IDENTITY.md`, etc.
- Memory data: `memory/` directory
- Knowledge base: `public/` directory
- **Your skills**: `skills/` directory (all your custom skills)
- **Your scripts**: `scripts/` root directory (not in `core/`)
- Your data and configurations

**📦 Updated (Template files):**
- Universal skills: `skills/core/` (memory-search, rag, self-evolution, web-knowledge)
- System scripts: `scripts/core/` directory
- Documentation: `README.md`, etc.

**⚠️ Important:**
- Your custom skills in `skills/` are **safe**
- Your custom scripts in `scripts/` are **safe**
- Only `skills/core/` and `scripts/core/` are updated

---

### 📋 Installation Options

#### Option 1: Fresh Install (New Agent)

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

No confirmation needed - creates new workspace.

#### Option 2: Re-install (Existing Agent)

**Recommended: Interactive mode**
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s existing-agent
```
- Will ask for confirmation (y/n)
- Shows what will be preserved/updated
- Safe - won't delete your data

**Force mode (skip confirmation)**
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s existing-agent --force
```
- Skips confirmation
- Use for automation

---

### 💡 Best Practices

1. **Backup important changes**
   ```bash
   cp -r ~/.openclaw/workspace-xxx /tmp/backup-$(date +%Y%m%d)
   ```

2. **Check what will be updated**
   - Install script shows preservation/update list
   - Review before confirming

3. **Place custom scripts correctly**
   - `scripts/` root → Your scripts (safe)
   - `scripts/core/` → System scripts (updated)

4. **Place custom skills correctly**
   - `skills/` root → Your skills (safe)
   - `skills/core/` → Universal skills (updated)

---

### 📞 Need Help?

- Check install script output - it shows what's preserved
- Review `README.md` for directory structure
- Ask in GitHub Issues if unsure

---

## 中文 {#中文}

### 🚨 重要：安装前请阅读

**已经为这个 Agent 安装过 workspace？**

如果你之前为这个 Agent 安装过 evo-agents（或 test-agents），本指南说明会发生什么。

---

### 🔄 重新安装时会发生什么

当你运行安装脚本且 workspace 已存在时：

**✅ 保留（不会删除）：**
- 个人配置：`USER.md`, `SOUL.md`, `IDENTITY.md` 等
- 记忆数据：`memory/` 目录
- 知识库：`public/` 目录
- **你的技能**：`skills/` 目录（所有自定义技能）
- **你的脚本**：`scripts/` 根目录（不在 `core/` 中）
- 你的数据和配置

**📦 更新（模板文件）：**
- 通用技能：`skills/core/`（memory-search, rag, self-evolution, web-knowledge）
- 系统脚本：`scripts/core/` 目录
- 文档：`README.md` 等

**⚠️ 重要：**
- 你的自定义技能在 `skills/` 是**安全**的
- 你的自定义脚本在 `scripts/` 是**安全**的
- 只有 `skills/core/` 和 `scripts/core/` 会被更新

---

### 📋 安装选项

#### 选项 1: 新安装（新 Agent）

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

无需确认 - 创建新 workspace。

#### 选项 2: 重新安装（现有 Agent）

**推荐：交互模式**
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s existing-agent
```
- 会询问确认（y/n）
- 显示保留/更新的内容
- 安全 - 不会删除你的数据

**强制模式（跳过确认）**
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s existing-agent --force
```
- 跳过确认
- 用于自动化

---

### 💡 最佳实践

1. **备份重要修改**
   ```bash
   cp -r ~/.openclaw/workspace-xxx /tmp/backup-$(date +%Y%m%d)
   ```

2. **检查会被更新的内容**
   - 安装脚本会显示保留/更新列表
   - 确认前查看

3. **正确放置自定义脚本**
   - `scripts/` 根目录 → 你的脚本（安全）
   - `scripts/core/` → 系统脚本（更新）

4. **正确放置自定义技能**
   - `skills/` 根目录 → 你的技能（安全）
   - `skills/core/` → 通用技能（更新）

---

### 📞 需要帮助？

- 查看安装脚本输出 - 显示保留内容
- 查看 `README.md` 了解目录结构
- 不确定就在 GitHub Issues 中提问

---

**记住：重新安装是安全的，不会删除你的个人数据！**
