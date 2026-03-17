# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Goal / Task

VibeMatch suggests songs from a small catalog based on what a user tells us they like. Given a preferred genre, mood, and energy level, it scores every song and returns the top 5 that best match. It is not trying to predict what you will click — it is trying to find songs that feel right for the vibe you described.

---

## 3. Algorithm Summary

Every song in the catalog gets a score. The score is built from five things:

- If the song's **genre** matches what the user wants, it gets points.
- If the song's **mood** matches, it gets points.
- For **energy**, **acousticness**, and **valence**, the system measures how close the song's value is to what the user asked for. A perfect match gets full points. A song that is far away gets fewer.

All five scores are added up. Songs with blocked IDs are removed before scoring even starts. The top 5 results are returned, with a cap of 2 songs per genre to keep the list varied.

---

## 4. Data

The catalog has 20 songs stored in a CSV file. Each song has a title, artist, genre, mood, and five numeric features: energy, tempo, valence, danceability, and acousticness. The 10 original songs came with the project. Ten more were added to cover genres and moods that were missing — including hip-hop, r&b, folk, classical, metal, reggae, soul, electronic, country, and psychedelic. Moods like sad, nostalgic, romantic, peaceful, angry, energetic, and dreamy were added to fill gaps. The dataset is still very small and mostly reflects one person's idea of what these genres sound like.

---

## 5. Strengths

The system works best when the user's preferences are clear and specific. A lofi/chill user or a rock/intense user gets results that feel right immediately — the top song matches on every dimension. The scoring is fully transparent: every point is printed with a reason, so you always know exactly why a song ranked where it did. It also handles blocking correctly — songs the user has rejected never appear, even if they would have scored highly.

---

## 6. Limitations and Bias

The most significant weakness is **genre scarcity bias**. Because most genres appear only once in the 20-song catalog, any user whose favorite genre has a single match will always see that song ranked first — regardless of whether its energy, mood, or acousticness actually fit. A classical user asking for intense, high-energy music still gets Glass Cathedrals (peaceful, energy=0.18) near the top simply because it is the only classical song. This is not a flaw in the scoring math — it is a flaw in the data. A second issue is **mood cliff matching**: moods like "chill" and "relaxed" are near-identical in feel but score the same as "chill" vs "angry" — either a full point or zero, with no partial credit for similar vibes. Finally, high-energy users have more songs clustered near their target (0.75–0.97) than low-energy users (0.18–0.42), giving high-energy profiles a structural advantage in numeric scoring.

---

## 7. Evaluation

Six user profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, and three adversarial edge cases — a user who wanted high energy but a sad mood, a user who asked for classical but intense music, and a user with perfectly average preferences across every feature. For the clean profiles, results matched intuition well. The edge cases were more revealing. Gym Hero kept appearing near the top for the Happy Pop profile even though the user wanted a happy mood — it is a pop song with matching energy, so the math pushed it up even though the vibe is wrong. It is like asking for a birthday party song and getting handed a pre-workout track. The classical-but-intense profile showed that strong energy weighting can push a rock song above a classical one, which is either honest or confusing depending on how you look at it. Weight experiments confirmed that no single configuration works perfectly for all profiles.

---

## 8. Intended Use and Non-Intended Use

**Intended use:** Classroom exploration of how content-based recommender systems work. Good for understanding weighted scoring, proximity math, and the tradeoffs between different feature weights.

**Not intended for:** Real users, real products, or any situation where the recommendations would affect someone's actual listening experience. The catalog is too small, the features are manually assigned, and there is no feedback loop to improve over time.

---

## 9. Ideas for Improvement

- **Bigger and more balanced catalog** — at least 5 songs per genre so the system has real choices to make instead of defaulting to the only match.
- **Partial mood scoring** — instead of binary match/no-match, group moods by similarity (e.g. chill/relaxed/peaceful as a cluster) so close moods get partial credit.
- **User feedback loop** — track skips and replays to adjust weights over time, so the system learns whether a particular user cares more about genre or energy.

---

## 10. Personal Reflection

The biggest learning moment was realizing that the weights are not just math — they are decisions. Every time I changed a number, I was making a statement about what matters more to a listener. When I had genre at 2.0, the system felt confident but boring. When I dropped it to 0.9, the results got more interesting but occasionally strange. There is no objectively correct weight — just tradeoffs, and that is something I did not expect going in.

Using AI tools helped a lot for moving fast. I could describe what I wanted in plain language and get working code back quickly, which meant I spent more time thinking about the results than fighting syntax. But I had to double-check things constantly — especially around edge cases. The AI gave me code that ran without errors but still produced recommendations that felt wrong when I actually read them. Running the output and asking "does this make sense?" was something the AI could not do for me.

The most surprising thing was how much the output felt like real recommendations even though the logic is just five numbers being added up. When Library Rain came back as the top chill lofi song, it genuinely felt right — not because the algorithm is smart, but because the features captured something true about how that song sounds. That gap between simple math and a result that feels meaningful is what makes recommender systems interesting.

If I extended this project, I would add a feedback loop first — even something simple like flagging songs as skipped or replayed and using that to nudge the weights over time. That one change would turn a static formula into something that actually learns, which is the core difference between this simulation and what Spotify is doing at scale.
