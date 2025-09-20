# src/broker_mock.py
"""
A simple in-memory broker simulator for paper trading.
"""
from dataclasses import dataclass

@dataclass
class Order:
    id: int
    symbol: str
    qty: int
    price: float
    side: str  # 'buy' or 'sell'
    status: str  # 'filled', 'open', etc.

class MockBroker:
    def __init__(self, cash=100000):
        self.cash = cash
        self.positions = {}  # symbol -> qty
        self.orders = []
        self._next_id = 1

    def place_order(self, symbol, qty, price, side):
        order = Order(self._next_id, symbol, qty, price, side, 'filled')
        self._next_id += 1
        self.orders.append(order)
        if side == 'buy':
            self.cash -= qty * price
            self.positions[symbol] = self.positions.get(symbol, 0) + qty
        else:
            self.cash += qty * price
            self.positions[symbol] = self.positions.get(symbol, 0) - qty
        return order

    def get_positions(self):
        return self.positions

    def get_cash(self):
        return self.cash
