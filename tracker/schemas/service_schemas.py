from datetime import date
from pydantic import BaseModel, HttpUrl, Field, EmailStr


class GeniusArtist(BaseModel):
    # general
    id: int 
    name: str
    alternate_names: list[str] | None

    # social
    instagram_name: str | None
    twitter_name: str | None
    followers_count: int

    # photo
    header_photo: str = Field(alias="header_image_url")
    avatar_photo: str = Field(alias="image_url")


class SpotifyTrackDetails(BaseModel):
    danceability: float
    energy: float
    loudness: float
    tempo: int
    duration_ms: int


class SpotifyTrack(BaseModel):
    id: str
    title: str
    release_date: date
    cover_url: str
    preview_url: str | None
    explicit: bool
    details: SpotifyTrackDetails


class AllStats(BaseModel):
    genius: GeniusArtist
    spotify_tracks: list[SpotifyTrack]
    