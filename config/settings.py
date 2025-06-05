import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API密钥
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

INDICATOR_META = {
    # === Trend class =========================================================
    "SMA": {
        "desc": "Simple Moving Average",
        "fields": ["SMA"],                                # Example of generating column names: SMA_50
        "param_space": {"period": [10, 20, 50, 100, 200]},
        "rule_templates": [
            "close > SMA",                               # Bullish
            "close < SMA"                                # Bearish
        ]
    },
    "EMA": {
        "desc": "Exponential Moving Average, more sensitive to new prices",
        "fields": ["EMA"],
        "param_space": {"period": [5, 10, 21, 55, 89]},
        "rule_templates": [
            "EMA > SMA",                                 # Trend confirmation
            "EMA_crosses_above_SMA"                      # Golden cross
        ]
    },
    "MACD": {
        "desc": "The difference between the fast and slow EMA, to judge the bullish and bearish momentum",
        "fields": ["MACD", "MACD_SIGNAL", "MACD_HIST"],
        "param_space": {
            "fast":   [8, 12, 20],
            "slow":   [18, 26, 40],
            "signal": [6, 9, 12]
        },
        "rule_templates": [
            "MACD > MACD_SIGNAL",                        # Golden cross
            "MACD_crosses_below_MACD_SIGNAL"             # Dead cross
        ]
    },
    "ADX": {
        "desc": "Trend strength (0–100), >25 is considered a strong trend",
        "fields": ["ADX"],
        "param_space": {"period": [14, 20, 28]},
        "rule_templates": [
            "ADX > {adx_th}",                            # Trend filtering
            "ADX < {adx_th}"                             # Trend weakening
        ]
    },

    # === Oscillation / Reversal class ================================================
    "RSI": {
        "desc": "Relative Strength Index, <30 is oversold, >70 is overbought",
        "fields": ["RSI"],
        "param_space": {
            "period":  [7, 14],
            "th_low":  [25, 30, 40],
            "th_high": [60, 70, 80]
        },
        "rule_templates": [
            "RSI < {th_low}",                            # Buy at low
            "RSI > {th_high}"                            # Sell at high
        ]
    },
    "STOCH": {
        "desc": "Stochastic indicator (KD), to judge the oversold and overbought points",
        "fields": ["STOCH_K", "STOCH_D"],
        "param_space": {"k_period":[9,14], "d_period":[3]},
        "rule_templates": [
            "STOCH_K_crosses_above_STOCH_D",             # Bullish
            "STOCH_K_crosses_below_STOCH_D"              # Bearish
        ]
    },

    # === Statistical volatility / Channel class ============================================
    "ATR": {
        "desc": "Average True Range, used for stop loss or volatility filtering",
        "fields": ["ATR"],
        "param_space": {"period":[7,14,20]},
        "rule_templates": []
    },
    "BBANDS": {
        "desc": "Bollinger Bands, ±k·σ channel",
        "fields": ["BB_UPPER", "BB_MIDDLE", "BB_LOWER"],
        "param_space": {"period":[20], "stdev":[2, 2.5]},
        "rule_templates": [
            "close > BB_UPPER",                          # Breakout
            "close < BB_LOWER"
        ]
    },
    "DONCHIAN": {
        "desc": "Donchian Channel, high and low breakout",
        "fields": ["DONCHIAN_HIGH", "DONCHIAN_LOW"],
        "param_space": {"period":[20,55]},
        "rule_templates": [
            "close > DONCHIAN_HIGH",                     # Bullish breakout
            "close < DONCHIAN_LOW"                       # Bearish breakout
        ]
    },

    # === Momentum / Rate of change ===============================================
    "ROC": {
        "desc": "Rate of Change, momentum percentage",
        "fields": ["ROC"],
        "param_space": {"period":[10,20]},
        "rule_templates": [
            "ROC > {pos_th}",                            # Momentum up
            "ROC < -{neg_th}"
        ]
    },

    # === Volume / Market depth ===========================================
    "OBV": {
        "desc": "On Balance Volume, cumulative volume momentum",
        "fields": ["OBV"],
        "param_space": {},
        "rule_templates": [
            "OBV_rising_for_3_bars"                      # OBV 3 consecutive rises
        ]
    }
}

# Strategy configuration schema definition
STRAT_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["name", "indicators", "params", "rule"],
        "properties": {
            "name": {"type": "string"},
            "indicators": {"type": "array", "items": {"type": "string"}},
            "params": {"type": "object"},
            "rule": {"type": "string"}
        }
    }
}