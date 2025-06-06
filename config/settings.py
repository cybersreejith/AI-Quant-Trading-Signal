import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Log settings
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Trading settings
TRADING_PAIRS = ['BTC-USD', 'ETH-USD', 'BNB-USD']
START_DATE = '2023-01-01'
END_DATE = '2024-01-01'
INITIAL_CAPITAL = 100000
POSITION_SIZE = 0.1  # 10% of the trading capital
COMMISSION_RATE = 0.001  # 0.1% commission
SLIPPAGE = 0.001  # 0.1% slippage

# Strategy parameters
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9
ADX_THRESHOLD = 25
ATR_MULTIPLIER = 2

# Data configuration
DEFAULT_TIMEFRAME = '1d'
DEFAULT_START_DATE = '2020-01-01'
DEFAULT_END_DATE = None  # Use current date

# Backtest configuration
DEFAULT_INITIAL_CASH = 100000.0
DEFAULT_COMMISSION = 0.001  # 0.1%

# Popular asset list
POPULAR_ASSETS = {
    '1': {  # Global stocks
        'name': 'Global stocks',
        'assets': [
            'AAPL',  # Apple
            'MSFT',  # Microsoft
            'GOOGL', # Google
            'AMZN',  # Amazon
            'META',  # Meta
            'NVDA',  # NVIDIA
            'TSLA',  # Tesla
            'BABA',  # Alibaba
            'PDD',   # PDD
            'NIO',   # NIO
            'JPM',   # JPMorgan Chase
            'V',     # Visa
            'WMT',   # Walmart
            'MA',    # Mastercard
            'HD',    # Home Depot
            'BAC',   # Bank of America
            'XOM',   # ExxonMobil
            'PFE',   # Pfizer
            'AVGO',  # Broadcom
            'COST',  # Costco
            'TMO',   # Thermo Fisher Scientific
            'CSCO',  # Cisco
            'DHR',   # Danaher
            'ABBV',  # AbbVie
            'WFC',   # Wells Fargo
            'MRK',   # Merck
            'VZ',    # Verizon
            'NKE',   # Nike
            'CRM',   # Salesforce
            'NEE'    # NextEra Energy
        ]
    },
    '2': {  # ETF
        'name': 'ETF',
        'assets': [
            'SPY',   # S&P 500 ETF
            'QQQ',   # Nasdaq 100 ETF
            'DIA',   # Dow Jones ETF
            'IWM',   # Russell 2000 ETF
            'EFA',   # Developed Markets ETF
            'EEM',   # Emerging Markets ETF
            'GLD',   # Gold ETF
            'SLV',   # Silver ETF
            'TLT',   # 20-year Treasury ETF
            'VNQ',   # Real Estate ETF
            'XLK',   # Technology ETF
            'XLF',   # Financial ETF
            'XLE',   # Energy ETF
            'XLV',   # Healthcare ETF
            'XLI',   # Industrial ETF
            'XLP',   # Consumer Staples ETF
            'XLY',   # Consumer Discretionary ETF
            'XLB',   # Materials ETF
            'XLU',   # Utilities ETF
            'XBI',   # Biotechnology ETF
            'ARKK',  # ARK Innovation ETF
            'IEFA',  # Developed Markets ETF
            'IEMG',  # Emerging Markets ETF
            'AGG',   # US Aggregate Bond ETF
            'LQD',   # Investment-grade Corporate Bond ETF
            'HYG',   # High-yield Corporate Bond ETF
            'GDX',   # Gold Miners ETF
            'GDXJ',  # Small-cap Gold Miners ETF
            'USO',   # Crude Oil ETF
            'UNG',   # Natural Gas ETF
        ]
    },
    '3': {  # Forex
        'name': 'Forex',
        'assets': [
            'EURUSD=X',  # EUR/USD
            'GBPUSD=X',  # GBP/USD
            'USDJPY=X',  # USD/JPY
            'AUDUSD=X',  # AUD/USD
            'USDCAD=X',  # USD/CAD
            'NZDUSD=X',  # NZD/USD
            'USDCHF=X',  # USD/CHF
            'EURGBP=X',  # EUR/GBP
            'EURJPY=X',  # EUR/JPY
            'GBPJPY=X',  # GBP/JPY
            'EURCAD=X',  # EUR/CAD
            'AUDJPY=X',  # AUD/JPY
            'NZDJPY=X',  # NZD/JPY
            'GBPAUD=X',  # GBP/AUD
            'EURAUD=X',  # EUR/AUD
            'USDSGD=X',  # USD/SGD
            'USDHKD=X',  # USD/HKD
            'EURCHF=X',  # EUR/CHF
            'GBPCHF=X',  # GBP/CHF
            'AUDNZD=X',  # AUD/NZD
            'CADJPY=X',  # CAD/JPY
            'CHFJPY=X',  # CHF/JPY
            'EURCAD=X',  # EUR/CAD
            'GBPNZD=X',  # GBP/NZD
            'AUDCAD=X',  # AUD/CAD
            'NZDCHF=X',  # NZD/CHF
            'CADCHF=X',  # CAD/CHF
            'EURHKD=X',  # EUR/HKD
            'GBPHKD=X',  # GBP/HKD
            'AUDHKD=X'   # AUD/HKD
        ]
    },
    '4': {  # Cryptocurrency
        'name': 'Cryptocurrency',
        'assets': [
            'BTC-USD',  # BTC/USD
            'ETH-USD',  # ETH/USD
            'BNB-USD',  # BNB/USD
            'XRP-USD',  # XRP/USD
            'ADA-USD',  # ADA/USD
            'DOGE-USD', # DOGE/USD
            'DOT-USD',  # DOT/USD
            'SOL-USD',  # SOL/USD
            'AVAX-USD', # AVAX/USD
            'MATIC-USD',# MATIC/USD
            'LINK-USD', # LINK/USD
            'UNI-USD',  # UNI/USD
            'AAVE-USD', # AAVE/USD
            'COMP-USD', # COMP/USD
            'SUSHI-USD',# SUSHI/USD
            'YFI-USD',  # YFI/USD
            'SNX-USD',  # SNX/USD
            'MKR-USD',  # MKR/USD
            'CRV-USD',  # CRV/USD
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

# Strategy parameters
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