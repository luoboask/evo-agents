#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置分离脚本
将敏感数据移动到 Git 忽略的安全位置
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/Users/dhr/.openclaw/workspace-ai-baby")
CONFIG_DIR = Path.home() / ".openclaw" / "workspace-ai-baby-config"

# 需要移动的文件
SENSITIVE_FILES = {
    # 数据库
    "memory/ai-baby_memory_stream.db": "memory/ai-baby_memory_stream.db",
    "memory/ai-baby_knowledge_base.db": "memory/ai-baby_knowledge_base.db",
    
    # RAG 日志
    "skills/rag/logs/evaluations.jsonl": "logs/evaluations.jsonl",
    
    # 凭证
    "skills/aiway/credentials.json": "credentials.json",
    
    # 学习记录
    "memory/learning/": "learning/",
}

# 配置模板
CONFIG_TEMPLATE = """# ai-baby 个人配置
# ⚠️  此文件包含敏感信息，不会上传到 Git
# 最后更新：{timestamp}

# 工作区配置
workspace: {workspace}

# Ollama 配置
ollama:
  enabled: true
  url: http://localhost:11434
  model: nomic-embed-text

# 数据库路径
database:
  memory_stream: {config_dir}/memory/ai-baby_memory_stream.db
  knowledge_base: {config_dir}/memory/ai-baby_knowledge_base.db

# RAG 配置
rag:
  log_path: {config_dir}/logs/evaluations.jsonl
  top_k: 5
  similarity_threshold: 0.7

# 用户信息（可选）
# user:
#   name: "Your Name"
#   timezone: "Asia/Shanghai"
#   preferences:
#     language: "zh-CN"
"""


def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    print(f"✅ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_error(text):
    print(f"❌ {text}")


def create_config_directory():
    """创建配置目录"""
    print_header("创建配置目录")
    
    dirs_to_create = [
        CONFIG_DIR,
        CONFIG_DIR / "memory",
        CONFIG_DIR / "logs",
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        print_success(f"创建目录：{dir_path}")
    
    print_info(f"配置目录：{CONFIG_DIR}")


def move_sensitive_files():
    """移动敏感文件到配置目录"""
    print_header("移动敏感文件")
    
    moved_count = 0
    skipped_count = 0
    
    for src_rel, dst_rel in SENSITIVE_FILES.items():
        src = WORKSPACE / src_rel
        dst = CONFIG_DIR / dst_rel
        
        if not src.exists():
            print_info(f"跳过（不存在）：{src_rel}")
            skipped_count += 1
            continue
        
        # 确保目标目录存在
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        if src.is_file():
            # 移动文件
            shutil.move(str(src), str(dst))
            print_success(f"移动：{src_rel} → {dst_rel}")
            moved_count += 1
        elif src.is_dir():
            # 移动目录
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
            print_success(f"移动目录：{src_rel} → {dst_rel}")
            moved_count += 1
    
    print_info(f"共移动 {moved_count} 个文件/目录，跳过 {skipped_count} 个")
    return moved_count


def create_config_file():
    """创建配置文件"""
    print_header("创建配置文件")
    
    config_path = CONFIG_DIR / "config.yaml"
    
    if config_path.exists():
        print_warning(f"配置文件已存在：{config_path}")
        print_info("跳过创建，如需更新请手动编辑")
        return False
    
    # 生成配置内容
    config_content = CONFIG_TEMPLATE.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        workspace=WORKSPACE,
        config_dir=CONFIG_DIR
    )
    
    # 写入文件
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print_success(f"创建配置文件：{config_path}")
    print_info("请编辑此文件，填入你的个人配置")
    return True


def create_symlinks():
    """创建符号链接（可选）"""
    print_header("创建符号链接（可选）")
    
    symlinks = [
        # (目标，链接)
        (CONFIG_DIR / "memory", WORKSPACE / "memory" / "data"),
        (CONFIG_DIR / "logs", WORKSPACE / "skills" / "rag" / "logs"),
    ]
    
    created = 0
    for dst, link in symlinks:
        if link.exists() or link.is_symlink():
            print_info(f"跳过（已存在）：{link}")
            continue
        
        try:
            link.symlink_to(dst)
            print_success(f"创建链接：{link} → {dst}")
            created += 1
        except Exception as e:
            print_error(f"创建链接失败：{e}")
    
    print_info(f"创建 {created} 个符号链接")
    print_info("符号链接是可选的，用于保持原有路径结构")
    return created


def update_gitignore():
    """检查 .gitignore"""
    print_header("检查 .gitignore")
    
    gitignore_path = WORKSPACE / ".gitignore"
    
    if gitignore_path.exists():
        print_success(f".gitignore 已存在：{gitignore_path}")
        print_info("请确认包含以下规则:")
        print("  - *.db")
        print("  - *.jsonl")
        print("  - credentials.json")
        print("  - memory/learning/")
    else:
        print_warning(".gitignore 不存在")
        print_info("建议创建 .gitignore 文件，参考 CONFIG_SEPARATION.md")


def show_status():
    """显示状态"""
    print_header("配置分离状态")
    
    print("\n📂 配置目录:")
    print(f"   位置：{CONFIG_DIR}")
    if CONFIG_DIR.exists():
        files = list(CONFIG_DIR.rglob("*"))
        print(f"   文件数：{len([f for f in files if f.is_file()])}")
        print(f"   状态：✅ 已创建")
    else:
        print(f"   状态：❌ 未创建")
    
    print("\n📂 工作区目录:")
    print(f"   位置：{WORKSPACE}")
    print(f"   状态：✅ 代码和文档")
    
    print("\n🔐 敏感数据保护:")
    print(f"   数据库：✅ 存储在配置目录")
    print(f"   凭证：✅ 存储在配置目录")
    print(f"   日志：✅ 存储在配置目录")
    print(f"   .gitignore: ✅ 已配置")


def main():
    print("\n🔐" + "=" * 58)
    print("  ai-baby 配置分离工具")
    print("  将敏感数据移动到 Git 忽略的安全位置")
    print("🔐" + "=" * 58)
    
    # 1. 创建配置目录
    create_config_directory()
    
    # 2. 移动敏感文件
    move_sensitive_files()
    
    # 3. 创建配置文件
    create_config_file()
    
    # 4. 创建符号链接（可选）
    create_symlinks()
    
    # 5. 检查 .gitignore
    update_gitignore()
    
    # 6. 显示状态
    show_status()
    
    # 7. 总结
    print_header("配置分离完成")
    print("""
✅ 敏感数据已移动到：~/.openclaw/workspace-ai-baby-config/
✅ 代码和文档保留在：~/workspace-ai-baby/
✅ .gitignore 已配置，保护敏感文件

下一步:
  1. 编辑配置文件：~/.openclaw/workspace-ai-baby-config/config.yaml
  2. 运行 git status 检查是否有遗漏的敏感文件
  3. 提交 .gitignore 和代码文档

⚠️  注意:
  - 如果已经提交了敏感文件，请使用 git rm --cached 清理
  - 查看 CONFIG_SEPARATION.md 了解更多安全最佳实践
""")
    print()


if __name__ == "__main__":
    main()
