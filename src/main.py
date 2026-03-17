"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.80,
        "acousticness": 0.20,
        "valence":      0.80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"  Profile: {user_prefs['genre']} / {user_prefs['mood']} / energy {user_prefs['energy']}")
    print("=" * 50)

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        normalized = round((score / 7.0) * 100, 1)
        print(f"\n#{i}  {song['title']} — {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 7.0  ({normalized}%)")
        print(f"    Why:   {explanation}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
