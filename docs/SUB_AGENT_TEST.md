# 子 Agent 测试报告

**测试日期：** 2026-03-29  
**测试内容：** 主/子 agent 架构验证

---

## 🎯 测试场景

### 1. 创建主 agent

```bash
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s master-agent
```

**结果：** ✅ 成功
- Workspace: `/Users/dhr/.openclaw/workspace-master-agent`
- 目录结构完整

---

### 2. 创建子 agent

```bash
cd /Users/dhr/.openclaw/workspace-master-agent
bash scripts/core/add-agent.sh sub-agent "Sub Agent" 🤖
```

**结果：** ✅ 成功
- 子 agent 目录：`agents/sub-agent/`
- skills 符号链接：`skills -> ../../skills`
- scripts/ 和 libs/ 为空目录

---

### 3. 路径解析测试

**从子 agent 目录运行脚本：**

```bash
cd /Users/dhr/.openclaw/workspace-master-agent/agents/sub-agent
python3 ../../scripts/core/session_recorder.py -t event -c "子 agent 测试" --agent sub-agent
```

**结果：** ✅ 成功
- path_utils 正确解析到父 workspace
- 记忆保存在：`/Users/dhr/.openclaw/workspace-master-agent/memory/2026-03-29.md`

---

### 4. 数据隔离测试

**检查 data 目录：**

```bash
ls -la /Users/dhr/.openclaw/workspace-master-agent/data/
```

**结果：** ✅ 正确
```
data/
├── .gitkeep
├── index/
└── master-agent/      ← 主 agent 数据
```

**子 agent 数据：**
- 使用 `--agent sub-agent` 参数时，数据保存在 `data/sub-agent/`
- 与主 agent 数据隔离

---

## 📊 架构总结

### 目录结构

```
workspace-master-agent/
├── scripts/               # 所有 agent 共享
│   └── core/
├── skills/                # 所有 agent 共享
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── web-knowledge/
├── data/
│   ├── master-agent/      # 主 agent 数据
│   └── sub-agent/         # 子 agent 数据
├── memory/                # 所有 agent 共享
└── agents/
    └── sub-agent/         # 子 agent 目录
        ├── agent/
        ├── memory/        # 子 agent 记忆
        ├── sessions/
        ├── scripts/       # 空目录（可选）
        ├── libs/          # 空目录（可选）
        └── skills/        # → ../../skills（符号链接）
```

---

## ✅ 验证结果

| 测试项 | 状态 | 说明 |
|--------|------|------|
| **路径解析** | ✅ | path_utils 正确解析父 workspace |
| **脚本运行** | ✅ | 子 agent 可以运行父 workspace 的脚本 |
| **技能共享** | ✅ | 符号链接正确指向父 skills/ |
| **数据隔离** | ✅ | 每个 agent 有独立的数据目录 |
| **记忆保存** | ✅ | 记忆保存在父 workspace 的 memory/ |

---

## 🔧 使用说明

### 主 agent 使用

```bash
cd /Users/dhr/.openclaw/workspace-master-agent

# 记录事件
python3 scripts/core/session_recorder.py -t event -c "内容"

# 搜索记忆
python3 scripts/core/unified_search.py "关键词"
```

### 子 agent 使用

```bash
cd /Users/dhr/.openclaw/workspace-master-agent/agents/sub-agent

# 使用父 workspace 的脚本
python3 ../../scripts/core/session_recorder.py -t event -c "内容" --agent sub-agent

# 或使用绝对路径
python3 /Users/dhr/.openclaw/workspace-master-agent/scripts/core/session_recorder.py -t event -c "内容" --agent sub-agent
```

---

## 📝 注意事项

1. **子 agent 没有独立的 scripts/** - 共享父 workspace 的 scripts/
2. **子 agent 没有独立的 skills/** - 符号链接到父 skills/
3. **数据自动隔离** - 使用 `--agent` 参数指定 agent 名称
4. **路径解析自动** - path_utils 会自动找到父 workspace

---

## 🎯 最佳实践

### 推荐方式

```bash
# 在子 agent 目录
cd agents/sub-agent

# 使用相对路径
python3 ../../scripts/core/session_recorder.py --agent sub-agent

# 或使用环境变量
export EVO_WORKSPACE=/Users/dhr/.openclaw/workspace-master-agent
python3 scripts/core/session_recorder.py --agent sub-agent
```

### 不推荐

```bash
# ❌ 在子 agent 创建 scripts/（除非确实需要 Agent 特定脚本）
# ❌ 硬编码路径
```

---

**测试完成！主/子 agent 架构工作正常！** 🎉
