import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
import yfinance as yf


# ---------------------------
# Data Loader
# ---------------------------
def fetch_data(ticker, start, end):
    """Download historical data from Yahoo Finance"""
    return yf.download(ticker, start=start, end=end)


# ---------------------------
# Backtesting Engine
# ---------------------------
class TradingBacktester:
    def __init__(self, market_data, initial_cash=1_000_000, risk_fraction=0.02):
        self.data = market_data
        self.cash = initial_cash
        self.positions = {}
        self.trades = []
        self.risk_fraction = risk_fraction

    def simulate(self):
        """Run the backtest based on signals"""
        for date, row in self.data.iterrows():
            signal = row['signal']
            price = row['Close']

            if signal == 1:  # Buy
                available = self.cash
                qty = (available * self.risk_fraction) / price
                self._execute(row.name, qty, price)

            elif signal == -1:  # Sell
                qty = self.positions.get(self.data.name, 0)
                if qty > 0:
                    self._execute(row.name, -qty, price)

    def _execute(self, ticker, qty, price):
        """Execute trade and update portfolio"""
        self.cash -= qty * price
        self.positions[ticker] = self.positions.get(ticker, 0) + qty
        self.trades.append({'ticker': ticker, 'quantity': qty, 'price': price})

    def portfolio_value(self, price):
        """Calculate total portfolio value"""
        pos_value = sum(qty * price for _, qty in self.positions.items())
        return self.cash + pos_value

    def returns(self):
        """Calculate daily portfolio returns"""
        values = [self.portfolio_value(row['Close']) for _, row in self.data.iterrows()]
        return np.diff(values) / values[:-1]

    def performance_summary(self):
        """Compute PnL, Sharpe ratio, etc."""
        returns = self.returns()
        initial_val = self.portfolio_value(self.data.iloc[0]['Close'])
        final_val = self.portfolio_value(self.data.iloc[-1]['Close'])

        total_return = (final_val - initial_val) / initial_val
        annual_return = (1 + total_return) ** (252 / len(self.data)) - 1
        volatility = np.std(returns) * np.sqrt(252)
        sharpe = (annual_return - 0.02) / volatility if volatility > 0 else 0

        trade_prices = np.array([t['price'] for t in self.trades])
        trade_qty = np.array([t['quantity'] for t in self.trades])
        trade_returns = np.diff(trade_prices) / trade_prices[:-1] if len(trade_prices) > 1 else [0]
        trade_pnl = trade_returns * trade_qty[:-1] if len(trade_qty) > 1 else [0]

        pnl = np.sum(trade_pnl)
        avg_return = np.mean(trade_returns) if len(trade_returns) > 0 else 0
        win_rate = np.sum(trade_pnl > 0) / len(trade_pnl) if len(trade_pnl) > 0 else 0

        return {
            "Total Return": total_return,
            "Annualized Return": annual_return,
            "Volatility": volatility,
            "Sharpe Ratio": sharpe,
            "PnL": pnl,
            "Avg Trade Return": avg_return,
            "Win Rate": win_rate,
        }

    def plot(self):
        """Plot portfolio value with signals"""
        values = [self.portfolio_value(row['Close']) for _, row in self.data.iterrows()]
        dates = self.data.index
        signals = self.data['signal']

        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, label="Portfolio Value")
        plt.plot(dates, signals * max(values) * 0.05, 'r-', label="Signals")
        plt.title("Portfolio Value Over Time")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.show()


# ---------------------------
# Main Runner
# ---------------------------
def main():
    ticker = input("Enter ticker: ")
    start = input("Start Date (YYYY-MM-DD): ")
    end = input("End Date (YYYY-MM-DD): ")

    data = fetch_data(ticker, start, end)

    short_ma = ta.trend.sma_indicator(data['Close'], window=50)
    long_ma = ta.trend.sma_indicator(data['Close'], window=200)
    data['signal'] = np.where(short_ma > long_ma, 1, -1)
    data.name = ticker

    bt = TradingBacktester(data)
    bt.simulate()

    summary = bt.performance_summary()
    print("--- Performance Summary ---")
    for k, v in summary.items():
        if isinstance(v, float):
            print(f"{k}: {v:.2%}" if "Return" in k or "Win" in k else f"{k}: {v:.2f}")
        else:
            print(f"{k}: {v}")

    bt.plot()


if __name__ == "__main__":
    main()
