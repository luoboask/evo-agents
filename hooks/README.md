# OpenClaw Hooks

本目录包含自定义 OpenClaw Hooks，用于扩展 OpenClaw 功能。

---

## 📦 可用 Hooks

### Memory Fallback

**功能**: 在 OpenClaw 原始记忆未找到时，自动从 memory-search 查询

**安装**:
```bash
./hooks/memory-fallback/install.sh
```

**卸载**:
```bash
./hooks/memory-fallback/uninstall.sh
```

**触发时机**: `before_llm_call`（LLM 调用前）

**用途**:
- 增强对话上下文
- 提供更准确的回复
- 自动查询历史记忆

---

## 🔧 管理命令

```bash
# 查看所有 Hooks
openclaw hooks list

# 查看 Hook 状态
openclaw hooks info memory-fallback

# 禁用 Hook
openclaw hooks disable memory-fallback

# 重新启用
openclaw hooks enable memory-fallback
```

---

## 📝 开发新 Hook

1. 创建目录：`hooks/your-hook-name/`
2. 添加文件：
   - `HOOK.md` - Hook 描述和配置
   - `handler.ts` - Hook 处理器
   - `package.json` - NPM 配置
   - `install.sh` - 安装脚本（可选）

参考：[OpenClaw Hooks 文档](https://docs.openclaw.ai/automation/hooks)

---

**最后更新**: 2026-04-10
