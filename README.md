# AI Quantitative trading signal system

This is a Python-based quantitative trading signal system built using the langchain framework. The system can obtain stock historical data and calculate various technical indicators

## Features

- Support inputting stock codes to obtain historical data
- Get stock data using yfinance API
- Calculate multiple technical indicators (MACD, RSI, ATR, etc.)
- Support A-share market (Shanghai and Shenzhen)

## Installation Instructions

1. Install dependency packages:
```bash
pip install -r requirements.txt
```

2. Install TA-Lib (Technical Analysis Library):
- Windows users can download the corresponding wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)
- Linux users can use：`sudo apt-get install ta-lib`

## How to use

Run the main program:
```bash
python main.py
```

Enter the stock code (for example: 'AAPL' for Apple, '600519' for Kweichow Moutai) to obtain relevant technical indicator data.
