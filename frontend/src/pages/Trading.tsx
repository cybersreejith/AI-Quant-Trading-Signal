import React, { useState } from 'react';
import { Card, Input, Button, Table, message, Radio, Space, List, Typography } from 'antd';

const { Text } = Typography;

const Trading: React.FC = () => {
  const [assetType, setAssetType] = useState<string>('');
  const [symbol, setSymbol] = useState<string>('');
  const [showAssetList, setShowAssetList] = useState<boolean>(false);

  const assetTypes = [
    { value: 'stock', label: '全球股票' },
    { value: 'etf', label: 'ETF' },
    { value: 'forex', label: '外汇' },
    { value: 'crypto', label: '加密货币' },
  ];

  const assetLists = {
    stock: [
      'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'BABA', 'PDD', 'NIO',
      'JPM', 'V', 'WMT', 'MA', 'HD', 'BAC', 'XOM', 'PFE', 'AVGO', 'COST',
      'TMO', 'CSCO', 'DHR', 'ABBV', 'WFC', 'MRK', 'VZ', 'NKE', 'CRM', 'NEE'
    ],
    etf: [
      'SPY', 'QQQ', 'DIA', 'IWM', 'EFA', 'EEM', 'GLD', 'SLV', 'TLT', 'VNQ',
      'XLK', 'XLF', 'XLE', 'XLV', 'XLI', 'XLP', 'XLY', 'XLB', 'XLU', 'XBI',
      'ARKK', 'IEFA', 'IEMG', 'AGG', 'LQD', 'HYG', 'GDX', 'GDXJ', 'USO', 'UNG'
    ],
    forex: [
      'EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X', 'NZDUSD=X', 'USDCHF=X',
      'EURGBP=X', 'EURJPY=X', 'GBPJPY=X', 'EURCAD=X', 'AUDJPY=X', 'NZDJPY=X', 'GBPAUD=X',
      'EURAUD=X', 'USDSGD=X', 'USDHKD=X', 'EURCHF=X', 'GBPCHF=X', 'AUDNZD=X'
    ],
    crypto: [
      'BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 'DOGE-USD', 'DOT-USD',
      'SOL-USD', 'AVAX-USD', 'MATIC-USD', 'LINK-USD', 'UNI-USD', 'AAVE-USD', 'COMP-USD',
      'SUSHI-USD', 'YFI-USD', 'SNX-USD', 'MKR-USD', 'CRV-USD', 'BAL-USD'
    ]
  };

  const handleAssetTypeChange = (value: string) => {
    setAssetType(value);
    setShowAssetList(true);
    setSymbol('');
  };

  const handleAssetSelect = (selectedSymbol: string) => {
    setSymbol(selectedSymbol);
    setShowAssetList(false);
  };

  const handleSubmit = async () => {
    try {
      if (!assetType) {
        message.warning('请选择资产类型');
        return;
      }
      if (!symbol) {
        message.warning('请输入交易对');
        return;
      }
      // TODO: 调用后端 API
      message.success('交易信号生成中...');
    } catch (error) {
      message.error('操作失败，请重试');
    }
  };

  return (
    <Card title="交易信号生成">
      <div style={{ marginBottom: 24 }}>
        <div style={{ marginBottom: 16 }}>
          <h3>请选择资产类型：</h3>
          <Radio.Group
            value={assetType}
            onChange={e => handleAssetTypeChange(e.target.value)}
            style={{ width: '100%' }}
          >
            <Space direction="vertical" style={{ width: '100%' }}>
              {assetTypes.map(type => (
                <Radio.Button 
                  key={type.value} 
                  value={type.value}
                  style={{ 
                    width: '100%', 
                    textAlign: 'center',
                    height: '40px',
                    lineHeight: '40px',
                    marginBottom: '8px'
                  }}
                >
                  {type.label}
                </Radio.Button>
              ))}
            </Space>
          </Radio.Group>
        </div>

        <div style={{ marginBottom: 16 }}>
          <h3>请输入交易对：</h3>
          <Input
            style={{ width: '100%' }}
            placeholder="例如：BTC-USD, AAPL, EURUSD=X"
            value={symbol}
            onChange={e => setSymbol(e.target.value)}
          />
        </div>

        {showAssetList && assetType && (
          <div style={{ marginBottom: 16 }}>
            <h3>参考资产列表：</h3>
            <List
              grid={{ gutter: 16, column: 4 }}
              dataSource={assetLists[assetType as keyof typeof assetLists]}
              renderItem={item => (
                <List.Item>
                  <Button 
                    type="text" 
                    onClick={() => handleAssetSelect(item)}
                    style={{ 
                      width: '100%',
                      textAlign: 'center',
                      border: '1px solid #d9d9d9',
                      borderRadius: '4px'
                    }}
                  >
                    <Text>{item}</Text>
                  </Button>
                </List.Item>
              )}
            />
          </div>
        )}

        <Button 
          type="primary" 
          onClick={handleSubmit}
          style={{ width: '100%', height: '40px' }}
        >
          生成信号
        </Button>
      </div>

      <Table
        columns={[
          { title: '交易对', dataIndex: 'symbol' },
          { title: '信号类型', dataIndex: 'signalType' },
          { title: '生成时间', dataIndex: 'timestamp' },
          { title: '建议操作', dataIndex: 'action' },
        ]}
        dataSource={[]}
      />
    </Card>
  );
};

export default Trading; 