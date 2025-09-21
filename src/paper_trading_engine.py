import time
import logging
from datetime import datetime, timedelta
from src.broker_alpaca import AlpacaBroker
from src.trade_logger import TradeLogger
from src.utils import to_rfc3339

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class PaperTradingEngine:
    def __init__(self, broker: AlpacaBroker, symbol: str, qty: int = 1, poll_interval: int = 60):
        self.broker = broker
        self.symbol = symbol
        self.qty = qty
        self.poll_interval = poll_interval
        self.in_position = False
        self.last_buy_price = None
        self.logger = TradeLogger()

    def fetch_data(self, lookback_days=90, timeframe="1Day"):
        end = datetime.now()
        start = end - timedelta(days=lookback_days)

        start_str = to_rfc3339(start)
        end_str = to_rfc3339(end)

        bars = self.broker.api.get_bars(
            self.symbol,
            timeframe,
            start=start_str,
            end=end_str,
            feed="iex"
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

    def run(self, strategy_fn, strategy_kwargs=None):
        logging.info("Starting generic paper trading engine...")
        strategy_kwargs = strategy_kwargs or {}

        while True:
            try:
                df = self.fetch_data()
                df = strategy_fn(df, **strategy_kwargs)
                latest = df.iloc[-1]

                if latest.get("entry", False) and not self.in_position:
                    price = latest["close"]
                    logging.info(f"BUY {self.qty} {self.symbol} @ {price}")
                    order = self.broker.place_order(self.symbol, self.qty, side="buy")
                    logging.info(f"Order response: {order}")
                    self.in_position = True
                    self.last_buy_price = price
                    self.logger.log_trade(self.symbol, "BUY", self.qty, price, order["id"])

                elif latest.get("exit", False) and self.in_position:
                    price = latest["close"]
                    logging.info(f"SELL {self.qty} {self.symbol} @ {price}")
                    order = self.broker.place_order(self.symbol, self.qty, side="sell")
                    logging.info(f"Order response: {order}")
                    self.in_position = False

                    # PnL calculation
                    pnl = (price - self.last_buy_price) * self.qty if self.last_buy_price else None
                    self.logger.log_trade(self.symbol, "SELL", self.qty, price, order["id"], pnl=pnl)
                    self.last_buy_price = None

            except Exception as e:
                logging.error(f"Error in trading loop: {e}")

            time.sleep(self.poll_interval)
