#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Embedding 模型检查工具

检查:
- Ollama 服务状态
- Embedding 模型安装
- Embedding 功能测试
- 配置文件检查
"""

import json
import sys
import urllib.request
from pathlib import Path


def check_ollama():
    """检查 Ollama 服务"""
    print("\n1️⃣ Ollama 服务状态:")
    try:
        response = urllib.request.urlopen('http://localhost:11434/api/tags', timeout=3)
        data = json.loads(response.read().decode())
        print(f"   ✅ Ollama 服务：运行中")
        print(f"   可用模型:")
        for model in data.get('models', []):
            name = model.get('name', 'unknown')
            size = model.get('size', 0) / 1024 / 1024 / 1024  # GB
            print(f"      - {name} ({size:.2f}GB)")
        return True
    except Exception as e:
        print(f"   ❌ Ollama 服务：未运行或无法访问")
        print(f"      错误：{e}")
        print(f"      启动命令：ollama serve")
        return False


def check_embedding_model():
    """检查 Embedding 模型"""
    print("\n2️⃣ Embedding 模型检查:")
    try:
        response = urllib.request.urlopen('http://localhost:11434/api/tags', timeout=3)
        data = json.loads(response.read().decode())
        models = [m.get('name', '') for m in data.get('models', [])]
        
        embedding_models = [m for m in models if 'embed' in m.lower()]
        
        if embedding_models:
            print(f"   ✅ 已安装 Embedding 模型:")
            for model in embedding_models:
                print(f"      - {model}")
            
            if 'nomic-embed-text' in models or 'nomic-embed-text:latest' in models:
                print(f"   ✅ nomic-embed-text：已安装")
                return True
            else:
                print(f"   ⚠️  nomic-embed-text：未安装")
                print(f"      安装命令：ollama pull nomic-embed-text")
                return False
        else:
            print(f"   ❌ 未找到 Embedding 模型")
            print(f"      安装命令：ollama pull nomic-embed-text")
            return False
    except Exception as e:
        print(f"   ❌ 无法检查模型：{e}")
        return False


def test_embedding():
    """测试 Embedding 功能"""
    print("\n3️⃣ Embedding 功能测试:")
    try:
        test_text = "这是一个测试文本"
        payload = {
            "model": "nomic-embed-text",
            "prompt": test_text
        }
        
        req = urllib.request.Request(
            'http://localhost:11434/api/embeddings',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode())
        
        if 'embedding' in data:
            embedding = data['embedding']
            print(f"   ✅ Embedding 生成成功")
            print(f"      输入文本：{test_text}")
            print(f"      向量维度：{len(embedding)}")
            print(f"      前 5 个值：{[round(x, 4) for x in embedding[:5]]}")
            return True
        else:
            print(f"   ❌ Embedding 生成失败：{data}")
            return False
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"   ❌ 模型不存在：nomic-embed-text")
            print(f"      请先安装：ollama pull nomic-embed-text")
        else:
            print(f"   ❌ HTTP 错误：{e.code}")
        return False
    except Exception as e:
        print(f"   ❌ 测试失败：{e}")
        return False


def check_config():
    """检查配置文件"""
    print("\n4️⃣ 配置文件检查:")
    config_paths = [
        Path.home() / '.openclaw' / 'workspace-ai-baby-config' / 'config.yaml',
        Path('config/config.yaml'),
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            print(f"   ✅ 配置文件：{config_path}")
            try:
                import yaml
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                embedding_config = config.get('embedding', {})
                if embedding_config:
                    print(f"      模型：{embedding_config.get('model', 'N/A')}")
                    print(f"      URL: {embedding_config.get('ollama_url', 'N/A')}")
            except Exception as e:
                print(f"      ⚠️  读取失败：{e}")
            return True
    
    print(f"   ⚠️  未找到配置文件")
    return False


def main():
    """主函数"""
    print("=" * 70)
    print("🔍 Embedding 模型检查")
    print("=" * 70)
    
    ollama_ok = check_ollama()
    if not ollama_ok:
        print("\n❌ Ollama 服务未运行，无法继续检查")
        sys.exit(1)
    
    model_ok = check_embedding_model()
    if not model_ok:
        print("\n❌ Embedding 模型未安装")
        sys.exit(1)
    
    test_ok = test_embedding()
    config_ok = check_config()
    
    print("\n" + "=" * 70)
    print("📊 检查总结")
    print("=" * 70)
    print(f"   Ollama 服务：{'✅ 正常' if ollama_ok else '❌ 异常'}")
    print(f"   Embedding 模型：{'✅ 已安装' if model_ok else '❌ 未安装'}")
    print(f"   功能测试：{'✅ 通过' if test_ok else '❌ 失败'}")
    print(f"   配置文件：{'✅ 存在' if config_ok else '⚠️  未找到'}")
    
    if all([ollama_ok, model_ok, test_ok]):
        print("\n✅ Embedding 系统运行正常！")
        sys.exit(0)
    else:
        print("\n⚠️  发现问题，请根据上述提示修复")
        sys.exit(1)


if __name__ == '__main__':
    main()
