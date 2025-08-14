# Intraday Micro-Backtest (Mean-Reversion)

**Vectorized NumPy/pandas micro-backtest** for a simple mean-reversion strategy.  
Prints performance metrics (throughput/latency) and strategy quality (Sharpe). Educational only — not investment advice.

## Features
- **Vectorized** computations (NumPy/pandas) for speed
- **Configurable** window, entry/exit thresholds, and trading costs
- **CLI** interface that prints a JSON summary (easy to parse)
- Basic **performance telemetry** (rows/sec, end-to-end latency)
- Unit **tests** + optional installable package layout

---

## Install

From repo root (inside your venv):

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
# install package in editable mode so 'python -m intraday_micro_backtest.backtest' works
pip install -e .
```

Run tests:

```bash
pytest
```

---

## Usage

Run with defaults:

```bash
python -m intraday_micro_backtest.backtest
```

Run with custom parameters:

```bash
python -m intraday_micro_backtest.backtest   --n 20000   --seed 0   --window 30   --entry-z 1.5   --exit-z 0.3   --fee-bps 0   --slip-bps 0
```

### CLI arguments

| Flag          | Type  | Default | Meaning |
|---|---:|---:|---|
| `--n`         | int   | 20000   | Number of synthetic ticks/rows |
| `--seed`      | int   | 0       | RNG seed for reproducibility |
| `--window`    | int   | 20      | Rolling window (returns) for z-score |
| `--entry-z`   | float | 1.0     | Enter long/short when \|z\| exceeds this |
| `--exit-z`    | float | 0.2     | Flatten when \|z\| falls below this |
| `--fee-bps`   | int   | 1       | Per-trade fee in basis points |
| `--slip-bps`  | int   | 2       | Slippage in basis points |

> **Note:** Costs (`fee-bps`, `slip-bps`) are applied on position changes.

---

## Example output

Command:

```bash
python -m intraday_micro_backtest.backtest --window 30 --entry-z 1.5 --exit-z 0.3 --fee-bps 0 --slip-bps 0
```

Output (two lines):

```json
{"n": 20000, "window": 30, "entry_z": 1.5, "exit_z": 0.3, "fee_bps": 0, "slip_bps": 0, "sharpe": -0.011407803236681216}
```

```
{'throughput_rows_per_sec': 6120400, 'latency_sec': 0.0033, 'sharpe': -10.515386317065339}
```

- The **first line** is a **JSON** summary (easy to capture/parse).  
- The **second line** is an internal performance summary. If you prefer a single JSON output, you can keep the JSON print and remove the extra summary print in `backtest.py`.

---

## Results (sample, on my machine)

| Metric | Value | Notes |
|---|---:|---|
| Throughput (rows/sec) | **6,120,400** | n=20,000 synthetic rows |
| Latency (sec) | **0.0033** | End-to-end run time |
| Sharpe (JSON) | **-0.0114** | With seed=0; depends on params/seed |

> Synthetic random walks + costs often yield negative Sharpe by default. Tune `window`, `entry-z`, `exit-z`, and costs to explore behaviour.

---

## Project structure

```
intraday_micro_backtest/
├─ src/
│  └─ intraday_micro_backtest/
│     ├─ __init__.py
│     └─ backtest.py
├─ tests/
│  └─ test_backtest.py
├─ pyproject.toml
├─ setup.cfg
├─ requirements.txt
└─ README.md
```

---

## How it works (brief)

1. **Synthetic price series**: random-walk mid price  
2. **Signal**: z-score of returns over a rolling window  
3. **Position**: enter long/short when \|z\| > entry-z; flatten when \|z\| < exit-z  
4. **P&L**: previous position × next return minus costs on turns  
5. **Sharpe**: mean/std (implementation detail may vary — see code)

---

## Dev tips

- Reproducibility: set `--seed` and pin package versions if benchmarking.
- Parsing JSON output:
  ```bash
  python -m intraday_micro_backtest.backtest --window 30 ... | head -1 > run.json
  ```
- If you see an import warning when running as a module, ensure your `__init__.py` does **not** import `backtest` at import time (keep it minimal).

---

## Next steps (nice enhancements)

- Add **plots** (equity curve, drawdown) saved to `figures/`
- Add **CLI flags** for output directory and PNG saving
- Add an optional **real dataset** loader (CSV) with date parsing
- Export metrics as a **single JSON** object (consolidated)

---

## License

MIT — see `LICENSE`.

---

*This repository is for educational purposes and does not constitute investment advice.*

