import numpy as np
import pandas as pd
import pytest
from backtester.strategy import VolatilityBreakoutStrategy

def test_signals_length(strategy, prices):
    sig = strategy.signals(prices)
    assert len(sig) == len(prices)

def test_signals_types_and_values(strategy, prices):
    sig = strategy.signals(prices)
    assert set(sig.unique()).issubset({-1, 0, 1})
    assert sig.dtype == int

def test_empty_series_returns_empty():
    s = pd.Series(dtype=float)
    st = VolatilityBreakoutStrategy(window=5)
    sig = st.signals(s)
    assert sig.empty

def test_constant_prices_all_zero(constant_prices):
    st = VolatilityBreakoutStrategy(window=5)
    sig = st.signals(constant_prices)
    assert (sig == 0).all()

def test_window_validation():
    with pytest.raises(ValueError):
        VolatilityBreakoutStrategy(window=1)

def test_nan_head_handled(strategy, nan_head_prices):
    sig = strategy.signals(nan_head_prices)
    # after NaNs, we still get integer signals (possibly zeros)
    assert len(sig) == len(nan_head_prices)
    assert set(sig.unique()).issubset({-1, 0, 1})
