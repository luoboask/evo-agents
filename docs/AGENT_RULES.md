# 📋 Agent Rules | Agent 规则

**Read this before working in this workspace!**  
**在这个 workspace 工作前请阅读！**

---

## 🚫 Never Do This | 永远不要这样做

```bash
# ❌ Don't clone in workspace root | 不要在 workspace 根目录克隆
cd ~/.openclaw/workspace-my-agent/
git clone https://github.com/xxx/project.git

# ❌ Don't create projects in root | 不要在根目录创建项目
mkdir my-project
npm init

# ❌ Don't create scripts in root | 不要在根目录创建脚本
cat > script.sh
```

---

## ✅ Always Do This | 永远这样做

```bash
# ✅ Use external directories for projects | 使用外部目录进行项目
cd ~/projects/
git clone https://github.com/xxx/project.git

# ✅ Use scripts/ for scripts | 在 scripts/ 创建脚本
cd scripts/
cat > my-script.sh

# ✅ Use data/<agent>/work/ for agent work | 在 data/<agent>/work/ 进行 Agent 工作
cd data/my-agent/work/
# Work here | 在这里工作

# ✅ Clean up after work | 工作后清理
rm -rf /tmp/temp-*
rm -rf data/my-agent/work/temp-*
```

---

## 📁 Directory Usage | 目录使用

| Directory | Use | Don't Use |
|-----------|-----|-----------|
| `scripts/` | ✅ Scripts only | ❌ Other files |
| `skills/` | ✅ Skills only | ❌ Other files |
| `data/<agent>/work/` | ✅ Temporary work | ❌ Permanent files |
| Root `/` | ❌ Nothing | ❌ Everything |

**External | 外部：**
- `~/projects/` - Your projects | 你的项目 ✅
- `/tmp/` - Temporary work | 临时工作 ✅

---

## 🧹 Cleanup | 清理

After completing tasks:
- ✅ Remove temporary files | 删除临时文件
- ✅ Remove build artifacts | 删除构建产物
- ✅ Clean `data/<agent>/work/` | 清理工作目录

---

**Full instructions: docs/AGENT_INSTRUCTIONS.md**  
**完整指令：docs/AGENT_INSTRUCTIONS.md**
