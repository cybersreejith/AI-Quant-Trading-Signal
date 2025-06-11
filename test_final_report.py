#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from core.tools.final_report_generation import ReportAgent

def test_simplified_final_report():
    """测试简化的最终报告生成"""
    
    print("🔍 正在测试简化的最终报告生成...")
    print("=" * 60)
    
    # 模拟量化分析结果
    mock_quant_analysis = {
        "symbol": "AAPL",
        "strategy_name": "Moving Average Crossover Strategy",
        "live_signal": "HOLD",
        "key_metrics": {
            "total_return": "-2.97%",
            "sharpe_ratio": -1.22,
            "max_drawdown": "-3.86%",
            "win_rate": "21.4%"
        },
        "summary": {
            "rating": "Poor",
            "recommendation": "不建议使用",
            "key_strength": "回撤控制良好",
            "main_weakness": "风险调整收益表现较差"
        },
        "is_satisfactory": False
    }
    
    # 模拟市场情绪分析结果
    mock_sentiment_analysis = {
        "overall_sentiment": "neutral",
        "sentiment_score": 0.0,
        "confidence": 0.8
    }
    
    try:
        # 创建ReportAgent实例并生成报告
        print("📊 生成最终报告...")
        agent = ReportAgent()
        result = agent.generate_report(mock_quant_analysis, mock_sentiment_analysis)
        
        # 展示结果
        print("📋 完整报告结构:")
        print("=" * 60)
        print(f"包含字段: {list(result.keys())}")
        print(f"量化分析数据: ✓" if 'quant_analysis' in result else "❌")
        print(f"市场情绪数据: ✓" if 'market_sentiment' in result else "❌")
        print(f"AI分析报告: ✓" if 'ai_analysis' in result else "❌")
        print(f"生成时间: {result.get('generated_at', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("📄 AI分析报告文本:")
        print(result.get('ai_analysis', 'N/A'))
        
        print("\n" + "=" * 60)
        print("📏 输出长度分析:")
        print(f"总结果长度: {len(str(result))} 字符")
        print(f"JSON格式长度: {len(json.dumps(result, ensure_ascii=False))} 字符")
        print(f"AI分析报告长度: {len(result.get('ai_analysis', ''))} 字符")
        
        print("\n" + "=" * 60)
        print("🔧 完整JSON结构:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simplified_final_report() 