from datetime import datetime, timezone
import plotly.graph_objects as go
import pandas as pd

def plot_trades(df: pd.DataFrame, trades: list, title="Price Chart with Trades"):
    """
    Creates an interactive candlestick chart with BUY/SELL markers.
    df: DataFrame with Date, Open, High, Low, Close
    trades: list of trade dicts with 'type', 'date', 'price'
    """
    fig = go.Figure(data=[go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price"
    )])

    # Add buy markers
    buys = [t for t in trades if t["type"] == "BUY"]
    if buys:
        fig.add_trace(go.Scatter(
            x=[t["date"] for t in buys],
            y=[t["price"] for t in buys],
            mode="markers",
            marker=dict(symbol="triangle-up", color="green", size=12),
            name="BUY"
        ))

    # Add sell markers
    sells = [t for t in trades if t["type"] == "SELL"]
    if sells:
        fig.add_trace(go.Scatter(
            x=[t["date"] for t in sells],
            y=[t["price"] for t in sells],
            mode="markers",
            marker=dict(symbol="triangle-down", color="red", size=12),
            name="SELL"
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        xaxis_rangeslider_visible=False
    )
    return fig

def to_rfc3339(dt: datetime) -> str:
    """
    Convert datetime to RFC3339 format with UTC offset.
    Example: 2025-09-20T15:30:00Z
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")
