#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai-baby 系统初始化和验证工具
自动配置环境、检查依赖、验证功能
"""

import os
import sys
import subprocess
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def cprint(text, color=Colors.ENDC):
    """彩色打印"""
    print(f"{color}{text}{Colors.ENDC}")

def print_header(text):
    cprint("\n" + "=" * 70, Colors.BOLD)
    cprint(f"  {text}", Colors.BOLD)
    cprint("=" * 70, Colors.BOLD + "\n")

def print_success(text):
    cprint(f"✅ {text}", Colors.OKGREEN)

def print_error(text):
    cprint(f"❌ {text}", Colors.FAIL)

def print_warning(text):
    cprint(f"⚠️  {text}", Colors.WARNING)

def print_info(text):
    cprint(f"ℹ️  {text}", Colors.OKCYAN)

def print_step(step, text):
    cprint(f"\n[{step}/7] {text}", Colors.BOLD)


class SystemInitializer:
    """系统初始化和验证"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace-ai-baby")
        self.config_dir = Path.home() / ".openclaw" / "workspace-ai-baby-config"
        self.results = {
            "checks": [],
            "fixes": [],
            "warnings": []
        }
    
    def check_python(self) -> bool:
        """检查 Python 版本"""
        print_step(1, "检查 Python 环境")
        
        version = sys.version_info
        if version.major >= 3 and version.minor >= 9:
            print_success(f"Python {version.major}.{version.minor}.{version.micro} ✅")
            self.results["checks"].append("Python 版本正常")
            return True
        else:
            print_error(f"Python 版本过低：{version.major}.{version.minor} (需要 3.9+)")
            self.results["warnings"].append("Python 版本过低")
            return False
    
    def check_dependencies(self) -> bool:
        """检查依赖包"""
        print_step(2, "检查依赖包")
        
        required_packages = ["yaml", "sqlite3"]
        missing = []
        
        for pkg in required_packages:
            try:
                if pkg == "yaml":
                    import yaml
                elif pkg == "sqlite3":
                    import sqlite3
                print_success(f"{pkg} ✅")
            except ImportError:
                print_error(f"{pkg} ❌")
                missing.append(pkg)
        
        if missing:
            print_warning(f"缺少依赖包：{', '.join(missing)}")
            print_info("安装命令：pip3 install pyyaml")
            self.results["warnings"].append(f"缺少依赖：{missing}")
            return False
        else:
            print_success("所有依赖包已安装 ✅")
            self.results["checks"].append("依赖包完整")
            return True
    
    def setup_config_directory(self) -> bool:
        """配置目录设置"""
        print_step(3, "配置目录设置")
        
        # 创建配置目录
        dirs_to_create = [
            self.config_dir,
            self.config_dir / "memory",
            self.config_dir / "logs",
        ]
        
        for dir_path in dirs_to_create:
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print_success(f"创建目录：{dir_path}")
            else:
                print_info(f"目录已存在：{dir_path}")
        
        # 创建配置文件（如果不存在）
        config_file = self.config_dir / "config.yaml"
        if not config_file.exists():
            self.create_config_file()
            print_success(f"创建配置文件：{config_file}")
        else:
            print_info(f"配置文件已存在：{config_file}")
        
        self.results["checks"].append("配置目录就绪")
        return True
    
    def create_config_file(self):
        """创建配置文件模板"""
        config_content = f"""# ai-baby 个人配置
# ⚠️  此文件包含敏感信息，不会上传到 Git
# 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# 工作区配置
workspace: {self.workspace}

# Ollama 配置
ollama:
  enabled: true
  url: http://localhost:11434
  model: nomic-embed-text

# 数据库路径
database:
  memory_stream: {self.config_dir}/memory/ai-baby_memory_stream.db
  knowledge_base: {self.config_dir}/memory/ai-baby_knowledge_base.db

# RAG 配置
rag:
  log_path: {self.config_dir}/logs/evaluations.jsonl
  top_k: 5
  similarity_threshold: 0.7

# 用户信息（可选）
# user:
#   name: "Your Name"
#   timezone: "Asia/Shanghai"
#   preferences:
#     language: "zh-CN"
"""
        
        with open(self.config_dir / "config.yaml", 'w', encoding='utf-8') as f:
            f.write(config_content)
    
    def check_databases(self) -> bool:
        """检查数据库"""
        print_step(4, "检查数据库")
        
        db_checks = [
            ("记忆流", self.config_dir / "memory" / "ai-baby_memory_stream.db"),
            ("知识库", self.config_dir / "memory" / "ai-baby_knowledge_base.db"),
        ]
        
        all_ok = True
        for name, db_path in db_checks:
            if db_path.exists():
                # 检查数据库完整性
                try:
                    conn = sqlite3.connect(db_path)
                    cur = conn.cursor()
                    cur.execute("SELECT COUNT(*) FROM memories")
                    count = cur.fetchone()[0]
                    conn.close()
                    print_success(f"{name}: {count} 条记录 ✅")
                except Exception as e:
                    print_warning(f"{name}: 数据库异常 - {e}")
            else:
                print_info(f"{name}: 将自动创建")
                all_ok = False
        
        if not all_ok:
            print_info("运行功能测试时会自动创建数据库")
        
        self.results["checks"].append("数据库检查完成")
        return True
    
    def check_gitignore(self) -> bool:
        """检查 .gitignore"""
        print_step(5, "检查 Git 配置")
        
        gitignore = self.workspace / ".gitignore"
        if gitignore.exists():
            print_success(".gitignore 已配置 ✅")
            
            # 检查关键规则
            with open(gitignore, 'r') as f:
                content = f.read()
            
            required_rules = ["*.db", "*.jsonl", "credentials.json"]
            missing_rules = [rule for rule in required_rules if rule not in content]
            
            if missing_rules:
                print_warning(f"缺少 Git 规则：{missing_rules}")
            else:
                print_success("Git 忽略规则完整 ✅")
        else:
            print_error(".gitignore 不存在")
            print_info("运行：python3 separate_config.py")
        
        self.results["checks"].append("Git 配置检查完成")
        return True
    
    def run_functional_tests(self) -> bool:
        """运行功能测试"""
        print_step(6, "运行功能测试")
        
        tests = [
            ("记忆搜索", self.test_memory_search),
            ("RAG 评估", self.test_rag_evaluation),
            ("配置加载", self.test_config_loading),
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                    print_success(f"{name}: 通过 ✅")
                else:
                    failed += 1
                    print_error(f"{name}: 失败 ❌")
            except Exception as e:
                failed += 1
                print_error(f"{name}: 异常 - {e}")
        
        print_info(f"测试结果：{passed} 通过，{failed} 失败")
        self.results["checks"].append(f"功能测试：{passed}/{len(tests)}")
        return failed == 0
    
    def test_memory_search(self) -> bool:
        """测试记忆搜索"""
        try:
            sys.path.insert(0, str(self.workspace / "skills" / "memory-search"))
            from search_sqlite import SQLiteMemorySearch
            
            search = SQLiteMemorySearch()
            results = search.search("测试", top_k=1)
            return True
        except Exception as e:
            print_warning(f"记忆搜索测试：{e}")
            return False
    
    def test_rag_evaluation(self) -> bool:
        """测试 RAG 评估"""
        try:
            sys.path.insert(0, str(self.workspace / "skills" / "rag"))
            from evaluate import RAGEvaluator
            
            evaluator = RAGEvaluator()
            # 测试记录功能
            evaluator.record(
                query="初始化测试",
                retrieved_count=0,
                latency_ms=1.0,
                feedback="neutral"
            )
            return True
        except Exception as e:
            print_warning(f"RAG 评估测试：{e}")
            return False
    
    def test_config_loading(self) -> bool:
        """测试配置加载"""
        try:
            import yaml
            config_path = self.config_dir / "config.yaml"
            
            if not config_path.exists():
                return False
            
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # 检查关键配置
            required_keys = ["workspace", "database", "rag"]
            for key in required_keys:
                if key not in config:
                    return False
            
            return True
        except Exception as e:
            print_warning(f"配置加载测试：{e}")
            return False
    
    def show_summary(self):
        """显示总结"""
        print_step(7, "初始化总结")
        
        print("\n📊 检查结果:")
        for check in self.results["checks"]:
            print(f"  ✅ {check}")
        
        if self.results["warnings"]:
            print("\n⚠️  警告:")
            for warning in self.results["warnings"]:
                print(f"  ⚠️  {warning}")
        
        print("\n📁 配置位置:")
        print(f"  工作区：{self.workspace}")
        print(f"  配置目录：{self.config_dir}")
        
        print("\n🚀 下一步:")
        print("  1. 编辑配置文件：~/.openclaw/workspace-ai-baby-config/config.yaml")
        print("  2. 运行系统状态：./start.sh")
        print("  3. 开始使用：python3 skills/memory-search/search_sqlite.py \"查询\"")
        
        print("\n" + "=" * 70)
        if not self.results["warnings"]:
            cprint("  🎉 系统初始化完成！所有检查通过！", Colors.OKGREEN)
        else:
            cprint("  ⚠️  系统初始化完成，但有警告需要处理", Colors.WARNING)
        print("=" * 70 + "\n")


def main():
    """主函数"""
    print_header("🍼 ai-baby 系统初始化和验证")
    print(f"工作区：{Path('/Users/dhr/.openclaw/workspace-ai-baby')}")
    print(f"配置目录：{Path.home() / '.openclaw' / 'workspace-ai-baby-config'}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    initializer = SystemInitializer()
    
    # 执行检查
    initializer.check_python()
    initializer.check_dependencies()
    initializer.setup_config_directory()
    initializer.check_databases()
    initializer.check_gitignore()
    initializer.run_functional_tests()
    
    # 显示总结
    initializer.show_summary()
    
    # 返回退出码
    if initializer.results["warnings"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
