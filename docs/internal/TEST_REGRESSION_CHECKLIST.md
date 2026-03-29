# evo-agents 完整测试回归清单

**版本：** v1.1.0  
**更新日期：** 2026-03-29  
**测试类型：** 完整功能回归

---

## 📋 目录

1. [安装测试](#1-安装测试)
2. [目录结构测试](#2-目录结构测试)
3. [路径系统测试](#3-路径系统测试)
4. [核心功能测试](#4-核心功能测试)
5. [子 Agent 测试](#5-子 agent 测试)
6. [数据隔离测试](#6-数据隔离测试)
7. [维护工具测试](#7-维护工具测试)
8. [文档完整性测试](#8-文档完整性测试)
9. [边界情况测试](#9-边界情况测试)

---

## 1. 安装测试

### 1.1 新安装测试

**测试步骤：**
```bash
# 清理旧 workspace
rm -rf ~/.openclaw/workspace-test-install

# 方式 1: Gitee 安装（国内推荐）
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s test-install

# 方式 2: GitHub 安装（海外）
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s test-install
```

**验证点：**
- [ ] 安装脚本成功下载
- [ ] Gitee/GitHub 源自动选择
- [ ] workspace 创建成功
- [ ] OpenClaw 注册成功
- [ ] .install-config 创建
- [ ] 目录结构完整（memory/, data/, scripts/, skills/）
- [ ] 清理开发文件（.github/, CONTRIBUTING.md 等）
- [ ] libs/memory_hub 保留

**预期结果：**
```
✅ 安装完成！
📊 位置：/Users/dhr/.openclaw/workspace-test-install
```

---

### 1.2 强制重装测试

**测试步骤：**
```bash
# 已存在 workspace 时强制安装
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s test-install --force
```

**验证点：**
- [ ] 检测到 workspace 已存在
- [ ] 清理开发文件
- [ ] 保留用户数据（memory/, data/, public/）
- [ ] 保留用户脚本（scripts/*）
- [ ] 保留用户技能（skills/*）

---

### 1.3 安装源切换测试

**测试步骤：**
```bash
# 测试 Gitee 源
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s test-gitee

# 验证 Git 源
cd ~/.openclaw/workspace-test-gitee
git remote -v
```

**验证点：**
- [ ] Gitee 下载速度快（<10 秒）
- [ ] Git 远程仓库是 Gitee
- [ ] 安装脚本自动选择最优源

---

## 2. 目录结构测试

### 2.1 主 workspace 结构

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-structure
find . -maxdepth 2 -type d | grep -v ".git" | sort
```

**预期结构：**
```
./
./.openclaw
./agents
./config
./data
./data/index
./data/test-structure
./docs
./libs
./libs/memory_hub
./memory
./memory/archive
./memory/monthly
./memory/weekly
./public
./scripts
./scripts/core
./scripts/user
./skills
./skills/memory-search
./skills/rag
./skills/self-evolution
./skills/web-knowledge
```

**验证点：**
- [ ] 所有必需目录存在
- [ ] .gitkeep 文件存在
- [ ] 没有多余文件（LICENSE, README.zh-CN.md 等）

---

### 2.2 skills 目录测试

**测试步骤：**
```bash
ls -la ~/.openclaw/workspace-test-structure/skills/
```

**验证点：**
- [ ] memory-search/ 存在
- [ ] rag/ 存在
- [ ] self-evolution/ 存在
- [ ] web-knowledge/ 存在
- [ ] 没有特定 agent 的技能（如 aura-*, pinterest-* 等）

---

### 2.3 data 目录测试

**测试步骤：**
```bash
ls -la ~/.openclaw/workspace-test-structure/data/
```

**验证点：**
- [ ] .gitkeep 存在
- [ ] index/ 存在
- [ ] test-structure/ 存在（当前 agent 数据）
- [ ] 没有其他 agent 的数据（如 ai-baby/, demo-agent/ 等）

---

## 3. 路径系统测试

### 3.1 path_utils 基础测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-path
python3 << 'EOF'
import sys
sys.path.insert(0, 'scripts/core')
from path_utils import resolve_workspace, resolve_agent_memory, resolve_data_dir

workspace = resolve_workspace()
print(f"Workspace: {workspace}")

memory = resolve_agent_memory(None)
print(f"Memory: {memory}")

data = resolve_data_dir()
print(f"Data: {data}")

# 验证
assert str(workspace).endswith("workspace-test-path"), "Workspace 解析错误"
assert str(memory).endswith("memory"), "Memory 解析错误"
assert str(data).endswith("data"), "Data 解析错误"

print("✅ 所有路径解析正确")
EOF
```

**验证点：**
- [ ] resolve_workspace() 返回正确的 workspace 路径
- [ ] resolve_agent_memory() 返回正确的记忆目录
- [ ] resolve_data_dir() 返回正确的数据目录

---

### 3.2 环境变量覆盖测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-path
EVO_WORKSPACE=/tmp/custom-workspace python3 << 'EOF'
import sys
sys.path.insert(0, 'scripts/core')
from path_utils import resolve_workspace

workspace = resolve_workspace()
print(f"Workspace: {workspace}")
assert str(workspace) == "/tmp/custom-workspace", "环境变量覆盖失败"
print("✅ 环境变量覆盖成功")
EOF
```

**验证点：**
- [ ] EVO_WORKSPACE 环境变量优先
- [ ] WORKSPACE_ROOT 环境变量也支持

---

### 3.3 子 Agent 路径测试

**测试步骤：**
```bash
# 创建子 agent
cd ~/.openclaw/workspace-master-agent
bash scripts/core/add-agent.sh sub-test "Sub Test" 🤖

# 从子 agent 目录测试路径解析
cd agents/sub-test
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, '../../scripts/core')
from path_utils import resolve_workspace

workspace = resolve_workspace()
print(f"当前目录：{Path.cwd()}")
print(f"解析的 workspace: {workspace}")
assert "workspace-master-agent" in str(workspace), "子 agent 路径解析错误"
print("✅ 子 agent 路径解析正确")
EOF
```

**验证点：**
- [ ] 子 agent 能正确解析到父 workspace
- [ ] 路径向上查找逻辑正确
- [ ] 最多查找 5 层目录

---

## 4. 核心功能测试

### 4.1 会话记录测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-func

# 记录事件
python3 scripts/core/session_recorder.py -t event -c "测试事件内容"

# 记录决定
python3 scripts/core/session_recorder.py -t decision -c "测试决定内容"

# 记录学习
python3 scripts/core/session_recorder.py -t learning -c "测试学习内容"

# 验证文件创建
cat memory/$(date +%Y-%m-%d).md
```

**验证点：**
- [ ] memory/YYYY-MM-DD.md 文件创建
- [ ] 内容正确格式化（## 📌 事件，## 🔨 决定，## 📚 学习）
- [ ] 时间戳正确
- [ ] 支持 --agent 参数指定不同 agent

---

### 4.2 记忆索引测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-func

# 全量索引
python3 scripts/core/memory_indexer.py --full

# 增量索引
python3 scripts/core/memory_indexer.py --incremental

# 带语义向量
python3 scripts/core/memory_indexer.py --full --embed

# 验证数据库
ls -la data/index/memory_index.db
```

**验证点：**
- [ ] SQLite 数据库创建
- [ ] FTS5 全文索引创建
- [ ] 语义向量生成（需要 Ollama）
- [ ] 增量索引只处理新文件

---

### 4.3 记忆搜索测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-func

# 关键词搜索
python3 scripts/memory-search/search.py "测试"

# 语义搜索（需要 Ollama）
python3 scripts/memory-search/semantic_search.py "测试查询"

# 统一搜索
python3 scripts/core/unified_search.py "测试"
```

**验证点：**
- [ ] 关键词搜索返回结果
- [ ] 语义搜索返回相关结果
- [ ] 搜索结果包含分数
- [ ] 支持中文分词（jieba）

---

### 4.4 双向同步测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-func

# 双向同步
python3 scripts/core/bridge/bridge_sync.py --agent test-func --days 1

# 只同步到 Markdown
python3 scripts/core/bridge/bridge_sync.py --direction to-md --agent test-func

# 只同步到知识系统
python3 scripts/core/bridge/bridge_sync.py --direction to-kb --agent test-func
```

**验证点：**
- [ ] Markdown → SQLite 同步
- [ ] SQLite → Markdown 同步
- [ ] 不重复同步已存在的数据
- [ ] 支持指定 agent

---

### 4.5 健康检查测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-func

# 健康检查
python3 scripts/core/health_check.py --agent test-func

# 自动修复
python3 scripts/core/health_check.py --agent test-func --fix
```

**验证点：**
- [ ] 检测文件存在性
- [ ] 检测数据库健康
- [ ] 检测索引一致性
- [ ] 提供修复建议

---

### 4.6 自检功能测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-func

# 快速检查
python3 scripts/core/self-check.py

# 完整检查
python3 scripts/core/self-check.py --full

# 自动修复
python3 scripts/core/self-check.py --fix

# 预览修复
python3 scripts/core/self-check.py --fix --dry-run

# JSON 报告
python3 scripts/core/self-check.py --report
```

**验证点：**
- [ ] 检测 25 项完整性检查
- [ ] 自动修复可修复的问题
- [ ] 创建缺失的目录
- [ ] 删除异常目录（scripts/data/, scripts/memory/）
- [ ] 生成 JSON 报告

---

### 4.7 功能激活测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-test-func

# 交互式激活
echo "6" | bash scripts/core/activate-features.sh

# 单独激活
echo "1" | bash scripts/core/activate-features.sh  # 语义搜索
echo "2" | bash scripts/core/activate-features.sh  # 知识库
echo "3" | bash scripts/core/activate-features.sh  # 自进化
echo "4" | bash scripts/core/activate-features.sh  # RAG
echo "5" | bash scripts/core/activate-features.sh  # 定时任务
```

**验证点：**
- [ ] Ollama 检查
- [ ] 模型拉取选项
- [ ] 知识库初始化
- [ ] 自进化系统激活
- [ ] RAG 评估系统就绪
- [ ] 定时任务配置

---

## 5. 子 Agent 测试

### 5.1 创建子 Agent 测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-master-test

# 创建子 agent
bash scripts/core/add-agent.sh sub1 "Sub Agent 1" 🤖
bash scripts/core/add-agent.sh sub2 "Sub Agent 2" 🐱

# 验证目录结构
ls -la agents/
ls -la agents/sub1/
```

**验证点：**
- [ ] agents/sub1/ 目录创建
- [ ] agent/ 配置目录创建
- [ ] memory/ 目录创建
- [ ] sessions/ 目录创建
- [ ] skills/ 符号链接创建（→ ../../skills）
- [ ] scripts/ 空目录创建
- [ ] libs/ 空目录创建

---

### 5.2 子 Agent 脚本运行测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-master-test/agents/sub1

# 从子 agent 目录运行父 workspace 的脚本
python3 ../../scripts/core/session_recorder.py -t event -c "子 agent 测试" --agent sub1

# 验证记忆保存
cat ../../memory/$(date +%Y-%m-%d).md | grep "子 agent 测试"
```

**验证点：**
- [ ] 子 agent 可以运行父 workspace 脚本
- [ ] 路径解析正确
- [ ] 记忆保存在父 workspace
- [ ] --agent 参数正确指定

---

### 5.3 子 Agent 数据隔离测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-master-test

# 为主 agent 记录数据
python3 scripts/core/session_recorder.py -t event -c "主 agent 数据"

# 为子 agent 记录数据
python3 scripts/core/session_recorder.py -t event -c "子 agent 数据" --agent sub1

# 验证数据隔离
ls -la data/
# 应该有 master-test/ 和 sub1/ 两个目录
```

**验证点：**
- [ ] 主 agent 数据在 data/master-test/
- [ ] 子 agent 数据在 data/sub1/
- [ ] 数据完全隔离
- [ ] 不会互相覆盖

---

### 5.4 子 Agent 技能共享测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-master-test/agents/sub1

# 验证 skills 符号链接
ls -la skills
readlink skills

# 从子 agent 使用技能
python3 ../../skills/memory-search/search.py "测试" --agent sub1
```

**验证点：**
- [ ] skills 是符号链接
- [ ] 指向 ../../skills
- [ ] 可以访问所有父 workspace 的技能
- [ ] 技能运行正常

---

## 6. 数据隔离测试

### 6.1 多 Agent 数据隔离

**测试步骤：**
```bash
cd ~/.openclaw/workspace-multi-test

# 创建多个子 agent
bash scripts/core/add-agent.sh agent1 "Agent 1" 1️⃣
bash scripts/core/add-agent.sh agent2 "Agent 2" 2️⃣

# 为每个 agent 记录数据
python3 scripts/core/session_recorder.py -t event -c "Agent 1 数据" --agent agent1
python3 scripts/core/session_recorder.py -t event -c "Agent 2 数据" --agent agent2

# 验证数据隔离
ls -la data/
cat data/agent1/memory/*.db 2>/dev/null || echo "SQLite 数据库存在"
cat data/agent2/memory/*.db 2>/dev/null || echo "SQLite 数据库存在"
```

**验证点：**
- [ ] 每个 agent 有独立的数据目录
- [ ] 数据不会交叉污染
- [ ] 数据库文件独立
- [ ] 记忆文件独立

---

### 6.2 硬编码清理测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-clean-test

# 检查 skills 中的硬编码
grep -rn "ai-baby\|demo-agent\|/Users/dhr" skills/ --include="*.py" --include="*.json" | wc -l

# 应该为 0
```

**验证点：**
- [ ] 没有 ai-baby 硬编码
- [ ] 没有 demo-agent 硬编码
- [ ] 没有 /Users/dhr 硬编码
- [ ] author 字段正确

---

## 7. 维护工具测试

### 7.1 重装/修复测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-reinstall-test

# 选项 1: 仅修复 skills
echo "1" | bash scripts/core/reinstall.sh

# 选项 2: 完全重装（保留数据）
echo "2" | bash scripts/core/reinstall.sh

# 选项 3: 完全重置
echo "3" | bash scripts/core/reinstall.sh
# 输入 YES 确认
```

**验证点：**
- [ ] 备份自动创建
- [ ] skills 更新成功
- [ ] 硬编码自动修复
- [ ] 缓存清理
- [ ] 数据保留（选项 2）
- [ ] 数据删除（选项 3）

---

### 7.2 卸载测试

**测试步骤：**
```bash
# 卸载子 agent
cd ~/.openclaw/workspace-uninstall-test
bash scripts/core/uninstall-agent.sh sub1

# 卸载整个 workspace
bash scripts/core/uninstall-workspace.sh

# 验证 OpenClaw 注销
openclaw agents list | grep "uninstall-test"
# 应该没有输出
```

**验证点：**
- [ ] 子 agent 从 OpenClaw 注销
- [ ] 子 agent 目录删除
- [ ] workspace 从 OpenClaw 注销
- [ ] workspace 目录删除（移到回收站）
- [ ] 会话数据清理

---

### 7.3 备份恢复测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-backup-test

# 创建测试数据
python3 scripts/core/session_recorder.py -t event -c "备份前数据"

# 备份
cp -r ~/.openclaw/workspace-backup-test /tmp/backup-$(date +%Y%m%d)

# 删除数据
rm -rf memory/*.md

# 恢复
cp -r /tmp/backup-*/memory/* memory/

# 验证
cat memory/*.md | grep "备份前数据"
```

**验证点：**
- [ ] 备份成功
- [ ] 恢复成功
- [ ] 数据完整

---

## 8. 文档完整性测试

### 8.1 文档文件测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-doc-test

# 检查必需文档
ls -la docs/
ls -la *.md
```

**验证点：**
- [ ] README.md 存在
- [ ] README.zh-CN.md 存在（已删除，因为 README.md 已包含中文）
- [ ] docs/AGENT_INSTRUCTIONS.md 存在
- [ ] docs/WORKSPACE_RULES.md 存在
- [ ] docs/SELF_CHECK.md 存在
- [ ] docs/SUB_AGENT_TEST.md 存在
- [ ] docs/SCRIPT_DEVELOPMENT.md 存在

---

### 8.2 文档内容测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-doc-test

# 检查文档中的硬编码
grep -rn "ai-baby\|demo-agent\|/Users/dhr" docs/ --include="*.md" | wc -l

# 应该为 0 或只有示例
```

**验证点：**
- [ ] 文档中没有硬编码路径
- [ ] 示例使用通用路径
- [ ] 中英文文档一致

---

## 9. 边界情况测试

### 9.1 空 workspace 测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-empty-test

# 删除所有数据
rm -rf memory/*.md data/*

# 运行自检
python3 scripts/core/self-check.py --fix

# 验证自动创建
ls -la memory/ data/
```

**验证点：**
- [ ] 自检检测缺失文件
- [ ] 自动创建必要目录
- [ ] 自动创建 .gitkeep

---

### 9.2 损坏修复测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-damage-test

# 模拟损坏
rm -rf scripts/core/path_utils.py

# 运行自检
python3 scripts/core/self-check.py

# 应该提示文件缺失
```

**验证点：**
- [ ] 自检检测文件缺失
- [ ] 提供修复建议
- [ ] reinstall.sh 可以恢复

---

### 9.3 权限测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-perm-test

# 修改权限
chmod 555 memory/
chmod 555 data/

# 尝试写入
python3 scripts/core/session_recorder.py -t event -c "测试"

# 应该失败并提示权限错误
```

**验证点：**
- [ ] 权限错误正确处理
- [ ] 清晰的错误提示
- [ ] 不崩溃

---

### 9.4 并发测试

**测试步骤：**
```bash
cd ~/.openclaw/workspace-concurrent-test

# 同时运行多个脚本
python3 scripts/core/session_recorder.py -t event -c "测试 1" &
python3 scripts/core/session_recorder.py -t event -c "测试 2" &
python3 scripts/core/session_recorder.py -t event -c "测试 3" &
wait

# 验证没有数据损坏
cat memory/*.md | grep "测试"
```

**验证点：**
- [ ] 文件锁正常工作
- [ ] 没有数据损坏
- [ ] 所有记录都保存

---

## 📊 测试结果汇总

### 测试覆盖率

| 类别 | 测试项数 | 通过数 | 失败数 | 覆盖率 |
|------|---------|--------|--------|--------|
| 安装测试 | 3 | - | - | - |
| 目录结构 | 3 | - | - | - |
| 路径系统 | 3 | - | - | - |
| 核心功能 | 7 | - | - | - |
| 子 Agent | 4 | - | - | - |
| 数据隔离 | 2 | - | - | - |
| 维护工具 | 3 | - | - | - |
| 文档完整性 | 2 | - | - | - |
| 边界情况 | 4 | - | - | - |
| **总计** | **31** | **-** | **-** | **-** |

---

## ✅ 通过标准

所有测试项必须 100% 通过才能发布新版本。

**关键测试（必须通过）：**
1. ✅ 安装测试
2. ✅ 路径系统测试
3. ✅ 核心功能测试
4. ✅ 数据隔离测试
5. ✅ 子 Agent 测试

---

**最后更新：** 2026-03-29  
**维护者：** evo-agents team
