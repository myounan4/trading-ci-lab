from dataclasses import dataclass

@dataclass
class Broker:
    def __init__(self, cash: float = 1_000_000):
        self.cash = cash
        self.position = 0

    def _check(self, side, qty, price):
        if side not in {"BUY", "SELL"}:
            raise ValueError("invalid side")
        if qty <= 0 or price <= 0:
            raise ValueError("qty and price must be positive")

    def market_order(self, side, qty, price):
        self._check(side, qty, price)
        cost = qty * price
        if side == "BUY":
            if self.cash < cost:
                raise RuntimeError("insufficient cash")
            self.cash -= cost
            self.position += qty
        else:
            if self.position < qty:
                raise RuntimeError("insufficient shares")
            self.cash += cost
            self.position -= qty
