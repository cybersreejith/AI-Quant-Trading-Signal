import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API密钥
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 邮件设置
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS').split(',')
EMAIL_SUBJECT = "交易分析报告"

# 日志设置
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 交易设置
TRADING_PAIRS = ['BTC-USD', 'ETH-USD', 'BNB-USD']
START_DATE = '2023-01-01'
END_DATE = '2024-01-01'
INITIAL_CAPITAL = 100000
POSITION_SIZE = 0.1  # 每次交易使用资金的10%
COMMISSION_RATE = 0.001  # 0.1%手续费
SLIPPAGE = 0.001  # 0.1%滑点

# 策略参数
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9
ADX_THRESHOLD = 25
ATR_MULTIPLIER = 2

# 数据配置
DEFAULT_TIMEFRAME = '1d'
DEFAULT_START_DATE = '2020-01-01'
DEFAULT_END_DATE = None  # 使用当前日期

# 回测配置
DEFAULT_INITIAL_CASH = 100000.0
DEFAULT_COMMISSION = 0.001  # 0.1%

# 策略参数
STRATEGY_PARAMS = {
    'ClassicTrendFollow': {
        'macd_fast': 12,
        'macd_slow': 26,
        'macd_signal': 9,
        'sma_short': 20,
        'sma_mid': 50,
        'sma_long': 200,
        'adx_period': 14,
        'adx_threshold': 25,
        'rsi_period': 14,
        'rsi_oversold': 30,
        'rsi_overbought': 70,
        'trailing_percent': 0.02,
        'profit_take': 0.05
    },
    'StrongStockPullback': {
        'rsi_period': 14,
        'sma_short': 50,
        'sma_long': 200,
        'adx_period': 14,
        'rsi_entry': 40,
        'rsi_exit': 70,
        'adx_threshold': 25
    },
    'MATrend': {
        'ema_short': 5,
        'ema_long': 20,
        'adx_period': 14,
        'adx_threshold': 25
    }
} 