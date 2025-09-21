import pandas as pd

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

    for i, row in df.iterrows():
        price = row[price_col]

        if row.get(entry_col) and position == 0:
            qty = cash // price
            if qty > 0:
                position = qty
                cash -= qty * price
                trades.append({"type": "BUY", "qty": qty, "price": price, "date": i})

        elif row.get(exit_col) and position > 0:
            cash += position * price
            trades.append({"type": "SELL", "qty": position, "price": price, "date": i})
            position = 0

        total_value = cash + position * price
        equity_curve.append(total_value)

    df["equity"] = equity_curve
    summary = {
        "initial_capital": initial_capital,
        "final_capital": equity_curve[-1] if equity_curve else initial_capital,
        "returns_pct": ((equity_curve[-1] - initial_capital) / initial_capital * 100) if equity_curve else 0,
        "trades": trades
    }
    return df, summary
