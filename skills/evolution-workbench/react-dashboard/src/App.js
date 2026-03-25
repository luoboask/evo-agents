import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Progress, Tag, Timeline, Button, Modal, Descriptions, Badge, Typography, Avatar } from 'antd';
import { 
  BookOutlined, FireOutlined, LineChartOutlined, ClockCircleOutlined, CheckCircleOutlined,
  ThunderboltOutlined, TrophyOutlined, ExperimentOutlined, BulbOutlined, RocketOutlined,
  DashboardOutlined, StarOutlined, CodeOutlined, GithubOutlined, GlobalOutlined,
  NetworkOutlined, FlowChartOutlined, TreeOutlined
} from '@ant-design/icons';

const { Text, Paragraph } = Typography;

const App = () => {
  const [loading, setLoading] = useState(true);
  const [showcaseVisible, setShowcaseVisible] = useState(false);
  const [logVisible, setLogVisible] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);
  const [showcaseData, setShowcaseData] = useState(null);
  const [learningLogs, setLearningLogs] = useState([]);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [overviewRes, learningRes, showcaseRes, logRes, kgRes] = await Promise.all([
        fetch('/api/overview'),
        fetch('/api/learning-stats'),
        fetch('/api/showcase'),
        fetch('/api/learning-log'),
        fetch('/api/memory/knowledge-graph')
      ]);
      
      const overview = await overviewRes.json();
      const learning = await learningRes.json();
      const showcase = await showcaseRes.json();
      const logs = await logRes.json();
      const kg = await kgRes.json();
      
      overview.memory.knowledge_entities = kg.entity_count || 0;
      overview.memory.knowledge_relations = kg.relation_count || 0;
      
      setDashboardData({ overview, learning });
      setShowcaseData(showcase);
      setLearningLogs(logs.logs || []);
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setLoading(false);
    }
  };

  const capabilities = showcaseData?.capabilities || {
    '学习能力': { initial: 4.0, current: 5.5, growth: '+1.5' },
    '推理能力': { initial: 4.0, current: 5.8, growth: '+1.8' },
    '创造能力': { initial: 3.0, current: 5.5, growth: '+2.5' },
    '自主能力': { initial: 4.0, current: 6.0, growth: '+2.0' },
    '协作能力': { initial: 4.0, current: 5.7, growth: '+1.7' },
    '元认知': { initial: 4.0, current: 5.8, growth: '+1.8' }
  };

  return (
    <div style={{ padding: '20px', background: '#f0f2f5', minHeight: '100vh' }}>
      {/* Header */}
      <Card style={{ marginBottom: 20, textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5em', marginBottom: 10, color: '#1890ff' }}>🧬 智能进化工作台</h1>
        <p style={{ fontSize: '1.2em', color: '#666' }}>Self-Evolution Dashboard</p>
        <div style={{ marginTop: 20 }}>
          <Button type="primary" size="large" onClick={() => setShowcaseVisible(true)} style={{ marginRight: 10 }}>
            📊 查看自我学习展示
          </Button>
          <Button size="large" onClick={() => setLogVisible(true)}>
            📖 查看学习日志
          </Button>
        </div>
      </Card>

      {/* 核心指标 */}
      <Card title="📊 核心指标" style={{ marginBottom: 20 }}>
        <Row gutter={16}>
          <Col span={6}>
            <Statistic title="智能评分" value={dashboardData?.overview?.intelligence?.percentage || 0} suffix="%" valueStyle={{ color: '#3f8600' }} />
            <Progress percent={dashboardData?.overview?.intelligence?.percentage || 0} strokeColor={{ '0%': '#108ee9', '100%': '#87d068' }} style={{ marginTop: 10 }} />
            <Tag color="purple" style={{ marginTop: 5 }}>{dashboardData?.overview?.intelligence?.grade || '-'}</Tag>
          </Col>
          <Col span={6}>
            <Statistic title="记忆大小" value={dashboardData?.overview?.memory?.total_size_mb || 0} suffix="MB" valueStyle={{ color: '#1890ff' }} />
          </Col>
          <Col span={6}>
            <Statistic title="进化事件" value={dashboardData?.overview?.evolution?.total_events || 0} valueStyle={{ color: '#722ed1' }} />
          </Col>
          <Col span={6}>
            <Statistic title="知识实体" value={dashboardData?.overview?.memory?.knowledge_entities || 0} valueStyle={{ color: '#fa8c16' }} />
          </Col>
        </Row>
      </Card>

      {/* 学习内容 */}
      <Row gutter={16} style={{ marginBottom: 20 }}>
        <Col span={12}>
          <Card title="📚 学习内容">
            <Row gutter={16}>
              <Col span={12}><Statistic title="定时学习" value={dashboardData?.learning?.scheduled || 0} /></Col>
              <Col span={12}><Statistic title="进化检查" value={dashboardData?.learning?.evolution || 0} /></Col>
              <Col span={12}><Statistic title="每日反思" value={dashboardData?.learning?.reflection || 0} /></Col>
              <Col span={12}><Statistic title="洞察生成" value={dashboardData?.learning?.insights || 0} /></Col>
            </Row>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="⚙️ 学习机制">
            <Timeline>
              <Timeline.Item color="green">定时学习 - 每小时自动学习</Timeline.Item>
              <Timeline.Item color="blue">深度反思 - 每日 23:00 深度分析</Timeline.Item>
              <Timeline.Item color="red">实时反馈 - 每次交互后收集</Timeline.Item>
              <Timeline.Item color="orange">创造性学习 - 类比/融合/洞察</Timeline.Item>
            </Timeline>
          </Card>
        </Col>
      </Row>

      {/* 能力成长 */}
      <Card title="📈 能力成长" style={{ marginBottom: 20 }}>
        <Row gutter={16}>
          {Object.entries(capabilities).map(([name, data]) => (
            <Col span={8} key={name}>
              <Card size="small" title={name}>
                <Progress percent={(data.current / 7) * 100} format={() => data.growth} />
                <div style={{ textAlign: 'center', marginTop: 5 }}>
                  {data.initial} → <strong style={{ color: '#52c41a' }}>{data.current}</strong>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>

      {/* 学习日志模态框 */}
      <Modal title="📖 学习日志" visible={logVisible} onCancel={() => setLogVisible(false)} width={800} footer={[<Button key="close" onClick={() => setLogVisible(false)}>关闭</Button>]}>
        <Timeline>
          {learningLogs.map((log, i) => (
            <Timeline.Item key={i} dot={<Avatar>{log.type?.[0] || 'L'}</Avatar>}>
              <Card size="small" style={{ marginBottom: 10 }}>
                <Tag color="blue">{log.type}</Tag> <Text type="secondary">{log.timestamp?.replace('T', ' ')?.substring(0, 19)}</Text>
                <Paragraph style={{ marginTop: 10 }}><strong>学习内容：</strong>{log.content}</Paragraph>
                <Paragraph><strong>学习收获：</strong>{log.收获 || log.content}</Paragraph>
              </Card>
            </Timeline.Item>
          ))}
        </Timeline>
      </Modal>

      {/* 展示模态框 */}
      <Modal title="🧠 自我学习展示" visible={showcaseVisible} onCancel={() => setShowcaseVisible(false)} width={800} footer={[<Button key="close" onClick={() => setShowcaseVisible(false)}>关闭</Button>]}>
        <Statistic title="定时学习" value={showcaseData?.metrics?.scheduled_learning_count || 0} suffix="次" style={{ marginBottom: 20 }} />
        {Object.entries(capabilities).map(([name, data]) => (
          <div key={name} style={{ marginBottom: 15 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <strong>{name}</strong>
              <span>{data.initial} → {data.current} ({data.growth})</span>
            </div>
            <Progress percent={(data.current / 7) * 100} />
          </div>
        ))}
      </Modal>
    </div>
  );
};

export default App;
