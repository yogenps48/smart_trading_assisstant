import csv
from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

class TradeLogger:
    def __init__(self, filename="trades.csv"):
        self.filepath = LOG_DIR / filename
        # If file doesn’t exist, create with header
        if not self.filepath.exists():
            with open(self.filepath, mode="w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "timestamp", "symbol", "side", "qty", "price", "order_id", "pnl"
                ])
                writer.writeheader()

    def log_trade(self, symbol, side, qty, price, order_id, pnl=None):
        with open(self.filepath, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "timestamp", "symbol", "side", "qty", "price", "order_id", "pnl"
            ])
            writer.writerow({
                "timestamp": datetime.now().isoformat(),
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "price": price,
                "order_id": order_id,
                "pnl": pnl if pnl is not None else ""
            })
