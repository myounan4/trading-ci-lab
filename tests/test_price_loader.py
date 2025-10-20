import pandas as pd
from backtester.price_loader import PriceLoader

def test_synthetic_walk_deterministic_length():
    pl = PriceLoader(seed=123)
    s = pl.synthetic_walk(n=50, start=100.0, vol=0.01)
    assert isinstance(s, pd.Series)
    assert len(s) == 50
    assert (s > 0).all()
