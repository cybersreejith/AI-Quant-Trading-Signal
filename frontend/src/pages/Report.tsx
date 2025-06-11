import React, { useState, useEffect } from 'react';
import { Card, Typography, Table, Button, List, Tag, Space } from 'antd';
import { ArrowLeftOutlined, HistoryOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { useNavigate, useLocation } from 'react-router-dom';

const { Title, Paragraph } = Typography;

// new data structure, match the backend return format
interface FinalReport {
  quant_analysis: {
    status: string;
    symbol: string;
    strategy_name: string;
    live_signal: string;
    key_metrics: {
      total_return: string;
      sharpe_ratio: number;
      max_drawdown: string;
      win_rate: string;
      total_trades?: number;
      avg_trade_duration?: string;
    };
    summary: {
      rating: string;
      recommendation: string;
      key_strength: string;
      main_weakness: string;
    };
    is_satisfactory: boolean;
  };
  market_sentiment: {
    overall_sentiment: string;
    sentiment_score: number;
    confidence: number;
    error?: string;
    raw_data?: string;
  };
  ai_analysis: string;
  generated_at: string;
}

interface AnalysisData {
  final_report: FinalReport;
}

interface ReportRecord {
  id: string;
  symbol: string;
  timestamp: string;
  analysisData: AnalysisData;
}

const Report: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [reportHistory, setReportHistory] = useState<ReportRecord[]>([]);
  const [selectedReport, setSelectedReport] = useState<ReportRecord | null>(null);

  // load history report
  useEffect(() => {
    const history = JSON.parse(localStorage.getItem('reportHistory') || '[]');
    setReportHistory(history.sort((a: ReportRecord, b: ReportRecord) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    ));
  }, []);

  // if there is new analysis data, add it to the history record
  useEffect(() => {
    if (location.state) {
      const { analysisData, symbol, timestamp } = location.state as {
        analysisData: AnalysisData;
        symbol: string;
        timestamp: string;
      };

      const newReport: ReportRecord = {
        id: Date.now().toString(),
        symbol,
        timestamp,
        analysisData
      };

      const updatedHistory = [newReport, ...reportHistory];
      localStorage.setItem('reportHistory', JSON.stringify(updatedHistory));
      setReportHistory(updatedHistory);
      setSelectedReport(newReport);
    }
  }, [location.state]);

  // if there is no history record
  if (reportHistory.length === 0) {
    return (
      <div style={{ padding: '20px' }}>
        <Card>
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
            No analysis history available. Please go back to the Trading page to generate a new analysis.
          </Paragraph>
        </Card>
      </div>
    );
  }

  // render report content  
  const renderReportContent = (report: ReportRecord) => {
    const { analysisData, symbol, timestamp } = report;
    const finalReport = analysisData.final_report;
    
    return (
      <>
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
            <Title level={3} style={{ margin: 0 }}>Trading Report - {symbol}</Title>
          </div>
          <Paragraph>
            Analysis Time: {new Date(timestamp).toLocaleString()}
          </Paragraph>
          <Paragraph>
            Generated: {finalReport.generated_at}
          </Paragraph>
        </Card>

        {/* market sentiment and trading signal analysis */}
        <Card title="Market Sentiment & Trading Signal Analysis" style={{ marginBottom: 24 }}>
          <ReactECharts 
            option={{
              title: {
                text: `${symbol} Sentiment vs Signal Analysis`,
                left: 'center'
              },
              tooltip: {
                trigger: 'item',
                formatter: function(params: any) {
                  if (params.seriesType === 'gauge') {
                    return `${params.seriesName}<br/>${params.name}: ${params.value}`;
                  }
                  return `${params.name}: ${params.value}`;
                }
              },
              series: [
                // market sentiment score gauge
                {
                  name: 'Market Sentiment Score',
                  type: 'gauge',
                  center: ['25%', '50%'],
                  radius: '60%',
                  min: -100,
                  max: 100,
                  splitNumber: 10,
                  axisLine: {
                    lineStyle: {
                      color: [
                        [0.3, '#fd666d'],   // negative sentiment area
                        [0.7, '#fac858'],   // neutral sentiment area
                        [1, '#67e0e3']      // positive sentiment area
                      ],
                      width: 8
                    }
                  },
                  pointer: {
                    itemStyle: {
                      color: 'inherit'
                    }
                  },
                  axisTick: {
                    distance: -30,
                    length: 8,
                    lineStyle: {
                      color: '#fff',
                      width: 2
                    }
                  },
                  splitLine: {
                    distance: -30,
                    length: 30,
                    lineStyle: {
                      color: '#fff',
                      width: 4
                    }
                  },
                  axisLabel: {
                    color: 'inherit',
                    distance: 40,
                    fontSize: 12,
                    formatter: function(value: number) {
                      if (value <= -50) return 'Negative';
                      if (value >= 50) return 'Positive';
                      return 'Neutral';
                    }
                  },
                  detail: {
                    valueAnimation: true,
                    formatter: '{value}',
                    color: 'inherit'
                  },
                  data: [
                    {
                      value: Math.round(finalReport.market_sentiment.sentiment_score * 100),
                      name: 'Sentiment'
                    }
                  ]
                },
                // trading signal indicator
                {
                  name: 'Trading Signal',
                  type: 'gauge',
                  center: ['75%', '50%'],
                  radius: '60%',
                  min: -1,
                  max: 1,
                  splitNumber: 4,
                  axisLine: {
                    lineStyle: {
                      color: [
                        [0.25, '#fd666d'],  // SELL area
                        [0.75, '#fac858'],  // HOLD area
                        [1, '#67e0e3']      // BUY area
                      ],
                      width: 8
                    }
                  },
                  axisLabel: {
                    distance: 40,
                    fontSize: 12,
                    formatter: function(value: number) {
                      if (value <= -0.5) return 'SELL';
                      if (value >= 0.5) return 'BUY';
                      return 'HOLD';
                    }
                  },
                  detail: {
                    valueAnimation: true,
                    formatter: function(value: number) {
                      if (value <= -0.5) return 'SELL';
                      if (value >= 0.5) return 'BUY';
                      return 'HOLD';
                    },
                    color: 'inherit',
                    fontSize: 20,
                    fontWeight: 'bold'
                  },
                  data: [
                    {
                      value: finalReport.quant_analysis.live_signal === 'BUY' ? 0.8 : 
                             finalReport.quant_analysis.live_signal === 'SELL' ? -0.8 : 0,
                      name: 'Signal'
                    }
                  ]
                }
              ]
            }}
            style={{ height: '400px' }}
          />
        </Card>

        {/* strategy information card */}
        <Card title="Strategy Overview" style={{ marginBottom: 24 }}>
          <Paragraph>
            <strong>Strategy:</strong> {finalReport.quant_analysis.strategy_name}
          </Paragraph>
          <Paragraph>
            <strong>Live Signal:</strong> 
            <Tag color={finalReport.quant_analysis.live_signal === 'BUY' ? 'green' : 
                       finalReport.quant_analysis.live_signal === 'SELL' ? 'red' : 'orange'}>
              {finalReport.quant_analysis.live_signal}
            </Tag>
          </Paragraph>
          <Paragraph>
            <strong>Rating:</strong> 
            <Tag color={finalReport.quant_analysis.summary.rating === 'Poor' ? 'red' : 'green'}>
              {finalReport.quant_analysis.summary.rating}
            </Tag>
          </Paragraph>
          <Paragraph>
            <strong>Recommendation:</strong> {finalReport.quant_analysis.summary.recommendation}
          </Paragraph>
        </Card>

        <Card title="Quantitative Analysis" style={{ marginBottom: 24 }}>
          <Table
            columns={[
              { title: 'Metric', dataIndex: 'metric' },
              { title: 'Value', dataIndex: 'value' },
            ]}
            dataSource={[
              {
                key: '1',
                metric: 'Total Return',
                value: finalReport.quant_analysis.key_metrics.total_return,
              },
              {
                key: '2',
                metric: 'Sharpe Ratio',
                value: finalReport.quant_analysis.key_metrics.sharpe_ratio.toFixed(2),
              },
              {
                key: '3',
                metric: 'Max Drawdown',
                value: finalReport.quant_analysis.key_metrics.max_drawdown,
              },
              {
                key: '4',
                metric: 'Win Rate',
                value: finalReport.quant_analysis.key_metrics.win_rate,
              },
              ...(finalReport.quant_analysis.key_metrics.total_trades ? [{
                key: '5',
                metric: 'Total Trades',
                value: finalReport.quant_analysis.key_metrics.total_trades.toString(),
              }] : []),
              ...(finalReport.quant_analysis.key_metrics.avg_trade_duration ? [{
                key: '6',
                metric: 'Avg Trade Duration',
                value: finalReport.quant_analysis.key_metrics.avg_trade_duration,
              }] : []),
            ]}
          />
          
          <div style={{ marginTop: 16 }}>
            <Paragraph>
              <strong>Key Strength:</strong> {finalReport.quant_analysis.summary.key_strength}
            </Paragraph>
            <Paragraph>
              <strong>Main Weakness:</strong> {finalReport.quant_analysis.summary.main_weakness}
            </Paragraph>
          </div>
        </Card>

        <Card title="Market Sentiment" style={{ marginBottom: 24 }}>
          <Paragraph>
            <strong>Overall Sentiment:</strong> 
            <Tag color={finalReport.market_sentiment.overall_sentiment === 'positive' ? 'green' : 
                       finalReport.market_sentiment.overall_sentiment === 'negative' ? 'red' : 'orange'}>
              {finalReport.market_sentiment.overall_sentiment}
            </Tag>
          </Paragraph>
          <Paragraph>
            <strong>Sentiment Score:</strong> {finalReport.market_sentiment.sentiment_score}
          </Paragraph>
          <Paragraph>
            <strong>Confidence:</strong> {(finalReport.market_sentiment.confidence * 100).toFixed(1)}%
          </Paragraph>
          {finalReport.market_sentiment.error && (
            <Paragraph style={{ color: '#ff4d4f' }}>
              <strong>Note:</strong> {finalReport.market_sentiment.error}
            </Paragraph>
          )}
        </Card>

        <Card title="AI Analysis Report" style={{ marginBottom: 24 }}>
          <div style={{ 
            whiteSpace: 'pre-wrap', 
            lineHeight: '1.6',
            background: '#f5f5f5',
            padding: '16px',
            borderRadius: '6px',
            border: '1px solid #d9d9d9'
          }}>
            {finalReport.ai_analysis}
          </div>
        </Card>
      </>
    );
  };

  return (
    <div style={{ padding: '20px' }}>
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
          <Title level={3} style={{ margin: 0 }}>Trading Report History</Title>
        </div>
      </Card>

      <div style={{ display: 'flex', gap: '20px' }}>
        {/* history record list */}
        <Card style={{ width: '300px' }}>
          <List
            dataSource={reportHistory}
            renderItem={report => (
              <List.Item>
                <Button
                  type={selectedReport?.id === report.id ? 'primary' : 'text'}
                  onClick={() => setSelectedReport(report)}
                  style={{ width: '100%', textAlign: 'left' }}
                >
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div>
                      <Tag color="blue">{report.symbol}</Tag>
                      <span style={{ marginLeft: 8 }}>
                        {new Date(report.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <div style={{ fontSize: '12px', color: '#666' }}>
                      {report.analysisData.final_report.market_sentiment.overall_sentiment}
                    </div>
                  </Space>
                </Button>
              </List.Item>
            )}
          />
      </Card>

        {/* report content */}
        <div style={{ flex: 1 }}>
          {selectedReport ? (
            renderReportContent(selectedReport)
          ) : (
      <Card>
              <Paragraph>
                Please select a report from the history to view its details.
              </Paragraph>
      </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default Report; 