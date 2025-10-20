import pytest
from backtester.broker import Broker

def test_buy_and_sell_updates_cash_and_pos(broker):
    broker.market_order("BUY", 2, 10.0)
    assert (broker.position, broker.cash) == (2, 1000.0 - 20.0)
    broker.market_order("SELL", 1, 12.0)
    assert (broker.position, broker.cash) == (1, 1000.0 - 20.0 + 12.0)

def test_rejects_bad_orders(broker):
    with pytest.raises(ValueError):
        broker.market_order("BUY", 0, 10.0)
    with pytest.raises(ValueError):
        broker.market_order("HOLD", 1, 10.0)
    with pytest.raises(ValueError):
        broker.market_order("BUY", 1, -1.0)

def test_insufficient_cash_raises(broker):
    with pytest.raises(RuntimeError):
        broker.market_order("BUY", 1000, 10.0)

def test_insufficient_shares_raises(broker):
    with pytest.raises(RuntimeError):
        broker.market_order("SELL", 1, 10.0)
