# 智能进化工作台 - 使用指南

**更新时间：** 2026-03-17 11:26

---

## 🎯 访问地址

### 主工作台
```
http://127.0.0.1:3002/
```

### 智能程度仪表盘
```
http://127.0.0.1:3002/intelligence_dashboard.html
```

---

## 📊 可用页面

### 1. React 主仪表板
**文件：** `react-dashboard/build/index.html`  
**特点：** 现代化 UI，完整功能

### 2. 智能程度仪表盘 ⭐ 新增
**文件：** `intelligence_dashboard.html`  
**特点：** 展示系统智能程度、检测结果、元规则

### 3. 其他仪表板
- `dashboard_final.html` - 深蓝渐变主题
- `dashboard_enhanced.html` - 增强版
- `visual_dashboard.html` - 可视化版本

---

## 🔌 API 端点

### 核心 API

| 端点 | 功能 | 说明 |
|------|------|------|
| `/api/overview` | 系统概览 | 记忆、进化、实例状态 |
| `/api/intelligence-report` | 智能报告 | ⭐ 新增，展示智商评分 |
| `/api/knowledge` | 知识库 | 知识列表和统计 |
| `/api/events` | 进化事件 | 事件列表 |
| `/api/stats` | 统计数据 | 各类统计 |

### 使用示例

```bash
# 获取智能报告
curl http://127.0.0.1:3002/api/intelligence-report

# 获取知识库
curl http://127.0.0.1:3002/api/knowledge

# 获取概览
curl http://127.0.0.1:3002/api/overview
```

---

## 🚀 启动工作台

### 自动启动（推荐）

工作台已配置为自动启动，检查状态：

```bash
# 检查是否运行
curl http://127.0.0.1:3002/api/overview

# 如果未运行，手动启动
cd /Users/dhr/.openclaw/workspace/skills/evolution-workbench
python3 integrated_server.py
```

### 手动启动

```bash
cd /Users/dhr/.openclaw/workspace/skills/evolution-workbench

# 默认端口 3002
python3 integrated_server.py

# 或指定端口
python3 integrated_server.py --port 8080
```

---

## 📊 智能程度仪表盘功能

### 核心统计
- 📚 知识库总数
- 📈 进化事件总数
- 🧠 记忆总数
- ⭐ 综合智商评分

### 能力评估
展示 5 大核心能力：
1. 模式识别 ⭐⭐⭐⭐⭐
2. 抽象思考 ⭐⭐⭐⭐⭐
3. 语义检索 ⭐⭐⭐⭐⭐
4. 自动学习 ⭐⭐⭐⭐⭐
5. 自我反思 ⭐⭐⭐⭐⭐

### 检测到的模式
- 系统自进化活跃期
- 持续代码改进
- 知识获取频繁
- 功能快速增加

每个模式显示：
- 出现次数
- 模式强度 (0-1)
- 严重性等级

### 生成的元规则
展示从事件中提取的智慧结晶

---

## 🎨 界面预览

### 智能程度仪表盘

**设计风格：**
- 深色渐变背景
- 毛玻璃效果卡片
- 动态数据展示
- 响应式布局

**交互功能：**
- 🔄 一键刷新数据
- 📊 实时统计
- 🎯 能力评分可视化

---

## 🔧 自定义配置

### 修改端口

编辑 `integrated_server.py`：

```python
def run_server(port=3002):  # 修改这里的端口
    ...
```

### 添加新页面

1. 在 `react-dashboard/build/` 目录创建 HTML 文件
2. 或在当前目录创建 HTML 文件
3. 访问 `http://127.0.0.1:3002/你的页面.html`

### 添加新 API

编辑 `integrated_server.py`：

```python
def _handle_api(self, path):
    if path == '/api/your-new-endpoint':
        data = self._get_your_data()
```

---

## 📝 常见问题

### Q1: 工作台无法访问？

```bash
# 检查是否运行
ps aux | grep integrated_server

# 检查端口
lsof -i :3002

# 重启服务
pkill -f integrated_server.py
python3 integrated_server.py
```

### Q2: 数据显示不正确？

```bash
# 清除缓存
rm -rf /tmp/workbench.log

# 重启服务
pkill -f integrated_server.py
python3 integrated_server.py
```

### Q3: 如何查看实时日志？

```bash
# 查看运行日志
tail -f /tmp/workbench.log

# 查看 API 请求
tail -f /tmp/workbench.log | grep "GET /api"
```

---

## 🎯 最佳实践

### 1. 定期查看智能报告
```bash
# 每天早上查看
curl http://127.0.0.1:3002/api/intelligence-report | python3 -m json.tool
```

### 2. 监控进化事件
```bash
# 查看最新事件
sqlite3 evolution.db "SELECT event_type, description, timestamp FROM evolution_events ORDER BY timestamp DESC LIMIT 10;"
```

### 3. 备份数据
```bash
# 备份数据库
cp evolution.db evolution_backup_$(date +%Y%m%d).db
```

---

## 📊 当前状态

| 组件 | 状态 | 地址 |
|------|------|------|
| 工作台服务 | ✅ 运行中 | http://127.0.0.1:3002/ |
| 智能仪表盘 | ✅ 可用 | /intelligence_dashboard.html |
| API 服务 | ✅ 正常 | /api/* |
| 数据库 | ✅ 正常 | evolution.db |

---

**工作台已优化完成！访问 http://127.0.0.1:3002/intelligence_dashboard.html 查看智能程度！** 🎉
