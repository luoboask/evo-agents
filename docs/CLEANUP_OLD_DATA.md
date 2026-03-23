# 清理旧数据目录

**创建时间：** 2026-03-23 19:30

---

## 📊 当前状态

### 旧数据目录（已废弃）

```
~/.openclaw/workspace-ai-baby-config/
├── config.yaml              ⚠️ 旧配置文件
├── credentials.json         ⚠️ API 凭证
├── memory/
│   ├── ai-baby_knowledge_base.db   ⚠️ 已迁移
│   └── ai-baby_memory_stream.db    ⚠️ 已迁移
└── logs/
    └── evaluations.jsonl           ⚠️ 已迁移
```

### 新数据目录（使用中）

```
workspace-ai-baby/data/
├── ai-baby/
│   ├── memory/             ✅ 使用中
│   ├── logs/               ✅ 使用中
│   └── cache/
├── baby1/
├── baby2/
└── baby3/
```

---

## ✅ 可以安全删除

**workspace-ai-baby-config 已经没用！**

**原因：**
1. ✅ 所有数据已迁移到新位置
2. ✅ Memory Hub 使用新路径
3. ✅ 所有 Agent 使用新路径
4. ✅ 测试验证通过

---

## 🗑️ 清理步骤

### 1. 备份（可选但推荐）

```bash
# 备份到临时位置
mkdir -p ~/backup
cp -r ~/.openclaw/workspace-ai-baby-config ~/backup/workspace-ai-baby-config.backup

echo "✅ 备份完成：~/backup/workspace-ai-baby-config.backup"
```

### 2. 删除旧目录

```bash
# 删除旧配置目录
rm -rf ~/.openclaw/workspace-ai-baby-config

echo "✅ 清理完成"
```

### 3. 验证

```bash
# 确认旧目录已删除
ls -la ~/.openclaw/ | grep workspace-ai-baby-config

# 应该无输出
```

---

## 📋 迁移历史

| 时间 | 事件 | 状态 |
|------|------|------|
| **2026-03-23 12:41** | 创建 workspace-ai-baby-config | ✅ 完成 |
| **2026-03-23 18:44** | 数据迁移到新位置 | ✅ 完成 |
| **2026-03-23 18:50** | 所有 Agent 使用新路径 | ✅ 完成 |
| **2026-03-23 19:30** | 标记为可删除 | ✅ 完成 |

---

## ⚠️ 注意事项

### 删除前确认

1. **确认数据已迁移**
   ```bash
   ls -la /Users/dhr/.openclaw/workspace-ai-baby/data/ai-baby/memory/
   # 应该看到数据库文件
   ```

2. **确认测试通过**
   ```bash
   python3 scripts/test_agents.py
   # 应该所有 Agent 测试通过
   ```

3. **备份重要凭证**
   ```bash
   cat ~/.openclaw/workspace-ai-baby-config/credentials.json
   # 如果有重要凭证，先备份
   ```

### 删除后恢复（如果需要）

```bash
# 从备份恢复
cp -r ~/backup/workspace-ai-baby-config.backup ~/.openclaw/workspace-ai-baby-config
```

---

## 🎯 建议

**推荐：立即删除**

- ✅ 数据已完全迁移
- ✅ 测试验证通过
- ✅ 新系统运行稳定
- ✅ 避免混淆

**保守：保留 1-2 周**

- 观察新系统稳定性
- 确认无问题后再删除

---

**维护者：** ai-baby  
**创建时间：** 2026-03-23 19:30  
**状态：** ⚠️ 待清理
