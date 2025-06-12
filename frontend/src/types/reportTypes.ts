export interface FinalReport {
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

export interface AnalysisData {
  final_report: FinalReport;
}

export interface ReportRecord {
  id: string;
  symbol: string;
  timestamp: string;
  analysisData: AnalysisData;
}
