import React, { useState, useEffect } from "react";
import { Card, Typography, Table, Tag } from "antd";
import ReactECharts from "echarts-for-react";
import { useNavigate, useLocation } from "react-router-dom";

const { Paragraph } = Typography;

/********************* MOCK Data Setup *******************************************/

// Add this mock data at the top of your file
const mockReportHistory: ReportRecord[] = [
  {
    id: "1",
    symbol: "AAPL",
    timestamp: new Date().toISOString(),
    analysisData: {
      final_report: {
        quant_analysis: {
          status: "success",
          symbol: "AAPL",
          strategy_name: "Momentum Strategy",
          live_signal: "BUY",
          key_metrics: {
            total_return: "15%",
            sharpe_ratio: 1.23,
            max_drawdown: "5%",
            win_rate: "60%",
            total_trades: 20,
            avg_trade_duration: "3d",
          },
          summary: {
            rating: "Good",
            recommendation: "Consider buying on dips.",
            key_strength: "Strong upward momentum.",
            main_weakness: "Sensitive to market corrections.",
          },
          is_satisfactory: true,
        },
        market_sentiment: {
          overall_sentiment: "positive",
          sentiment_score: 0.75,
          confidence: 0.92,
        },
        ai_analysis: "The asset shows strong momentum and positive sentiment.",
        generated_at: new Date().toLocaleString(),
      },
    },
  },
  {
    id: "2",
    symbol: "TEST1",
    timestamp: new Date().toISOString(),
    analysisData: {
      final_report: {
        quant_analysis: {
          status: "success",
          symbol: "AAPL",
          strategy_name: "Momentum Strategy",
          live_signal: "BUY",
          key_metrics: {
            total_return: "15%",
            sharpe_ratio: 1.23,
            max_drawdown: "5%",
            win_rate: "60%",
            total_trades: 20,
            avg_trade_duration: "3d",
          },
          summary: {
            rating: "Good",
            recommendation: "Consider buying on dips.",
            key_strength: "Strong upward momentum.",
            main_weakness: "Sensitive to market corrections.",
          },
          is_satisfactory: true,
        },
        market_sentiment: {
          overall_sentiment: "positive",
          sentiment_score: 0.75,
          confidence: 0.92,
        },
        ai_analysis: "The asset shows strong momentum and positive sentiment.",
        generated_at: new Date().toLocaleString(),
      },
    },
  },
  {
    id: "3",
    symbol: "TEST3",
    timestamp: new Date().toISOString(),
    analysisData: {
      final_report: {
        quant_analysis: {
          status: "success",
          symbol: "AAPL",
          strategy_name: "Momentum Strategy",
          live_signal: "BUY",
          key_metrics: {
            total_return: "15%",
            sharpe_ratio: 1.23,
            max_drawdown: "5%",
            win_rate: "60%",
            total_trades: 20,
            avg_trade_duration: "3d",
          },
          summary: {
            rating: "Good",
            recommendation: "Consider buying on dips.",
            key_strength: "Strong upward momentum.",
            main_weakness: "Sensitive to market corrections.",
          },
          is_satisfactory: true,
        },
        market_sentiment: {
          overall_sentiment: "positive",
          sentiment_score: 0.75,
          confidence: 0.92,
        },
        ai_analysis: "The asset shows strong momentum and positive sentiment.",
        generated_at: new Date().toLocaleString(),
      },
    },
  },
  {
    id: "4",
    symbol: "TEST4",
    timestamp: new Date().toISOString(),
    analysisData: {
      final_report: {
        quant_analysis: {
          status: "success",
          symbol: "AAPL",
          strategy_name: "Momentum Strategy",
          live_signal: "BUY",
          key_metrics: {
            total_return: "15%",
            sharpe_ratio: 1.23,
            max_drawdown: "5%",
            win_rate: "60%",
            total_trades: 20,
            avg_trade_duration: "3d",
          },
          summary: {
            rating: "Good",
            recommendation: "Consider buying on dips.",
            key_strength: "Strong upward momentum.",
            main_weakness: "Sensitive to market corrections.",
          },
          is_satisfactory: true,
        },
        market_sentiment: {
          overall_sentiment: "positive",
          sentiment_score: 0.75,
          confidence: 0.92,
        },
        ai_analysis: "The asset shows strong momentum and positive sentiment.",
        generated_at: new Date().toLocaleString(),
      },
    },
  },
  {
    id: "5",
    symbol: "TEST5",
    timestamp: new Date().toISOString(),
    analysisData: {
      final_report: {
        quant_analysis: {
          status: "success",
          symbol: "AAPL",
          strategy_name: "Momentum Strategy",
          live_signal: "BUY",
          key_metrics: {
            total_return: "15%",
            sharpe_ratio: 1.23,
            max_drawdown: "5%",
            win_rate: "60%",
            total_trades: 20,
            avg_trade_duration: "3d",
          },
          summary: {
            rating: "Good",
            recommendation: "Consider buying on dips.",
            key_strength: "Strong upward momentum.",
            main_weakness: "Sensitive to market corrections.",
          },
          is_satisfactory: true,
        },
        market_sentiment: {
          overall_sentiment: "positive",
          sentiment_score: 0.75,
          confidence: 0.92,
        },
        ai_analysis: "The asset shows strong momentum and positive sentiment.",
        generated_at: new Date().toLocaleString(),
      },
    },
  },
  {
    id: "6",
    symbol: "TEST7",
    timestamp: new Date().toISOString(),
    analysisData: {
      final_report: {
        quant_analysis: {
          status: "success",
          symbol: "AAPL",
          strategy_name: "Momentum Strategy",
          live_signal: "BUY",
          key_metrics: {
            total_return: "15%",
            sharpe_ratio: 1.23,
            max_drawdown: "5%",
            win_rate: "60%",
            total_trades: 20,
            avg_trade_duration: "3d",
          },
          summary: {
            rating: "Good",
            recommendation: "Consider buying on dips.",
            key_strength: "Strong upward momentum.",
            main_weakness: "Sensitive to market corrections.",
          },
          is_satisfactory: true,
        },
        market_sentiment: {
          overall_sentiment: "positive",
          sentiment_score: 0.75,
          confidence: 0.92,
        },
        ai_analysis: "The asset shows strong momentum and positive sentiment.",
        generated_at: new Date().toLocaleString(),
      },
    },
  },
];

/********************* MOCK Data Setup *******************************************/

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

const sentimentColor = (sentiment: string) => {
  if (sentiment === "positive") return "#52c41a";
  if (sentiment === "negative") return "#ff4d4f";
  return "#faad14";
};

interface ReportRecord {
  id: string;
  symbol: string;
  timestamp: string;
  analysisData: AnalysisData;
}

const Report: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  /****************** mock setup *************************** */
  /*const [reportHistory, setReportHistory] = useState<ReportRecord[]>([]);
  const [selectedReport, setSelectedReport] = useState<ReportRecord | null>(
    null
  );*/

  // Use mock data for testing
  const [reportHistory, setReportHistory] =
    useState<ReportRecord[]>(mockReportHistory);
  const [selectedReport, setSelectedReport] = useState<ReportRecord | null>(
    mockReportHistory[0]
  );

  /*****************mock setup **************************** */

  // load history report
  /*useEffect(() => {
    const history = JSON.parse(localStorage.getItem("reportHistory") || "[]");
    setReportHistory(
      history.sort(
        (a: ReportRecord, b: ReportRecord) =>
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      )
    );
  }, []);
  */

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
        analysisData,
      };

      const updatedHistory = [newReport, ...reportHistory];
      localStorage.setItem("reportHistory", JSON.stringify(updatedHistory));
      setReportHistory(updatedHistory);
      setSelectedReport(newReport);
    }
  }, [location.state]);

  // if there is no history record
  if (reportHistory.length === 0) {
    return (
      <div style={{ padding: "20px" }}>
        <div
          style={{
            background: "#fff",
            borderRadius: 16,
            boxShadow: "0 4px 24px #e3eafc",
            padding: 32,
            maxWidth: 600,
            margin: "40px auto",
          }}
        >
          <div
            style={{ display: "flex", alignItems: "center", marginBottom: 16 }}
          >
            <button
              onClick={() => navigate("/")}
              style={{
                marginRight: 16,
                background: "none",
                border: "none",
                color: "#1976d2",
                fontSize: 18,
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
              }}
            >
              &#8592; Back
            </button>
            <h2 style={{ margin: 0, fontWeight: 700, color: "#1976d2" }}>
              Trading Report
            </h2>
          </div>
          <p style={{ fontSize: 16, color: "#555", margin: 0 }}>
            No analysis history available. Please go back to the Trading page to
            generate a new analysis.
          </p>
        </div>
      </div>
    );
  }

  // render report content
  const renderReportContent = (report: ReportRecord) => {
    const { analysisData, symbol, timestamp } = report;
    const finalReport = analysisData.final_report;

    return (
      <>
        {/* Trading Report Header */}
        <div
          style={{
            marginBottom: 32,
            boxShadow: "0 4px 24px #e3eafc",
            background: "#fff",
            borderRadius: 16,
            padding: "32px 32px 24px 32px",
            display: "flex",
            alignItems: "center",
            minHeight: 100,
            position: "relative",
          }}
        >
          <div style={{ flex: 1 }}>
            <h3
              style={{
                margin: 0,
                color: "#1976d2",
                fontWeight: 500,
                fontSize: 24,
                lineHeight: 1.2,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <span>Stock Symbol</span>
              <span
                style={{ color: "grey", fontWeight: 400, fontStyle: "italic" }}
              >
                {symbol}
              </span>
            </h3>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginTop: 18,
                fontSize: 15,
                color: "#555",
                fontWeight: 500,
              }}
            >
              <span>
                <i>Analysis Time:</i> {new Date(timestamp).toLocaleString()}
              </span>
              <span>
                <i>Generated Time:</i> {finalReport.generated_at}
              </span>
            </div>
          </div>
        </div>

        {/* Market Sentiment & Trading Signal Analysis */}
        <div
          style={{
            marginBottom: 24,
            boxShadow: "0 4px 24px #e3eafc",
            background: "#fff",
            borderRadius: 16,
            padding: "6px 28px",
          }}
        >
          <ReactECharts
            option={{
              title: {
                text: `${symbol} Sentiment vs Signal Analysis`,
                left: "center",
                top: 30,
                padding: [16, 0, 16, 0],
                textStyle: {
                  color: "#1976d2",
                  fontWeight: 700,
                  fontSize: 24,
                  lineHeight: 1.2,
                  margin: "0 0 28px 0",
                  letterSpacing: 1.5,
                  textAlign: "center",
                },
              },
              tooltip: {
                trigger: "item",
                formatter: function (params: any) {
                  if (params.seriesType === "gauge") {
                    return `${params.seriesName}<br/>${params.name}: ${params.value}`;
                  }
                  return `${params.name}: ${params.value}`;
                },
              },
              series: [
                // market sentiment score gauge
                {
                  name: "Market Sentiment Score",
                  type: "gauge",
                  center: ["25%", "50%"],
                  radius: "60%",
                  min: -100,
                  max: 100,
                  splitNumber: 10,
                  axisLine: {
                    lineStyle: {
                      color: [
                        [0.3, "#fd666d"], // negative sentiment area
                        [0.7, "#fac858"], // neutral sentiment area
                        [1, "#67e0e3"], // positive sentiment area
                      ],
                      width: 8,
                    },
                  },
                  pointer: {
                    itemStyle: {
                      color: "inherit",
                    },
                  },
                  axisTick: {
                    distance: -30,
                    length: 8,
                    lineStyle: {
                      color: "#fff",
                      width: 2,
                    },
                  },
                  splitLine: {
                    distance: -30,
                    length: 30,
                    lineStyle: {
                      color: "#fff",
                      width: 4,
                    },
                  },
                  axisLabel: {
                    color: "inherit",
                    distance: 40,
                    fontSize: 12,
                    formatter: function (value: number) {
                      if (value <= -50) return "Negative";
                      if (value >= 50) return "Positive";
                      return "Neutral";
                    },
                  },
                  detail: {
                    valueAnimation: true,
                    formatter: "{value}",
                    color: "inherit",
                  },
                  data: [
                    {
                      value: Math.round(
                        finalReport.market_sentiment.sentiment_score * 100
                      ),
                      name: "Sentiment",
                    },
                  ],
                },
                // trading signal indicator
                {
                  name: "Trading Signal",
                  type: "gauge",
                  center: ["75%", "50%"],
                  radius: "60%",
                  min: -1,
                  max: 1,
                  splitNumber: 4,
                  axisLine: {
                    lineStyle: {
                      color: [
                        [0.25, "#fd666d"], // SELL area
                        [0.75, "#fac858"], // HOLD area
                        [1, "#67e0e3"], // BUY area
                      ],
                      width: 8,
                    },
                  },
                  axisLabel: {
                    distance: 40,
                    fontSize: 12,
                    formatter: function (value: number) {
                      if (value <= -0.5) return "SELL";
                      if (value >= 0.5) return "BUY";
                      return "HOLD";
                    },
                  },
                  detail: {
                    valueAnimation: true,
                    formatter: function (value: number) {
                      if (value <= -0.5) return "SELL";
                      if (value >= 0.5) return "BUY";
                      return "HOLD";
                    },
                    color: "inherit",
                    fontSize: 20,
                    fontWeight: "bold",
                  },
                  data: [
                    {
                      value:
                        finalReport.quant_analysis.live_signal === "BUY"
                          ? 0.8
                          : finalReport.quant_analysis.live_signal === "SELL"
                          ? -0.8
                          : 0,
                      name: "Signal",
                    },
                  ],
                },
              ],
            }}
            style={{ height: "400px" }}
          />
        </div>

        {/* Strategy Overview */}
        <div
          style={{
            marginBottom: 32,
            boxShadow: "0 4px 24px #e3eafc",
            background: "#fff",
            borderRadius: 16,
            padding: "32px 48px",
            maxWidth: 1000,
            marginLeft: "auto",
            marginRight: "auto",
          }}
        >
          <h4
            style={{
              margin: "0 0 28px 0",
              color: "#1976d2",
              fontWeight: 700,
              fontSize: 24,
              letterSpacing: 1,
              textAlign: "center",
              lineHeight: 1.2,
            }}
          >
            Strategy Overview
          </h4>
          <table
            style={{
              width: "100%",
              borderCollapse: "separate",
              borderSpacing: 0,
              background: "#f8fbff",
              borderRadius: 12,
              overflow: "hidden",
              marginBottom: 24,
              boxShadow: "0 2px 8px #e3eafc",
            }}
          >
            <thead>
              <tr>
                <th
                  style={{
                    textAlign: "left",
                    padding: "14px 18px",
                    background: "#e6f0fa",
                    color: "#1976d2",
                    fontWeight: 700,
                    fontSize: 16,
                    letterSpacing: 1,
                    borderBottom: "1px solid #e3eafc",
                  }}
                >
                  Attribute
                </th>
                <th
                  style={{
                    textAlign: "right",
                    padding: "14px 18px",
                    background: "#e6f0fa",
                    color: "#1976d2",
                    fontWeight: 700,
                    fontSize: 16,
                    letterSpacing: 1,
                    borderBottom: "1px solid #e3eafc",
                  }}
                >
                  Value
                </th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  label: "Strategy",
                  value: finalReport.quant_analysis.strategy_name,
                },
                {
                  label: "Live Signal",
                  value: (
                    <span
                      style={{
                        display: "inline-block",
                        padding: "2px 18px",
                        borderRadius: 8,
                        background:
                          finalReport.quant_analysis.live_signal === "BUY"
                            ? "#e6f9ed"
                            : finalReport.quant_analysis.live_signal === "SELL"
                            ? "#ffeaea"
                            : "#fffbe6",
                        color:
                          finalReport.quant_analysis.live_signal === "BUY"
                            ? "#52c41a"
                            : finalReport.quant_analysis.live_signal === "SELL"
                            ? "#ff4d4f"
                            : "#faad14",
                        fontWeight: 700,
                        fontSize: 16,
                        letterSpacing: 1,
                      }}
                    >
                      {finalReport.quant_analysis.live_signal}
                    </span>
                  ),
                },
                {
                  label: "Rating",
                  value: (
                    <span
                      style={{
                        display: "inline-block",
                        padding: "2px 18px",
                        borderRadius: 8,
                        background:
                          finalReport.quant_analysis.summary.rating === "Poor"
                            ? "#ffeaea"
                            : "#e6f9ed",
                        color:
                          finalReport.quant_analysis.summary.rating === "Poor"
                            ? "#ff4d4f"
                            : "#52c41a",
                        fontWeight: 700,
                        fontSize: 16,
                        letterSpacing: 1,
                      }}
                    >
                      {finalReport.quant_analysis.summary.rating}
                    </span>
                  ),
                },
                {
                  label: "Recommendation",
                  value: (
                    <span
                      style={{
                        color: "#1976d2",
                        fontWeight: 600,
                        fontSize: 16,
                        textAlign: "right",
                      }}
                    >
                      {finalReport.quant_analysis.summary.recommendation}
                    </span>
                  ),
                },
              ].map((row, idx) => (
                <tr
                  key={row.label}
                  style={{
                    background: idx % 2 === 0 ? "#f8fbff" : "#f2f6fb",
                    transition: "background 0.2s",
                  }}
                >
                  <td
                    style={{
                      padding: "12px 18px",
                      color: "#555",
                      fontWeight: 600,
                      minWidth: 140,
                    }}
                  >
                    {row.label}
                  </td>
                  <td
                    style={{
                      padding: "12px 18px",
                      textAlign: "right",
                      color: "#222",
                      fontWeight: 700,
                    }}
                  >
                    {row.value}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Quantitative Analysis */}

        <div
          style={{
            marginBottom: 32,
            boxShadow: "0 4px 24px #e3eafc",
            background: "#fff",
            borderRadius: 16,
            padding: "32px 48px", // more horizontal padding
            maxWidth: 1000, // match main content width
            marginLeft: "auto",
            marginRight: "auto",
          }}
        >
          <h4
            style={{
              margin: "0 0 28px 0",
              color: "#1976d2",
              fontWeight: 700,
              fontSize: 24,
              letterSpacing: 1,
              textAlign: "center",
              lineHeight: 1.2,
            }}
          >
            Quantitative Analysis
          </h4>
          <table
            style={{
              width: "100%",
              borderCollapse: "separate",
              borderSpacing: 0,
              background: "#f8fbff",
              borderRadius: 12,
              overflow: "hidden",
              marginBottom: 24,
              boxShadow: "0 2px 8px #e3eafc",
            }}
          >
            <thead>
              <tr>
                <th
                  style={{
                    textAlign: "left",
                    padding: "14px 18px",
                    background: "#e6f0fa",
                    color: "#1976d2",
                    fontWeight: 700,
                    fontSize: 16,
                    letterSpacing: 1,
                    borderBottom: "1px solid #e3eafc",
                  }}
                >
                  Metric
                </th>
                <th
                  style={{
                    textAlign: "right",
                    padding: "14px 18px",
                    background: "#e6f0fa",
                    color: "#1976d2",
                    fontWeight: 700,
                    fontSize: 16,
                    letterSpacing: 1,
                    borderBottom: "1px solid #e3eafc",
                  }}
                >
                  Value
                </th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  label: "Total Return",
                  value: finalReport.quant_analysis.key_metrics.total_return,
                },
                {
                  label: "Sharpe Ratio",
                  value:
                    finalReport.quant_analysis.key_metrics.sharpe_ratio.toFixed(
                      2
                    ),
                },
                {
                  label: "Max Drawdown",
                  value: finalReport.quant_analysis.key_metrics.max_drawdown,
                },
                {
                  label: "Win Rate",
                  value: finalReport.quant_analysis.key_metrics.win_rate,
                },
                ...(finalReport.quant_analysis.key_metrics.total_trades
                  ? [
                      {
                        label: "Total Trades",
                        value:
                          finalReport.quant_analysis.key_metrics.total_trades,
                      },
                    ]
                  : []),
                ...(finalReport.quant_analysis.key_metrics.avg_trade_duration
                  ? [
                      {
                        label: "Avg Trade Duration",
                        value:
                          finalReport.quant_analysis.key_metrics
                            .avg_trade_duration,
                      },
                    ]
                  : []),
              ].map((row, idx) => (
                <tr
                  key={row.label}
                  style={{
                    background: idx % 2 === 0 ? "#f8fbff" : "#f2f6fb",
                    transition: "background 0.2s",
                  }}
                >
                  <td
                    style={{
                      padding: "12px 18px",
                      color: "#555",
                      fontWeight: 600,
                    }}
                  >
                    {row.label}
                  </td>
                  <td
                    style={{
                      padding: "12px 18px",
                      textAlign: "right",
                      color: "#222",
                      fontWeight: 700,
                    }}
                  >
                    {row.value}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div
            style={{
              marginTop: 8,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 16,
              flexWrap: "wrap",
            }}
          >
            <div style={{ color: "#1976d2", fontWeight: 600, fontSize: 16 }}>
              <span style={{ color: "#555" }}>Key Strength:</span>{" "}
              {finalReport.quant_analysis.summary.key_strength}
            </div>
            <div
              style={{
                color: "#ff4d4f",
                fontWeight: 600,
                fontSize: 16,
                textAlign: "right",
              }}
            >
              <span style={{ color: "#555" }}>Main Weakness:</span>{" "}
              {finalReport.quant_analysis.summary.main_weakness}
            </div>
          </div>
        </div>

        {/* Market Sentiment */}
        <div
          style={{
            marginBottom: 24,
            boxShadow: "0 4px 24px #e3eafc",
            background: "#fff",
            borderRadius: 16,
            padding: "32px 48px",
            maxWidth: 1000,
            marginLeft: "auto",
            marginRight: "auto",
          }}
        >
          <h4
            style={{
              margin: "0 0 28px 0",
              color: "#1976d2",
              fontWeight: 700,
              fontSize: 24,
              letterSpacing: 1,
              textAlign: "center",
              lineHeight: 1.2,
            }}
          >
            Market Sentiment
          </h4>
          <table
            style={{
              width: "100%",
              borderCollapse: "separate",
              borderSpacing: 0,
              background: "#f8fbff",
              borderRadius: 12,
              overflow: "hidden",
              marginBottom: 16,
              boxShadow: "0 2px 8px #e3eafc",
            }}
          >
            <thead>
              <tr>
                <th
                  style={{
                    textAlign: "left",
                    padding: "14px 18px",
                    background: "#e6f0fa",
                    color: "#1976d2",
                    fontWeight: 700,
                    fontSize: 16,
                    letterSpacing: 1,
                    borderBottom: "1px solid #e3eafc",
                  }}
                >
                  Attribute
                </th>
                <th
                  style={{
                    textAlign: "right",
                    padding: "14px 18px",
                    background: "#e6f0fa",
                    color: "#1976d2",
                    fontWeight: 700,
                    fontSize: 16,
                    letterSpacing: 1,
                    borderBottom: "1px solid #e3eafc",
                  }}
                >
                  Value
                </th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  label: "Overall Sentiment",
                  value: (
                    <span
                      style={{
                        display: "inline-block",
                        padding: "2px",
                        borderRadius: 8,
                        background:
                          finalReport.market_sentiment.overall_sentiment ===
                          "positive"
                            ? "#e6f9ed"
                            : finalReport.market_sentiment.overall_sentiment ===
                              "negative"
                            ? "#ffeaea"
                            : "#fffbe6",
                        color:
                          finalReport.market_sentiment.overall_sentiment ===
                          "positive"
                            ? "#52c41a"
                            : finalReport.market_sentiment.overall_sentiment ===
                              "negative"
                            ? "#ff4d4f"
                            : "#faad14",
                        fontWeight: 700,
                        fontSize: 16,
                        letterSpacing: 1,
                        textTransform: "capitalize",
                      }}
                    >
                      {finalReport.market_sentiment.overall_sentiment}
                    </span>
                  ),
                },
                {
                  label: "Sentiment Score",
                  value: finalReport.market_sentiment.sentiment_score,
                },
                {
                  label: "Confidence",
                  value: `${(
                    finalReport.market_sentiment.confidence * 100
                  ).toFixed(1)}%`,
                },
              ].map((row, idx) => (
                <tr
                  key={row.label}
                  style={{
                    background: idx % 2 === 0 ? "#f8fbff" : "#f2f6fb",
                    transition: "background 0.2s",
                  }}
                >
                  <td
                    style={{
                      padding: "12px 18px",
                      color: "#555",
                      fontWeight: 600,
                      minWidth: 140,
                    }}
                  >
                    {row.label}
                  </td>
                  <td
                    style={{
                      padding: "12px 18px",
                      textAlign: "right",
                      color: "#222",
                      fontWeight: 700,
                    }}
                  >
                    {row.value}
                  </td>
                </tr>
              ))}
              {finalReport.market_sentiment.error && (
                <tr>
                  <td
                    style={{
                      padding: "12px 18px",
                      color: "#ff4d4f",
                      fontWeight: 600,
                      minWidth: 140,
                    }}
                  >
                    Note
                  </td>
                  <td
                    style={{
                      padding: "12px 18px",
                      textAlign: "right",
                      color: "#ff4d4f",
                      fontWeight: 700,
                    }}
                  >
                    {finalReport.market_sentiment.error}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* AI Analysis Report */}
        <div
          style={{
            marginBottom: 32,
            boxShadow: "0 4px 24px #e3eafc",
            background: "#fff",
            borderRadius: 16,
            padding: "32px 48px",
            maxWidth: 1000,
            marginLeft: "auto",
            marginRight: "auto",
          }}
        >
          <h4
            style={{
              margin: "0 0 28px 0",
              color: "#1976d2",
              fontWeight: 700,
              fontSize: 24,
              letterSpacing: 1,
              textAlign: "center",
              lineHeight: 1.2,
            }}
          >
            AI Analysis Report
          </h4>
          <div
            style={{
              whiteSpace: "pre-wrap",
              lineHeight: "1.7",
              background: "#f8fbff",
              padding: "24px 28px",
              borderRadius: 12,
              border: "1px solid #e3eafc",
              color: "#222",
              fontSize: 17,
              fontWeight: 500,
              boxShadow: "0 1px 4px #e3eafc",
              minHeight: 80,
            }}
          >
            {finalReport.ai_analysis}
          </div>
        </div>
      </>
    );
  };

  return (
    <div style={{ maxWidth: 1400, margin: "0 auto", padding: "20px" }}>
      {/* Header */}
      <div
        style={{
          marginBottom: 24,
          boxShadow: "0 4px 24px #e3eafc",
          borderRadius: 16,
          background: "#fff",
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: 120,
        }}
      >
        <button
          onClick={() => navigate("/")}
          style={{
            background: "none",
            border: "none",
            color: "#1976d2",
            fontSize: 18,
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
          }}
        >
          <span style={{ fontSize: 20, marginLeft: 6 }}>&#8592;&nbsp;</span>
          <strong>Back</strong>
        </button>
        <h2
          style={{
            margin: 0,
            color: "#1976d2",
            fontWeight: 800,
            textAlign: "center",
            width: "100%",
            fontSize: 26,
            letterSpacing: 1,
            lineHeight: 1.2,
          }}
        >
          JPMorgan's AI Powered - Trading Report
        </h2>
      </div>

      <div
        style={{
          display: "flex",
          gap: 32,
          alignItems: "flex-start",
          maxWidth: 1400,
          margin: "0 auto",
        }}
      >
        {/* Left menu */}
        <div
          style={{
            width: 340,
            background: "#fff",
            borderRadius: 16,
            boxShadow: "0 4px 24px #e3eafc",
            padding: "24px 0",
            minHeight: "100vh", // extend to bottom of page
            height: "100vh", // ensure full viewport height
            position: "sticky",
            top: 0,
            alignSelf: "flex-start",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <h2
            style={{
              margin: "0 0 24px 32px",
              color: "#1976d2",
              fontWeight: 700,
              fontSize: 22,
              letterSpacing: 1,
            }}
          >
            Report History
          </h2>
          <div>
            {reportHistory.map((report) => {
              const isSelected = selectedReport?.id === report.id;
              return (
                <div
                  key={report.id}
                  onClick={() => setSelectedReport(report)}
                  style={{
                    cursor: "pointer",
                    background: isSelected ? "#e6f0fa" : "transparent",
                    borderLeft: isSelected
                      ? "4px solid #1976d2"
                      : "4px solid transparent",
                    padding: "14px 24px",
                    margin: "0 0 8px 0",
                    borderRadius: "0 12px 12px 0",
                    transition: "all 0.2s",
                    boxShadow: isSelected ? "0 2px 8px #e3f0fc" : "none",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <span
                    style={{
                      display: "inline-block",
                      minWidth: 48,
                      textAlign: "center",
                      fontWeight: 700,
                      fontSize: 16,
                      letterSpacing: 1,
                      borderRadius: 6,
                      padding: "4px 0",
                      background: isSelected ? "#1976d2" : "#e6f0fa",
                      color: isSelected ? "#fff" : "#1976d2",
                      marginRight: 16,
                    }}
                  >
                    {report.symbol}
                  </span>
                  <span
                    style={{
                      fontSize: 13,
                      color: "#888",
                      marginRight: 8,
                      textAlign: "center",
                      flex: 1,
                    }}
                  >
                    {new Date(report.timestamp).toLocaleString()}
                  </span>
                  <span
                    style={{
                      fontSize: 13,
                      color: sentimentColor(
                        report.analysisData.final_report.market_sentiment
                          .overall_sentiment
                      ),
                      fontWeight: 600,
                      textTransform: "capitalize",
                    }}
                  >
                    {
                      report.analysisData.final_report.market_sentiment
                        .overall_sentiment
                    }
                  </span>
                </div>
              );
            })}
          </div>
        </div>
        {/* Main content */}
        <div style={{ flex: 1, minWidth: 320 }}>
          {selectedReport ? (
            renderReportContent(selectedReport)
          ) : (
            <div
              style={{
                background: "#fff",
                borderRadius: 16,
                boxShadow: "0 4px 24px #e3eafc",
                padding: 32,
                minHeight: 400,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 18,
                color: "#888",
              }}
            >
              Please select a report from the history to view its details.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Report;
