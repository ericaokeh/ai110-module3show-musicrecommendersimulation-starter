# 🎵 Music Recommender Simulation

## Project Summary

This project builds a content-based music recommender from scratch. It scores every song in a 20-song catalog against a user's stated preferences — genre, mood, energy, acousticness, and valence — and returns the top 5 matches with an explanation for every point awarded. Real-world recommenders like Spotify layer in collaborative filtering and behavioral signals on top of this kind of content scoring. This version focuses on making the math visible and explainable.

---

## How The System Works

### Data Flow

**Input (User Profile)** → **Process (Score every song)** → **Output (Top K ranked results)**

1. Load all songs from `data/songs.csv`
2. Remove any blocked song IDs before scoring runs
3. For each remaining song, compute a weighted score against the user profile
4. Sort all songs descending, apply genre cap (max 2 per genre) and artist cap (max 1 per artist), return Top K

---

### Song Features

Each song stores: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, `popularity` (0–100), `release_decade`, `mood_tags` (e.g. euphoric, calm, driving)

### User Preference Fields

| Field | Type | Purpose |
|---|---|---|
| `genre` | string | Binary match against `song.genre` |
| `mood` | string | Binary match against `song.mood` |
| `energy` | float 0–1 | Proximity scored against `song.energy` |
| `acousticness` | float 0–1 | Proximity scored against `song.acousticness` |
| `valence` | float 0–1 | Proximity scored against `song.valence` |
| `mood_tags` | list of strings | Overlap bonus with song's mood tags |
| `preferred_decade` | int | Bonus if song's decade matches |
| `min_popularity` | int | Enables popularity bonus in scoring |
| `blocked_ids` | list of int | Removed from candidate pool before scoring |

---

### Algorithm Recipe (Balanced Mode)

```
genre match       → +0.9 pts   (binary)
mood match        → +1.0 pts   (binary)
energy            → (1 - |user - song|) × 2.0
acousticness      → (1 - |user - song|) × 1.2
valence           → (1 - |user - song|) × 0.5
mood tag overlap  → number of matches × 0.8 / 3
decade match      → +0.3 pts   (binary)
popularity        → (song_pop / 100) × 0.3
```

Four scoring modes available: `balanced`, `genre-first`, `mood-first`, `energy-focused`

---

### Potential Biases

- **Genre scarcity** — most genres have only 1 song, so that song always wins for users of that genre regardless of numeric fit
- **Mood cliff** — "chill" and "relaxed" score the same as "chill" vs "angry" — binary, no partial credit
- **Energy distribution** — high-energy songs cluster 0.75–0.97, giving high-energy users more close matches than low-energy users (0.18–0.42)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python3 src/main.py
   ```

### Running Tests

```bash
pytest
```

---

## Experiments You Tried

**Genre weight at 2.0:** Every #1 result won because of the genre match alone. Numeric features didn't matter. The same song topped every profile that had a genre match — boring and inaccurate for edge cases.

**Genre weight dropped to 0.9, energy raised to 2.0:** Results got more interesting. The "Classical but Intense" profile now correctly surfaces Storm Runner (rock/intense) above Glass Cathedrals (classical/peaceful) because energy and mood carry more weight. The tradeoff is that genre preferences feel slightly weaker.

**Three adversarial profiles tested:**
- *High energy + sad mood* — the only soul/sad song still won, but intense rock songs jumped to #2/#3 because energy now dominates
- *Classical but intense* — Storm Runner (rock) beat Glass Cathedrals once energy weight increased, which is arguably more honest
- *Everything at 0.5* — top 5 spread across 5 different genres, scores compressed into a tight 40–60% band

**Four scoring modes compared:** Genre-first amplifies the catalog's scarcity problem. Mood-first gives better results when the user's mood is the main signal (e.g. "sad" or "focused"). Energy-focused works well for workout/activity profiles but makes scores feel inflated.

---

## Limitations and Risks

- **Catalog is too small** — 20 songs means most genres have one entry. The system can't really choose; it just defaults to the only option.
- **No learning** — weights are static. The system never improves based on what users skip or replay.
- **Manually assigned features** — energy, mood, and acousticness values are human estimates, not measured from audio. Two people might score the same song differently.
- **No lyrics or language understanding** — a song about heartbreak with high energy scores the same as a pump-up anthem if their audio features match.

---

## Reflection

Recommenders turn data into predictions by finding patterns between what a user says they want and what each item actually contains. The tricky part is that the features have to actually capture what makes something feel right — and in this project, the gap between the math and the vibe was the most interesting thing to watch. Library Rain scoring #1 for chill lofi felt genuinely correct. Gym Hero appearing in a happy pop list felt wrong even though the math was technically valid.

Bias shows up quietly. It is not always an error — sometimes it is just a consequence of the data being uneven. A classical user will always get Glass Cathedrals first not because the algorithm is unfair, but because it is the only classical song. That is the kind of thing that would never appear in a test as a failure but would frustrate a real user immediately.

[**Model Card →**](model_card.md)
