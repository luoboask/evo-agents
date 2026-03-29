# 文档索引

**更新日期：** 2026-03-29

---

## 📚 用户文档（安装后保留）

### 快速开始
- **[QUICKSTART.md](QUICKSTART.md)** - 快速开始指南

### 使用指南
- **[FAQ.md](FAQ.md)** - 常见问题解答
- **[SELF_CHECK.md](SELF_CHECK.md)** - 自检工具使用
- **[UNINSTALL.md](UNINSTALL.md)** - 卸载指南
- **[AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md)** - Agent 指令
- **[WORKSPACE_RULES.md](WORKSPACE_RULES.md)** - Workspace 使用规范

---

## 👨‍💻 开发者文档（安装时删除）

位于 `docs/dev/` 目录：

- **SCRIPT_DEVELOPMENT.md** - 脚本开发规范
- **STRUCTURE_RULES.md** - 结构规则
- **SCRIPTS_INVENTORY.md** - 脚本清单

**用途：** 开发新脚本或维护模板时参考

---

## 🏗️ 架构文档（安装时删除）

位于 `docs/arch/` 目录：

- **ARCHITECTURE_GENERIC_CN.md** - 架构说明（中文）
- **ARCHITECTURE_GENERIC_EN.md** - 架构说明（英文）
- **PERFORMANCE_OPTIMIZATION_PLAN.md** - 性能优化方案

**用途：** 了解系统架构和性能优化

---

## 🔒 内部文档（安装时删除）

位于 `docs/internal/` 目录：

- **TEST_REGRESSION_CHECKLIST.md** - 测试回归清单
- **REGRESSION_TEST_FINAL_2026-03-29.md** - 测试报告
- **RELEASE_2026-03-28.md** - 发布说明
- **SUB_AGENT_TEST.md** - 子 agent 测试报告
- **MIGRATION.md** - 迁移指南
- **TODO.md** - 待办事项

**用途：** 开发团队内部使用

---

## 📊 安装后文档结构

用户安装后，docs/ 目录只保留：

```
docs/
├── QUICKSTART.md          # 快速开始
├── FAQ.md                 # 常见问题
├── SELF_CHECK.md          # 自检工具
├── UNINSTALL.md           # 卸载指南
├── AGENT_INSTRUCTIONS.md  # Agent 指令
└── WORKSPACE_RULES.md     # 使用规范
```

**共 6 个文档，简洁清晰！**

---

## 🎯 文档分类原则

1. **用户文档** - 日常使用需要参考
2. **开发者文档** - 开发维护时参考
3. **架构文档** - 了解系统设计
4. **内部文档** - 团队内部使用

**安装时自动清理后 3 类，用户只看到必要的文档。**
