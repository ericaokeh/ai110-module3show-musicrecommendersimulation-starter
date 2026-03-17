# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Goal / Task

VibeMatch takes a user's stated preferences (genre, mood, energy level, acousticness, and valence) and returns the 5 best-matching songs from a 20-song catalog. It predicts what song fits a vibe, not what someone will click. Every recommendation includes a point-by-point explanation so the user knows exactly why each song ranked where it did.

---

## 3. How the Model Works

Every song gets a score from 0 to about 6 points. The score comes from two types of checks.

**Categorical checks (match or no match):** If the song's genre matches what the user asked for, it earns points. Same for mood. There is no partial credit; it either matches or it does not.

**Proximity checks (how close is close enough):** For energy, acousticness, and valence, the system measures the gap between what the user wants and what the song has. A perfect match earns the full weight. A song that is far away earns almost nothing. The formula is `1 - |user value - song value|`, multiplied by a weight that reflects how important that feature is.

Additional bonuses apply if the song's release decade matches, if the song's mood tags overlap with the user's requested tags, and if popularity scoring is turned on.

Blocked songs are removed before any scoring happens. The final list caps at 2 songs per genre and 1 song per artist so the same artist cannot dominate the results.

Four scoring modes let the user shift what matters most: `balanced`, `genre-first`, `mood-first`, or `energy-focused`.

---

## 4. Data

- **20 songs** total in `data/songs.csv`
- **10 original songs** from the starter project covering pop, lofi, rock, ambient, jazz, synthwave, and indie pop
- **10 added songs** to fill missing genres including hip-hop, r&b, folk, classical, metal, reggae, soul, electronic, country, and psychedelic
- Each song has: genre, mood, energy (0-1), tempo BPM, valence (0-1), danceability (0-1), acousticness (0-1), popularity (0-100), release decade, and mood tags
- Most genres have only 1 song. The dataset skews toward 2020s releases and reflects one person's interpretation of what these genres sound like.

---

## 5. Strengths

- Works well for users with clear, specific preferences. A lofi/chill or rock/intense user gets results that feel right on the first try.
- Fully transparent. Every point is printed with a reason so there are no mystery recommendations.
- Four scoring modes let users shift priorities without changing the underlying data.
- Artist and genre diversity caps prevent one artist from taking over the top 5.

---

## 6. Limitations and Bias

**Genre scarcity bias** is the biggest problem. Most genres appear once in the catalog, so any user whose favorite genre has one song will always see that song ranked first, even if its energy, mood, and acousticness are completely wrong. A classical user asking for intense, high-energy music gets Glass Cathedrals (peaceful, energy=0.18) near the top simply because it is the only classical song. This is a data problem, not a math problem.

**Mood cliff matching** means "chill" and "relaxed" score identically to "chill" and "angry" because mood matching is binary. A song that is close in feel but uses a different mood label gets zero points for mood.

**Energy distribution asymmetry** gives high-energy users a structural advantage. High-energy songs cluster between 0.75-0.97 so there are more close matches available. Low-energy songs cluster between 0.18-0.42, leaving fewer options for users who want calm music.

---

## 7. Evaluation

**Six profiles tested:** High-Energy Pop, Chill Lofi, Deep Intense Rock, and three adversarial cases: high energy with a sad mood, classical with an intense mood, and everything set to 0.5.

**What worked:** Clean profiles matched intuition right away. Library Rain ranked number one for chill lofi on every weight configuration tested. Storm Runner always topped deep intense rock.

**What surprised me:** Gym Hero kept appearing in the Happy Pop top 5 even though the user wanted a happy mood. Gym Hero is tagged as intense. But it is a pop song with energy=0.93, so genre and energy pushed it up despite the mood mismatch. It is technically correct by the math but feels wrong as a recommendation, like asking for a birthday party playlist and getting a pre-workout track instead.

**Weight experiments:** Genre at 2.0 made every result predictable and boring. Genre at 0.9 with energy at 2.0 produced the most interesting and honest results across all six profiles. No single weight configuration worked perfectly for every profile.

---

## 8. Intended Use and Non-Intended Use

**Intended for:** Learning how content-based recommender systems work. This project is a classroom simulation, good for understanding weighted scoring, proximity math, filter bubbles, and the tradeoff between genre matching and numeric feature matching.

**Not intended for:** Real users or real products. The catalog is too small, the feature values are manually estimated, and there is no feedback loop. Using this to make actual music recommendations for real people would produce results that feel random to anyone outside the narrow profiles it was tuned for.

---

## 9. Ideas for Improvement

- **Expand the catalog:** at least 5 songs per genre so the system has real choices instead of defaulting to the only match
- **Partial mood scoring:** group similar moods into clusters like (chill/relaxed/peaceful) or (intense/angry/energetic) and award partial points for near-matches
- **Feedback loop:** track skips and saves to nudge weights over time, turning the static formula into something that actually learns the user's taste

---

## 10. Personal Reflection

**Biggest learning moment:** The weights are not just math, they are decisions. Every time I changed a number, I was deciding what matters more to a listener. When genre was at 2.0, the system felt confident but boring. When I dropped it to 0.9, the results got more interesting but occasionally contradicted the user's stated preference. There is no correct answer, just tradeoffs.

**How AI tools helped, and when I had to double-check:** AI tools made the coding fast. I could describe what I wanted in plain language and get working code back immediately, which meant I spent more time reading the output than writing the logic. But the AI never caught that Gym Hero showing up in a happy playlist was wrong. It produced code that ran without errors and still gave bad recommendations. Checking whether results actually made sense was something I had to do myself.

**What surprised me about simple algorithms feeling like recommendations:** Library Rain scoring number one for chill lofi genuinely felt right. Not because the algorithm is smart (it is just five numbers being added up) but because the features captured something real about how that song sounds. That gap between simple math and a result that feels meaningful was the most interesting discovery in the whole project.

**What I would try next:** Add a feedback loop. Even something simple like flagging a song as skipped or replayed and nudging the relevant feature weights up or down. That one change is the core difference between this simulation and what Spotify is actually doing.
