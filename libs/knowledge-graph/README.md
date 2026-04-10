# Knowledge Graph - 知识图谱构建器

从记忆中自动提取实体和关系，构建结构化知识网络。

## ✨ 功能特性

- **规则提取** - 基于正则表达式快速识别实体
- **AI 辅助提取** - 使用 Ollama LLM 提取规则无法匹配的实体（可选）
- **关系推断** - 自动发现隐含关系（传递闭包）
- **失败回退** - 如果 LLM 不可用，自动回退到规则提取

## 📦 依赖要求

### 必需
- Python 3.9+
- SQLite3

### 可选（增强功能）
- Ollama + `qwen2.5:0.5b` 模型（AI 实体提取）

```bash
# 安装 Ollama（如未安装）
brew install ollama  # macOS
# 或访问 https://ollama.ai

# 拉取模型
ollama pull qwen2.5:0.5b
```

## 🚀 使用方法

### 基础用法

```bash
# 进入技能目录
cd ~/.openclaw/workspace-<agent>/libs/knowledge-graph

# 构建知识图谱（规则 + AI）
python3 builder.py

# 仅使用规则提取（更快，无需 Ollama）
python3 builder.py --no-ai

# 查看统计信息
python3 builder.py --stats
```

### 输出示例

```bash
$ python3 builder.py

🔨 开始构建知识图谱...
📄 找到 15 个记忆文件
  📌 规则提取 18 个实体 (2026-04-01.md)
  🤖 AI 提取 3 个实体 (2026-04-02.md)
  🔍 推断出 8 条隐含关系
✅ 知识图谱已保存：48 个实体，17 条关系

✅ 知识图谱构建完成！
   实体数：48
   关系数：17
```

### 自动化（推荐）

**每周六凌晨 4 点自动更新知识图谱：**

```bash
crontab -e

# 添加以下行：
0 4 * * 6 cd ~/.openclaw/workspace-<agent>/libs/knowledge-graph && python3 builder.py >> /tmp/kg_build.log 2>&1
```

## 📊 数据结构

生成的 `memory/knowledge_graph.json`：

```json
{
  "entities": {
    "Technology:openclaw": {
      "type": "Technology",
      "name": "OpenClaw",
      "mentions": 48,
      "properties": {},
      "created_at": "2026-03-16T11:35:39"
    }
  },
  "relations": [
    {
      "source": "Technology:openclaw",
      "relation": "基于",
      "target": "Technology:jvs_claw",
      "confidence": 0.9,
      "inferred": false
    },
    {
      "source": "Technology:openclaw",
      "relation": "间接基于→使用",
      "target": "Technology:ollama",
      "confidence": 0.6,
      "inferred": true
    }
  ]
}
```

## 🔧 命令行参数

| 参数 | 说明 |
|------|------|
| `--no-ai` | 不使用 AI 提取（仅规则） |
| `--stats` | 只显示统计信息，不构建 |
| `-h, --help` | 显示帮助信息 |

## ⚠️ 故障排除

### Q: AI 提取很慢或失败？

**A:** 使用 `--no-ai` 参数仅使用规则提取：
```bash
python3 builder.py --no-ai
```

### Q: Ollama 连接失败？

**A:** 检查 Ollama 服务是否运行：
```bash
ollama list  # 确认模型已安装
ollama run qwen2.5:0.5b "测试"  # 测试模型
```

### Q: 如何重置知识图谱？

**A:** 删除 `knowledge_graph.json` 后重新构建：
```bash
rm ../memory/knowledge_graph.json
python3 builder.py
```

## 📝 最佳实践

1. **更新频率**
   - 高频使用：每周更新 1 次
   - 中频使用：每两周更新 1 次
   - 低频使用：每月更新 1 次

2. **AI vs 规则**
   - 日常使用：规则提取（快速）
   - 定期深度整理：规则 + AI（完整）

3. **备份**
   ```bash
   cp ../memory/knowledge_graph.json \
      ../memory/knowledge_graph.backup_$(date +%Y%m%d).json
   ```

## 🔗 相关技能

- **memory-search** - 记忆搜索（使用知识图谱增强搜索结果）
- **memory-compression** - 记忆压缩（日→周→月摘要）

---

**最后更新：** 2026-04-04  
**版本：** v2.0 (Enhanced with AI)
