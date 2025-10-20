import numpy as np
import pandas as pd

class VolatilityBreakoutStrategy:
    """Signal is +1 when today's return > rolling std (window),
    -1 when today's return < -rolling std, else 0.

    Signals are aligned to the price index (same length). The first (window) values
    may be 0 due to insufficient lookback.
    """
    def __init__(self, window: int = 20, min_periods: int | None = None):
        if window <= 1:
            raise ValueError("window must be > 1")
        self.window = int(window)
        self.min_periods = int(min_periods) if min_periods is not None else window

    def signals(self, prices: pd.Series) -> pd.Series:
        if not isinstance(prices, pd.Series):
            raise TypeError("prices must be a pandas Series")
        if prices.empty:
            return pd.Series(dtype=float)

        # Work on a copy to avoid mutating caller
        p = pd.Series(prices.astype(float).values, index=prices.index)
        rets = p.pct_change()
        vol = rets.rolling(self.window, min_periods=self.min_periods).std()

        sig = pd.Series(0, index=p.index, dtype=int)

        cond_buy = rets > vol
        cond_sell = rets < -vol

        sig[cond_buy.fillna(False)] = 1
        sig[cond_sell.fillna(False)] = -1
        sig = sig.fillna(0).astype(int)
        return sig
