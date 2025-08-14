from intraday_micro_backtest.backtest import generate_synth, strategy, pnl
import numpy as np

def test_shapes():
    df = generate_synth(1000, seed=1)
    pos = strategy(df)
    p = pnl(df, pos.values)
    assert len(p) == len(df)

def test_costs_reduce_pnl():
    df = generate_synth(5000, seed=1)
    pos = strategy(df)
    p0 = pnl(df, pos.values, fee_bps=0, slip_bps=0).sum()
    p1 = pnl(df, pos.values, fee_bps=10, slip_bps=10).sum()
    assert p1 <= p0

def test_no_lookahead():
    df = generate_synth(1000, seed=2)
    pos = strategy(df)
    # position at t must not depend on return at t+1 (loose sanity bound)
    r_next = df["mid"].pct_change().shift(-1).fillna(0.0)
    corr = np.corrcoef(pos.values[:-1], r_next.values[:-1])[0, 1]
    assert abs(corr) < 0.2
