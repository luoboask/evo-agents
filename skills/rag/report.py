#!/usr/bin/env python3
"""
RAG 评估可视化报告
生成 HTML 格式的评估报告
"""

import json
from pathlib import Path
from path_utils import resolve_workspace, resolve_data_dir
from datetime import datetime, timedelta

SKILLS_DIR = Path(__file__).parent
# 使用统一路径：data/${agent_name}/logs/evaluations.jsonl
DATA_DIR = SKILLS_DIR.parent.parent / "data" / os.environ.get("OPENCLAW_AGENT", os.path.basename(str(resolve_workspace())).replace("workspace-", ""))"
LOGS_DIR = DATA_DIR / "logs"
EVALUATIONS_FILE = LOGS_DIR / "evaluations.jsonl"

def generate_report(days=7):
    """生成 HTML 报告"""
    # 加载评估数据
    evals = []
    cutoff = datetime.now() - timedelta(days=days)
    
    if EVALUATIONS_FILE.exists():
        with open(EVALUATIONS_FILE, 'r') as f:
            for line in f:
                try:
                    eval_data = json.loads(line)
                    eval_time = datetime.fromisoformat(eval_data["timestamp"])
                    if eval_time >= cutoff:
                        evals.append(eval_data)
                except:
                    continue
    
    # 计算指标
    total = len(evals)
    feedback = {'positive': 0, 'neutral': 0, 'negative': 0}
    latencies = []
    retrieved_counts = []
    
    for e in evals:
        fb = e.get('feedback', 'neutral')
        feedback[fb] = feedback.get(fb, 0) + 1
        latencies.append(e.get('latency_ms', 0))
        retrieved_counts.append(e.get('retrieved_count', 0))
    
    # 处理空数据情况
    if total == 0:
        print("⚠️ 没有评估数据，无法生成报告")
        return None
    
    # 生成 HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>RAG 评估报告 - 过去{days}天</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .metric {{ display: inline-block; margin: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
        .metric h3 {{ margin: 0 0 10px 0; }}
        .metric .value {{ font-size: 24px; font-weight: bold; color: #2196F3; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #2196F3; color: white; }}
    </style>
</head>
<body>
    <h1>📊 RAG 评估报告</h1>
    <p>周期：过去{days}天 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <h2>核心指标</h2>
    <div class="metric">
        <h3>总查询数</h3>
        <div class="value">{total}</div>
    </div>
    <div class="metric">
        <h3>正面反馈</h3>
        <div class="value">{feedback['positive']} ({feedback['positive']/total*100:.1f}%)</div>
    </div>
    <div class="metric">
        <h3>平均延迟</h3>
        <div class="value">{sum(latencies)/len(latencies):.1f}ms</div>
    </div>
    <div class="metric">
        <h3>平均检索数</h3>
        <div class="value">{sum(retrieved_counts)/len(retrieved_counts):.1f}条</div>
    </div>
    
    <h2>反馈分布</h2>
    <table>
        <tr><th>反馈类型</th><th>数量</th><th>占比</th></tr>
        <tr><td>✅ 正面</td><td>{feedback['positive']}</td><td>{feedback['positive']/total*100:.1f}%</td></tr>
        <tr><td>⚠️ 中性</td><td>{feedback['neutral']}</td><td>{feedback['neutral']/total*100:.1f}%</td></tr>
        <tr><td>❌ 负面</td><td>{feedback['negative']}</td><td>{feedback['negative']/total*100:.1f}%</td></tr>
    </table>
</body>
</html>
"""
    
    # 保存报告
    report_path = LOGS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 报告已生成：{report_path}")
    return report_path

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='RAG 评估可视化报告')
    parser.add_argument('--days', type=int, default=7, help='报告天数')
    args = parser.parse_args()
    generate_report(args.days)
