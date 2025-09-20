# src/backtest.py
import pandas as pd
import numpy as np

def simple_backtest(df: pd.DataFrame, 
                    entry_col='entry',
                    exit_col='exit',
                    price_col='Close',
                    initial_capital=10000,
                    risk_per_trade=0.01,
                    fixed_size=None):
    """
    Very simple backtest: each entry opens a position at next day's open (or close), 
    exit closes at next day's open. Position sizing uses risk_per_trade on stop-loss if given.
    Returns result DataFrame and summary statistics.
    """
    df = df.copy().reset_index()
    cash = initial_capital
    position = 0
    pos_price = 0
    equity_curve = []
    trades = []

    for i, row in df.iterrows():
        price = row[price_col]
        if row.get(entry_col):
            # buy full position or fixed size
            if fixed_size:
                qty = fixed_size
            else:
                qty = cash // price  # integer shares
            if qty > 0:
                position += qty
                pos_price = price
                cost = qty * price
                cash -= cost
                trades.append({'type': 'buy', 'qty': qty, 'price': price, 'index': i})
        if row.get(exit_col) and position > 0:
            # sell all
            proceeds = position * price
            cash += proceeds
            trades.append({'type': 'sell', 'qty': position, 'price': price, 'index': i})
            position = 0
            pos_price = 0
        total_value = cash + position * price
        equity_curve.append(total_value)

    df['equity'] = equity_curve
    summary = {
        'initial_capital': initial_capital,
        'final_capital': equity_curve[-1] if len(equity_curve) else initial_capital,
        'returns_pct': (equity_curve[-1] - initial_capital) / initial_capital * 100 if len(equity_curve) else 0,
        'trades': trades
    }
    return df.set_index('Date'), summary
