# src/plotting.py
import matplotlib.pyplot as plt


def save_equity_and_drawdown(equity, drawdown, path):
    fig = plt.figure(figsize=(7, 4))
    ax = plt.gca()
    ax.plot(equity.index, equity.values, label="Equity")
    ax.set_xlabel("Index")
    ax.set_ylabel("Equity (×)")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
