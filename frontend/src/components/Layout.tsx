import React from 'react';
import { Layout as AntLayout, Menu } from 'antd';
import { Outlet, useNavigate } from 'react-router-dom';

const { Header, Content } = AntLayout;

const Layout: React.FC = () => {
  const navigate = useNavigate();

  const menuItems = [
    { key: '/', label: 'Home page' },
    { key: '/trading', label: 'Trading' },
    { key: '/report', label: 'Report' },
  ];

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header>
        <div style={{ float: 'left', color: 'white', fontSize: '18px', marginRight: '24px' }}>
          AI Quantitative Trading Signal System
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Header>
      <Content style={{ padding: '24px' }}>
        <Outlet />
      </Content>
    </AntLayout>
  );
};

export default Layout; 