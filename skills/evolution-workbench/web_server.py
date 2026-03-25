#!/usr/bin/env python3
"""
Web 服务器 - 提供动态数据 API 和前端界面
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class EvolutionWebHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器"""
    
    def __init__(self, *args, **kwargs):
        self.db_path = Path(__file__).parent / 'evolution.db'
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理 GET 请求"""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == '/' or path == '/index.html':
            self._serve_html()
        elif path == '/api/dashboard':
            self._serve_dashboard_data()
        elif path == '/api/instances':
            self._serve_instances()
        elif path == '/api/bugs':
            self._serve_bugs()
        elif path == '/api/predictions':
            self._serve_predictions()
        elif path == '/api/events':
            self._serve_events()
        elif path == '/api/intelligence':
            self._serve_intelligence()
        elif path == '/api/stats':
            self._serve_stats()
        else:
            self._serve_404()
    
    def _serve_html(self):
        """服务前端页面"""
        html = self._get_html_content()
        self._send_response(200, 'text/html', html)
    
    def _serve_dashboard_data(self):
        """服务仪表板数据"""
        data = self._get_dashboard_data()
        self._send_response(200, 'application/json', json.dumps(data, ensure_ascii=False))
    
    def _serve_instances(self):
        """服务实例数据"""
        data = self._query_db('SELECT * FROM instances ORDER BY created_at DESC LIMIT 10')
        self._send_response(200, 'application/json', json.dumps(data, ensure_ascii=False, default=str))
    
    def _serve_bugs(self):
        """服务 Bug 数据"""
        data = self._query_db('SELECT * FROM bugs WHERE fixed = 0 ORDER BY timestamp DESC LIMIT 10')
        self._send_response(200, 'application/json', json.dumps(data, ensure_ascii=False, default=str))
    
    def _serve_predictions(self):
        """服务预测数据"""
        data = self._query_db('SELECT * FROM predictions WHERE fulfilled = 0 ORDER BY timestamp DESC LIMIT 10')
        self._send_response(200, 'application/json', json.dumps(data, ensure_ascii=False, default=str))
    
    def _serve_events(self):
        """服务事件数据"""
        data = self._query_db('SELECT * FROM evolution_events ORDER BY timestamp DESC LIMIT 20')
        self._send_response(200, 'application/json', json.dumps(data, ensure_ascii=False, default=str))
    
    def _serve_intelligence(self):
        """服务智能评分数据"""
        data = self._query_db('SELECT * FROM intelligence_scores ORDER BY timestamp DESC LIMIT 1')
        self._send_response(200, 'application/json', json.dumps(data, ensure_ascii=False, default=str))
    
    def _serve_stats(self):
        """服务统计数据"""
        stats = self._get_stats()
        self._send_response(200, 'application/json', json.dumps(stats, ensure_ascii=False))
    
    def _serve_404(self):
        """404 页面"""
        self._send_response(404, 'text/plain', 'Not Found')
    
    def _send_response(self, code, content_type, content):
        """发送响应"""
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if isinstance(content, str):
            content = content.encode('utf-8')
        self.wfile.write(content)
    
    def _query_db(self, query, params=()):
        """查询数据库"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def _get_stats(self):
        """获取统计数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # 实例统计
            cursor.execute('SELECT status, COUNT(*) FROM instances GROUP BY status')
            stats['instances'] = dict(cursor.fetchall())
            
            # Bug 统计
            cursor.execute('SELECT severity, COUNT(*) FROM bugs WHERE fixed = 0 GROUP BY severity')
            stats['bugs'] = dict(cursor.fetchall())
            
            # 预测
            cursor.execute('SELECT COUNT(*) FROM predictions WHERE fulfilled = 0')
            stats['pending_predictions'] = cursor.fetchone()[0]
            
            # 今日事件
            cursor.execute("SELECT COUNT(*) FROM evolution_events WHERE date(timestamp) = date('now')")
            stats['today_events'] = cursor.fetchone()[0]
            
            return stats
    
    def _get_dashboard_data(self):
        """获取仪表板完整数据"""
        return {
            'timestamp': datetime.now().isoformat(),
            'intelligence': self._query_db('SELECT * FROM intelligence_scores ORDER BY timestamp DESC LIMIT 1')[0] if self._query_db('SELECT * FROM intelligence_scores ORDER BY timestamp DESC LIMIT 1') else {},
            'instances': self._query_db('SELECT * FROM instances ORDER BY created_at DESC LIMIT 5'),
            'bugs': self._query_db('SELECT * FROM bugs WHERE fixed = 0 ORDER BY timestamp DESC LIMIT 5'),
            'predictions': self._query_db('SELECT * FROM predictions WHERE fulfilled = 0 ORDER BY timestamp DESC LIMIT 5'),
            'events': self._query_db('SELECT * FROM evolution_events ORDER BY timestamp DESC LIMIT 10'),
            'stats': self._get_stats()
        }
    
    def _get_html_content(self):
        """获取 HTML 内容"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧬 智能进化工作台 v3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: rgba(22, 33, 62, 0.8);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
        
        .card h2 {
            color: #e94560;
            margin-bottom: 20px;
            font-size: 1.4em;
            border-bottom: 2px solid #e94560;
            padding-bottom: 10px;
        }
        
        .intelligence-score {
            text-align: center;
            padding: 20px;
            background: rgba(78, 204, 163, 0.1);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .score-big {
            font-size: 3em;
            font-weight: bold;
            color: #4ecca3;
        }
        
        .grade {
            font-size: 1.5em;
            color: #f9a825;
            margin-top: 10px;
        }
        
        .dimension {
            display: flex;
            align-items: center;
            padding: 8px 0;
        }
        
        .dimension-name {
            width: 100px;
        }
        
        .dimension-bar {
            flex: 1;
            height: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
            margin: 0 10px;
        }
        
        .dimension-fill {
            height: 100%;
            background: linear-gradient(90deg, #4ecca3, #667eea);
            border-radius: 10px;
            transition: width 0.5s;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .metric-value {
            font-weight: bold;
            color: #4ecca3;
        }
        
        .instance-item, .bug-item, .prediction-item, .event-item {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 3px solid #667eea;
        }
        
        .status-running { border-left-color: #4ecca3; }
        .status-completed { border-left-color: #667eea; }
        .status-created { border-left-color: #f9a825; }
        .status-error { border-left-color: #e94560; }
        
        .severity-critical { color: #e94560; }
        .severity-high { color: #f9a825; }
        .severity-medium { color: #667eea; }
        .severity-low { color: #4ecca3; }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #888;
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
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
        }
        
        .refresh-btn:hover {
            background: #ff6b6b;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #888;
            font-size: 0.9em;
        }
        
        #update-time {
            color: #4ecca3;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧬 智能进化工作台 v3</h1>
        <div class="subtitle">实时监控 AI 智能水平、记忆状态、进化预测</div>
    </div>
    
    <div class="grid">
        <div class="card">
            <h2>🧠 智能评估</h2>
            <div id="intelligence">
                <div class="loading">加载中...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>📦 沙箱实例</h2>
            <div id="instances">
                <div class="loading">加载中...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>🐛 Bug 追踪</h2>
            <div id="bugs">
                <div class="loading">加载中...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>🔮 预测分析</h2>
            <div id="predictions">
                <div class="loading">加载中...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>📜 最近事件</h2>
            <div id="events">
                <div class="loading">加载中...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>📊 实时指标</h2>
            <div id="stats">
                <div class="loading">加载中...</div>
            </div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="refreshData()">🔄 刷新数据</button>
    
    <div class="footer">
        <p>💡 自动刷新 (10秒) | 最后更新: <span id="update-time">--:--:--</span></p>
        <p>🚀 智能进化系统运行中 | 数据来源: SQLite</p>
    </div>
    
    <script>
        async function fetchData() {
            try {
                const response = await fetch('/api/dashboard');
                const data = await response.json();
                updateUI(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        
        function updateUI(data) {
            // 更新智能评分
            if (data.intelligence) {
                const intel = data.intelligence;
                const dims = JSON.parse(intel.dimensions || '{}');
                let html = `
                    <div class="intelligence-score">
                        <div class="score-big">${intel.percentage}%</div>
                        <div class="grade">${intel.grade}级</div>
                    </div>
                `;
                for (const [name, score] of Object.entries(dims)) {
                    const pct = (score / 5) * 100;
                    html += `
                        <div class="dimension">
                            <span class="dimension-name">${name}</span>
                            <div class="dimension-bar">
                                <div class="dimension-fill" style="width: ${pct}%"></div>
                            </div>
                            <span>${score}/5</span>
                        </div>
                    `;
                }
                document.getElementById('intelligence').innerHTML = html;
            }
            
            // 更新实例
            if (data.instances) {
                let html = '';
                data.instances.forEach(inst => {
                    const statusClass = `status-${inst.status.toLowerCase()}`;
                    html += `
                        <div class="instance-item ${statusClass}">
                            <strong>[${inst.status}]</strong> ${inst.id}<br>
                            <small>需求: ${inst.requirement_id} | 端口: ${inst.port}</small>
                        </div>
                    `;
                });
                document.getElementById('instances').innerHTML = html;
            }
            
            // 更新 Bug
            if (data.bugs) {
                let html = '';
                data.bugs.forEach(bug => {
                    html += `
                        <div class="bug-item">
                            <span class="severity-${bug.severity.toLowerCase()}">[${bug.severity}]</span>
                            ${bug.bug_type}<br>
                            <small>${bug.description}</small>
                        </div>
                    `;
                });
                document.getElementById('bugs').innerHTML = html;
            }
            
            // 更新预测
            if (data.predictions) {
                let html = '';
                data.predictions.forEach(pred => {
                    const confBar = '█'.repeat(pred.confidence / 10) + '░'.repeat(10 - pred.confidence / 10);
                    html += `
                        <div class="prediction-item">
                            <strong>[${pred.prediction_type}]</strong><br>
                            ${pred.prediction_text}<br>
                            <small>置信度: ${confBar} ${pred.confidence}%</small><br>
                            <small>建议: ${pred.action}</small>
                        </div>
                    `;
                });
                document.getElementById('predictions').innerHTML = html;
            }
            
            // 更新事件
            if (data.events) {
                let html = '';
                data.events.forEach(event => {
                    const time = event.timestamp ? event.timestamp.substring(11, 19) : '--:--:--';
                    html += `
                        <div class="event-item">
                            <strong>[${time}] ${event.event_type}</strong><br>
                            <small>${event.description}</small>
                        </div>
                    `;
                });
                document.getElementById('events').innerHTML = html;
            }
            
            // 更新统计
            if (data.stats) {
                let html = '';
                html += `<div class="metric"><span>实例总数</span><span class="metric-value">${Object.values(data.stats.instances || {}).reduce((a, b) => a + b, 0)}</span></div>`;
                html += `<div class="metric"><span>未修复Bug</span><span class="metric-value">${Object.values(data.stats.bugs || {}).reduce((a, b) => a + b, 0)}</span></div>`;
                html += `<div class="metric"><span>待实现预测</span><span class="metric-value">${data.stats.pending_predictions || 0}</span></div>`;
                html += `<div class="metric"><span>今日事件</span><span class="metric-value">${data.stats.today_events || 0}</span></div>`;
                document.getElementById('stats').innerHTML = html;
            }
            
            // 更新时间
            document.getElementById('update-time').textContent = new Date().toLocaleTimeString();
        }
        
        function refreshData() {
            fetchData();
        }
        
        // 初始加载
        fetchData();
        
        // 自动刷新
        setInterval(fetchData, 10000);
    </script>
</body>
</html>'''


def run_server(port=8080):
    """运行服务器"""
    server = HTTPServer(('', port), EvolutionWebHandler)
    print(f"🚀 Web 服务器启动: http://localhost:{port}")
    print(f"📊 API 端点:")
    print(f"   - http://localhost:{port}/api/dashboard")
    print(f"   - http://localhost:{port}/api/instances")
    print(f"   - http://localhost:{port}/api/bugs")
    print(f"   - http://localhost:{port}/api/predictions")
    print(f"   - http://localhost:{port}/api/events")
    print(f"   - http://localhost:{port}/api/stats")
    server.serve_forever()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
