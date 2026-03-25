# Ollama 自动启动配置

**配置时间：** 2026-03-17  
**状态：** ✅ 已完成

---

## 🚀 自动启动方式

### 方式 1: 运行时自动检查（推荐）

**配置：** ✅ 已集成到 `main.py`

**使用：**
```bash
# 直接运行任何命令，会自动检查并启动 Ollama
python3 main.py status
python3 main.py fractal --limit 10
python3 main.py embedding "修复 Bug" "修复错误"
```

**行为：**
- ✅ 如果 Ollama 正在运行 → 直接使用
- ⚠️ 如果 Ollama 未运行 → 自动启动（等待最多 10 秒）
- ❌ 如果启动失败 → 提示手动运行 `ollama serve`

---

### 方式 2: macOS 开机自启（推荐）

**配置：** ✅ 已配置 LaunchAgent

**文件位置：** `~/Library/LaunchAgents/com.ollama.ollama.plist`

**特性：**
- ✅ 开机自动启动
- ✅ 崩溃自动重启
- ✅ 后台运行

**管理命令：**
```bash
# 查看状态
launchctl list | grep ollama

# 停止服务
launchctl unload ~/Library/LaunchAgents/com.ollama.ollama.plist

# 启动服务
launchctl load ~/Library/LaunchAgents/com.ollama.ollama.plist

# 查看日志
tail -f /tmp/ollama.log
```

---

### 方式 3: 手动启动脚本

**脚本位置：** `start_ollama.sh`

**使用：**
```bash
# 运行脚本
bash start_ollama.sh

# 或添加到 shell 配置
echo "alias ollama-start='bash /path/to/start_ollama.sh'" >> ~/.zshrc
```

---

## 📊 验证 Ollama 状态

### 快速检查

```bash
# 方法 1: 检查进程
pgrep -x ollama && echo "✅ 运行中" || echo "❌ 未运行"

# 方法 2: 检查 API
curl http://localhost:11434/api/tags | python3 -m json.tool

# 方法 3: 使用 main.py
python3 main.py status
```

### 查看已安装的模型

```bash
ollama list
```

**输出示例：**
```
NAME                       ID              SIZE      MODIFIED
nomic-embed-text:latest    0a109f422b47    274 MB    24 hours ago
deepseek-r1:14b            ea35dfe18182    9.0 GB    13 months ago
```

---

## 🔧 故障排查

### 问题 1: Ollama 无法启动

**症状：**
```
❌ Ollama 启动失败
```

**解决：**
```bash
# 1. 检查端口是否被占用
lsof -i :11434

# 2. 查看日志
cat /tmp/ollama.log

# 3. 手动启动测试
ollama serve
```

---

### 问题 2: Embedding 失败

**症状：**
```
Error getting embedding: Connection refused
```

**解决：**
```bash
# 1. 确认 Ollama 运行
ollama list

# 2. 确认模型存在
ollama ls | grep nomic-embed

# 3. 如果模型不存在，拉取
ollama pull nomic-embed-text
```

---

### 问题 3: 开机自启不工作

**症状：**
```
重启后 Ollama 未自动启动
```

**解决：**
```bash
# 1. 检查 LaunchAgent 是否加载
launchctl list | grep ollama

# 2. 重新加载
launchctl unload ~/Library/LaunchAgents/com.ollama.ollama.plist
launchctl load ~/Library/LaunchAgents/com.ollama.ollama.plist

# 3. 检查文件权限
ls -l ~/Library/LaunchAgents/com.ollama.ollama.plist
```

---

## 📝 配置文件说明

### LaunchAgent 配置文件

**位置：** `~/Library/LaunchAgents/com.ollama.ollama.plist`

**关键配置：**
```xml
<key>RunAtLoad</key>
<true/>  <!-- 开机启动 -->

<key>KeepAlive</key>
<true/>  <!-- 崩溃自动重启 -->
```

---

## 🎯 推荐配置

### 最佳实践

1. **配置开机自启**（方式 2）
   - 一劳永逸，无需手动启动
   
2. **使用 main.py**（方式 1）
   - 自动检查，双重保险

3. **监控日志**
   ```bash
   # 定期查看
   tail -f /tmp/ollama.log
   ```

---

## ✅ 当前状态

| 配置项 | 状态 |
|--------|------|
| Ollama 服务 | ✅ 运行中 |
| nomic-embed-text | ✅ 已安装 |
| 开机自启 | ✅ 已配置 |
| 运行时检查 | ✅ 已集成 |
| 启动脚本 | ✅ 已创建 |

---

## 🚀 使用示例

```bash
# 直接使用（会自动检查 Ollama）
python3 main.py status

# 测试 embedding
python3 main.py embedding "修复 Bug" "修复错误"

# 运行分形思考（使用 Ollama embedding）
python3 main.py fractal --limit 10
```

**系统会自动：**
1. ✅ 检查 Ollama 是否运行
2. ✅ 如果未运行，自动启动
3. ✅ 等待启动完成（最多 10 秒）
4. ✅ 使用 Ollama embedding 进行分析

---

**配置完成！Ollama 会自动启动，无需手动干预。** 🎉
