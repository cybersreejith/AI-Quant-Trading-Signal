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

# 热门资产列表
POPULAR_ASSETS = {
    '1': {  # 全球股票
        'name': '全球股票',
        'assets': [
            'AAPL',  # 苹果
            'MSFT',  # 微软
            'GOOGL', # 谷歌
            'AMZN',  # 亚马逊
            'META',  # Meta
            'NVDA',  # 英伟达
            'TSLA',  # 特斯拉
            'BABA',  # 阿里巴巴
            'PDD',   # 拼多多
            'NIO',   # 蔚来
            'JPM',   # 摩根大通
            'V',     # Visa
            'WMT',   # 沃尔玛
            'MA',    # 万事达
            'HD',    # 家得宝
            'BAC',   # 美国银行
            'XOM',   # 埃克森美孚
            'PFE',   # 辉瑞
            'AVGO',  # 博通
            'COST',  # 好市多
            'TMO',   # 赛默飞世尔
            'CSCO',  # 思科
            'DHR',   # 丹纳赫
            'ABBV',  # 艾伯维
            'WFC',   # 富国银行
            'MRK',   # 默克
            'VZ',    # 威瑞森
            'NKE',   # 耐克
            'CRM',   # Salesforce
            'NEE'    # NextEra Energy
        ]
    },
    '2': {  # ETF
        'name': 'ETF',
        'assets': [
            'SPY',   # 标普500ETF
            'QQQ',   # 纳斯达克100ETF
            'DIA',   # 道琼斯ETF
            'IWM',   # 罗素2000ETF
            'EFA',   # 发达市场ETF
            'EEM',   # 新兴市场ETF
            'GLD',   # 黄金ETF
            'SLV',   # 白银ETF
            'TLT',   # 20年期国债ETF
            'VNQ',   # 房地产ETF
            'XLK',   # 科技ETF
            'XLF',   # 金融ETF
            'XLE',   # 能源ETF
            'XLV',   # 医疗保健ETF
            'XLI',   # 工业ETF
            'XLP',   # 消费品ETF
            'XLY',   # 非必需消费品ETF
            'XLB',   # 材料ETF
            'XLU',   # 公用事业ETF
            'XBI',   # 生物科技ETF
            'ARKK',  # ARK创新ETF
            'IEFA',  # 发达市场ETF
            'IEMG',  # 新兴市场ETF
            'AGG',   # 美国综合债券ETF
            'LQD',   # 投资级公司债ETF
            'HYG',   # 高收益债券ETF
            'GDX',   # 金矿ETF
            'GDXJ',  # 小型金矿ETF
            'USO',   # 原油ETF
            'UNG'    # 天然气ETF
        ]
    },
    '3': {  # 外汇
        'name': '外汇',
        'assets': [
            'EURUSD=X',  # 欧元/美元
            'GBPUSD=X',  # 英镑/美元
            'USDJPY=X',  # 美元/日元
            'AUDUSD=X',  # 澳元/美元
            'USDCAD=X',  # 美元/加元
            'NZDUSD=X',  # 新西兰元/美元
            'USDCHF=X',  # 美元/瑞郎
            'EURGBP=X',  # 欧元/英镑
            'EURJPY=X',  # 欧元/日元
            'GBPJPY=X',  # 英镑/日元
            'EURCAD=X',  # 欧元/加元
            'AUDJPY=X',  # 澳元/日元
            'NZDJPY=X',  # 新西兰元/日元
            'GBPAUD=X',  # 英镑/澳元
            'EURAUD=X',  # 欧元/澳元
            'USDSGD=X',  # 美元/新加坡元
            'USDHKD=X',  # 美元/港币
            'EURCHF=X',  # 欧元/瑞郎
            'GBPCHF=X',  # 英镑/瑞郎
            'AUDNZD=X',  # 澳元/新西兰元
            'CADJPY=X',  # 加元/日元
            'CHFJPY=X',  # 瑞郎/日元
            'EURCAD=X',  # 欧元/加元
            'GBPNZD=X',  # 英镑/新西兰元
            'AUDCAD=X',  # 澳元/加元
            'NZDCHF=X',  # 新西兰元/瑞郎
            'CADCHF=X',  # 加元/瑞郎
            'EURHKD=X',  # 欧元/港币
            'GBPHKD=X',  # 英镑/港币
            'AUDHKD=X'   # 澳元/港币
        ]
    },
    '4': {  # 加密货币
        'name': '加密货币',
        'assets': [
            'BTC-USD',  # 比特币
            'ETH-USD',  # 以太坊
            'BNB-USD',  # 币安币
            'XRP-USD',  # 瑞波币
            'ADA-USD',  # 卡尔达诺
            'DOGE-USD', # 狗狗币
            'DOT-USD',  # 波卡
            'SOL-USD',  # 索拉纳
            'AVAX-USD', # Avalanche
            'MATIC-USD',# Polygon
            'LINK-USD', # Chainlink
            'UNI-USD',  # Uniswap
            'AAVE-USD', # Aave
            'COMP-USD', # Compound
            'SUSHI-USD',# SushiSwap
            'YFI-USD',  # Yearn Finance
            'SNX-USD',  # Synthetix
            'MKR-USD',  # Maker
            'CRV-USD',  # Curve
            'BAL-USD',  # Balancer
            'SXP-USD',  # SXP
            'CAKE-USD', # PancakeSwap
            'RUNE-USD', # THORChain
            'GRT-USD',  # The Graph
            'LRC-USD',  # Loopring
            'ZRX-USD',  # 0x
            'BAT-USD',  # Basic Attention Token
            'ENJ-USD',  # Enjin
            'MANA-USD', # Decentraland
            'SAND-USD'  # The Sandbox
        ]
    }
}

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