import React from "react";
import { ConfigProvider } from "antd";
import zhCN from "antd/locale/zh_CN";
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout_New";
import Home from "./pages/Home_New";
import Trading from "./pages/Trading_New";
import Report from "./pages/Report";
import JPMFooter from "./components/Footer";

const App: React.FC = () => {
  return (
    <ConfigProvider locale={zhCN}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="trading" element={<Trading />} />
          <Route path="report" element={<Report />} />
        </Route>
      </Routes>
      <JPMFooter />
    </ConfigProvider>
  );
};

export default App;
