from __future__ import annotations
import pandas as pd
from dataclasses import dataclass

@dataclass
class Backtester:
    strategy: any
    broker: any
    share_qty: int = 1  # trade one share per signal event

    def run(self, prices: pd.Series) -> float:
        if not isinstance(prices, pd.Series):
            raise TypeError("prices must be a pandas Series")
        if prices.empty:
            raise ValueError("prices cannot be empty")

        prices = prices.astype(float)
        sig = self.strategy.signals(prices)

        if len(sig) != len(prices):
            raise ValueError("strategy.signals must match price length")

        # Execute at close(t) using signal from t-1
        prev_sig = sig.shift(1).fillna(0).astype(int)

        for t in range(1, len(prices)):
            s = prev_sig.iloc[t]
            px = float(prices.iloc[t])
            if s > 0:
                self.broker.market_order("BUY", self.share_qty, px)
            elif s < 0:
                self.broker.market_order("SELL", self.share_qty, px)

        final_equity = float(self.broker.cash + self.broker.position * float(prices.iloc[-1]))
        return final_equity
