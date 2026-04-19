# Self-Evolution - 自进化系统

## 描述
Agent 自进化系统，支持效果追踪、方案复用、策略切换等。

## 功能
- 效果追踪（成功/失败统计）
- 方案复用（语义级匹配）
- 自动策略切换
- Gene 进化分析
- 元学习

## 依赖
- `libs/memory_hub` (记忆存储)
- `libs/embedding_utils` (Embedding 工具)
- `libs/effect_tracker` (效果追踪)

## 用法
```bash
# 夜间进化循环
python3 skills/self-evolution/nightly_cycle.py

# 方案复用
python3 skills/self-evolution/solution_reuse.py
```

## 独立性
✅ 仅依赖 libs/，无跨 skill 依赖
