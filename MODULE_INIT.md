# 🔧 模块化初始化指南

**版本：** v5.1  
**最后更新：** 2026-03-23

---

## 📋 概述

ai-baby 支持**完整初始化**和**模块化初始化**两种方式。

### 完整初始化 vs 模块化初始化

| 方式 | 命令 | 适用场景 | 时间 |
|------|------|----------|------|
| **完整初始化** | `python3 init_system.py` | 新用户首次使用 | ~10 秒 |
| **模块化初始化** | `python3 init_system.py -m <module>` | 只使用部分功能/故障修复 | ~3 秒 |

---

## 🎯 可用模块

### 1. memory-search（记忆搜索）

**功能：** 关键词搜索 + 向量语义搜索

**初始化内容：**
- ✅ 检查数据库文件
- ✅ 验证数据库完整性
- ✅ 测试搜索功能

**命令：**
```bash
python3 init_system.py -m memory-search
```

**输出示例：**
```
[1/3] 检查记忆搜索依赖...
✅ 数据库已存在：~/.openclaw/workspace-ai-baby-config/memory/...
✅ 数据库正常：23 条记忆
✅ 记忆搜索模块初始化完成 ✅
```

---

### 2. rag（RAG 评估）

**功能：** 检索质量评估与优化

**初始化内容：**
- ✅ 检查日志文件
- ✅ 创建必要目录
- ✅ 测试记录功能

**命令：**
```bash
python3 init_system.py -m rag
```

**输出示例：**
```
[1/3] 检查 RAG 评估依赖...
✅ 日志文件已存在：6 条记录

[2/3] 测试 RAG 记录功能...
✅ RAG 记录功能正常 ✅

[3/3] RAG 评估模块初始化完成 ✅
```

---

### 3. self-evolution（自进化核心）

**功能：** 分形思考 + 夜间循环 + 记忆流

**初始化内容：**
- ✅ 检查核心文件
- ✅ 测试模块导入
- ✅ 验证依赖关系

**命令：**
```bash
python3 init_system.py -m self-evolution
```

**输出示例：**
```
[1/3] 检查自进化核心依赖...
检查核心文件...
✅   ✅ main.py
✅   ✅ memory_stream.py
✅   ✅ fractal_thinking.py
✅   ✅ nightly_cycle.py

[2/3] 测试模块导入...
✅ memory_stream 导入成功 ✅
✅ fractal_thinking 导入成功 ✅

[3/3] 自进化核心模块初始化完成 ✅
```

---

## 🚀 使用方式

### 列出所有模块

```bash
python3 init_system.py --list
```

**输出：**
```
可用模块

  memory-search    - 记忆搜索模块
  rag             - RAG 评估模块
  self-evolution  - 自进化核心模块
  all             - 所有模块（默认）
```

---

### 初始化单个模块

```bash
# 记忆搜索
python3 init_system.py -m memory-search

# RAG 评估
python3 init_system.py -m rag

# 自进化核心
python3 init_system.py -m self-evolution
```

---

### 初始化所有模块

```bash
# 方式 1：使用 -m all
python3 init_system.py -m all

# 方式 2：不带参数（默认）
python3 init_system.py
```

---

## 📊 使用场景

### 场景 1：新用户首次使用

**推荐：** 完整初始化

```bash
python3 init_system.py
```

**原因：** 一次性检查所有依赖和配置

---

### 场景 2：只使用记忆搜索

**推荐：** 模块化初始化

```bash
python3 init_system.py -m memory-search
```

**原因：** 快速初始化，跳过不需要的模块

---

### 场景 3：某个模块出现问题

**推荐：** 重新初始化该模块

```bash
# RAG 评估出现问题
python3 init_system.py -m rag

# 自进化核心出现问题
python3 init_system.py -m self-evolution
```

**原因：** 针对性修复，不影响其他模块

---

### 场景 4：日常快速检查

**推荐：** 快速验证

```bash
python3 quick_verify.py
```

**原因：** 10 秒内完成所有功能验证

---

## 🔧 高级用法

### 组合使用

```bash
# 初始化记忆搜索 + RAG 评估
python3 init_system.py -m memory-search
python3 init_system.py -m rag

# 跳过自进化核心
python3 init_system.py -m memory-search
python3 init_system.py -m rag
```

---

### 脚本化

```bash
#!/bin/bash
# 批量初始化模块

MODULES=("memory-search" "rag")

for module in "${MODULES[@]}"; do
    echo "初始化：$module"
    python3 init_system.py -m "$module"
done
```

---

## 📋 初始化检查清单

### memory-search 模块

- [ ] Python 3.9+ 已安装
- [ ] sqlite3 可用
- [ ] 数据库文件存在（或可创建）
- [ ] 数据库表结构正确

### rag 模块

- [ ] Python 3.9+ 已安装
- [ ] yaml 包已安装
- [ ] 日志文件存在（或可创建）
- [ ] 记录功能正常

### self-evolution 模块

- [ ] Python 3.9+ 已安装
- [ ] 核心文件完整
- [ ] 模块可正常导入
- [ ] 依赖关系正确

---

## 🆘 故障处理

### 问题 1：模块初始化失败

```bash
# 查看详细错误
python3 init_system.py -m <module> -v

# 重新初始化
python3 init_system.py -m <module>
```

### 问题 2：数据库损坏

```bash
# 重新初始化记忆搜索
python3 init_system.py -m memory-search

# 如果仍然失败，检查数据库文件
ls -la ~/.openclaw/workspace-ai-baby-config/memory/
```

### 问题 3：日志文件权限问题

```bash
# 检查权限
ls -la ~/.openclaw/workspace-ai-baby-config/logs/

# 修复权限
chmod 755 ~/.openclaw/workspace-ai-baby-config/logs/
```

### 问题 4：模块文件丢失

```bash
# 重新初始化该模块
python3 init_system.py -m <module>

# 如果文件确实丢失，从 Git 恢复
git checkout HEAD -- skills/<module>/
```

---

## 📊 性能对比

| 初始化方式 | 时间 | 检查项 |
|------------|------|--------|
| **完整初始化** | ~10 秒 | 7 项 |
| **单个模块** | ~3 秒 | 3 项 |
| **快速验证** | ~2 秒 | 3 项 |

---

## 🎯 最佳实践

### 新用户

```bash
# Day 1: 完整初始化
python3 init_system.py

# 验证功能
python3 quick_verify.py

# 开始使用
./start.sh
```

### 日常使用

```bash
# 每天：查看状态
./start.sh

# 每周：快速验证
python3 quick_verify.py

# 每月：完整检查
python3 init_system.py
```

### 故障排查

```bash
# 1. 快速验证
python3 quick_verify.py

# 2. 针对性初始化
python3 init_system.py -m <problematic_module>

# 3. 完整检查
python3 init_system.py
```

---

## 📚 相关文档

- `GETTING_STARTED.md` - 快速开始指南
- `USER_MANUAL.md` - 详细使用手册
- `CONFIG_SEPARATION.md` - 配置分离方案
- `SECURITY_REPORT.md` - 安全报告

---

## 🎉 总结

**模块化初始化的优势：**

✅ **快速** - 只初始化需要的模块  
✅ **灵活** - 可以组合使用  
✅ **针对性** - 故障修复更精准  
✅ **独立** - 模块间互不影响  

**推荐使用方式：**

- 新用户：完整初始化
- 日常使用：快速验证
- 故障修复：模块化初始化

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23  
**许可证：** MIT
