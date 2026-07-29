import pandas as pd
from pathlib import Path
from stats import bootstrap_rate, summarize_rate

DATA_PATH = Path("data/processed/deliveries_with_style.csv")

def main():
    df = pd.read_csv(DATA_PATH)

    print("=== Dismissal rate by phase ===\n")
    for phase in ["powerplay", "middle", "death"]:
        subset = df[df["phase"] == phase]
        if len(subset) == 0:
            print(f"{phase}: no balls faced yet\n")
            continue
        rates = bootstrap_rate(subset["is_wicket"].values)
        summarize_rate(rates, phase, len(subset), subset["is_wicket"].sum(), invert=True)

    print("=== Strike rate by phase ===")
    sr_by_phase = (
        df.groupby("phase")
        .agg(balls=("batter_runs", "count"), runs=("batter_runs", "sum"))
    )
    sr_by_phase["strike_rate"] = (sr_by_phase["runs"] / sr_by_phase["balls"] * 100).round(1)
    print(sr_by_phase)

if __name__ == "__main__":
    main()