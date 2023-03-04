import asyncio

from controllers.services.spotify import SpotifyAPI
from controllers.services.genius import GeniusAPI
from schemas.service_schemas import AllStats
from utils import validate_artist_names


async def get_artist(genius: GeniusAPI, spotify: SpotifyAPI, artist_name: str) -> AllStats:
    spotify_artist_id = await spotify.get_artist_id(artist_name)
    spotify_artist = await spotify.get_artist(spotify_artist_id)
    print(spotify_artist.name)
    genius_artist_id = await genius.get_artist_id(spotify_artist.name)

    artist_info_tasks = [
        genius.get_artist(genius_artist_id),
        spotify.get_artist_top_tracks(spotify_artist_id),
    ]
    stats = await asyncio.gather(*artist_info_tasks)
    all_stats = AllStats(
        genius=stats[0],
        spotify=spotify_artist,
        spotify_tracks=stats[1],
    )
    validate_artist_names(all_stats.spotify.name, all_stats.genius.name)
    return all_stats
