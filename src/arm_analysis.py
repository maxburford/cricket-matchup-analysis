import pandas as pd
from pathlib import Path
from stats import bootstrap_rate, summarize_rate

DATA_PATH = Path("data/processed/deliveries_with_style.csv")

def main():
    df = pd.read_csv(DATA_PATH)
    df["matchup"] = df["arm"] + "-arm " + df["bowl_type"]

    print("=== Dismissal rate by arm + bowl type ===\n")
    for matchup in sorted(df["matchup"].unique()):
        subset = df[df["matchup"] == matchup]
        rates = bootstrap_rate(subset["is_wicket"].values)
        summarize_rate(rates, matchup, len(subset), subset["is_wicket"].sum(), invert=True)

    print("=== Sample size reality check ===")
    print(df.groupby("matchup").size().sort_values(ascending=False))
    print("\nRule of thumb used in this project: under ~10 dismissal events,")
    print("treat the confidence interval as informative but not conclusive.")

if __name__ == "__main__":
    main()