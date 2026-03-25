# evolution-workbench - 自我进化工作台安装指南

**实时监控 AI 的自我进化过程，可视化展示系统状态和进化事件。**

> 📊 实时指标监控 | 🧬 进化事件追踪 | 🔧 系统状态检查

---

## ⚡ 一键安装（推荐）

技能已预装，只需验证和测试：

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/evolution-workbench

# 2. 测试运行（命令行版）
python3 dashboard.py --once

# 3. 查看帮助
python3 dashboard.py --help
```

**就这么简单！** 技能已预装，无需额外依赖。

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 5MB 磁盘空间

### 可选

- ⭕ Flask（用于 Web 界面）
  ```bash
  pip3 install flask
  ```

---

## 🚀 详细安装步骤

### Step 1: 验证技能文件

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/evolution-workbench/

# 应该看到：
# dashboard.py, web_dashboard.py, README.md, 和各种 HTML 模板
```

### Step 2: 检查 Python 依赖

```bash
# Python 版本
python3 --version  # 需要 3.9+

# SQLite3
python3 -c "import sqlite3; print('SQLite3:', sqlite3.version)"

# Flask（可选，用于 Web 界面）
python3 -c "import flask; print('Flask:', flask.__version__)" 2>/dev/null || echo "Flask 未安装（可选）"
```

### Step 3: 测试运行

```bash
cd ~/.openclaw/workspace/skills/evolution-workbench

# 命令行版本（显示一次）
python3 dashboard.py --once

# 应该看到类似输出：
# ╔══════════════════════════════════════════════════════════════════╗
# ║                       🧬 自我进化工作台                           ║
# ╚══════════════════════════════════════════════════════════════════╝
# 📊 实时指标 ...
```

---

## 🔧 配置说明

### 数据源配置

编辑 `dashboard.py` 中的数据路径（如需要）：

```python
# 默认配置
WORKSPACE = Path("/Users/dhr/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
SKILLS_DIR = WORKSPACE / "skills"
```

### Web 界面配置（可选）

编辑 `web_dashboard.py` 配置 Web 服务器：

```python
# Flask 配置
app = Flask(__name__)
PORT = 8080  # Web 界面端口
HOST = "localhost"
```

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/skills/evolution-workbench/
├── README.md                 # 快速开始指南
├── INSTALL.md                # 本文件
├── dashboard.py              # 命令行仪表板
├── web_dashboard.py          # Web 版仪表板
├── dashboard.html            # Web 界面模板
├── dashboard_*.html          # 各种界面变体
├── data_generator.py         # 测试数据生成器
└── static/                   # 静态资源（如需要）
```

### 数据依赖

工作台从以下位置读取数据：

```
~/.openclaw/workspace/
├── memory/
│   ├── memory_stream.db      # 记忆流数据
│   ├── knowledge_base.db     # 知识库数据
│   └── *.md                  # 记忆文件
├── skills/                   # 技能目录（统计数量）
└── MEMORY.md                 # 长期记忆
```

---

## 🎯 常用命令

### 命令行版本

```bash
# 显示一次（不刷新）
python3 dashboard.py --once

# 实时监控模式（每 2 秒刷新）
python3 dashboard.py --watch

# 记录日志
python3 dashboard.py --log "完成新功能开发"

# 记录进化事件
python3 dashboard.py --evolve "创建了新的搜索技能"

# 查看帮助
python3 dashboard.py --help
```

### Web 版本

```bash
# 启动 Web 服务器
python3 web_dashboard.py

# 然后在浏览器打开 http://localhost:8080
```

### 进化控制中心

```bash
# 一键完整检查
python3 ../self-reflection/evolution_control.py full-check
```

---

## ✅ 安装验证

运行以下命令验证安装：

```bash
# 1. 命令行仪表板
python3 dashboard.py --once

# 2. 检查数据源
ls -la ../memory/*.db
ls -la ../memory/*.md

# 3. Web 界面（可选）
python3 web_dashboard.py &
curl http://localhost:8080
```

---

## 📊 界面预览

### 命令行输出

```
╔══════════════════════════════════════════════════════════════════╗
║                       🧬 自我进化工作台                           ║
╚══════════════════════════════════════════════════════════════════╝

📊 实时指标
──────────────────────────────────────────────────────────────────
  总交互次数：42
  成功率：95.2%
  技能数量：8
  记忆大小：2.34 MB
  健康评分：83/100

🔧 系统状态
──────────────────────────────────────────────────────────────────
  记忆系统            ✅ 运行中
  语义搜索            ✅ 就绪
  自动反思            ✅ 启用
  预测维护            ✅ 运行中

🧬 最近进化事件
──────────────────────────────────────────────────────────────────
  [14:03:15] skill_created: 创建了 websearch 技能
  [14:05:22] improvement: 添加了重试机制
  [14:08:10] optimization: 优化了搜索性能
```

### Web 界面

启动后访问 `http://localhost:8080` 查看可视化仪表板。

---

## ❓ 常见问题

### Q: 运行时提示 "ModuleNotFoundError"

**A:** 检查 Python 依赖：

```bash
# 安装 Flask（用于 Web 界面）
pip3 install flask
```

### Q: 仪表板显示空数据

**A:** 检查工作目录是否有数据：

```bash
# 检查记忆文件
ls -la ~/.openclaw/workspace/memory/

# 如果没有数据，先运行一些交互或每日回顾
python3 ../memory-search/daily_review.py
```

### Q: Web 界面无法访问

**A:** 检查端口是否被占用：

```bash
# 检查端口
lsof -i :8080

# 或使用其他端口
python3 web_dashboard.py --port 8081
```

### Q: 如何自定义仪表板指标？

**A:** 编辑 `dashboard.py` 中的指标计算逻辑：

```python
# 添加自定义指标
def get_custom_metrics():
    return {
        "自定义指标": calculate_custom_value()
    }
```

### Q: 如何卸载技能？

**A:** 删除技能目录：

```bash
rm -rf ~/.openclaw/workspace/skills/evolution-workbench
```

---

## 📚 相关技能

| 技能 | 说明 |
|------|------|
| **memory-search** | 记忆搜索和管理 |
| **self-reflection** | 自我反思系统 |
| **evolution-workbench** | 进化监控仪表板 |

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **README.md** | 快速开始指南 |
| **INSTALL.md** | 本文件 - 安装指南 |
| **dashboard.py** | 命令行仪表板（内嵌帮助） |

---

## 🆘 获取帮助

遇到问题？

1. 运行 `python3 dashboard.py --help` 查看帮助
2. 检查数据文件是否存在
3. 查看技能的 `README.md` 文件
4. 在 OpenClaw 社区提问：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-22**: 创建独立安装文档
- **2026-03-17**: evolution-workbench 技能创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** OpenClaw Assistant
