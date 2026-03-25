import React from 'react';
import { Card, Progress, Row, Col } from 'antd';
import { TrophyOutlined, StarOutlined } from '@ant-design/icons';

const IntelligencePanel = ({ data, loading }) => {
  const { percentage, grade, dimensions } = data;

  const getProgressColor = (value) => {
    if (value >= 5) return '#4ecca3';
    if (value >= 4) return '#667eea';
    if (value >= 3) return '#f9a825';
    return '#e94560';
  };

  return (
    <Card 
      title={<><TrophyOutlined /> 智能评估</>} 
      className="panel-card"
      loading={loading}
    >
      <div className="intelligence-score">
        <div className="score-big">{percentage}%</div>
        <div className="grade">
          <StarOutlined /> {grade}级
        </div>
      </div>

      <Row gutter={[16, 16]}>
        {Object.entries(dimensions).map(([name, value]) => (
          <Col span={24} key={name}>
            <div className="dimension-item">
              <div className="dimension-label">
                <span>{name}</span>
                <span>{value}/5</span>
              </div>
              <Progress
                percent={(value / 5) * 100}
                strokeColor={getProgressColor(value)}
                trailColor="rgba(255,255,255,0.1)"
                strokeWidth={12}
                showInfo={false}
              />
            </div>
          </Col>
        ))}
      </Row>
    </Card>
  );
};

export default IntelligencePanel;
