import React from 'react';
import { Card, Typography, Table, Button } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;

const Report: React.FC = () => {
  const navigate = useNavigate();
  
  // 示例数据
  const option = {
    title: {
      text: 'Trading Signal Analysis'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: [820, 932, 901, 934, 1290, 1330, 1320],
      type: 'line'
    }]
  };

  return (
    <div>
      <Card style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
          <Button 
            type="text" 
            icon={<ArrowLeftOutlined />} 
            onClick={() => navigate('/')}
            style={{ marginRight: 16 }}
          >
            Back
          </Button>
          <Title level={3} style={{ margin: 0 }}>Trading Report</Title>
        </div>
        <Paragraph>
          A trading suggestion report generated based on historical data and technical indicators.
        </Paragraph>
      </Card>

      <Card style={{ marginBottom: 24 }}>
        <ReactECharts option={option} />
      </Card>

      <Card>
        <Table
          columns={[
            { title: 'Indicator Name', dataIndex: 'indicator' },
            { title: 'Current Value', dataIndex: 'value' },
            { title: 'Signal', dataIndex: 'signal' },
            { title: 'Suggestion', dataIndex: 'suggestion' },
          ]}
          dataSource={[
            {
              key: '1',
              indicator: 'MACD',
              value: '0.0023',
              signal: 'Bullish',
              suggestion: 'Buy',
            },
            {
              key: '2',
              indicator: 'RSI',
              value: '65.32',
              signal: 'Neutral',
              suggestion: 'Hold',
            },
          ]}
        />
      </Card>
    </div>
  );
};

export default Report; 