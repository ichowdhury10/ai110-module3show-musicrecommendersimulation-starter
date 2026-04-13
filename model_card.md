# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** — a content-based music recommender simulation.

---

## 2. Intended Use

VibeFinder suggests songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration only — not for real users or production deployment. It assumes every user can be described by a single, static taste profile and that song attributes captured in a CSV fully represent musical experience.

---

## 3. How the Model Works

For every song in the catalog, VibeFinder computes a compatibility score by checking four things:

1. **Genre match** — if the song's genre matches the user's favorite genre, it earns the biggest reward (2 points). Genre is treated as the strongest signal.
2. **Mood match** — if the song's mood matches the user's preferred mood, it earns 1 point.
3. **Energy proximity** — the closer the song's energy level is to the user's target energy (on a 0–1 scale), the more points it earns (up to 1 point). A song that is exactly the right energy earns the full point; a song at the opposite extreme earns 0.
4. **Acoustic bonus** — if the user prefers acoustic music and the song is highly acoustic, it gets an extra 0.5 points.

Once every song has a score, VibeFinder sorts the list from highest to lowest and returns the top results.

---

## 4. Data

The catalog contains **20 songs** stored in `data/songs.csv`. The original 10 starter songs were expanded with 10 additional tracks to cover a wider range of genres and moods:

- **Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, country, r&b, electronic, metal, folk, reggae, blues, latin
- **Moods represented:** happy, chill, intense, relaxed, focused, moody, energetic, peaceful, nostalgic, romantic, euphoric, angry, melancholic, laid-back, soulful, festive

Each song has numerical features: `energy` (0–1), `tempo_bpm`, `valence`, `danceability`, and `acousticness` (all 0–1). The dataset was generated for this simulation and does not reflect the listening habits of any real population.

---

## 5. Strengths

- **Transparent scoring:** Every recommendation comes with a plain-English explanation of exactly which features contributed and how many points each earned.
- **Works well for well-represented genres:** Users with popular genres like pop, lofi, or rock get results that clearly match their profile. Testing "High-Energy Pop" correctly surfaces *Sunrise City* first (genre + mood + energy all align).
- **Acoustic preference is additive:** The acoustic bonus correctly shifts rankings for users who prefer quieter, guitar-driven sounds without making it impossible for non-acoustic songs to appear.

---

## 6. Limitations and Bias

**Genre dominance:** Genre carries 2 points while mood carries 1 point and energy closeness carries at most 1 point. This means a genre-matching song can outrank a song that perfectly matches the user's mood and energy. For the "Electronic + Peaceful" adversarial profile, *Pulse Protocol* (electronic, euphoric, energy 0.95) ranked #1 with a score of 2.25 despite a terrible energy match — simply because it was the only electronic song in the catalog.

**Filter bubble risk:** Because genre is weighted so heavily and the catalog is small, users in niche genres (e.g., blues or latin) see one strong match followed by a drop to pure energy-proximity results. The system cannot "bridge" related genres (e.g., suggesting jazz to a blues fan).

**No genre similarity:** The model treats every genre as completely separate. It cannot recognize that a reggae fan might also enjoy latin, or that folk and country share acoustic qualities.

**Static user model:** The system has no memory. It cannot learn from skips, plays, or feedback, so it will recommend the same songs every time unless the profile changes manually.

**Tiny catalog:** With only 20 songs, many categories have just one or two entries, which limits meaningful diversity in results.

---

## 7. Evaluation

Six user profiles were tested, spanning standard and adversarial cases:

| Profile | Top Result | Observation |
|---|---|---|
| High-Energy Pop (genre=pop, mood=happy, energy=0.9) | Sunrise City (3.92) | Correct — genre + mood + near-perfect energy |
| Chill Lofi acoustic (genre=lofi, mood=chill, energy=0.35) | Library Rain (4.50) | Correct — all four scoring conditions met |
| Deep Intense Rock (genre=rock, mood=intense, energy=0.95) | Storm Runner (3.96) | Correct — only one rock song, sits clearly on top |
| Electronic + Peaceful, energy=0.2 (adversarial) | Pulse Protocol (2.25) | Genre wins despite energy=0.95 vs target=0.2 |
| Latin Festive | Fiesta de Colores (4.00) | Correct, but #2–#5 are all energy-proximity only |
| Blues Soulful acoustic | Delta Smoke (4.49) | Correct — strong match across all criteria |

The most revealing result was the adversarial "Electronic + Peaceful" profile. *Pulse Protocol* ranked #1 with an energy score of only 0.25 out of 1.0 because 2.0 genre points overwhelmed the energy penalty. This confirms that genre weight is too dominant when genre and energy point in opposite directions.

A weight-shift experiment (mentally doubling energy importance) showed it would have flipped the ranking: *Moonlight Sonata Remix* (classical, peaceful, energy=0.22) would have ranked above *Pulse Protocol*, which feels more intuitive for someone seeking peaceful, low-energy music.

---

## 8. Future Work

- **Normalize genre weight:** Reduce genre from 2.0 to 1.5 so that energy proximity plays a larger relative role, reducing the adversarial case where genre overrides everything.
- **Genre similarity graph:** Build a lookup table (e.g., blues ↔ jazz ↔ soul) so the system can give partial credit to related genres rather than treating all non-matches equally.
- **Diversity enforcement:** Add a rule that prevents the top-k results from being all the same genre, ensuring variety even when one genre dominates the scoring.
- **User feedback loop:** Track which recommended songs the user skips or replays and adjust `target_energy` and genre weights over time.

---

## 9. Personal Reflection

The biggest learning moment was seeing how a small numeric weight — just 2 points for genre versus 1 for mood — can completely control which songs appear at the top. Before building this, I assumed "more features = smarter recommendations." But the adversarial test showed that the *balance* of weights matters far more than the number of features. A system that is technically correct can still feel wrong if the priorities don't match real listening behavior.

What surprised me most was how often energy proximity alone determined the bottom half of the rankings. Once the genre-matching songs were exhausted, VibeFinder essentially became an energy-similarity engine, which means users in niche genres get a very different experience than pop or lofi fans. This mirrors a real problem in streaming platforms: users with uncommon tastes often receive recommendations that feel generic, because the model defaults to whatever universal feature (like tempo or energy) it can score.

Building even this tiny recommender made me more skeptical of "because you listened to X" explanations on real apps. The explanation sounds personal, but the underlying logic may be just as blunt as our four-line scoring function.
