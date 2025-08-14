from src.backtest import generate_synth, strategy, pnl

def test_shapes():
    df = generate_synth(1000, seed=1)
    pos = strategy(df)
    p = pnl(df, pos.values)
    assert len(p) == len(df)
