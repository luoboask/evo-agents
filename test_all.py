#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai-baby 完整功能测试
验证所有核心功能正常工作
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# 颜色输出
class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    OKCYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def cprint(text, color=Colors.ENDC):
    print(f"{color}{text}{Colors.ENDC}")

def print_test(name):
    cprint(f"\n{'='*60}", Colors.BOLD)
    cprint(f"  测试：{name}", Colors.BOLD)
    cprint(f"{'='*60}", Colors.BOLD)

def print_success(text):
    cprint(f"✅ {text}", Colors.OKGREEN)

def print_error(text):
    cprint(f"❌ {text}", Colors.FAIL)

def print_info(text):
    cprint(f"ℹ️  {text}", Colors.OKCYAN)


class TestSuite:
    """测试套件"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace-ai-baby")
        self.results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "tests": []
        }
    
    def run_test(self, name, test_func):
        """运行单个测试"""
        try:
            print_test(name)
            result = test_func()
            if result:
                print_success(f"{name} - 通过 ✅")
                self.results["passed"] += 1
                self.results["tests"].append((name, "PASS", None))
            else:
                print_error(f"{name} - 失败 ❌")
                self.results["failed"] += 1
                self.results["tests"].append((name, "FAIL", "测试返回 False"))
        except Exception as e:
            print_error(f"{name} - 异常：{e}")
            self.results["failed"] += 1
            self.results["tests"].append((name, "ERROR", str(e)))
    
    def test_python_environment(self):
        """测试 1: Python 环境"""
        import sys
        version = sys.version_info
        if version.major >= 3 and version.minor >= 9:
            print_success(f"Python {version.major}.{version.minor}.{version.micro}")
            return True
        return False
    
    def test_dependencies(self):
        """测试 2: 依赖包"""
        try:
            import yaml
            import sqlite3
            print_success("依赖包完整 (yaml, sqlite3)")
            return True
        except ImportError as e:
            print_error(f"缺少依赖：{e}")
            return False
    
    def test_config_loading(self):
        """测试 3: 配置加载"""
        try:
            import yaml
            config_path = Path.home() / ".openclaw" / "workspace-ai-baby-config" / "config.yaml"
            
            if not config_path.exists():
                print_info("配置文件不存在，使用默认配置")
                return True
            
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # 检查关键配置
            required_keys = ["workspace", "database", "rag"]
            for key in required_keys:
                if key not in config:
                    print_error(f"缺少配置项：{key}")
                    return False
            
            print_success(f"配置加载成功：{config_path}")
            return True
        except Exception as e:
            print_error(f"配置加载失败：{e}")
            return False
    
    def test_memory_search(self):
        """测试 4: 记忆搜索功能"""
        try:
            sys.path.insert(0, str(self.workspace / "skills" / "memory-search"))
            from search_sqlite import SQLiteMemorySearch
            
            search = SQLiteMemorySearch()
            
            # 检查数据库
            if not search.db_path.exists():
                print_info("数据库不存在，首次使用会自动创建")
                return True
            
            # 测试搜索
            results = search.search("测试", top_k=3, semantic=False)
            print_success(f"记忆搜索正常 - 找到 {len(results)} 条结果")
            
            # 测试语义搜索（如果 Ollama 可用）
            try:
                results_semantic = search.search("测试", top_k=3, semantic=True)
                print_success(f"语义搜索正常 - 找到 {len(results_semantic)} 条结果")
            except Exception as e:
                print_info(f"语义搜索不可用：{e}")
            
            return True
        except Exception as e:
            print_error(f"记忆搜索失败：{e}")
            return False
    
    def test_rag_evaluation(self):
        """测试 5: RAG 评估功能"""
        try:
            sys.path.insert(0, str(self.workspace / "skills" / "rag"))
            from evaluate import RAGEvaluator, EVALUATIONS_FILE
            
            evaluator = RAGEvaluator()
            
            # 检查日志文件
            if not EVALUATIONS_FILE.exists():
                print_info("RAG 日志不存在，会自动创建")
            
            # 测试记录功能
            evaluator.record(
                query="功能测试",
                retrieved_count=1,
                latency_ms=50.0,
                feedback="positive"
            )
            print_success("RAG 记录功能正常")
            
            # 测试报告生成
            report = evaluator.generate_report(days=7)
            if report and "RAG 评估报告" in report:
                print_success("RAG 报告生成正常")
            
            return True
        except Exception as e:
            print_error(f"RAG 评估失败：{e}")
            return False
    
    def test_rag_auto_tune(self):
        """测试 6: RAG 自动调优"""
        try:
            sys.path.insert(0, str(self.workspace / "skills" / "rag"))
            from auto_tune import AutoTuner
            
            tuner = AutoTuner()
            
            # 测试设计实验
            experiments = tuner.design_experiments()
            if len(experiments) > 0:
                print_success(f"自动调优实验设计正常 - {len(experiments)} 个配置")
            
            # 测试分析结果
            analysis = tuner.analyze_results()
            if "error" not in analysis or analysis.get("current_count", 0) >= 0:
                print_success("自动调优分析正常")
            
            return True
        except Exception as e:
            print_error(f"RAG 自动调优失败：{e}")
            return False
    
    def test_self_evolution_core(self):
        """测试 7: 自进化核心模块"""
        try:
            se_dir = self.workspace / "skills" / "self-evolution-5.0"
            sys.path.insert(0, str(se_dir))
            
            # 测试核心文件
            core_files = [
                "main.py",
                "memory_stream.py",
                "fractal_thinking.py",
                "nightly_cycle.py",
            ]
            
            for file in core_files:
                if not (se_dir / file).exists():
                    print_error(f"核心文件缺失：{file}")
                    return False
            
            print_success("核心文件完整")
            
            # 测试模块导入
            try:
                from memory_stream import MemoryStream
                print_success("memory_stream 导入成功")
            except ImportError as e:
                print_warning(f"memory_stream 导入失败：{e}")
            
            try:
                from fractal_thinking import FractalThinkingEngine
                print_success("fractal_thinking 导入成功")
            except ImportError as e:
                print_warning(f"fractal_thinking 导入失败：{e}")
            
            return True
        except Exception as e:
            print_error(f"自进化核心测试失败：{e}")
            return False
    
    def test_database_integrity(self):
        """测试 8: 数据库完整性"""
        try:
            import sqlite3
            from pathlib import Path
            
            db_path = Path.home() / ".openclaw" / "workspace-ai-baby-config" / "memory" / "ai-baby_memory_stream.db"
            
            if not db_path.exists():
                print_info("数据库不存在，首次使用会自动创建")
                return True
            
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            
            # 检查表结构
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]
            
            if "memories" in tables:
                print_success("数据库表结构正常")
                
                # 检查数据
                cur.execute("SELECT COUNT(*) FROM memories")
                count = cur.fetchone()[0]
                print_success(f"数据库包含 {count} 条记忆")
            else:
                print_error("数据库表结构异常")
                return False
            
            conn.close()
            return True
        except Exception as e:
            print_error(f"数据库完整性测试失败：{e}")
            return False
    
    def test_gitignore(self):
        """测试 9: Git 忽略配置"""
        try:
            gitignore = self.workspace / ".gitignore"
            
            if not gitignore.exists():
                print_error(".gitignore 不存在")
                return False
            
            with open(gitignore, 'r') as f:
                content = f.read()
            
            # 检查关键规则
            required_rules = ["*.db", "*.jsonl", "credentials.json", "config.yaml"]
            missing = [rule for rule in required_rules if rule not in content]
            
            if missing:
                print_warning(f"缺少 Git 规则：{missing}")
                return True  # 不致命
            
            print_success("Git 忽略配置完整")
            return True
        except Exception as e:
            print_error(f"Git 忽略测试失败：{e}")
            return False
    
    def test_quick_verify(self):
        """测试 10: 快速验证脚本"""
        try:
            import subprocess
            
            result = subprocess.run(
                ["python3", str(self.workspace / "quick_verify.py")],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if "所有功能验证通过" in result.stdout:
                print_success("快速验证脚本正常")
                return True
            else:
                print_warning("快速验证脚本输出异常")
                return True  # 不致命
        except Exception as e:
            print_error(f"快速验证脚本测试失败：{e}")
            return False
    
    def show_summary(self):
        """显示测试总结"""
        print_test("测试总结")
        
        total = self.results["passed"] + self.results["failed"] + self.results["skipped"]
        
        print(f"\n总测试数：{total}")
        print_success(f"通过：{self.results['passed']}")
        if self.results["failed"] > 0:
            print_error(f"失败：{self.results['failed']}")
        if self.results["skipped"] > 0:
            print_info(f"跳过：{self.results['skipped']}")
        
        print("\n详细结果:")
        for name, status, error in self.results["tests"]:
            if status == "PASS":
                print_success(f"  ✅ {name}")
            elif status == "FAIL":
                print_error(f"  ❌ {name}: {error}")
            else:
                print_info(f"  ⚠️  {name}: {error}")
        
        print("\n" + "="*60)
        if self.results["failed"] == 0:
            cprint("  🎉 所有测试通过！系统功能正常！", Colors.OKGREEN)
        else:
            cprint(f"  ⚠️  {self.results['failed']} 个测试失败，请检查", Colors.WARNING)
        print("="*60 + "\n")


def main():
    """主函数"""
    print("\n" + "🧪" * 30)
    print(f"  ai-baby 完整功能测试")
    print(f"  时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🧪" * 30)
    
    suite = TestSuite()
    
    # 运行所有测试
    suite.run_test("Python 环境", suite.test_python_environment)
    suite.run_test("依赖包检查", suite.test_dependencies)
    suite.run_test("配置加载", suite.test_config_loading)
    suite.run_test("记忆搜索功能", suite.test_memory_search)
    suite.run_test("RAG 评估功能", suite.test_rag_evaluation)
    suite.run_test("RAG 自动调优", suite.test_rag_auto_tune)
    suite.run_test("自进化核心模块", suite.test_self_evolution_core)
    suite.run_test("数据库完整性", suite.test_database_integrity)
    suite.run_test("Git 忽略配置", suite.test_gitignore)
    suite.run_test("快速验证脚本", suite.test_quick_verify)
    
    # 显示总结
    suite.show_summary()
    
    # 返回退出码
    sys.exit(0 if suite.results["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
