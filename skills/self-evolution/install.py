#!/usr/bin/env python3
"""
自进化系统 v5.0 - 自动安装脚本

自动完成：
1. 检查 Python 和 SQLite3
2. 创建配置文件
3. 初始化目录结构
4. 创建空数据库
5. 验证安装
"""

import os
import sys
import sqlite3
from pathlib import Path
import sys

# 添加 libs 到路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "libs"))
from path_utils import resolve_workspace, resolve_data_dir
from datetime import datetime


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 50)
    print(f"🚀 {text}")
    print("=" * 50)


def print_success(text):
    """打印成功信息"""
    print(f"✅ {text}")


def print_error(text):
    """打印错误信息"""
    print(f"❌ {text}")


def print_info(text):
    """打印提示信息"""
    print(f"ℹ️  {text}")


def check_python():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} 已安装")
        return True
    else:
        print_error(f"Python 版本过低：{version.major}.{version.minor}.{version.micro}")
        print_info("需要 Python 3.9 或更高版本")
        return False


def check_sqlite3():
    """检查 SQLite3"""
    try:
        import sqlite3
        version = sqlite3.sqlite_version
        print_success(f"SQLite3 {version} 已安装")
        return True
    except ImportError:
        print_error("SQLite3 未安装")
        return False


def create_config():
    """创建配置文件"""
    config_file = Path(__file__).parent / 'config.yaml'
    config_template = Path(__file__).parent / 'config.yaml.example'
    
    if config_file.exists():
        print_info(f"配置文件已存在：{config_file}")
        return True
    
    # 获取用户 home 目录
    home = Path.home()
    workspace = home / '.openclaw' / 'workspace'
    
    if config_template.exists():
        # 读取模板并替换 workspace
        content = config_template.read_text(encoding='utf-8')
        content = content.replace(
            'workspace: /your/path/to/workspace',
            f'workspace: {workspace}'
        )
        
        config_file.write_text(content, encoding='utf-8')
        print_success(f"创建配置文件：{config_file}")
        return True
    else:
        # 创建默认配置
        default_config = f"""# 自进化系统 v5.0 配置文件
# 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# 工作目录（数据库和记忆文件将创建在此）
workspace: {workspace}

# Ollama 配置（可选）
ollama:
  enabled: false
  url: http://localhost:11434
  model: nomic-embed-text

# 记忆压缩配置
memory:
  compress_after_days: 7
  keep_high_importance: 7.0
  target_compression_rate: 0.49

# 模式识别阈值
patterns:
  recurring_bug_threshold: 2
  feature_bloat_threshold: 3
  min_similarity: 0.35

# 夜间循环配置
nightly:
  enabled: true
  max_learning_files: 30
  max_log_size_mb: 100

# 分形思考配置
fractal:
  default_limit: 10
  verbose_report: true
"""
        config_file.write_text(default_config, encoding='utf-8')
        print_success(f"创建配置文件：{config_file}")
        return True


def create_directories():
    """创建目录结构"""
    home = Path.home()
    workspace = home / '.openclaw' / 'workspace'
    
    dirs = [
        workspace,
        workspace / 'memory',
        workspace / 'memory' / 'vector_db',
        workspace / 'evolution',
    ]
    
    for dir_path in dirs:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print_success(f"创建目录：{dir_path}")
        else:
            print_info(f"目录已存在：{dir_path}")
    
    return True


def create_databases():
    """创建空数据库"""
    home = Path.home()
    workspace = home / '.openclaw' / 'workspace'
    
    databases = {
        workspace / 'memory' / 'memory_stream.db': '''
            -- 记忆流数据库
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance REAL DEFAULT 5.0,
                tags TEXT,
                embedding BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type);
            CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at);
        ''',
        workspace / 'memory' / 'knowledge_base.db': '''
            -- 知识库数据库
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                domain TEXT,
                subtopic TEXT,
                content TEXT NOT NULL,
                insight TEXT,
                thinking TEXT,
                key_point TEXT,
                difficulty INTEGER,
                time_spent INTEGER,
                learning_type TEXT,
                outcome TEXT
            );
            
            CREATE INDEX IF NOT EXISTS idx_domain ON knowledge(domain);
            CREATE INDEX IF NOT EXISTS idx_timestamp ON knowledge(timestamp);
        ''',
        workspace / 'evolution' / 'evolution.db': '''
            -- 进化事件数据库
            CREATE TABLE IF NOT EXISTS evolution_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_event_type ON evolution_events(event_type);
            CREATE INDEX IF NOT EXISTS idx_created_at ON evolution_events(created_at);
        ''',
    }
    
    for db_path, schema in databases.items():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.executescript(schema)
            conn.commit()
            conn.close()
            
            size_mb = db_path.stat().st_size / 1024 / 1024
            print_success(f"创建数据库：{db_path} ({size_mb:.2f}MB)")
        except Exception as e:
            print_error(f"创建数据库失败：{db_path}")
            print_error(f"错误：{e}")
            return False
    
    return True


def verify_installation():
    """验证安装"""
    print_header("验证安装")
    
    home = Path.home()
    workspace = home / '.openclaw' / 'workspace'
    
    checks = [
        ("配置文件", workspace.parent / 'skills' / 'self-evolution' / 'config.yaml'),
        ("记忆流数据库", workspace / 'memory' / 'memory_stream.db'),
        ("知识库数据库", workspace / 'memory' / 'knowledge_base.db'),
        ("进化事件数据库", workspace / 'evolution' / 'evolution.db'),
    ]
    
    all_ok = True
    for name, path in checks:
        if path.exists():
            print_success(f"{name}: {path}")
        else:
            print_error(f"{name} 不存在：{path}")
            all_ok = False
    
    return all_ok


def print_next_steps():
    """打印下一步指引"""
    print_header("安装完成！下一步")
    
    print("""
📝 配置（可选）:
   编辑 config.yaml 调整配置
   位置：~/.openclaw/workspace/skills/self-evolution/config.yaml

🔍 查看系统状态:
   cd ~/.openclaw/workspace/skills/self-evolution
   python3 main.py status

📝 记录第一个事件:
   python3 main.py evolve --type KNOWLEDGE_GAINED --content "系统安装完成"

⏰ 配置定时任务（可选）:
   crontab -e
   添加：0 2 * * * cd ~/.openclaw/workspace/skills/self-evolution && python3 main.py nightly

📚 阅读文档:
   - INSTALL.md - 安装指南（本文档）
   - INITIAL_SETUP.md - 初始化和使用指南
   - ARCHITECTURE.md - 系统架构详解
""")


def main():
    """主函数"""
    print_header("自进化系统 v5.0 - 安装程序")
    print_info(f"安装时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"目标目录：{Path.home()}/.openclaw/workspace")
    
    # 检查依赖
    print_header("检查依赖")
    checks = [
        ("Python 3.9+", check_python()),
        ("SQLite3", check_sqlite3()),
    ]
    
    if not all(result for _, result in checks):
        print_error("依赖检查失败，请安装缺失的依赖后重试")
        sys.exit(1)
    
    # 创建配置和目录
    print_header("创建配置文件")
    create_config()
    
    print_header("创建目录结构")
    create_directories()
    
    print_header("创建数据库")
    if not create_databases():
        print_error("数据库创建失败")
        sys.exit(1)
    
    # 验证安装
    if not verify_installation():
        print_error("安装验证失败")
        sys.exit(1)
    
    # 打印下一步
    print_next_steps()
    
    print("\n" + "=" * 50)
    print("🎉 安装成功！开始你的自进化之旅吧！")
    print("=" * 50 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  安装已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 安装失败：{e}")
        print("\n请检查错误信息，或手动安装（参考 INSTALL.md）")
        sys.exit(1)
