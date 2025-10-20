import numpy as np
import pandas as pd
from typing import Optional

class PriceLoader:
    """Return a pandas Series of daily close prices for a symbol.
    In this assignment, we avoid I/O and allow synthetic data generation.
    """
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)

    def synthetic_walk(self, n: int = 200, start: float = 100.0, vol: float = 0.01) -> pd.Series:
        """Deterministic-ish geometric random walk using a fixed RNG.
        Returns prices indexed 0..n-1.
        """
        rets = self.rng.normal(0.0, vol, size=n)
        prices = start * np.exp(np.cumsum(rets))
        return pd.Series(prices)
