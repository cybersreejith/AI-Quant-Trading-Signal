import React from 'react';
import { Card, Typography, Row, Col, Button } from 'antd';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div style={{ padding: '24px' }}>
      <Row gutter={[24, 24]}>
        <Col span={24}>
          <Card style={{ background: '#1a1a1a', border: 'none' }}>
            <Title level={2} style={{ color: '#fff', textAlign: 'center' }}>
              欢迎使用 AI 量化交易信号系统
            </Title>
            <Paragraph style={{ color: '#fff', textAlign: 'center' }}>
              本系统使用先进的人工智能技术，为您提供专业的量化交易信号服务
            </Paragraph>
          </Card>
        </Col>

        <Col span={24}>
          <Card style={{ background: '#1a1a1a', border: 'none', height: '400px', overflow: 'hidden', position: 'relative' }}>
            {/* 背景网格 */}
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              backgroundImage: 'linear-gradient(rgba(255, 215, 0, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 215, 0, 0.1) 1px, transparent 1px)',
              backgroundSize: '20px 20px',
              animation: 'gridMove 20s linear infinite'
            }} />
            
            {/* 数据流效果 */}
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              background: 'linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent)',
              animation: 'dataFlow 3s linear infinite'
            }} />

            {/* 价格波动线 */}
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '80%',
              height: '2px',
              background: 'linear-gradient(90deg, transparent, #FFD700, transparent)',
              animation: 'priceWave 2s ease-in-out infinite'
            }} />

            {/* 交易指标 */}
            <div style={{
              position: 'absolute',
              top: '30%',
              left: '20%',
              fontSize: '24px',
              color: '#FFD700',
              animation: 'indicatorPulse 2s infinite'
            }}>
              📈 RSI: 65
            </div>
            <div style={{
              position: 'absolute',
              top: '40%',
              right: '20%',
              fontSize: '24px',
              color: '#FFD700',
              animation: 'indicatorPulse 2s infinite 0.5s'
            }}>
              📊 MACD: 0.25
            </div>
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '20%',
              fontSize: '24px',
              color: '#FFD700',
              animation: 'indicatorPulse 2s infinite 1s'
            }}>
              📉 KDJ: 45
            </div>

            {/* 交易信号 */}
            <div style={{
              position: 'absolute',
              top: '60%',
              right: '20%',
              fontSize: '24px',
              color: '#FFD700',
              animation: 'signalGlow 2s infinite'
            }}>
              💡 买入信号
            </div>

            {/* 中心标题 */}
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              fontSize: '48px',
              color: '#FFD700',
              textShadow: '0 0 10px rgba(255, 215, 0, 0.5)',
              animation: 'titleGlow 2s infinite'
            }}>
              智能量化交易
            </div>
          </Card>
        </Col>

        <Col span={24}>
          <Row gutter={[24, 24]}>
            <Col span={12}>
              <Card 
                style={{ 
                  background: '#2a2a2a', 
                  border: 'none',
                  height: '200px',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.3s'
                }}
                onClick={() => navigate('/trading')}
                hoverable
              >
                <Title level={3} style={{ color: '#fff' }}>交易信号</Title>
                <Paragraph style={{ color: '#fff', textAlign: 'center' }}>
                  选择资产类型，输入交易对，生成专业的交易信号
                </Paragraph>
                <Button 
                  type="primary" 
                  size="large"
                  style={{ marginTop: '20px' }}
                >
                  开始交易
                </Button>
              </Card>
            </Col>
            <Col span={12}>
              <Card 
                style={{ 
                  background: '#2a2a2a', 
                  border: 'none',
                  height: '200px',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.3s'
                }}
                onClick={() => navigate('/report')}
                hoverable
              >
                <Title level={3} style={{ color: '#fff' }}>交易报告</Title>
                <Paragraph style={{ color: '#fff', textAlign: 'center' }}>
                  查看历史交易记录，分析交易表现，优化交易策略
                </Paragraph>
                <Button 
                  type="primary" 
                  size="large"
                  style={{ marginTop: '20px' }}
                >
                  查看报告
                </Button>
              </Card>
            </Col>
          </Row>
        </Col>

        <Col span={24}>
          <Card style={{ background: '#1a1a1a', border: 'none' }}>
            <Title level={3} style={{ color: '#fff' }}>主要功能</Title>
            <Row gutter={[24, 24]}>
              <Col span={6}>
                <Card style={{ background: '#2a2a2a', border: 'none' }}>
                  <Title level={4} style={{ color: '#fff' }}>选择资产类型</Title>
                  <Paragraph style={{ color: '#fff' }}>
                    支持全球股票、ETF、外汇、加密货币等多种资产类型
                  </Paragraph>
                </Card>
              </Col>
              <Col span={6}>
                <Card style={{ background: '#2a2a2a', border: 'none' }}>
                  <Title level={4} style={{ color: '#fff' }}>查看参考列表</Title>
                  <Paragraph style={{ color: '#fff' }}>
                    提供丰富的资产代码参考，方便快速选择
                  </Paragraph>
                </Card>
              </Col>
              <Col span={6}>
                <Card style={{ background: '#2a2a2a', border: 'none' }}>
                  <Title level={4} style={{ color: '#fff' }}>输入交易对</Title>
                  <Paragraph style={{ color: '#fff' }}>
                    支持多种交易对格式，满足不同市场需求
                  </Paragraph>
                </Card>
              </Col>
              <Col span={6}>
                <Card style={{ background: '#2a2a2a', border: 'none' }}>
                  <Title level={4} style={{ color: '#fff' }}>生成交易报告</Title>
                  <Paragraph style={{ color: '#fff' }}>
                    基于AI分析生成专业的交易建议报告
                  </Paragraph>
                </Card>
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>

      <style>
        {`
          @keyframes gridMove {
            0% { background-position: 0 0; }
            100% { background-position: 20px 20px; }
          }
          
          @keyframes dataFlow {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
          }
          
          @keyframes priceWave {
            0% { transform: translate(-50%, -50%) scaleX(1); }
            50% { transform: translate(-50%, -50%) scaleX(1.2); }
            100% { transform: translate(-50%, -50%) scaleX(1); }
          }
          
          @keyframes indicatorPulse {
            0% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.1); }
            100% { opacity: 0.5; transform: scale(1); }
          }
          
          @keyframes signalGlow {
            0% { text-shadow: 0 0 5px rgba(255, 215, 0, 0.5); }
            50% { text-shadow: 0 0 15px rgba(255, 215, 0, 0.8); }
            100% { text-shadow: 0 0 5px rgba(255, 215, 0, 0.5); }
          }
          
          @keyframes titleGlow {
            0% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }
            50% { text-shadow: 0 0 20px rgba(255, 215, 0, 0.8); }
            100% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }
          }

          .ant-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
          }
        `}
      </style>
    </div>
  );
};

export default Home; 