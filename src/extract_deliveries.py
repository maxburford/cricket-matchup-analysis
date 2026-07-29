import json
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw/ipl_json")
PLAYER_ID = "470f446b"

def load_match(filepath: Path) -> dict:
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def get_player_name_in_match(match: dict, player_id: str) -> str | None:
    """The name string used inside deliveries can vary slightly per match,
    so look up which exact string this match uses for our player_id."""
    people = match.get("info", {}).get("registry", {}).get("people", {})
    for name, pid in people.items():
        if pid == player_id:
            return name
    return None

def extract_deliveries_for_player(match: dict, filepath: Path, player_id: str) -> list[dict]:
    player_name = get_player_name_in_match(match, player_id)
    if player_name is None:
        return []

    match_id = filepath.stem
    info = match.get("info", {})
    date = info.get("dates", [None])[0]
    season = info.get("season")
    teams = info.get("teams", [])
    venue = info.get("venue")

    rows = []
    for innings in match.get("innings", []):
        batting_team = innings.get("team")
        opponent = next((t for t in teams if t != batting_team), None)
        for over_block in innings.get("overs", []):
            over_num = over_block.get("over")
            for ball_index, delivery in enumerate(over_block.get("deliveries", []), start=1):
                if delivery.get("batter") != player_name:
                    continue
                runs = delivery.get("runs", {})
                wickets = delivery.get("wickets", [])
                dismissed = any(w.get("player_out") == player_name for w in wickets)
                dismissal_kind = next(
                    (w.get("kind") for w in wickets if w.get("player_out") == player_name),
                    None
                )
                rows.append({
                    "match_id": match_id,
                    "date": date,
                    "season": season,
                    "batting_team": batting_team,
                    "opponent": opponent,
                    "venue": venue,
                    "over": over_num,
                    "ball": ball_index,
                    "bowler": delivery.get("bowler"),
                    "batter_runs": runs.get("batter", 0),
                    "total_runs": runs.get("total", 0),
                    "is_wicket": dismissed,
                    "dismissal_kind": dismissal_kind,
                })
    return rows

def main():
    all_rows = []
    for filepath in sorted(RAW_DIR.glob("*.json")):
        match = load_match(filepath)
        people = match.get("info", {}).get("registry", {}).get("people", {})
        if PLAYER_ID not in people.values():
            continue
        all_rows.extend(extract_deliveries_for_player(match, filepath, PLAYER_ID))

    df = pd.DataFrame(all_rows)
    out_path = Path("data/processed/suryavanshi_deliveries.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Extracted {len(df)} deliveries faced across {df['match_id'].nunique()} matches")
    print(df.head())

if __name__ == "__main__":
    main()