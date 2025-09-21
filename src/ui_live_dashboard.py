import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import threading
import time

from src.broker_alpaca import AlpacaBroker
from src.paper_trading_engine import PaperTradingEngine
from src.strategy import generate_signals
from src.indicators import add_rsi

# Global engine reference
engine = None
engine_thread = None
engine_running = False

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "trades.csv"

# ----------------------
# Strategy Wrapper
# ----------------------
def strategy_wrapper(df, fast_sma=20, slow_sma=50, rsi_threshold=70):
    df = add_rsi(df, length=14)
    df = generate_signals(df, fast_sma=fast_sma, slow_sma=slow_sma, rsi_threshold=rsi_threshold)
    return df

# ----------------------
# Engine Controller
# ----------------------
def start_engine(symbol="AAPL", qty=1, poll_interval=60):
    global engine, engine_thread, engine_running
    if engine_running:
        return
    broker = AlpacaBroker()
    engine = PaperTradingEngine(broker, symbol, qty, poll_interval)
    engine_running = True

    def run_engine():
        engine.run(strategy_wrapper, strategy_kwargs={"fast_sma": 20, "slow_sma": 50, "rsi_threshold": 70})

    engine_thread = threading.Thread(target=run_engine, daemon=True)
    engine_thread.start()

def stop_engine():
    global engine_running
    engine_running = False
    # NOTE: Right now the engine loop runs forever. To stop gracefully, you’d add a `while self.running:` condition in PaperTradingEngine.

# ----------------------
# Streamlit UI
# ----------------------
st.set_page_config(page_title="Trading Assistant Dashboard", layout="wide")

st.title("📊 Smart Trading Assistant — Live Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
symbol = st.sidebar.text_input("Symbol", "AAPL")
qty = st.sidebar.number_input("Order Quantity", min_value=1, value=1)
interval = st.sidebar.number_input("Polling Interval (sec)", min_value=10, value=60)

if st.sidebar.button("▶️ Start Trading"):
    start_engine(symbol, qty, interval)
    st.sidebar.success("Trading engine started")

if st.sidebar.button("⏹ Stop Trading"):
    if engine:
        engine.stop()  # 👈 call stop method
        st.sidebar.success("Trading engine stopped gracefully")
    else:
        st.sidebar.warning("No engine running")


# Account Info
st.header("📈 Account Info")
broker = AlpacaBroker()
account = broker.get_account()
st.write(account)

# Open Positions
st.header("📌 Open Positions")
positions = broker.get_positions()
if positions:
    st.dataframe(pd.DataFrame(positions))
else:
    st.info("No open positions")

# Trade History
st.header("📑 Trade History")
if LOG_FILE.exists():
    trades_df = pd.read_csv(LOG_FILE)
    st.dataframe(trades_df.tail(20))  # show last 20 trades

    # Plot equity curve (cumulative PnL)
    if "pnl" in trades_df.columns:
        trades_df["cumulative_pnl"] = trades_df["pnl"].cumsum()
        st.line_chart(trades_df[["cumulative_pnl"]])
else:
    st.info("No trades logged yet")

# Auto refresh every 30s
st.experimental_set_query_params(refresh=str(time.time()))
