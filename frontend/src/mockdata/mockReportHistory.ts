import { ReportRecord } from "../types/reportTypes";

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
export default mockReportHistory;
