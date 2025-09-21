from datetime import datetime
import pandas as pd
from src.broker_alpaca import AlpacaBroker
from src.utils import to_rfc3339

def fetch_history_alpaca(symbol: str, 
                         start: datetime, 
                         end: datetime, 
                         timeframe="1Day") -> pd.DataFrame:
    """
    Fetch historical OHLCV bars from Alpaca using IEX feed (free plan).
    """
    broker = AlpacaBroker()

    start_str = to_rfc3339(start)
    end_str = to_rfc3339(end)

    bars = broker.api.get_bars(
        symbol,
        timeframe,
        start=start_str,
        end=end_str,
        feed="iex"   # 👈 free plan requires IEX feed
    ).df

    # Reset index so timestamp is a column
    bars = bars.reset_index()

    # Rename to standard OHLCV
    bars = bars.rename(columns={
        "timestamp": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    })

    # Keep only what backtester needs
    return bars[["Date", "Open", "High", "Low", "Close", "Volume"]]
