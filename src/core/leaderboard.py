import os
import json
import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "leaderboard.json")

def is_valid_name(name: str) -> bool:
    if not (3 <= len(name) <= 12):
        return False
    # Allow alphanumeric, underscore, and Vietnamese characters
    return bool(re.match(r"^[\w\sÀ-ỹ]{3,12}$", name))

def get_leaderboard() -> List[Dict[str, Any]]:
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("entries", [])
    except Exception:
        return []

def save_leaderboard(entries: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(LEADERBOARD_FILE), exist_ok=True)
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump({"entries": entries}, f, indent=2, ensure_ascii=False)

def add_leaderboard_entry(name: str, score: int, nights_won: int, seed: int) -> bool:
    if not is_valid_name(name):
        return False

    entries = get_leaderboard()
    now_iso = datetime.now(timezone.utc).astimezone().isoformat()

    new_entry = {
        "name": name.strip(),
        "score": int(score),
        "nights_won": int(nights_won),
        "achieved_at": now_iso,
        "seed": int(seed)
    }
    entries.append(new_entry)

    # Sort descending by score; equal scores preserve FIFO order (earlier achiever first)
    # Python sort is stable, so sorting with reverse=True on score preserves earlier additions
    entries.sort(key=lambda x: x["score"], reverse=True)

    # Keep top 10
    entries = entries[:10]
    save_leaderboard(entries)
    return True

def export_leaderboard(out_path: str):
    entries = get_leaderboard()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"entries": entries}, f, indent=2, ensure_ascii=False)

