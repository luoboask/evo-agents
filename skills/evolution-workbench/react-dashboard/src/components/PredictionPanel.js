import React from 'react';
import { Card, Tag, Progress } from 'antd';
import { BulbOutlined, ArrowRightOutlined } from '@ant-design/icons';

const PredictionPanel = ({ predictions, loading }) => {
  const getTypeName = (type) => {
    const names = {
      'memory_growth': '记忆增长',
      'skill_expansion': '技能扩展',
      'intelligence_growth': '智能提升',
    };
    return names[type] || type;
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return '#4ecca3';
    if (confidence >= 70) return '#667eea';
    if (confidence >= 60) return '#f9a825';
    return '#e94560';
  };

  return (
    <Card 
      title={<><BulbOutlined /> 预测分析</>} 
      className="panel-card"
      loading={loading}
    >
      {predictions.map((item, index) => (
        <div key={index} className="prediction-card">
          <div className="prediction-type">
            [{getTypeName(item.type)}]
          </div>
          <div className="prediction-text">
            {item.prediction}
          </div>
          <div className="prediction-action">
            <ArrowRightOutlined /> {item.action}
          </div>
          <div style={{ marginTop: 8 }}>
            <Progress
              percent={item.confidence}
              strokeColor={getConfidenceColor(item.confidence)}
              trailColor="rgba(255,255,255,0.1)"
              strokeWidth={8}
              format={(percent) => (
                <span style={{ color: getConfidenceColor(item.confidence) }}>
                  置信度: {percent}%
                </span>
              )}
            />
          </div>
        </div>
      ))}
    </Card>
  );
};

export default PredictionPanel;
