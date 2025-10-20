from dataclasses import dataclass

@dataclass
class Broker:
    cash: float = 1_000_000.0
    position: int = 0

    def _check_inputs(self, side: str, qty: int, price: float):
        if side not in {"BUY", "SELL"}:
            raise ValueError("side must be 'BUY' or 'SELL'")
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("qty must be positive int")
        if price <= 0:
            raise ValueError("price must be > 0")

    def market_order(self, side: str, qty: int, price: float):
        self._check_inputs(side, qty, price)
        cost = qty * float(price)
        if side == "BUY":
            if self.cash < cost:
                raise RuntimeError("insufficient cash")
            self.cash -= cost
            self.position += qty
        else:  # SELL
            if self.position < qty:
                raise RuntimeError("insufficient shares")
            self.cash += cost
            self.position -= qty
