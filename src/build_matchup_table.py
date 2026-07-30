import argparse
import pandas as pd
from pathlib import Path

LOOKUP_PATH = Path("src/bowler_lookup.csv")

def assign_phase(over: int) -> str:
    """Cricsheet overs are zero-indexed, so over 0 = the 1st over."""
    if over < 6:
        return "powerplay"
    elif over < 15:
        return "middle"
    else:
        return "death"

def main():
    parser = argparse.ArgumentParser(description="Join bowler style onto a player's deliveries and add phase.")
    parser.add_argument("--name", required=True, help="Matches the name used in extract_deliveries.py, e.g. kohli")
    args = parser.parse_args()

    deliveries_path = Path(f"data/processed/{args.name}_deliveries.csv")
    out_path = Path(f"data/processed/{args.name}_with_style.csv")

    deliveries = pd.read_csv(deliveries_path)
    lookup = pd.read_csv(LOOKUP_PATH)

    dupes = lookup[lookup.duplicated(subset="bowler", keep=False)]
    if len(dupes) > 0:
        print("ERROR: duplicate bowler entries in lookup file:")
        print(dupes)
        return

    merged = deliveries.merge(lookup, on="bowler", how="left")
    merged["phase"] = merged["over"].apply(assign_phase)

    unmapped = merged[merged["bowl_type"].isna()]["bowler"].unique()
    if len(unmapped) > 0:
        print("WARNING: these bowlers have no style mapping yet:")
        for name in unmapped:
            print(f"  - {name}")
        print("Add them to src/bowler_lookup.csv before trusting the summary below.\n")

    merged.to_csv(out_path, index=False)

    summary = (
        merged.dropna(subset=["bowl_type"])
        .groupby("bowl_type")
        .agg(
            balls_faced=("batter_runs", "count"),
            runs_scored=("batter_runs", "sum"),
            dismissals=("is_wicket", "sum"),
        )
    )
    summary["strike_rate"] = (summary["runs_scored"] / summary["balls_faced"] * 100).round(1)
    summary["balls_per_dismissal"] = (summary["balls_faced"] / summary["dismissals"]).round(1)

    print("Performance by bowl type:")
    print(summary)

if __name__ == "__main__":
    main()