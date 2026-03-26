# GitHub 仓库配置清单

请在 https://github.com/luoboask/evo-agents/settings 中按以下配置：

## 1. 仓库名称（可选，建议保留）

当前：luoboask/evo-agents
建议：保留（改名会影响所有 clone 链接）

## 2. 仓库描述（Description）

**英文：**
```
Unified Memory System for OpenClaw — Markdown + SQLite bidirectional sync, semantic search with local Ollama, zero external API keys.
```

**中文（备用）：**
```
OpenClaw 统一记忆系统 — Markdown + SQLite 双向同步，本地 Ollama 语义搜索，无需外部 API Key。
```

## 3. 网站（Website）

```
https://github.com/luoboask/evo-agents
```

或如果有文档站点：
```
https://luoboask.github.io/evo-agents
```

## 4. Topics / 标签（最多 20 个）

请添加以下标签：
- openclaw
- memory-system
- agent
- ai-memory
- semantic-search
- sqlite
- markdown
- ollama
- bge-m3
- fts5
- chinese-nlp
- local-ai
- knowledge-base
- rag
- self-evolution

## 5. 社交预览图（Social Preview）

建议上传一张 1280×640 的封面图，包含：
- 项目名称：Unified Memory System
- 副标题：Give your OpenClaw agent real memory
- 关键特性图标（Markdown ↔ SQLite, Semantic Search, Local AI）

可以用 Canva 或 Figma 制作。

## 6. 功能设置（Features）

✅ **启用 Issues** — 用于 bug 报告和功能请求
✅ **启用 Discussions** — 用于社区讨论
✅ **启用 Projects** — 可选，用于项目管理
❌ **禁用 Wikis** — 文档已在 repo 中
✅ **启用 Sponsorships** — 可选，如果接受赞助

## 7. 分支保护规则（Branch Protection）

为 master 分支添加保护：
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
- ✅ Include administrators
- ✅ Restrict pushes that create files larger than 100MB

## 8. 安全设置

- ✅ Enable vulnerability alerts
- ✅ Enable automated security fixes

## 9. 操作确认

配置完成后，请确认：
- [ ] 仓库描述已更新
- [ ] Topics 已添加（显示在仓库标题下方）
- [ ] README 徽章正常显示
- [ ] 社交预览图已上传（可选）

## 10. 本地验证

配置后本地验证：
```bash
# 检查远程 URL
git remote -v

# 应该显示：
# origin  git@github.com:luoboask/evo-agents.git (fetch)
# origin  git@github.com:luoboask/evo-agents.git (push)
```

---

**注意：** 项目名称（仓库名）建议保留 `evo-agents`，因为：
1. 改名会影响所有已 fork/clone 的用户
2. 可以通过描述和 README 清晰表达项目用途
3. 保持 URL 稳定性

如果坚持要改名，可以在 Settings → Repository name 中修改，但会有一段时间的 404 风险。
