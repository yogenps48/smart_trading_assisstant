# examples/run_backtest_example.py
from src.data_fetcher import fetch_history_yfinance
from src.indicators import add_rsi
from src.strategy import generate_signals
from src.backtest import simple_backtest
import matplotlib.pyplot as plt

def main():
    ticker = "AAPL"   # example
    df = fetch_history_yfinance(ticker, period="2y", interval="1d")
    df = add_rsi(df, length=14)
    df = generate_signals(df, fast_sma=20, slow_sma=50, rsi_threshold=70)
    bt_df, summary = simple_backtest(df, entry_col='entry', exit_col='exit', price_col='Close', initial_capital=10000)
    print("Backtest summary:", summary)
    bt_df['equity'].plot(title=f"Equity Curve for {ticker}")
    plt.show()

if __name__ == "__main__":
    main()
