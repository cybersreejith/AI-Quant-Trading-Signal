import React from 'react';
import { Card, Typography, Table } from 'antd';
import ReactECharts from 'echarts-for-react';

const { Title, Paragraph } = Typography;

const Report: React.FC = () => {
  // 示例数据
  const option = {
    title: {
      text: '交易信号分析'
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
        <Title level={3}>交易报告</Title>
        <Paragraph>
          基于历史数据和技术指标分析生成的交易建议报告。
        </Paragraph>
      </Card>

      <Card style={{ marginBottom: 24 }}>
        <ReactECharts option={option} />
      </Card>

      <Card>
        <Table
          columns={[
            { title: '指标名称', dataIndex: 'indicator' },
            { title: '当前值', dataIndex: 'value' },
            { title: '信号', dataIndex: 'signal' },
            { title: '建议', dataIndex: 'suggestion' },
          ]}
          dataSource={[
            {
              key: '1',
              indicator: 'MACD',
              value: '0.0023',
              signal: '多头',
              suggestion: '建议买入',
            },
            {
              key: '2',
              indicator: 'RSI',
              value: '65.32',
              signal: '中性',
              suggestion: '建议观望',
            },
          ]}
        />
      </Card>
    </div>
  );
};

export default Report; 