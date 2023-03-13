import asyncio
from pprint import pprint

from controllers.services.spotify import SpotifyAPI
from controllers.services.genius import GeniusAPI, GeniusParser, get_most_popular_words
from schemas.service_schemas import AllStats
from utils import validate_artist_names


async def get_artist(genius: GeniusAPI, spotify: SpotifyAPI, genius_parser: GeniusParser, artist_name: str) -> AllStats:
    spotify_artist_id = spotify.get_artist_id(artist_name)
    genius_artist_id = genius.get_artist_id(artist_name)
    artist_ids_tasks = [
        spotify_artist_id,
        genius_artist_id
    ]
    artist_ids_tasks = await asyncio.gather(*artist_ids_tasks)
    spotify_artist_id, genius_artist_id = artist_ids_tasks[0], artist_ids_tasks[1]
    spotify_artist = spotify.get_artist(spotify_artist_id)
    genius_artist = genius.get_artist(genius_artist_id)
    artist_tasks = [
        spotify_artist,
        genius_artist,
    ]
    artist_tasks = await asyncio.gather(*artist_tasks)
    spotify_artist, genius_artist = artist_tasks[0], artist_tasks[1]
    all_tracks_links = await genius_parser.get_track_links(genius_artist.url)

    tracks_text_tasks = []
    for track_link in all_tracks_links:
        tracks_text_tasks.append(genius_parser.parse_text(track_link))

    global_tasks = [
        spotify.get_artist_top_tracks(spotify_artist_id),
        *tracks_text_tasks
    ]
    global_tasks = await asyncio.gather(*global_tasks)
    most_popular_words = get_most_popular_words(global_tasks[1:])
    all_stats = AllStats(
        genius=genius_artist,
        spotify=spotify_artist,
        spotify_tracks=global_tasks[0],
        most_popular_words=most_popular_words
    )
    validate_artist_names(all_stats.spotify.name, all_stats.genius.name)
    return all_stats
