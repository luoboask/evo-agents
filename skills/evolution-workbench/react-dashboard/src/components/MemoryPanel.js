import React from 'react';
import { Card, List, Tag, Statistic, Row, Col } from 'antd';
import { DatabaseOutlined, FileTextOutlined } from '@ant-design/icons';

const MemoryPanel = ({ entries, metrics, loading }) => {
  const { working_count, memory_mb, kg_entities, kg_relations } = metrics;

  const getImportanceColor = (importance) => {
    switch (importance) {
      case 'critical': return 'red';
      case 'high': return 'orange';
      case 'medium': return 'blue';
      default: return 'default';
    }
  };

  return (
    <Card 
      title={<><DatabaseOutlined /> 记忆详情</>} 
      className="panel-card"
      loading={loading}
    >
      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={12}>
          <Statistic 
            title="工作记忆" 
            value={working_count} 
            suffix="条"
            valueStyle={{ color: '#4ecca3' }}
          />
        </Col>
        <Col span={12}>
          <Statistic 
            title="记忆大小" 
            value={memory_mb} 
            suffix="MB"
            valueStyle={{ color: '#667eea' }}
          />
        </Col>
      </Row>

      <div style={{ marginBottom: 16 }}>
        <Tag color="blue">知识图谱: {kg_entities}实体</Tag>
        <Tag color="purple">{kg_relations}关系</Tag>
      </div>

      <List
        header={<div style={{ color: '#888' }}>最近工作记忆</div>}
        dataSource={entries}
        renderItem={(item) => (
          <List.Item>
            <div className="memory-entry" style={{ width: '100%' }}>
              <div className="memory-entry-header">
                <span className="memory-role">
                  <FileTextOutlined /> [{item.role}]
                </span>
                <Tag color={getImportanceColor(item.importance)} size="small">
                  {item.importance}
                </Tag>
              </div>
              <div className="memory-content">{item.content}</div>
            </div>
          </List.Item>
        )}
      />
    </Card>
  );
};

export default MemoryPanel;
