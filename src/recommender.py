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


# ─── Challenge 2: Scoring Modes (Strategy Pattern) ───────────────────────────

SCORING_MODES = {
    "balanced": {
        "genre":        0.9,
        "mood":         1.0,
        "energy":       2.0,
        "acousticness": 1.2,
        "valence":      0.5,
        "popularity":   0.3,
        "decade":       0.3,
        "mood_tags":    0.8,
    },
    "genre-first": {
        "genre":        3.0,
        "mood":         1.0,
        "energy":       1.0,
        "acousticness": 0.5,
        "valence":      0.3,
        "popularity":   0.2,
        "decade":       0.2,
        "mood_tags":    0.5,
    },
    "mood-first": {
        "genre":        0.5,
        "mood":         1.5,
        "energy":       1.0,
        "acousticness": 0.8,
        "valence":      1.0,
        "popularity":   0.2,
        "decade":       0.2,
        "mood_tags":    1.5,
    },
    "energy-focused": {
        "genre":        0.5,
        "mood":         0.5,
        "energy":       3.5,
        "acousticness": 1.5,
        "valence":      0.3,
        "popularity":   0.2,
        "decade":       0.2,
        "mood_tags":    0.3,
    },
}


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int/float."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":             int(row["id"]),
                "title":          row["title"],
                "artist":         row["artist"],
                "genre":          row["genre"],
                "mood":           row["mood"],
                "energy":         float(row["energy"]),
                "tempo_bpm":      float(row["tempo_bpm"]),
                "valence":        float(row["valence"]),
                "danceability":   float(row["danceability"]),
                "acousticness":   float(row["acousticness"]),
                "popularity":     int(row["popularity"]),
                "release_decade": int(row["release_decade"]),
                "mood_tags":      row["mood_tags"].split("|"),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score a song against user preferences using the selected scoring mode."""
    W = SCORING_MODES.get(mode, SCORING_MODES["balanced"])

    score = 0.0
    reasons = []

    # Genre match
    if song["genre"] == user_prefs.get("genre"):
        score += W["genre"]
        reasons.append(f"genre match (+{W['genre']})")

    # Mood match
    if song["mood"] == user_prefs.get("mood"):
        score += W["mood"]
        reasons.append(f"mood match (+{W['mood']})")

    # Numeric proximity features
    for feature, weight in [("energy", W["energy"]),
                             ("acousticness", W["acousticness"]),
                             ("valence", W["valence"])]:
        if feature in user_prefs:
            proximity = 1 - abs(user_prefs[feature] - song[feature])
            points = round(proximity * weight, 2)
            score += points
            reasons.append(f"{feature} proximity (+{points})")

    # Challenge 1: Popularity bonus (normalized 0-1)
    if "min_popularity" in user_prefs:
        pop_score = round((song["popularity"] / 100) * W["popularity"], 2)
        score += pop_score
        reasons.append(f"popularity {song['popularity']}/100 (+{pop_score})")

    # Challenge 1: Decade match bonus
    if "preferred_decade" in user_prefs:
        if song["release_decade"] == user_prefs["preferred_decade"]:
            score += W["decade"]
            reasons.append(f"decade match {song['release_decade']} (+{W['decade']})")

    # Challenge 1: Mood tags overlap bonus
    if "mood_tags" in user_prefs:
        user_tags = set(user_prefs["mood_tags"])
        song_tags = set(song["mood_tags"])
        overlap = user_tags & song_tags
        if overlap:
            tag_points = round(len(overlap) * W["mood_tags"] / 3, 2)
            score += tag_points
            reasons.append(f"mood tags {list(overlap)} (+{tag_points})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Score every song, apply diversity penalties, and return the top k results."""
    blocked_ids = set(user_prefs.get("blocked_ids", []))
    candidates = [s for s in songs if s["id"] not in blocked_ids]

    scored = []
    for song in candidates:
        score, reasons = score_song(user_prefs, song, mode=mode)
        explanation = ", ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    # Challenge 3: Diversity — max 2 per genre, max 1 per artist
    results = []
    genre_count = {}
    artist_seen = set()

    for song, score, explanation in scored:
        g = song["genre"]
        a = song["artist"]

        if genre_count.get(g, 0) >= 2:
            continue
        if a in artist_seen:
            continue

        results.append((song, score, explanation))
        genre_count[g] = genre_count.get(g, 0) + 1
        artist_seen.add(a)

        if len(results) == k:
            break

    return results
