import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio/genre attributes."""
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
    """Represents a user's musical taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Content-based music recommender using weighted feature scoring."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute a compatibility score between a user profile and a song."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        score += 1.0 - abs(song.energy - user.target_energy)
        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by compatibility score, highest first."""
        return sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        parts = []
        if song.genre == user.favorite_genre:
            parts.append("genre match (+2.0)")
        if song.mood == user.favorite_mood:
            parts.append("mood match (+1.0)")
        energy_proximity = 1.0 - abs(song.energy - user.target_energy)
        parts.append(f"energy proximity (+{energy_proximity:.2f})")
        if user.likes_acoustic and song.acousticness > 0.6:
            parts.append("acoustic match (+0.5)")
        return ", ".join(parts) if parts else "no strong match"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_proximity = 1.0 - abs(song["energy"] - user_prefs.get("energy", 0.5))
    score += energy_proximity
    reasons.append(f"energy proximity (+{energy_proximity:.2f})")

    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acoustic match (+0.5)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs; return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
