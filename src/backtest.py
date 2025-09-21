import pandas as pd
import numpy as np

def simple_backtest(df: pd.DataFrame, 
                    entry_col='entry',
                    exit_col='exit',
                    price_col='Close',
                    initial_capital=10000):
    """
    Backtest using normalized Alpaca schema (Date, Open, High, Low, Close, Volume).
    """
    df = df.copy().set_index("Date")
    cash = initial_capital
    position = 0
    equity_curve = []
    trades = []
    trade_pnls = []

    for i, row in df.iterrows():
        price = row[price_col]

        if row.get(entry_col) and position == 0:
            qty = cash // price
            if qty > 0:
                position = qty
                cash -= qty * price
                trades.append({"type": "BUY", "qty": qty, "price": price, "date": i})

        elif row.get(exit_col) and position > 0:
            sell_value = position * price
            cash += sell_value
            buy_price = trades[-1]["price"]
            pnl = (price - buy_price) * position
            trade_pnls.append(pnl)
            trades.append({"type": "SELL", "qty": position, "price": price, "date": i, "pnl": pnl})
            position = 0

        total_value = cash + position * price
        equity_curve.append(total_value)

    df["equity"] = equity_curve
    final_capital = equity_curve[-1] if equity_curve else initial_capital
    returns = pd.Series(df["equity"]).pct_change().dropna()

    # --- Performance Metrics ---
    total_return = (final_capital - initial_capital) / initial_capital * 100
    days = (df.index[-1] - df.index[0]).days if len(df) > 1 else 1
    cagr = (final_capital / initial_capital) ** (365.0 / days) - 1 if days > 0 else 0
    sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() != 0 else 0
    roll_max = df["equity"].cummax()
    drawdown = (df["equity"] - roll_max) / roll_max
    max_drawdown = drawdown.min()
    win_rate = (sum(1 for pnl in trade_pnls if pnl > 0) / len(trade_pnls) * 100) if trade_pnls else 0

    summary = {
        "initial_capital": initial_capital,
        "final_capital": final_capital,
        "total_return_pct": total_return,
        "CAGR": cagr,
        "Sharpe_Ratio": sharpe,
        "Max_Drawdown": max_drawdown,
        "Win_Rate": win_rate,
        "num_trades": len(trade_pnls),
        "trades": trades
    }
    return df, summary
