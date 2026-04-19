# Knowledge Graph - 知识图谱

## 描述
构建和管理知识图谱，发现实体关系。

## 功能
- 自动扩展知识图谱
- 搜索增强（相关概念发现）

## 依赖
- `libs/memory_hub` (记忆存储)

## 用法
```bash
# 自动扩展
python3 skills/knowledge-graph/auto_expander.py --agent <agent_name>

# 搜索增强
python3 skills/knowledge-graph/search_enhancer.py --query "查询词"
```

## 独立性
✅ 仅依赖 libs/，无跨 skill 依赖
