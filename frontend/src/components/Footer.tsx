import React from "react";
import { Typography } from "antd";

const { Link } = Typography;

const JPM_BLUE = "#003366";
const GOLD = "#FFD700";

const footerLinks = [
  { label: "Privacy", url: "https://www.jpmorgan.com/privacy" },
  { label: "Terms of Use", url: "https://www.jpmorgan.com/terms" },
  { label: "Accessibility", url: "https://www.jpmorgan.com/accessibility" },
  { label: "Cookies Policy", url: "https://www.jpmorgan.com/cookies" },
  {
    label: "Regulatory Disclosures",
    url: "https://www.jpmorgan.com/disclosures",
  },
];

const JPMFooter: React.FC = () => (
  <footer
    style={{
      background: "#002244",
      color: "#fff",
      borderRadius: 0,
      padding: "32px 16px 24px 16px",
      textAlign: "center",
      boxShadow: "0 2px 12px rgba(0,83,155,0.10)",
    }}
  >
    <div style={{ maxWidth: 900, margin: "0 auto" }}>
      <div style={{ marginTop: 18 }}>
        {footerLinks.map((item, idx) => (
          <React.Fragment key={item.label}>
            <Link
              href={item.url}
              target="_blank"
              style={{
                color: "#b0c4de",
                fontSize: 13,
                margin: "0 10px",
              }}
            >
              {item.label}
            </Link>
            {idx < footerLinks.length - 1 && (
              <span style={{ color: "#b0c4de" }}>|</span>
            )}
          </React.Fragment>
        ))}
      </div>
      <div style={{ marginTop: 18, color: "#b0c4de", fontSize: 13 }}>
        &copy; {new Date().getFullYear()} J.P. Morgan. All rights reserved.
      </div>
    </div>
  </footer>
);

export default JPMFooter;
