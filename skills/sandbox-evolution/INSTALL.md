# sandbox-evolution - 沙箱进化技能安装指南

**为 sandbox-agent 提供自进化能力：记录事件、学习经验、智能建议。**

> 🧠 记忆能力 | 📚 学习能力 | 💡 智能建议 | 🔄 持续改进

---

## ⚡ 一键安装（推荐）

技能已预装，只需验证和测试：

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/sandbox-evolution

# 2. 测试模块导入
python3 -c "from evolution import SandboxEvolution; print('✅ 模块加载成功')"

# 3. 查看文档
cat README.md
```

**就这么简单！** 技能已预装，无需额外依赖。

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 10MB 磁盘空间

### 可选

- ⭕ sandbox-agent（主要调用方）

---

## 🚀 详细安装步骤

### Step 1: 验证技能文件

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/sandbox-evolution/

# 应该看到：
# SKILL.md, README.md, USAGE.md, __init__.py, evolution.py
```

### Step 2: 检查 Python 依赖

```bash
# Python 版本
python3 --version  # 需要 3.9+

# SQLite3
python3 -c "import sqlite3; print('SQLite3:', sqlite3.version)"

# 测试模块导入
python3 -c "from evolution import SandboxEvolution; print('✅ SandboxEvolution 加载成功')"
```

### Step 3: 测试运行

```bash
cd ~/.openclaw/workspace/skills/sandbox-evolution

# 测试初始化
python3 -c "
from evolution import SandboxEvolution
evolution = SandboxEvolution()
print('✅ 沙箱进化系统初始化成功')
print(f'数据库位置：{evolution.db_path}')
"
```

---

## 🔧 配置说明

### 数据路径配置

编辑 `evolution.py` 中的数据路径（如需要）：

```python
# 默认配置
self.workspace = Path("/Users/dhr/.openclaw/workspace")
self.data_dir = self.workspace / "memory" / "sandbox-evolution"
self.data_dir.mkdir(parents=True, exist_ok=True)
self.db_path = self.data_dir / "evolution.db"
```

### 事件类型

支持的事件类型：

| 事件类型 | 说明 |
|----------|------|
| `SANDBOX_CREATED` | 沙箱创建 |
| `SANDBOX_STARTED` | 沙箱启动 |
| `INTEGRATION_STARTED` | 联调开始 |
| `INTEGRATION_COMPLETED` | 联调完成 |
| `TEST_PASSED` | 测试通过 |
| `TEST_FAILED` | 测试失败 |
| `BUG_DETECTED` | 检测到 Bug |
| `BUG_FIXED` | Bug 修复 |

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/skills/sandbox-evolution/
├── SKILL.md              # 技能定义
├── README.md             # 快速开始
├── USAGE.md              # 详细使用说明
├── INSTALL.md            # 本文件
├── __init__.py           # 技能入口
├── evolution.py          # 进化核心逻辑
└── integration.py        # 与 sandbox-agent 集成（如需要）

数据目录（自动创建）：
~/.openclaw/workspace/memory/sandbox-evolution/
└── evolution.db          # 进化事件数据库
```

---

## 🎯 使用方法

### 在 sandbox-agent 中调用

```python
# 记录事件
await self.call_skill('sandbox-evolution', {
    'action': 'record_event',
    'event_type': 'SANDBOX_CREATED',
    'instance_id': instance_id,
    'details': {
        'requirement_id': 'REQ-001',
        'config': {...}
    }
})

# 获取智能建议
suggestions = await self.call_skill('sandbox-evolution', {
    'action': 'get_suggestions',
    'requirement_id': 'REQ-001'
})

# 从结果学习
await self.call_skill('sandbox-evolution', {
    'action': 'learn_from_result',
    'instance_id': instance_id,
    'test_result': {...},
    'report': {...}
})
```

### Python 直接调用

```python
from evolution import SandboxEvolution

# 初始化
evolution = SandboxEvolution()

# 记录事件
evolution.record_event(
    event_type='BUG_DETECTED',
    instance_id='sandbox-REQ-001-abc',
    details={
        'description': 'SQL 注入漏洞',
        'severity': 'critical',
        'lesson': '所有 SQL 查询必须使用参数化'
    }
)

# 获取建议
suggestions = evolution.get_suggestions('REQ-001')
for s in suggestions:
    print(f"💡 建议：{s['content']}")

# 获取统计
stats = evolution.get_stats()
print(f"总事件数：{stats['total_events']}")
```

---

## 📊 API 参考

### record_event

记录沙箱事件

**参数：**
- `event_type`: 事件类型
- `instance_id`: 沙箱实例 ID
- `details`: 详细信息（字典）

### learn_from_result

从测试结果学习

**参数：**
- `instance_id`: 沙箱实例 ID
- `test_result`: 测试结果
- `report`: 联调报告

### get_suggestions

获取智能建议

**参数：**
- `requirement_id`: 需求 ID

**返回：**
```python
[
    {
        'content': '所有 SQL 查询必须使用参数化',
        'confidence': 0.9,
        'source': 'REQ-003 的经验'
    },
    ...
]
```

### get_common_bugs

获取常见 Bug

**参数：**
- `requirement_type`: 需求类型

### optimize_config

优化沙箱配置

**参数：**
- `instance_id`: 沙箱实例 ID
- `performance_data`: 性能数据

### get_stats

获取统计信息

**返回：**
```python
{
    'total_events': 42,
    'total_suggestions': 15,
    'success_rate': 0.95,
    ...
}
```

### generate_report

生成报告

**参数：**
- `days`: 天数（默认 7）

---

## ✅ 安装验证

运行以下命令验证安装：

```bash
# 1. 测试模块导入
cd ~/.openclaw/workspace/skills/sandbox-evolution
python3 -c "from evolution import SandboxEvolution; print('✅ 加载成功')"

# 2. 测试基本操作
python3 -c "
from evolution import SandboxEvolution
evolution = SandboxEvolution()
evolution.record_event('TEST_EVENT', 'test-001', {'note': '安装验证'})
stats = evolution.get_stats()
print(f'✅ 基本操作成功，总事件数：{stats[\"total_events\"]}')
"

# 3. 检查数据文件
ls -la ~/.openclaw/workspace/memory/sandbox-evolution/
```

---

## 🎯 使用场景

### 场景 1: 创建沙箱时获取历史建议

```python
# 创建沙箱
instance_id = await create_sandbox(config)

# 记录事件
await call_skill('sandbox-evolution', {
    'action': 'record_event',
    'event_type': 'SANDBOX_CREATED',
    'instance_id': instance_id,
    'details': {...}
})

# 获取历史建议
suggestions = await call_skill('sandbox-evolution', {
    'action': 'get_suggestions',
    'requirement_id': config['requirement_id']
})

# 应用建议
for suggestion in suggestions:
    print(f"💡 建议：{suggestion['content']}")
```

### 场景 2: 联调完成后学习

```python
# 执行联调
report = await run_integration(instance_id)

# 从结果学习
await call_skill('sandbox-evolution', {
    'action': 'learn_from_result',
    'instance_id': instance_id,
    'report': report
})

# 生成改进建议
improvements = await call_skill('sandbox-evolution', {
    'action': 'get_improvements',
    'instance_id': instance_id
})
```

---

## ❓ 常见问题

### Q: 导入模块失败

**A:** 检查 Python 路径：

```bash
cd ~/.openclaw/workspace/skills/sandbox-evolution
python3 -c "import sys; print(sys.path)"
```

### Q: 数据库文件不存在

**A:** 首次运行时会自动创建：

```bash
python3 -c "
from evolution import SandboxEvolution
evolution = SandboxEvolution()
print(f'数据库位置：{evolution.db_path}')
"
```

### Q: 如何在 sandbox-agent 中启用？

**A:** 在 sandbox-agent 配置中添加技能：

```python
skills = ['sandbox-evolution', ...]
```

### Q: 如何备份数据？

**A:** 备份数据目录：

```bash
cp -r ~/.openclaw/workspace/memory/sandbox-evolution \
   /path/to/backup/sandbox-evolution-$(date +%Y%m%d)
```

### Q: 如何查看进化历史？

**A:** 使用 get_stats 或生成报告：

```python
evolution = SandboxEvolution()
report = evolution.generate_report(days=7)
print(report)
```

### Q: 如何卸载技能？

**A:** 删除技能目录（数据保留）：

```bash
rm -rf ~/.openclaw/workspace/skills/sandbox-evolution
```

---

## 📚 相关技能

| 技能 | 说明 |
|------|------|
| **sandbox-evolution** | 沙箱进化 |
| **memory-search** | 记忆搜索 |
| **self-reflection** | 自我反思 |

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **SKILL.md** | 技能详细说明 |
| **README.md** | 快速开始指南 |
| **USAGE.md** | 详细使用说明 |
| **INSTALL.md** | 本文件 - 安装指南 |

---

## 🆘 获取帮助

遇到问题？

1. 运行测试命令验证安装
2. 查看 `README.md` 和 `USAGE.md`
3. 在 OpenClaw 社区提问：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-22**: 创建独立安装文档
- **2026-03-17**: sandbox-evolution 技能创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** OpenClaw Assistant
