# 🎵 Music Recommender Simulation

## Project Summary

This project builds a content-based music recommender system. It reads a catalog of songs from a CSV file, compares each song's attributes against a user's taste profile, scores every song using a weighted rule set, and returns the top-k highest-scoring tracks.

Real-world platforms like Spotify combine two main strategies:
- **Collaborative filtering** — recommending songs that *other users with similar tastes* also enjoyed.
- **Content-based filtering** — recommending songs that *share attributes* (genre, tempo, mood, energy) with what a user already likes.

This simulation focuses on content-based filtering because it only requires song metadata and a single user profile, making it transparent and easy to reason about.

---

## How The System Works

### Song features

Each `Song` object stores:

| Feature | Type | Description |
|---|---|---|
| `genre` | string | Musical genre (pop, lofi, rock, jazz, …) |
| `mood` | string | Emotional tone (happy, chill, intense, romantic, …) |
| `energy` | float 0–1 | How energetic/loud the track feels |
| `tempo_bpm` | float | Beats per minute |
| `valence` | float 0–1 | Musical positivity (high = cheerful) |
| `danceability` | float 0–1 | How suitable for dancing |
| `acousticness` | float 0–1 | How acoustic (vs. electronic) the track is |

### UserProfile features

Each `UserProfile` stores the user's preferences:

| Field | Type | Description |
|---|---|---|
| `favorite_genre` | string | Preferred genre |
| `favorite_mood` | string | Preferred mood |
| `target_energy` | float 0–1 | Desired energy level |
| `likes_acoustic` | bool | Whether the user prefers acoustic sound |

### Algorithm Recipe (Scoring Rule)

For each song in the catalog, the recommender computes a **compatibility score**:

```
score = 0

if song.genre == user.favorite_genre:
    score += 2.0          # genre is the strongest signal

if song.mood == user.favorite_mood:
    score += 1.0          # mood is a secondary signal

score += 1.0 - abs(song.energy - user.target_energy)
# energy proximity: 1.0 when exact match, 0.0 when opposite ends

if user.likes_acoustic and song.acousticness > 0.6:
    score += 0.5          # bonus for acoustic preference
```

Genre match is worth twice a mood match because genre is the broadest filter listeners use. Energy proximity rewards closeness rather than just "higher is better," so a chill user is not punished for calm songs.

### Ranking Rule

After scoring every song, the list is sorted in descending order by score. The top **k** songs (default k = 5) are returned as the recommendations.

### Data flow

```
Input (User Prefs)
        |
        v
Loop over every song in songs.csv
        |
        v
score_song(user_prefs, song) → (score, reasons)
        |
        v
Sort all (song, score) pairs descending
        |
        v
Output: Top-K Recommendations
```

### Potential biases

- Genre is weighted 2x mood, so songs in a niche genre the user loves will always beat well-matched songs from any other genre — even if mood and energy are perfect.
- The catalog is tiny (20 songs) and skewed toward Western genres, so some tastes have no close match at all.
- Acoustic preference only adds a bonus; there is no penalty for non-acoustic songs, so the bias is one-directional.

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

Six user profiles were tested to evaluate the system:

| Profile | Top Result | Score | Key Finding |
|---|---|---|---|
| High-Energy Pop (genre=pop, mood=happy, energy=0.9) | Sunrise City | 3.92 | Correct — genre + mood + energy all aligned |
| Chill Lofi acoustic (genre=lofi, mood=chill, energy=0.35) | Library Rain | 4.50 | All four scoring rules fired; highest possible score |
| Deep Intense Rock (genre=rock, mood=intense, energy=0.95) | Storm Runner | 3.96 | Clear winner; ~2-point gap to #2 |
| Electronic + Peaceful, energy=0.2 (adversarial) | Pulse Protocol | 2.25 | Genre's 2.0 pts beat a near-zero energy match |
| Latin Festive | Fiesta de Colores | 4.00 | One catalog match; #2–#5 are energy-only results |
| Blues Soulful acoustic | Delta Smoke | 4.49 | Strong match on all four criteria |

**Weight-shift experiment:** Mentally doubling energy's weight for the adversarial "Electronic + Peaceful" profile would flip the top result from *Pulse Protocol* to *Moonlight Sonata Remix* — which feels more correct for a low-energy, peaceful listener. This confirms genre weight dominates too heavily when genre and energy point in opposite directions.

---

## Limitations and Risks

- The catalog has only 20 songs; niche-genre users see one strong match then fall back to energy-only results.
- Genre carries 2x the weight of mood, which can override all other signals for adversarial profiles.
- No genre similarity: blues and jazz are treated as completely unrelated categories.
- The system has no feedback loop — it recommends the same songs every session.
- Song attributes are all numbers; lyrics, language, and cultural context are invisible to the model.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

The most surprising finding was how a single two-point weight for genre can completely override a user's energy preference. Before building this, more features seemed to equal smarter recommendations. The adversarial test showed that weight balance matters far more than the number of features — a numerically correct system can still feel wrong if its priorities do not match real listening behavior.

Building even this tiny recommender made it clearer why real streaming platforms sometimes feel stuck in a loop. Once genre dominates the score, the system stops exploring, mirroring the "filter bubble" problem in real AI recommenders. Deciding how much any single feature should matter is a values decision, not a math problem — and that is where human judgment still matters most.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

