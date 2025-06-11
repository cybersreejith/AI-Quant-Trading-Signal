#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from core.tools.strategy_generation import generate_strategy
from core.tools.backtest import quant_analysis

def test_simplified_quant_analysis():
    """测试简化的量化分析输出"""
    
    print("🔍 正在测试简化的量化分析...")
    print("=" * 60)
    
    try:
        # 1. 生成交易策略
        print("📈 生成交易策略...")
        strategy = generate_strategy()
        
        # 2. 运行量化分析
        print("🔬 运行量化分析...")
        result = quant_analysis('AAPL', strategy)
        
        # 3. 展示简化结果
        print("📊 简化分析结果:")
        print(f"状态: {result.get('status', 'N/A')}")
        print(f"股票代码: {result.get('symbol', 'N/A')}")
        print(f"策略名称: {result.get('strategy_name', 'N/A')}")
        print(f"实时信号: {result.get('live_signal', 'N/A')}")
        
        print("\n💡 核心指标:")
        key_metrics = result.get('key_metrics', {})
        for metric, value in key_metrics.items():
            print(f"  • {metric}: {value}")
        
        print("\n📋 策略总结:")
        summary = result.get('summary', {})
        for key, value in summary.items():
            print(f"  • {key}: {value}")
        
        print(f"\n✅ 是否满足要求: {result.get('is_satisfactory', False)}")
        
        print("\n" + "=" * 60)
        print("📏 输出长度分析:")
        print(f"总结果长度: {len(str(result))} 字符")
        print(f"JSON格式长度: {len(json.dumps(result, ensure_ascii=False))} 字符")
        
        print("\n" + "=" * 60)
        print("🔧 完整JSON结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simplified_quant_analysis() 