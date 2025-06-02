from flask import Flask, request, jsonify
from flask_cors import CORS
from workflow import create_workflow_graph, WorkflowState
import logging
from utils.logger import setup_logger

# 配置日志
logger = setup_logger(__name__)

app = Flask(__name__)
CORS(app)  # 启用CORS支持

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # 获取请求数据
        data = request.get_json()
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({
                'status': 'error',
                'message': '未提供资产代码'
            }), 400
            
        # 创建工作流图实例
        workflow_graph = create_workflow_graph()
        
        # 初始化状态
        initial_state = WorkflowState(
            messages=[],
            symbol=symbol,
            historical_data=None,
            technical_data=None,
            trading_strategy=None,
            backtest_results=None,
            backtest_evaluation={"is_satisfactory": False},
            sentiment_analysis=None,
            final_report="",
            live_signal=None
        )
        
        # 运行工作流
        final_state = workflow_graph.invoke(initial_state)
        
        # 返回分析结果
        return jsonify({
            'status': 'success',
            'data': {
                'backtest_results': final_state.get('backtest_results'),
                'backtest_evaluation': final_state.get('backtest_evaluation'),
                'live_signal': final_state.get('live_signal'),
                'sentiment_analysis': final_state.get('sentiment_analysis'),
                'final_report': final_state.get('final_report')
            }
        })
        
    except Exception as e:
        logger.error(f"分析请求处理失败: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 