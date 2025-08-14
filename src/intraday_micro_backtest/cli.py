import argparse
import json
import time
from pathlib import Path

import numpy as np

from .backtest import generate_synth, pnl, strategy
from .plotting import save_equity_and_drawdown


def _nowstamp():
    return time.strftime("%Y%m%d-%H%M%S")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--window", type=int, default=20)
    ap.add_argument("--entry-z", type=float, default=1.0)
    ap.add_argument("--exit-z", type=float, default=0.2)
    ap.add_argument("--fee-bps", type=float, default=1.0)
    ap.add_argument("--slip-bps", type=float, default=2.0)
    ap.add_argument("--outdir", type=str, default=f"runs/{_nowstamp()}")
    args = ap.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    df = generate_synth(n=args.n, seed=args.seed)

    t0 = time.perf_counter()
    pos = strategy(df, window=args.window, entry_z=args.entry_z, exit_z=args.exit_z)
    p = pnl(df, pos.values, fee_bps=args.fee_bps, slip_bps=args.slip_bps)
    dt = time.perf_counter() - t0

    equity = (1 + p).cumprod()
    dd = equity / equity.cummax() - 1
    sharpe = float(np.sqrt(252) * (p.mean() / (p.std() + 1e-12)))
    max_dd = float(dd.min())

    save_equity_and_drawdown(equity, dd, out / "equity_drawdown.png")
    (out / "params.json").write_text(json.dumps(vars(args), indent=2))

    metrics = {
        "rows": len(df),
        "throughput_rows_per_sec": int(len(df) / dt),
        "latency_sec": round(dt, 6),
        "sharpe": round(sharpe, 4),
        "max_drawdown": round(max_dd, 4),
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
