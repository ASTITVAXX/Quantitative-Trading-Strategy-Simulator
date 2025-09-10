# Trading Strategy Backtesting Framework

A Python-based framework for simulating and evaluating trading strategies using historical market data.  
This tool enables users to fetch data, apply trading logic, execute trades, and assess performance metrics such as returns and win rates.  

It’s designed as a flexible foundation for experimenting with different strategies and analyzing their outcomes.

---

## Features

- **Historical Data Retrieval**: Uses `yfinance` to download stock data for any ticker and time period.  
- **Core Backtesting Engine**: Handles portfolio management, trade execution, and performance tracking.  
- **Customizable Strategies**: Easily implement your own trading logic (example: Moving Average Crossover).  
- **Performance Metrics**: Calculates total return, number of trades, and win rate for evaluation.  
- **Visualization**: Plots price data with buy/sell signals for better strategy insight.  

---

## Example Strategy

The included demo uses a **Simple Moving Average (SMA) Crossover**:  
- **Buy** when the short SMA crosses above the long SMA.  
- **Sell** when the short SMA crosses below the long SMA.  

---

## Usage

1. Install required libraries:
   ```bash
   pip install yfinance matplotlib pandas

└── output.png # Example visualization (sample chart)

