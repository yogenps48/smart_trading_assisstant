import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import threading
from pathlib import Path

from src.broker_alpaca import AlpacaBroker
from src.paper_trading_engine import PaperTradingEngine
from src.data_fetcher_alpaca import fetch_history_alpaca
from src.backtest import simple_backtest
from src.indicators import add_rsi
from src.strategy import generate_signals

# Global engine/thread references
engine = None
engine_thread = None

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "trades.csv"

# ------------------------
# Strategy Wrapper
# ------------------------
def strategy_wrapper(df, fast_sma=20, slow_sma=50, rsi_threshold=70):
    df = add_rsi(df, length=14)
    df = generate_signals(df, fast_sma=fast_sma, slow_sma=slow_sma, rsi_threshold=rsi_threshold)
    return df

# ------------------------
# Engine Controls
# ------------------------
def start_engine(symbol, qty, interval, fast_sma, slow_sma, rsi_threshold, timeframe):
    global engine, engine_thread
    broker = AlpacaBroker()
    engine = PaperTradingEngine(broker, symbol, qty,
                                poll_interval=interval,
                                timeframe=timeframe)  # 👈 pass timeframe

    def run_engine():
        engine.run(strategy_wrapper, strategy_kwargs={
            "fast_sma": fast_sma,
            "slow_sma": slow_sma,
            "rsi_threshold": rsi_threshold
        })

    engine_thread = threading.Thread(target=run_engine, daemon=True)
    engine_thread.start()


def stop_engine():
    global engine
    if engine:
        engine.stop()

# ------------------------
# Streamlit UI Layout
# ------------------------
st.set_page_config(page_title="Trading Assistant", layout="wide")
st.title("💹 Smart Trading Assistant")

tabs = st.tabs(["📊 Dashboard", "📈 Backtesting", "🛠 Trade Execution"])

# ------------------------
# Tab 1: Dashboard
# ------------------------
with tabs[0]:
    st.header("📊 Portfolio Dashboard")
    broker = AlpacaBroker()
    account = broker.get_account()
    st.metric("Portfolio Value", f"${account['portfolio_value']}", f"{float(account['equity']) - float(account['cash']):.2f} change")
    st.write(account)

    st.subheader("Open Positions")
    positions = broker.get_positions()
    if positions:
        st.dataframe(pd.DataFrame(positions))
    else:
        st.info("No open positions")

    st.subheader("Trade History")
    if LOG_FILE.exists():
        trades_df = pd.read_csv(LOG_FILE)
        st.dataframe(trades_df.tail(20))
        if "pnl" in trades_df.columns:
            trades_df["cumulative_pnl"] = trades_df["pnl"].cumsum()
            st.line_chart(trades_df[["cumulative_pnl"]])
    else:
        st.info("No trades logged yet")

# ------------------------
# Tab 2: Backtesting
# ------------------------
with tabs[1]:
    st.header("📈 Backtesting")

    # Inputs in 3 columns
    col1, col2, col3 = st.columns(3)
    with col1:
        symbol = st.text_input("Symbol", "AAPL", key="bt_symbol")
        fast_sma = st.number_input("Fast SMA Window", min_value=5, value=20, key="bt_fast_sma")
    with col2:
        timeframe = st.selectbox("Timeframe", ["1Day", "1Hour", "15Min"], index=0, key="bt_timeframe")
        slow_sma = st.number_input("Slow SMA Window", min_value=10, value=50, key="bt_slow_sma")
    with col3:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365), key="bt_start_date")
        end_date = st.date_input("End Date", datetime.now(), key="bt_end_date")
        rsi_threshold = st.number_input("RSI Threshold", min_value=30, max_value=90, value=70, key="bt_rsi")

    # Run Backtest Button
    if st.button("Run Backtest", key="bt_run"):
        df = fetch_history_alpaca(
            symbol,
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.min.time()),
            timeframe=timeframe
        )
        df = add_rsi(df, length=14)
        df = generate_signals(df, fast_sma=fast_sma, slow_sma=slow_sma, rsi_threshold=rsi_threshold)

        bt_df, summary = simple_backtest(
            df, entry_col="entry", exit_col="exit", price_col="Close", initial_capital=10000
        )

        # Show Metrics
        st.subheader("Summary Metrics")
        metrics = {
            "Initial Capital": f"${summary['initial_capital']}",
            "Final Capital": f"${summary['final_capital']:.2f}",
            "Total Return %": f"{summary['total_return_pct']:.2f}%",
            "CAGR": f"{summary['CAGR']*100:.2f}%",
            "Sharpe Ratio": f"{summary['Sharpe_Ratio']:.2f}",
            "Max Drawdown": f"{summary['Max_Drawdown']*100:.2f}%",
            "Win Rate": f"{summary['Win_Rate']:.2f}%",
            "Trades Taken": summary['num_trades']
        }
        st.table(pd.DataFrame(metrics.items(), columns=["Metric", "Value"]))

        # Chart
        st.subheader("Performance Chart")
        st.line_chart(bt_df[["equity"]])

        # Trade List
        st.subheader("Trade List")
        trades = summary.get("trades", [])
        if trades:
            trades_df = pd.DataFrame(trades)
            trades_df["date"] = pd.to_datetime(trades_df["date"]).dt.strftime("%Y-%m-%d")
            st.dataframe(trades_df)
        else:
            st.info("No trades executed in this backtest.")



# ------------------------
# Tab 3: Trade Execution
# ------------------------
with tabs[2]:
    st.header("🛠 Trade Execution Window")

    # Inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        symbol = st.text_input("Live Trading Symbol", "AAPL", key="exec_symbol")
    with col2:
        qty = st.number_input("Quantity", min_value=1, value=1, key="exec_qty")
    with col3:
        interval = st.number_input("Polling Interval (sec)", min_value=10, value=60, key="exec_interval")

    col4, col5, col6 = st.columns(3)
    with col4:
        fast_sma = st.number_input("Fast SMA Window", min_value=5, value=20, key="exec_fast_sma")
    with col5:
        slow_sma = st.number_input("Slow SMA Window", min_value=10, value=50, key="exec_slow_sma")
    with col6:
        rsi_threshold = st.number_input("RSI Threshold", min_value=30, max_value=90, value=70, key="exec_rsi")

    timeframe = st.selectbox("Timeframe", ["1Day", "1Hour", "15Min"], index=0, key="exec_timeframe")

    # Start/Stop Trading
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Trading", key="exec_start"):
            start_engine(symbol, qty, interval, fast_sma, slow_sma, rsi_threshold, timeframe)
            st.success("Trading engine started")
    with col2:
        if st.button("⏹ Stop Trading", key="exec_stop"):
            stop_engine()
            st.warning("Trading engine stopped")


    # Open Positions
    st.subheader("Open Positions")
    positions = broker.get_positions()
    if positions:
        st.dataframe(pd.DataFrame(positions))
    else:
        st.info("No open positions")

    # Trade History
    st.subheader("Trade History")
    if LOG_FILE.exists():
        trades_df = pd.read_csv(LOG_FILE)
        st.dataframe(trades_df.tail(20))
