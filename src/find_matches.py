import json
import csv
from pathlib import Path

RAW_DIR = Path("data/raw/ipl_json")
PEOPLE_CSV = Path("data/raw/people.csv")

def get_player_id(player_name: str) -> str:
    """Look up a player's Cricsheet identifier by name."""
    with open(PEOPLE_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["name"] == player_name:
                return row["identifier"]
    raise ValueError(f"No identifier found for {player_name}")

def find_matches_with_player(player_id: str) -> list[Path]:
    """Return paths of match files where this player_id appears."""
    matches = []
    for filepath in RAW_DIR.glob("*.json"):
        with open(filepath, encoding="utf-8") as f:
            match = json.load(f)
        people = match.get("info", {}).get("registry", {}).get("people", {})
        if player_id in people.values():
            matches.append(filepath)
    return matches

if __name__ == "__main__":
    player_id = get_player_id("V Suryavanshi")
    print(f"Player ID: {player_id}")
    matches = find_matches_with_player(player_id)
    print(f"Found {len(matches)} matches")
    for m in matches[:5]:
        print(m)