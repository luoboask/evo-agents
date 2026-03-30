#!/bin/bash
# 初始化 Agent 数据目录和数据库
# 用法：./init-agent-data.sh agent-name

set -e

AGENT_NAME="${1:-}"

if [ -z "$AGENT_NAME" ]; then
    echo "用法：$0 <agent-name>"
    echo "示例：$0 my-agent"
    exit 1
fi

WORKSPACE_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DATA_DIR="$WORKSPACE_ROOT/data/$AGENT_NAME/memory"

echo "╔══════════════════════════════════════════════════╗"
echo "║     初始化 Agent 数据                               ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "📦 Agent: $AGENT_NAME"
echo "📁 数据目录：$DATA_DIR"
echo ""

# 创建目录
echo "📁 创建目录..."
mkdir -p "$DATA_DIR"
echo "   ✅ 完成"

# 初始化数据库
echo "🗄️  初始化数据库..."
cd "$WORKSPACE_ROOT"
python3 << PYEOF
import sqlite3
from pathlib import Path

db_dir = Path("$DATA_DIR")
db_dir.mkdir(parents=True, exist_ok=True)

# 创建记忆流数据库
stream_db = db_dir / "memory_stream.db"
conn = sqlite3.connect(str(stream_db))
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    content TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    importance REAL DEFAULT 5.0
)
''')
conn.commit()
conn.close()
print(f"   ✅ 创建 memory_stream.db")

# 创建知识库数据库
kb_db = db_dir / "knowledge_base.db"
conn = sqlite3.connect(str(kb_db))
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    domain TEXT,
    content TEXT,
    insight TEXT
)
''')
conn.commit()
conn.close()
print(f"   ✅ 创建 knowledge_base.db")

print("\n✅ Agent 数据库初始化完成！")
PYEOF

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║     ✅ 初始化完成！                               ║"
echo "╚══════════════════════════════════════════════════╝"
