import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path("data/processed/deliveries_with_style.csv")
N_BOOTSTRAPS = 10000
np.random.seed(42)  # makes results reproducible run to run

def bootstrap_dismissal_rate(deliveries: pd.DataFrame, n_bootstraps: int = N_BOOTSTRAPS) -> np.ndarray:
    """Resample the deliveries with replacement n_bootstraps times,
    return the dismissal rate (dismissals per ball) for each resample."""
    n = len(deliveries)
    is_wicket = deliveries["is_wicket"].values.astype(int)
    rates = np.empty(n_bootstraps)
    for i in range(n_bootstraps):
        sample_idx = np.random.randint(0, n, size=n)
        resampled = is_wicket[sample_idx]
        rates[i] = resampled.mean()
    return rates

def summarize(rates: np.ndarray, label: str):
    point_estimate = rates.mean()
    lower, upper = np.percentile(rates, [2.5, 97.5])
    print(f"{label}:")
    print(f"  dismissal rate per ball: {point_estimate:.4f}")
    print(f"  95% CI: [{lower:.4f}, {upper:.4f}]")
    print(f"  in balls-per-dismissal terms: {1/point_estimate:.1f} "
          f"(CI: {1/upper:.1f} to {1/lower:.1f})\n")

def main():
    df = pd.read_csv(DATA_PATH)

    for bowl_type in ["pace", "spin"]:
        subset = df[df["bowl_type"] == bowl_type]
        rates = bootstrap_dismissal_rate(subset)
        summarize(rates, f"{bowl_type} (n={len(subset)} balls, {subset['is_wicket'].sum()} dismissals)")

if __name__ == "__main__":
    main()