# src/data_fetcher.py
import yfinance as yf
import pandas as pd
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_DIR.mkdir(exist_ok=True)

def fetch_history_yfinance(ticker: str, period="1y", interval="1d", force_download=False) -> pd.DataFrame:
    """
    Returns DataFrame with columns: ['Open','High','Low','Close','Adj Close','Volume']
    Caches to data/<ticker>.csv
    """
    cache_file = CACHE_DIR / f"{ticker.replace(':','_')}_{period}_{interval}.csv"
    if cache_file.exists() and not force_download:
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
        return df

    tk = yf.Ticker(ticker)
    df = tk.history(period=period, interval=interval)
    df.to_csv(cache_file)
    return df
