import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from stats import bootstrap_rate

OUT_DIR = Path("charts")
OUT_DIR.mkdir(exist_ok=True)

PLAYERS = {
    "suryavanshi": "V Suryavanshi (2025-2026, 23 matches)",
    "kohli": "V Kohli (2008-2026, 275 matches)",
    "williamson": "K Williamson (2017-2026, 76 matches)",
}

def get_ci_for_bowl_type(name: str, bowl_type: str):
    df = pd.read_csv(f"data/processed/{name}_with_style.csv")
    subset = df[df["bowl_type"] == bowl_type]
    rates = bootstrap_rate(subset["is_wicket"].values)
    point = 1 / rates.mean()
    lower, upper = np.percentile(rates, [2.5, 97.5])
    return point, 1 / upper, 1 / lower  # point, ci_low, ci_high (inverted, so bounds swap)

def make_comparison_chart():
    fig, ax = plt.subplots(figsize=(8, 5))
    x_labels = []
    points = []
    err_low = []
    err_high = []
    colors = []

    for name, label in PLAYERS.items():
        for bowl_type, color in [("pace", "#4C72B0"), ("spin", "#DD8452")]:
            point, ci_low, ci_high = get_ci_for_bowl_type(name, bowl_type)
            x_labels.append(f"{label.split(' (')[0]}\n{bowl_type}")
            points.append(point)
            err_low.append(point - ci_low)
            err_high.append(ci_high - point)
            colors.append(color)

    x = np.arange(len(x_labels))
    ax.bar(x, points, yerr=[err_low, err_high], capsize=5, color=colors, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_ylabel("Balls per dismissal (higher = harder to dismiss)")
    ax.set_title("Dismissal rate vs pace and spin, with 95% confidence intervals")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "pace_vs_spin_comparison.png", dpi=150)
    plt.close()
    print("Saved charts/pace_vs_spin_comparison.png")

def make_phase_chart():
    df = pd.read_csv("data/processed/suryavanshi_with_style.csv")
    phases = ["powerplay", "middle", "death"]
    points, err_low, err_high = [], [], []

    for phase in phases:
        subset = df[df["phase"] == phase]
        if subset["is_wicket"].sum() == 0:
            points.append(0); err_low.append(0); err_high.append(0)
            continue
        rates = bootstrap_rate(subset["is_wicket"].values)
        point = 1 / rates.mean()
        lower, upper = np.percentile(rates, [2.5, 97.5])
        points.append(point)
        err_low.append(point - (1/upper) if upper > 0 else 0)
        err_high.append((1/lower) - point if lower > 0 else 0)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(phases, points, yerr=[err_low, err_high], capsize=5, color="#55A868", alpha=0.85)
    ax.set_ylabel("Balls per dismissal")
    ax.set_title("Suryavanshi: dismissal rate by innings phase")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "suryavanshi_phase.png", dpi=150)
    plt.close()
    print("Saved charts/suryavanshi_phase.png")

if __name__ == "__main__":
    make_comparison_chart()
    make_phase_chart()