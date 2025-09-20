# src/ui_streamlit.py
import streamlit as st
from src.data_fetcher import fetch_history_yfinance
from src.indicators import add_rsi
from src.strategy import generate_signals
from src.backtest import simple_backtest
import matplotlib.pyplot as plt

st.title("Smart Trading Assistant — Demo")

ticker = st.text_input("Ticker", value="AAPL")
period = st.selectbox("Period", ["6mo","1y","2y","5y"], index=1)
if st.button("Run backtest"):
    df = fetch_history_yfinance(ticker, period=period)
    df = add_rsi(df)
    df = generate_signals(df)
    bt_df, summary = simple_backtest(df)
    st.write(summary)
    st.line_chart(bt_df['equity'])
