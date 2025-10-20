import numpy as np
import pandas as pd
import pytest
from backtester.strategy import VolatilityBreakoutStrategy
from backtester.broker import Broker

@pytest.fixture
def prices():
    # deterministic linear ramp (no randomness)
    return pd.Series(np.linspace(100, 120, 200))

@pytest.fixture
def short_prices():
    return pd.Series([100.0, 101.0, 102.0])

@pytest.fixture
def nan_head_prices():
    s = pd.Series([None, None, 100.0, 101.0, 100.5, 101.5])
    return s

@pytest.fixture
def constant_prices():
    return pd.Series([100.0]*50)

@pytest.fixture
def strategy():
    return VolatilityBreakoutStrategy(window=10)

@pytest.fixture
def broker():
    return Broker(cash=1_000.0)
