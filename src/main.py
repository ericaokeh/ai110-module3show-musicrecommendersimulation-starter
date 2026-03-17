"""
Command line runner for the Music Recommender Simulation.
"""

from recommender import load_songs, recommend_songs

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


PROFILES = {
    "High-Energy Pop": {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.90,
        "acousticness": 0.10,
        "valence":      0.85,
        "mood_tags":    ["euphoric", "uplifting"],
        "preferred_decade": 2020,
        "min_popularity": 60,
    },
    "Chill Lofi": {
        "genre":        "lofi",
        "mood":         "chill",
        "energy":       0.35,
        "acousticness": 0.80,
        "valence":      0.55,
        "mood_tags":    ["calm", "nostalgic", "focused"],
        "preferred_decade": 2020,
        "min_popularity": 50,
    },
    "Deep Intense Rock": {
        "genre":        "rock",
        "mood":         "intense",
        "energy":       0.92,
        "acousticness": 0.08,
        "valence":      0.40,
        "mood_tags":    ["aggressive", "powerful", "driving"],
        "preferred_decade": 2010,
        "min_popularity": 60,
    },
    # Edge cases
    "Conflicted: High Energy but Sad": {
        "genre":        "soul",
        "mood":         "sad",
        "energy":       0.90,
        "acousticness": 0.50,
        "valence":      0.20,
        "mood_tags":    ["dark", "melancholic"],
    },
    "Genre Mismatch: Classical but Intense": {
        "genre":        "classical",
        "mood":         "intense",
        "energy":       0.85,
        "acousticness": 0.90,
        "valence":      0.50,
        "mood_tags":    ["powerful", "vast"],
    },
    "Impossible Middle: Everything at 0.5": {
        "genre":        "ambient",
        "mood":         "focused",
        "energy":       0.50,
        "acousticness": 0.50,
        "valence":      0.50,
        "mood_tags":    ["calm", "dreamy"],
    },
}


def print_recommendations(label, user_prefs, recommendations, mode, max_score):
    print(f"\n{'=' * 62}")
    print(f"  Profile : {label}")
    print(f"  Mode    : {mode}")
    print(f"  Prefs   : genre={user_prefs.get('genre')}  mood={user_prefs.get('mood')}  energy={user_prefs.get('energy')}")
    print(f"{'=' * 62}")

    if not recommendations:
        print("  No results.\n")
        return

    if HAS_TABULATE:
        # Challenge 4: tabulate formatted table
        rows = []
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            pct = f"{round((score / max_score) * 100, 1)}%"
            rows.append([
                f"#{i}",
                f"{song['title']} — {song['artist']}",
                song["genre"],
                song["mood"],
                f"{score:.2f} ({pct})",
                explanation[:60] + "..." if len(explanation) > 60 else explanation,
            ])
        print(tabulate(
            rows,
            headers=["#", "Song — Artist", "Genre", "Mood", "Score", "Why"],
            tablefmt="rounded_outline"
        ))
    else:
        # ASCII fallback
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            pct = round((score / max_score) * 100, 1)
            print(f"\n  #{i}  {song['title']} — {song['artist']}")
            print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Pop: {song['popularity']}/100  |  {song['release_decade']}s")
            print(f"       Score: {score:.2f} / {max_score}  ({pct}%)")
            print(f"       Why:   {explanation}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Run each profile in all 4 scoring modes
    modes_to_run = ["balanced", "genre-first", "mood-first", "energy-focused"]
    max_scores = {"balanced": 6.0, "genre-first": 6.7, "mood-first": 6.5, "energy-focused": 7.3}

    for label, user_prefs in PROFILES.items():
        for mode in modes_to_run:
            recs = recommend_songs(user_prefs, songs, k=5, mode=mode)
            print_recommendations(label, user_prefs, recs, mode, max_scores[mode])


if __name__ == "__main__":
    main()
