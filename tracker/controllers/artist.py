import asyncio
from pprint import pprint
from datetime import timedelta, datetime

from sqlalchemy import desc


from controllers.services.spotify import SpotifyAPI
from controllers.services.genius import GeniusAPI, GeniusParser, get_most_popular_words
from models.db_models import Artist
from schemas.service_schemas import AllStats
from utils import validate_artist_names


class ArtistController:
    def __init__(self, db, genius: GeniusAPI, spotify: SpotifyAPI, genius_parser: GeniusParser) -> None:
        self.db = db
        self.genius = genius
        self.spotify = spotify
        self.genius_parser = genius_parser

    def is_day_delta(self, date_query, date_db_query):
        return abs(date_query - date_db_query) <= timedelta(days=1)

    def preprocess_json(self, json: str) -> str:
        return json.replace('header_photo', 'header_image_url').replace('avatar_photo', 'image_url', 1)

    async def get_artist(self, artist_name: str) -> AllStats:
        genius_artist_id = self.genius.get_artist_id(artist_name)
        spotify_artist_id = self.spotify.get_artist_id(artist_name)
        artist_ids_tasks = [
            spotify_artist_id,
            genius_artist_id
        ]
        artist_ids_tasks = await asyncio.gather(*artist_ids_tasks)
        if (query := self.db.query(Artist).order_by(desc(Artist.parse_date)).first()) and query.genius_id == artist_ids_tasks[1]:
            if self.is_day_delta(query.parse_date, datetime.now()):
                return AllStats.parse_raw(self.preprocess_json(query.json))
            self.db.delete(query)
            self.db.commit()
        spotify_artist_id, genius_artist_id = artist_ids_tasks[0], artist_ids_tasks[1]
        spotify_artist = self.spotify.get_artist(spotify_artist_id)
        genius_artist = self.genius.get_artist(genius_artist_id)
        artist_tasks = [
            spotify_artist,
            genius_artist,
        ]
        artist_tasks = await asyncio.gather(*artist_tasks)
        spotify_artist, genius_artist = artist_tasks[0], artist_tasks[1]
        all_tracks_links = await self.genius_parser.get_track_links(genius_artist.url)

        tracks_text_tasks = []
        for track_link in all_tracks_links:
            tracks_text_tasks.append(self.genius_parser.parse_text(track_link))

        global_tasks = [
            self.spotify.get_artist_top_tracks(spotify_artist_id),
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
        artist = Artist(
            genius_id=all_stats.genius.id,
            json=str(all_stats.json())
        )
        self.db.add(artist)
        self.db.commit()
        return all_stats
