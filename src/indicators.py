# src/indicators.py
import pandas as pd
import pandas_ta as ta

def add_sma(df: pd.DataFrame, window: int, column='Close', name=None):
    name = name or f"SMA_{window}"
    df[name] = df[column].rolling(window).mean()
    return df

def add_rsi(df: pd.DataFrame, length: int = 14, column='Close', name='RSI'):
    df[name] = ta.rsi(df[column], length=length)
    return df

def add_macd(df: pd.DataFrame, column='Close'):
    macd = ta.macd(df[column])
    # returns macd columns like 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9'
    df = pd.concat([df, macd], axis=1)
    return df
