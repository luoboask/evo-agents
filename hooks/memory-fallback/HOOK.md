# Memory Fallback Hook

> **功能**: 在 OpenClaw 原始记忆未找到相关信息时，自动从 memory-search 查询  
> **触发时机**: 用户发送消息前  
> **用途**: 增强对话上下文，提供更准确的回复  

---

## 🚀 功能

当用户问到与历史、记忆、上下文相关的问题时：

1. **检测** - 检查用户消息是否包含触发词
2. **查询** - 从 memory-search 检索相关记忆
3. **增强** - 将查询结果添加到系统提示
4. **回复** - LLM 基于增强的上下文生成回复

---

## 📋 触发词

| 类型 | 关键词 |
|------|--------|
| 时间 | 之前、以前、历史、上次 |
| 记忆 | 记得、说过、问过、讨论 |
| 查询 | 怎么、如何、什么、哪里 |
| 内容 | 项目、系统、任务、配置 |

---

## 🔧 安装

```bash
# 从 workspace 安装
openclaw hooks install /Users/dhr/.openclaw/workspace-claude-code-agent/hooks/memory-fallback

# 启用
openclaw hooks enable memory-fallback

# 检查状态
openclaw hooks info memory-fallback
```

---

## 📝 配置

```json
{
  "hooks": {
    "memory-fallback": {
      "enabled": true,
      "top_k": 5,
      "agent_name": "claude-code-agent",
      "trigger_keywords": ["之前", "如何", "记得"]
    }
  }
}
```

---

## 💡 使用示例

### 示例 1：查询历史

```
用户：我之前说过什么关于定时任务的？
   ↓
Hook 检测："之前" → 触发查询
   ↓
memory-search 查询：找到相关记忆
   ↓
增强系统提示：添加查询结果
   ↓
LLM 回复：根据记忆，你之前说过...
```

### 示例 2：配置问题

```
用户：如何配置定时任务？
   ↓
Hook 检测："如何"、"配置" → 触发查询
   ↓
memory-search 查询：找到配置文档
   ↓
增强系统提示：添加配置信息
   ↓
LLM 回复：配置定时任务的步骤是...
```

---

## 🔗 相关文件

- `handler.ts` - Hook 处理器
- `index.ts` - 入口文件
- `package.json` - 依赖配置

---

**最后更新**: 2026-04-10  
**版本**: v1.0
