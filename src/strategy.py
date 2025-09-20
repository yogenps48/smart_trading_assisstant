# src/strategy.py
import pandas as pd
from typing import Tuple

def generate_signals(df: pd.DataFrame,
                     fast_sma=10, slow_sma=50, rsi_threshold=60) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna()
    df['SMA_fast'] = df['Close'].rolling(fast_sma).mean()
    df['SMA_slow'] = df['Close'].rolling(slow_sma).mean()
    # signal: 1 = long, 0 = flat
    df['signal'] = 0
    df.loc[(df['SMA_fast'] > df['SMA_slow']) & (df.get('RSI', 100) < rsi_threshold), 'signal'] = 1
    # generate entry/exit
    df['signal_shift'] = df['signal'].shift(1).fillna(0)
    df['entry'] = (df['signal'] == 1) & (df['signal_shift'] == 0)
    df['exit'] = (df['signal'] == 0) & (df['signal_shift'] == 1)
    return df
