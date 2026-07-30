import argparse
import pandas as pd
from pathlib import Path
from stats import bootstrap_rate, summarize_rate

def main():
    parser = argparse.ArgumentParser(description="Bootstrap dismissal-rate confidence intervals by bowl type.")
    parser.add_argument("--name", required=True, help="Matches the name used in build_matchup_table.py, e.g. kohli")
    args = parser.parse_args()

    df = pd.read_csv(f"data/processed/{args.name}_with_style.csv")
    for bowl_type in ["pace", "spin"]:
        subset = df[df["bowl_type"] == bowl_type]
        rates = bootstrap_rate(subset["is_wicket"].values)
        summarize_rate(rates, bowl_type, len(subset), subset["is_wicket"].sum(), invert=True)

if __name__ == "__main__":
    main()