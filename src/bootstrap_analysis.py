import pandas as pd
from pathlib import Path
from stats import bootstrap_rate, summarize_rate

DATA_PATH = Path("data/processed/deliveries_with_style.csv")

def main():
    df = pd.read_csv(DATA_PATH)
    for bowl_type in ["pace", "spin"]:
        subset = df[df["bowl_type"] == bowl_type]
        rates = bootstrap_rate(subset["is_wicket"].values)
        summarize_rate(rates, bowl_type, len(subset), subset["is_wicket"].sum(), invert=True)

if __name__ == "__main__":
    main()