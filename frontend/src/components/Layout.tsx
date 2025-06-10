import React from "react";
import { Layout as AntLayout, Menu } from "antd";
import { Outlet, useNavigate, useLocation } from "react-router-dom";

const { Header, Content } = AntLayout;

const JPM_BLUE = "#003366";
const JPM_GRADIENT = "linear-gradient(90deg, #003366 0%, #00539B 100%)";

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { key: "/", label: "Home" },
    { key: "/trading", label: "Trading" },
    { key: "/report", label: "Report" },
  ];

  return (
    <AntLayout style={{ minHeight: "100vh", background: JPM_GRADIENT }}>
      <Header
        style={{
          background: JPM_GRADIENT,
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          padding: "0 32px",
          display: "flex",
          alignItems: "center",
        }}
      >
        <div
          style={{
            color: "#fff",
            fontSize: 22,
            fontWeight: 700,
            letterSpacing: 1,
            marginRight: 32,
            fontFamily: "Segoe UI, Arial, sans-serif",
            flex: "none",
          }}
        >
          CHASE
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{
            background: "transparent",
            fontWeight: 600,
            fontSize: 16,
            flex: 1,
            minWidth: 0,
          }}
        />
      </Header>
      <Content
        style={{
          padding: "32px",
          background: JPM_GRADIENT,
          minHeight: "calc(100vh - 64px)",
        }}
      >
        <Outlet />
      </Content>
    </AntLayout>
  );
};

export default Layout;
