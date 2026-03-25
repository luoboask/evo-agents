#!/usr/bin/env python3
"""
Web 版进化工作台 - Web Dashboard
通过浏览器实时查看进化状态
"""

import json
import os
import sys
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


class EvolutionData:
    """进化数据管理"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.memory_dir = self.workspace / "memory"
        self.learning_dir = self.memory_dir / "learning"
        self.skills_dir = self.workspace / "skills"
        
        self.metrics = {
            "total_interactions": 0,
            "success_rate": 100.0,
            "skills_count": 0,
            "memory_size_mb": 0,
            "health_score": 100,
            "last_update": datetime.now().isoformat()
        }
        
        self.evolution_events = []
        self.logs = []
        
        self._update_data()
    
    def _update_data(self):
        """更新数据"""
        # 技能数量
        self.metrics["skills_count"] = len([d for d in self.skills_dir.iterdir() if d.is_dir()])
        
        # 记忆大小
        total_size = sum(f.stat().st_size for f in self.memory_dir.rglob("*") if f.is_file())
        self.metrics["memory_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        # 读取反思日志
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.learning_dir / f"auto_reflections_{today}.jsonl"
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = [json.loads(line) for line in f if line.strip()]
                self.metrics["total_interactions"] = len(logs)
                if logs:
                    success_count = sum(1 for l in logs if l.get("success"))
                    self.metrics["success_rate"] = round((success_count / len(logs)) * 100, 1)
        
        self.metrics["last_update"] = datetime.now().isoformat()
    
    def get_data(self):
        """获取当前数据"""
        self._update_data()
        return {
            "metrics": self.metrics,
            "skills": self._get_skills_list()
        }
    
    def _get_skills_list(self):
        """获取技能列表"""
        skills = []
        for skill_dir in sorted(self.skills_dir.iterdir()):
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                name = skill_dir.name
                if skill_md.exists():
                    with open(skill_md, 'r') as f:
                        content = f.read()
                        desc = content.split('\n')[0][:50] if content else "No description"
                        skills.append({"name": name, "description": desc})
                else:
                    skills.append({"name": name, "description": "No SKILL.md"})
        return skills


data_manager = EvolutionData()


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器"""
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/':
            self._serve_html()
        elif path == '/api/data':
            self._serve_json(data_manager.get_data())
        elif path == '/api/refresh':
            data_manager._update_data()
            self._serve_json({"status": "refreshed"})
        else:
            self._serve_404()
    
    def _serve_html(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🧬 自我进化工作台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: #16213e;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #0f3460;
        }
        .card h2 {
            color: #e94560;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #0f3460;
        }
        .metric:last-child { border-bottom: none; }
        .metric-value {
            font-weight: bold;
            color: #4ecca3;
        }
        .skill-tag {
            display: inline-block;
            padding: 5px 10px;
            margin: 3px;
            background: #0f3460;
            border-radius: 15px;
            font-size: 0.85em;
        }
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px 30px;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            font-size: 1em;
        }
        .refresh-btn:hover { background: #ff6b6b; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧬 自我进化工作台</h1>
        <p>实时监控 AI 的自我进化过程</p>
    </div>
    
    <div class="grid">
        <div class="card">
            <h2>📊 实时指标</h2>
            <div id="metrics"></div>
        </div>
        <div class="card">
            <h2>🛠️ 技能列表</h2>
            <div id="skills"></div>
        </div>
        <div class="card">
            <h2>🔧 系统状态</h2>
            <div class="metric"><span>记忆系统</span><span style="color:#4ecca3">✅ 运行中</span></div>
            <div class="metric"><span>语义搜索</span><span style="color:#4ecca3">✅ 就绪</span></div>
            <div class="metric"><span>自动反思</span><span style="color:#4ecca3">✅ 启用</span></div>
            <div class="metric"><span>预测维护</span><span style="color:#4ecca3">✅ 运行中</span></div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="refreshData()">🔄 刷新数据</button>
    
    <script>
        function refreshData() {
            fetch('/api/data')
                .then(r => r.json())
                .then(data => updateUI(data));
        }
        
        function updateUI(data) {
            // 更新指标
            const metrics = data.metrics;
            document.getElementById('metrics').innerHTML = `
                <div class="metric"><span>总交互次数</span><span class="metric-value">${metrics.total_interactions}</span></div>
                <div class="metric"><span>成功率</span><span class="metric-value">${metrics.success_rate}%</span></div>
                <div class="metric"><span>技能数量</span><span class="metric-value">${metrics.skills_count}</span></div>
                <div class="metric"><span>记忆大小</span><span class="metric-value">${metrics.memory_size_mb} MB</span></div>
                <div class="metric"><span>健康评分</span><span class="metric-value">${metrics.health_score}/100</span></div>
            `;
            
            // 更新技能
            const skillsHtml = data.skills.map(s => 
                `<span class="skill-tag">${s.name}</span>`
            ).join('');
            document.getElementById('skills').innerHTML = skillsHtml;
        }
        
        // 自动刷新
        refreshData();
        setInterval(refreshData, 5000);
    </script>
</body>
</html>'''