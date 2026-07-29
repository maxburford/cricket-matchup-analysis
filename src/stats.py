import numpy as np
import pandas as pd

def bootstrap_rate(is_event: np.ndarray, n_bootstraps: int = 10000, seed: int = 42) -> np.ndarray:
    """Generic bootstrap: resamples a boolean array with replacement
    n_bootstraps times, returns the rate (mean) for each resample.
    Works for dismissal rate, boundary rate, or any other 0/1 outcome."""
    rng = np.random.default_rng(seed)
    n = len(is_event)
    is_event = is_event.astype(int)
    rates = np.empty(n_bootstraps)
    for i in range(n_bootstraps):
        sample_idx = rng.integers(0, n, size=n)
        rates[i] = is_event[sample_idx].mean()
    return rates

def summarize_rate(rates: np.ndarray, label: str, n: int, n_events: int, invert: bool = False):
    """Print point estimate and 95% CI. If invert=True, also show the
    '1 in every X balls' framing (useful for dismissal rate)."""
    point_estimate = rates.mean()
    lower, upper = np.percentile(rates, [2.5, 97.5])
    print(f"{label} (n={n} balls, {n_events} events):")
    print(f"  rate per ball: {point_estimate:.4f}")
    print(f"  95% CI: [{lower:.4f}, {upper:.4f}]")
    if invert and point_estimate > 0:
            upper_display = f"{1/lower:.1f}" if lower > 0 else "inf (too few events to bound)"
            print(f"  balls per event: {1/point_estimate:.1f} "
                f"(CI: {1/upper:.1f} to {upper_display})")
    print()