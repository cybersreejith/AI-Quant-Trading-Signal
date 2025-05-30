import React from 'react';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Home from './pages/Home';
import Trading from './pages/Trading';
import Report from './pages/Report';

const { Header, Content, Footer } = Layout;

const App: React.FC = () => {
  return (
    <ConfigProvider locale={zhCN}>
      <Layout className="layout" style={{ minHeight: '100vh' }}>
        <Header style={{ 
          display: 'flex', 
          alignItems: 'center',
          background: '#fff',
          padding: '0 50px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <h1 style={{ margin: 0, color: '#1890ff' }}>AI量化交易系统</h1>
        </Header>
        <Content style={{ padding: '24px 50px' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/trading" element={<Trading />} />
            <Route path="/report" element={<Report />} />
          </Routes>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          AI量化交易系统 ©{new Date().getFullYear()} Created by Your Company
        </Footer>
      </Layout>
    </ConfigProvider>
  );
};

export default App; 