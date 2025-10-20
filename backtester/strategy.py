import numpy as np
import pandas as pd

class VolatilityBreakoutStrategy:
    def __init__(self, window: int = 20):
        if window <= 1:
            raise ValueError("window must be > 1")
        self.window = window

    def signals(self, prices: pd.Series) -> pd.Series:
        if prices.empty:
            return pd.Series(dtype=int)
        rets = prices.pct_change()
        vol = rets.rolling(self.window).std()
        sig = pd.Series(0, index=prices.index, dtype=int)
        sig[rets > vol] = 1
        sig[rets < -vol] = -1
        return sig.fillna(0).astype(int)
