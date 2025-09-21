from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from src.data_fetcher_alpaca import fetch_history_alpaca
from src.indicators import add_rsi
from src.strategy import generate_signals
from src.backtest import simple_backtest

def main():
    symbol = "AAPL"
    end = datetime.now()
    start = end - timedelta(days=365 * 2)

    print(f"Fetching Alpaca historical data for {symbol}...")
    df = fetch_history_alpaca(symbol, start=start, end=end, timeframe="1Day")

    df = add_rsi(df, length=14)
    df = generate_signals(df, fast_sma=20, slow_sma=50, rsi_threshold=70)

    bt_df, summary = simple_backtest(df, entry_col="entry", exit_col="exit", price_col="Close", initial_capital=10000)

    print("Backtest summary:", summary)
    bt_df["equity"].plot(title=f"Equity Curve (Alpaca Data) — {symbol}")
    plt.show()

if __name__ == "__main__":
    main()
