import pytest
from unittest.mock import MagicMock
from backtester.engine import Backtester

def test_engine_uses_tminus1_signal(prices, broker):
    # Force exactly one buy at t=10 by controlling signals (signal at index 9 -> buy at 10)
    fake_strategy = MagicMock()
    sig = prices.copy()*0  # correct length
    sig.iloc[:] = 0
    sig.iloc[9] = 1
    fake_strategy.signals.return_value = sig.astype(int)
    bt = Backtester(fake_strategy, broker, share_qty=1)
    eq = bt.run(prices)
    assert broker.position == 1
    assert broker.cash == 1000.0 - float(prices.iloc[10])
    assert isinstance(eq, float)

def test_engine_final_equity_matches_cash_plus_pos(prices, broker):
    # Strategy: buy every other day (after warmup) using t-1 signal
    fake_strategy = MagicMock()
    import pandas as pd
    s = pd.Series([0]*len(prices))
    s.iloc[1::2] = 1
    fake_strategy.signals.return_value = s.astype(int)
    bt = Backtester(fake_strategy, broker, share_qty=1)
    eq = bt.run(prices)
    # Manual recompute
    pos = broker.position
    cash = broker.cash
    expected = cash + pos * float(prices.iloc[-1])
    assert pytest.approx(eq) == expected

def test_engine_rejects_length_mismatch(prices, broker):
    fake_strategy = MagicMock()
    fake_strategy.signals.return_value = prices.iloc[:-1]*0  # shorter by 1
    bt = Backtester(fake_strategy, broker)
    with pytest.raises(ValueError):
        bt.run(prices)

def test_engine_raises_on_empty(broker):
    import pandas as pd
    bt = Backtester(MagicMock(), broker)
    with pytest.raises(ValueError):
        bt.run(pd.Series(dtype=float))

def test_mocked_broker_failure_propagates(prices, broker):
    fake_strategy = MagicMock()
    fake_strategy.signals.return_value = (prices*0).astype(int).where(~(prices.index==0), other=1)
    # monkeypatch broker to raise on first order
    class BadBroker:
        def __init__(self): pass
        def market_order(self, side, qty, price):
            raise RuntimeError("downstream failure")
        cash = 1000.0
        position = 0
    bt = Backtester(fake_strategy, BadBroker(), share_qty=1)
    with pytest.raises(RuntimeError):
        bt.run(prices)
