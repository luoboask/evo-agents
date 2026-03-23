# 个人配置 - 不包含在 Git 中

**位置：** `~/.openclaw/workspace-ai-baby-config/` (Git 忽略)

---

## 📁 目录结构

```
~/.openclaw/workspace-ai-baby-config/
├── config.yaml              # 个人配置（API keys、数据库路径等）
├── credentials.json         # 敏感凭证（API 密钥、密码等）
├── user_profile.json        # 用户信息
├── memory/                  # 个人记忆数据库
│   ├── ai-baby_memory_stream.db
│   └── ai-baby_knowledge_base.db
└── logs/                    # 日志文件
    └── evaluations.jsonl
```

---

## 🔐 敏感信息清单

### 不包含在 Git 中的内容

1. **API 密钥和凭证**
   - AIWay API Key
   - Ollama 配置
   - 其他第三方服务密钥

2. **个人数据库**
   - 记忆流数据库
   - 知识库数据库
   - RAG 评估日志

3. **用户个人信息**
   - 姓名、联系方式
   - 个人偏好
   - 私人记忆

4. **日志文件**
   - 评估日志
   - 运行日志
   - 调试信息

---

## 📝 配置模板

### config.yaml.example (在 Git 中)

```yaml
# 工作区配置（公开）
workspace: /Users/dhr/.openclaw/workspace-ai-baby

# Ollama 配置（示例）
ollama:
  enabled: true
  url: http://localhost:11434
  model: nomic-embed-text

# RAG 配置（示例）
rag:
  top_k: 5
  similarity_threshold: 0.7
```

### config.yaml (本地，Git 忽略)

```yaml
# 工作区配置
workspace: /Users/dhr/.openclaw/workspace-ai-baby

# 个人配置（敏感）
ollama:
  enabled: true
  url: http://localhost:11434
  model: nomic-embed-text
  api_key: "your-api-key-here"  # ⚠️ 敏感

# 数据库路径（个人）
database:
  memory_stream: ~/.openclaw/workspace-ai-baby-config/memory/ai-baby_memory_stream.db
  knowledge_base: ~/.openclaw/workspace-ai-baby-config/memory/ai-baby_knowledge_base.db

# RAG 配置
rag:
  top_k: 5
  similarity_threshold: 0.7
  log_path: ~/.openclaw/workspace-ai-baby-config/logs/evaluations.jsonl

# 用户信息
user:
  name: "Your Name"
  timezone: "Asia/Shanghai"
  preferences:
    language: "zh-CN"
    voice: "Nova"
```

---

## 🔧 使用方法

### 1. 首次设置

```bash
# 创建个人配置目录
mkdir -p ~/.openclaw/workspace-ai-baby-config/{memory,logs}

# 复制配置模板
cp config.yaml.example ~/.openclaw/workspace-ai-baby-config/config.yaml

# 编辑个人配置
nano ~/.openclaw/workspace-ai-baby-config/config.yaml
```

### 2. 代码中加载配置

```python
from pathlib import Path
import yaml

# 加载个人配置（Git 忽略）
config_paths = [
    Path.home() / ".openclaw" / "workspace-ai-baby-config" / "config.yaml",
    Path("config.yaml"),  # fallback 到公开配置
]

config = {}
for config_path in config_paths:
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        break

# 使用配置
database_path = config.get('database', {}).get('memory_stream')
api_key = config.get('ollama', {}).get('api_key')
```

### 3. 环境变量（可选）

```bash
# ~/.bashrc 或 ~/.zshrc
export AI_BABY_CONFIG_PATH=~/.openclaw/workspace-ai-baby-config
export AI_BABY_DB_PATH=~/.openclaw/workspace-ai-baby-config/memory
export AIWAY_API_KEY="your-api-key-here"
```

---

## 📂 Git 忽略规则

创建 `.gitignore` 文件：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# 个人配置（敏感）
config.yaml
credentials.json
user_profile.json
*.db
*.sqlite
*.jsonl

# 日志
logs/
*.log

# 系统
.DS_Store
Thumbs.db
*.swp
*.swo
*~

# IDE
.vscode/
.idea/
*.iml

# 个人配置目录（整个目录）
~/.openclaw/workspace-ai-baby-config/
```

---

## 🔄 迁移现有数据

如果已有数据在 Git 目录中：

```bash
# 1. 创建新目录
mkdir -p ~/.openclaw/workspace-ai-baby-config/{memory,logs}

# 2. 移动敏感文件
mv memory/*.db ~/.openclaw/workspace-ai-baby-config/memory/
mv skills/rag/logs/*.jsonl ~/.openclaw/workspace-ai-baby-config/logs/
mv skills/aiway/credentials.json ~/.openclaw/workspace-ai-baby-config/

# 3. 创建符号链接（可选）
ln -s ~/.openclaw/workspace-ai-baby-config/memory memory/data
ln -s ~/.openclaw/workspace-ai-baby-config/logs skills/rag/logs

# 4. 从 Git 历史中删除（谨慎！）
git rm --cached memory/*.db
git rm --cached skills/rag/logs/*.jsonl
git rm --cached skills/aiway/credentials.json
```

---

## 🛡️ 安全最佳实践

### 1. 配置分离
- ✅ 代码和配置分离
- ✅ 公开模板和个人数据分离
- ✅ 使用符号链接或配置路径

### 2. Git 安全
- ✅ 完善的 `.gitignore`
- ✅ 提交前检查敏感文件
- ✅ 使用 `git rm --cached` 清理历史

### 3. 凭证管理
- ✅ 使用环境变量存储密钥
- ✅ 不硬编码在代码中
- ✅ 定期轮换 API 密钥

### 4. 备份策略
- ✅ 定期备份个人配置目录
- ✅ 加密敏感备份
- ✅ 多地点备份

---

## 📋 检查清单

### 提交前检查

```bash
# 检查是否有敏感文件
git status

# 查看将要提交的内容
git diff --cached

# 使用工具检查
git-secrets --scan
```

### 配置验证

```bash
# 测试配置加载
python3 -c "
from pathlib import Path
import yaml
config_path = Path.home() / '.openclaw' / 'workspace-ai-baby-config' / 'config.yaml'
if config_path.exists():
    print('✅ 个人配置存在')
else:
    print('⚠️  个人配置不存在')
"
```

---

## 🔍 常见问题

### Q: 如果不小心提交了敏感信息怎么办？

**A:** 
1. 立即撤销提交：`git reset --soft HEAD~1`
2. 从历史中删除：`git filter-branch` 或 BFG Repo-Cleaner
3. 轮换泄露的密钥
4. 检查 Git 历史：`git log -p -- credentials.json`

### Q: 如何在多设备间同步配置？

**A:**
- 使用加密的云存储（iCloud、1Password 等）
- 不要直接同步到 Git
- 每个设备单独配置

### Q: 团队协作时怎么处理？

**A:**
- 每个人有自己的配置文件
- 共享 `config.yaml.example` 模板
- 使用环境变量管理团队密钥

---

## 📚 参考资源

- [Git Secrets](https://github.com/awslabs/git-secrets) - 防止提交敏感信息
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) - 清理 Git 历史
- [12-Factor App Config](https://12factor.net/config) - 配置最佳实践

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23  
**状态：** ✅ 配置分离方案
