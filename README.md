# AI量化交易信号系统

这是一个基于Python的量化交易信号系统，使用langchain框架构建。系统可以获取股票历史数据并计算各种技术指标。

## 功能特点

- 支持输入股票代码获取历史数据
- 使用yfinance API获取股票数据
- 计算多个技术指标（MACD、RSI、ATR等）
- 支持A股市场（沪深两市）

## 安装说明

1. 安装依赖包：
```bash
pip install -r requirements.txt
```

2. 安装TA-Lib（技术分析库）：
- Windows用户可以从[这里](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)下载对应的wheel文件
- Linux用户可以使用：`sudo apt-get install ta-lib`

## 使用方法

运行主程序：
```bash
python main.py
```

输入股票代码（例如：'AAPL'为苹果公司，'600519'为贵州茅台）即可获取相关技术指标数据。
