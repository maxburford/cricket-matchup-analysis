import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/processed/kohli_with_style.csv")
LOOKUP_PATH = Path("src/bowler_lookup.csv")

def main():
    deliveries = pd.read_csv(DATA_PATH)
    lookup = pd.read_csv(LOOKUP_PATH)

    unmapped = deliveries[~deliveries["bowler"].isin(lookup["bowler"])]
    counts = unmapped.groupby("bowler").size().sort_values(ascending=False)

    total_unmapped_balls = len(unmapped)
    total_balls = len(deliveries)
    print(f"{total_unmapped_balls} of {total_balls} balls ({total_unmapped_balls/total_balls:.1%}) are unmapped\n")
    print("Top 40 unmapped bowlers by balls faced:")
    print(counts.head(40))

if __name__ == "__main__":
    main()