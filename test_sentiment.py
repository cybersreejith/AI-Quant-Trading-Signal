#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from core.tools.finance_market_sentiment_analyse import analyze_market_sentiment

def test_sentiment_analysis():
    """测试情感分析功能并查看返回结果"""
    
    print("🔍 正在测试AAPL的市场情绪分析...")
    print("=" * 50)
    
    try:
        # 调用情感分析
        result = analyze_market_sentiment('AAPL')
        
        # 打印结果
        print("📊 分析结果:")
        print(f"总体情绪: {result.get('overall_sentiment', 'N/A')}")
        print(f"情绪分数: {result.get('sentiment_score', 'N/A')}")
        print(f"置信度: {result.get('confidence', 'N/A')}")
        print(f"关键点: {result.get('key_points', 'N/A')}")
        print(f"新闻摘要: {result.get('news_summary', 'N/A')}")
        
        print("\n" + "=" * 50)
        print("📏 输出长度分析:")
        print(f"总结果长度: {len(str(result))} 字符")
        print(f"JSON格式长度: {len(json.dumps(result, ensure_ascii=False))} 字符")
        
        print("\n" + "=" * 50)
        print("🔧 完整JSON结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sentiment_analysis() 