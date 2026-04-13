"""
Command line runner for the Music Recommender Simulation.
Runs multiple user profiles and prints ranked recommendations for each.
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, recommendations: list) -> None:
    """Print a formatted block of top-k recommendations for one user profile."""
    print(f"\n{'=' * 55}")
    print(f"  Profile: {label}")
    print(f"{'=' * 55}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} ({song['genre']}, {song['mood']})")
        print(f"       Score: {score:.2f}  |  {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        # --- standard profiles ---
        ("High-Energy Pop",
         {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False}),

        ("Chill Lofi (acoustic)",
         {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}),

        ("Deep Intense Rock",
         {"genre": "rock", "mood": "intense", "energy": 0.95, "likes_acoustic": False}),

        # --- adversarial / edge-case profiles ---
        ("Electronic + Peaceful (conflicting energy)",
         {"genre": "electronic", "mood": "peaceful", "energy": 0.2, "likes_acoustic": False}),

        ("Latin Festive",
         {"genre": "latin", "mood": "festive", "energy": 0.85, "likes_acoustic": False}),

        ("Blues Soulful (acoustic)",
         {"genre": "blues", "mood": "soulful", "energy": 0.45, "likes_acoustic": True}),
    ]

    for label, prefs in profiles:
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(label, recs)


if __name__ == "__main__":
    main()
