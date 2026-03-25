import React from 'react';
import { Card, Timeline, Tag } from 'antd';
import { RocketOutlined, CheckCircleOutlined, SyncOutlined } from '@ant-design/icons';

const EvolutionPanel = ({ history, loading }) => {
  const getDecisionIcon = (decision) => {
    if (decision.includes('deploy') || decision.includes('create')) {
      return <RocketOutlined style={{ color: '#4ecca3' }} />;
    }
    if (decision.includes('no_action')) {
      return <CheckCircleOutlined style={{ color: '#667eea' }} />;
    }
    return <SyncOutlined style={{ color: '#f9a825' }} />;
  };

  const getDecisionColor = (decision) => {
    if (decision.includes('deploy') || decision.includes('create')) return 'green';
    if (decision.includes('no_action')) return 'blue';
    return 'default';
  };

  return (
    <Card 
      title={<><RocketOutlined /> 进化历史</>} 
      className="panel-card"
      loading={loading}
    >
      <Timeline mode="left">
        {history.map((item, index) => (
          <Timeline.Item
            key={index}
            dot={getDecisionIcon(item.decision)}
            label={item.timestamp.substring(11, 16)}
          >
            <Tag color={getDecisionColor(item.decision)}>
              {item.decision}
            </Tag>
            <div style={{ color: '#888', fontSize: 12, marginTop: 4 }}>
              {item.reason}
            </div>
          </Timeline.Item>
        ))}
      </Timeline>
    </Card>
  );
};

export default EvolutionPanel;
