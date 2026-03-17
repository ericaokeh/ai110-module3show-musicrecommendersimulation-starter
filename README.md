# 🎵 Music Recommender Simulation

## Project Summary

Real-world recommenders like Spotify filter out blocked content first, then score what's left using a mix of collaborative signals (what similar users liked) and content signals (audio features like energy and tempo) — all weighted and tuned continuously by skips, replays, and saves. My version keeps it focused: pure content-based scoring across 20 songs using genre, mood, energy, acousticness, and valence. Each song gets a score based on how closely it matches the user's stated preferences — genre match carries the most weight because a wrong genre is a dealbreaker, mood is second, and numeric features use `1 - |user_value - song_value|` to reward closeness over raw values. Blocked songs are filtered before scoring runs. The priority is explainability — every recommendation traces directly back to something in the user's profile, with a reason printed for every point awarded.

---

## How The System Works

### Data Flow

**Input (User Profile)** → **Process (Score every song)** → **Output (Top K ranked results)**

1. Load all songs from `data/songs.csv`
2. Remove any blocked song IDs before scoring runs
3. For each remaining song, compute a score against the user profile
4. Sort all scored songs descending, apply a genre cap (max 2 per genre), return Top K with score and explanation

---

### Song Features

Each `Song` stores: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`

### User Preference Fields

| Field | Type | Purpose |
|---|---|---|
| `genre` | string | Matched against `song.genre` — binary match |
| `mood` | string | Matched against `song.mood` — binary match |
| `energy` | float 0–1 | Proximity scored against `song.energy` |
| `acousticness` | float 0–1 | Proximity scored against `song.acousticness` |
| `valence` | float 0–1 | Proximity scored against `song.valence` |
| `blocked_ids` | list of int | Songs removed from candidate pool before scoring |

---

### Algorithm Recipe

**Categorical features — binary match × weight:**
```
genre match  → +2.0 points
mood match   → +1.0 points
```

**Numeric features — proximity × weight:**
```
energy score       = (1 - |user.target_energy - song.energy|)       × 1.5
acousticness score = (1 - |user.acousticness  - song.acousticness|) × 1.2
valence score      = (1 - |user.valence       - song.valence|)      × 0.5
```

**Max possible score: 7.0**
**Normalized to 0–100:** `(score / 7.0) × 100`

---

### Potential Biases

- **Genre over-prioritization** — a mediocre song in the right genre can outscore a near-perfect match in a different genre. Great songs outside the user's favorite genre may never surface.
- **Filter bubble** — pure content-based scoring only recommends more of what the user already likes. No discovery or surprise built in.
- **Small catalog bias** — with 20 songs, some genres appear once. If the user's favorite genre has one song, that song almost always wins regardless of numeric fit.
- **Binary mood matching** — mood is either a full point or zero, even though some moods are closer in feel than others (e.g. "chill" is closer to "relaxed" than to "intense").

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

