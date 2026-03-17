from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int/float."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences using weighted category matches and numeric proximity."""
    WEIGHTS = {
        "genre":        2.0,
        "mood":         1.0,
        "energy":       1.5,
        "acousticness": 1.2,
        "valence":      0.5,
    }
    MAX_SCORE = 7.0

    score = 0.0
    reasons = []

    # Categorical: binary match
    if song["genre"] == user_prefs.get("genre"):
        score += WEIGHTS["genre"]
        reasons.append(f"genre match (+{WEIGHTS['genre']})")

    if song["mood"] == user_prefs.get("mood"):
        score += WEIGHTS["mood"]
        reasons.append(f"mood match (+{WEIGHTS['mood']})")

    # Numeric: proximity scoring
    for feature, weight in [("energy", WEIGHTS["energy"]),
                             ("acousticness", WEIGHTS["acousticness"]),
                             ("valence", WEIGHTS["valence"])]:
        if feature in user_prefs:
            proximity = 1 - abs(user_prefs[feature] - song[feature])
            points = round(proximity * weight, 2)
            score += points
            reasons.append(f"{feature} proximity (+{points})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, filter blocked IDs, enforce a genre cap, and return the top k results."""
    blocked_ids = set(user_prefs.get("blocked_ids", []))
    candidates = [s for s in songs if s["id"] not in blocked_ids]

    scored = []
    for song in candidates:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    # Genre cap: max 2 songs per genre
    results = []
    genre_count = {}
    for song, score, explanation in scored:
        g = song["genre"]
        if genre_count.get(g, 0) < 2:
            results.append((song, score, explanation))
            genre_count[g] = genre_count.get(g, 0) + 1
        if len(results) == k:
            break

    return results
