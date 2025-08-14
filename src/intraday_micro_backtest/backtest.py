from time import perf_counter

import numpy as np
import pandas as pd


def generate_synth(n=20000, seed=0):
    rng = np.random.default_rng(seed)
    # simple random walk mid price
    steps = rng.normal(0, 0.02, size=n).cumsum()
    return pd.DataFrame({"mid": 100 + steps})


def strategy(df, window=20, entry_z=1.0, exit_z=0.2):
    r = df["mid"].pct_change().fillna(0.0)
    mu = r.rolling(window).mean()
    sd = r.rolling(window).std().replace(0, np.nan)
    z = (r - mu) / sd
    pos = np.where(z < -entry_z, 1, np.where(z > entry_z, -1, np.nan))
    # hold until exit
    pos = pd.Series(pos).ffill().fillna(0.0).values
    pos[(np.abs(z) < exit_z)] = 0.0
    return pd.Series(pos, index=df.index, name="pos")


def pnl(df, pos, fee_bps=1, slip_bps=2):
    r = df["mid"].pct_change().fillna(0.0).values
    gross = pos[:-1] * r[1:]
    costs = (np.abs(np.diff(pos)) > 0).astype(float) * (fee_bps + slip_bps) / 1e4
    net = gross - costs
    return pd.Series(np.r_[0.0, net], index=df.index, name="pnl")


def main():
    df = generate_synth()
    t0 = perf_counter()
    pos = strategy(df)
    p = pnl(df, pos.values)
    dt = perf_counter() - t0
    sharpe = np.sqrt(252) * (p.mean() / (p.std() + 1e-9))
    print(
        {
            "throughput_rows_per_sec": int(len(df) / dt),
            "latency_sec": round(dt, 4),
            "sharpe": float(sharpe),
        }
    )


if __name__ == "__main__":
    import argparse
    import json

    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--window", type=int, default=20)
    ap.add_argument("--entry-z", type=float, default=1.0)
    ap.add_argument("--exit-z", type=float, default=0.2)
    ap.add_argument("--fee-bps", type=int, default=1)
    ap.add_argument("--slip-bps", type=int, default=2)
    args = ap.parse_args()

    df = generate_synth(n=args.n, seed=args.seed)
    pos = strategy(df, window=args.window, entry_z=args.entry_z, exit_z=args.exit_z)
    p = pnl(df, pos.values, fee_bps=args.fee_bps, slip_bps=args.slip_bps)

    from time import perf_counter  # if not already imported at top

    # compute metrics…
    sharpe = float(np.sqrt(252) * (p.mean() / (p.std() + 1e-9)))
    out = {
        "n": len(df),
        "window": args.window,
        "entry_z": args.entry_z,
        "exit_z": args.exit_z,
        "fee_bps": args.fee_bps,
        "slip_bps": args.slip_bps,
        "sharpe": sharpe,
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
