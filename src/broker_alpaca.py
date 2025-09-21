from alpaca_trade_api.rest import REST, TimeFrame
from src import config

class AlpacaBroker:
    def __init__(self):
        self.api = REST(
            key_id=config.ALPACA_API_KEY_ID,
            secret_key=config.ALPACA_API_SECRET_KEY,
            base_url=config.ALPACA_BASE_URL
        )

    def get_account(self):
        """Return account info (cash, portfolio value, etc.)"""
        return self.api.get_account()._raw

    def get_latest_price(self, symbol: str):
        """Fetch latest trade price for a symbol"""
        barset = self.api.get_latest_trade(symbol,feed="iex")
        return barset.price

    def place_order(self, symbol: str, qty: int, side="buy", order_type="market", time_in_force="gtc"):
        """Place a simple order"""
        order = self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )
        return order._raw

    def get_positions(self):
        """Get all open positions"""
        return [pos._raw for pos in self.api.list_positions()]

    def close_position(self, symbol: str):
        """Close an open position"""
        return self.api.close_position(symbol)._raw
